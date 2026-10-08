package com.alarm.premium

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.content.ContextCompat

class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val id = intent.getIntExtra("alarm_id", 0)
        val label = intent.getStringExtra("label") ?: "المنبّه"
        val snooze = intent.getBooleanExtra("snooze", false)

        ContextCompat.startForegroundService(
            context,
            Intent(context, AlarmService::class.java).apply {
                action = AlarmService.ACTION_START
                putExtra("alarm_id", id)
                putExtra("label", label)
            }
        )

        if (!snooze) {
            val alarm = AlarmStore.get(context, id)
            if (alarm != null) {
                if (alarm.days.isEmpty()) {
                    AlarmStore.updateEnabled(context, id, false)
                } else {
                    AlarmScheduler.schedule(context, alarm)
                }
            }
        }
    }
}
