# M01–M04 · Fundamentos, laboratorio y método

Cada módulo tiene 14 h: teoría 5 h y tres laboratorios de 3 h. Todos heredan el contrato y la recuperación de [laboratorio](../LABORATORIO.md). Fuentes y manuales: [S01, S03, S04, S07, S10](../FUENTES.md). Perfil: tronco común para todas las especialidades.

## M01 · Diagnóstico, trabajo seguro y laboratorio

**Entrada:** ninguna. **Resultado:** preparar un entorno aislado, identificar alcance y privilegios, registrar una intervención y restaurar un cambio de prueba.

### Unidades teóricas

1. Qué hace un administrador, un analista de seguridad y un investigador; observación frente a modificación.
2. Equipo físico, anfitrión, huésped, hipervisor, contenedor y servicio remoto: localizar la ejecución real.
3. Usuario estándar, administrador y autorización. Riesgo técnico, operativo y de privacidad.
4. Consola, terminal, shell e intérprete: cuatro conceptos que no son sinónimos.
5. Snapshot, copia de seguridad y evidencia: objetivos distintos y límites.
6. Cuaderno técnico: fecha, versión, acción, salida, conclusión y reversión.

**GUI/CLI:** gestor del hipervisor y ajustes de red; explorador y terminal de cada SO; ayuda integrada; consulta de identidad y directorio actual. No se requiere modificar la red del anfitrión.

### Laboratorios

**L01A · Diagnóstico reproducible.** Entorno: cuenta estándar en el equipo asignado. Tareas: identificar SO/versión; abrir GUI y terminal; localizar un archivo de práctica por ambas vías; guardar la salida de una consulta inocua; explicar un error de ruta. Evidencia: ficha inicial y captura mínima sin datos personales. Éxito: identificar máquina, usuario y ubicación, y distinguir dato observado de su interpretación. Recuperación: cerrar sesiones y conservar solo materiales del curso.

**L01B · Aislar y recuperar.** Entorno: VM vacía y red de práctica preaprobada. Tareas: describir adaptadores y rutas; comprobar un flujo permitido y otro denegado hacia destinos asignados; crear snapshot; cambiar un archivo de texto; restaurarlo. Evidencia: diagrama y comparación antes/después. Éxito: restauración comprobada y ausencia de exposición externa. Recuperación: retornar al snapshot base, revisando que el registro de trabajo se conserva fuera de la VM.

**L01C · Primera intervención.** Entorno: árbol de archivos sintéticos. Tareas: redactar objetivo y límites; aplicar una modificación reversible; registrar hora y acción; pedir a otro alumno que reproduzca el resultado; documentar desviaciones. Evidencia: ticket, registro y revisión cruzada. Éxito: otra persona obtiene el mismo resultado sin instrucciones orales. Recuperación: deshacer únicamente el cambio aprobado.

**Dominio mínimo:** no actuar sobre una máquina no identificada; no confundir privilegio técnico con autorización. **Pregunta de defensa:** por qué restaurar un snapshot puede destruir evidencia relevante. **Error frecuente:** guardar el único cuaderno de trabajo dentro de la VM que se restaura.

## M02 · Representación de información y hardware

**Entrada:** M01. **Resultado:** relacionar datos, recursos y síntomas de funcionamiento sin tratar cada diferencia de tamaño como anomalía.

### Unidades teóricas

1. Bits, bytes, binario, hexadecimal; unidades decimales y binarias.
2. Texto y bytes: ASCII, Unicode, UTF-8, UTF-16, BOM y finales de línea.
3. CPU, arquitectura e instrucciones; núcleos, hilos, RAM, caché, disco y buses.
4. Almacenamiento lógico/físico, bloques, latencia, IOPS y capacidad; memoria virtual introductoria.
5. Archivos de texto y binarios; formato, extensión, compresión, hash y firma.
6. Interpretar mediciones: uso instantáneo, promedio, saturación y denominador.

**GUI/CLI:** información del sistema, monitor de recursos; `lscpu`, `free`, `df`, `od`; `Get-ComputerInfo`, `Format-Hex`; `system_profiler` con tipos de datos acotados. Herramientas según disponibilidad del SO.

### Laboratorios

**L02A · El mismo texto, bytes diferentes.** Entorno: archivos creados por el alumno, sin datos reales. Tareas: guardar un texto con tildes en dos codificaciones; comparar tamaño y representación hexadecimal; cambiar LF/CRLF; calcular hash; explicar por qué el significado puede ser igual y los bytes distintos. Evidencia: tabla de codificación, tamaño y hash. Éxito: lectura correcta sin pérdida de caracteres. Recuperación: conservar originales y eliminar solo copias desechables.

**L02B · Inventario razonado.** Entorno: una VM y su anfitrión con permisos de consulta. Tareas: registrar CPU, RAM, discos, arquitectura y virtualización visible; contrastar GUI/CLI; diferenciar recursos físicos de asignados. Evidencia: inventario minimizado sin números de serie. Éxito: explicar dos discrepancias aparentes. Recuperación: ninguna modificación; cerrar herramientas de monitorización.

**L02C · Diagnóstico de recursos.** Entorno: muestras de métricas preparadas por el docente, no generadores de carga ilimitada. Tareas: clasificar un cuello de CPU, RAM y disco; justificar qué medición falta; proponer una comprobación de bajo impacto. Evidencia: hipótesis y plan de prueba. Éxito: no concluir falta de RAM solo por ver caché ocupada ni comparar GB/GiB como si fueran idénticos. Recuperación: archivar las muestras originales.

