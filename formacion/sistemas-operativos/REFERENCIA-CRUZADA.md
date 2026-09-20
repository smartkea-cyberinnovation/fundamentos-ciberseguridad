# Tareas equivalentes: Linux, Windows y macOS

Referencia de **tareas**, no equivalencia binaria de comandos. Cada utilidad conserva su sintaxis, permisos, formato y efectos. Consultar ayuda local y [fuentes](FUENTES.md). Windows usa PowerShell salvo indicación CMD. Una consulta de lectura puede producir telemetría; no es sinónimo de adquisición forense sin impacto.

| Tarea | Linux | Windows | macOS |
|---|---|---|---|
| Identificar versión | `/etc/os-release`, `uname` | `Get-ComputerInfo`, `winver` | `sw_vers`, `uname` |
| Ver shell/motor | versión de Bash y proceso actual | `$PSVersionTable`, `cmd /?` | versión de zsh y proceso actual |
| Ayuda | `man`, `info`, `--help` | `Get-Help`, `Get-Command`, `/?` | `man`, ayuda de Terminal |
| Resolver ejecutable | `type`, `command -v` | `Get-Command`, `where.exe` | `type`, `command -v` |
| Directorio actual | `pwd` | `Get-Location`, CMD `cd` | `pwd` |
| Listar archivos | `ls`, `find` | `Get-ChildItem`, CMD `dir` | `ls`, `find` |
| Navegar/crear carpetas | `cd`, `mkdir` | `Set-Location`, `New-Item` | `cd`, `mkdir` |
| Leer contenido | `less`, `cat`, `head`, `tail` | `Get-Content`, CMD `type` | `less`, `cat`, `head`, `tail` |
| Copiar/mover | `cp`, `mv` | `Copy-Item`, `Move-Item`, `robocopy` | `cp`, `mv`, `ditto` según preservación |
| Buscar nombres | `find` con límites | `Get-ChildItem` con filtro/alcance | `find`, Spotlight para objetivos compatibles |
| Buscar texto | `grep`, `awk`, `sed` | `Select-String`, CMD `findstr` | `grep`, `awk`, `sed` BSD |
| Comparar archivos | `diff`, `cmp` | `Compare-Object` para datos; CMD `fc` | `diff`, `cmp` |
| Tamaños/metadatos | `stat`, `du`, `file` | `Get-Item`, propiedades del archivo | `stat`, `du`, `file`, `ls -le@` |
| Hash SHA-256 | `sha256sum` | `Get-FileHash -Algorithm SHA256` | `shasum -a 256` |
| Enlaces | `ln`, `readlink` | enlaces/reparse points y `Get-Item` | `ln`, `readlink`; alias Finder no idéntico |
| Identidad y grupos | `id`, `groups`, `getent` | `whoami`, cmdlets LocalAccounts | `id`, consultas acotadas `dscl` |
| Permisos | `stat`, `getfacl`, `chmod`, `setfacl` | `Get-Acl`, `icacls`, seguridad avanzada | permisos Unix, ACL, TCC por separado |
| Privilegios | `sudo -l`, pertenencia a grupos | token, UAC, grupos y privilegios | grupos, sudo, TCC y controles de plataforma |
| Procesos | `ps`, `top`, `pgrep` | `Get-Process`, `tasklist` | `ps`, `top`, Monitor de Actividad |
| Recursos abiertos | `lsof`, `/proc` si corresponde | herramientas de procesos/handles aprobadas | `lsof` y permisos pertinentes |
| Servicios | `systemctl` en systemd | `Get-Service`, `sc.exe`, Servicios | `launchctl`, servicios de Compartir |
| Programación | timers, cron | ScheduledTasks, `schtasks` | launchd; no asumir cron como patrón principal |
| Software | `apt/dpkg` o `dnf/rpm` | herramientas nativas/gestor aprobado | `softwareupdate`, gestores aprobados de terceros |
| Discos/montajes | `lsblk`, `findmnt`, `df` | `Get-Disk`, `Get-Volume`, Administración de discos | `diskutil`, `df`, Utilidad de Discos |
| Cifrado de volumen | tecnología elegida y recuperación | BitLocker según edición | FileVault y recuperación |
| Interfaces/IP | `ip` | `Get-NetIPConfiguration`, `ipconfig` | `ifconfig`, `networksetup` |
| Rutas | `ip route` | `Get-NetRoute`, `route print` | `route -n get default`, consultas de ruta |
| Resolución DNS | `getent hosts`, `resolvectl`, `dig` | `Resolve-DnsName`, `nslookup` | `scutil --dns`, herramientas DNS instaladas |
| Sockets/listeners | `ss` | `Get-NetTCPConnection`, `netstat` | `lsof -i`, herramientas nativas de red |
| Firewall | nftables/ufw/firewalld según stack | perfiles y reglas Windows Firewall | firewall de aplicaciones; PF es otra capa |
| HTTP/TLS | `curl` y herramientas TLS | `curl.exe`, `Invoke-WebRequest` | `curl` y herramientas TLS instaladas |
| Sesión remota | SSH | RDP, WinRM o SSH según endpoint | SSH; compartición GUI aprobada |
| Transferencia | SFTP/SCP/rsync | SFTP/SCP disponibles, copia autorizada | SFTP/SCP/rsync, comprobar versiones |
| Logs | journal/syslog/audit según configuración | Event Log, PowerShell, Sysmon opcional | Unified Log, logs de aplicación |
| Configuración | archivos, entorno, drop-ins | Registro, políticas, archivos, entorno | plist, perfiles, preferencias, entorno |
| Backup | solución elegida y restauración | solución elegida y restauración | Time Machine/solución elegida y restauración |
| Texto estructurado | parser y `jq` opcional | objetos, JSON/CSV/XML | parser y `plutil` para plist |
| Automatización | Bash y Python opcional | PowerShell; BAT para legado | zsh, Bash declarado y Python opcional |

## Diferencias que deben quedar demostradas

PATH y perfiles: no son idénticos entre shell interactiva, tarea, servicio y sesión remota. Un alias no se comporta como el ejecutable homónimo. Windows es normalmente insensible a mayúsculas en muchos contextos; Linux y los volúmenes macOS elegidos pueden comportarse de otra forma. Se prueba el filesystem concreto en vez de asumir reglas globales.

El pipeline Unix suele transportar texto/bytes; PowerShell transporta objetos entre cmdlets y debe tratar aparte programas nativos. `Format-Table` no reemplaza exportación de datos. Las versiones de PowerShell difieren en codificaciones y manejo de ejecutables: comprobar resultados.

`stat`, `date`, `sed`, `find` y otras utilidades GNU/BSD no comparten necesariamente opciones. Los permisos del SO, ACL, política de aplicación y controles de privacidad pueden concurrir: una sola capa no explica siempre el acceso efectivo.

Un nombre de proceso, ruta o servicio puede ser un indicador útil, pero debe contrastarse con origen, firma/hash cuando proceda, cuenta, padre, versión y contexto. Ninguna columna es una receta automática de análisis forense.
