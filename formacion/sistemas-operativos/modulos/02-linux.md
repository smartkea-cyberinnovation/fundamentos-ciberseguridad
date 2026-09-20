# M05–M12 · Linux y Bash

Cada módulo: 14 h, con 5 h de teoría y tres laboratorios de 3 h. Leer [el contrato de laboratorio](../LABORATORIO.md). Fuentes: [S01, S02, S08, S13 y manuales locales](../FUENTES.md). Sistema base: VM Linux con soporte vigente; una segunda familia de distribución se utiliza para comparar, no para mezclar gestores.

## M05 · Shell, directorios y ficheros

**Entrada:** M04. **Resultado:** localizar, crear, copiar, comparar y organizar archivos de forma segura, interpretando rutas y metadatos.

**Unidades:** jerarquía `/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/run`, `/proc` y `/sys`; rutas absolutas/relativas; nombres ocultos; globbing y quoting; enlaces duros y simbólicos; archivos ordinarios frente a dispositivos; tamaño, propietario, timestamps y permisos; edición segura y comparación antes de sustituir.

**Herramientas:** explorador y editor; `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `stat`, `file`, `readlink`, `ln`, `diff`, `cmp`, `du`, `find`, `sha256sum`. Enseñar el efecto de cada opción antes de usar recursividad. No practicar sobre `/dev` ni escribir en `/proc` o `/sys`.

**L05A · Archivo perdido.** Entorno: árbol sintético de 20 ficheros. Tareas: recorrer por GUI/CLI; buscar por nombre, tipo y profundidad; identificar archivos ocultos y espacios; justificar rutas absolutas/relativas. Evidencia: inventario y comandos comentados. Éxito: localizar los objetivos sin búsquedas innecesarias por todo el sistema. Recuperación: volver al directorio inicial y no alterar originales.

**L05B · Copiar sin confundir.** Entorno: dos carpetas del alumno. Tareas: copiar archivos y comparar contenidos; crear enlaces en el volumen de práctica; observar cambios de nombre y de metadatos; explicar qué preserva cada operación. Evidencia: tabla antes/después con hash. Éxito: distinguir copia, enlace y referencia rota. Recuperación: retirar solo los enlaces y copias creados.

**L05C · Cambio de configuración.** Entorno: configuración de aplicación ficticia, sin efecto de sistema. Tareas: guardar copia; editar una clave; revisar diff; validar formato; simular restauración. Evidencia: versión original, diff y verificación. Éxito: cero cambios fuera del archivo autorizado y rollback reproducible. Recuperación: reponer la versión inicial.

**Dominio:** trabajar con nombres que contienen espacios y no interpretar metadatos como prueba concluyente de autoría. **Error frecuente:** comandos recursivos desde un directorio equivocado.

## M06 · Texto, búsqueda y pipelines

**Entrada:** M05. **Resultado:** transformar datos de texto y construir búsquedas acotadas, repetibles y comprobables.

**Unidades:** flujo de bytes/líneas; stdout/stderr; pipes y redirecciones; literales, glob y regex; filtros y agregación; ordenación y locale; delimitadores y nombres con saltos de línea; tratamiento de errores y archivos vacíos; datos estructurados frente a texto libre.

**Herramientas:** `cat`, `less`, `head`, `tail`, `wc`, `cut`, `tr`, `sort`, `uniq`, `grep`, `sed`, `awk`, `find`, `xargs`, `tee`; `jq` como herramienta adicional para JSON. No analizar JSON anidado con expresiones regulares. Usar delimitación NUL donde la herramienta la soporte.

**L06A · Resumen de actividad.** Entorno: 30 líneas de log sintético. Tareas: filtrar por intervalo y evento; contar resultados; agrupar por campo; conservar entrada sin cambios. Evidencia: pipeline, resultado y recuento manual de control. Éxito: total consistente y distinción entre cero coincidencias y fallo. Recuperación: conservar el log original.

**L06B · Nombres difíciles.** Entorno: archivos con espacios, guiones iniciales y Unicode. Tareas: comparar un recorrido ingenuo con otro seguro; tratar nombres como argumentos, no como código; explicar comillas y separadores. Evidencia: prueba positiva y caso límite. Éxito: cada archivo se procesa una sola vez. Recuperación: eliminar solamente el dataset propio tras documentarlo.

**L06C · Informe de diferencias.** Entorno: dos exportaciones sintéticas. Tareas: normalizar solo los campos definidos; deduplicar sin perder procedencia; comparar; explicar diferencias por orden, formato y contenido. Evidencia: salida ordenada y reglas de normalización. Éxito: no borrar diferencias sustantivas durante la limpieza. Recuperación: repetir desde originales para comprobar determinismo.

**Dominio:** justificar patrón y denominador. **Error frecuente:** interpretar una coincidencia parcial de una IP o un dominio como identidad exacta.

## M07 · Usuarios, permisos y privilegios

**Entrada:** M05. **Resultado:** diseñar y verificar un acceso de mínimo privilegio, sin romper autenticación ni exponer secretos.

**Unidades:** UID/GID y cuentas de servicio; usuarios locales y resolución de identidades; permisos rwx y significado en directorios; umask; ACL y máscara; propietario/grupo; sudo y delegación; PAM/NSS como arquitectura; capabilities y bits especiales como superficie de auditoría; AppArmor/SELinux como control adicional; ciclo de vida de cuentas.

**Herramientas:** ajustes de usuarios; `id`, `getent`, `groups`, `stat`, `namei`, `getfacl`, `setfacl`, `chmod`, `chown`, `umask`, `sudo -l`; `useradd/usermod/userdel` o equivalentes de distribución para cuentas ficticias, bajo supervisión. Leer capacidades con herramientas instaladas; no se practican escaladas de privilegio.

**L07A · Carpeta de equipo.** Entorno: VM y dos cuentas ficticias. Tareas: definir matriz lectura/escritura; aplicar grupo y permisos en carpeta dedicada; verificar con ambas identidades; explicar acceso a los directorios padres. Evidencia: matriz y pruebas positivas/negativas. Éxito: colaboración sin permisos globales. Recuperación: reponer ACL original y retirar cuentas de la práctica bajo control docente.

**L07B · Auditoría de privilegios.** Entorno: snapshot con permisos de ejemplo. Tareas: inventariar miembros administrativos, reglas delegadas y permisos del directorio de una aplicación; distinguir necesidad funcional de exceso; proponer corrección. Evidencia: hallazgo con impacto y propietario. Éxito: justificar el mínimo privilegio sin intentar explotar el fallo. Recuperación: no modificar reglas de autenticación.

**L07C · Alta y baja controladas.** Entorno: VM desechable. Tareas: diseñar solicitud, aprobación y expiración; crear una cuenta de laboratorio; comprobar acceso asignado; deshabilitarla sin destruir datos necesarios. Evidencia: registro de ciclo de vida y verificación. Éxito: ausencia de privilegios residuales y conservación documentada. Recuperación: restaurar snapshot o retirar la cuenta con plan aprobado.

**Dominio:** un permiso visible no basta: verificar permiso efectivo, ACL, máscara y política adicional. **Error frecuente:** resolver cualquier fallo con permisos universales.

## M08 · Procesos, paquetes, servicios y planificación

**Entrada:** M06, M07. **Resultado:** diagnosticar y operar servicios, software y tareas con trazabilidad y sin confundir configuración con estado.

**Unidades:** procesos, señales, jobs y recursos; paquetes, repositorios firmados, dependencias y actualizaciones; systemd unit/service/timer/socket; start/stop frente a enable/disable; archivos de unidad y overrides; cron y entorno restringido; journal y errores de arranque; aislamiento de servicio y cuentas dedicadas.

**Herramientas:** monitor de procesos y gestor de software; `ps`, `top`, `pgrep`, `jobs`, `wait`, `systemctl`, `journalctl`, `crontab`; `apt/dpkg` o `dnf/rpm`. Cambios siempre sobre servicio de demostración; no detener componentes de seguridad ni procesos de otros usuarios.

**L08A · Proceso o servicio.** Entorno: VM con servicio de texto/estado de laboratorio. Tareas: asociar unidad, proceso, usuario, ejecutable y log; comparar servicio activo y habilitado al arranque; explicar dependencias. Evidencia: ficha de servicio. Éxito: identificar por qué un proceso existe sin interfaz visible. Recuperación: conservar configuración de arranque original.

**L08B · Actualización controlada.** Entorno: clon de VM. Tareas: inventariar versiones; revisar origen de paquetes; simular/resumir cambios del gestor; aplicar una actualización aprobada; comprobar servicio y rollback disponible. Evidencia: ticket y prueba funcional. Éxito: no introducir repositorios no aprobados ni asumir que actualizar nunca rompe dependencias. Recuperación: restaurar clon si falla la comprobación.

**L08C · Tarea periódica legítima.** Entorno: script propio que genera un resumen sin secretos. Tareas: ejecutarlo a mano; declarar ruta, usuario y entorno; programarlo con timer o cron; comprobar éxito y fallo controlado. Evidencia: configuración, timestamp y log. Éxito: ejecución con privilegios mínimos y sin duplicados. Recuperación: retirar únicamente la programación creada.

**Dominio:** localizar causa en logs antes de reiniciar repetidamente. **Error frecuente:** scripts que funcionan en sesión interactiva pero dependen de PATH o variables ausentes en una tarea.

## M09 · Almacenamiento, copias y recuperación

**Entrada:** M07, M08. **Resultado:** explicar almacenamiento y recuperar datos de laboratorio, distinguiendo integridad, disponibilidad y evidencia.

**Unidades:** dispositivos, particiones, volúmenes y filesystem; inodos y capacidad; mount y opciones; LVM/RAID como conceptos; ext4/XFS/Btrfs según distribución; cuotas y cifrado; archivado/compresión; respaldo completo/incremental; RPO/RTO; retención; snapshots y copias externas; borrado en SSD, TRIM y COW: límites de sobrescritura por archivo.

**Herramientas:** gestor de discos; `lsblk`, `findmnt`, `df`, `du`, `stat`, `tar`, `gzip`, `rsync`; comprobaciones de sistema de archivos solo sobre medios de prueba y según documentación, nunca reparaciones indiscriminadas del disco activo.

**L09A · Mapa de almacenamiento.** Entorno: VM y pequeño disco virtual adicional identificado por el docente. Tareas: inventariar dispositivos y montajes; distinguir tamaño aparente, ocupado y libre; analizar opciones; explicar un caso de inodos agotados mediante datos preparados. Evidencia: mapa y diagnóstico. Éxito: identificar inequívocamente el disco de práctica. Recuperación: no alterar el disco de sistema.

**L09B · Copia verificable.** Entorno: directorio de datos sintéticos. Tareas: crear manifiesto y respaldo; restaurar en ruta distinta; comparar contenido y permisos; explicar diferencias de metadatos entre formatos. Evidencia: manifiesto, resultados y tiempo de recuperación. Éxito: restauración útil, no solo archivo de backup existente. Recuperación: mantener originales y retirar restauración de ensayo.

**L09C · Ensayo de pérdida.** Entorno: copia desechable del dataset, nunca original. Tareas: simular pérdida de un documento; seleccionar punto de copia; restaurar; calcular pérdida potencial y duración; proponer retención y cifrado con recuperación. Evidencia: runbook y RPO/RTO medidos. Éxito: distinguir objetivo acordado de resultado observado. Recuperación: volver al estado base documentado.

**Dominio:** no presentar `rm`, una pasada de sobrescritura o snapshot como garantía universal de sanitización. **Error frecuente:** copias en el mismo fallo de almacenamiento y sin prueba de restauración.

## M10 · Red del host y exposición

**Entrada:** M08. **Resultado:** diagnosticar conectividad siguiendo capas y justificar los puertos que realmente deben estar accesibles.

**Unidades:** interfaces, direcciones, CIDR, IPv4/IPv6 y loopback; vecinos ARP/NDP; rutas; DNS y resolución local; DHCP; TCP/UDP, sockets y estados; firewall de host; proxy y VPN como conceptos; captura acotada y privacidad; diferencia entre puerto escuchando y accesibilidad efectiva.

**Herramientas:** configuración GUI de red; `ip`, `ss`, `ping`, `tracepath` si está instalado, `getent hosts`, `resolvectl` si existe, `dig` como paquete adicional, `curl`; `nft`, `ufw` o `firewall-cmd` según stack. No administrar varias capas de firewall sin comprender su interacción.

**L10A · Resolver una avería.** Entorno: dos VMs asignadas. Tareas: verificar enlace e IP; ruta al destino; DNS; conexión al puerto aprobado; respuesta de aplicación; formular hipótesis en ese orden. Evidencia: árbol de diagnóstico. Éxito: diferenciar timeout, rechazo, fallo DNS y fallo de aplicación. Recuperación: reponer exclusivamente la configuración alterada por el docente.

**L10B · Inventario de listeners.** Entorno: VM propia. Tareas: asociar sockets a procesos y usuarios cuando los permisos lo permitan; distinguir localhost de todas las interfaces; contrastar con el servicio esperado. Evidencia: matriz servicio/interfaz/puerto/finalidad. Éxito: justificar cada listener sin hacer escaneo externo. Recuperación: ninguna modificación.

**L10C · Regla mínima.** Entorno: clon con consola y conexión de administración de reserva. Tareas: formular flujo permitido; revisar reglas; aplicar restricción aprobada para un servicio de prueba; verificar un cliente autorizado y otro no autorizado. Evidencia: diff y pruebas. Éxito: servicio disponible para el cliente previsto y administración conservada. Recuperación: restaurar configuración conocida desde consola si fuera necesario.

**Dominio:** separar DNS, enrutamiento, transporte y HTTP. **Error frecuente:** desactivar todo el firewall para comprobar conectividad.

## M11 · Bash estructurado

**Entrada:** M06, M08. **Resultado:** escribir un script pequeño con contrato de entrada/salida, validación y comportamiento explicable.

**Unidades:** shebang y shell efectivo; parámetros posicionales y `getopts`; variables, expansión y comillas; arrays y versiones; condiciones, `case`, bucles y funciones; sustitución de comandos; aritmética; stdin/stdout/stderr; exit codes; ámbito y entorno; señales; lectura segura y temporales; depuración que no revele secretos.

**Herramientas:** Bash instalado, editor, `bash -n`, ShellCheck como complemento opcional revisado. `set -e` no se enseña como manejo universal de errores: se estudian contextos donde no aborta y se comprueban resultados explícitamente. No construir comandos concatenando entradas no confiables.

**L11A · CLI de inventario de carpeta.** Entorno: dataset L05. Tareas: aceptar una ruta; validar existencia; producir conteo y tamaños; separar errores; devolver estado coherente. Evidencia: script, ayuda y tres casos de prueba. Éxito: funcionar con espacios, carpeta vacía y ruta inválida. Recuperación: script de solo lectura sobre datos de práctica.

**L11B · Funciones y parsing.** Entorno: CSV sencillo y JSON preparado. Tareas: definir contrato; dividir funciones; utilizar parser apropiado; validar campos ausentes; mantener procedencia. Evidencia: salidas esperadas y casos inválidos. Éxito: no confundir validación de sintaxis con validez de negocio. Recuperación: no modificar los archivos de entrada.

**L11C · Errores controlados.** Entorno: script propio con fallo de permiso y comando ausente simulados. Tareas: capturar errores; limpiar temporales propios con `trap`; comprobar exit codes de pipeline; evitar logs con secretos. Evidencia: matriz fallo/resultado. Éxito: ausencia de éxito falso y de borrados fuera del directorio temporal. Recuperación: eliminar solo temporales identificados.

**Dominio:** explicar cada expansión y su posible división de palabras. **Error frecuente:** `eval`, variables sin comillas y considerar todo stderr como fallo fatal.

## M12 · Bash de operación y automatización segura

**Entrada:** M09–M11. **Resultado:** construir una automatización que pueda revisarse, repetirse y fallar de forma segura.

**Unidades:** idempotencia; modo lectura y dry-run; requisitos y versiones; validación de rutas; errores parciales; límites de ejecución y concurrencia; locks; logging estructurado; escritura temporal y sustitución controlada; permisos de salida; revisión estática; pruebas de regresión; configuración separada de secretos; documentación y empaquetado de una CLI.

**Herramientas:** Bash, `getopts`, `mktemp`, `trap`, `jq` opcional; mecanismos de bloqueo compatibles con la plataforma; ShellCheck y pruebas shell sencillas. No afirmar que `flock` u opciones GNU están presentes en macOS.

**L12A · Informe de salud.** Entorno: VM Linux propia. Tareas: recopilar versión, espacio, servicios definidos y estado de un puerto local autorizado; aplicar timeouts; generar salida estructurada; omitir variables de entorno completas. Evidencia: script, ejemplo sanitizado y pruebas. Éxito: estados OK/WARN/ERROR distinguibles y fallo parcial visible. Recuperación: solo salida de informe.

**L12B · Backup automatizado.** Entorno: dataset y destino de práctica. Tareas: validar origen/destino; implementar dry-run; impedir solapes peligrosos; ejecutar respaldo; verificar restauración; simular segundo lanzamiento. Evidencia: pruebas de idempotencia y recuperación. Éxito: no sobrescribir el original ni considerar la repetición como copia independiente. Recuperación: retirar únicamente datos de ensayo.

**L12C · Revisión adversarial del script.** Entorno: código del alumno y entradas sintéticas. Tareas: probar espacios, guiones, campos vacíos, permiso denegado y salida parcial; medir si informa correctamente; revisar con compañero; corregir y documentar. Evidencia: casos de prueba y diff. Éxito: no ejecutar entradas como comandos y no ocultar fallos. Recuperación: conservar la versión previa en Git.

**Checkpoint C2:** administrar y diagnosticar Linux sin recurrir a privilegios globales; demostrar una automatización repetible con fallos y recuperación.
