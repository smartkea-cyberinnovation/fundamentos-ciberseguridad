# Bastionado basado en evidencia y reversibilidad

Objetivo: reducir superficie y privilegios sin destruir disponibilidad ni capacidad de investigación. Utilizar benchmarks del producto y versión elegidos, junto con documentación del fabricante [S07, S13](FUENTES.md). No se incluye un script universal que aplique todos los controles ni se afirma conformidad CIS por completar esta lista.

## Procedimiento

**1. Descubrir.** Identificar activo, propósito, datos, dependencias, versión, usuarios, servicios, puertos, backups y acceso de recuperación. Obtener estado actual sin modificarlo.

**2. Seleccionar.** Elegir baseline aplicable y justificar perfil. Separar requisito, recomendación, control no aplicable y control no comprobable. Documentar diferencias entre estación, servidor y máquina docente.

**3. Planificar.** Priorizar identidad, exposición, actualización, copias y registro. Para cada cambio: impacto, aprobación, copia, prueba de funcionalidad y rollback. No cambiar simultáneamente autenticación, firewall y acceso remoto sin vía de recuperación.

**4. Aplicar.** Primero en clon o snapshot de laboratorio. Un cambio o grupo pequeño por vez. Identidad administrativa solo cuando sea necesaria. No instalar software de origen desconocido para obtener un resultado de auditoría.

**5. Verificar.** Comprobar estado efectivo, no solo archivo configurado. Probar un uso legítimo y una restricción prevista. Confirmar logs y restauración. Registrar errores.

**6. Operar.** Revisar drift, cambios de versión, excepciones y caducidades. Una baseline aprobada no permanece válida indefinidamente.

## Controles transversales

| Control | Evidencia mínima | Riesgo a evitar |
|---|---|---|
| Soporte y actualizaciones | Versión, estado y registro de prueba | Actualización a ciegas o software sin soporte no declarado |
| Inventario de software | Origen, versión y responsable | Dependencias/gestores sin control |
| Cuentas estándar y administrativas separadas | Grupos, permisos efectivos y pruebas | Administrador permanente para todas las tareas |
| Cuentas de servicio mínimas | Identidad, recursos y log | Reutilizar credenciales personales |
| Acceso remoto restringido | Flujos, autenticación, autorización y cierre | Publicación exterior o confianza indiscriminada |
| Puertos/servicios necesarios | Listener, función, propietario y firewall | Confundir instalado con necesario |
| Permisos de datos/configuración | ACL y prueba por identidad | Lectura de secretos o escritura general |
| Protección de secretos | Ubicación y método de acceso, sin valor | Secretos en argumentos, logs, Git o imágenes |
| Cifrado y recuperación | Estado y custodia verificada de recuperación | Bloquear datos sin capacidad de restaurar |
| Auditoría y retención | Evento benigno recibido y política | Pérdida de visibilidad o registros accesibles a todos |
| Copias y restauración | Resultado funcional, tiempo y pérdida | Copia no probada o en mismo punto de fallo |
| Integridad/procedencia de aplicaciones | Canal y verificación aplicable | Eliminar controles para permitir software |
| Hora | Fuente, zona y diferencia observada | Correlación errónea |
| Cambios/excepciones | Responsable, plazo, compensación y retest | Excepciones perpetuas sin revisión |

## Linux

Auditar repositorios de paquetes y servicios; separar usuario de servicio y operador; revisar grupos y sudo de forma acotada; comprobar propietario/permisos de configuración y ejecutables; evaluar ACL y máscara; limitar listeners e ingreso/egreso según función; comprobar SSH y verificación de host; validar gestión de claves y revocación; mantener SELinux/AppArmor cuando estén integrados; revisar timers/cron/units; aplicar restricciones de unidad apropiadas sin romper el servicio; comprobar rotación/retención; revisar montajes y cifrado conforme al uso. Cada opción concreta se valida contra distribución/versión.

No aplicar un fichero de sysctl, lista de paquetes a eliminar o reglas de firewall universales. La necesidad de capacidades, dispositivos, filesystem de escritura o interfaces se determina por servicio. No considerar `systemd-analyze security` ni cualquier puntuación automática como conformidad completa.

## Windows

Comprobar compilación/edición y actualizaciones; revisar grupos locales, cuentas inactivas y delegaciones; comprobar UAC y protección de credenciales disponibles; políticas de dominio con alcance definido; permisos NTFS y recursos compartidos; cuentas de servicio y tareas; estado de protección endpoint y firewall por perfil; limitar RDP/WinRM a vías autorizadas; verificar auditoría y canales relevantes; comprobar BitLocker y recuperación sin exportar claves; evaluar políticas de ejecución de aplicaciones y reducción de superficie según compatibilidad.

No tratar execution policy de PowerShell como frontera de seguridad ni usar bypass global como solución docente. La transcripción y logging de scripts pueden recoger información sensible: deben tener controles de acceso y retención.

## macOS

Revisar actualización y compatibilidad; usuarios administrativos; FileVault y recuperación; integridad de sistema y arranque según hardware; Gatekeeper y procedencia de aplicaciones; TCC y permisos de privacidad; perfiles de gestión autorizados; ítems de inicio, LaunchAgents y LaunchDaemons; servicios de Compartir; firewall y conectividad; firma de aplicaciones; Unified Log y copias/restauración. Diferenciar controles administrados por MDM de preferencias locales.

No desactivar SIP, protección de arranque, Gatekeeper o cuarentena para ejecutar material del curso. No extraer secretos de Keychain como práctica de inventario. La ausencia de acceso total al disco puede ser un resultado correcto del mínimo privilegio.

## Servicio web y contenedores

Cuenta dedicada y directorio mínimo; configuración validada antes de recarga; TLS con confianza correcta; claves privadas fuera del repositorio; permisos de logs; límite de información expuesta; rutas/puertos estrictamente necesarios; datos persistentes claramente separados; backup y health check útiles; versiones fijadas y actualizables; revisión de imagen/origen. En contenedores: usuario no root cuando sea compatible, mínimos permisos/capacidades, filesystem de solo lectura cuando sea viable y rutas temporales declaradas, límites de recursos y ausencia de socket de administración del host.

En Swarm, revisar el modo de publicación de puertos y el alcance del routing mesh; no trasladar sin comprobación la expectativa de bind local de Compose. En Kubernetes, comprobar RBAC y exposición del servicio; codificar un secreto no lo protege por sí solo. [S09]

## Aceptación del cambio

Control marcado «comprobado» solo con evidencia de estado efectivo y prueba. «Configurado, pendiente de comprobar» no es equivalente. Registrar excepciones con caducidad y responsable. El informe debe separar riesgo residual, controles no evaluados y funciones que quedaron fuera del laboratorio.
