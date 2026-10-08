from pathlib import Path

p = Path("quran-premium-android/app/src/main/java/com/quran/premium/MainActivity.kt")
s = p.read_text()

if "import kotlin.math.abs" not in s:
    s = s.replace(
        "import java.util.Locale\n",
        "import java.util.Locale\nimport kotlin.math.abs\n"
    )

old = """        if (scrollAyah != null) {
            b.ayahScroll.post { ayahViews.getOrNull(scrollAyah)?.let { b.ayahScroll.smoothScrollTo(0, it.top) } }
        }
"""
new = """        if (scrollAyah != null) {
            currentAyah = scrollAyah.coerceIn(0, s.ayahs.lastIndex.coerceAtLeast(0))
            highlightAyah(currentAyah)
            scrollToAyah(currentAyah, force = true)
        } else {
            b.ayahScroll.post { b.ayahScroll.scrollTo(0, 0) }
        }
"""
if old not in s:
    raise SystemExit("showSurah patch target not found")
s = s.replace(old, new)

old = """    private val playerListener = object : Player.Listener {
        override fun onIsPlayingChanged(isPlaying: Boolean) { updatePlayButton() }
        override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
            syncFromPlayer()
        }
    }
"""
new = """    private val playerListener = object : Player.Listener {
        override fun onIsPlayingChanged(isPlaying: Boolean) { updatePlayButton() }

        override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
            val idx = mediaItem?.mediaId?.toIntOrNull() ?: controller?.currentMediaItemIndex ?: return
            if (idx in 0..113 && surahs.isNotEmpty()) {
                if (idx != currentSurah) showSurah(idx, 0, syncAudio = false)
                else scrollToAyah(currentAyah, force = true)
            }
            syncFromPlayer()
        }
    }
"""
if old not in s:
    raise SystemExit("playerListener patch target not found")
s = s.replace(old, new)

old = """            val c = controller
            if (c != null) {
                val d = c.duration
"""
new = """            val c = controller
            if (c != null) {
                val playerSurah = c.currentMediaItemIndex
                if (playerSurah in 0..113 && playerSurah != currentSurah && surahs.isNotEmpty()) {
                    showSurah(playerSurah, 0, syncAudio = false)
                }
                val d = c.duration
"""
if old not in s:
    raise SystemExit("progress loop patch target not found")
s = s.replace(old, new)

old = """    private fun highlightAyah(index: Int) {
        currentAyah = index.coerceAtLeast(0)
        ayahViews.forEachIndexed { i, v ->
            v.setBackgroundColor(if (i == currentAyah) Color.argb(70, 192, 38, 211) else Color.TRANSPARENT)
        }
    }
"""
new = """    private fun highlightAyah(index: Int) {
        currentAyah = index.coerceAtLeast(0)
        ayahViews.forEachIndexed { i, v ->
            v.setBackgroundColor(if (i == currentAyah) Color.argb(70, 192, 38, 211) else Color.TRANSPARENT)
        }
        scrollToAyah(currentAyah, force = false)
    }

    private fun scrollToAyah(index: Int, force: Boolean) {
        val v = ayahViews.getOrNull(index) ?: return
        b.ayahScroll.post {
            val scroll = b.ayahScroll
            val viewportTop = scroll.scrollY
            val viewportBottom = viewportTop + scroll.height
            val viewTop = v.top
            val viewBottom = v.bottom
            val margin = (scroll.height * 0.22f).toInt()
            val outsideComfortZone = viewTop < viewportTop + margin || viewBottom > viewportBottom - margin
            if (force || outsideComfortZone) {
                val target = (viewTop - (scroll.height - v.height) / 2).coerceAtLeast(0)
                if (abs(scroll.scrollY - target) > 12) scroll.smoothScrollTo(0, target)
            }
        }
    }
"""
if old not in s:
    raise SystemExit("highlight patch target not found")
s = s.replace(old, new)

p.write_text(s)

g = Path("quran-premium-android/app/build.gradle.kts")
gs = g.read_text()
gs = gs.replace("versionCode = 101", "versionCode = 102")
gs = gs.replace('versionName = "1.1.0-premium"', 'versionName = "1.2.0-premium"')
g.write_text(gs)

print("Quran Premium v1.2 synchronized follow patch applied")
