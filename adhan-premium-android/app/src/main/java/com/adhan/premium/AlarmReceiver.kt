package com.adhan.premium

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.content.ContextCompat

class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val prayer = intent.getStringExtra("prayer") ?: "الصلاة"
        ContextCompat.startForegroundService(
            context,
            Intent(context, AdhanService::class.java).apply {
                action = AdhanService.ACTION_PLAY
                putExtra(AdhanService.EXTRA_PRAYER, prayer)
            }
        )
    }
}
