package com.alarm.premium

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import java.util.Calendar

object AlarmScheduler {
    fun schedule(context: Context, alarm: AlarmModel) {
        cancel(context, alarm.id)
        if (!alarm.enabled) return

        val am = context.getSystemService(AlarmManager::class.java)
        val trigger = nextTrigger(alarm)
        val pi = PendingIntent.getBroadcast(
            context,
            alarm.id,
            Intent(context, AlarmReceiver::class.java).apply {
                putExtra("alarm_id", alarm.id)
                putExtra("label", alarm.label)
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        if (Build.VERSION.SDK_INT >= 31 && !am.canScheduleExactAlarms()) {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pi)
        } else {
            am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pi)
        }
    }

    fun scheduleAll(context: Context) {
        AlarmStore.load(context).filter { it.enabled }.forEach { schedule(context, it) }
    }

    fun cancel(context: Context, id: Int) {
        val am = context.getSystemService(AlarmManager::class.java)
        val pi = PendingIntent.getBroadcast(
            context,
            id,
            Intent(context, AlarmReceiver::class.java),
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pi != null) am.cancel(pi)
    }

    fun snooze(context: Context, id: Int, label: String, minutes: Int = 10) {
        val am = context.getSystemService(AlarmManager::class.java)
        val trigger = System.currentTimeMillis() + minutes * 60_000L
        val requestCode = id + 500_000
        val pi = PendingIntent.getBroadcast(
            context,
            requestCode,
            Intent(context, AlarmReceiver::class.java).apply {
                putExtra("alarm_id", id)
                putExtra("label", label)
                putExtra("snooze", true)
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        if (Build.VERSION.SDK_INT >= 31 && !am.canScheduleExactAlarms()) {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pi)
        } else {
            am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pi)
        }
    }

    private fun nextTrigger(alarm: AlarmModel): Long {
        val now = Calendar.getInstance()
        val base = Calendar.getInstance().apply {
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
            set(Calendar.HOUR_OF_DAY, alarm.hour)
            set(Calendar.MINUTE, alarm.minute)
        }

        if (alarm.days.isEmpty()) {
            if (base.timeInMillis <= now.timeInMillis) base.add(Calendar.DAY_OF_YEAR, 1)
            return base.timeInMillis
        }

        for (offset in 0..7) {
            val candidate = base.clone() as Calendar
            candidate.add(Calendar.DAY_OF_YEAR, offset)
            val validDay = alarm.days.contains(candidate.get(Calendar.DAY_OF_WEEK))
            if (validDay && candidate.timeInMillis > now.timeInMillis + 1_000L) return candidate.timeInMillis
        }

        base.add(Calendar.DAY_OF_YEAR, 7)
        return base.timeInMillis
    }
}
