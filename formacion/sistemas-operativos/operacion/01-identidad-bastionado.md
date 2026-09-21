# Control operativo: identidades, perfiles y bastionado

**D22 · Edición docente ES/EN · 21 de septiembre de 2026.** Complementa M07, M08, M17, M18, M19, M22 y M23. No añade horas a las 480 planificadas ni altera el progreso. Las actividades requieren equipos propios del laboratorio y aprobación del docente; leer no equivale a ejecutar.

[Redes y recursos compartidos](#/recurso/D23) · [Navegación y TLS](#/recurso/D24) · [Detección y pruebas](#/recurso/D25)

## 1. Qué significa tener un sistema bajo control

El objetivo no es observar toda la vida de una persona. Es conocer qué dispositivos y servicios administramos, quién puede hacer qué, qué política se aplica realmente, cómo detectamos desviaciones y cómo recuperamos el servicio. Un inventario desconocido no se convierte en conforme por no emitir alertas.

Para cada equipo, mantener identificador de inventario, responsable, función, SO/edición/versión, soporte, ubicación, estado de gestión, identidad del directorio, fecha de última observación, exposición necesaria y método de recuperación. Relacionarlo con cuentas, datos, servicios, reglas y fuentes de registro. No incluir contraseñas, tokens o claves de recuperación en ese inventario ni en Git.

Antes de una operación: identificar equipo, sesión, shell, versión, directorio, privilegios y alcance. Después: comprobar estado efectivo, registrar el resultado y probar recuperación. Un informe de consola central demuestra una declaración del agente; una prueba funcional desde la identidad afectada aporta otra evidencia.

## 2. Identidad local, LDAP, AD DS y Entra ID

**Cuenta local:** identidad administrada por ese equipo, con su identificador y grupos. El mismo nombre de usuario en dos equipos no implica la misma identidad. En Linux se trabaja con UID/GID y resolución mediante NSS; en Windows con SID y tokens; en macOS con sus identidades locales y controles adicionales.

**LDAP:** protocolo para consultar o modificar un directorio según autenticación y permisos. No es por sí solo un dominio Windows, un segundo factor, una GPO o un sistema completo de gobierno. Separar búsqueda de identidad, autenticación y autorización. Un bind válido no autoriza acceso a todas las entradas.

**Active Directory Domain Services:** directorio y servicios de dominio. Se estudian DNS, Kerberos, objetos, grupos, unidades organizativas, equipos, replicación y delegación. Una OU sirve para organización y alcance de políticas; no sustituye un grupo de autorización. Una cuenta que puede unir equipos no necesita recibir administración del dominio.

**Microsoft Entra ID:** servicio de identidad cloud; no equivale a un controlador AD DS ni garantiza que una aplicación LDAP antigua pueda conectarse directamente. Distinguir dispositivo registrado, unido al dominio, unido a Entra e híbrido. Documentar la autoridad de cada atributo y el efecto de la sincronización.

En Linux integrado con AD, SSSD/realmd relacionan resolución de identidad, autenticación, acceso y creación de home. DNS y reloj son dependencias del acceso, no detalles accesorios. El ejemplo oficial de Ubuntu permite caché de credenciales: un inicio offline no demuestra validación reciente contra el controlador. [Ubuntu: SSSD con AD](https://ubuntu.com/server/docs/how-to/sssd/with-active-directory/).

## 3. Alta, cambio y baja: contrato comprobable

**Alta.** Solicitud y aprobación del responsable del recurso; identidad individual; grupo asociado al rol; expiración para accesos temporales; autenticación adecuada al servicio; creación del perfil solo si es necesario. Probar el recurso permitido y uno expresamente no permitido.

**Cambio de puesto.** Retirar permisos incompatibles antes o junto al nuevo acceso, revisar grupos anidados y derechos concedidos directamente. No copiar todos los permisos del compañero: puede arrastrar excepciones y privilegios que ya no necesita.

**Baja.** Inventariar directorio, cuentas locales, accesos SaaS, sesiones, tickets, certificados, claves SSH, dispositivos y cuentas de servicio asociadas. Deshabilitar la cuenta no implica revocar instantáneamente cada sesión ya emitida o cada acceso offline. Definir ventanas de revocación y verificar sesión nueva, sesión existente, cliente sin conexión y reconexión. Separar bloqueo de acceso, conservación de datos y eliminación del perfil; pueden tener plazos y responsables distintos.

**Identidades no humanas.** Cuenta de servicio con dueño, propósito, recursos y rotación. Evitar login interactivo cuando no sea necesario; no almacenar credenciales de un empleado en una tarea periódica. gMSA, identidades administradas u otras soluciones se seleccionan según plataforma y aplicación; no son universales.

**Privilegios.** Cuenta normal y administrativa separadas; delegación acotada; revisión periódica; recuperación de emergencia controlada y auditada. Windows LAPS gestiona contraseñas de administrador local en plataformas compatibles: no sustituye PAM completo ni la revisión de permisos del directorio. El informe registra estado de gestión, no el secreto. [Microsoft: Windows LAPS](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview).

## 4. Permisos efectivos y políticas aplicadas

Autenticación válida, pertenencia a un grupo y permiso efectivo son tres observaciones diferentes. Analizar identidad estable, grupos directos/anidados, token o caché actuales, ACL, herencia, derechos específicos y controles adicionales. Una modificación de grupos puede requerir renovar el contexto de acceso; no concluir que falló porque una sesión anterior conserva sus derechos.

En Linux: permisos del archivo y de directorios padres, ACL y máscara, sudo, capabilities y políticas SELinux/AppArmor. En Windows: DACL, grupos del token, derechos de inicio de sesión, UAC y política de aplicación. En macOS: permisos Unix/ACL, TCC, identidad del proceso, perfiles de gestión y protección de plataforma. No solucionar fallos con permisos universales o desactivación de controles.

Distinguir configuración local, GPO y MDM. Registrar origen, ámbito usuario/equipo, precedencia aplicable, conflictos, última actualización y resultado. La precedencia entre una GPO y un ajuste MDM depende de la configuración concreta: no enseñar que uno gana siempre. Consultar el resultado en el equipo, no solo el objeto editado en la consola.

## 5. Los cinco significados de perfil

| Perfil | Qué contiene o describe | Qué no demuestra |
|---|---|---|
| Perfil de usuario del SO | Home, preferencias y datos asociados a la sesión | No equivale a una cuenta del directorio ni a una copia restaurable |
| Perfil itinerante, redirección o contenedor de perfil | Ubicación y mecanismo de persistencia de parte del entorno | Sincronización no garantiza backup ni compatibilidad entre versiones |
| Perfil del navegador | Cookies, extensiones, preferencias y sesiones de ese navegador | Dos perfiles no son una frontera fuerte frente al dueño del mismo usuario del SO |
| Perfil de configuración/MDM | Conjunto de ajustes distribuidos al dispositivo o usuario | Instalarlo no prueba que todos los ajustes sean efectivos |
| Perfil de red/firewall | Contexto de aplicación de reglas del host | No identifica necesariamente al usuario ni al tenant SaaS |

En un equipo compartido, probar que el usuario B no recibe documentos, sesiones o autocompletado del A; revisar cierre de sesión, limpieza definida y datos que sí deben persistir. No copiar perfiles completos a un repositorio o a un equipo de un compañero. Probar restauración de datos y preferencias de laboratorio por separado de secretos.

## 6. Baseline y bastionado por función

Aplicar una línea base compatible con SO, versión y función; una estación docente y un controlador de dominio no comparten todas las necesidades. Secuencia: inventario → baseline elegida → desviación → impacto → cambio en clon → prueba funcional y negativa → recuperación → despliegue gradual → detección de deriva.

Controles mínimos a evaluar: soporte y actualizaciones; cuentas privilegiadas; permisos de servicios; software permitido; acceso remoto; cifrado y recuperación; firewall; auditoría y hora; copia y restauración; protección endpoint y estado del agente; secretos; configuración del navegador y de red. Documentar no aplicable y no comprobado en vez de convertirlos en aprobados.

Una puntuación de hardening no es una certificación. Wazuh SCA es un ejemplo abierto de comprobación de configuración; sus resultados dependen de la política, permisos y plataforma. Un resultado favorable de una comprobación no valida todo el host. [Wazuh: Security Configuration Assessment](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/index.html).

No cambiar simultáneamente autenticación, firewall y acceso remoto sin consola de recuperación. Custodiar la clave de recuperación antes de activar cifrado. No desactivar SIP, Gatekeeper, Defender, SELinux o logging para completar un ejercicio.

## 7. Consultas iniciales de laboratorio

Son ejemplos de lectura, no un recolector forense sin impacto. Consultar ayuda local y permisos; las salidas pueden contener datos personales. No ejecutar todas las herramientas si el módulo o sistema no las admite.

```bash
# Linux: contexto y estado acotados
id
uname -s
getent passwd "$(id -un)"
systemctl --failed
```

```powershell
# Windows: motor, identidad y grupo administrativo por SID, no nombre traducido
$PSVersionTable.PSVersion
whoami /user
Get-LocalGroup -SID 'S-1-5-32-544' | Get-LocalGroupMember
gpresult /r
```

```sh
# macOS: sistema, identidad y estado de inscripción
sw_vers
id
profiles status -type enrollment
```

Éxito: explicar el origen de la información y una limitación. Acceso denegado o cmdlet ausente se registra como resultado, no como ausencia del control. En equipos no Windows, PowerShell no incorpora mágicamente las APIs LocalAccounts o GPO.

## 8. Autoevaluación y evidencia

Caso: una persona dada de baja ayer abre hoy una sesión offline y sigue leyendo una copia local. ¿Es prueba de que el directorio ignoró la baja? No: separar autenticación almacenada, datos ya disponibles, sesión/ticket y revocación online. Diseñar la prueba de reconexión y el tratamiento del dispositivo, sin borrar datos necesarios.

Entregable: matriz identidad–rol–recurso–acción, informe de política efectiva y acta de alta/cambio/baja con controles positivos/negativos. El alumno debe poder justificar cada permiso y mostrar cómo retira uno sin interrumpir administración legítima. Los doce diseños de verificación están en D25.
