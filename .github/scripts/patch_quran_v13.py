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

# Add Salah Abu Khater recitations to Quran Premium, leaving all readers and UI intact.
# Reader 14 plays all 114 surahs directly from MP3Quran's verified original catalog.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
s = p.read_text()
old = '''        "أحمد عقل · 60 سورة متاحة"
    )

    val primaryAudio = listOf('''
new = '''        "أحمد عقل · 60 سورة متاحة",
        "صلاح أبو خاطر"
    )

    val primaryAudio = listOf('''
if s.count(old) != 1:
    raise SystemExit("Salah reciter list target missing or ambiguous")
p.write_text(s.replace(old, new, 1))

# Reader 14 has its own MP3 stream, no indexing legacy reader arrays and no
# fallback to other reciters' audio through the old Cloudflare proxy.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/playback/QuranPlaybackService.kt")
s = p.read_text()
old = '''        val uri = if (readerIndex == 12) {
            "https://media.way2quran.com/alaa-aql/hafs-an-asim/" +
                surah.toString().padStart(3, '0') + ".mp3"
        } else when (slot) {'''
new = '''        val uri = if (readerIndex == 14) {
            "https://cdn.mp3quran.net/audio/salah-bukhatir/r1/" +
                surah.toString().padStart(3, '0') + ".mp3"
        } else if (readerIndex == 12) {
            "https://media.way2quran.com/alaa-aql/hafs-an-asim/" +
                surah.toString().padStart(3, '0') + ".mp3"
        } else when (slot) {'''
if s.count(old) != 1:
    raise SystemExit("Salah direct playback target missing or ambiguous")
p.write_text(s.replace(old, new, 1))

# The original API timing endpoint has no Salah reader index. Preserve the app's
# existing approximate ayah-follow fallback instead of returning unrelated timings.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/data/QuranRepository.kt")
s = p.read_text()
old = '''        if (reader == 12) {
            main.post { callback(null) }'''
new = '''        if (reader == 12 || reader == 14) {
            main.post { callback(null) }'''
if s.count(old) != 1:
    raise SystemExit("Salah timing fallback target missing or ambiguous")
p.write_text(s.replace(old, new, 1))

print("Add Salah Abu Khater recitations to Quran Premium: other readers/design unchanged")

# Fix Android "App not installed" caused by different GitHub-runner debug signing keys.
# Use a separate application ID to install alongside the existing app without deleting its data.
# This does not alter app UI, existing reciters, playback functionality, or other projects.
build = Path("quran-premium-android/app/build.gradle.kts")
txt = build.read_text()
old = 'applicationId = "com.quran.premium"'
new = 'applicationId = "com.quran.premium.compat"'
if txt.count(old) != 1:
    raise SystemExit("Separate-install package target missing or ambiguous")
txt = txt.replace(old, new, 1)
if txt.count("versionCode = 103") != 1:
    raise SystemExit("Expected versionCode 103 is missing")
txt = txt.replace("versionCode = 103", "versionCode = 104", 1)
if txt.count('versionName = "1.3.0-premium"') != 1:
    raise SystemExit("Expected versionName 1.3.0 is missing")
txt = txt.replace('versionName = "1.3.0-premium"', 'versionName = "1.3.1-compatible"', 1)
build.write_text(txt)
print("Separate package ID enabled: installs safely beside original without uninstalling")

# Abu Rayan Al-Qaza'a recording status: user-requested name but no verifiable
# Quran recitation source currently found. Clearly label as unavailable and
# never substitute someone else's voice or feed into the 114-track playlist.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/AppConfig.kt")
s = p.read_text()
old = '''        "صلاح أبو خاطر"
    )

    val primaryAudio = listOf('''
new = '''        "صلاح أبو خاطر",
        "أبو ريان القزعة · التسجيلات غير متاحة"
    )

    val primaryAudio = listOf('''
if s.count(old) != 1:
    raise SystemExit("Abu Rayan name insertion target missing")
p.write_text(s.replace(old, new, 1))

# Show honest availability notice. Do NOT persist 15 or attempt to play as a
# reciter: old indexed stream lists cannot provide this reader's authentic audio.
p = Path("quran-premium-android/app/src/main/java/com/quran/premium/MainActivity.kt")
s = p.read_text()
old = '''                currentReader = which
                prefs.edit().putInt("reader", which).apply()'''
