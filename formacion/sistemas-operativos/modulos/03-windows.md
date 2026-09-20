# M13–M19 · Windows, CMD, BAT y PowerShell

Cada módulo: 14 h, con teoría 5 h y tres prácticas de 3 h. Requiere Windows nativo para administración, Registro, NTFS, servicios y eventos. Fuentes: [S03–S06, S13](../FUENTES.md). Leer el [contrato de laboratorio](../LABORATORIO.md). Se diferencian Windows PowerShell 5.1 y PowerShell 7; el docente fija versiones y módulos disponibles.

## M13 · Arquitectura de Windows y administración GUI

**Entrada:** M03, M04. **Resultado:** relacionar las herramientas visuales con el componente de sistema que administran.

**Unidades:** Windows NT, sesiones, procesos y servicios; archivos PE y bibliotecas como conceptos; rutas, unidades, perfiles y variables; NTFS, metadatos y herencia; Registro, hives, claves y valores; cuentas locales y dominio; UAC, token de acceso y privilegios; edición, compilación, roles y características; actualizaciones y recuperación.

**GUI/CLI:** Configuración, Administrador de tareas, Administración de equipos, Servicios, Visor de eventos, Monitor de recursos y Administrador de dispositivos; `winver`, `systeminfo`, `whoami`, `$PSVersionTable`, `Get-ComputerInfo`. No registrar claves de producto ni volcados completos de datos personales.

**L13A · Mapa administrativo.** Entorno: VM Windows cliente. Tareas: localizar versión, dispositivos, servicios, usuarios y almacenamiento; registrar para cada función su alternativa CLI; explicar qué requiere elevación. Evidencia: mapa GUI/CLI y captura mínima. Éxito: distinguir herramienta de administración y componente administrado. Recuperación: cerrar consolas sin modificar políticas.

**L13B · Proceso, servicio y usuario.** Entorno: aplicación de demostración y servicio existente benigno. Tareas: observar PID, cuenta de ejecución y recursos; relacionarlos con servicios; comprobar estado sin detener componentes críticos. Evidencia: tabla de relaciones. Éxito: no concluir que un nombre conocido hace confiable cualquier ejecutable. Recuperación: cerrar la aplicación propia.

**L13C · Configuración y Registro.** Entorno: exportación sintética de una clave de aplicación. Tareas: interpretar tipos de valor; comparar dos versiones; identificar ámbito de usuario/máquina; redactar plan de cambio y reversión sin aplicarlo al Registro del sistema. Evidencia: diff y justificación. Éxito: no extrapolar una exportación parcial a una copia completa de Windows. Recuperación: conservar el archivo original.

**Dominio:** identificar versión y contexto de ejecución antes de utilizar instrucciones. **Error frecuente:** tratar todas las ediciones y compilaciones como equivalentes.

## M14 · CMD y utilidades nativas

**Entrada:** M13. **Resultado:** trabajar desde `cmd.exe` y comprender sus reglas sin confundirlas con PowerShell o Bash.

**Unidades:** comandos internos/externos; ayuda y PATH; unidades y directorio actual; variables `%VAR%`; rutas entrecomilladas; redirecciones y pipes de texto; búsqueda; archivos/atributos; códigos de salida; utilidades administrativas de consulta; localización y codificación de consola.

**Herramientas:** `help`, `where`, `cd /d`, `dir`, `type`, `more`, `findstr`, `fc`, `copy`, `move`, `mkdir`, `attrib`, `set`, `whoami`, `tasklist`, `ipconfig`, `route print`, `netstat`, `sc.exe query`, `schtasks /query`, `robocopy` con modo de listado antes de copiar. Se escribe `sc.exe` para evitar confundir un ejecutable con un alias de otro shell.

**L14A · Navegación y búsqueda.** Entorno: carpeta propia con espacios y dos unidades disponibles. Tareas: cambiar unidad/directorio; localizar archivos por extensión; inspeccionar atributos y contenido; comparar dos versiones. Evidencia: transcripción saneada y resultados. Éxito: operar correctamente con rutas con espacios y explicar `cd /d`. Recuperación: ninguna modificación sobre originales.

