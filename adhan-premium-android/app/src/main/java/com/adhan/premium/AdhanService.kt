package com.adhan.premium

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.media.AudioAttributes
import android.media.AudioDeviceInfo
import android.media.AudioManager
import android.media.MediaPlayer
import android.net.Uri
import android.os.Build
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

        val prefs = getSharedPreferences("adhan_prefs", MODE_PRIVATE)
        val custom = prefs.getString("selected_audio_uri", null)
        val uri = if (custom.isNullOrBlank()) Uri.parse(MuezzinCatalog.DEFAULT_AUDIO) else Uri.parse(custom)
        val routeMode = prefs.getString("audio_route", ROUTE_AUTO) ?: ROUTE_AUTO
        val route = resolveOutput(routeMode)
        val headphoneOutput = route?.let { isHeadphone(it) } == true

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
                .setContentText("Adhan Premium · " + routeDescription(routeMode, headphoneOutput))
                .setContentIntent(openPi)
                .setOngoing(true)
                .addAction(0, "إيقاف", stopPi)
                .build()
        )

        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AdhanPremium:Playback").apply {
                setReferenceCounted(false)
                acquire(10 * 60 * 1000L)
            }

        player = MediaPlayer().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(if (headphoneOutput) AudioAttributes.USAGE_MEDIA else AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            route?.let { setPreferredDevice(it) }
            setDataSource(this@AdhanService, uri)
            setOnPreparedListener { it.start() }
            setOnCompletionListener { stopNow() }
            setOnErrorListener { _, _, _ -> stopNow(); true }
            prepareAsync()
        }
    }

    private fun resolveOutput(mode: String): AudioDeviceInfo? {
        val am = getSystemService(AudioManager::class.java)
        val outputs = am.getDevices(AudioManager.GET_DEVICES_OUTPUTS).toList()
        val headphone = outputs.firstOrNull { isHeadphone(it) }
        val speaker = outputs.firstOrNull { it.type == AudioDeviceInfo.TYPE_BUILTIN_SPEAKER }

        return when (mode) {
            ROUTE_HEADPHONES -> headphone ?: speaker
            ROUTE_SPEAKER -> speaker ?: headphone
            else -> headphone ?: speaker
        }
    }

    private fun isHeadphone(device: AudioDeviceInfo): Boolean {
        return when (device.type) {
            AudioDeviceInfo.TYPE_WIRED_HEADSET,
            AudioDeviceInfo.TYPE_WIRED_HEADPHONES,
            AudioDeviceInfo.TYPE_BLUETOOTH_A2DP,
            AudioDeviceInfo.TYPE_BLUETOOTH_SCO,
            AudioDeviceInfo.TYPE_USB_DEVICE,
            AudioDeviceInfo.TYPE_USB_HEADSET -> true
            else -> if (Build.VERSION.SDK_INT >= 31) {
                device.type == AudioDeviceInfo.TYPE_BLE_HEADSET ||
                    device.type == AudioDeviceInfo.TYPE_BLE_SPEAKER
            } else false
        }
    }

    private fun routeDescription(mode: String, headphoneOutput: Boolean): String = when {
        headphoneOutput -> "🎧 السماعات"
        mode == ROUTE_SPEAKER -> "🔊 مكبر الهاتف"
        mode == ROUTE_HEADPHONES -> "🔊 لا توجد سماعات · الهاتف"
        else -> "🔊 الهاتف"
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

        const val ROUTE_AUTO = "AUTO"
        const val ROUTE_HEADPHONES = "HEADPHONES"
        const val ROUTE_SPEAKER = "SPEAKER"

        private const val CHANNEL = "adhan_prayer"
        private const val ADHAN_NOTIFICATION = 8801
    }
}
