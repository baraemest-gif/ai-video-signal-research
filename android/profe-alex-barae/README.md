# Profe Alex — Barae — Android

Aplicación nativa Android que muestra Profe Alex para Barae sin barras del navegador.

URL oficial: https://profe-alex.baraemest.workers.dev/

Incluye la foto auténtica de Profe Alex, el diseño Arcoíris y las 28 actividades porque utiliza el mismo backend de Cloudflare Workers y la misma base de datos, no una copia nueva.

Funciones del contenedor: navegación HTTPS aislada, almacenamiento del perfil en WebView, fotos de la cámara/galería, reconocimiento de voz nativo (cuando Android tenga el servicio instalado), pantalla de reconexión y tecla Atrás.

**Requiere Internet** para el tutor y las respuestas de IA.

En cada compilación, GitHub Actions genera un APK de prueba firmado automáticamente; no es un APK de Google Play ni usa una clave de firma de publicación persistente. Para actualizar futuras versiones sin desinstalar y conservar los datos locales, configure una clave de firma de producción protegida.

El código está aislado en `android/profe-alex-barae` y no modifica el proyecto AI Video Signal.
