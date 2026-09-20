# M20–M23 · macOS, Darwin y zsh

Cada módulo: 14 h, con teoría 5 h y tres laboratorios de 3 h. Sistema macOS real sobre hardware/licencia permitidos. Sin él, los análisis de archivos preparados se etiquetan como simulación y no validan administración nativa. Fuentes: [S07 y manuales locales de Apple/zsh](../FUENTES.md). Se registran versión, arquitectura y permisos; no se trasladan automáticamente opciones GNU a utilidades BSD.

## M20 · Darwin, APFS y operación básica

**Entrada:** M03, M05. **Resultado:** explicar la organización de macOS y realizar operaciones GUI/CLI sin tratarlo como una distribución Linux.

**Unidades:** Darwin/XNU, framework y aplicación; Intel/Apple Silicon y límites de arquitectura; arranque, recuperación y volumen de sistema; APFS, contenedores/volúmenes, snapshots y sensibilidad a mayúsculas; rutas `/Applications`, `/System`, `/Library`, `~/Library`, `/Users`, `/Volumes`; bundles y extensiones; Finder y Terminal; metadatos, enlaces y atributos extendidos.

**Herramientas:** Finder, Ajustes del Sistema, Utilidad de Discos, Monitor de Actividad; `sw_vers`, `uname`, `system_profiler` acotado, `diskutil list`, `df`, `du`, `stat`, `file`, `ls -le@`, `xattr` de consulta y `open`. No escribir en volúmenes del sistema ni eliminar atributos de cuarentena para permitir programas.

**L20A · Mapa del Mac.** Entorno: Mac de laboratorio y usuario estándar. Tareas: identificar versión y arquitectura; localizar aplicación, configuración global y configuración de usuario; contrastar Finder/Terminal; explicar un bundle sin modificarlo. Evidencia: mapa de rutas y funciones. Éxito: distinguir directorios globales y personales. Recuperación: ninguna modificación.

**L20B · Metadatos y copias.** Entorno: carpeta de documentos sintéticos. Tareas: observar permisos, ACL y atributos; copiar con métodos distintos; comparar contenido y metadatos; explicar diferencias. Evidencia: tabla de preservación. Éxito: no afirmar que un hash de contenido verifica todos los metadatos. Recuperación: conservar originales.

**L20C · Volúmenes y espacio.** Entorno: consultas al disco y pequeño volumen de práctica preparado. Tareas: representar disco/contenedor/volumen; comparar espacio aparente; explicar snapshots y COW a partir de información observada. Evidencia: diagrama y dos límites. Éxito: no tratar todos los volúmenes como particiones independientes. Recuperación: no desmontar ni modificar el volumen de arranque.

**Dominio:** reconocer qué parte es Unix y qué parte es específica de Apple. **Error frecuente:** equiparar oculto, protegido y cifrado.

## M21 · zsh, archivos y automatización

**Entrada:** M11, M20. **Resultado:** automatizar tareas propias en macOS y detectar diferencias relevantes entre zsh, Bash y herramientas BSD/GNU.

**Unidades:** shell de login/interactiva/no interactiva; archivos de inicio; PATH y resolución; quoting, expansión y globbing; arrays y opciones de shell; funciones, argumentos y errores; texto/datos; plist y preferencias; paquetes y actualizaciones; Homebrew como ecosistema de terceros; scripting portable y pruebas explícitas.

**Herramientas:** `zsh`, ayuda y `man`; `command -v`, `type`, `printf`, `find`, `grep`, `sed`, `awk`, `shasum -a 256`, `plutil`, `defaults read`; `softwareupdate --list`; `brew list/info` solo si ya está aprobado e instalado. No usar `sudo` para encubrir problemas del gestor de paquetes.

**L21A · Portar sin asumir.** Entorno: un script Bash propio que solo lee archivos. Tareas: registrar intérprete; ejecutarlo en el intérprete previsto; comparar comportamientos al adaptarlo a zsh; revisar arrays, glob sin coincidencias y opciones de utilidades. Evidencia: matriz compatible/no compatible. Éxito: shebang correcto y ninguna pretensión de portabilidad no probada. Recuperación: mantener versiones separadas.

**L21B · Datos plist.** Entorno: copias sintéticas de preferencias, no perfiles reales. Tareas: validar formato; convertir una copia para inspección; consultar claves; comparar versiones; separar dato y configuración aplicada. Evidencia: informe con claves esperadas y faltantes. Éxito: no modificar preferencias reales ni confundir un valor persistido con estado efectivo. Recuperación: conservar originales.

**L21C · Inventario de carpeta en zsh.** Entorno: dataset con espacios y Unicode. Tareas: recibir ruta; validar entradas; generar manifiesto de nombres/tamaños/hashes; tratar errores; documentar versión de herramientas. Evidencia: script y pruebas de ruta inválida y carpeta vacía. Éxito: no seguir enlaces fuera del alcance sin decisión explícita. Recuperación: eliminar solo salidas de ensayo.

