# Validación de TERM

## Alcances distintos

Una compilación válida, una prueba de navegador, una ejecución Docker y una publicación observada son comprobaciones diferentes. Este repositorio conserva las pruebas que permiten repetir cada alcance.

## Verificaciones automáticas

- Integridad curricular: orden de módulos, IDs estables, completitud de pasos, retos, preguntas y fuentes.
- Sintaxis shell de los ejemplos: Bash/sh analizan los comandos sin ejecutarlos.
- Estado local: importaciones inválidas, índices fuera de rango, tamaños, notas y cálculo de progreso.
- Configuración de terminal: orígenes exactos, HTTPS, separación del origen del campus, ausencia de credenciales y CSP.
- Publicación: inventario explícito, no symlinks, manifiestos SHA-256 y enlaces locales.
- Navegador: carga, ruta de lección, fases, cuestionario, notas, exportación, importación y navegación móvil.
- Laboratorio: tests del servidor HTTP y scripts, validación de configuración y, en un runner con Docker, construcción y smoke test de Compose.

## Repetir la validación

```sh
python3 term/build.py
python3 -m unittest discover -s term/tests -p 'test_*.py' -v
node --test term/tests/*.test.mjs
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
```

Consulta `term/tests/browser.mjs` para la aceptación de interfaz y `labs/tests` para las pruebas de laboratorio. Los workflows guardan diagnósticos del commit que se evalúa.

## Límites

No se certifica la seguridad total del entorno ni la habilidad del alumno por el mero resultado del cuestionario. No se escanean objetivos externos durante estas comprobaciones. Una terminal no configurada permanece deshabilitada y su disponibilidad se verifica solo después de que el operador la despliegue.

La configuración Docker/Kali depende de repositorios de paquetes y arquitectura. Registrar digest y versiones usados en la cohorte. Las imágenes rolling deben reconstruirse, probarse y fijarse antes de distribuirlas a un grupo.

## Evidencia de publicación

El curso expone `build-info.json` y `SHA256SUMS.txt`. El primero informa commit de origen, estado local de cambios durante el build, hash del curso, número de módulos/lecciones/preguntas y si hay un endpoint configurado. La publicación se confirma comparando estos datos con el commit integrado y con la comprobación HTTP del endpoint real.

## Revisión de fiabilidad · 19 de octubre de 2026

La edición conserva las 48 lecciones y sus IDs. Esta revisión corrige la persistencia de TERM sin cambiar las claves de progreso ni los contenidos del campus general.

El guardado usa un Web Lock por origen y compara el registro actual con la copia que esta pestaña leyó. Una copia corrupta se conserva intacta; una pestaña obsoleta no sobrescribe la nueva ni restaura datos tras un reinicio. En caso de conflicto se muestran acciones para exportar la sesión, descargar los bytes originales y recargar la copia guardada. La recuperación y la importación son explícitas. La confirmación de reemplazo se invalida si entretanto cambia la copia guardada. Sin almacenamiento o sin Web Locks se continúa en memoria y se solicita exportar; nunca se presenta ese estado como guardado persistente.

El último punto visitado se actualiza en memoria al navegar y se incluye en la siguiente edición o exportación de progreso; abrir una lección no escribe todo el historial. Los mensajes de importación, reinicio y notas distinguen un guardado efectivo de los cambios solo disponibles en la sesión.

```sh
node --test term/tests/*.test.mjs
python3 term/build.py
python3 -m unittest discover -s term/tests -p 'test_*.py' -v
# Con Playwright y el preview local preparados por el workflow:
node term/tests/persistence-browser.mjs
```

Las pruebas nuevas cubren corrupción, exportación del original, dos pestañas simultáneas, reinicio, cambios durante la confirmación, recuperación y límite de almacenamiento. Los tests de navegador corren en los motores declarados por el workflow. Un error de política del navegador local no equivale a una prueba superada: se conserva la evidencia real del runner.

### Verificación de publicación real

El job `public-release` se ejecuta en `main` después de las pruebas del curso y del laboratorio. No despliega un segundo Worker: verifica la publicación de Workers Builds ya vinculada a GitHub.

```sh
python3 term/verify_public.py --expected-commit COMMIT_COMPLETO --output term/qa/public-release.json
```

El verificador solo hace GET HTTPS a los dos hostnames del curso. Comprueba commit exacto, `sourceDirty: false`, inventario, hashes de todos los activos publicados, 16 módulos, 48 lecciones, 194 pasos, 96 preguntas, entradas con/sin barra, cabeceras de seguridad y respuesta 404 real. Relee los metadatos al terminar para detectar despliegues concurrentes. No abre ttyd ni verifica identidades Access. Su JSON se conserva como artefacto de Actions; solo un resultado `passed` demuestra esas comprobaciones, no la ausencia de todas las vulnerabilidades.

