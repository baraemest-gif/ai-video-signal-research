package com.adhan.premium

import android.Manifest
import android.app.AlarmManager
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.widget.EditText
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.adhan.premium.databinding.ActivityMainBinding
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import java.time.Duration
import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Locale

class MainActivity : AppCompatActivity() {
    private lateinit var b: ActivityMainBinding
    private val prefs by lazy { getSharedPreferences("adhan_prefs", MODE_PRIVATE) }
    private val locationClient by lazy { LocationServices.getFusedLocationProviderClient(this) }
    private val handler = Handler(Looper.getMainLooper())
    private var latitude = 40.4168
    private var longitude = -3.7038
    private var pendingName = "مؤذن من اختياري"

    private val audioPicker = registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            try { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) } catch (_: Throwable) {}
            prefs.edit().putString("selected_audio_uri", uri.toString()).putString("muezzin", pendingName).apply()
            b.muezzinValue.text = pendingName
            Toast.makeText(this, "تم حفظ صوت المؤذن", Toast.LENGTH_SHORT).show()
        }
    }

    private val locationPermission = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { grants ->
        if (grants.values.any { it }) updateLocation()
    }

    private val notificationPermission = registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        b = ActivityMainBinding.inflate(layoutInflater)
        setContentView(b.root)
        latitude = prefs.getString("lat", "40.4168")!!.toDoubleOrNull() ?: 40.4168
        longitude = prefs.getString("lon", "-3.7038")!!.toDoubleOrNull() ?: -3.7038
        b.muezzinValue.text = prefs.getString("muezzin", MuezzinCatalog.DEFAULT_ID)
        wireUi()
        requestNeededPermissions()
        refreshTimes()
        handler.post(ticker)
    }

    private fun wireUi() {
        b.btnLocation.setOnClickListener { if (hasLocation()) updateLocation() else requestLocation() }
        b.btnMethod.setOnClickListener { chooseMethod() }
        b.btnMuezzin.setOnClickListener { chooseMuezzin() }
        b.btnCustom.setOnClickListener { addCustomMuezzin() }
        b.btnExactAlarm.setOnClickListener { requestExactAlarmAccess() }
        b.btnTest.setOnClickListener {
            ContextCompat.startForegroundService(
                this,
                Intent(this, AdhanService::class.java).apply {
                    action = AdhanService.ACTION_PLAY
                    putExtra(AdhanService.EXTRA_PRAYER, "تجربة الأذان")
                }
            )
        }
    }

    private fun requestNeededPermissions() {
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        if (!hasLocation()) requestLocation() else updateLocation()
    }

    private fun hasLocation(): Boolean =
        ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED

    private fun requestLocation() {
        locationPermission.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
    }

    private fun updateLocation() {
        if (!hasLocation()) return
        try {
            val cts = CancellationTokenSource()
            locationClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, cts.token)
                .addOnSuccessListener { loc ->
                    if (loc != null) {
                        latitude = loc.latitude
                        longitude = loc.longitude
                        prefs.edit().putString("lat", latitude.toString()).putString("lon", longitude.toString()).apply()
                        b.locationValue.text = "GPS: %.4f, %.4f".format(Locale.US, latitude, longitude)
                        refreshTimes()
                    }
                }
        } catch (_: SecurityException) {}
    }

    private fun chooseMethod() {
        val current = prefs.getString("method", "Muslim World League") ?: "Muslim World League"
        val checked = PrayerEngine.methods.indexOf(current).coerceAtLeast(0)
        AlertDialog.Builder(this)
            .setTitle("طريقة حساب مواقيت الصلاة")
            .setSingleChoiceItems(PrayerEngine.methods, checked) { d, which ->
                prefs.edit().putString("method", PrayerEngine.methods[which]).apply()
                d.dismiss()
                refreshTimes()
            }
            .setNeutralButton("Asr: Shafi / Hanafi") { _, _ -> toggleMadhab() }
            .show()
    }

    private fun toggleMadhab() {
        val hanafi = !prefs.getBoolean("hanafi", false)
        prefs.edit().putBoolean("hanafi", hanafi).apply()
        Toast.makeText(this, if (hanafi) "العصر: حنفي" else "العصر: شافعي", Toast.LENGTH_SHORT).show()
        refreshTimes()
    }

    private fun chooseMuezzin() {
        val current = prefs.getString("muezzin", MuezzinCatalog.DEFAULT_ID) ?: MuezzinCatalog.DEFAULT_ID
        val checked = MuezzinCatalog.names.indexOf(current).coerceAtLeast(0)
        AlertDialog.Builder(this)
            .setTitle("اختر المؤذن")
            .setSingleChoiceItems(MuezzinCatalog.names, checked) { d, which ->
                val name = MuezzinCatalog.names[which]
                d.dismiss()
                if (name == MuezzinCatalog.DEFAULT_ID) {
                    prefs.edit().remove("selected_audio_uri").putString("muezzin", name).apply()
                    b.muezzinValue.text = name
                } else if (name == "مؤذن من اختياري") {
                    addCustomMuezzin()
                } else {
                    pendingName = name
                    Toast.makeText(this, "اختر تسجيل الأذان لـ $name", Toast.LENGTH_LONG).show()
                    audioPicker.launch(arrayOf("audio/*"))
                }
            }.show()
    }

    private fun addCustomMuezzin() {
        val input = EditText(this).apply { hint = "اسم المؤذن" }
        AlertDialog.Builder(this)
            .setTitle("إضافة مؤذن من اختياري")
            .setView(input)
            .setPositiveButton("اختيار ملف الصوت") { _, _ ->
                pendingName = input.text.toString().trim().ifBlank { "مؤذن من اختياري" }
                audioPicker.launch(arrayOf("audio/*"))
            }
            .setNegativeButton("إلغاء", null)
            .show()
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
        Toast.makeText(this, "المنبهات الدقيقة مفعّلة", Toast.LENGTH_SHORT).show()
        schedule()
    }

    private fun refreshTimes() {
        val method = prefs.getString("method", "Muslim World League") ?: "Muslim World League"
        val hanafi = prefs.getBoolean("hanafi", false)
        val day = PrayerEngine.calculate(latitude, longitude, LocalDate.now(), method, hanafi)
        val zone = ZoneId.systemDefault()
        val fmt = DateTimeFormatter.ofPattern("HH:mm")
        fun f(i: Instant) = fmt.format(i.atZone(zone))

        b.timeFajr.text = f(day.fajr)
        b.timeSunrise.text = f(day.sunrise)
        b.timeDhuhr.text = f(day.dhuhr)
        b.timeAsr.text = f(day.asr)
        b.timeMaghrib.text = f(day.maghrib)
        b.timeIsha.text = f(day.isha)
        b.methodValue.text = "$method · " + if (hanafi) "Hanafi" else "Shafi"
        if (b.locationValue.text.isNullOrBlank()) b.locationValue.text = "Madrid · %.4f, %.4f".format(Locale.US, latitude, longitude)
        updateNextPrayer()
        schedule()
    }

    private fun schedule() {
        val method = prefs.getString("method", "Muslim World League") ?: "Muslim World League"
        val hanafi = prefs.getBoolean("hanafi", false)
        PrayerScheduler.scheduleMonth(this, latitude, longitude, method, hanafi)
    }

    private fun updateNextPrayer() {
        val method = prefs.getString("method", "Muslim World League") ?: "Muslim World League"
        val hanafi = prefs.getBoolean("hanafi", false)
        val now = Instant.now()
        var day = PrayerEngine.calculate(latitude, longitude, LocalDate.now(), method, hanafi)
        var next = day.adhanOnly().entries.firstOrNull { it.value.isAfter(now) }
        if (next == null) {
            day = PrayerEngine.calculate(latitude, longitude, LocalDate.now().plusDays(1), method, hanafi)
            next = day.adhanOnly().entries.first()
        }
        val d = Duration.between(now, next.value)
        val h = d.toHours()
        val m = d.minusHours(h).toMinutes()
        b.nextPrayer.text = next.key + " · بعد " + h + "س " + m + "د"
    }

    private val ticker = object : Runnable {
        override fun run() {
            updateNextPrayer()
            handler.postDelayed(this, 30_000)
        }
    }

    override fun onDestroy() {
        handler.removeCallbacks(ticker)
        super.onDestroy()
    }
}
