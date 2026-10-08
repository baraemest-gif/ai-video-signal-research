package com.alarm.premium

import android.Manifest
import android.app.AlarmManager
import android.app.TimePickerDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.alarm.premium.databinding.ActivityMainBinding
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView
import com.google.android.material.switchmaterial.SwitchMaterial
import java.util.Calendar
import java.util.Locale

class MainActivity : AppCompatActivity() {
    private lateinit var b: ActivityMainBinding
    private var alarms = mutableListOf<AlarmModel>()
    private val prefs by lazy { getSharedPreferences("alarm_prefs", MODE_PRIVATE) }

    private val soundPicker = registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            try { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) } catch (_: Throwable) {}
            prefs.edit().putString("custom_sound", uri.toString()).apply()
            b.soundValue.text = "🎵 صوت مخصص محفوظ"
        }
    }

    private val notificationPermission = registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        b = ActivityMainBinding.inflate(layoutInflater)
        setContentView(b.root)

        b.soundValue.text = if (prefs.getString("custom_sound", null).isNullOrBlank()) {
            "الصوت الافتراضي للنظام"
        } else "🎵 صوت مخصص محفوظ"

        b.btnAddAlarm.setOnClickListener { pickTime() }
        b.btnSound.setOnClickListener { soundPicker.launch(arrayOf("audio/*")) }
        b.btnExact.setOnClickListener { requestExactAlarmAccess() }

        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)

        render()
    }

    override fun onResume() {
        super.onResume()
        render()
    }

    private fun pickTime() {
        val now = Calendar.getInstance()
        TimePickerDialog(
            this,
            { _, hour, minute -> askLabel(hour, minute) },
            now.get(Calendar.HOUR_OF_DAY),
            now.get(Calendar.MINUTE),
            true
        ).show()
    }

    private fun askLabel(hour: Int, minute: Int) {
        val input = EditText(this).apply {
            hint = "اسم المنبّه"
            setText("المنبّه")
        }
        AlertDialog.Builder(this)
            .setTitle("اسم المنبّه")
            .setView(input)
            .setPositiveButton("التالي") { _, _ ->
                chooseDays(hour, minute, input.text.toString().trim().ifBlank { "المنبّه" })
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun chooseDays(hour: Int, minute: Int, label: String) {
        val names = arrayOf("الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت")
        val checked = BooleanArray(7)
        AlertDialog.Builder(this)
            .setTitle("أيام التكرار · اتركها فارغة لمرة واحدة")
            .setMultiChoiceItems(names, checked) { _, which, isChecked -> checked[which] = isChecked }
            .setPositiveButton("حفظ") { _, _ ->
                val days = mutableSetOf<Int>()
                checked.forEachIndexed { index, value ->
                    if (value) days += Calendar.SUNDAY + index
                }
                val id = ((System.currentTimeMillis() / 1000L) % 2_000_000_000L).toInt()
                val alarm = AlarmModel(id, hour, minute, label, days, true)
                alarms = AlarmStore.load(this)
                alarms += alarm
                AlarmStore.save(this, alarms)
                AlarmScheduler.schedule(this, alarm)
                render()
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun render() {
        alarms = AlarmStore.load(this)
        b.alarmList.removeAllViews()
        b.emptyText.visibility = if (alarms.isEmpty()) View.VISIBLE else View.GONE

        alarms.sortedWith(compareBy<AlarmModel> { it.hour }.thenBy { it.minute }).forEach { alarm ->
            val card = MaterialCardView(this).apply {
                radius = 18f
                strokeWidth = 1
                setStrokeColor(Color.parseColor("#D9B66E"))
                setCardBackgroundColor(Color.parseColor("#171027"))
                val lp = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
                lp.setMargins(0, 0, 0, 16)
                layoutParams = lp
            }

            val box = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setPadding(28, 22, 28, 22)
            }

            val top = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = android.view.Gravity.CENTER_VERTICAL
            }

            val info = TextView(this).apply {
                text = String.format(Locale.US, "%02d:%02d  ·  %s", alarm.hour, alarm.minute, alarm.label)
                textSize = 23f
                setTextColor(Color.parseColor("#FFF8FF"))
                setTypeface(typeface, android.graphics.Typeface.BOLD)
                layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
            }

            val toggle = SwitchMaterial(this).apply {
                isChecked = alarm.enabled
                setOnCheckedChangeListener { _, checked ->
                    val all = AlarmStore.load(this@MainActivity)
                    val idx = all.indexOfFirst { it.id == alarm.id }
                    if (idx >= 0) {
                        all[idx] = all[idx].copy(enabled = checked)
                        AlarmStore.save(this@MainActivity, all)
                        if (checked) AlarmScheduler.schedule(this@MainActivity, all[idx])
                        else AlarmScheduler.cancel(this@MainActivity, alarm.id)
                    }
                }
            }
            top.addView(info)
            top.addView(toggle)
            box.addView(top)

            val repeat = TextView(this).apply {
                text = repeatText(alarm)
                setTextColor(Color.parseColor("#C9BDD6"))
                textSize = 14f
                setPadding(0, 8, 0, 8)
            }
            box.addView(repeat)

            val delete = MaterialButton(this).apply {
                text = "🗑 حذف"
                setOnClickListener {
                    AlarmScheduler.cancel(this@MainActivity, alarm.id)
                    val all = AlarmStore.load(this@MainActivity).filterNot { it.id == alarm.id }
                    AlarmStore.save(this@MainActivity, all)
                    render()
                }
            }
            box.addView(delete)
            card.addView(box)
            b.alarmList.addView(card)
        }
    }

    private fun repeatText(alarm: AlarmModel): String {
        if (alarm.days.isEmpty()) return "مرة واحدة"
        val short = mapOf(
            Calendar.SUNDAY to "ح",
            Calendar.MONDAY to "ن",
            Calendar.TUESDAY to "ث",
            Calendar.WEDNESDAY to "ر",
            Calendar.THURSDAY to "خ",
            Calendar.FRIDAY to "ج",
            Calendar.SATURDAY to "س"
        )
        return "يتكرر: " + alarm.days.sorted().joinToString(" · ") { short[it] ?: "?" }
    }

    private fun requestExactAlarmAccess() {
        if (Build.VERSION.SDK_INT >= 31) {
            val am = getSystemService(AlarmManager::class.java)
            if (!am.canScheduleExactAlarms()) {
                startActivity(Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM).apply {
                    data = Uri.parse("package:$packageName")
                })
                return
            }
        }
        AlarmScheduler.scheduleAll(this)
        Toast.makeText(this, "المنبّهات الدقيقة مفعّلة", Toast.LENGTH_SHORT).show()
    }
}
