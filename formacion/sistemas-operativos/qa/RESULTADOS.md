# Resultados de validación · edición 1.1

**Fecha: 2026-09-14. Entorno: Linux x86_64, Python 3.13.5, Bash 5.2.37.** Validación local de los archivos de esta edición, no una ejecución en GitHub Actions ni un certificado de seguridad.

## Pruebas ejecutadas

| Grupo | Pruebas | Resultado | Alcance |
|---|---:|---|---|
| Herramientas offline y ejemplo Bash | 34 | Correctas; ninguna omitida | Fixtures, hashes, límites, parsing, timestamps, indicadores exactos, esquema IA y errores |
| Servicio HTTP local | 8 | Correctas; ninguna omitida | Rutas fijas, health, HEAD, 404, POST rechazado, cabeceras y no reflexión de query |
| Planificación | 8 | Correctas; ninguna omitida | 32 módulos, prerrequisitos, 240 sesiones, 96 laboratorios y reparto de minutos |
| **Total automatizado** | **50** | **0 fallos, 0 omitidas** | **No equivale a 50 prácticas completas de SO** |

Se ejecutó además `bash -n kit/resumen.bash`. Los logs sin datos personales están en [pruebas del kit](pruebas.txt) y [pruebas de planificación](planificacion-pruebas.txt). El [manifiesto de integridad](integridad.json) identifica el código, pruebas y configuraciones entregados mediante SHA-256; una coincidencia de hash demuestra igualdad de bytes comparados, no seguridad o procedencia por sí sola.

En `.cmd` se compara la representación textual con CRLF normalizado a LF, coherente con la conversión de checkout declarada en `.gitattributes`. Esa comprobación no es una comparación binaria forense del archivo de trabajo. Los demás archivos del manifiesto se comparan byte a byte.

## Resultados de referencia

El dataset tiene ocho archivos, incluidos uno oculto, uno vacío y uno con nombre con espacios. Suma **62 bytes**: el archivo Unicode ocupa 19 bytes en UTF-8. Los archivos LF y CRLF ocupan 8 y 10 bytes respectivamente y tienen hashes distintos.

La cronología conserva los ocho eventos originales y sus timestamps con zona; rechaza fechas sin zona y IDs repetidos. El barrido exacto devuelve cuatro coincidencias en tres eventos: dominio e IP en E02, hash de archivo inocuo en E04 y dominio en E08. E03 y E07 son controles negativos.

La validación de respuesta IA devuelve `semantically_verified: false` incluso con esquema correcto. No se ejecuta salida del modelo ni se consulta un proveedor. El marcador del dataset no es una barrera contra un atacante concurrente.

## Repetir las pruebas

Desde la carpeta del curso:

```bash
python3 -m unittest discover -s kit -v
python3 -m unittest discover -s planificacion -v
python3 planificacion/generar.py --check
bash -n kit/resumen.bash
python3 qa/verificar.py
```

`qa/verificar.py` comprueba el manifiesto y la existencia de destinos de enlaces relativos en una copia completa del curso. Para revisar únicamente esta ampliación se utilizó además un inventario de las 21 rutas existentes, obtenido del árbol Git previo. No comprueba todas las anclas Markdown ni revalida sitios externos por HTTP.

## No ejecutado y pendiente

CMD/BAT y PowerShell en Windows; zsh/macOS y controles Apple; construcción Docker; despliegues Compose/Swarm; servicios de directorio, TLS nativo, adquisición forense y los 96 laboratorios integrales sobre imágenes de cohorte. Las herramientas nativas correspondientes y Docker no están disponibles en este entorno de ejecución.

El servidor usa HTTP local y carece de autenticación/TLS. Es un recurso didáctico, no una aplicación de producción. La variante Compose limita su publicación a loopback y la variante Swarm no publica puertos, pero esto sigue pendiente de prueba con el motor y clúster elegidos. Las etiquetas de imagen deben sustituirse por un digest revisado antes de la aprobación de cohorte.

## Criterio de aceptación docente

Probar cada runbook en las versiones reales, medir duración, verificar aislamiento y recuperación, adaptar accesibilidad y documentar límites. Aprobar la práctica solo con su evidencia propia. No convertir un test unitario o una revisión de documento en acreditación de administración multiplataforma.
