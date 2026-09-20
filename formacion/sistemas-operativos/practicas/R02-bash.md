# R02 · Un script Bash que se puede defender

**L11A · 3 h.** Entrada: M06 y M08; [lección 02](../lecciones/02-bash.md). Entorno: Bash en Linux y workspace ficticio. No se requieren privilegios administrativos.

## Tareas guiadas

1. Lee `kit/resumen.bash`. Anota contrato, parámetro, validación del marcador, alcance no recursivo, redirecciones y código de error. Predice el resultado antes de ejecutarlo.
2. Comprueba sintaxis con `bash -n kit/resumen.bash`. Explica qué errores no puede detectar esa comprobación.
3. Ejecuta `bash kit/resumen.bash mi-laboratorio`. Resultado de referencia: `{"count":8,"total_bytes":62}`.
4. Repite con una ruta con espacios usando un workspace nuevo. No añadas comillas al contenido de la variable; ponlas alrededor de la expansión.
5. Ejecuta sin argumento y con ruta inexistente. Captura `$?` inmediatamente. Debe producir error, no un informe de cero archivos.
6. Compara `python3 kit/oslab.py manifest mi-laboratorio` con el resumen Bash. Identifica funciones adicionales de Python y garantías que el ejemplo Bash no ofrece.

## Variante sin copiar solución

Copia el script a `mi-laboratorio/salida/resumen-alumno.bash`. Añade una opción de ayuda y dos pruebas. No añadas shell evaluada desde entrada, operaciones recursivas ni permisos administrativos. La mejora debe conservar el resultado del caso base y los fallos previstos.

Entrega contrato, diff, resultados y justificación del tratamiento de ocultos. Explica cómo se comporta el glob sin coincidencias. El ejercicio avanzado propone límites de tamaño, bloqueo y manejo de errores, pero no se afirma que el pequeño resumen ya los tenga todos.

## Éxito y recuperación

Debe funcionar con el dataset base y fallar de forma visible con entrada inválida. El alumno explica la diferencia entre salida de datos y diagnóstico. No se ejecutan scripts generados por IA sin revisión. Retira únicamente la copia del alumno tras entregar; los archivos del kit y el dataset base permanecen intactos.
