# Control operativo de sistemas / Operating-system operational control

Edición 21-09-2026. Cuatro lecturas integradas como D22–D25 al final de la biblioteca; D01–D21 conservan sus identificadores. El programa activo mantiene M01–M32, L01A–L32C y 480 horas. Las lecturas complementan contenido existente: no sustituyen los módulos ni añaden marcas de progreso.

| Recurso | Español | English |
|---|---|---|
| D22 | [Identidades, perfiles y bastionado](01-identidad-bastionado.md) | [Parallel teaching edition](../../../campus/locales/en/operations-control.md) |
| D23 | [Redes, permisos y recursos compartidos](02-redes-recursos.md) | [Parallel teaching edition](../../../campus/locales/en/operations-control.md) |
| D24 | [Navegación, cuentas y TLS](03-navegacion-tls.md) | [Parallel teaching edition](../../../campus/locales/en/operations-control.md) |
| D25 | [Detección, controles y laboratorios](04-deteccion-laboratorios.md) | [Parallel teaching edition](../../../campus/locales/en/operations-control.md) |

La ampliación deriva del encargo de profundizar detección, administración/bastionado, identidades locales/LDAP/AD, perfiles, redes/recursos y políticas de navegación. Su diseño docente añade una matriz de 16 controles, ocho reglas ilustrativas de navegación y doce escenarios de aceptación. No se ha ejecutado una instalación nativa de esas políticas en equipos de alumnos ni se ha inspeccionado tráfico personal.

## Contrato de evidencia

Para cada control registrar objetivo, activo, sujeto, contexto, configuración efectiva, prueba permitida y denegada, fuente/hora, límites, excepción, aprobador y recuperación. Un estado desconocido no es conforme; un control instalado no es necesariamente efectivo. Las rúbricas y métricas son propuestas de enseñanza, no certificación legal.

## Fuentes y cambios de versión

Las fuentes primarias se enlazan junto al concepto en las cuatro lecturas: Microsoft para identidades, LAPS, SMB, Sysmon y restricciones de tenant; Ubuntu para SSSD; Samba y FreeIPA para sus implementaciones; Apple para filtrado gestionado; Cloudflare para TLS/HTTP3; WhatsApp para E2EE; Wazuh para evaluación de configuración; NIST para respuesta; BOE para garantías de privacidad. Los nombres de productos son ejemplos, no requisitos de compra.

Registrar las versiones realmente instaladas antes de impartir cada escenario. No se presume que las opciones, licencias o cobertura sean idénticas entre sistemas, ediciones o versiones. El análisis de aplicabilidad legal de una implantación concreta corresponde a sus responsables.

## Publicación y verificación

`campus/audit_publication.py` realiza únicamente siete GETs fijos al campus público, con validación TLS normal, sin credenciales ni redirecciones seguidas. Sus observaciones incluyen estado HTTP, MIME, hashes y metadatos públicos de versión. No es un pentest, un rastreador ni una prueba de todas las funciones del navegador.

La comprobación inicial del 21-09-2026, 08:07 UTC, obtuvo 200 en portada, build-info, ambos catálogos, JavaScript y CSS, y 404 en la ruta de prueba inexistente. El build servido identificaba `beae889a580b3bd36864eb19bb05760d232ff805`, versión 2.3.0 y 21 recursos. Es una observación anterior a esta ampliación, no una afirmación de que D22–D25 ya estuvieran publicados.

La aceptación de nuevas lecturas combina pruebas estructurales, invariantes de IDs/horas y pruebas de navegador Chromium/WebKit en CI. Una simulación de anchura no equivale a un iPad físico. La evidencia de cada ejecución se conserva en sus artefactos; no se confunde construir, fusionar y publicar.

## English handover

This extension appends D22–D25 without changing core module/lab IDs, hours or progress storage. It contains full parallel readings, sixteen control checks, eight illustrative browsing rules and twelve lab designs. Native OS control deployment is not claimed. Public HTTP observation and browser acceptance are separate evidence types. Existing Cloudflare routing and deployment commands are preserved.
