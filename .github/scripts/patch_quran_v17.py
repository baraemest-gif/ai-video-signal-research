#!/usr/bin/env python3
"""Quran Premium v1.7: readable Arabic nav, safe insets, immersive mode, pinch zoom.

Never modifies Quran page images, verse data, or audio sources.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "quran-premium-android")
app = root / "app"
source = app / "src/main"


def replace(path, old, new):
    original = path.read_text(encoding="utf-8")
    if old not in original:
        raise RuntimeError(f"v1.7 patch anchor missing: {path}: {old[:100]}")
    path.write_text(original.replace(old, new, 1), encoding="utf-8")


gradle = app / "build.gradle.kts"
replace(gradle, 'applicationId = "com.quran.premium.mushafcontrastbeta"',
        'applicationId = "com.quran.premium.mushafreaderbeta"')
replace(gradle, 'versionCode = 106', 'versionCode = 107')
replace(gradle, 'versionName = "1.6.0-contrast-beta"',
        'versionName = "1.7.0-reader-beta"')

manifest = source / "AndroidManifest.xml"
replace(manifest, 'android:label="القرآن الكريم · خط واضح"',
        'android:label="القرآن الكريم · قراءة مريحة"')

themes = source / "res/values/themes.xml"
replace(themes, '        <item name="android:textSize">13sp</item>\n        <item name="android:textAllCaps">false</item>\n        <item name="android:minWidth">0dp</item>\n        <item name="android:insetLeft">0dp</item>\n        <item name="android:insetRight">0dp</item>\n    </style>',
        '        <item name="android:textSize">14sp</item>\n        <item name="android:textAllCaps">false</item>\n        <item name="android:minWidth">0dp</item>\n        <item name="android:paddingLeft">2dp</item>\n        <item name="android:paddingRight">2dp</item>\n        <item name="android:insetLeft">0dp</item>\n        <item name="android:insetRight">0dp</item>\n    </style>')

layout = source / "res/layout/activity_main.xml"
replace(layout, 'android:padding="9dp">\n            <com.google.android.material.button.MaterialButton\n                android:id="@+id/mushafClose"',
        'android:padding="7dp">\n            <com.google.android.material.button.MaterialButton\n                android:id="@+id/mushafFullScreen"\n                style="@style/Widget.QuranPremium.MushafNav"\n                android:layout_width="wrap_content"\n                android:layout_height="48dp"\n                android:text="عرض كامل" />\n            <com.google.android.material.button.MaterialButton\n                android:id="@+id/mushafClose"')
replace(layout, 'android:text="الصفحة ١ من ٦٠٤"\n                android:textColor="#382B1C"\n                android:textSize="17sp"',
        'android:text="ص ١ / ٦٠٤"\n                android:textColor="#382B1C"\n                android:maxLines="1"\n                android:textSize="16sp"')

start = layout.read_text(encoding="utf-8")
begin = start.index('        <!-- Arabic indices and reading bookmarks, like a printed-Mushaf reader. -->')
end = start.index('    </LinearLayout>\n\n</androidx.constraintlayout.widget.ConstraintLayout>', begin)
new_controls = '''        <!-- Full labels in spacious rows prevent Arabic clipping on small phones. -->
        <LinearLayout
            android:id="@+id/mushafToolsPrimary"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:paddingHorizontal="5dp">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafIndex"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="الفهرس" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafJuz"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="الأجزاء" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafGoPage"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="46dp"
                android:layout_weight="1"
                android:text="الصفحات" />
        </LinearLayout>

        <LinearLayout
            android:id="@+id/mushafToolsSecondary"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:paddingHorizontal="5dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafSave"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="حفظ الصفحة" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafSaved"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="العلامة المحفوظة" />
        </LinearLayout>

        <LinearLayout
            android:id="@+id/mushafNavigationBar"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:padding="7dp">
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafPrevious"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="السابق" />
            <Space android:layout_width="6dp" android:layout_height="1dp" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafAudio"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="▶ الصوت" />
            <Space android:layout_width="6dp" android:layout_height="1dp" />
            <com.google.android.material.button.MaterialButton
                android:id="@+id/mushafNext"
                style="@style/Widget.QuranPremium.MushafNav"
                android:layout_width="0dp"
                android:layout_height="48dp"
                android:layout_weight="1"
                android:text="التالي" />
        </LinearLayout>
'''
layout.write_text(start[:begin] + new_controls + start[end:], encoding="utf-8")

page_layout = source / "res/layout/item_mushaf_page.xml"
replace(page_layout, '<ImageView\n            android:id="@+id/mushafImage"',
        '<com.quran.premium.ZoomableMushafImageView\n            android:id="@+id/mushafImage"')

adapter = source / "java/com/quran/premium/MushafPageAdapter.kt"
replace(adapter, 'import android.widget.ImageView\n', '')
replace(adapter, 'val image: ImageView = itemView.findViewById(R.id.mushafImage)',
        'val image: ZoomableMushafImageView = itemView.findViewById(R.id.mushafImage)')
replace(adapter, 'holder.image.setImageDrawable(null)\n',
        'holder.image.resetZoom()\n        holder.image.setImageDrawable(null)\n')

zoom = source / "java/com/quran/premium/ZoomableMushafImageView.kt"
zoom.write_text('''package com.quran.premium

import android.content.Context
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.appcompat.widget.AppCompatImageView
import kotlin.math.max

/** Pinch zoom and one-finger pan at zoom > 1; vertical pager works at zoom 1. */
class ZoomableMushafImageView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : AppCompatImageView(context, attrs) {
    private var zoom = 1f
    private var lastX = 0f
    private var lastY = 0f
    private var isPanning = false
    private val pinch = ScaleGestureDetector(context, object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScaleBegin(detector: ScaleGestureDetector): Boolean {
            parent?.requestDisallowInterceptTouchEvent(true)
            return true
        }
        override fun onScale(detector: ScaleGestureDetector): Boolean {
            zoom = (zoom * detector.scaleFactor).coerceIn(1f, 3.5f)
            pivotX = width / 2f
            pivotY = height / 2f
            scaleX = zoom
            scaleY = zoom
            constrainTranslation()
            parent?.requestDisallowInterceptTouchEvent(zoom > 1f)
            return true
        }
    })

    init { isClickable = true }

    fun resetZoom() {
        zoom = 1f
        scaleX = 1f
        scaleY = 1f
        translationX = 0f
        translationY = 0f
        isPanning = false
    }

    private fun constrainTranslation() {
        val limitX = max(0f, width * (zoom - 1f) / 2f)
        val limitY = max(0f, height * (zoom - 1f) / 2f)
        translationX = translationX.coerceIn(-limitX, limitX)
        translationY = translationY.coerceIn(-limitY, limitY)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                lastX = event.x
                lastY = event.y
                isPanning = false
                parent?.requestDisallowInterceptTouchEvent(zoom > 1f)
            }
            MotionEvent.ACTION_POINTER_DOWN -> {
                parent?.requestDisallowInterceptTouchEvent(true)
            }
        }
        pinch.onTouchEvent(event)
        if (event.actionMasked == MotionEvent.ACTION_MOVE && zoom > 1f && event.pointerCount == 1 && !pinch.isInProgress) {
            val dx = event.x - lastX
            val dy = event.y - lastY
            if (kotlin.math.abs(dx) + kotlin.math.abs(dy) > 2f) isPanning = true
            translationX += dx
            translationY += dy
            constrainTranslation()
            parent?.requestDisallowInterceptTouchEvent(true)
            lastX = event.x
            lastY = event.y
            return true
        }
        if (event.actionMasked == MotionEvent.ACTION_POINTER_UP) {
            lastX = event.x
            lastY = event.y
        }
        if (event.actionMasked == MotionEvent.ACTION_UP || event.actionMasked == MotionEvent.ACTION_CANCEL) {
            parent?.requestDisallowInterceptTouchEvent(false)
            if (zoom > 1f || isPanning) return true
        }
        return if (zoom > 1f || event.pointerCount > 1 || pinch.isInProgress) true else super.onTouchEvent(event)
    }
}
''', encoding="utf-8")

activity = source / "java/com/quran/premium/MainActivity.kt"
replace(activity, 'import androidx.core.view.setPadding\n',
        'import androidx.core.view.setPadding\nimport androidx.core.view.ViewCompat\nimport androidx.core.view.WindowInsetsCompat\n')
replace(activity, '        setContentView(b.root)\n', '''        setContentView(b.root)
        // Android 15/16 edge-to-edge: reader/header must sit below the system status bar.
        ViewCompat.setOnApplyWindowInsetsListener(b.root) { view, windowInsets ->
            val bars = windowInsets.getInsets(WindowInsetsCompat.Type.systemBars())
            view.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            windowInsets
        }
        ViewCompat.requestApplyInsets(b.root)
''')
replace(activity, '"الصفحة ${arabicNumber(page)} من ٦٠٤ · اسحب للأعلى"',
        '"ص ${arabicNumber(page)} / ٦٠٤"')
replace(activity, '        b.mushafClose.setOnClickListener { closeMushaf() }', '''        b.mushafFullScreen.setOnClickListener {
            val show = b.mushafToolsPrimary.visibility == View.GONE
            val visibility = if (show) View.VISIBLE else View.GONE
            b.mushafToolsPrimary.visibility = visibility
            b.mushafToolsSecondary.visibility = visibility
            b.mushafNavigationBar.visibility = visibility
            b.mushafFullScreen.text = if (show) "عرض كامل" else "القوائم"
        }
        b.mushafClose.setOnClickListener { closeMushaf() }''')

print("Quran Premium v1.7: readable full Arabic labels, proper insets, immersive reader, pinch zoom; sacred pages unchanged.")
