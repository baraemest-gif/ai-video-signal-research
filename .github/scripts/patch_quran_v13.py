from pathlib import Path

# Main activity: persistent repeat-surah toggle.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/MainActivity.kt")
s = p.read_text()

old = "    private var currentAyah = 0\n"
new = "    private var currentAyah = 0\n    private var repeatSurah = false\n"
if old not in s:
    raise SystemExit("repeat state target not found")
s = s.replace(old, new, 1)

old = '        currentSurah = prefs.getInt("surah", 0).coerceIn(0, 113)\n'
new = '        currentSurah = prefs.getInt("surah", 0).coerceIn(0, 113)\n        repeatSurah = prefs.getBoolean("repeat_surah", false)\n'
if old not in s:
    raise SystemExit("repeat prefs target not found")
s = s.replace(old, new, 1)

old = "        wireUi()\n        connectController()\n"
new = "        wireUi()\n        updateRepeatButton()\n        connectController()\n"
if old not in s:
    raise SystemExit("repeat initial ui target not found")
s = s.replace(old, new, 1)

old = "        b.btnShare.setOnClickListener { shareCurrentAyah() }\n"
new = "        b.btnShare.setOnClickListener { shareCurrentAyah() }\n        b.btnRepeatSurah.setOnClickListener { toggleRepeatSurah() }\n"
if old not in s:
    raise SystemExit("repeat button listener target not found")
s = s.replace(old, new, 1)

old = "                    controller = future.get().also { it.addListener(playerListener) }\n                    syncFromPlayer()\n"
new = "                    controller = future.get().also { it.addListener(playerListener) }\n                    applyRepeatMode()\n                    syncFromPlayer()\n"
if old not in s:
    raise SystemExit("repeat controller target not found")
s = s.replace(old, new, 1)

marker = "    private fun togglePlay() {\n"
if marker not in s:
    raise SystemExit("togglePlay marker not found")
repeat_code = """    private fun toggleRepeatSurah() {
        repeatSurah = !repeatSurah
        prefs.edit().putBoolean("repeat_surah", repeatSurah).apply()
        applyRepeatMode()
        updateRepeatButton()
        Toast.makeText(
            this,
            if (repeatSurah) "سيتم تكرار السورة الحالية" else "تم إيقاف تكرار السورة",
            Toast.LENGTH_SHORT
        ).show()
    }

    private fun applyRepeatMode() {
        controller?.repeatMode = if (repeatSurah) Player.REPEAT_MODE_ONE else Player.REPEAT_MODE_OFF
        ContextCompat.startForegroundService(this, Intent(this, QuranPlaybackService::class.java).apply {
            action = QuranPlaybackService.ACTION_SET_REPEAT
            putExtra(QuranPlaybackService.EXTRA_REPEAT, repeatSurah)
        })
    }

    private fun updateRepeatButton() {
        b.btnRepeatSurah.text = if (repeatSurah) "🔂 تكرار السورة · مفعّل" else "🔁 تكرار السورة"
        b.btnRepeatSurah.alpha = if (repeatSurah) 1.0f else 0.72f
    }

"""
s = s.replace(marker, repeat_code + marker, 1)
p.write_text(s)

# Layout: add a dedicated repeat-surah button below transport controls.
lp = Path("quran-premium-android/app/src/main/res/layout/activity_main.xml")
x = lp.read_text()
old = """            <LinearLayout
                android:layout_width="match_parent" android:layout_height="wrap_content"
                android:orientation="horizontal" android:gravity="center">
                <com.google.android.material.button.MaterialButton
                    android:id="@+id/btnPrev" style="@style/Widget.QuranPremium.Round" android:text="⏮" />
                <Space android:layout_width="14dp" android:layout_height="1dp" />
                <com.google.android.material.button.MaterialButton
                    android:id="@+id/btnPlay" style="@style/Widget.QuranPremium.Play" android:text="▶" />
                <Space android:layout_width="14dp" android:layout_height="1dp" />
                <com.google.android.material.button.MaterialButton
                    android:id="@+id/btnNext" style="@style/Widget.QuranPremium.Round" android:text="⏭" />
            </LinearLayout>
"""
new = old + """
            <com.google.android.material.button.MaterialButton
                android:id="@+id/btnRepeatSurah"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="match_parent"
                android:layout_height="44dp"
                android:layout_marginTop="8dp"
                android:text="🔁 تكرار السورة" />
"""
if old not in x:
    raise SystemExit("repeat layout target not found")
