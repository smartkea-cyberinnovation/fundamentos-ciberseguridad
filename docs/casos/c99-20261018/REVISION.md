# Revisión y límites · 2026-10-18

## Procedencia y fechas

El dossier recibido declara internamente `2026-09-30`. Esa fecha se conserva como metadato del artefacto, no como adquisición independiente acreditada ni como fecha de esta revisión. El ZIP original no se modifica.

- ZIP de referencia SHA-256: `dac410237c57bb6eab50ea7f64be8f44182356117f5dc128517a1b01db769248`.
- 43 miembros en el ZIP; CRC correcto; 42 entradas del manifiesto verificadas, cero diferencias.
- PHP canónico: 395291 bytes; SHA-256 `1e07598c2e41b7827840ba6c8611912abd88c0344a5d1eff364eaabeccdc6420`.
- El PHP con exactamente un LF final tiene SHA-256 `2e89c9c01290c9b2d6979d778fed1868d43aacaad1bd9df1dcc60bf11542b338`.
- Identidad de publicación documentada: repositorio `c99-shell/c99`, commit `ff62d07db6b99284ad90c2c97f143cd64fe51727`, blob `7f95818a5608c930b2c1fc27e7b824347a226053`.

## Representación y comportamiento

El dossier cuenta 2783 literales constantes, 35729 escapes hexadecimales, 35215 octales, 2301 instrucciones goto, 2435 etiquetas y 34 declaraciones de función. Son métricas de representación, no indicadores de ejecución. Los 47 recursos Base64 examinados se validaron estructuralmente como GIF; esto no demuestra ausencia universal de esteganografía.

El preámbulo reconstruye esquema + HTTP_HOST + REQUEST_URI y prepara un POST al receptor. El intento está antes del login. La rama de subida inicial sale antes del callback. El actualizador tiene una rama eval distinta, con URL base vacía por defecto. No se reconstruye ni publica una shell ejecutable.

No existe un PHP padre recuperado de ese repositorio que permita atribuir las modificaciones al ofuscador. La cuenta que publica un commit no acredita quién escribió el código ni quién controla el dominio.

## Comprobaciones de esta revisión

El 2026-10-18 se reejecutaron las 10 pruebas del triage offline, todas superadas, y se verificó el manifiesto original. No se ejecutó la webshell ni se contactó con el receptor. YARA/Suricata no estaban disponibles en el entorno; Sigma no se convirtió ni se probó contra un backend real. Las validaciones históricas adicionales del PDF/HTML/GIF siguen identificadas como resultados declarados del dossier, no como repeticiones de esta revisión.

## Pendientes

La issue #8 mantiene validación de motores y eventos sintéticos, enriquecimiento pasivo fresco, determinación de un posible entorno afectado y revisión/integración docente. Los datos de infraestructura del dossier no se presentan como DNS vivo de esta revisión. No bloquear IP compartidas automáticamente. No hay prueba de incidente real.

## Fuentes

El dossier neutralizado y sus mapas son la base de esta edición. Fuente pública de procedencia: https://github.com/c99-shell/c99/commit/ff62d07db6b99284ad90c2c97f143cd64fe51727 . Documentación de semántica: https://www.php.net/manual/en/function.extract.php y https://www.php.net/manual/en/function.unserialize.php . Antecedente histórico citado por el dossier: https://github.com/SpiderLabs/owasp-modsecurity-crs/issues/189 . Estas referencias no convierten los dominios citados en destinos para pruebas activas.
