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

old = "controller = future.get().also { it.addListener(playerListener) }"
new = """controller = future.get().also { it.addListener(playerListener) }
                    applyRepeatMode()"""
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

# Add Abdullah Al-Johany recitations to the native APK only.
# Leave all existing reciters and app styling unchanged.
app = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
a = app.read_text()
for old, new in [
    (
        """        "عبدالباسط · مجوّد"
    )

    val primaryAudio = listOf(""",
        """        "عبدالباسط · مجوّد",
        "عبدالله عواد الجهني"
    )

    val primaryAudio = listOf("""
    ),
    (
        """        "https://cdn.mp3quran.net/audio/abdulbasit-abdulsamad/r1/"
    )

    val backupAudio = listOf(""",
        """        "https://cdn.mp3quran.net/audio/abdulbasit-abdulsamad/r1/",
        "https://cdn.mp3quran.net/audio/abdullah-juhani/r1/"
    )

    val backupAudio = listOf("""
    ),
    (
        """        "https://cdn.mp3quran.net/audio/abdulbasit-abdulsamad/r1/"
    )
}""",
        """        "https://cdn.mp3quran.net/audio/abdulbasit-abdulsamad/r1/",
        "https://server13.mp3quran.net/jhn/"
    )
}"""
    ),
]:
    if a.count(old) != 1:
        raise SystemExit("Johany AppConfig target not found or ambiguous")
    a = a.replace(old, new, 1)
app.write_text(a)

# The web audio proxy supports readers 0..8, so ensure reader 9
# never falls back to someone else's voice.
sp = Path("quran-premium-android/app/src/main/java/com/quran/premium/playback/QuranPlaybackService.kt")
q = sp.read_text()
old = '''            2 -> "${AppConfig.API_BASE}/audio/file?reader=$readerIndex&surah=$surah&source=0&native=1"'''
new = '''            2 -> if (readerIndex == 9) {
                AppConfig.primaryAudio[readerIndex] + surah.toString().padStart(3, '0') + ".mp3"
            } else {
                "${AppConfig.API_BASE}/audio/file?reader=$readerIndex&surah=$surah&source=0&native=1"
            }'''
if q.count(old) != 1:
    raise SystemExit("Johany playback fallback target not found or ambiguous")
sp.write_text(q.replace(old, new, 1))

# The web timing endpoint also supports readers 0..8 only.
# Fetch Abdullah Al-Johany's own timing metadata (read 62);
# on missing/incomplete timing, keep the existing approximate-follow fallback.
rp = Path("quran-premium-android/app/src/main/java/com/quran/premium/data/QuranRepository.kt")
r = rp.read_text()
old = '''                val c = URL("${AppConfig.API_BASE}/api/timing?reader=$reader&surah=$surah&native=1").openConnection() as HttpURLConnection'''
new = '''                val timingUrl = if (reader == 9)
                    "https://mp3quran.net/api/v3/ayat_timing?surah=$surah&read=62"
                else "${AppConfig.API_BASE}/api/timing?reader=$reader&surah=$surah&native=1"
                val c = URL(timingUrl).openConnection() as HttpURLConnection'''
if r.count(old) != 1:
    raise SystemExit("Johany timing endpoint target not found or ambiguous")
r = r.replace(old, new, 1)
old = '''                    val j = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                    val a = j.getJSONArray("t")
                    LongArray(a.length()) { a.getLong(it) }'''
new = '''                    val responseText = c.inputStream.bufferedReader().use { it.readText() }
                    if (reader == 9) {
                        val array = org.json.JSONArray(responseText)
                        val verses = (0 until array.length()).map { array.getJSONObject(it) }
                            .filter { it.optInt("ayah", 0) >= 1 }
                        val expected = surahs.getOrNull(surah - 1)?.ayahs?.size ?: 0
                        if (verses.size != expected ||
                            verses.withIndex().any { (index, verse) -> verse.optInt("ayah", -1) != index + 1 }) {
                            null
                        } else {
                            val starts = LongArray(verses.size) { verses[it].getLong("start_time") }
                            if (starts.indices.drop(1).any { starts[it] < starts[it - 1] }) null else starts
                        }
                    } else {
                        val j = JSONObject(responseText)
                        val a = j.getJSONArray("t")
                        LongArray(a.length()) { a.getLong(it) }
                    }'''
if r.count(old) != 1:
    raise SystemExit("Johany timing parsing target not found or ambiguous")
rp.write_text(r.replace(old, new, 1))
print("Added Abdullah Al-Johany to Quran Premium native without modifying other reciters")

