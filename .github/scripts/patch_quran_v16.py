#!/usr/bin/env python3
"""High-contrast labels on boxed Madani reader navigation, no verse/image changes."""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "quran-premium-android")
app = root / "app"


def replace(path, before, after):
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    if before not in source:
        raise RuntimeError(f"Expected v15 anchor missing from {path}: {before[:80]}")
    path.write_text(source.replace(before, after, 1), encoding="utf-8")


gradle = app / "build.gradle.kts"
replace(gradle, 'applicationId = "com.quran.premium.mushafcalligraphy"',
        'applicationId = "com.quran.premium.mushafcontrastbeta"')
replace(gradle, 'versionCode = 105', 'versionCode = 106')
replace(gradle, 'versionName = "1.5.0-madani-beta"',
        'versionName = "1.6.0-contrast-beta"')

manifest = app / "src/main/AndroidManifest.xml"
replace(manifest, 'android:label="القرآن الكريم · مصحف المدينة"',
        'android:label="القرآن الكريم · خط واضح"')

themes = app / "src/main/res/values/themes.xml"
replace(themes, '    <style name="Widget.QuranPremium.Round"', '''    <!-- Separate high-contrast controls for light parchment reading mode. -->
    <style name="Widget.QuranPremium.MushafNav" parent="Widget.Material3.Button">
        <item name="backgroundTint">#172E4F</item>
        <item name="android:textColor">#FFFFFF</item>
        <item name="strokeColor">#D8AF64</item>
        <item name="strokeWidth">1dp</item>
        <item name="cornerRadius">11dp</item>
        <item name="android:textStyle">bold</item>
        <item name="android:textSize">13sp</item>
        <item name="android:textAllCaps">false</item>
        <item name="android:minWidth">0dp</item>
        <item name="android:insetLeft">0dp</item>
        <item name="android:insetRight">0dp</item>
    </style>

    <style name="Widget.QuranPremium.Round"''')

layout = app / "src/main/res/layout/activity_main.xml"
for button_id in (
    "mushafClose", "mushafIndex", "mushafJuz", "mushafGoPage",
    "mushafSave", "mushafSaved", "mushafPrevious", "mushafAudio", "mushafNext"
):
    replace(layout, f'android:id="@+id/{button_id}"\n                style="@style/Widget.QuranPremium.Chip"',
            f'android:id="@+id/{button_id}"\n                style="@style/Widget.QuranPremium.MushafNav"')

print("Quran Premium v1.6 high-contrast navigation applied; Quran images and audio unchanged.")
