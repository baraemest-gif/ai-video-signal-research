package com.alarm.premium

import android.content.Intent
import android.os.Bundle
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity
import com.alarm.premium.databinding.ActivityAlarmRingBinding
import java.time.LocalTime
import java.time.format.DateTimeFormatter

class AlarmRingActivity : AppCompatActivity() {
    private lateinit var b: ActivityAlarmRingBinding
    private var alarmId = 0
    private var label = "المنبّه"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON or
                WindowManager.LayoutParams.FLAG_ALLOW_LOCK_WHILE_SCREEN_ON
        )
        b = ActivityAlarmRingBinding.inflate(layoutInflater)
        setContentView(b.root)

        alarmId = intent.getIntExtra("alarm_id", 0)
        label = intent.getStringExtra("label") ?: "المنبّه"
        b.ringLabel.text = label
        b.ringTime.text = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"))

        b.btnDismiss.setOnClickListener {
            stopAlarm()
            finishAndRemoveTask()
        }

        b.btnSnooze.setOnClickListener {
            AlarmScheduler.snooze(this, alarmId, label, 10)
            stopAlarm()
            finishAndRemoveTask()
        }
    }

    private fun stopAlarm() {
        startService(Intent(this, AlarmService::class.java).apply { action = AlarmService.ACTION_STOP })
    }

    override fun onBackPressed() {
        // Prevent accidental dismissal with back button.
    }
}