# Add Ahmad bin Ali Al-Ajmy as the eleventh native reciter.
# Keep all existing names, their indexes, the layout and other app behavior untouched.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
a = p.read_text()
for old, new in [
    (
        '''        "عبدالله عواد الجهني"
    )

    val primaryAudio = listOf(''',
        '''        "عبدالله عواد الجهني",
        "أحمد بن علي العجمي"
    )

    val primaryAudio = listOf('''
    ),
    (
        '''        "https://cdn.mp3quran.net/audio/abdullah-juhani/r1/"
    )

    val backupAudio = listOf(''',
        '''        "https://cdn.mp3quran.net/audio/abdullah-juhani/r1/",
        "https://cdn.mp3quran.net/download/audio/ahmad-ajmi/r1/"
    )

    val backupAudio = listOf('''
    ),
    (
        '''        "https://server13.mp3quran.net/jhn/"
    )
}''',
        '''        "https://server13.mp3quran.net/jhn/",
        "https://server10.mp3quran.net/ajm/"
    )
}'''
    ),
]:
    if a.count(old) != 1:
        raise SystemExit("Ahmad Al-Ajmy AppConfig target missing or ambiguous")
    a = a.replace(old, new, 1)
p.write_text(a)

# Prevent proxy fallback from serving a different reader's audio for native-only readers.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/playback/QuranPlaybackService.kt")
q = p.read_text()
old = "            2 -> if (readerIndex == 9) {"
new = "            2 -> if (readerIndex == 9 || readerIndex == 10) {"
if q.count(old) != 1:
    raise SystemExit("Ahmad Al-Ajmy fallback target missing")
p.write_text(q.replace(old, new, 1))

# The Ajmy recording has an official per-ayah timing feed: read=5.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/data/QuranRepository.kt")
r = p.read_text()
old = '''                val timingUrl = if (reader == 9)
                    "https://mp3quran.net/api/v3/ayat_timing?surah=$surah&read=62"
                else "${AppConfig.API_BASE}/api/timing?reader=$reader&surah=$surah&native=1"'''
new = '''                val timingUrl = when (reader) {
                    9 -> "https://mp3quran.net/api/v3/ayat_timing?surah=$surah&read=62"
                    10 -> "https://mp3quran.net/api/v3/ayat_timing?surah=$surah&read=5"
                    else -> "${AppConfig.API_BASE}/api/timing?reader=$reader&surah=$surah&native=1"
                }'''
if r.count(old) != 1:
    raise SystemExit("Ahmad Al-Ajmy timing endpoint target missing")
r = r.replace(old, new, 1)
old = "                    if (reader == 9) {"
new = "                    if (reader == 9 || reader == 10) {"
if r.count(old) != 1:
    raise SystemExit("Ahmad Al-Ajmy timing response target missing")
p.write_text(r.replace(old, new, 1))

print("Added Ahmad Al-Ajmy to Quran Premium native; no other changes")

# Add Hani Al-Azouni official recitations (available surahs only).
# His full 114-surah audio catalog has not been verified. NEVER substitute another voice.
# This is a selection of links to his own SoundCloud tracks; other readers are unchanged.
app = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
cfg = app.read_text()
old = '''        "أحمد بن علي العجمي"
    )

    val primaryAudio = listOf('''
new = '''        "أحمد بن علي العجمي",
        "هاني العزوني · تلاوات مختارة"
    )

    val primaryAudio = listOf('''
if cfg.count(old) != 1:
    raise SystemExit("Hani Al-Azouni reciter list target not found")
app.write_text(cfg.replace(old, new, 1))

# Selecting Hani opens a small chooser of authentic published recordings instead
# of sending invalid/unverified MP3 URLs into the 114-surah native playlist.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/MainActivity.kt")
s = p.read_text()
old = '''            .setSingleChoiceItems(AppConfig.reciterNames.toTypedArray(), currentReader) { d, which ->
                currentReader = which'''
new = '''            .setSingleChoiceItems(AppConfig.reciterNames.toTypedArray(), currentReader) { d, which ->
                if (which == 11) {
                    d.dismiss()
                    showHaniRecitationsDialog()
                    return@setSingleChoiceItems
                }
                currentReader = which'''
if s.count(old) != 1:
    raise SystemExit("Hani recitation selection target not found")
