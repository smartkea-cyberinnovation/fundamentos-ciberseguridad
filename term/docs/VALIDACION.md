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