**Dominio mínimo:** distinguir codificación, compresión, cifrado y hashing. **Pregunta:** qué cambia un hash y qué no acredita. **Error frecuente:** asumir que extensión equivale al formato real.

## M03 · Arquitectura del SO, arranque y ejecución

**Entrada:** M02. **Resultado:** construir un modelo de procesos, memoria, archivos, identidades y servicios que sirva para los tres sistemas.

### Unidades teóricas

1. Kernel y espacio de usuario; llamadas al sistema, controladores, APIs y separación de privilegios.
2. Firmware/UEFI, arranque verificado, cargador, kernel, inicio de servicios y sesión.
3. Procesos e hilos, PID/PPID, planificador, estados, señales y objetos de proceso.
4. Memoria virtual, paginación, espacio de direcciones, aislamiento y consumo residente.
5. Descriptores/handles, entrada/salida, sockets e IPC; recursos abiertos y bloqueos.
6. Sistemas de archivos, montajes, metadatos, rutas, journaling y copy-on-write.
7. Unix/Linux, Windows NT y Darwin/XNU: modelos relacionados, implementaciones diferentes.

**GUI/CLI:** administrador de tareas, monitor de actividad, herramientas de procesos; `ps`, `top`, `lsof`, `/proc` en Linux; `Get-Process`; `launchctl` como introducción. La presencia de `/proc` no se presupone en macOS.

### Laboratorios

**L03A · Árbol de ejecución.** Entorno: editor y terminal en una cuenta estándar. Tareas: abrir un proceso benigno; observar PID, padre, usuario y recursos; cerrar normalmente; confirmar finalización por GUI y CLI. Evidencia: árbol explicado. Éxito: diferenciar terminal, shell y programa hijo. Recuperación: cerrar solo procesos propios creados para la práctica.

**L03B · Camino de un archivo.** Entorno: volumen de práctica. Tareas: seguir una ruta desde el directorio hasta el volumen; identificar propietario, tamaño, permisos y metadatos; abrir el archivo y observar el recurso cuando la herramienta lo permita. Evidencia: diagrama de capas. Éxito: no confundir ruta, archivo, descriptor y bloque físico. Recuperación: no desmontar volúmenes del sistema.

**L03C · Servicio frente a sesión.** Entorno: VM con servicio de demostración administrado por el docente. Tareas: observar proceso y estado; cerrar una sesión ordinaria; comprobar qué servicio continúa; analizar un registro de arranque. Evidencia: cronología y explicación. Éxito: distinguir inicio automático, servicio en ejecución y aplicación visible. Recuperación: reconectar sin modificar los servicios de seguridad.

**Dominio mínimo:** explicar dónde se aplican los permisos y dónde se ejecuta el código. **Pregunta:** por qué un contenedor no es un SO completo independiente. **Error frecuente:** interpretar memoria virtual como consumo físico directo.

## M04 · Terminal, documentación y Git

**Entrada:** M03. **Resultado:** realizar operaciones reproducibles desde terminal y conservar cambios y documentación sin subir secretos.

### Unidades teóricas

1. Prompt, comando, argumentos, opciones, ruta, directorio actual y autocompletado.
2. Ayuda y manuales: leer sinopsis, límites, versión, ejemplos y códigos de salida.
3. stdin, stdout, stderr, redirecciones, pipeline; texto frente a objetos.
4. Entorno, PATH, alias, perfiles y resolución de ejecutables; riesgos de sombreado.
5. Git: working tree, índice, commit, diff, log, rama, merge y revisión.
6. Markdown, README, issues y bitácora; licencias, privacidad y revisión de contenido antes del commit.

**GUI/CLI:** editor con terminal integrada; `man`, `help`, `type`, `command -v`; `Get-Help`, `Get-Command`; `git status`, `git diff`, `git add`, `git commit`, `git log`, `git switch`. Evitar forzar pushes como solución a conflictos.

### Laboratorios

**L04A · Aprender un comando nuevo.** Entorno: carpeta de práctica. Tareas: formular un objetivo; consultar ayuda local; localizar versión y sintaxis; ensayar con un archivo sintético; separar stdout de stderr; anotar exit code. Evidencia: receta explicada. Éxito: reproducirla sin copiar un comando no comprendido. Recuperación: retirar los archivos temporales identificados.

**L04B · Cuaderno versionado.** Entorno: repositorio local de alumno. Tareas: crear README y árbol de entregas; revisar diff; realizar tres commits significativos; crear una rama; corregir un error documental y comparar versiones. Evidencia: historial y justificación. Éxito: no incluir credenciales, artefactos binarios ni datos personales. Recuperación: preservar historial y revertir con una operación explicada, sin borrarlo.

**L04C · Revisión entre pares.** Entorno: repositorio de prueba sin acceso a producción. Tareas: revisar instrucciones de otro alumno; detectar una ruta absoluta no portable y un supuesto de privilegios; proponer corrección; resolver un conflicto de texto sencillo. Evidencia: comentario, diff y prueba. Éxito: instrucciones válidas en un directorio nuevo. Recuperación: dejar la rama de trabajo limpia y documentada.

**Checkpoint C1:** obtener ayuda, navegar, reconocer efectos y registrar una operación sin permisos innecesarios. **Error frecuente:** creer que borrar un secreto del último archivo lo elimina del historial Git.
