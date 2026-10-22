# Quran — Ahmed Akl preview (separate Android APK)

This is a **separate test app**, NOT a patched or updated version of Quran-Premium-Native. It uses a different package name and does not uninstall, modify, or share data with the user's original Quran APK.

- "تلاوات أحمد عقل": opens the publicly accessible Ahmed Akl recitation page at Assabile, with 60 available surahs. **Not all 114 surahs are available**.
- "قراءة القرآن": opens Assabile's Quran reading page.
- Requires internet access; audio is played by the provider's website. No audio files are redistributed.
- Does **not** claim native per-ayah audio synchronization, guaranteed background audio, download/offline functionality, or the exact UI/features of Quran-Premium-Native.
- Debug APK for personal testing only; signed with Android's generated debug key, not the original app's signing key.

Build: `gradle :app:assembleDebug --no-daemon` on an Android SDK-enabled system.