new = '''                if (which == 15) {
                    d.dismiss()
                    AlertDialog.Builder(this)
                        .setTitle("أبو ريان القزعة")
                        .setMessage("لم نعثر بعد على تسجيلات قرآنية موثوقة منسوبة لهذا القارئ. لم نغيّر أصوات القراء الآخرين. يمكن إضافة تلاواته عند توفر مصدر موثوق.")
                        .setPositiveButton("حسنًا", null)
                        .show()
                    return@setSingleChoiceItems
                }
                currentReader = which
                prefs.edit().putInt("reader", which).apply()'''
if s.count(old) != 1:
    raise SystemExit("Abu Rayan selector insertion target missing")
p.write_text(s.replace(old, new, 1))

# GitHub runners generate different debug signing keys per run. Use a fresh
# package ID, so Samsung can install alongside last compatible build safely
# without uninstalling or deleting user data.
p = Path("quran-premium-android/app/build.gradle.kts")
s = p.read_text()
checks = [
    ('applicationId = "com.quran.premium.compat"', 'applicationId = "com.quran.premium.aburayyan"'),
    ('versionCode = 104', 'versionCode = 105'),
    ('versionName = "1.3.1-compatible"', 'versionName = "1.3.2-aburayyan"'),
]
for old, new in checks:
    if s.count(old) != 1:
        raise SystemExit("Package version target missing: " + old)
    s = s.replace(old, new, 1)
p.write_text(s)
print("Abu Rayan Al-Qaza'a labeled as audio unavailable; existing readers unchanged")


# Offline-first Quran Premium v1.4
# Keep the entire Qur'an text in APK assets; bundle 38 surahs of Sudais audio
# (Al-Fatiha and Juz Amma), and provide system-managed permanent downloads
# for other surahs/readers via Wi-Fi. No account, subscription, or new API.
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
import json
from pathlib import Path

root = Path("quran-premium-android/app/src/main")
assets = root / "assets"
assets.mkdir(parents=True, exist_ok=True)

# Exact format already parsed by the existing native QuranRepository.
text_urls = [
    "https://quran-kareem.baraemest.workers.dev/api/quran",
    "https://api.alquran.cloud/v1/quran/quran-uthmani",
]
quran_data = None
for source in text_urls:
    try:
        req = Request(source, headers={"User-Agent": "QuranPremiumOffline/1.4", "Accept": "application/json"})
        with urlopen(req, timeout=45) as response:
            body = response.read(6500000)
        candidate = json.loads(body)
        surahs = candidate["data"]["surahs"]
        count = sum(len(s["ayahs"]) for s in surahs)
        assert len(surahs) == 114, "Missing surahs"
        assert 6200 <= count <= 6300, "Unexpected ayah count"
        assert [s["number"] for s in surahs] == list(range(1, 115)), "Surah order"
        assert all(s.get("name") and len(s["ayahs"]) > 0 for s in surahs), "Empty surah"
        assert all(a.get("text") and a.get("numberInSurah") == i
                   for s in surahs for i, a in enumerate(s["ayahs"], 1)), "Incomplete Quran verses"
        quran_data = candidate
        print("OFFLINE_QURAN_TEXT", source, count, "ayahs")
        break
    except Exception as exc:
        print("Quran source unavailable", source, str(exc)[:240])
if quran_data is None:
    raise SystemExit("Quran text verification failed: do not ship an incomplete offline Mushaf")
