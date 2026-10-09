package com.duamercy.premium

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.media.AudioAttributes
import android.os.Bundle
import android.os.IBinder
import android.os.PowerManager
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.core.app.NotificationCompat
import java.util.Locale

class DuaAudioService : Service(), TextToSpeech.OnInitListener {
    private var tts: TextToSpeech? = null
    private var ready = false
    private var queue: List<DuaItem> = emptyList()
    private var index = 0
    private var wakeLock: PowerManager.WakeLock? = null

    override fun onCreate() {
        super.onCreate()
        getSystemService(NotificationManager::class.java).createNotificationChannel(
            NotificationChannel(CHANNEL, "أدعية الرحمة", NotificationManager.IMPORTANCE_LOW)
        )
        tts = TextToSpeech(this, this)
    }

    override fun onInit(status: Int) {
        if (status != TextToSpeech.SUCCESS) {
            stopNow()
            return
        }
        val engine = tts ?: return
        val result = engine.setLanguage(Locale("ar", "SA"))
        if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
            engine.language = Locale("ar")
        }
        engine.setAudioAttributes(
            AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                .build()
        )
        engine.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {}
            override fun onError(utteranceId: String?) { advance() }
            override fun onDone(utteranceId: String?) { advance() }
        })
        ready = true
        if (queue.isNotEmpty()) speakCurrent()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_STOP -> stopNow()
            ACTION_PLAY_ONE -> {
                val id = intent.getIntExtra(EXTRA_ID, 1)
                DuaRepository.byId(id)?.let { startQueue(listOf(it)) }
            }
            ACTION_PLAY_ALL -> {
                val category = intent.getStringExtra(EXTRA_CATEGORY) ?: "all"
                startQueue(DuaRepository.byCategory(category))
            }
        }
        return START_NOT_STICKY
    }

    private fun startQueue(items: List<DuaItem>) {
        if (items.isEmpty()) return
        queue = items
        index = 0
        acquireWakeLock()
        showNotification(queue.first().title)
        if (ready) speakCurrent()
    }

    private fun speakCurrent() {
        val item = queue.getOrNull(index) ?: return stopNow()
        val prefs = getSharedPreferences("dua_prefs", MODE_PRIVATE)
        val rate = prefs.getFloat("speech_rate", 1.0f).coerceIn(0.7f, 1.4f)
        tts?.setSpeechRate(rate)
        showNotification(item.title)
        tts?.speak(
            item.text,
            TextToSpeech.QUEUE_FLUSH,
            Bundle(),
            "dua_" + item.id + "_" + System.currentTimeMillis()
        )
    }

    private fun advance() {
        val repeat = getSharedPreferences("dua_prefs", MODE_PRIVATE).getBoolean("repeat", false)
        if (repeat) {
            speakCurrent()
            return
        }
        index++
        if (index < queue.size) speakCurrent() else stopNow()
    }

    private fun showNotification(title: String) {
        val stopPi = PendingIntent.getService(
            this,
            71,
            Intent(this, DuaAudioService::class.java).apply { action = ACTION_STOP },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val openPi = PendingIntent.getActivity(
            this,
            72,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        startForeground(
            NOTIFICATION_ID,
            NotificationCompat.Builder(this, CHANNEL)
                .setSmallIcon(R.drawable.ic_dua)
                .setContentTitle("أدعية لأبي وأمي وأخي")
                .setContentText(title)
                .setContentIntent(openPi)
                .setOngoing(true)
                .addAction(0, "إيقاف", stopPi)
                .build()
        )
    }

    private fun acquireWakeLock() {
        if (wakeLock?.isHeld == true) return
        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "DuaMercy:Audio").apply {
                setReferenceCounted(false)
                acquire(30 * 60 * 1000L)
            }
    }

    private fun stopNow() {
        tts?.stop()
        queue = emptyList()
        index = 0
        if (wakeLock?.isHeld == true) wakeLock?.release()
        wakeLock = null
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        if (wakeLock?.isHeld == true) wakeLock?.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        const val ACTION_PLAY_ONE = "com.duamercy.premium.PLAY_ONE"
        const val ACTION_PLAY_ALL = "com.duamercy.premium.PLAY_ALL"
        const val ACTION_STOP = "com.duamercy.premium.STOP"
        const val EXTRA_ID = "dua_id"
        const val EXTRA_CATEGORY = "category"
        private const val CHANNEL = "dua_mercy_audio"
        private const val NOTIFICATION_ID = 9301
    }
}
