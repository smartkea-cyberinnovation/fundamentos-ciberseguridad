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
