#!/usr/bin/env python3
"""Quran Premium v1.5 beta: Madani page images + Arabic navigation index.

Apply after v12, v13, v14. Keeps old installations and foreground audio unchanged.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "quran-premium-android")
app = root / "app"
java = app / "src/main/java/com/quran/premium"
res = app / "src/main/res"


def edit(path, old, new):
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    if old not in raw:
        if new in raw:
            return
        raise RuntimeError(f"Patch anchor absent from {path}: {old[:90]}")
    path.write_text(raw.replace(old, new, 1), encoding="utf-8")


def put(path, content):
    Path(path).write_text(content, encoding="utf-8")


edit(app / "build.gradle.kts", 'applicationId = "com.quran.premium.mushafbeta"',
     'applicationId = "com.quran.premium.mushafcalligraphy"')
edit(app / "build.gradle.kts", 'versionCode = 104', 'versionCode = 105')
edit(app / "build.gradle.kts", 'versionName = "1.4.0-mushaf-beta"',
     'versionName = "1.5.0-madani-beta"')
edit(app / "src/main/AndroidManifest.xml", 'android:label="القرآن الكريم · مصحف تجريبي"',
     'android:label="القرآن الكريم · مصحف المدينة"')

put(java / "data/MushafImages.kt", '''package com.quran.premium.data

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Handler
import android.os.Looper
import android.util.LruCache
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

/** High-resolution Madani page artwork, cached locally after first view.
 * Artwork: Quran.com image generator / King Fahd Quran Complex;
 * hosted by the public akram-seid/quran-hd-images collection (604 pages).
 */
class MushafImages(context: Context) {
    private val executor = Executors.newFixedThreadPool(2)
    private val main = Handler(Looper.getMainLooper())
    private val directory = File(context.filesDir, "mushaf-hd-images").also { it.mkdirs() }
    private val memory = object : LruCache<Int, Bitmap>(32 * 1024 * 1024) {
        override fun sizeOf(key: Int, value: Bitmap): Int = value.byteCount
    }

    fun load(page: Int, ok: (Bitmap) -> Unit, failed: (Throwable) -> Unit) {
        require(page in 1..604)
        memory.get(page)?.let { bitmap ->
            main.post { ok(bitmap) }
            return
        }
        executor.execute {
            try {
                val sourceFile = File(directory, "${page.toString().padStart(3, '0')}.jpg")
                if (!sourceFile.exists() || sourceFile.length() < 20000) {
                    val temp = File(directory, "${page.toString().padStart(3, '0')}.download")
                    val endpoint = "https://raw.githubusercontent.com/akram-seid/quran-hd-images/main/images/${page.toString().padStart(3, '0')}.jpg"
                    val conn = URL(endpoint).openConnection() as HttpURLConnection
                    conn.connectTimeout = 8500
                    conn.readTimeout = 16000
                    try {
                        check(conn.responseCode in 200..299) { "Image HTTP ${conn.responseCode}" }
                        conn.inputStream.use { input -> temp.outputStream().use { output -> input.copyTo(output) } }
                    } finally {
                        conn.disconnect()
                    }
                    require(temp.length() > 20000) { "Incomplete Mushaf page $page" }
                    check(temp.renameTo(sourceFile)) { "Could not cache Mushaf page $page" }
                }
                var bitmap = BitmapFactory.decodeFile(sourceFile.absolutePath)
                    ?: error("Unreadable Mushaf page image $page")
                require(bitmap.width >= 800 && bitmap.height >= 1000) { "Invalid Mushaf page $page" }
                // Al-Fatihah occupies the upper portion of page 1; trim blank lower margin.
                if (page == 1) bitmap = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, (bitmap.height * 0.65).toInt())
                memory.put(page, bitmap)
                main.post { ok(bitmap) }
            } catch (t: Throwable) {
                main.post { failed(t) }
            }
        }
    }
}
''')

put(java / "MushafPageAdapter.kt", '''package com.quran.premium

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.quran.premium.data.MushafImages

/** 604 authentic typeset Madani pages; swipe up/down via vertical ViewPager2. */
class MushafPageAdapter(
    private val images: MushafImages,
    private val onPageTap: (Int) -> Unit
) : RecyclerView.Adapter<MushafPageAdapter.PageHolder>() {
    class PageHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val image: ImageView = itemView.findViewById(R.id.mushafImage)
        val message: TextView = itemView.findViewById(R.id.mushafLoading)
        val footer: TextView = itemView.findViewById(R.id.mushafPageFooter)
        var boundPage = -1
    }

    override fun getItemCount(): Int = 604

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PageHolder =
        PageHolder(LayoutInflater.from(parent.context).inflate(R.layout.item_mushaf_page, parent, false))

    override fun onBindViewHolder(holder: PageHolder, position: Int) {
        val page = position + 1
        holder.boundPage = page
        holder.image.setImageDrawable(null)
        holder.message.visibility = View.VISIBLE
        holder.message.text = "جارٍ تحميل صفحة المصحف…"
        holder.footer.text = "الصفحة ${arabicDigits(page)} من ٦٠٤"
        holder.image.setOnClickListener { onPageTap(page) }
        request(holder, page)
    }

    private fun request(holder: PageHolder, page: Int) {
        holder.message.setOnClickListener { request(holder, page) }
        holder.message.visibility = View.VISIBLE
        holder.message.text = "جارٍ تحميل الصفحة…"
        images.load(page, { bitmap ->
            if (holder.boundPage == page) {
                holder.image.setImageBitmap(bitmap)
                holder.message.visibility = View.GONE
            }
        }, {
            if (holder.boundPage == page) {
                holder.message.text = "تعذّر تحميل الصفحة. اضغط لإعادة المحاولة."
                holder.message.visibility = View.VISIBLE
            }
        })
    }

    private fun arabicDigits(value: Int): String = value.toString().map { char ->
        if (char in '0'..'9') "٠١٢٣٤٥٦٧٨٩"[char - '0'] else char
    }.joinToString("")
}
''')

put(res / "layout/item_mushaf_page.xml", '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F8F2E5"
    android:orientation="vertical"
    android:padding="5dp">

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:background="@drawable/bg_mushaf_sheet"
        android:padding="4dp">
        <ImageView
            android:id="@+id/mushafImage"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:contentDescription="صفحة من المصحف الشريف"
            android:scaleType="fitCenter"
            android:background="#FFFFFF" />

        <TextView
            android:id="@+id/mushafLoading"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:gravity="center"
            android:text="جارٍ تحميل صفحة المصحف…"
            android:textColor="#5B4828"
            android:textSize="19sp" />
    </FrameLayout>

    <TextView
        android:id="@+id/mushafPageFooter"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:textColor="#624C2D"
        android:textSize="14sp"
        android:padding="3dp" />
</LinearLayout>
''')

layout = res / "layout/activity_main.xml"
edit(layout, 'android:text="📖 قراءة المصحف · ٦٠٤ صفحة"',
     'android:text="📖 مصحف المدينة · خط عثماني وفهرس"')
edit(layout, '''        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:padding="7dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafPrevious"''',
     '''        <!-- Arabic indices and reading bookmarks, like a printed-Mushaf reader. -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:paddingHorizontal="4dp">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafIndex"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="الفهرس" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafJuz"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="الأجزاء" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafGoPage"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="الصفحات" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafSave"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="حفظ" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafSaved"
                style="@style/Widget.QuranPremium.Chip"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="علامتي" />
        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:padding="7dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafPrevious"''')

repo = java / "data/QuranRepository.kt"
edit(repo, '    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {',
     '''    /** Resolve a chapter or juz entry to its exact printed Madani page. */
    fun pageForAyah(surah: Int, ayah: Int, ok: (Int) -> Unit, failed: (Throwable) -> Unit) {
        executor.execute {
            try {
                require(surah in 1..114 && ayah > 0)
                val lookup = File(context.filesDir, "mushaf-index-$surah-$ayah.txt")
                val page = if (lookup.exists()) lookup.readText().trim().toInt() else {
                    val connection = URL("https://api.alquran.cloud/v1/ayah/$surah:$ayah/quran-uthmani")
                        .openConnection() as HttpURLConnection
                    connection.connectTimeout = 8500
                    connection.readTimeout = 12000
                    val raw = try {
                        check(connection.responseCode in 200..299)
                        connection.inputStream.bufferedReader().use { it.readText() }
                    } finally {
                        connection.disconnect()
                    }
                    val response = JSONObject(raw)
                    check(response.optInt("code") == 200)
                    response.getJSONObject("data").getInt("page").also { found ->
                        require(found in 1..604)
                        lookup.writeText(found.toString())
                    }
                }
                main.post { ok(page) }
            } catch (t: Throwable) {
                main.post { failed(t) }
            }
        }
    }

    fun timing(reader: Int, surah: Int, callback: (LongArray?) -> Unit) {''')

activity = java / "MainActivity.kt"
edit(activity, 'import android.text.InputType', 'import android.text.InputType\nimport com.quran.premium.data.MushafImages')
edit(activity,
     'b.mushafPager.adapter = MushafPageAdapter(repo) { page ->',
     'b.mushafPager.adapter = MushafPageAdapter(MushafImages(this)) { page ->')
edit(activity, '        b.mushafAudio.setOnClickListener { togglePlay() }',
     '''        b.mushafAudio.setOnClickListener { togglePlay() }
        b.mushafIndex.setOnClickListener { showMushafSurahIndex() }
        b.mushafJuz.setOnClickListener { showMushafJuzIndex() }
        b.mushafGoPage.setOnClickListener { showMushafGoPageDialog() }
        b.mushafSave.setOnClickListener {
            val page = b.mushafPager.currentItem + 1
            prefs.edit().putInt("mushaf_saved_bookmark", page).apply()
            Toast.makeText(this, "تم حفظ الصفحة ${arabicNumber(page)}", Toast.LENGTH_SHORT).show()
        }
        b.mushafSaved.setOnClickListener {
            val page = prefs.getInt("mushaf_saved_bookmark", 0)
            if (page in 1..604) goToMushafPage(page)
            else Toast.makeText(this, "احفظ الصفحة أولاً", Toast.LENGTH_SHORT).show()
        }''')
edit(activity, '    private fun closeMushaf() {',
     '''    private fun goToMushafPage(page: Int) {
        if (page in 1..604) b.mushafPager.setCurrentItem(page - 1, false)
    }

    private fun showMushafSurahIndex() {
        if (surahs.isEmpty()) {
            Toast.makeText(this, "انتظر تحميل فهرس السور", Toast.LENGTH_SHORT).show()
            return
        }
        val choices = surahs.map { "${arabicNumber(it.number)} · ${it.name}" }.toTypedArray()
        AlertDialog.Builder(this).setTitle("فهرس السور · ١١٤ سورة")
            .setItems(choices) { _, index -> locateMushafAyah(index + 1, 1) }
            .setNegativeButton("إغلاق", null).show()
    }

    private fun showMushafJuzIndex() {
        val labels = juzStarts.mapIndexed { idx, _ -> "الجزء ${arabicNumber(idx + 1)}" }.toTypedArray()
        AlertDialog.Builder(this).setTitle("فهرس الأجزاء · ٣٠ جزءًا")
            .setItems(labels) { _, index ->
                val (surah, ayah) = juzStarts[index]
                locateMushafAyah(surah, ayah)
            }.setNegativeButton("إغلاق", null).show()
    }

    private fun locateMushafAyah(surah: Int, ayah: Int) {
        Toast.makeText(this, "جارٍ فتح صفحة المصحف…", Toast.LENGTH_SHORT).show()
        repo.pageForAyah(surah, ayah, { page -> goToMushafPage(page) }, {
            Toast.makeText(this, "تعذّر تحديد الصفحة. تحقق من الإنترنت.", Toast.LENGTH_LONG).show()
        })
    }

    private fun showMushafGoPageDialog() {
        val input = EditText(this).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            hint = "من ١ إلى ٦٠٤"
            setText((b.mushafPager.currentItem + 1).toString())
        }
        AlertDialog.Builder(this).setTitle("الانتقال إلى صفحة")
            .setView(input)
            .setPositiveButton("انتقال") { _, _ ->
                val page = input.text.toString().toIntOrNull()
                if (page != null && page in 1..604) goToMushafPage(page)
                else Toast.makeText(this, "أدخل رقمًا من ١ إلى ٦٠٤", Toast.LENGTH_SHORT).show()
            }.setNegativeButton("إلغاء", null).show()
    }

    private fun closeMushaf() {''')

print("Applied Quran Premium v1.5 Madani images/index patch (separate install).")
