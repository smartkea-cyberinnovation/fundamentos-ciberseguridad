# TERM y herramientas de publicación · 28 de octubre de 2026

## Alcance

Revisión de TERM y de sus comprobaciones públicas, PR #32. Se conservan los contenidos, el Worker existente y las rutas. No se conecta una VM al curso ni se publica una shell.

## Actualización de la herramienta de despliegue

El audit del primer run del PR detectó avisos sobre Undici 7.29.1 transitivo a través de Miniflare en Wrangler 4.151.1. Son dependencias de desarrollo/publicación de `campus/tooling`, no bibliotecas enviadas al navegador del alumno. El resultado no demuestra explotación ni compromiso del sitio.

Se actualizan conjuntamente `campus/cloudflare.py`, `campus/tooling/package.json` y el lockfile generado por npm: Wrangler **4.154.0**, Miniflare **5.20261023.1-beta**, Undici **7.30.1**. No se utilizan overrides ni se desactiva el audit. Instalación mediante `npm ci --ignore-scripts` y métricas del CLI deshabilitadas. La versión que devuelve `python3 campus/cloudflare.py plan` es la referencia operativa actual; las menciones 4.151.1 en informes del 19 de octubre son evidencia histórica, no la versión vigente.

El lockfile se regeneró y auditó en Actions sin ejecutar scripts de paquetes. [Run de preparación y auditoría](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/40722132704): cero vulnerabilidades reportadas por npm en ese momento. Los blobs se contrastaron con sus hashes Git y SHA-256 antes de incorporarlos. El workflow de preparación solo existe en su rama; no se añade al flujo de producción. La aceptación del runtime y del despliegue corresponde a los runs posteriores del PR/main, no a esta auditoría aislada.

Fuentes primarias: [release oficial Wrangler 4.154.0](https://github.com/cloudflare/workers-sdk/releases/tag/wrangler%404.154.0), [aviso Undici](https://github.com/nodejs/undici/security/advisories/GHSA-2m5v-pch6-74hx).

## Persistencia de rutas: incidencia abierta

La incidencia #31 es independiente del módulo TERM: pérdida intermitente de marcas de rutas con dos pestañas en WebKit. Se reprodujo en la línea base y el ensayo adicional resultó insuficiente (39/40). No se incorpora ese ensayo, no se elimina el test y no se declara cerrado el problema por un run verde aislado. Mitigación: usar una sola pestaña para editar marcas de la vista de rutas. [Detalle y criterios de cierre](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/31).

## Aceptación de publicación

El job TERM `public-release` debe comprobar el SHA de main, `sourceDirty: false`, hashes de todos los activos, las cuatro entradas y las cabeceras efectivas de todos los HTML, incluidas las respuestas 404. Su resultado `passed` acredita esas comprobaciones, no seguridad absoluta, ni conectividad a ttyd, ni cierre de #31.
