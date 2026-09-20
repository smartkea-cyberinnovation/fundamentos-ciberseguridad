# Fuentes primarias y control de vigencia

Revisión documental de esta edición: **2026-09-14**. Las fuentes sustentan conceptos y decisiones técnicas; no certifican el curso ni acreditan ejecución de laboratorios. El selector de versión de una web no determina la versión instalada en el equipo del alumno.

| ID | Fuente primaria | Aplicación |
|---|---|---|
| S01 | GNU: [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) y [exit status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) | Expansión, comillas, flujo de ejecución y errores |
| S02 | Proyecto [systemd](https://systemd.io/) | Servicios, unidades, contexto y documentación local |
| S03 | Microsoft: [Windows Commands](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) | CMD/BAT y diferencias con PowerShell |
| S04 | Microsoft: [about_Pipelines](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines) y [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) | Objetos, presentación y límites de execution policy |
| S05 | Microsoft: [about_Remote_Requirements](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_requirements) | Requisitos y transportes de administración remota |
| S06 | Microsoft Sysinternals: [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) | Telemetría adicional y configuración; no instalación obligatoria |
| S07 | Apple: [Platform Security](https://support.apple.com/guide/security/welcome/web) | Integridad de plataforma, cifrado y controles nativos |
| S08 | OpenBSD/OpenSSH: [ssh(1)](https://man.openbsd.org/ssh) | Confianza del host y administración autorizada |
| S09 | Docker: [stack deploy](https://docs.docker.com/engine/swarm/stack-deploy/) y [routing mesh](https://docs.docker.com/engine/swarm/ingress/) | Separación Compose/Swarm y alcance de puertos publicados |
| S10 | NIST: [actualizaciones de NICE](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/about/nice-framework-latest-updates) | Referencia de tareas, conocimientos y habilidades |
| S11 | NIST: [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Respuesta a incidentes y gestión del riesgo |
| S12 | MITRE: [ATT&CK](https://attack.mitre.org/) | Contexto de comportamientos; no atribución automática |
| S13 | CIS: [Benchmarks](https://www.cisecurity.org/cis-benchmarks) | Selección de referencias por producto; no declaración de conformidad |
| S14 | Ollama: [CLI](https://docs.ollama.com/cli) | Ejemplo opcional de modelo desde terminal; no ejecutado en esta entrega |
| S15 | Python: [biblioteca estándar](https://docs.python.org/3/library/) | Lectura complementaria sobre JSON, archivos, hashing y fechas |
| S16 | Proyecto zsh: [Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html) | Opciones y expansión de archivos; diferencias respecto a Bash |
| S17 | Python: [http.server](https://docs.python.org/3/library/http.server.html) | Servidor de demostración y advertencia de no utilizarlo en producción |

## Decisiones derivadas

La edición conserva ejemplos de shells separados. Las opciones y el intérprete se comprueban en el sistema local; una característica del manual reciente no se presupone disponible en Bash incluido en macOS. El kit Bash probado aquí no acredita el ejemplo zsh. [S01, S16]

PowerShell se enseña mediante objetos, no análisis de tablas visuales. Execution policy no se presenta como frontera de seguridad ni se pide desactivarla para ejecutar un ejemplo. Una política que impida el script debe resolverse por el procedimiento autorizado del entorno. [S04]

El servicio web se mantiene pequeño, sin servir archivos del usuario y con rutas fijas. Es un recurso docente HTTP, sin autenticación o TLS: no se declara seguro para producción. [S17]

Compose y Swarm tienen manifiestos distintos. No se presupone que una opción de Compose sea aceptada por `docker stack deploy`. La variante Swarm no publica puertos, evitando atribuir a su routing mesh el bind a localhost de la variante Compose. Se requiere validación nativa antes de utilizar el clúster. [S09]

La matriz de competencias es interpretación pedagógica, no un mapeo exhaustivo de identificadores NICE ni una certificación de puestos. Los materiales de bastionado no reproducen un benchmark completo ni acreditan conformidad CIS. [S10, S13]

## Versiones y alcance

Se retiran las afirmaciones de versiones exactas de portadas que no son necesarias para la planificación. Las versiones realmente ejecutadas figuran en [resultados](qa/RESULTADOS.md). Las referencias son páginas mantenidas por sus autores y pueden cambiar después de esta revisión.

Consultar `man`, ayuda del programa instalado, `Get-Help`, `Get-Command` y manuales del proveedor para versión/edición/arquitectura elegidas. Los comandos de lectura también pueden generar telemetría o alterar metadatos: no se presentan como adquisición forense sin impacto.

Antes de cada cohorte, registrar producto, versión, soporte, licencia, procedencia, fecha de consulta, comando de comprobación y laboratorios afectados. Revisar enlaces y repetir pruebas después de cambios relevantes. Bibliografía complementaria pendiente de seleccionar según stack: manuales oficiales de Nginx/Apache/IIS, hipervisor, Kubernetes y solución de copias/colector elegidos.

No se incorporan correos, datos personales de terceros, vínculos internos de trabajo ni materiales institucionales. Se enlazan fuentes; no se copian manuales íntegros.
