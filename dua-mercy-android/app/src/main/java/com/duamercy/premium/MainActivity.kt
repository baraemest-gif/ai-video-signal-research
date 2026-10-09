package com.duamercy.premium

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.os.Build
import android.os.Bundle
import android.text.SpannableString
import android.text.Spanned
import android.text.style.BackgroundColorSpan
import android.text.style.ForegroundColorSpan
import android.text.style.StyleSpan
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.SeekBar
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.duamercy.premium.databinding.ActivityMainBinding
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView

class MainActivity : AppCompatActivity() {
    private lateinit var b: ActivityMainBinding
    private val prefs by lazy { getSharedPreferences("dua_prefs", MODE_PRIVATE) }
    private var category = "all"
    private var fontSize = 30f
    private val rates = floatArrayOf(0.8f, 0.9f, 1.0f, 1.15f, 1.3f)

    private val textViews = mutableMapOf<Int, TextView>()
    private val cards = mutableMapOf<Int, MaterialCardView>()
    private var activeId: Int? = null

    private val notificationPermission = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { }

    private val syncReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action != DuaAudioService.ACTION_SYNC) return
            val id = intent.getIntExtra(DuaAudioService.EXTRA_ID, -1)
            val start = intent.getIntExtra(DuaAudioService.EXTRA_RANGE_START, -1)
            val end = intent.getIntExtra(DuaAudioService.EXTRA_RANGE_END, -1)
            val state = intent.getStringExtra(DuaAudioService.EXTRA_STATE) ?: DuaAudioService.STATE_RANGE
            if (id <= 0) return

            when (state) {
                DuaAudioService.STATE_START -> {
                    activeId = id
                    clearHighlights(exceptId = id)
                    showDua(id, -1, -1, true)
                }
                DuaAudioService.STATE_RANGE -> {
                    activeId = id
                    showDua(id, start, end, true)
                }
                DuaAudioService.STATE_DONE -> {
                    showDua(id, -1, -1, false)
                }
                DuaAudioService.STATE_STOP -> {
                    activeId = null
                    clearHighlights()
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        b = ActivityMainBinding.inflate(layoutInflater)
        setContentView(b.root)

        fontSize = prefs.getFloat("font_size", 30f)
        val savedRate = prefs.getFloat("speech_rate", 1.0f)
        val rateIndex = rates.indices.minByOrNull { kotlin.math.abs(rates[it] - savedRate) } ?: 2
        b.speedSeek.progress = rateIndex
        updateSpeedLabel(rateIndex)

        b.switchRepeat.isChecked = prefs.getBoolean("repeat", false)
        b.switchRepeat.setOnCheckedChangeListener { _, checked ->
            prefs.edit().putBoolean("repeat", checked).apply()
        }

        b.speedSeek.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                val idx = progress.coerceIn(rates.indices)
                prefs.edit().putFloat("speech_rate", rates[idx]).apply()
                updateSpeedLabel(idx)
            }
            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        b.btnAll.setOnClickListener { selectCategory("all") }
        b.btnFather.setOnClickListener { selectCategory("father") }
        b.btnMother.setOnClickListener { selectCategory("mother") }
        b.btnBrother.setOnClickListener { selectCategory("brother") }

        b.btnPlayAll.setOnClickListener {
            ContextCompat.startForegroundService(
                this,
                Intent(this, DuaAudioService::class.java).apply {
                    action = DuaAudioService.ACTION_PLAY_ALL
                    putExtra(DuaAudioService.EXTRA_CATEGORY, category)
                }
            )
        }

        b.btnStop.setOnClickListener {
            startService(Intent(this, DuaAudioService::class.java).apply {
                action = DuaAudioService.ACTION_STOP
            })
        }

        b.btnFont.setOnClickListener {
            fontSize = when {
                fontSize < 33f -> 36f
                fontSize < 39f -> 42f
                else -> 30f
            }
            prefs.edit().putFloat("font_size", fontSize).apply()
            render()
        }

        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) {
            notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        }

        ContextCompat.registerReceiver(
            this,
            syncReceiver,
            IntentFilter(DuaAudioService.ACTION_SYNC),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )

        render()
    }

    private fun selectCategory(value: String) {
        category = value
        render()
    }

    private fun updateSpeedLabel(index: Int) {
        b.speedLabel.text = "سرعة الصوت: " + rates[index] + "×"
    }

    private fun render() {
        b.duaList.removeAllViews()
        textViews.clear()
        cards.clear()

        DuaRepository.byCategory(category).forEach { item ->
            val card = makeCard(item)
            cards[item.id] = card
            b.duaList.addView(card)
        }

        val sizeLabel = when {
            fontSize >= 40f -> "الخط: كبير جداً"
            fontSize >= 35f -> "الخط: كبير"
            else -> "تكبير الخط"
        }
        b.btnFont.text = sizeLabel
        b.countLabel.text = DuaRepository.byCategory(category).size.toString() + " دعاء"

        activeId?.let { id ->
            if (textViews.containsKey(id)) showDua(id, -1, -1, false)
        }
    }

    private fun makeCard(item: DuaItem): MaterialCardView {
        val card = MaterialCardView(this).apply {
            radius = 22f
            strokeWidth = 1
            setStrokeColor(Color.parseColor("#D9B66E"))
            setCardBackgroundColor(Color.parseColor("#171027"))
            val lp = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
            lp.setMargins(0, 0, 0, 18)
            layoutParams = lp
        }

        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(28, 24, 28, 24)
        }

        val title = TextView(this).apply {
            text = item.title
            textSize = 17f
            setTextColor(Color.parseColor("#E879F9"))
            gravity = Gravity.END
        }

        val textView = TextView(this).apply {
            text = item.text
            textSize = fontSize
            setTextColor(Color.parseColor("#FFF8FF"))
            gravity = Gravity.END
            textDirection = TextView.TEXT_DIRECTION_RTL
            setLineSpacing(10f, 1.22f)
            setPadding(0, 16, 0, 16)
        }
        textViews[item.id] = textView

        val source = TextView(this).apply {
            text = item.source
            textSize = 13f
            setTextColor(Color.parseColor("#D9B66E"))
            gravity = Gravity.END
        }

        val play = MaterialButton(this).apply {
            text = "▶ استماع"
            setOnClickListener {
                ContextCompat.startForegroundService(
                    this@MainActivity,
                    Intent(this@MainActivity, DuaAudioService::class.java).apply {
                        action = DuaAudioService.ACTION_PLAY_ONE
                        putExtra(DuaAudioService.EXTRA_ID, item.id)
                    }
                )
            }
        }

        box.addView(title)
        box.addView(textView)
        box.addView(source)
        box.addView(play)
        card.addView(box)
        return card
    }

    private fun showDua(id: Int, start: Int, end: Int, scroll: Boolean) {
        val item = DuaRepository.byId(id) ?: return
        val tv = textViews[id] ?: return

        val span = SpannableString(item.text)
        if (start >= 0 && end > start && start < item.text.length) {
            val safeEnd = end.coerceAtMost(item.text.length)
            span.setSpan(
                BackgroundColorSpan(Color.parseColor("#55E879F9")),
                start,
                safeEnd,
                Spanned.SPAN_EXCLUSIVE_EXCLUSIVE
            )
            span.setSpan(
                ForegroundColorSpan(Color.parseColor("#D9B66E")),
                start,
                safeEnd,
                Spanned.SPAN_EXCLUSIVE_EXCLUSIVE
            )
            span.setSpan(
                StyleSpan(Typeface.BOLD),
                start,
                safeEnd,
                Spanned.SPAN_EXCLUSIVE_EXCLUSIVE
            )
        }
        tv.text = span

        cards[id]?.apply {
            strokeWidth = 3
            setStrokeColor(Color.parseColor("#E879F9"))
        }

        if (scroll) scrollToCard(id)
    }

    private fun clearHighlights(exceptId: Int? = null) {
        textViews.forEach { (id, tv) ->
            if (id != exceptId) {
                DuaRepository.byId(id)?.let { tv.text = it.text }
            }
        }
        cards.forEach { (id, card) ->
            if (id != exceptId) {
                card.strokeWidth = 1
                card.setStrokeColor(Color.parseColor("#D9B66E"))
            }
        }
    }

    private fun scrollToCard(id: Int) {
        val card = cards[id] ?: return
        b.mainScroll.post {
            val target = (b.duaList.top + card.top - 90).coerceAtLeast(0)
            if (kotlin.math.abs(b.mainScroll.scrollY - target) > 20) {
                b.mainScroll.smoothScrollTo(0, target)
            }
        }
    }

    override fun onDestroy() {
        runCatching { unregisterReceiver(syncReceiver) }
        super.onDestroy()
    }
}
