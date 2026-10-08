package com.adhan.premium

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.net.Uri
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat

class AdhanService : Service() {
    private var player: MediaPlayer? = null
    private var wakeLock: PowerManager.WakeLock? = null

    override fun onCreate() {
        super.onCreate()
        getSystemService(NotificationManager::class.java).createNotificationChannel(
            NotificationChannel(CHANNEL, "Adhan", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "Prayer time adhan"
                setSound(null, null)
            }
        )
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_STOP -> stopNow()
            ACTION_PLAY -> play(intent.getStringExtra(EXTRA_PRAYER) ?: "الصلاة")
        }
        return START_NOT_STICKY
    }

    private fun play(prayer: String) {
        stopPlayerOnly()
        val stopPi = PendingIntent.getService(
            this, 91, Intent(this, AdhanService::class.java).apply { action = ACTION_STOP },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val openPi = PendingIntent.getActivity(
            this, 92, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        startForeground(
            ADHAN_NOTIFICATION,
            NotificationCompat.Builder(this, CHANNEL)
                .setSmallIcon(R.drawable.ic_mosque)
                .setContentTitle("حان وقت $prayer")
                .setContentText("Adhan Premium")
                .setContentIntent(openPi)
                .setOngoing(true)
                .addAction(0, "إيقاف", stopPi)
                .build()
        )

        val p = getSharedPreferences("adhan_prefs", MODE_PRIVATE)
        val custom = p.getString("selected_audio_uri", null)
        val uri = if (custom.isNullOrBlank()) Uri.parse(MuezzinCatalog.DEFAULT_AUDIO) else Uri.parse(custom)

        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AdhanPremium:Playback").apply {
                setReferenceCounted(false)
                acquire(10 * 60 * 1000L)
            }

        player = MediaPlayer().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            setDataSource(this@AdhanService, uri)
            setOnPreparedListener { it.start() }
            setOnCompletionListener { stopNow() }
            setOnErrorListener { _, _, _ -> stopNow(); true }
            prepareAsync()
        }
    }

    private fun stopPlayerOnly() {
        try { player?.stop() } catch (_: Throwable) {}
        player?.release()
        player = null
        if (wakeLock?.isHeld == true) wakeLock?.release()
        wakeLock = null
    }

    private fun stopNow() {
        stopPlayerOnly()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onDestroy() {
        stopPlayerOnly()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val ACTION_PLAY = "com.adhan.premium.PLAY"
        const val ACTION_STOP = "com.adhan.premium.STOP"
        const val EXTRA_PRAYER = "prayer"
        private const val CHANNEL = "adhan_prayer"
        private const val ADHAN_NOTIFICATION = 8801
    }
}
