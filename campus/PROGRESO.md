# Progreso y traspaso / Progress and transfer

## Español

### Qué se guarda

La clave histórica `fundamentos-ciberseguridad:progress:v1` conserva lecturas, autoevaluaciones, favoritos, notas y las cinco fases/finalización de cada práctica. El porcentaje usa los 160 hitos del catálogo actual, no horas. `sessionStorage` mantiene el último punto de cada pestaña. Sin almacenamiento disponible se informa del problema: exporta antes de cerrar. Una copia local inválida no se sobrescribe automáticamente; se permite descargar el original para recuperación.

### Tres operaciones distintas

**Compartir lección:** copia URL con idioma y módulo/práctica; no incluye hitos ni notas.

**Enlace de progreso:** desde «Continuar en otro dispositivo», pulsar «Crear enlace de progreso». Elige copiar, compartir con el sistema, correo, WhatsApp o Telegram. El receptor ve una vista previa y debe confirmar «Combinar y continuar». Se unen las marcas, se conservan sus notas y se adopta el punto recibido. No se instala una cuenta ni se recuperan automáticamente cambios posteriores.

**JSON completo:** exporta también notas; consérvalo de forma privada. La importación valida estructura, catálogo y tamaño máximo de 1 MiB UTF-8; requiere confirmación porque sustituye el estado local. No compartirlo públicamente.

### Seguridad del enlace

El payload contiene únicamente versión, ID y disposición del catálogo, fecha de creación/caducidad, idioma, ruta validada, indicadores de módulo y fases de laboratorio. Excluye notas, direcciones de correo, identificadores personales, cookies, contraseñas y tokens de sesión.

Se cifra con AES-GCM y aleatorios nuevos por enlace. **La clave viaja en el propio enlace: quien tenga la URL completa puede leer e importar la copia.** También puede hacerlo el servicio de mensajería al que voluntariamente se envíe. El cifrado no acredita identidad, autoría ni realización de las prácticas. Los hitos siguen siendo autodeclarados.

El fragmento `#` no se envía en una solicitud HTTP ordinaria al servidor del campus. El cliente lo retira de la barra antes de mostrar la vista previa. Esto no elimina copias del historial, extensiones o mensajería. La aplicación no registra ni sube el enlace a un servidor de progreso. Cualquier script del mismo origen o extensión con permisos apropiados sigue dentro del modelo de confianza del navegador.

Caducidad predeterminada: 24 horas, comprobada por el reloj del cliente; no es revocable ni de un solo uso. No utilizar como enlace de acceso a información sensible. Se rechazan payloads alterados, demasiado grandes, caducados, con IDs/orden de catálogo distintos, campos extra o rutas ajenas al curso. Crear enlaces requiere Web Crypto en HTTPS o localhost; la alternativa es JSON.

Un enlace es una instantánea. Para unir cambios posteriores, crea otra copia. No enviar sesiones de autenticación en URLs. [OTP e identidad opcional](IDENTITY-OPTIONAL.md) es otra arquitectura no habilitada.

### Ejemplo

En móvil: leer M05, confirmar lectura, abrir continuidad y crear enlace. Enviar a tu propio correo o dispositivo; abrirlo en el portátil, revisar hitos y confirmar. La lectura aparece marcada y puedes empezar la práctica local. Las notas del móvil no han salido con el enlace; trasládalas únicamente mediante una copia JSON privada cuando proceda.

## English

The historical v1 key retains readings, self-checks, bookmarks, notes and lab phases. Progress is self-reported, not attendance or proof of competence. Session storage keeps each tab's resume location; blocked storage has an in-memory fallback and requires a manual export before closing.

**Share lesson** copies a language-aware deep link without learning records. **Continue on another device** creates a snapshot of milestones, bookmarks, lab phases, language and resume location. The receiving browser previews it and requires confirmation before merging; current notes are preserved. **JSON backup** includes notes and replaces local state only after validation and confirmation.

Portable links exclude notes, email, cookies, passwords and session tokens. AES-GCM protects the encoded payload against accidental modification, but **the encryption key is part of the same URL**: anyone holding it can read/import it, including a messaging service you choose. This is not identity verification or authenticated progress. The fragment is removed from the address bar after reading, not from all browser or third-party copies.

The application checks a default 24-hour expiry using the client clock. Links are not revocable or single-use, and later changes do not synchronize. Validations reject incompatible catalogues, unexpected fields, invalid routes and oversized data. Use HTTPS/Web Crypto or a private JSON backup. JSON notes are unencrypted; do not store secrets or real personal data in the notebook.

## Sources for platform behavior

- [URI fragments](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment)
- [Web Share API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API)
- [SubtleCrypto](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto)

The file describes implemented behavior, not a cryptographic or legal certification. Tests and their execution status are in [QA.md](QA.md).