**L14B · Inventario desde CMD.** Entorno: Windows nativo, cuenta estándar. Tareas: recopilar identidad, procesos, servicios y red de forma acotada; separar salidas; documentar límites de permisos y texto localizado. Evidencia: informe sin contraseñas ni perfiles completos. Éxito: no interpretar acceso denegado como ausencia de un objeto. Recuperación: proteger o eliminar salidas tras evaluación.

**L14C · Copia controlada.** Entorno: directorio origen y destino de práctica. Tareas: previsualizar una copia con herramienta nativa; revisar qué se preserva; ejecutar sobre datos sintéticos; interpretar códigos de retorno documentados; comprobar diferencias. Evidencia: plan, log y comparación. Éxito: distinguir advertencia, cambios y fallo según el programa, sin asumir que cualquier valor no cero significa lo mismo. Recuperación: retirar únicamente el destino de ensayo.

**Dominio:** ejecutar utilidades en su shell real. **Error frecuente:** usar opciones GNU en comandos Windows o aplicar opciones de espejo sin comprender posibles borrados.

## M15 · BAT y mantenimiento de automatización heredada

**Entrada:** M14, M11. **Resultado:** comprender, mantener y migrar scripts por lotes pequeños sin convertir BAT en la solución para todos los problemas.

**Unidades:** `.bat` y `.cmd`; `@echo off`; parámetros y expansión de ruta; `setlocal/endlocal`; asignación segura; expansión inmediata y diferida; `if`, `for`, `call`, etiquetas y subrutinas; `errorlevel`; redirecciones; metacaracteres; límites de parsing y Unicode; migración hacia PowerShell.

**Herramientas:** `cmd.exe`, editor, `set`, `setlocal`, `if`, `for`, `call`, `exit /b`. Evitar manipular secretos o entradas no confiables concatenadas. Desactivar eco no equivale a ocultar datos del sistema de auditoría.

**L15A · Script de carpeta.** Entorno: dataset sintético. Tareas: aceptar una ruta; validarla; listar archivos; devolver un código de resultado; mostrar ayuda; probar argumento ausente y ruta con espacios. Evidencia: script y tabla de pruebas. Éxito: no ejecutar una entrada como comando y no modificar datos. Recuperación: eliminar solo salidas de prueba.

**L15B · Diagnóstico de expansión.** Entorno: lote didáctico con bucle y variables. Tareas: predecir salida; comparar expansión al parsear frente a expansión diferida; probar nombres con signos de exclamación; corregir una pérdida de información. Evidencia: explicación y resultados. Éxito: reconocer cuándo la solución exige otro lenguaje. Recuperación: conservar versiones en Git.

**L15C · Migración justificada.** Entorno: un script BAT propio. Tareas: expresar su contrato; reescribirlo con objetos en PowerShell tras la demostración del docente; comparar salidas, errores y mantenimiento; explicar lo que deja de depender del idioma del SO. Evidencia: comparación y casos de prueba reutilizables. Éxito: preservar comportamiento funcional, no traducir línea por línea sin revisión. Recuperación: mantener el script anterior como referencia, no como tarea activa.

**Dominio:** leer lotes heredados, identificar riesgos y decidir cuándo migrar. **Error frecuente:** `errorlevel` evaluado tarde o expansión diferida que altera nombres válidos.

## M16 · PowerShell: objetos, lenguaje y datos

**Entrada:** M13, M15. **Resultado:** construir pipelines de objetos y funciones con contrato, validación y salida estructurada.

**Unidades:** motores 5.1/7 y módulos compatibles; cmdlets verbo-sustantivo y ayuda; tipos, propiedades y métodos; pipeline; selección y filtrado; arrays, hashtables y `PSCustomObject`; funciones/parámetros/validación; control de flujo; providers; errores terminantes/no terminantes; excepciones; JSON/CSV/XML; formatos y codificaciones; ejecutables nativos y `$LASTEXITCODE`.

**Herramientas:** `Get-Help`, `Get-Command`, `Get-Member`, `Select-Object`, `Where-Object`, `Sort-Object`, `Group-Object`, `Measure-Object`, `ForEach-Object`, `Import-Csv`, `Export-Csv`, `ConvertFrom-Json`, `ConvertTo-Json`, `Test-Path`, `Join-Path`. `Format-Table` se reserva para presentación final, no para datos que deban exportarse.

