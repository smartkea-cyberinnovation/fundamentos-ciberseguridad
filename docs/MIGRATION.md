# Migración del campus a SmartKEA

Fecha: 20 de septiembre de 2026.

| Elemento | Referencia |
|---|---|
| Destino | [smartkea-cyberinnovation/fundamentos-ciberseguridad](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad) |
| Origen conservado | [WiktorNykiel/fundamentos-ciberseguridad](https://github.com/WiktorNykiel/fundamentos-ciberseguridad) |
| Snapshot de main utilizado | [`d816c3aef627f1ff323034946244ef247d4bd649`](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/tree/d816c3aef627f1ff323034946244ef247d4bd649) |
| Web pública | [smartkea.com/introduccion-ciberseguridad/](https://smartkea.com/introduccion-ciberseguridad/) |
| Worker / rama de producción | `fundamentos-ciberseguridad` / `main` |

## Qué se conserva

La copia procede exclusivamente de los archivos rastreados de ese commit, exportados con `git archive`. Se conservan `campus/`, `formacion/`, `wrangler.jsonc`, las reglas de exclusión y los workflows necesarios para validar el campus. Esto incluye todo el contenido docente de main: materiales de sistemas operativos, kit, lecciones, prácticas, traducciones, evaluación y plan maestro.

Se mantienen 32 módulos, 96 fichas, 21 referencias, 480 horas planificadas y los identificadores usados por el progreso local. Las modificaciones de migración actualizan enlaces al repositorio y documentación operativa. Las referencias a incidencias y PR del origen permanecen identificadas como históricas.

## Qué no se importa

El destino tiene un historial nuevo. No se transfieren commits, ramas, etiquetas, PR ni propuestas sin integrar del origen. Tampoco se copian archivos sin seguimiento, duplicados locales, cachés, activos compilados ni registros locales de trabajo.

La aplicación Next.js de referencia permanece en el repositorio original: se excluyen `src/`, `public/`, los manifiestos npm y configuraciones de Next de la raíz, sus pruebas de dependencias y su workflow. No son dependencias del campus. También se excluye la comprobación de ancestros de PR de esa aplicación; exigir aquellos commits sería incompatible con un historial nuevo. Se conservan las pruebas funcionales del campus, de sus artefactos, del runtime estático y del plan maestro.

Los registros de QA ya rastreados dentro del material docente se conservan como parte del snapshot y no se presentan como pruebas nuevas de esta migración. La evidencia de publicación se vincula al commit y al despliegue del nuevo repositorio.

## Conexión y aceptación

Workers Builds debe seleccionar `smartkea-cyberinnovation/fundamentos-ciberseguridad`, rama de producción `main`, y los comandos y versiones del [procedimiento de publicación](../campus/WORKERS-RECOVERY.md). Cambiar un enlace en el README no configura la conexión del proveedor.

La URL pública y su prefijo se mantienen. Para aceptar el traslado, comprobar el build del nuevo repositorio, el `sourceCommit` servido en [build-info.json](https://smartkea.com/introduccion-ciberseguridad/build-info.json), la versión activa del Worker, ambos idiomas, activos, 404 y redirección de barra final. Verificar también que portada, `/legal` y `/privacidad` continúan funcionando. El commit generado en el destino será distinto del SHA del snapshot de origen.

El aviso de traslado del repositorio original se añade después de verificar el nuevo origen Git y el funcionamiento de la web. El origen se conserva como referencia histórica y recuperación; no se elimina ni se sobrescribe su historial.

## Autoría y licencia

Se conserva la atribución a **Wiktor Nykiel** y las referencias originales. El snapshot no contiene un archivo `LICENSE` o `COPYING`; esta migración no añade una licencia ni amplía derechos de uso por el hecho de hacer público el repositorio. Los materiales de terceros mantienen sus condiciones originales.
