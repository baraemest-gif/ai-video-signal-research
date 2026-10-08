# Quran Premium Native

This branch is isolated from main and is used only to build the native Android Quran app.

Why native:
- Android can suspend browser/PWA audio when the screen is off.
- The native build uses Media3/ExoPlayer inside a MediaSessionService with foreground media playback.
- Playback state, current surah, reader and position are persisted.
- Audio has primary, backup and Cloudflare proxy sources.
- A watchdog rotates source without losing position if playback stalls.

Build output:
The GitHub Actions workflow produces a debug APK artifact named `quran-premium-debug-apk`.

The source project is stored in `quran-premium-project.tar.gz.b64`; the workflow decodes and builds it.
