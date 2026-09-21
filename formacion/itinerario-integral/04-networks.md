<!-- ES -->
# Redes: capas, equipos, movilidad y controles verificables

**Lectura D29.** Conecta [hardware](#/recurso/D28), M10/M18/M22/M24 y [control de navegación](#/recurso/D24). Referencias N01–N05 y T01 en [D36](#/recurso/D36). Las actividades se realizan únicamente en redes asignadas.

## 1. Qué problema resuelve una red

Una red permite intercambiar información bajo acuerdos sobre señal, direccionamiento, transporte y aplicación. LAN y WAN describen alcance/organización, no niveles automáticos de seguridad. Una red «interna» puede contener dispositivos no confiables; una conexión cifrada puede transportar una operación no autorizada.

Separa topología física y lógica, enlace y ruta, dirección y nombre, dispositivo y persona. Una IP puede cambiar o compartirse. La MAC no sustituye una identidad fuerte. Dibuja origen, destino, protocolo, propósito, dueño y evidencia antes de configurar una regla.

## 2. Capas: mapa mental y no encaje forzado

| OSI, como modelo docente | Ejemplo y pregunta | Observación/seguridad |
|---|---|---|
| 1 Física | Cobre, fibra, radio, potencia y conectores | Enlace, errores, interferencia, acceso físico |
| 2 Enlace | Ethernet, Wi-Fi, tramas, VLAN | Aprendizaje MAC, bucles, admisión, segmentación |
| 3 Red | IP, subred, router, siguiente salto | Rutas, ACL, límites y retorno |
| 4 Transporte | TCP, UDP, puertos | Estado, pérdida, latencia y firewall |
| 5 Sesión | Continuidad de diálogo | Estado y renovación; no toda aplicación separa esta capa |
| 6 Presentación | Formatos y representación | Codificaciones; no confundir formato con seguridad |
| 7 Aplicación | HTTP, DNS y protocolos de servicio | Identidad, autorización, validación y logs |

El modelo TCP/IP agrupa funciones de otra forma. TLS y QUIC no deben colocarse en una casilla a costa de ocultar su comportamiento. QUIC es un transporte multiplexado sobre UDP con mecanismos de seguridad; HTTP/3 lo utiliza. UDP no significa «sin seguridad» y TCP no aporta por sí solo cifrado [N01–N02].

## 3. Equipos y funciones que debes reconocer

| Familia | Función | Administración y seguridad a comprobar |
|---|---|---|
| Repetidor/hub, puente | Regeneración o reenvío según tecnología | Alcance, exposición compartida; equipos históricos no equivalen a switches modernos |
| Switch L2/L3 | Conmuta tramas y, en modelos L3, enruta | VLAN, bucles, administración, ACL y actualizaciones |
| Router/gateway | Interconecta redes; gateway puede designar varias funciones | Rutas, retorno, filtros, gestión y redundancia |
| Módem/ONT/OLT | Acceso según tecnología del operador | Responsabilidad del operador, firmware y acceso de gestión |
| AP/controlador Wi-Fi | Acceso radio y coordinación | SSID, autenticación, cifrado, invitados, RF y updates |
| Estación base/RAN y núcleo móvil | Acceso y servicios celulares | Operador, identidad de abonado, segmentación y cobertura |
| NIC/SFP/cableado/patch panel | Conectividad física/lógica | Compatibilidad, inventario, enlaces y manipulación física |
| Balanceador/CDN/proxy inverso | Entrega y distribución de solicitudes | Certificados, salud, cabeceras y caché |
| Firewall/VPN/SWG | Política de flujo y acceso | Regla efectiva, identidad, rutas y excepciones |
| IDS/IPS/NDR | Detección y, según modo, intervención | Cobertura, colocación, carga y falsos positivos |
| TAP/SPAN/packet broker | Copia y distribución de tráfico a sensores | Pérdidas, acceso a capturas y confidencialidad |
| WAF/WAAP | Políticas sobre web/API | Ubicación, reglas, endpoints y pruebas de negocio |
| DNS/DHCP/NTP/RADIUS | Servicios de soporte, físicos o virtuales | Integridad, disponibilidad, autorizaciones y logs |
| KVM/consola/BMC | Administración del hardware | Red separada, MFA donde exista y recuperación |

Es una taxonomía de funciones ampliable, no una lista de todos los modelos fabricados. Muchos appliances combinan funciones; las virtualizaciones y servicios cloud cambian la forma de entrega, no eliminan las preguntas de operación.

## 4. Arquitecturas: del aula a la empresa

Una red pequeña puede combinar AP, router y firewall. Una empresa separa usuarios, servidores, gestión, invitados, IoT/OT y accesos remotos según necesidades. Un centro de datos puede utilizar topologías leaf-spine y automatización; una sucursal puede acceder por WAN, SD-WAN o servicios cloud. No se impone una topología empresarial a un laboratorio de dos máquinas.

Para cada diseño declara dominios de broadcast, prefijos, rutas, DNS, puntos de inspección y dependencia de identidad. Documenta alta disponibilidad y camino de retorno. El plano de administración no se publica en Internet. Un fallo de DNS/NTP puede afectar autenticación aunque los enlaces físicos estén operativos.

## 5. Wi-Fi 6, 6E y 7

Wi-Fi 6 se relaciona con 802.11ax; 6E extiende el uso a 6 GHz donde esté permitido. Wi-Fi 7 se relaciona con 802.11be y capacidades como multi-link; la norma IEEE 802.11be-2024 identifica su edición [N03–N04]. No confundas «6» con banda de 6 GHz ni con «6G» celular.

La experiencia depende de cliente, AP, firmware, sistema operativo, espectro permitido, canal, interferencia, densidad y backhaul. Una tasa física anunciada no es una descarga sostenida. Seguridad: autenticación empresarial cuando proceda, certificados, separación de invitados, configuración compatible de WPA, gestión de claves, detección de AP no autorizado y actualización. No se enseña captura de credenciales ni intrusión radio.

## 6. 5G y la dirección de 6G

Distingue acceso radio y núcleo, despliegues autónomos/no autónomos, abonado, servicio y aplicaciones. No existe una equivalencia «generación más alta = autorización más fuerte». La seguridad del terminal, identidad, aplicaciones y datos sigue siendo necesaria.

A 21-09-2026, ITU describe IMT-2030/6G mediante un proceso de requisitos y normalización; la publicación de marzo de 2026 trata requisitos técnicos en borrador [N05]. Presenta objetivos como objetivos, no redes 6G comerciales universalmente operativas ni fechas garantizadas. Las propuestas de investigación deben incluir medida, condiciones y fuente.

## 7. Diagnóstico y seguridad por capas

Utiliza GUI/CLI nativas: estado de interfaz, IP/prefijo, ruta, DNS, puerto y aplicación. Linux: `ip`, `ss`, resolución del sistema; Windows: `Get-NetIPConfiguration`, `Resolve-DnsName`, `Test-NetConnection` sobre destino asignado; macOS: `networksetup`, `scutil`, `route`, `lsof`. Comprueba ayuda local y permisos.

Una captura solo cubre su punto de observación. TLS limita contenido visible; DNS cifrado, QUIC, ECH, CDN y aplicaciones con E2EE cambian capacidades de inspección. No diseñes controles basados en poder leer siempre SNI, URL completa o contenido. Verifica lo que el producto realmente observa y respeta la privacidad. [Políticas de navegación y TLS](#/recurso/D24).

## Prácticas y criterios

**INT-L07: mapa de red del servicio.** En el laboratorio asignado dibuja cliente, DNS, router/firewall y servidor. Especifica un flujo permitido y otro denegado, con origen/destino/puerto/propósito. Evidencia: diagrama y comprobaciones desde el host. Éxito: separar «no resuelve», «no enruta», «no conecta» y «no autoriza». No escanear redes ajenas.

**INT-L08: capacidad radio y seguridad.** Con métricas preparadas, compara dos aulas: una tiene tasa física alta y backhaul saturado; otra, interferencia. Propón mediciones y cambios mínimos. Incluye aislamiento de invitados y vía de recuperación. Éxito: no inferir causa solo del número Wi-Fi del AP. La configuración real requiere autorización y copia previa.

Autoevaluación: ¿un switch L3 es siempre más seguro que uno L2? No; depende de función, configuración, actualización y control de administración. ¿Una inspección TLS ve el contenido de cualquier mensajería? No; la protección de extremo a extremo puede existir por encima del transporte.
<!-- EN -->
# Networks: layers, equipment, mobility and verifiable controls

**Reading D29.** Connects [hardware](#/recurso/D28), M10/M18/M22/M24 and [browsing controls](#/recurso/D24). References N01–N05/T01 are in [D36](#/recurso/D36). Work only on assigned networks.

## 1. The problem a network solves

Networks exchange information using agreements about signals, addressing, transport and applications. LAN/WAN describe scope or organization, not automatic security levels. An internal network can contain untrusted devices; an encrypted connection can carry unauthorized actions.

Separate physical/logical topology, link/route, address/name and device/person. IP addresses can change or be shared. A MAC address is not strong identity. Define source, destination, protocol, purpose, owner and evidence before adding a rule.

## 2. Layers are a model, not a forced fit

| OSI teaching layer | Example/question | Observation/security |
|---|---|---|
| 1 Physical | Copper, fibre, radio, power and connectors | Link, errors, interference and physical access |
| 2 Data link | Ethernet, Wi-Fi, frames and VLANs | MAC learning, loops, admission and segmentation |
| 3 Network | IP, subnets, routers and next hops | Routing, ACLs, boundaries and return paths |
| 4 Transport | TCP, UDP and ports | State, loss, latency and firewall |
| 5 Session | Dialogue continuity | State/renewal; applications may not isolate this layer |
| 6 Presentation | Formats and representation | Encoding is not security |
| 7 Application | HTTP, DNS and service protocols | Identity, authorization, validation and logs |

TCP/IP groups functions differently. Do not force TLS/QUIC into boxes that hide their behavior. QUIC is a secure multiplexed transport over UDP, used by HTTP/3. UDP does not mean insecure, and TCP does not itself encrypt [N01–N02].

## 3. Equipment and functions to recognize

| Family | Purpose | Management/security questions |
|---|---|---|
| Repeater/hub/bridge | Regeneration or forwarding | Shared exposure and scope; historical equipment is not a modern switch |
| L2/L3 switch | Switches frames and, for L3 models, routes | VLANs, loops, administration, ACLs and updates |
| Router/gateway | Interconnects networks; gateway has several meanings | Routes, return path, filtering and redundancy |
| Modem/ONT/OLT | Provider access technology | Provider responsibility, firmware and management |
| Wi-Fi AP/controller | Radio access and coordination | SSID, authentication, encryption, guests, RF and updates |
| Base station/RAN/mobile core | Cellular access and services | Operator, subscriber identity, segmentation and coverage |
| NIC/SFP/cabling/patch panel | Physical/logical connectivity | Compatibility, inventory, link health and tampering |
| Load balancer/CDN/reverse proxy | Request delivery/distribution | Certificates, health, headers and caching |
| Firewall/VPN/SWG | Flow/access policy | Effective rule, identity, routes and exceptions |
| IDS/IPS/NDR | Detection and mode-dependent intervention | Coverage, placement, load and false positives |
| TAP/SPAN/packet broker | Copies/distributes traffic to sensors | Loss, capture access and confidentiality |
| WAF/WAAP | Web/API policies | Placement, rules, endpoints and business tests |
| DNS/DHCP/NTP/RADIUS | Physical or virtual support services | Integrity, availability, authorization and logging |
| KVM/console/BMC | Hardware administration | Separate network, supported MFA and recovery |

This is an extensible functional taxonomy, not every manufactured model. Appliances may combine roles; virtual/cloud delivery does not remove operational questions.

## 4. Architectures from classroom to enterprise

A small network may combine AP, router and firewall. Enterprises separate users, servers, management, guests, IoT/OT and remote access according to needs. Data centers may use leaf-spine and automation; branches may use WAN, SD-WAN or cloud services. Do not impose an enterprise topology on a two-VM exercise.

Declare broadcast domains, prefixes, routes, DNS, inspection points and identity dependencies. Document availability and return traffic. Keep administration off the public Internet. DNS/NTP failures can affect authentication even when physical links work.

## 5. Wi-Fi 6, 6E and 7

Wi-Fi 6 relates to 802.11ax; 6E extends use to 6 GHz where permitted. Wi-Fi 7 relates to 802.11be and capabilities such as multi-link; IEEE 802.11be-2024 identifies the standard edition [N03–N04]. Do not confuse the number 6 with the 6 GHz band or cellular 6G.

Experience depends on client, AP, firmware, OS, permitted spectrum, channel, interference, density and backhaul. Advertised physical rate is not sustained file throughput. Examine suitable enterprise authentication, certificates, guest separation, compatible WPA configuration, key management, unauthorized AP detection and updates. No credential interception or radio intrusion exercises.

## 6. 5G and the direction of 6G

Separate radio/core, standalone/non-standalone deployment, subscriber, service and application. A higher generation does not guarantee stronger authorization. Device, identity, application and data security remain necessary.

As reviewed on 2026-09-21, ITU describes IMT-2030/6G through requirements and standardization; the March 2026 publication concerns draft technical requirements [N05]. Goals are not universally deployed commercial networks or guaranteed delivery dates. Research claims need measurements, conditions and sources.

## 7. Layered diagnosis and security

Use native GUI/CLI to examine interface, IP/prefix, route, DNS, port and application. Linux: `ip`, `ss` and system resolution; Windows: `Get-NetIPConfiguration`, `Resolve-DnsName`, `Test-NetConnection` to assigned destinations; macOS: `networksetup`, `scutil`, `route`, `lsof`. Check local help and permissions.

Captures cover their observation points. TLS limits content visibility; encrypted DNS, QUIC, ECH, CDNs and end-to-end encrypted applications change inspection capabilities. Do not assume controls always see SNI, full URLs or payloads. Verify actual product visibility and privacy boundaries. See [browsing and TLS policies](#/recurso/D24).

## Exercises and criteria

**INT-L07: service network map.** Draw the assigned client, DNS, router/firewall and server. Specify an allowed and a denied flow with source/destination/port/purpose. Evidence: diagram and host checks. Success: distinguish name-resolution, routing, transport and authorization failures. No external scanning.

**INT-L08: radio capacity and security.** Use prepared metrics for two classrooms: one has a high PHY rate with saturated backhaul; the other has interference. Propose measurements and minimal changes, including guest isolation and recovery. Success: do not infer root cause from the AP's Wi-Fi generation alone. Real changes require authorization and a prior copy.

Self-check: is an L3 switch always more secure than L2? No: role, configuration, updates and management matter. Does TLS inspection reveal every messaging payload? No: end-to-end protection can operate above transport.
