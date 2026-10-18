# Contenido base — terminal Linux

## Entrega

- Archivo: core.json, esquema raíz `{"modules": [...]}`.
- 8 módulos m01–m08, 24 lecciones, 96 pasos de práctica, 24 retos con solución y rúbrica, 48 preguntas únicas de cuatro opciones.
- Todas las lecciones tienen tres objetivos, tres secciones desarrolladas, cuatro pasos, tres conclusiones y al menos dos fuentes primarias.
- Duración orientativa acumulada: 1155 minutos (19.25 horas), ajustable por el docente.
- Extensión total del contenido de lecciones: 24447 palabras contando comandos, etiquetas y campos; rango por lección 923–1307.
- JSON UTF-8: 253353 bytes. SHA-256: 90ee26c305eb4d8caf402268bd50bf975bce89c738efc68804938c6013f93983.

## Integración

1. Los pasos de cada lección deben realizarse en orden y en la misma sesión. Algunas variables (`term_copias`, `term_busqueda`, `term_acl`, etc.) conservan la ruta única creada con mktemp.
2. Los bloques declaran el intérprete. La creación del saludo portable usa `shell: sh`; los demás bloques usan Bash. En Kali la terminal inicial puede usar otra shell: el texto pide abrir Bash antes de las prácticas específicas.
3. Los campos `challenge.solution` combinan comandos y comentarios `#` con la interpretación resuelta. Todos pasan comprobación de sintaxis Bash. No deben ejecutarse automáticamente sin revisión del alumno.
4. `verify` y `undo` son campos explicativos y pueden combinar texto con comandos; no son un protocolo de ejecución automática.
5. Una terminal ttyd real ejecuta en la máquina que aloja la sesión. El contenido lo explica desde m01. Los bloques se deben copiar o enviar con acción explícita del alumno; nunca ejecutar por abrir una lección.
6. Algunos fallos están introducidos para aprender: `printf --help` del builtin Bash, lectura de un archivo inexistente, estado 1 de diff, errores de validación, timeout 124 y rechazo de conjunto vacío. El diseño del frontend no debe marcar automáticamente todo estado no cero como fallo de aprendizaje.

## Requisitos diferenciados

- Base: Linux con Bash, sh, GNU coreutils/findutils, awk, sed, grep, tar y procps.
- JSON: jq (m03-l03).
- ACL: getfacl/setfacl del paquete acl y un sistema de archivos que las soporte (m04-l03).
- systemd: VM con gestor de usuario y bus de sesión funcionales (m05-l03). Instalar systemctl en un contenedor no satisface ese requisito.
- Análisis estático: ShellCheck (m08-l03).
- Único paso de instalación administrativa: m06-l01, paso 4. Es opcional si las dependencias existen y requiere una VM Debian/Ubuntu/Kali propia, repositorios oficiales, red, sudo e instantánea. No ejecutarlo automáticamente en el runner de contenido. El bloque no inicia instalación si update falla.

## Validación realizada

- Esquema y cardinalidades comprobados, IDs únicos y secuenciales, 48 preguntas sin repetición literal.
- 96/96 bloques de pasos pasan `bash -n` o `sh -n` según su lenguaje.
- 24/24 soluciones de retos pasan comprobación de sintaxis Bash; los comentarios de interpretación no se tratan como órdenes.
- Se ejecutó una pasada integrada de las prácticas disponibles en un árbol temporal. Para las copias de prueba se sustituyó la referencia `$HOME` por una variable específica `TERM_VERIFY_HOME`; no se cambió ni reasignó HOME. No se instalaron paquetes ni se alteraron servicios del sistema.
- Las prácticas de archivos, nombres con salto de línea, pipes, texto, jq, modos, backups con restauración, aritmética, arrays y los scripts de m08 ejecutaron correctamente sus bloques disponibles.
- El ejecutor `pruebas.sh` dio 10 casos OK y `Fallos: 0`: líneas, bytes, parámetros ausentes, opción sin valor, modo inválido, archivo inexistente, nombre literal con `$()`, manifiesto, conjunto vacío y rechazo fuera del alcance. También verificó hashes y ausencia de manifiesto para el conjunto vacío.
- Se verificó repetición del manifiesto: resultado idéntico, modo 600 y limpieza de temporales en ejecución normal. El respaldo detectó una alteración deliberada y volvió a verificar tras restaurar el documento.