s = s.replace(old, new, 1)
old = '''    private fun showSurahDialog() {'''
new = '''    private fun showHaniRecitationsDialog() {
        val labels = arrayOf("سورة ق · هاني العزوني", "سورة الإنسان · هاني العزوني", "تلاوات أخرى من حساب القارئ")
        val links = arrayOf(
            "https://soundcloud.com/hany-al-tmsah/3lbos6jm3kpy",
            "https://soundcloud.com/hany-al-tmsah/nb1yo7omc45w",
            "https://soundcloud.com/hany-al-tmsah"
        )
        AlertDialog.Builder(this)
            .setTitle("هاني العزوني · التلاوات المنشورة")
            .setItems(labels) { _, i ->
                val intent = Intent(Intent.ACTION_VIEW, android.net.Uri.parse(links[i]))
                try {
                    startActivity(intent)
                } catch (_: android.content.ActivityNotFoundException) {
                    Toast.makeText(this, "لا يوجد متصفح لفتح التلاوة", Toast.LENGTH_LONG).show()
                }
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun showSurahDialog() {'''
if s.count(old) != 1:
    raise SystemExit("Hani dialog insertion target not found")
p.write_text(s.replace(old, new, 1))
print("Added Hani Al-Azouni official recitations; other readers and the visual design unchanged")

# Add Alaa Aql and Ahmed Akl to Quran Premium; preserve all existing readers/design.
# Alaa: 114 verified native MP3 files (Way2Quran). Ahmed: 60 published surahs (Assabile),
# opened directly in the source catalog rather than fabricating missing audio URLs.
app = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
a = app.read_text()
old = '''        "هاني العزوني · تلاوات مختارة"
    )

    val primaryAudio = listOf('''
new = '''        "هاني العزوني · تلاوات مختارة",
        "علاء عقل",
        "أحمد عقل · 60 سورة متاحة"
    )

    val primaryAudio = listOf('''
if a.count(old) != 1:
    raise SystemExit("Alaa/Ahmed AppConfig reciter insertion target not found")
app.write_text(a.replace(old, new, 1))

# Keep indexes 0..10 and Hani selection 11 unchanged. Alaa is reader 12, Ahmed reader 13.
main = Path("quran-premium-android/app/src/main/java/com/quran/premium/MainActivity.kt")
m = main.read_text()
old = '''                if (which == 11) {
                    d.dismiss()
                    showHaniRecitationsDialog()
                    return@setSingleChoiceItems
                }
                currentReader = which'''
new = '''                if (which == 11) {
                    d.dismiss()
                    showHaniRecitationsDialog()
                    return@setSingleChoiceItems
                }
                if (which == 13) {
                    d.dismiss()
                    val link = android.net.Uri.parse("https://ar.assabile.com/ahmed-akl/quran")
                    try {
                        startActivity(Intent(Intent.ACTION_VIEW, link))
                    } catch (_: android.content.ActivityNotFoundException) {
                        Toast.makeText(this, "لا يوجد متصفح لفتح تلاوات أحمد عقل", Toast.LENGTH_LONG).show()
                    }
                    return@setSingleChoiceItems
                }
                currentReader = which'''
if m.count(old) != 1:
    raise SystemExit("Alaa/Ahmed reader selector insertion target not found")
main.write_text(m.replace(old, new, 1))

# Route only the newly added native reader directly to his own 114-track catalog.
# Do not index original 11-entry audio arrays using readerIndex 12 or 13.
svc = Path("quran-premium-android/app/src/main/java/com/quran/premium/playback/QuranPlaybackService.kt")
q = svc.read_text()
old = "        val uri = when (slot) {"
new = """        val uri = if (readerIndex == 12) {
            "https://media.way2quran.com/alaa-aql/hafs-an-asim/" +
                surah.toString().padStart(3, '0') + ".mp3"
        } else when (slot) {"""
if q.count(old) != 1:
    raise SystemExit("Alaa direct MP3 playback target not found")
svc.write_text(q.replace(old, new, 1))

# Do not request timing for reader 12 from the web proxy, which only supports
# old reader indexes. Use the native reader's pre-existing approximate ayah follow.
repo = Path("quran-premium-android/app/src/main/java/com/quran/premium/data/QuranRepository.kt")
r = repo.read_text()
old = '''    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {
        executor.execute {'''
new = '''    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {
        if (reader == 12) {
            main.post { callback(null) }
            return
        }
        executor.execute {'''
if r.count(old) != 1:
    raise SystemExit("Alaa timing fallback target not found")
repo.write_text(r.replace(old, new, 1))

print("Add Alaa Aql and Ahmed Akl to Quran Premium: unchanged previous readers/design")
