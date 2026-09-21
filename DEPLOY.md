# Operación y despliegue / Deployment

La guía de estudio está en [README](README.md). Este documento es para mantenedores.

## Arquitectura

El campus es estático. `campus/build.py` genera el núcleo y el aula OS en `campus/dist/sistemas/` antes de sellar el manifiesto y ZIP. `campus/stage_worker.py` monta todos los activos bajo `/introduccion-ciberseguridad/`. No se añade servidor de sesiones, base de datos, ejecución remota o llamadas a IA.

El Worker y sus routes existentes se conservan. La nueva entrada pública será `/introduccion-ciberseguridad/sistemas/` en una publicación que incluya estos archivos. Un enlace en el README no acredita que esa versión esté activa.

## Compilación sin publicar

Desde la raíz, con Python soportado por el proyecto:

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
python3 campus/serve.py --port 8788
```

Abrir `http://127.0.0.1:8788/sistemas/?lang=es`. La versión inglesa utiliza `?lang=en`. No instalar el antiguo proyecto Next.js para compilar el campus.

## Aceptación

```sh
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
node --test campus/tests/*.test.mjs
python3 campus/tests/browser_os_study.py
CAMPUS_BROWSER=webkit python3 campus/tests/browser_os_study.py
CAMPUS_BROWSER=firefox python3 campus/tests/browser_os_study.py
```

Los motores se instalan mediante la versión de Playwright fijada en el workflow. La ausencia o bloqueo de un navegador no se convierte en un test superado. Conservar logs y capturas y comprobar fuentes, no solo contadores.

## Cloudflare

Se conserva la configuración operativa versionada en [WORKERS-RECOVERY](campus/WORKERS-RECOVERY.md) y [DEPLOY-CLOUDFLARE](campus/DEPLOY-CLOUDFLARE.md). Las acciones `preview` y `deploy` tienen efectos distintos: una preview no acredita activación en producción. Mantener las rutas y el dominio corporativo sin cambios fuera del prefijo del campus.

El incidente histórico del 20-09-2026 omitía la compilación y subía sin `campus/dist`. Su prevención consiste en ejecutar el wrapper de build/verificación antes de Wrangler, no crear una carpeta vacía ni reinstalar una app ajena. No se presenta ese incidente histórico como una caída actual.

Después de publicar, contrastar `build-info.json`, su `sourceCommit` y `osStudy` con la release, abrir ES/EN y probar navegación, lectura continua, una práctica, exportación/importación y viewport móvil. Revisar que portada y rutas corporativas ajenas conservan funcionamiento.

## Recuperación

Conservar el identificador de versión previa y configuración de rutas. La reversión de versión y de rutas es independiente. Este cambio no requiere nuevas routes ni cambios de DNS. No purgar toda la zona ni modificar políticas corporativas para diagnosticar el aula.

## English

The OS classroom is generated inside the same static release at `sistemas/`. Build, validate, stage and deploy using the existing wrapper. No new backend or provider route is needed. Run the exact source commit through unit, browser and release acceptance. Verify the active public build separately from uploading a preview. Retain the prior version and route configuration for scoped rollback.