## Limitaciones observadas en el runtime de validación

- No estaban instalados ShellCheck, getfacl ni setfacl. No se afirma que hayan pasado esos controles: quedan previstos para VM/CI preparada. El contenido da el procedimiento concreto para ejecutarlos.
- procps `ps` presenta `fatal library error, lookup self` en este runtime restringido, por lo que la representación de procesos queda pendiente de una VM normal. Las esperas finitas, señales, trap y timeout sí se ejecutaron.
- sudo mostró errores de inicialización del plugin/política del runtime. Sus consultas se documentan como no concluyentes; no se escaló ni alteró configuración.
- APT no disponía de índices suficientes para resolver shellcheck y acl en la simulación. Se conserva como requisito de preparación; no se ejecutó update ni instalación en el entorno de trabajo.
- El gestor systemd de usuario no pudo completar la unidad en este runtime. El contenido maneja tanto ausencia inicial como fallo posterior y mantiene la práctica pendiente. No se presenta el journal vacío como evidencia de éxito.

## Decisiones docentes y de seguridad

- Datos sintéticos y escrituras bajo ~/term-lab, con carpetas únicas cuando hay enlaces, ACL, respaldos o temporales.
- Sin escaneos externos, explotación, extracción de secretos ni cambios de cuentas/sudoers. Sudo se consulta; la única instalación se distingue explícitamente.
- No se incluyen PowerShell, CMD ni BAT.
- Se enseña que los hashes verifican contenido frente a una referencia y no autentican por sí solos al autor; que un enlace duro no es copia independiente; que el contador de líneas no es contador universal de nombres; y que un archivo oculto no obtiene protección adicional.
- `manifestar.sh` es una utilidad didáctica para un árbol privado estable. El texto explica que realpath más comprobación de prefijo no constituye una frontera resistente a carreras adversarias, y que la publicación atómica del nombre no equivale a durabilidad o instantánea consistente.

## Fuentes principales consultadas

- GNU Bash Reference Manual: https://www.gnu.org/software/bash/manual/bash.html
- GNU Coreutils: https://www.gnu.org/software/coreutils/manual/coreutils.html
- GNU Findutils: https://www.gnu.org/software/findutils/manual/html_node/find_html/index.html
- GNU Findutils, nombres seguros: https://www.gnu.org/software/findutils/manual/html_node/find_html/Safe-File-Name-Handling.html
- GNU Findutils, seguridad y carreras: https://www.gnu.org/software/findutils/manual/html_node/find_html/Security-Considerations-for-find.html
- GNU Grep / sed / Awk / tar: páginas oficiales específicas en cada lección.
- jq: https://jqlang.org/manual/
- Debian Reference: https://www.debian.org/doc/manuals/debian-reference/
- Debian APT/dpkg/ACL/systemd: páginas de manual del proyecto distribuidas por manpages.debian.org.
- Kali, repositorios: https://www.kali.org/docs/general-use/kali-linux-sources-list-repositories/
- ShellCheck: https://github.com/koalaman/shellcheck y https://www.shellcheck.net/wiki/

Se consultaron fuentes primarias mediante búsqueda y aperturas web el 7 de octubre de 2026. Algunas aperturas directas de freedesktop devolvieron 403; se contrastó el comportamiento con las páginas de systemd publicadas por Debian. Las fuentes específicas permanecen enlazadas en cada lección. El material es original y no reproduce fragmentos extensos de los manuales.