**Dominio:** separar sintaxis de shell y opciones del programa ejecutado. **Error frecuente:** asumir que el Bash incluido en macOS dispone de todas las características de un Bash reciente de Linux.

## M22 · Usuarios, launchd, servicios y red

**Entrada:** M10, M21. **Resultado:** diagnosticar ejecución y conectividad, y configurar una tarea legítima en el ámbito adecuado.

**Unidades:** usuarios/grupos, administración y elevación; permisos Unix, ACL y TCC; LaunchAgents frente a LaunchDaemons; dominios de launchd, sesión e identidad; plist de servicio, rutas y entorno; servicios compartidos y acceso remoto; DNS y configuración por servicios de red; firewall de aplicaciones frente a filtrado de paquetes; cambios reversibles.

**Herramientas:** Usuarios y grupos, Compartir, elementos de inicio y red; `id`, `dscl` de consulta acotada, `launchctl print`, `plutil`, `ps`, `lsof -i`, `networksetup -listallnetworkservices`, `scutil --dns`, `route -n get default`, `ifconfig`; SSH cuando el docente haya preparado acceso limitado. No usar órdenes heredadas de launchd sin comprobar la versión.

**L22A · Identidad y acceso.** Entorno: dos usuarios ficticios en Mac de laboratorio. Tareas: definir acceso a una carpeta compartida; observar permisos y ACL; verificar lectura/escritura; explicar diferencia entre permiso de archivo y autorización TCC. Evidencia: matriz y resultado. Éxito: no otorgar acceso total al disco como solución universal. Recuperación: restaurar permisos del directorio de práctica.

**L22B · Agente de usuario auditable.** Entorno: cuenta de alumno y script benigno que crea un resumen propio. Tareas: escribir plist; validarlo; definir rutas absolutas; activar mediante mecanismo documentado de launchd; comprobar resultado y log. Evidencia: definición y comprobación. Éxito: ámbito de usuario, sin ocultación ni privilegios administrativos innecesarios. Recuperación: descargar/desactivar y retirar exclusivamente el agente creado siguiendo la ayuda local.

**L22C · Conectividad y servicio.** Entorno: Mac y servidor asignado. Tareas: identificar servicio de red e interfaz; consultar DNS/ruta; comprobar puerto y respuesta de aplicación; revisar estado de Compartir; identificar exposición innecesaria sin cambiarla automáticamente. Evidencia: diagnóstico y plan. Éxito: explicar diferencias con herramientas Linux/Windows. Recuperación: revertir solo ajustes temporales aprobados.

**Dominio:** identificar usuario y dominio de ejecución de cada tarea. **Error frecuente:** dar por disponible el entorno interactivo en launchd.

## M23 · Seguridad de plataforma, logs y evidencias

**Entrada:** M19, M22. **Resultado:** auditar controles de macOS y obtener evidencia proporcionada, respetando protección de plataforma y privacidad.

**Unidades:** FileVault y gestión de recuperación; SIP, volumen de sistema firmado y arranque; Gatekeeper/notarización/XProtect; firma de código y procedencia; TCC y permisos de privacidad; Keychain como almacén de secretos, sin extracción; actualización y reducción de exposición; Unified Log y retención; historial de shell y artefactos de ejecución con límites; Time Machine y restauración.

**Herramientas:** Privacidad y seguridad, FileVault y Console; `fdesetup status`, `csrutil status`, `spctl --status` cuando esté admitido, `codesign` en consulta sobre aplicación aprobada, `log show` con intervalo y predicado, `log stream` acotado, `tmutil` de consulta. Comprobar manual local y capacidades del equipo. No desactivar SIP/Gatekeeper ni eliminar cuarentena.

**L23A · Baseline del Mac.** Entorno: Mac asignado. Tareas: registrar actualización, cifrado, protección de integridad, servicios remotos y usuarios; clasificar desviaciones; redactar excepción justificada si un control no aplica. Evidencia: checklist sin claves de recuperación. Éxito: diferenciar no conforme, no aplicable y no comprobable. Recuperación: no cambiar controles de plataforma durante la auditoría.

**L23B · Unified Log acotado.** Entorno: actividad benigna del curso y ventana temporal conocida. Tareas: consultar por tiempo y componente; contrastar Console/CLI; observar campos omitidos o redactados; normalizar tiempo conservando el original. Evidencia: extracto minimizado y cobertura. Éxito: no presentar ausencia de evento como prueba de que no ocurrió. Recuperación: custodiar/eliminar extractos según retención acordada.

**L23C · Restaurar e investigar.** Entorno: copia sintética de archivo y logs preparados. Tareas: calcular hash; construir una secuencia de cambios; restaurar una versión en ruta distinta; distinguir recuperación de investigación; señalar lo que el historial de shell no demuestra. Evidencia: manifiesto, cronología y límites. Éxito: conservar los originales y no extraer secretos del llavero. Recuperación: retirar solo restauración de ensayo.

**Checkpoint C4:** explicar y verificar macOS mediante GUI y CLI, reconocer las diferencias de arquitectura y respetar sus controles nativos.
