# R04 · macOS, zsh y límites de portabilidad

**L21A · 3 h.** Entrada: M11 y M20. Requiere Mac autorizado. [Lección 04](../lecciones/04-macos.md). Los datos son ficticios; no leer perfiles o preferencias personales.

## Recorrido

1. Registra `sw_vers`, `uname -m`, `zsh --version` y la versión del intérprete Python disponible. Escribe qué parte es SO, arquitectura, shell y lenguaje.
2. Abre el workspace en Finder y en Terminal. Activa visualización de ocultos y localiza `.nota.txt`.
3. Lee `kit/resumen.zsh`. Explica `emulate -L zsh`, las opciones locales y los calificadores del glob para ocultos y ausencia de coincidencias.
4. En el entorno aprobado, ejecuta `zsh -n kit/resumen.zsh` y después `zsh kit/resumen.zsh mi-laboratorio`. Resultado esperado: 8 archivos y 62 bytes. Captura sintaxis y ejecución como evidencias distintas.
5. Compara con `python3 kit/oslab.py manifest mi-laboratorio`. Examina un archivo con `ls -le@` y distingue contenido, permisos y atributos.
6. Revisa el Bash incluido sin ejecutarlo bajo zsh. Explica por qué cambiar el intérprete no equivale a portar el script. Consulta el manual local de `stat` y compara su sintaxis con la documentada para GNU/Linux.

## Variante y reflexión

Crea un workspace nuevo con nombre que contenga espacios. Prueba argumento ausente y marcador incorrecto en una copia. Revisa de forma conceptual qué entorno tendría el script si se ejecutara desde launchd y qué rutas/variables habría que declarar. No instales un agente persistente como parte de este guion de portabilidad.

Entrega matriz de comandos compatibles/no compatibles, salida esperada/observada y limitaciones. Una lectura de APFS o TCC sin intervención no sustituye las pruebas de sus módulos. No concedas acceso completo al disco para hacer funcionar un conteo sobre archivos del alumno.

## Recuperación y estado

No modificar seguridad de plataforma, llavero o volúmenes de arranque. Retirar solo la copia de práctica tras evaluación. **Código y guion preparados, sin ejecución nativa macOS/zsh en esta edición.** El docente registra versión y resultado antes de aprobarlos para una cohorte.