(assets / "quran.json").write_text(
    json.dumps(quran_data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

# Package a genuinely offline listening library in the APK:
# Reader 0 (Abdulrahman Al-Sudais), Al-Fatiha + all Juz Amma (78..114).
# Each MP3 is validated before it can be added to the Android assets.
audio_assets = assets / "audio" / "r0"
audio_assets.mkdir(parents=True, exist_ok=True)
surah_numbers = [1] + list(range(78, 115))
def get_audio(surah):
    fn = f"{surah:03d}.mp3"
    for base in (
        "https://server11.mp3quran.net/sds/",
        "https://cdn.mp3quran.net/audio/abdulrahman-sudais/r1/",
    ):
        try:
            request = Request(base + fn, headers={"User-Agent": "Mozilla/5.0", "Accept": "audio/mpeg,*/*"})
            with urlopen(request, timeout=25) as response:
                result = response.read(18000000)
            if not 4096 < len(result) < 18000000:
                raise ValueError("Not an MP3 file size")
            if not (result.startswith(b"ID3") or result[0] == 255):
                raise ValueError("Invalid MP3 signature")
            (audio_assets / fn).write_bytes(result)
            return surah, len(result)
        except Exception as exc:
            print("Offline audio mirror failed", surah, str(exc)[:140])
    return surah, 0

with ThreadPoolExecutor(max_workers=8) as pool:
    audio_results = list(pool.map(get_audio, surah_numbers))
available_surahs = sorted(s for s, n in audio_results if n > 0)
total_audio_bytes = sum(n for s, n in audio_results)
if 1 not in available_surahs or len(available_surahs) < 30:
    raise SystemExit("Insufficient verified bundled offline audio: "
                     + repr(available_surahs))
(assets / "offline_manifest.json").write_text(
    json.dumps({"reader": 0, "surahs": available_surahs,
                "audio_bytes": total_audio_bytes}, separators=(",", ":")), encoding="utf-8")
print("OFFLINE_AUDIO_BUNDLED", len(available_surahs), "surahs", total_audio_bytes, "bytes")

# Qt repository reads the bundled exact Uthmani Quran text without ever
# contacting the internet. Search, juz, bookmarks and text all remain local.
p = root / "java/com/quran/premium/data/QuranRepository.kt"
s = p.read_text()
old = '''                val json = tryNetwork() ?: if (cacheFile.exists()) cacheFile.readText() else error("Quran data unavailable")'''
new = '''                val json = context.assets.open("quran.json").bufferedReader(Charsets.UTF_8).use { it.readText() }'''
if s.count(old) != 1:
    raise SystemExit("Offline Quran text repository patch target not found")
s = s.replace(old, new, 1)
old = '''    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {
        if (reader == 12 || reader == 14) {'''
new = '''    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {
        if (!com.quran.premium.data.OfflineAudio.isConnected(context) || reader == 12 || reader == 14) {'''
if s.count(old) != 1:
    raise SystemExit("Offline timing patch target not found")
s = s.replace(old, new, 1)
p.write_text(s)

# Persistent file-based audio library + system DownloadManager, so a download
# continues even after the app UI closes. Uses Wi-Fi-only by default.
p = root / "java/com/quran/premium/data/OfflineAudio.kt"
p.write_text('''package com.quran.premium.data

import android.app.DownloadManager
import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.Uri
import android.os.Environment
import com.quran.premium.AppConfig
import java.io.File

object OfflineAudio {
    private var bundledFiles: Set<String>? = null

    fun isConnected(context: Context): Boolean {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val caps = cm.getNetworkCapabilities(cm.activeNetwork) ?: return false
        return caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) &&
            caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED)
    }

    private fun filename(surah: Int): String = surah.toString().padStart(3, '0') + ".mp3"

    private fun downloadFile(context: Context, reader: Int, surah: Int): File? {
        val music = context.getExternalFilesDir(Environment.DIRECTORY_MUSIC) ?: return null
        return File(music, "quran/r" + reader + "/" + filename(surah))
    }

    private fun bundled(context: Context): Set<String> {
        bundledFiles?.let { return it }
        return synchronized(this) {
            bundledFiles ?: (context.assets.list("audio/r0")?.toSet() ?: emptySet<String>())
                .also { bundledFiles = it }
        }
    }

    fun uri(context: Context, reader: Int, surah: Int): Uri? {
        val downloaded = downloadFile(context, reader, surah)
        if (downloaded?.isFile == true && downloaded.length() > 4096L) {
            return Uri.fromFile(downloaded)
        }
        if (reader == 0 && filename(surah) in bundled(context)) {
            return Uri.parse("asset:///audio/r0/" + filename(surah))
        }
        return null
    }

    fun availableCount(context: Context, reader: Int): Int =
        (1..114).count { uri(context, reader, it) != null }

    fun onlineUrl(reader: Int, surah: Int): String? {
        val file = filename(surah)
        return when (reader) {
            in 0..8 -> AppConfig.primaryAudio[reader] + file
            9 -> "https://cdn.mp3quran.net/audio/abdullah-juhani/r1/" + file
            10 -> "https://cdn.mp3quran.net/download/audio/ahmad-ajmi/r1/" + file
            12 -> "https://media.way2quran.com/alaa-aql/hafs-an-asim/" + file
            14 -> "https://cdn.mp3quran.net/audio/salah-bukhatir/r1/" + file
            else -> null
        }
    }

    // System DownloadManager persists jobs across process death and network interruption.
    // Returns number of newly enqueued surahs; already saved or bundled are skipped.
    fun enqueue(context: Context, reader: Int, surahs: Iterable<Int>): Int {
        val manager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        var queued = 0
        for (surah in surahs) {
            if (surah !in 1..114 || uri(context, reader, surah) != null) continue
            val url = onlineUrl(reader, surah) ?: continue
            val target = downloadFile(context, reader, surah) ?: continue
            target.parentFile?.mkdirs()
            if (target.exists() && target.length() <= 4096L) target.delete()
            val request = DownloadManager.Request(Uri.parse(url))
                .setTitle("القرآن الكريم • " + AppConfig.reciterNames[reader])
                .setDescription("سورة " + surah)
                .setDestinationInExternalFilesDir(
                    context, Environment.DIRECTORY_MUSIC,
                    "quran/r" + reader + "/" + filename(surah))
                .setAllowedOverMetered(false)
                .setAllowedOverRoaming(false)
                .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE)
            try {
                manager.enqueue(request)
                queued++
            } catch (_: Exception) {
                // If Android denies this particular URL/slot, leave other surahs intact.
            }
        }
        return queued
    }
}
''', encoding="utf-8")

# Keep ExoPlayer's native background playback, but prefer bundled or downloaded
# offline media before online streams, preserving the reader's correct voice.
p = root / "java/com/quran/premium/playback/QuranPlaybackService.kt"
s = p.read_text()
if "import com.quran.premium.AppConfig" not in s:
    raise SystemExit("Offline audio service import target not found")
s = s.replace("import com.quran.premium.AppConfig",
              "import com.quran.premium.AppConfig\nimport com.quran.premium.data.OfflineAudio", 1)
old = '''        val uri = if (readerIndex == 14) {'''
new = '''        val savedUri = OfflineAudio.uri(this, readerIndex, surah)
        val uri = savedUri?.toString() ?: if (readerIndex == 14) {'''
if s.count(old) != 1:
    raise SystemExit("Offline ExoPlayer URI patch target not found")
s = s.replace(old, new, 1)
old = '''    private fun recoverSource(reason: String) {
        if (player.mediaItemCount == 0) return'''
new = '''    private fun recoverSource(reason: String) {
        if (!OfflineAudio.isConnected(this)) {
            player.pause()
            return
        }
        if (player.mediaItemCount == 0) return'''
if s.count(old) != 1:
    raise SystemExit("Offline media source recovery patch target not found")
s = s.replace(old, new, 1)
p.write_text(s)

# Add a discrete offline library control, matching current button style.
p = root / "res/layout/activity_main.xml"
s = p.read_text()
old = '''                android:text="🔁 تكرار السورة" />'''
new = '''                android:text="🔁 تكرار السورة" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/btnOffline"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="match_parent"
                android:layout_height="44dp"
                android:layout_marginTop="6dp"
                android:text="⬇ حفظ السور للاستماع بدون إنترنت" />'''
if s.count(old) != 1:
    raise SystemExit("Offline button layout patch target not found")
p.write_text(s.replace(old, new, 1))

p = root / "java/com/quran/premium/MainActivity.kt"
s = p.read_text()
old = '''import com.quran.premium.data.QuranRepository'''
new = '''import com.quran.premium.data.QuranRepository
import com.quran.premium.data.OfflineAudio'''
if s.count(old) != 1:
    raise SystemExit("Offline MainActivity import target not found")
s = s.replace(old, new, 1)
old = '''        b.btnShare.setOnClickListener { shareCurrentAyah() }'''
new = '''        b.btnShare.setOnClickListener { shareCurrentAyah() }
        b.btnOffline.setOnClickListener { showOfflineLibraryDialog() }'''
if s.count(old) != 1:
    raise SystemExit("Offline button action target not found")
s = s.replace(old, new, 1)
old = '''            b.status.text = "جاهز · النص والصوت متزامنان"'''
new = '''            b.status.text = "المصحف كاملًا بلا إنترنت • الصوت المحفوظ يعمل دون اتصال"'''
if s.count(old) != 1:
    raise SystemExit("Offline Quran UI status target not found")
s = s.replace(old, new, 1)
old = '''    private fun showSurahDialog() {'''
new = '''    private fun showOfflineLibraryDialog() {
        val ready = OfflineAudio.availableCount(this, currentReader)
        val readerName = AppConfig.reciterNames[currentReader]
        AlertDialog.Builder(this)
            .setTitle("المكتبة الصوتية بدون إنترنت")
            .setMessage(readerName + " • المحفوظ " + ready + " من 114 سورة" +
                "\\nالمصحف مكتمل ويمكن قراءته والبحث فيه دون إنترنت. التلاوات غير المحفوظة تحتاج تنزيلًا واحدًا عبر Wi-Fi.")
            .setItems(arrayOf("⬇ حفظ السورة الحالية", "⬇ حفظ 114 سورة لهذا القارئ عبر Wi-Fi",
                "تحديث حالة الملفات المحفوظة")) { _, which ->
                if (which == 2) {
                    showOfflineLibraryDialog()
                } else if (OfflineAudio.onlineUrl(currentReader, currentSurah + 1) == null) {
                    Toast.makeText(this, "التسجيلات الصوتية غير متاحة لهذا القارئ", Toast.LENGTH_LONG).show()
                } else if (which == 0) {
                    val queued = OfflineAudio.enqueue(this, currentReader, listOf(currentSurah + 1))
                    Toast.makeText(this, if (queued > 0) "بدأ تحميل السورة عبر Wi-Fi" else "السورة محفوظة أو التحميل غير متاح",
                        Toast.LENGTH_LONG).show()
                } else {
                    AlertDialog.Builder(this)
                        .setTitle("حفظ المصحف صوتيًا")
                        .setMessage("قد تتطلب التلاوات مئات الميغابايت. سيُستعمل Wi-Fi فقط، وستبقى الملفات محفوظة على الهاتف.")
                        .setPositiveButton("بدء التحميل") { _, _ ->
                            val queued = OfflineAudio.enqueue(this, currentReader, 1..114)
                            Toast.makeText(this, "أضيفت " + queued + " سورة لقائمة تنزيلات Wi-Fi",
                                Toast.LENGTH_LONG).show()
                        }
                        .setNegativeButton("إلغاء", null)
                        .show()
                }
            }
            .setNegativeButton("إغلاق", null)
            .show()
    }

    private fun showSurahDialog() {'''
if s.count(old) != 1:
    raise SystemExit("Offline library dialog target not found")
s = s.replace(old, new, 1)
old = '''    private fun togglePlay() {
        val c = controller'''
new = '''    private fun togglePlay() {
        val c = controller
        val audioIndex = c?.currentMediaItemIndex?.takeIf { it in 0..113 } ?: currentSurah
        if (!OfflineAudio.isConnected(this) &&
            OfflineAudio.uri(this, currentReader, audioIndex + 1) == null) {
            Toast.makeText(this, "هذه السورة غير محفوظة. اضغط زر حفظ السور عند توفر Wi-Fi.",
                Toast.LENGTH_LONG).show()
            return
        }'''
if s.count(old) != 1:
    raise SystemExit("Offline play button guard target not found")
s = s.replace(old, new, 1)
old = '''    private fun playSurah(index: Int) {
        val i = Intent(this, QuranPlaybackService::class.java).apply {'''
new = '''    private fun playSurah(index: Int) {
        if (!OfflineAudio.isConnected(this) &&
            OfflineAudio.uri(this, currentReader, index + 1) == null) {
            Toast.makeText(this, "الصوت غير محفوظ لهذا القارئ. احفظ السورة عبر Wi-Fi أولًا.",
                Toast.LENGTH_LONG).show()
            return
        }
        val i = Intent(this, QuranPlaybackService::class.java).apply {'''
if s.count(old) != 1:
    raise SystemExit("Offline playSurah guard target not found")
s = s.replace(old, new, 1)
p.write_text(s)

# Connectivity status permission; DOWNLOAD_MANAGER is a system service (no other
# dangerous permission required) and all downloaded files are in app-specific storage.
p = root / "AndroidManifest.xml"
s = p.read_text()
old = '''    <uses-permission android:name="android.permission.INTERNET" />'''
new = '''    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />'''
if s.count(old) != 1:
    raise SystemExit("Offline connectivity manifest patch target not found")
p.write_text(s.replace(old, new, 1))

# GitHub runners sign debug builds with per-run different keys: ensure the
# new offline app can install alongside the previous APK without data loss.
p = Path("quran-premium-android/app/build.gradle.kts")
s = p.read_text()
for old, new in [
    ('applicationId = "com.quran.premium.aburayyan"', 'applicationId = "com.quran.premium.offline"'),
    ('versionCode = 105', 'versionCode = 106'),
    ('versionName = "1.3.2-aburayyan"', 'versionName = "1.4.0-offline"'),
]:
    if s.count(old) != 1:
        raise SystemExit("Offline install compatibility target missing: " + old)
    s = s.replace(old, new, 1)
p.write_text(s)
print("QURAN_PREMIUM_OFFLINE_READY - Arabic text and embedded recitations work without connectivity")
