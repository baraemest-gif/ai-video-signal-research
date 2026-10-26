#!/usr/bin/env python3
"""Add a separate vertical 604-page mushaf reader to Quran Premium v1.3.

Run after patch_quran_v12.py and patch_quran_v13.py in the restored Android project.
Fail on missing source anchors so that a changed upstream app is not silently modified.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "quran-premium-android")
app = root / "app"
java = app / "src/main/java/com/quran/premium"
res = app / "src/main/res"


def replace(path, old, new):
    path = Path(path)
    content = path.read_text(encoding="utf-8")
    if old not in content:
        if new in content:
            print("Already patched:", path, flush=True)
            return
        raise RuntimeError(f"Missing patch anchor in {path}: {old[:85]}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


gradle = app / "build.gradle.kts"
replace(gradle, 'applicationId = "com.quran.premium"', 'applicationId = "com.quran.premium.mushafbeta"')
replace(gradle, 'versionCode = 103', 'versionCode = 104')
replace(gradle, 'versionName = "1.3.0-premium"', 'versionName = "1.4.0-mushaf-beta"')
replace(gradle,
        'implementation("androidx.constraintlayout:constraintlayout:2.2.1")',
        'implementation("androidx.constraintlayout:constraintlayout:2.2.1")\n    implementation("androidx.viewpager2:viewpager2:1.1.0")')

manifest = app / "src/main/AndroidManifest.xml"
replace(manifest, 'android:label="القرآن الكريم Premium"', 'android:label="القرآن الكريم · مصحف تجريبي"')

model = java / "model/MushafAyah.kt"
model.write_text('''package com.quran.premium.model

/** Verse text as provided by the Uthmani edition, indexed by Mushaf page. */
data class MushafAyah(
    val text: String,
    val numberInSurah: Int,
    val surahNumber: Int,
    val surahName: String
)
''', encoding="utf-8")

repository = java / "data/QuranRepository.kt"
replace(repository,
        'import com.quran.premium.model.Ayah',
        'import com.quran.premium.model.Ayah\nimport com.quran.premium.model.MushafAyah')
replace(repository,
        '    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {',
        '''    /** AlQuran Cloud Uthmani pages: exactly 604 page identifiers, cached for offline re-reading. */
    fun page(number: Int, onSuccess: (List<MushafAyah>) -> Unit, onError: (Throwable) -> Unit) {
        require(number in 1..604)
        executor.execute {
            try {
                val directory = File(context.filesDir, "mushaf-pages").also { it.mkdirs() }
                val file = File(directory, "page-$number.json")
                val cached = if (file.exists()) file.readText() else null
                val raw = cached ?: run {
                    val connection = URL("https://api.alquran.cloud/v1/page/$number/quran-uthmani")
                        .openConnection() as HttpURLConnection
                    connection.connectTimeout = 8000
                    connection.readTimeout = 14000
                    try {
                        check(connection.responseCode in 200..299) { "Page HTTP ${connection.responseCode}" }
                        connection.inputStream.bufferedReader().use { it.readText() }
                    } finally {
                        connection.disconnect()
                    }
                }
                val data = JSONObject(raw)
                check(data.optInt("code") == 200) { "Unexpected response for page $number" }
                val ayahArray = data.getJSONObject("data").getJSONArray("ayahs")
                require(ayahArray.length() > 0) { "Empty Mushaf page $number" }
                val ayahs = buildList {
                    for (i in 0 until ayahArray.length()) {
                        val a = ayahArray.getJSONObject(i)
                        val surah = a.getJSONObject("surah")
                        if (a.has("page")) require(a.getInt("page") == number)
                        add(MushafAyah(
                            text = a.getString("text"),
                            numberInSurah = a.getInt("numberInSurah"),
                            surahNumber = surah.getInt("number"),
                            surahName = surah.getString("name")
                        ))
                    }
                }
                if (cached == null) file.writeText(raw)
                main.post { onSuccess(ayahs) }
            } catch (t: Throwable) {
                main.post { onError(t) }
            }
        }
    }

    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {''')

page_layout = res / "layout/item_mushaf_page.xml"
page_layout.write_text('''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F3E7C9"
    android:padding="8dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:background="@drawable/bg_mushaf_sheet"
        android:orientation="vertical"
        android:paddingHorizontal="13dp"
        android:paddingTop="10dp"
        android:paddingBottom="10dp">

        <TextView
            android:id="@+id/mushafPageHeading"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:layoutDirection="rtl"
            android:text="القرآن الكريم"
            android:textSize="16sp"
            android:textStyle="bold"
            android:textColor="#76603A"
            android:paddingBottom="8dp" />

        <TextView
            android:id="@+id/mushafPageBody"
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1"
            android:gravity="center"
            android:layoutDirection="rtl"
            android:textDirection="rtl"
            android:fontFamily="serif"
            android:includeFontPadding="true"
            android:textColor="#27201A"
            android:textSize="27sp"
            android:lineSpacingExtra="4dp"
            android:autoSizeTextType="uniform"
            android:autoSizeMinTextSize="15sp"
            android:autoSizeMaxTextSize="31sp"
            android:autoSizeStepGranularity="1sp"
            android:text="جارٍ تحميل الصفحة…" />

        <TextView
            android:id="@+id/mushafPageFooter"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:textColor="#76603A"
            android:textSize="13sp"
            android:paddingTop="7dp" />
    </LinearLayout>
</FrameLayout>
''', encoding="utf-8")

drawable = res / "drawable/bg_mushaf_sheet.xml"
drawable.write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#FFF9EC" />
    <corners android:radius="10dp" />
    <stroke android:width="2dp" android:color="#BFA36D" />
</shape>
''', encoding="utf-8")

adapter = java / "MushafPageAdapter.kt"
adapter.write_text('''package com.quran.premium

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.quran.premium.data.QuranRepository
import com.quran.premium.model.MushafAyah

/** Native, full-height pages. A tap advances; swipe up/down navigates with ViewPager2. */
class MushafPageAdapter(
    private val repository: QuranRepository,
    private val onPageTap: (Int) -> Unit
) : RecyclerView.Adapter<MushafPageAdapter.PageHolder>() {

    class PageHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val heading: TextView = itemView.findViewById(R.id.mushafPageHeading)
        val body: TextView = itemView.findViewById(R.id.mushafPageBody)
        val footer: TextView = itemView.findViewById(R.id.mushafPageFooter)
        var boundPage = -1
    }

    override fun getItemCount(): Int = 604

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PageHolder =
        PageHolder(LayoutInflater.from(parent.context).inflate(R.layout.item_mushaf_page, parent, false))

    override fun onBindViewHolder(holder: PageHolder, position: Int) {
        val page = position + 1
        holder.boundPage = page
        holder.heading.text = "﷽   •   القرآن الكريم"
        holder.body.text = "جارٍ تحميل الصفحة…"
        holder.footer.text = "الصفحة ${arabicDigits(page)} من ٦٠٤"
        holder.itemView.setOnClickListener { onPageTap(page) }
        holder.body.setOnClickListener { onPageTap(page) }
        repository.page(page, { ayahs ->
            if (holder.boundPage == page) {
                holder.heading.text = ayahs.firstOrNull()?.surahName ?: "القرآن الكريم"
                holder.body.text = renderPage(ayahs)
            }
        }, {
            if (holder.boundPage == page) {
                holder.body.text = "تعذّر تحميل الصفحة. تحقق من الإنترنت ثم اضغط لإعادة المحاولة."
                holder.body.setOnClickListener {
                    repository.page(page, { ayahs ->
                        if (holder.boundPage == page) holder.body.text = renderPage(ayahs)
                    }, {
                        if (holder.boundPage == page) holder.body.text = "يرجى الاتصال بالإنترنت لإعادة التحميل"
                    })
                }
            }
        })
    }

    private fun renderPage(ayahs: List<MushafAyah>): String = buildString {
        var lastSurah = -1
        ayahs.forEach { ayah ->
            if (ayah.surahNumber != lastSurah) {
                if (isNotEmpty()) append("\\n\\n")
                append("۞ ").append(ayah.surahName).append(" ۞")
                append("\\n")
                lastSurah = ayah.surahNumber
            }
            append(ayah.text)
            append(" ﴿").append(arabicDigits(ayah.numberInSurah)).append("﴾ ")
        }
    }

    private fun arabicDigits(number: Int): String = number.toString().map { ch ->
        if (ch in '0'..'9') "٠١٢٣٤٥٦٧٨٩"[ch - '0'] else ch
    }.joinToString("")
}
''', encoding="utf-8")

layout = res / "layout/activity_main.xml"
replace(layout,
        '        </LinearLayout>\n    </LinearLayout>\n\n    <LinearLayout\n        android:id="@+id/titleBlock"',
        '''        </LinearLayout>

        <com.google.android.material.button.MaterialButton
            android:id="@+id/btnMushaf"
            style="@style/Widget.QuranPremium.Chip"
            android:layout_width="match_parent"
            android:layout_height="44dp"
            android:layout_marginTop="8dp"
            android:text="📖 قراءة المصحف · ٦٠٤ صفحة" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/titleBlock"''')
replace(layout,
        '</androidx.constraintlayout.widget.ConstraintLayout>',
        '''    <!-- A separate reader surface; existing player continues underneath unchanged. -->
    <LinearLayout
        android:id="@+id/mushafOverlay"
        android:layout_width="0dp"
        android:layout_height="0dp"
        android:orientation="vertical"
        android:background="#F3E7C9"
        android:visibility="gone"
        android:elevation="20dp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center_vertical"
            android:padding="9dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafClose"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="wrap_content"
                android:layout_height="48dp"
                android:text="✕ إغلاق" />
            <TextView
                android:id="@+id/mushafPageIndicator"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:gravity="center"
                android:text="الصفحة ١ من ٦٠٤"
                android:textColor="#382B1C"
                android:textSize="17sp"
                android:textStyle="bold" />
        </LinearLayout>

        <androidx.viewpager2.widget.ViewPager2
            android:id="@+id/mushafPager"
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1"
            android:layoutDirection="ltr" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:padding="7dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafPrevious"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="السابق" />
            <Space android:layout_width="6dp" android:layout_height="1dp" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafAudio"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="▶ الصوت" />
            <Space android:layout_width="6dp" android:layout_height="1dp" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafNext"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="التالي" />
        </LinearLayout>
    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>''')

activity = java / "MainActivity.kt"
replace(activity,
        'import androidx.activity.ComponentActivity',
        'import androidx.activity.ComponentActivity\nimport androidx.activity.OnBackPressedCallback\nimport androidx.activity.addCallback\nimport androidx.viewpager2.widget.ViewPager2')
replace(activity,
        '    private val prefs by lazy { getSharedPreferences("ui", Context.MODE_PRIVATE) }',
        '''    private val prefs by lazy { getSharedPreferences("ui", Context.MODE_PRIVATE) }
    private val mushafBackCallback = object : OnBackPressedCallback(false) {
        override fun handleOnBackPressed() { closeMushaf() }
    }''')
replace(activity,
        '        wireUi()\n        updateRepeatButton()',
        '        wireUi()\n        setupMushaf()\n        updateRepeatButton()')
replace(activity,
        '    private fun connectController() {',
        '''    private fun setupMushaf() {
        onBackPressedDispatcher.addCallback(this, mushafBackCallback)
        b.mushafPager.orientation = ViewPager2.ORIENTATION_VERTICAL
        b.mushafPager.adapter = MushafPageAdapter(repo) { page ->
            if (page < 604) b.mushafPager.currentItem = page
        }
        b.mushafPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                val page = position + 1
                prefs.edit().putInt("mushaf_page", page).apply()
                b.mushafPageIndicator.text = "الصفحة ${arabicNumber(page)} من ٦٠٤ · اسحب للأعلى"
            }
        })
        b.btnMushaf.setOnClickListener {
            b.mushafOverlay.visibility = View.VISIBLE
            mushafBackCallback.isEnabled = true
            val savedPage = prefs.getInt("mushaf_page", 1).coerceIn(1, 604)
            b.mushafPager.setCurrentItem(savedPage - 1, false)
        }
        b.mushafClose.setOnClickListener { closeMushaf() }
        b.mushafPrevious.setOnClickListener {
            val current = b.mushafPager.currentItem
            if (current > 0) b.mushafPager.currentItem = current - 1
        }
        b.mushafNext.setOnClickListener {
            val current = b.mushafPager.currentItem
            if (current < 603) b.mushafPager.currentItem = current + 1
        }
        b.mushafAudio.setOnClickListener { togglePlay() }
    }

    private fun closeMushaf() {
        b.mushafOverlay.visibility = View.GONE
        mushafBackCallback.isEnabled = false
    }

    private fun connectController() {''')

print("Quran Premium v1.4 Mushaf beta patch applied. Existing audio/player code retained.")