**L16A · Texto frente a objetos.** Entorno: PowerShell con dataset sintético y procesos propios consultables. Tareas: inspeccionar tipos y propiedades; filtrar y agrupar; exportar CSV/JSON; verificar campos; contrastar formato visual y dato subyacente. Evidencia: pipeline y salida. Éxito: no analizar tablas visuales cuando existen propiedades. Recuperación: mantener únicamente salidas sanitizadas.

**L16B · Función segura.** Entorno: archivos del curso. Tareas: escribir función con parámetro de ruta; validar entrada; obtener propiedades y SHA-256 de archivos regulares; manejar excepción; emitir objetos, no mensajes mezclados. Evidencia: ayuda y pruebas de ruta vacía, inválida y con espacios. Éxito: error explícito y resultado interpretable. Recuperación: solo lectura de entradas.

**L16C · Datos y regresión.** Entorno: JSON y CSV con campos ausentes. Tareas: verificar esquema acordado; preservar tipos cuando el formato lo permita; probar profundidad de JSON, Unicode y fechas; comparar salidas entre motores disponibles. Evidencia: pruebas y matriz de compatibilidad. Éxito: documentar diferencias reales, no afirmar portabilidad universal. Recuperación: conservar originales.

**Dominio:** seleccionar por propiedades, distinguir datos de formato y errores de comandos nativos. **Error frecuente:** considerar la execution policy un control que impide ejecutar cualquier código no autorizado.

## M17 · Administración Windows con PowerShell

**Entrada:** M16. **Resultado:** inventariar y realizar cambios pequeños sobre Windows con verificación y posibilidad de recuperación.

**Unidades:** procesos/servicios y dependencias; CIM/WMI y consulta de clases; filesystem y Registro como providers; NTFS/ACL/SID; tareas programadas; instalación/actualizaciones y procedencia; administración de cuentas locales; políticas aplicadas; rendimiento; `ShouldProcess`, `-WhatIf` y sus límites; transcripción y gestión de errores.

**Herramientas:** `Get-Process`, `Get-Service`, `Get-CimInstance`, `Get-ItemProperty`, `Get-Acl`, `Get-LocalUser`, `Get-LocalGroupMember`, `Get-ScheduledTask`, `Get-WinEvent`; herramientas gráficas equivalentes. Disponibilidad depende de Windows, arquitectura y módulos. No exigir `Get-WmiObject` en PowerShell 7.

**L17A · Inventario normalizado.** Entorno: VM Windows. Tareas: seleccionar clases/campos de equipo y servicios; exportar objetos con fecha y origen; manejar acceso denegado; comparar con GUI. Evidencia: inventario sanitizado y contrato de campos. Éxito: no usar exportaciones completas de Registro o perfiles. Recuperación: proteger salidas.

**L17B · Permisos efectivos.** Entorno: carpeta de aplicación ficticia y dos cuentas. Tareas: definir permisos esperados; consultar ACL e herencia; contrastar permisos efectivos mediante pruebas; planificar un cambio mínimo; ejecutar bajo supervisión. Evidencia: antes/después y prueba denegada. Éxito: no otorgar control total general para resolver acceso. Recuperación: restaurar ACL inicial y validar.

**L17C · Servicio y tarea auditables.** Entorno: tarea benigna que escribe un resumen en carpeta propia. Tareas: declarar usuario, directorio y trigger; probar manualmente; programar; comprobar log y fallo controlado; revisar con GUI y CLI. Evidencia: definición, resultado y procedimiento de baja. Éxito: ejecución sin privilegios innecesarios. Recuperación: retirar solo la tarea del ejercicio.

**Dominio:** previsualizar no garantiza reversibilidad; verificar si el comando implementa `WhatIf`. **Error frecuente:** cambiar un servicio sin revisar dependencias ni identidad.

## M18 · Identidad, red y administración remota

**Entrada:** M10, M17. **Resultado:** operar una conexión administrativa autorizada y explicar las dependencias de identidad, transporte y confianza.

**Unidades:** cuentas/SID/grupos/tokens; local frente a dominio; AD DS, DNS, LDAP y Kerberos como base conceptual; GPO y alcance; MFA y protección de credenciales; firewall/perfiles; RDP y seguridad de transporte; WinRM/PowerShell Remoting; SSH en Windows cuando esté disponible; JEA como delegación restringida; auditoría de sesiones y gestión de acceso temporal.

