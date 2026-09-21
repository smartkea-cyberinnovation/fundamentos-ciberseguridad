# Detección, matrices de control y laboratorios de aceptación

**D25 · Edición docente ES/EN · 21 de septiembre de 2026.** Completa [D22](#/recurso/D22), [D23](#/recurso/D23) y [D24](#/recurso/D24), especialmente M19, M23, M27, M28 y M29. Esta ampliación reúne controles verificables; no instala sensores ni impone restricciones reales a los lectores.

## 1. De un control configurado a uno demostrado

Inventariar qué se protege, con qué configuración y qué evidencias prueban su operación. Distinguir política aprobada, configuración distribuida, estado efectivo, observación reciente y resultado de prueba. El estado «sin datos» no es verde. Una excepción aceptada tampoco equivale a control efectivo.

| ID | Control | Prueba positiva y negativa | Responsable operativo |
|---|---|---|---|
| OS-01 | Inventario y propietario | Equipo conocido aparece; equipo sin agente queda explícitamente sin cobertura | Sistemas |
| OS-02 | Soporte y actualización | Versión aprobada y servicio funcional; versión fuera de baseline genera hallazgo | Sistemas |
| OS-03 | Cuentas y privilegios | Usuario estándar opera lo permitido; no administra un recurso ajeno | IAM/sistemas |
| OS-04 | Alta, cambio y baja | Nuevo acceso correcto; derecho anterior retirado y sesiones revisadas | IAM/propietario |
| OS-05 | Directorio y autenticación | Resolución/autenticación correctas; fallo documentado sin degradar validación | IAM |
| OS-06 | Caché y acceso offline | Caso admitido dentro de política; límite de revocación medido y declarado | IAM/sistemas |
| OS-07 | Perfiles compartidos | Entorno propio disponible; usuario B no hereda sesión/documentos de A | Puesto de trabajo |
| OS-08 | ACL y shares | Lector lee/editor edita; invitado y cambio de ACL denegados | Dueño de datos |
| OS-09 | Segmentación y firewall | Flujo aprobado funciona; origen no aprobado no llega al servicio | Redes/sistemas |
| OS-10 | Navegación identificada | Grupo admitido llega; no admitido recibe decisión de la regla prevista | Redes/IAM |
| OS-11 | Cuentas SaaS | Tenant aprobado funciona; personal/no aprobado bloqueado donde se soporta | IAM/aplicaciones |
| OS-12 | TLS y privacidad | Canario inspeccionado; servidor inválido rechazado y exclusiones limitadas | Redes/privacidad |
| OS-13 | Sensor y telemetría | Evento benigno recibido; pérdida de heartbeat genera falta de cobertura | SOC/sistemas |
| OS-14 | Detección y triaje | Caso preparado detectado; actividad esperada no se declara incidente sin contexto | SOC |
| OS-15 | Respuesta y contención | Acción autorizada reduce impacto y mantiene recuperación | CSIRT/sistemas |
| OS-16 | Restauración y revisión | Datos/ACL/servicio restaurados; permisos retirados no reaparecen | Sistemas/datos |

Formato de evidencia: control, activo ficticio, versión, identidad de prueba, hora/zona, configuración antes/después, fuente, resultado, límite, aprobador y recuperación. Guardar solo lo necesario. No subir conversaciones, credenciales, exportaciones completas de perfiles o informes corporativos reales a Git.

## 2. Detección de amenazas en sistemas operativos

Separar evento, registro, alerta e incidente. La primera pregunta del analista es si el dato fue observado y con qué cobertura. La segunda es si hay una hipótesis razonable de comportamiento no autorizado. Un nombre de proceso, IP o hash aislado no permite atribuir por sí solo un ataque a una persona.

Fuentes: autenticación y cambios de grupos; uso administrativo; servicios/tareas/autoinicio; creación/ejecución de procesos; acceso a recursos compartidos; cambios de firewall/DNS/proxy; estado del sensor; logs de aplicación y egress. No todas se generan de forma predeterminada: documentar política, proveedor/canal, versión y retención.

En Windows, Event Log y Sysmon aportan fuentes diferentes; Sysmon no es un SIEM ni equivale a prevención por sí solo. En Linux, journal/syslog/audit y telemetría endpoint dependen del despliegue. En macOS, Unified Log y eventos accesibles al agente pueden estar restringidos o redactados. [Microsoft: Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon).

Diseñar detecciones con datos sintéticos: un alta administrativa fuera del ticket; creación de tarea no inventariada; cambio de proxy; ejecución desde una ubicación inesperada; acceso denegado repetido a un share; subida bloqueada por política; desaparición de un sensor. Corroborar con identidad, dispositivo, padre/procedencia cuando exista, ticket, tiempo y segundo origen.

No necesita malware real: una tarea legítima etiquetada para el laboratorio genera un evento útil para evaluar cobertura. Una alerta de pérdida de sensor se prueba mediante fixture o una ventana de mantenimiento autorizada; no mediante evasión del agente.

## 3. Triaje, contención y recuperación

Triage: validar fuente y reloj; delimitar activo/usuario/servicio; identificar impacto y actividad aún en curso; formular hipótesis alternativas; priorizar; registrar decisión de escalar o cerrar. Distinguir falso positivo de actividad real pero autorizada y de caso sin evidencia suficiente.

Contención: elegir aislamiento del equipo, revocación de acceso, restricción de un flujo o parada de servicio conforme al impacto y autoridad. Conservar vías de administración y recuperación. Una acción EDR puede interrumpir recopilación o servicios; documentar por qué el beneficio supera el efecto.

Preservación: originales protegidos, copias de trabajo, hashes y bitácora; leer un host vivo puede alterar estado y generar eventos. No limpiar logs ni eliminar perfiles antes de decidir conservación. Recuperar desde una fuente conocida, verificar funcionalidad y permisos, vigilar recurrencia y cerrar con mejora de controles. [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

## 4. Doce diseños de laboratorio verificables

Son escenarios complementarios, no doce laboratorios nativos ya ejecutados ni horas adicionales. El docente debe probar versiones y recursos antes de impartir. Todos usan datos ficticios, equipos asignados, alcance aprobado y una vía de recuperación.

### OPS-L01 · Inventario y baseline

Objetivo: separar cobertura y conformidad. Entorno: una VM y ficha de baseline. Tareas: obtener versión, identidad, servicios definidos, estado de firewall y sensor; comparar GUI/CLI; marcar dato ausente. Evidencia: inventario mínimo y dos discrepancias explicadas. Éxito: desconocido no se convierte en aprobado. Recuperación: sin cambios; retirar informes de ensayo según retención.

### OPS-L02 · Alta, cambio y baja

Objetivo: verificar ciclo de vida. Entorno: directorio aislado y cuentas ficticias. Tareas: alta por grupo; prueba permitida/denegada; cambio de rol retirando privilegio anterior; baja y revisión de sesión nueva/existente. Evidencia: matriz y hora efectiva. Éxito: ninguna aprobación depende de usar administrador global. Recuperación: retirar cuentas temporales conservando la evidencia y los datos previstos.

### OPS-L03 · Identidad y caché offline

Objetivo: entender límites de revocación. Entorno: cliente de laboratorio con política de caché conocida. Tareas: registrar acceso online; probar desconexión preparada por el docente; observar caso de baja y reconexión; no alterar el directorio real. Evidencia: secuencia y ventanas. Éxito: diferenciar cuenta, ticket, caché y archivo local. Recuperación: restaurar conectividad y snapshot solo después de guardar resultados.

### OPS-L04 · Perfiles compartidos

Objetivo: separar configuración y datos personales. Entorno: dos usuarios ficticios y navegador sin cuentas reales. Tareas: crear documento/preferencia de prueba; cerrar; iniciar otro usuario; probar aislamiento; contrastar perfil OS y de navegador. Evidencia: tabla de persistencia y acceso. Éxito: B no hereda sesión ni datos de A. Recuperación: retirar perfiles ficticios mediante procedimiento documentado, nunca borrado global.

### OPS-L05 · Permisos de share y filesystem

Objetivo: comprobar cada capa. Entorno: carpeta sintética, lector/editor/invitado. Tareas: registrar ACL; probar lectura/escritura/cambio de permisos por acceso local y remoto; comparar una copia restaurada. Evidencia: matriz y logs del servidor. Éxito: la denegación se atribuye a la capa observada. Recuperación: restaurar ACL inicial y retirar share del ejercicio.

### OPS-L06 · Segmentación

Objetivo: verificar origen permitido/denegado. Entorno: dos clientes de laboratorio y un servicio de prueba. Tareas: documentar ruta/listener/regla; probar solo ese destino/puerto desde ambos; revisar IPv4/IPv6 y retorno. Evidencia: matriz de flujos y resultado. Éxito: gestión conservada y servicio solo accesible donde procede. Recuperación: regla de ensayo retirada desde consola disponible.

### OPS-L07 · DNS y proxy

Objetivo: no confundir capas. Entorno: nombres `.test` y gateway de ensayo. Tareas: comparar resolución, conexión y respuesta web; aplicar una política sintética; observar identidad y regla; distinguir proxy de navegador y WinHTTP cuando proceda. Evidencia: pruebas positivas/negativas. Éxito: no interpretar NXDOMAIN como evidencia de inspección HTTP. Recuperación: configuración inicial restaurada.

### OPS-L08 · Cuentas SaaS

Objetivo: evaluar política de cuenta/tenant, no solo dominio. Entorno: tenant y cuentas de ensayo autorizados o fixtures explícitamente offline. Tareas: probar cuenta propia, externa aprobada y no aprobada; cliente web/nativo y sesión anterior; documentar límites. Evidencia: matriz con método nativo o simulado identificado. Éxito: correo legítimo conservado. Recuperación: revocar sesiones de prueba y retirar asignaciones temporales.

### OPS-L09 · Mensajería y salida de archivos

Objetivo: comprobar el alcance declarado. Entorno: política de aula simulada y archivo sin datos reales. Tareas: distinguir bloqueo de aplicación, dominio y carga; caso permitido de soporte y caso denegado; analizar metadatos sintéticos. Evidencia: tabla de cobertura. Éxito: no afirmar lectura de E2EE ni control de móviles fuera del perímetro. Recuperación: retirar excepción temporal y confirmar caducidad.

### OPS-L10 · TLS canario

Objetivo: validar confianza y límites. Entorno: VM administrada, CA y servidor propios de laboratorio, sin uso de cuentas personales. Tareas: aprobar alcance; verificar canal sin inspección; aplicar perfil de ensayo; comprobar certificado del inspector y rechazo de certificado de servidor inválido; probar exclusión limitada. Evidencia: propiedades públicas de certificados y decisión, sin claves privadas. Éxito: no desactivar validación. Recuperación: retirar CA/perfil de ensayo de los almacenes donde se instalaron, comprobar acceso normal y conservar seguridad de la CA.

### OPS-L11 · Detección y calidad

Objetivo: comprobar detección y cobertura. Entorno: tarea benigna etiquetada y logs sintéticos de tres SO. Tareas: anticipar evento; observar fuente y colector; correlacionar cambio con ticket; añadir control negativo y hueco de ingestión simulado. Evidencia: regla/consulta, positivos, falsos positivos y tiempo observado. Éxito: un sensor sin datos no figura sano. Recuperación: retirar tarea sin borrar logs del caso.

### OPS-L12 · Incidente y restauración

Objetivo: decidir con evidencia y recuperar. Entorno: caso sintético de cambio de permisos y proxy. Tareas: triaje; preservar; decidir contención; restaurar datos/ACL/política; verificar cuenta legítima y denegada; redactar riesgo residual. Evidencia: cronología, acta y runbook. Éxito: recuperación funcional y conclusiones proporcionales. Recuperación: volver al estado base después de aceptación, no antes de conservar el caso.

## 5. Glosario aplicado y ejemplos de soluciones

Los ejemplos son capacidades documentadas, no compras recomendadas ni equivalencias universales. Registrar producto, edición, licencia, SO y versión antes de seleccionar una práctica. Ninguna instalación se da por realizada aquí.

| Término ES / EN | Uso y contraste | Ejemplos para estudiar |
|---|---|---|
| Directorio / Directory | Identidades y atributos; protocolo no equivale a servicio completo | AD DS, FreeIPA; LDAP como protocolo |
| Cliente de identidad / Identity client | Resolución, autenticación y acceso del host | SSSD/realmd; integración nativa Windows |
| Administración local / Local administrator management | Privilegio del host con recuperación controlada | Windows LAPS; sudo delegado en Linux |
| Perfil de configuración / Configuration profile | Política gestionada, no home del usuario | Perfiles MDM de Apple; CSP/GPO según entorno Windows |
| Recurso compartido / File share | Autenticación, ACL y protocolo | Windows SMB, Samba y NAS compatibles |
| Firma SMB / SMB signing | Integridad, no confidencialidad por sí sola | Implementaciones SMB compatibles de cliente y servidor |
| DNS protector / Protective DNS | Control sobre consultas/nombres, no cuentas de un SaaS | Políticas DNS de Cloudflare Gateway; resolutores de laboratorio |
| Pasarela web / Secure web gateway | Navegación saliente con identidad/visibilidad | Cloudflare Gateway; no confundir con Cloudflare WAF |
| Restricción de tenant / Tenant restriction | Control de cuentas/instancias soportadas | Microsoft Entra tenant restrictions |
| Inspección TLS / TLS inspection | Dos canales con confianza administrada | Gateway con política de descifrado y CA controlada |
| Cifrado extremo a extremo / End-to-end encryption | Protección entre participantes, adicional al transporte | Mensajería WhatsApp; TLS de proxy no la elimina |
| Evaluación de configuración / Security configuration assessment | Estado frente a reglas, no certificación total | Wazuh SCA y políticas seleccionadas |
| Telemetría / Telemetry | Datos con fuente/cobertura/tiempo | Sysmon, journal, Event Log, Unified Log |
| Deriva / Configuration drift | Diferencia respecto del estado aprobado | Inventario versionado y evaluación periódica |
| Excepción / Exception | Desviación con alcance y caducidad | Registro de excepciones del responsable del control |
| DLP / Data loss prevention | Protección de datos en canales soportados | Controles endpoint/SaaS seleccionados tras prueba |

FreeIPA integra capacidades de identidad y políticas orientadas a entornos Linux; no se enseña como clon idéntico de AD DS. [FreeIPA: About](https://www.freeipa.org/page/About). Para perfiles y filtrado Apple, comprobar tipo de inscripción y restricciones del payload. [Apple: Filter content](https://support.apple.com/guide/deployment/filter-content-dep1129ff8d2/web). Wazuh SCA y Sysmon tienen funciones distintas: comprobar configuración no equivale a correlacionar incidentes ni a prevenirlos.

## 6. Métricas y cierre

Usar denominadores explícitos: equipos con telemetría reciente / equipos esperados; controles verificados / controles aplicables; bajas dentro de ventana / bajas evaluadas; excepciones vencidas / excepciones activas; restauraciones correctas / ensayos. Separar no aplicable, no probado y no conforme. No promediar todo en un número que oculte privilegios críticos o falta de evidencia.

Rúbrica sugerida: alcance y modelo 20 %, operación correcta 25 %, seguridad/privacidad 20 %, evidencia 20 %, recuperación y límites 15 %. El instructor aplica requisitos críticos aunque la media sea alta: no actuar fuera de alcance, no interceptar personas sin autorización, no divulgar secretos ni borrar originales. Lectura móvil y simulaciones son útiles, pero se etiquetan por lo que realmente demuestran.