x = x.replace(old, new, 1)
lp.write_text(x)

# Playback service: make repeat mode native and persistent even with screen off.
sp = Path("quran-premium-android/app/src/main/java/com/quran/premium/playback/QuranPlaybackService.kt")
q = sp.read_text()

old = "    private var stalledTicks = 0\n"
new = "    private var stalledTicks = 0\n    private var repeatSurah = false\n"
if old not in q:
    raise SystemExit("service repeat state target not found")
q = q.replace(old, new, 1)

old = '        readerIndex = prefs.getInt("reader", 0).coerceIn(0, AppConfig.reciterNames.lastIndex)\n'
new = '        readerIndex = prefs.getInt("reader", 0).coerceIn(0, AppConfig.reciterNames.lastIndex)\n        repeatSurah = prefs.getBoolean("repeat_surah", false)\n'
if old not in q:
    raise SystemExit("service repeat prefs target not found")
q = q.replace(old, new, 1)

old = """        player = ExoPlayer.Builder(this).build().apply {
            setAudioAttributes(attrs, true)
            setWakeMode(C.WAKE_MODE_NETWORK)
            setHandleAudioBecomingNoisy(true)
            addListener(listener)
        }
"""
new = """        player = ExoPlayer.Builder(this).build().apply {
            setAudioAttributes(attrs, true)
            setWakeMode(C.WAKE_MODE_NETWORK)
            setHandleAudioBecomingNoisy(true)
            repeatMode = if (repeatSurah) Player.REPEAT_MODE_ONE else Player.REPEAT_MODE_OFF
            addListener(listener)
        }
"""
if old not in q:
    raise SystemExit("service player repeat target not found")
q = q.replace(old, new, 1)

old = """            ACTION_TOGGLE -> if (player.isPlaying) player.pause() else player.play()
        }
"""
new = """            ACTION_TOGGLE -> if (player.isPlaying) player.pause() else player.play()
            ACTION_SET_REPEAT -> {
                repeatSurah = intent.getBooleanExtra(EXTRA_REPEAT, false)
                player.repeatMode = if (repeatSurah) Player.REPEAT_MODE_ONE else Player.REPEAT_MODE_OFF
                prefs.edit().putBoolean("repeat_surah", repeatSurah).apply()
            }
        }
"""
if old not in q:
    raise SystemExit("service action repeat target not found")
q = q.replace(old, new, 1)

old = """        const val ACTION_TOGGLE = "com.quran.premium.TOGGLE"
        const val EXTRA_SURAH = "surah"
        const val EXTRA_READER = "reader"
"""
new = """        const val ACTION_TOGGLE = "com.quran.premium.TOGGLE"
        const val ACTION_SET_REPEAT = "com.quran.premium.SET_REPEAT"
        const val EXTRA_SURAH = "surah"
        const val EXTRA_READER = "reader"
        const val EXTRA_REPEAT = "repeat"
"""
if old not in q:
    raise SystemExit("service constants repeat target not found")
q = q.replace(old, new, 1)
sp.write_text(q)

# Version bump.
g = Path("quran-premium-android/app/build.gradle.kts")
gs = g.read_text()
gs = gs.replace("versionCode = 102", "versionCode = 103")
gs = gs.replace('versionName = "1.2.0-premium"', 'versionName = "1.3.0-premium"')
g.write_text(gs)

print("Quran Premium v1.3 repeat-surah button patch applied")