**Herramientas:** ajustes de red y firewall; `Get-NetIPConfiguration`, `Get-NetRoute`, `Get-NetTCPConnection`, `Resolve-DnsName`, `Test-NetConnection`, `Get-NetFirewallProfile`, `Get-NetFirewallRule`, `gpresult`; `Enter-PSSession` y `Invoke-Command` únicamente hacia endpoints preparados. La configuración remota del docente restringe origen, identidad y funciones. No se utilizan comodines globales de confianza ni listeners abiertos a Internet.

**L18A · Diagnóstico Windows de red.** Entorno: Windows y servidor propio asignado. Tareas: localizar DNS/ruta/puerto; comprobar servicio por nombre y dirección de laboratorio; diferenciar resolución de autorización. Evidencia: cadena de comprobaciones. Éxito: reconocer qué prueba genera tráfico y a qué destino. Recuperación: restaurar solo parámetros de prueba.

**L18B · Sesión delegada.** Entorno: endpoint preparado por el docente y cuenta con alcance limitado. Tareas: verificar destino y mecanismo de autenticación; ejecutar una consulta permitida; comprobar que una acción no autorizada es rechazada; cerrar sesión; revisar registros. Evidencia: matriz autorización/resultado. Éxito: no ampliar permisos para evitar una restricción prevista. Recuperación: revocar acceso temporal.

**L18C · Directorio y política.** Entorno: dominio aislado opcional o exportaciones sintéticas claramente etiquetadas. Tareas: representar usuario/grupo/equipo/GPO; explicar herencia y DNS; analizar una política aplicada; proponer delegación. Evidencia: mapa y diagnóstico. Éxito: distinguir laboratorio nativo de análisis de datos offline. Recuperación: sin cambios al directorio fuera de la unidad organizativa de práctica.

**Dominio:** una conexión cifrada no sustituye autenticación y autorización correctas. **Error frecuente:** publicar RDP/WinRM para simplificar el acceso al laboratorio.

## M19 · Eventos, protección y recuperación Windows

**Entrada:** M17, M18. **Resultado:** evaluar una baseline, consultar eventos y demostrar una recuperación sin desactivar controles esenciales.

**Unidades:** canales/proveedores/Event IDs y política de auditoría; Security/System/Application; PowerShell logging; Sysmon como fuente adicional; Defender y firewall; BitLocker y recuperación; actualizaciones y reducción de superficie; políticas de aplicación como ampliación; copias, restauración y evidencia; permisos de logs y retención.

**Herramientas:** Seguridad de Windows, Visor de eventos, configuración de recuperación; `Get-WinEvent`, `wevtutil qe/epl`, `auditpol /get`, `Get-MpComputerStatus` cuando corresponda, consultas de BitLocker y firewall. No extraer protectores de recuperación a Git. Sysmon requiere configuración y su ausencia no prueba ausencia de actividad.

**L19A · Lectura contextual de eventos.** Entorno: eventos exportados o VM con auditoría conocida. Tareas: seleccionar proveedor/canal/intervalo; buscar un evento benigno generado por el docente; asociar usuario y hora; explicar qué eventos no deberían aparecer por configuración. Evidencia: consulta y ficha de cobertura. Éxito: no identificar eventos solo por número sin proveedor. Recuperación: conservar exportación original.

**L19B · Baseline razonada.** Entorno: clon Windows. Tareas: revisar actualización, cuentas, servicios, firewall, cifrado, registro y protección; priorizar cinco hallazgos; corregir uno aprobado; verificar funcionalidad. Evidencia: checklist y excepción documentada. Éxito: mantener protección y acceso administrativo. Recuperación: rollback probado del cambio.

**L19C · Recuperación y evidencia.** Entorno: documentos ficticios con backup. Tareas: preservar el estado inicial del caso; restaurar una copia en destino distinto; comprobar hash, permisos y apertura; redactar lo que la restauración no conserva. Evidencia: acta y resultado. Éxito: separar recuperación operativa de preservación forense. Recuperación: volver al snapshot de la práctica tras recoger evidencias.

**Checkpoint C3:** administrar Windows nativo, justificar PowerShell frente a BAT, verificar permisos y obtener eventos sin afirmar certezas fuera de la cobertura.
