# Inventario publicable y trazabilidad

El ZIP descargable del kit usa una lista explícita de once archivos revisados en `release_inputs.py`, no un recorrido recursivo por el laboratorio del alumno. Incluye scripts, README, Compose/Swarm, Dockerfile y .dockerignore. Los archivos añadidos bajo `mi-laboratorio-local`, ficheros .env y otros nombres no declarados no entran en esa descarga. Al ampliar el kit, revisar contenido y añadir expresamente el nombre; no convertir la lista en un glob general.

La identificación del commit se obtiene antes de recopilar fuentes y generar activos. Un checkout con cambios rastreados, nuevos ficheros o entradas ignoradas potencialmente relevantes se considera no atribuible a un commit limpio y produce `sourceCommit: null`. Los artefactos generados en `campus/dist`, QA y cachés de Python no son nuevas fuentes. Sin Git no se inventa procedencia. Esta comprobación no sustituye revisar el contenido de archivos ya rastreados ni acredita autoría o inocuidad de los materiales.

Las pruebas de procedencia utilizan repositorios Git temporales reales; las de empaquetado comprueban lista exacta, exclusión de notas locales, archivos ausentes, tamaño máximo y enlaces simbólicos. Un manifiesto SHA-256 verifica los bytes incluidos; no constituye una firma digital.

Los logs originales de Cloudflare se conservan fuera del repositorio público. El campus no incorpora secretos, expedientes o notas del navegador al despliegue. Los metadatos de build y las cifras son públicos. Ver también [despliegue](DEPLOY-CLOUDFLARE.md) y [progreso](PROGRESO.md).
