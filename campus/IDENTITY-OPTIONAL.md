# Optional identity and synchronization / Identidad y sincronización opcionales

**Architecture reference only: not implemented or enabled by Campus 2.3.**

## Español

La edición estática no pide correo ni crea cuentas. El enlace de progreso es una copia voluntaria sin notas ni tokens, no una sesión autenticada. No se debe compartir una cookie de sesión o credencial en una URL para moverla entre equipos.

Cloudflare Access One-time PIN es una posible vía administrada para permitir acceso mediante correo y código, con políticas de acceso explícitas. Controlar acceso no crea automáticamente un repositorio de progreso. Antes de activarlo deben definirse usuarios admitidos, dominios, duración de sesión, recuperación, privacidad, retención, borrado y responsable del tratamiento. No configurar acceso universal al correo sin revisar el alcance.

Una sincronización real necesitaría backend: API de progreso con autorización por usuario en cada lectura/escritura, validación de tokens del proveedor, claves de verificación rotables y comprobación de emisor/audiencia/expiración. No confiar en un encabezado de identidad aportado directamente por el cliente. Almacenar datos mediante consultas parametrizadas y separar progreso de identidad; minimizar correos y no guardar notas por defecto. Gestionar versiones y conflictos mediante revisión/ETag, limitar tamaño y tasa, auditar sin registrar tokens y permitir exportación/borrado. Cookies seguras, SameSite y protección CSRF cuando proceda.

Un enlace autenticado de un solo uso, si se implementa, debe usar token opaco de alta entropía, caducidad de servidor, almacenamiento de hash, consumo atómico y protección contra intentos repetidos. Los previsualizadores de enlaces de correo/mensajería no deben consumirlo mediante una visita GET. Nunca introducir JWT o cookies de otra sesión en el enlace compartido.

Pruebas de aceptación requeridas: usuario A no lee/escribe datos B, token vencido o de audiencia distinta rechazado, revocación, replay, rate limiting, conflicto entre dispositivos, caída del proveedor, sesión cerrada, exportación y supresión. La cuenta y los permisos reales del proveedor deben prepararse y comprobarse antes de exponerlo. No sustituir esas pruebas por un formulario visual.

## English

The static release has no email account system. Progress links are voluntary snapshots, not authentication. Never place session cookies, reusable authentication tokens or another device's session in a shared URL.

Cloudflare Access One-time PIN is one possible managed email-code access mechanism. Access control alone does not synchronize learning records. Real synchronization requires an authenticated API with per-user authorization, token issuer/audience/expiry validation, server-side limits, parameterized storage, minimal identity data and a documented retention/deletion policy. Conflict handling must preserve newer records and make merges explicit.

A future single-use transfer needs an opaque random token, server-enforced expiry, hashed token storage, atomic consumption, replay/rate protection and a confirmation action that mail link-preview crawlers cannot trigger with GET. Test ownership isolation, token failure cases, logout, provider outages and data export/deletion before enabling. No identity service or database is deployed by this repository change.

References: [Access One-time PIN](https://developers.cloudflare.com/cloudflare-one/identity/one-time-pin/), [Access JWT validation](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/), [progress snapshot model](PROGRESO.md).
