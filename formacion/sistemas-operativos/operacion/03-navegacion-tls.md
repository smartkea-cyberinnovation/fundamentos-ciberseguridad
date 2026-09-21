# Control de navegación: DNS, firewall, proxy, cuentas y TLS

**D24 · Edición docente ES/EN · 21 de septiembre de 2026.** Profundiza M10, M18, M22, M24 y M25. [Identidades](#/recurso/D22) · [Recursos compartidos](#/recurso/D23) · [Detección y aceptación](#/recurso/D25).

## 1. La regla empieza por la necesidad

«Bloquear correo personal» no especifica todavía una implementación. Hay que decidir usuarios, equipos gestionados, aplicación web o nativa, cuentas corporativas admitidas, uso de invitados, ubicaciones y datos protegidos. No equivale a bloquear todos los servicios de un proveedor, inspeccionar mensajes personales o prohibir cualquier acceso en el teléfono privado.

Contrato de regla: ID, propósito, sujeto/grupo, dispositivo y estado de gestión, red/origen, aplicación/destino, operación, acción, punto de aplicación, precedencia, excepciones, registro mínimo, responsable, expiración y pruebas. Distinguir lo propuesto, configurado, recibido por el cliente, efectivo y verificado. La web docente no aplica estas políticas a los alumnos.

## 2. Capas que no son intercambiables

| Capa | Qué puede decidir según implementación | Límite que debe comprobarse |
|---|---|---|
| DNS protector | Permitir/bloquear resolución de nombres o categorías | No distingue por sí solo ruta URL, cuenta del mismo SaaS ni contenido; considerar caché y resolución efectiva |
| Firewall de host/red | Flujos, aplicaciones o identidades según producto | IP compartida/NAT no identifica de forma fiable a cada persona; permitir 443 no equivale a autorización web |
| Proxy explícito/PAC | Encaminamiento de solicitudes de clientes compatibles | Configurar PAC no fuerza por sí solo a toda aplicación a utilizarlo |
| Secure Web Gateway | Políticas de navegación y aplicaciones con el tráfico que realmente recibe | Depende de identidad, cliente, transporte, visibilidad y edición |
| Navegador gestionado | Políticas, perfiles, extensiones, cuentas y restricciones admitidas | No controla necesariamente otros navegadores o aplicaciones nativas |
| IdP/tenant/app | Identidad, tenant, sesión y operaciones propias de la aplicación | El IdP corporativo no controla todos los servicios personales ajenos |
| DLP | Uso o salida de datos clasificados en canales soportados | No cubre todos los formatos/aplicaciones ni convierte TLS en lectura de E2EE |
| WAF | Solicitudes hacia una aplicación publicada | No es el proxy de navegación saliente de los usuarios |

No existe una precedencia universal para toda esta tabla. Documentar cómo combina reglas el producto y cómo se combinan capas independientes. Un permiso del firewall no anula la denegación de una aplicación; una excepción a inspección no debe convertirse accidentalmente en una autorización general.

## 3. Identificar al usuario y el dispositivo

En proxy o gateway, relacionar autenticación, grupo y dispositivo con la conexión. Probar dos usuarios sucesivos en el mismo equipo y dos equipos detrás del mismo NAT. No atribuir automáticamente todo el tráfico de la IP al último usuario conectado. Contemplar tráfico de sistema sin sesión y servicios con otra identidad.

Clasificar equipos: gestionados de aula/empresa; gestionados remotos; servidores; BYOD; invitados. En equipos propios no gestionados, preferir segmentación y controles de acceso al recurso antes que instalar una CA interceptora. Una regla de la Wi-Fi institucional no controla la conexión móvil particular fuera de esa red. La limitación debe aparecer en el informe, no ocultarse con un porcentaje de cumplimiento.

Revisar DNS efectivo, proxy, rutas del cliente, VPN administrada, IPv6, DoH/DoT, QUIC/HTTP3 y extensiones autorizadas. Estos transportes no son malware por naturaleza. El administrador define cómo se soportan en su entorno; no se enseñan instrucciones para eludir los controles. Comprobar capacidad real por versión en lugar de afirmar que todo QUIC es imposible de inspeccionar. [Cloudflare: HTTP/3 inspection](https://developers.cloudflare.com/cloudflare-one/traffic-policies/http-policies/http3/).

## 4. Correo corporativo frente a correo personal

Permitir un dominio compartido puede permitir más de una identidad. Bloquearlo puede inutilizar el correo corporativo, colaboradores o funciones del dispositivo. Microsoft documenta este problema y los efectos colaterales de bloquear indiscriminadamente `login.live.com`. [Microsoft: tenant restrictions](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/tenant-restrictions).

Diseñar restricciones de tenant/cuenta, configuración de aplicaciones y navegador gestionado para los servicios que lo admitan. Revisar la generación vigente de tenant restrictions y sus clientes, licencias y limitaciones: no copiar una cabecera histórica y afirmar que controla toda aplicación. [Microsoft: tenant restrictions v2](https://learn.microsoft.com/en-us/entra/external-id/tenant-restrictions-v2).

Para cada servicio probar: cuenta del tenant propio, tenant externo aprobado, tenant no aprobado, cuenta personal de ensayo, sesión anterior y cliente nativo. Si un flujo no es soportado, documentar la brecha y decidir otro control o prohibir ese cliente en equipos gestionados. Usar identidades ficticias de laboratorio; no solicitar credenciales personales de alumnos.

Separar bloqueo del servicio y protección de datos. Puede permitirse un navegador para uso limitado mientras se restringen carga de archivos, sincronización o cuentas externas mediante controles soportados. No afirmar que un proxy distingue cualquier tenant solo por ver el nombre del dominio.

## 5. WhatsApp y otras aplicaciones de mensajería

Definir primero si se pretende bloquear el servicio, permitirlo solo a un equipo de soporte, impedir transferencia de archivos corporativos o limitar notificaciones en una actividad. Son objetivos distintos. Distinguir navegador, aplicación nativa y dispositivo personal; probar cada superficie declarada.

Para bloquear en equipos administrados, combinar control de aplicaciones, política del gateway y gestión del cliente según capacidades. Una lista de dominios es un dato mantenido, no una solución eterna; no bloquear indiscriminadamente toda la infraestructura compartida del fabricante. Una excepción debe limitar grupo, dispositivo, finalidad y periodo, con revisión.

La inspección TLS no elimina el cifrado de extremo a extremo de los mensajes de WhatsApp. Un gateway puede observar o controlar parte del transporte y metadatos disponibles; no debe prometer texto de conversaciones cifradas entre participantes. [WhatsApp: protección de conversaciones](https://blog.whatsapp.com/introducing-advanced-chat-privacy).

Una política DLP se valida con un archivo sintético y un canal admitido. No inspeccionar conversaciones privadas ni instalar software encubierto para demostrar eficacia. Si no se puede observar el contenido de forma legítima y técnicamente soportada, registrar el límite y elegir control de acceso o de aplicación.

## 6. TLS inspection: diseño de confianza, no desactivar seguridad

Usar el término TLS, aunque una consola comercial conserve «SSL inspection». Una inspección autorizada establece conexiones separadas cliente–inspector y inspector–destino. Necesita confianza correctamente distribuida, protección de la CA y validación del servidor remoto. No corregir un error con `--insecure`, aceptación ciega de certificados o desactivación global de validación.

Ciclo de vida: autorización y alcance → piloto en equipos gestionados → distribución de CA en los almacenes pertinentes → política de inspección → comprobación con sitio canario → excepciones justificadas → monitorización → rotación y retirada. Inventariar qué apps usan el almacén del sistema y cuáles mantienen confianza propia.

Probar certificate pinning, mTLS, ECH, protocolos soportados y comportamiento de actualización; no prometer inspección universal. Un flujo excluido de descifrado debe mantener la autorización, registro proporcional y controles que sí sean posibles. Las limitaciones y requisitos del gateway son específicos del producto. [Cloudflare: TLS decryption](https://developers.cloudflare.com/cloudflare-one/traffic-policies/http-policies/tls-decryption/).

Diseñar dos verificaciones diferentes: el certificado presentado por el inspector es confiado por el cliente autorizado; un certificado inválido del servidor de laboratorio continúa siendo rechazado. El proxy no debe esconder una pérdida de validación aguas arriba.

No descifrar por defecto servicios sensibles o tráfico BYOD. Documentar base jurídica, finalidad, necesidad, proporcionalidad, información a las personas, acceso a logs, conservación, excepciones y evaluación de impacto cuando corresponda. En España, el artículo 87 LOPDGDD regula garantías laborales específicas; no trasladarlo automáticamente a alumnado o dispositivos privados. Esta lección no acredita cumplimiento legal. [BOE: LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673#a87).

## 7. Política de ejemplo: aula gestionada

Plantilla docente ficticia, no una política aplicada en SmartKEA ni en una institución. El propietario del servicio y los responsables de privacidad deben adaptar y aprobar su uso real.

| ID | Sujeto y objetivo | Acción diseñada | Evidencia esperada |
|---|---|---|---|
| NAV-01 | Equipo administrado, servicios del curso | Permitir campus y dependencias aprobadas | Lectura, recursos y descargas funcionan |
| NAV-02 | Equipo administrado, correo | Permitir cuentas/tenants aprobados mediante capacidad soportada | Cuenta de ensayo admitida y cuenta no aprobada rechazada |
| NAV-03 | Equipo administrado, correo personal | Bloquear uso fuera de la política declarada | Prueba web y nativa; registrar canales no cubiertos |
| NAV-04 | Mensajería en aula gestionada | Bloquear salvo excepción de soporte limitada | Servicio bloqueado y excepción con caducidad comprobada |
| NAV-05 | Navegación general | Categorías permitidas y restricciones por riesgo/finalidad | Usuario/grupo y regla efectiva correlacionados |
| NAV-06 | TLS en piloto administrado | Inspeccionar únicamente alcance aprobado | Sitio canario, confianza y rechazo de certificado inválido |
| NAV-07 | BYOD/invitados | Red separada, acceso mínimo a recursos, sin CA invasiva por defecto | No acceso a SMB/gestión; campus accesible |
| NAV-08 | Tráfico de sistema | Mantener gestión, updates, DNS, hora y PKI necesarios | Recuperación y actualización siguen funcionando |

## 8. Despliegue, excepciones y autoevaluación

Primero modo de observación con datos minimizados, después piloto y luego anillos de implantación. Registrar falsos positivos, latencia, tickets de soporte, aplicaciones afectadas y prueba de reversión. Si el agente/gateway falla, definir por tipo de servicio una decisión de continuidad; ni fail-open ni fail-closed son universalmente correctos.

Toda excepción necesita ID, solicitante, aprobador, motivo, activo, regla, compensación, vencimiento y prueba de retirada. Evitar comodines permanentes creados por urgencias. Revisión después de cambios del SaaS, navegador, OS, cliente de red o certificados.

Autoevaluación: «bloqueé un dominio y nadie abrió WhatsApp Web; por tanto, WhatsApp está bloqueado en todos los teléfonos y puedo leer sus mensajes». La conclusión no está soportada: faltan clientes nativos, otros caminos de red y alcance de dispositivos; además, TLS y E2EE son capas diferentes. Entregar una afirmación limitada a pruebas y cobertura observadas.
