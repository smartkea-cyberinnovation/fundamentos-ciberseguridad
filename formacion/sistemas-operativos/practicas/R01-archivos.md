# R01 · Directorios, nombres, bytes y comprobación

**L05A · 3 h.** Entrada: M01–M04. Material: [lección 01](../lecciones/01-terminal.md) y [kit](../kit/README.md). Objetivo: operar el mismo árbol mediante GUI y terminal y explicar por qué conteos aparentemente distintos pueden ser correctos.

## Preparación

Desde la raíz del curso, crea `mi-laboratorio` con `python3 kit/oslab.py init mi-laboratorio`. En Windows sustituye `python3` por el intérprete aprobado, por ejemplo `py -3`. No reutilices una carpeta personal ni ejecutes elevado. El docente puede entregar el dataset precreado.

## Recorrido guiado

1. Abre `datos` por GUI. Cuenta lo visible y activa la vista de elementos ocultos. No cambies atributos todavía.
2. En Linux/macOS, ejecuta `ls -la mi-laboratorio/datos` y `wc -c mi-laboratorio/datos/hola.txt`. En PowerShell usa `Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force` y consulta `Length`; en CMD, `dir /a mi-laboratorio\datos`.
3. Lee el archivo con espacios utilizando una ruta entrecomillada. Explica cuántos argumentos recibe el programa.
4. Compara `lineas-lf.txt` y `lineas-crlf.txt` sin editarlos. Calcula su hash con el manifiesto del kit y localiza por qué sus tamaños son 8 y 10 bytes.
5. Ejecuta `python3 kit/oslab.py manifest mi-laboratorio`. Debe dar 8 archivos y 62 bytes. Contrasta con una segunda herramienta; no compares ese total con espacio de bloques de disco como si midieran lo mismo.
6. Copia `hola.txt` a `salida/copia.txt` mediante GUI y verifica por terminal que su contenido coincide. La copia no aumenta el conteo del manifiesto, porque este solo lee `datos`.

## Variantes y evidencias

Introduce una ruta inexistente y captura el código inmediatamente. Explica por qué elevar permisos no arregla un nombre incorrecto. Modifica únicamente `salida/copia.txt`; demuestra que cambia su hash y que el original no cambió. No practiques borrado recursivo.

Entrega tabla con archivo, bytes, hash y observación; captura mínima GUI/CLI; respuesta a “¿por qué `.nota.txt` cuenta?”; y comparación original/copia. Éxito: localizar todos los elementos y distinguir contenido, nombre, metadatos y espacio ocupado.

## Recuperación y criterio

Conserva el dataset original. Retira solo la copia de `salida` desde GUI después de identificarla. Una diferencia entre métodos debe explicarse, no ocultarse. El kit de referencia está probado en Linux; la ejecución GUI y las alternativas nativas de cada alumno requieren su ficha de validación.
