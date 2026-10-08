package com.adhan.premium

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import java.time.Instant
import java.time.LocalDate

object PrayerScheduler {
    fun scheduleMonth(context: Context, latitude: Double, longitude: Double, method: String, hanafi: Boolean) {
        val alarmManager = context.getSystemService(AlarmManager::class.java)
        val now = Instant.now()
        for (offset in 0..30) {
            val date = LocalDate.now().plusDays(offset.toLong())
            val day = PrayerEngine.calculate(latitude, longitude, date, method, hanafi)
            day.adhanOnly().entries.forEachIndexed { index, entry ->
                val at = entry.value
                if (at.isAfter(now.plusSeconds(20))) {
                    val intent = Intent(context, AlarmReceiver::class.java).apply {
                        putExtra("prayer", entry.key)
                        putExtra("when", at.toEpochMilli())
                    }
                    val requestCode = (date.toEpochDay().hashCode() * 10) + index
                    val pi = PendingIntent.getBroadcast(
                        context, requestCode, intent,
                        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
                    )
                    val time = at.toEpochMilli()
                    if (Build.VERSION.SDK_INT >= 31 && !alarmManager.canScheduleExactAlarms()) {
                        alarmManager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, time, pi)
                    } else {
                        alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, time, pi)
                    }
                }
            }
        }
    }
}