El staging del campus ya regenera los manifiestos después de adaptar las rutas; no se modifica ese mecanismo. La validación añadida comprueba además los bytes recibidos por HTTPS, no solamente la construcción local.

### Laboratorio y alcance

Se añade ShellCheck dentro de la imagen Kali y `docker stack config` a CI. Este último comprueba sintaxis sin crear un clúster; sus referencias `syntax-check-only` no se descargan ni son imágenes de producción. Las imágenes finales de un despliegue Swarm deben fijarse por digest como indica la guía.

Fuentes del comportamiento de plataforma: [Web Locks](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API), [evento storage](https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event), [cabeceras de Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/headers/).


## Contrato HTTP y transformación de Cloudflare

La comprobación del commit `a941c189de54625f6f308aeb4654367442950e8e` identificó una diferencia real entre las fuentes y las respuestas: Cloudflare añadía automáticamente su beacon de Web Analytics antes del cierre de `body`. Los JavaScript propios, estilos, JSON, favicon y ZIP coincidían con sus hashes; los HTML estaban transformados. Las cuatro entradas del curso respondían 200 y la ruta inexistente respondía 404. No era un error de rutas ni un manifiesto desactualizado.

Evidencia: [diagnóstico HTTP acotado 39267278017](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/39267278017). El workflow de diagnóstico existe únicamente en su rama y no se incorpora al despliegue. Ese resultado es observación, no aceptación de la entrega.

La corrección declara `Cache-Control: public, no-cache, no-transform` para los activos estáticos de TERM. `no-cache` conserva la revalidación y `no-transform` solicita no modificar la representación; según la [documentación oficial de Web Analytics](https://developers.cloudflare.com/web-analytics/get-started/), evita la inserción automática del beacon. El adaptador del campus restringe estas cabeceras a `/fundamentos-ciberseguridad/term/*`, sin modificar la política de otras páginas de SmartKEA. El curso no contiene respuestas personalizadas ni credenciales: las notas siguen exclusivamente en el navegador. No se debe copiar la directiva `public` a respuestas privadas.

La CSP permanece sin permisos para el beacon ni scripts inline. Tampoco se normaliza el HTML, se eliminan scripts antes de calcular hashes o se excluyen HTML de la aceptación. El verificador continúa exigiendo los bytes exactos y el commit limpio publicado. Su resultado posterior al despliegue es la evidencia definitiva de esta corrección.

Este control puede impedir optimizaciones de transformación, incluida compresión en el edge cuando el origen entrega datos sin comprimir. Se prioriza aquí el contenido docente verificable y sin inyección automática; no equivale a desactivar el WAF, la autenticación o Access. Referencia: [Origin Cache Control](https://developers.cloudflare.com/cache/concepts/cache-control/). La eficacia de las cabeceras se vuelve a comprobar por HTTPS; una configuración de zona que las sobrescriba se detectaría como fallo, no se aceptaría silenciosamente.


## Revisión del contrato de publicación · 28 de octubre de 2026

El verificador interpreta las directivas CSP como listas de tokens, no como subcadenas: `default-src 'self' https://otro.example` no satisface una política que exige únicamente `'self'`. También rechaza ampliaciones de `script-src`, overrides de elementos/atributos, directivas duplicadas y políticas múltiples ambiguas para este contrato. Esto valida la política concreta del curso; no es un evaluador general de cualquier CSP.

La comprobación se aplica a todos los HTML del manifiesto, a las cuatro entradas públicas y a la ruta 404. Exige `nosniff`, `X-Frame-Options: DENY`, revalidación y `no-transform`. Conserva hashes exactos, commit limpio y límites de red. El JSON incluye las cuatro URL solicitadas y sus destinos finales para facilitar la trazabilidad.

La incidencia [#31 de las rutas del campus](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/31) se reproduce por separado en WebKit. No se considera resuelta por una ejecución verde aislada ni por la aceptación de TERM. No se incorpora a producción el ensayo insuficiente de la rama de diagnóstico. Hasta resolverla, editar las marcas de la vista de rutas desde una sola pestaña. Esta observación no equivale a una certificación de todos los mecanismos de persistencia.

La publicación estática y la aceptación Docker no verifican una VM de alumno ni el recorrido Access/Tunnel. El material del laboratorio SSH es un despliegue independiente; no se ha conectado automáticamente al curso.
