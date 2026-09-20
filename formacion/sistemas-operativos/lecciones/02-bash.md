# 02 · Bash: de una orden útil a una automatización confiable

## Diseñar el contrato

Antes de programar, escribe qué entra, qué sale, qué cambia y qué significa cada fallo. `resumen.bash` recibe un workspace; verifica su marcador; recorre únicamente `datos/`; cuenta archivos regulares y bytes; devuelve JSON. No realiza una auditoría completa ni necesita permisos administrativos. La versión Python añade restricciones que el ejemplo shell no implementa: comparar ambas es parte del ejercicio, no una equivalencia de garantías.

## Expansión y quoting

La shell interpreta antes de ejecutar el programa. Revisa los argumentos efectivos, no solo cómo parece leerse la línea. `"$1"` mantiene un parámetro como una palabra; `"$@"` conserva la separación original de todos los argumentos. Una cadena de texto que parece un comando no debe convertirse en código. Los ejemplos no necesitan `eval` ni construir una orden concatenando datos. [S01](../FUENTES.md)

En el resumen, `for file in datos/*` necesita dos decisiones: qué ocurre si el directorio está vacío y si se incluyen ocultos. Bash permite fijarlo con `nullglob` y `dotglob`; zsh tiene mecanismos distintos. Define la semántica deliberadamente. Los nombres con espacios permanecen unidos al usar la variable entre comillas en cada operación.

## Errores explícitos

`set -u` ayuda a detectar variables no definidas. `pipefail` modifica el estado agregado de una tubería. Ninguna opción valida por sí sola los datos ni convierte un script en seguro. Una estrategia seria prueba rutas inválidas, permisos, entradas vacías y comandos ausentes, y decide qué devolver. El ejemplo comprueba operaciones esenciales de forma explícita. [S01]

Tras una orden, consulta `$?` inmediatamente o utiliza una condición. En una construcción `orden || exit 2`, el código 2 pertenece al contrato de nuestro script; no conserva necesariamente el código original de la herramienta. Al diseñar un colector profesional puede interesar preservar ambos: estado del flujo y causa de la suboperación.

## Idempotencia y reversibilidad

Repetir una consulta sobre los mismos datos debe producir el mismo resultado. Esa propiedad se comprueba en los tests. Repetir `init` es distinto: se rechaza para evitar sobrescritura. No todas las operaciones tienen que ser idempotentes del mismo modo; lo importante es que su comportamiento sea explícito.

En una modificación de configuración, una secuencia útil es: leer estado; validar; proponer diff; aprobar; guardar copia; aplicar cambio mínimo; comprobar; recuperar si falla. Un dry-run que recorre un código completamente distinto puede dejar sin probar precisamente el camino peligroso. El rollback debe tener criterios y prueba, no solo un párrafo que prometa deshacerlo.

## Concurrencia, tiempos y secretos

El ejemplo presupone una carpeta sin editores concurrentes. Una herramienta de operación necesitaría estudiar locks, sustitución atómica y coherencia de varias fuentes. El tamaño observado antes de leer puede cambiar durante la lectura. Registrar esos límites enseña más que afirmar que un script es “forense” por calcular SHA-256.

En tareas programadas, especifica rutas y entorno; no dependas del perfil interactivo. Evita imprimir variables de entorno completas o activar trazas que expongan secretos. Un timeout y una salida parcial deben reflejarse como tales: no se presentan como inventario completo.

## Ejercicio de revisión

Lee el resumen sin ejecutarlo y predice resultado con ocho archivos, con ninguno y con un enlace. Contrasta con `bash -n`, ejecución real y tests. `bash -n` comprueba sintaxis, no permisos, efectos ni resultado. Propón una mejora y añade primero un caso de prueba que falle con la versión anterior. No aumentes privilegios para hacer pasar el test. Continúa en [R02](../practicas/R02-bash.md).
