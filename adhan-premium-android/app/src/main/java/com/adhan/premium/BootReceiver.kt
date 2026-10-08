package com.adhan.premium

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent?) {
        val p = context.getSharedPreferences("adhan_prefs", Context.MODE_PRIVATE)
        val lat = p.getString("lat", "40.4168")!!.toDoubleOrNull() ?: 40.4168
        val lon = p.getString("lon", "-3.7038")!!.toDoubleOrNull() ?: -3.7038
        val method = p.getString("method", "Muslim World League") ?: "Muslim World League"
        val hanafi = p.getBoolean("hanafi", false)
        PrayerScheduler.scheduleMonth(context, lat, lon, method, hanafi)
    }
}
