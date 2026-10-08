package com.alarm.premium

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.net.Uri
import android.os.IBinder
import android.os.PowerManager
import android.os.VibrationEffect
import android.os.Vibrator
import androidx.core.app.NotificationCompat

class AlarmService : Service() {
    private var player: MediaPlayer? = null
    private var vibrator: Vibrator? = null
    private var wakeLock: PowerManager.WakeLock? = null

    override fun onCreate() {
        super.onCreate()
        getSystemService(NotificationManager::class.java).createNotificationChannel(
            NotificationChannel(CHANNEL, "Alarm Premium", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "Alarm ringing"
                setSound(null, null)
                enableVibration(false)
            }
        )
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_STOP -> stopNow()
            ACTION_START -> ring(
                intent.getIntExtra("alarm_id", 0),
                intent.getStringExtra("label") ?: "المنبّه"
            )
        }
        return START_NOT_STICKY
    }

    private fun ring(id: Int, label: String) {
        stopMediaOnly()

        val fullScreen = PendingIntent.getActivity(
            this,
            id + 900_000,
            Intent(this, AlarmRingActivity::class.java).apply {
                putExtra("alarm_id", id)
                putExtra("label", label)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val stopPi = PendingIntent.getService(
            this,
            id + 910_000,
            Intent(this, AlarmService::class.java).apply { action = ACTION_STOP },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        startForeground(
            NOTIFICATION_ID,
            NotificationCompat.Builder(this, CHANNEL)
                .setSmallIcon(R.drawable.ic_alarm)
                .setContentTitle(label)
                .setContentText("Alarm Premium · حان وقت المنبّه")
                .setPriority(NotificationCompat.PRIORITY_MAX)
                .setCategory(NotificationCompat.CATEGORY_ALARM)
                .setOngoing(true)
                .setFullScreenIntent(fullScreen, true)
                .setContentIntent(fullScreen)
                .addAction(0, "إيقاف", stopPi)
                .build()
        )

        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AlarmPremium:Ringing").apply {
                setReferenceCounted(false)
                acquire(15 * 60 * 1000L)
            }

        val prefs = getSharedPreferences("alarm_prefs", MODE_PRIVATE)
        val custom = prefs.getString("custom_sound", null)
        val uri = if (custom.isNullOrBlank()) {
            RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE)
        } else Uri.parse(custom)

        player = MediaPlayer().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            isLooping = true
            setDataSource(this@AlarmService, uri)
            setOnPreparedListener { it.start() }
            setOnErrorListener { _, _, _ -> stopNow(); true }
            prepareAsync()
        }

        vibrator = getSystemService(Vibrator::class.java)
        vibrator?.vibrate(
            VibrationEffect.createWaveform(longArrayOf(0, 700, 350, 700, 350), 0)
        )

        try { fullScreen.send() } catch (_: Throwable) {}
    }

    private fun stopMediaOnly() {
        try { player?.stop() } catch (_: Throwable) {}
        player?.release()
        player = null
        vibrator?.cancel()
        vibrator = null
        if (wakeLock?.isHeld == true) wakeLock?.release()
        wakeLock = null
    }

    private fun stopNow() {
        stopMediaOnly()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onDestroy() {
        stopMediaOnly()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val ACTION_START = "com.alarm.premium.START"
        const val ACTION_STOP = "com.alarm.premium.STOP"
        private const val CHANNEL = "alarm_premium_ring"
        private const val NOTIFICATION_ID = 7401
    }
}
