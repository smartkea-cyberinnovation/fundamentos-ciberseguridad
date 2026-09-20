# Workers: publicación en la subruta de SmartKEA

Revisión: 2026-09-20. El campus se publica en **https://smartkea.com/introduccion-ciberseguridad/**. `campus/publication.py` define la base y la URL; la comprobación de `wrangler.jsonc` exige que su única ruta coincida con esa definición.

## Diagnóstico y corrección

El log del 20-09-2026 a las 09:47 UTC muestra que `wrangler versions upload` falló porque faltaba `campus/dist`. Instalar las dependencias npm del repositorio no genera este campus Python. El custom build de Wrangler ejecuta `python3 campus/cloudflare.py build` antes de procesar los activos: compila, valida el ZIP portable, prepara el staging y verifica su integridad. Si falla, Wrangler detiene la subida.

`campus/dist` y `campus/pages-ready.zip` siguen siendo la edición portable. La publicación usa `campus/worker-dist/introduccion-ciberseguridad/`, conserva íntegros los contenidos ES/EN y adapta únicamente la página 404 y los metadatos de publicación. `_headers` queda en la raíz del staging; `.assetsignore` excluye el marcador interno. Los manifiestos se recalculan para reflejar los archivos reales y `build-info.json` conserva el `sourceCommit` original e incorpora la URL, el prefijo y el hash del manifiesto fuente.

El Worker sólo sirve activos estáticos, sin entrypoint JavaScript, backend ni bindings. La única ruta de producción es `smartkea.com/introduccion-ciberseguridad/*`; no captura la web corporativa, otras rutas ni `www`. La redirección exacta de `/introduccion-ciberseguridad` a `/introduccion-ciberseguridad/`, preservando query string, se gestiona por separado en la zona Cloudflare. Una URL de preview se abre añadiendo el mismo prefijo al hostname de preview.

## Configuración del panel

En Workers > fundamentos-ciberseguridad > Settings > Builds:

| Campo | Valor |
|---|---|
| Git repository | `smartkea-cyberinnovation/fundamentos-ciberseguridad` |
| Root directory | Raíz del repositorio |
| Build command | Vacío |
| Production branch | `main` |
| Deploy command | `python3 campus/cloudflare.py deploy` |
| Non-production branch deploy command | `python3 campus/cloudflare.py preview` |
| Build variable | `SKIP_DEPENDENCY_INSTALL=1` |
| Build variable | `PYTHON_VERSION=3.13.3` |
| Build variable | `NODE_VERSION=22.23.2` |

Los wrappers validan la configuración y llaman a Wrangler 4.132.0; Wrangler ejecuta el custom build exactamente una vez. No añadir otro build al panel ni usar `--no-bundle` para intentar saltar el custom build. Las versiones verificadas no tienen un argumento `--no-build`.

`deploy` publica producción y sincroniza la ruta declarada. `preview` utiliza exclusivamente `versions upload`: sube una versión, no la promueve ni sincroniza las rutas. `workers_dev` y `preview_urls` están habilitados explícitamente para verificar el Worker y las versiones. La cuenta/token de publicación debe permitir gestionar el Worker y su ruta en la zona SmartKEA; mantener los tokens fuera de Git.

Las variables, la conexión Git y los comandos del panel deben comprobarse allí: integrar este archivo no los configura. El dominio sin slash se configura y verifica como regla independiente, sin ampliar la ruta del Worker.

La [migración del repositorio](../docs/MIGRATION.md) conserva el Worker y la URL pública. Al cambiar la conexión Git, seleccionar el repositorio de SmartKEA en la instalación de GitHub usada por Cloudflare y mantener `main` como rama de producción. Comprobar después el repositorio y commit del build real; un build del origen antiguo no acredita la conexión nueva. Publicar el aviso de traslado en el repositorio original sólo después de aceptar el nuevo build y la ruta pública.

## Pruebas sin publicación

Desde la raíz del repositorio:

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py dry-run
python3 campus/cloudflare.py check
npx --yes wrangler@4.132.0 dev --config wrangler.jsonc --local --ip 127.0.0.1 --port 8789
```

En otra terminal:

```sh
python3 campus/tests/cloudflare_smoke.py
```

La CI comprueba comandos raw `versions upload --dry-run` y `deploy --dry-run` desde checkout sin ambos directorios generados, con Wrangler 4.132.0 y 4.135.0. El smoke verifica el prefijo, ambos idiomas, activos, cabeceras, procedencia, respuestas 404 y los recursos enlazados por la propia página 404. Estas pruebas nunca ejecutan laboratorios ni publican.

Tras publicar desde un commit limpio, comprobar la URL real, el SHA servido en `/introduccion-ciberseguridad/build-info.json`, las redirecciones y la continuidad de la web corporativa. Se puede usar `python3 campus/tests/cloudflare_smoke.py --origin https://smartkea.com` si el entorno HTTP permite acceder; la aceptación remota exige un `sourceCommit` no nulo que coincida con el checkout. Un upload correcto o un dry-run local no acredita por sí solo la operación del dominio.

## Recuperación

Antes de activar una publicación, guardar la versión que recibe el 100 % del tráfico, las rutas del Worker, el ruleset de redirecciones y los comandos/variables de Builds. El despliegue inicial de septiembre partía de la versión de plantilla `cf5f1c57-99de-4fb7-a0bd-6dc05b9df99a`, sin ninguna ruta del campus.

Si falla la aceptación, detener nuevas publicaciones del campus y restaurar la versión previa mediante el historial de deployments del Worker. Recuperar las rutas y reglas por separado: retirar únicamente la ruta del campus creada durante esta intervención, deshabilitar su nueva regla de barra final y devolver a la regla apex→www su expresión anterior guardada. No reemplazar el ruleset completo si otros cambios han ocurrido entretanto. Restaurar los valores previos de Builds si son la causa del fallo.

Después, verificar de nuevo portada, `/legal` y `/privacidad`, y documentar qué versión recibe tráfico. Revertir una versión no revierte las rutas ni las reglas de zona. Para una actualización posterior, conservar la versión funcional del campus como referencia de recuperación; no utilizar la plantilla inicial.

## English operational summary

The September 20 failure was a missing generated asset directory. The dashboard wrappers delegate to Wrangler's checked custom build, which builds and validates the portable course and stages it at `/introduccion-ciberseguridad/` exactly once before uploading. The production route is limited to this prefix on `smartkea.com`; a separate exact redirect adds the missing trailing slash. Preview uploads do not promote versions or synchronize production routes. Static content bytes remain unchanged; publication metadata, 404 links and checksums reflect the staged layout. Verify both the published commit and the corporate site after deployment.

## Fuentes primarias

- [Custom builds](https://developers.cloudflare.com/workers/wrangler/custom-builds/)
- [Workers Builds configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)
- [Build image](https://developers.cloudflare.com/workers/ci-cd/builds/build-image/)
- [Serving a subdirectory](https://developers.cloudflare.com/workers/static-assets/routing/advanced/serving-a-subdirectory/)
- [Versions and deployments](https://developers.cloudflare.com/workers/versions-and-deployments/)
