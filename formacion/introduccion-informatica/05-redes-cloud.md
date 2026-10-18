<!-- ES -->
# Redes, servicios de Internet, virtualización y cloud

D45 desarrolla T11 y T12. D29 introduce redes y dispositivos; M10 y M24 ofrecen prácticas de diagnóstico, M26 continúa con contenedores y M31 trata el uso supervisado de IA. Aquí seguimos un dato desde su red local hasta un servicio y delimitamos qué administra cada participante.

## Resultados de aprendizaje

Podrás distinguir direcciones y puertos, explicar DHCP y DNS, comparar TCP y UDP, interpretar evidencias por capas y asignar responsabilidades en IaaS, PaaS y SaaS. También distinguirás una máquina virtual de un contenedor sin asumir que cualquier aislamiento resulta suficiente.

## Direcciones, dispositivos y protocolos

LAN y WAN describen ámbitos de red; WLAN añade acceso local inalámbrico. Un switch reenvía tramas dentro de su dominio de enlace y un router decide el siguiente salto entre redes. Cliente y servidor son papeles en una interacción: un servidor web también puede ser cliente de una base de datos.

| Modelo TCP/IP | Función y ejemplos | Relación didáctica con OSI |
|---|---|---|
| Acceso a red | Tramas y medio: Ethernet, Wi-Fi | Física y enlace |
| Internet | Direcciones y encaminamiento: IP | Red |
| Transporte | Comunicación entre extremos: TCP, UDP | Transporte |
| Aplicación | Servicios: DNS, HTTP | Agrupa funciones de las capas superiores |

La correspondencia ayuda a razonar, pero no impone una equivalencia perfecta entre modelos. Una dirección **MAC** identifica interfaces en determinados enlaces; una dirección **IP** permite encaminamiento. IPv4 tiene 32 bits e IPv6, 128. Los puertos pertenecen a protocolos de transporte: TCP 53 y UDP 53 son espacios distintos. Un puerto habitual sugiere un servicio, pero no demuestra qué programa lo atiende ni quién lo utiliza.

**DHCPv4** puede entregar dirección, prefijo, router y servidores DNS mediante una concesión. Su intercambio inicial típico sigue Discover, Offer, Request y Acknowledge: DORA. Usa UDP, normalmente puerto 67 del servidor y 68 del cliente. La configuración recibida no demuestra por sí sola la identidad fiable del servidor [S1].

**DNS** resuelve nombres y otros datos. Un cliente consulta un resolvedor que puede responder desde caché o consultar servidores autoritativos. El TTL limita la conservación de una respuesta en caché. Los registros A contienen IPv4, AAAA contienen IPv6, CNAME indican alias y MX orientan la entrega de correo. DNS no descarga la página ni valida sus permisos [S2].

## Transporte y servicio: probar cada afirmación

**TCP** proporciona un flujo ordenado y fiable de bytes, con mecanismos de retransmisión y control; no conserva por sí mismo los límites de los mensajes de aplicación ni cifra el contenido [S3]. **UDP** transporta datagramas y no garantiza entrega, orden ni eliminación de duplicados; una aplicación puede añadir mecanismos propios [S4].

HTTP define solicitudes, respuestas y su significado. HTTPS protege HTTP mediante TLS. La validación de TLS y una respuesta HTTP son evidencias diferentes. Un `403` indica que el servicio ha entendido la solicitud y se niega a atenderla: investiga permisos y políticas del servicio según el contexto; no deduzcas automáticamente una contraseña incorrecta [S5]. Un ping ICMP contestado tampoco demuestra que funcione HTTP.

Un firewall aplica una política de tráfico. NAT traduce direcciones y, en algunos casos, puertos; esa traducción no define por sí sola una política suficiente. Una VPN protege un trayecto según su configuración, no todo el tratamiento posterior de los datos.

## Cloud: quién administra qué

| Modelo | El consumidor administra principalmente | Ejemplo de decisión |
|---|---|---|
| IaaS | Sistemas operativos, aplicaciones y configuración asignada | Actualizar el sistema de una máquina virtual |
| PaaS | Aplicación desplegada, datos y configuración disponible | Proteger secretos y permisos de la aplicación |
| SaaS | Uso del servicio, identidades, datos y ajustes disponibles | Revisar acceso y exportación de documentos |

El reparto exacto depende del servicio y del contrato. NIST distingue estos tres modelos y despliegues públicos, privados, comunitarios e híbridos. Su definición de cloud incluye autoservicio bajo demanda, acceso por red, recursos compartidos, elasticidad y medición. Tener una máquina virtual aislada no demuestra que se cumplan todas esas características [S6].

Una **máquina virtual** ejecuta un sistema invitado con su propio núcleo sobre una plataforma de virtualización. Un **contenedor** comparte el núcleo de su anfitrión y utiliza mecanismos de aislamiento y control de recursos. Docker Desktop puede incorporar una máquina virtual para alojar ese núcleo. Permisos, volúmenes y configuración condicionan el aislamiento; no se deduce una protección equivalente a una VM por usar una imagen [S7]. Compose describe aplicaciones con varios servicios; Swarm y Kubernetes añaden orquestación con modelos diferentes. Una descripción no acredita un despliegue funcionando.

La IA combina datos, algoritmos y recursos de cómputo: entrenamiento y uso del modelo son etapas distintas y una salida plausible requiere verificación. IoT integra dispositivos conectados; edge acerca procesamiento al origen del dato. Distribuir componentes cambia latencia, dependencias y puntos de fallo. Relaciona esas decisiones con arquitectura, acceso y recuperación, sin convertir una tendencia en requisito.

## Práctica local: interpretar una conexión ficticia

Ejecuta Python 3. Los rangos son de documentación; no se envían paquetes, no se resuelven nombres y no se inspecciona tráfico ajeno. Predice primero si el destino necesita router.

```bash
python3 - <<'PY'
from ipaddress import ip_address, ip_network

network = ip_network('192.0.2.0/24')
host = ip_address('192.0.2.10')
gateway = ip_address('192.0.2.1')
destination = ip_address('203.0.113.20')
assert host in network and gateway in network
next_hop = destination if destination in network else gateway
assert next_hop == gateway
print('siguiente salto:', next_hop)

def next_check(trace):
    if not trace['dns_answer']:
        return 'resolucion de nombres'
    if not trace['tcp_established']:
        return 'transporte y ruta'
    if not trace['tls_validated']:
        return 'validacion TLS'
    if trace['http_status'] == 403:
        return 'permisos y politicas del servicio'
    return 'interpretar la respuesta de aplicacion'

trace = dict(dns_answer=True, tcp_established=True,
             tls_validated=True, http_status=403)
assert next_check(trace) == 'permisos y politicas del servicio'
print('comprobar:', next_check(trace))
trace['tls_validated'] = False
assert next_check(trace) == 'validacion TLS'
print('caso alternativo:', next_check(trace))
PY
```

**Validación:** aparecen `192.0.2.1`, la comprobación de políticas y el caso TLS. El segundo caso recuerda que una observación HTTP atribuida a una conexión no validada no resuelve ese problema. El programa interpreta un conjunto declarado de evidencias; no diagnostica una red real. Solo utiliza memoria, que se libera al terminar.

**Evaluación:** dibuja DORA y una consulta DNS, explica por qué DNS correcto no garantiza HTTPS y asigna tres tareas de seguridad a consumidor o proveedor bajo un servicio concreto. Como extensión, interpreta un PCAP docente preparado y autorizado; justifica cada conclusión con el campo observado y reconoce lo que el cifrado no permite ver.

<!-- EN -->
# Networks, Internet services, virtualization, and cloud

D45 develops T11 and T12. D29 introduces networks and devices; M10 and M24 provide diagnostic practice, M26 continues with containers, and M31 addresses supervised AI use. Here we follow data from its local network to a service and identify what each participant administers.

## Learning outcomes

You will be able to distinguish addresses and ports, explain DHCP and DNS, compare TCP and UDP, interpret evidence by layer, and assign responsibilities in IaaS, PaaS, and SaaS. You will also distinguish a virtual machine from a container without assuming that every form of isolation is sufficient.

## Addresses, devices, and protocols

LAN and WAN describe network scope; WLAN adds local wireless access. A switch forwards frames within its link domain, while a router determines the next hop between networks. Client and server are roles in an interaction: a web server can also be a database client.

| TCP/IP model | Function and examples | Teaching relationship to OSI |
|---|---|---|
| Network access | Frames and medium: Ethernet, Wi-Fi | Physical and data link |
| Internet | Addressing and routing: IP | Network |
| Transport | Communication between endpoints: TCP, UDP | Transport |
| Application | Services: DNS, HTTP | Groups upper-layer functions |

The correspondence supports reasoning but does not impose a perfect equivalence between models. A **MAC** address identifies interfaces on certain links; an **IP** address supports routing. IPv4 has 32 bits and IPv6 has 128. Ports belong to transport protocols: TCP 53 and UDP 53 are separate spaces. A customary port suggests a service but does not demonstrate which program handles it or who uses it.

**DHCPv4** can supply an address, prefix, router, and DNS servers through a lease. Its typical initial exchange follows Discover, Offer, Request, and Acknowledge: DORA. It uses UDP, normally server port 67 and client port 68. Received configuration does not by itself establish the server's trusted identity [S1].

**DNS** resolves names and other data. A client queries a resolver, which can answer from cache or query authoritative servers. The TTL limits how long a response is retained in cache. A records hold IPv4 addresses, AAAA records hold IPv6 addresses, CNAME records indicate aliases, and MX records guide mail delivery. DNS neither downloads a page nor validates its permissions [S2].

## Transport and service: verify each claim

**TCP** provides an ordered, reliable byte stream with retransmission and control mechanisms; it does not preserve application message boundaries or encrypt content by itself [S3]. **UDP** carries datagrams without guaranteeing delivery, order, or duplicate elimination; an application can add mechanisms of its own [S4].

HTTP defines requests, responses, and their meaning. HTTPS protects HTTP using TLS. TLS validation and an HTTP response are different evidence. A `403` means that the service understood the request and refuses to fulfill it: investigate the service's permissions and policies in context; do not automatically infer an incorrect password [S5]. An answered ICMP ping does not demonstrate working HTTP either.

A firewall applies a traffic policy. NAT translates addresses and, in some cases, ports; translation does not define an adequate policy on its own. A VPN protects a path according to its configuration, not every subsequent use of the data.

## Cloud: who administers what

| Model | The consumer mainly administers | Example decision |
|---|---|---|
| IaaS | Operating systems, applications, and assigned configuration | Update a virtual machine's operating system |
| PaaS | Deployed application, data, and available configuration | Protect application secrets and permissions |
| SaaS | Service use, identities, data, and available settings | Review document access and export |

The precise division depends on the service and contract. NIST distinguishes these three service models and public, private, community, and hybrid deployments. Its cloud definition includes on-demand self-service, network access, resource pooling, elasticity, and measurement. An isolated virtual machine does not demonstrate all those characteristics [S6].

A **virtual machine** runs a guest system with its own kernel on a virtualization platform. A **container** shares its host's kernel and uses isolation and resource control mechanisms. Docker Desktop can include a virtual machine to host that kernel. Permissions, volumes, and configuration shape isolation; using an image does not establish protection equivalent to a VM [S7]. Compose describes applications with multiple services; Swarm and Kubernetes add orchestration with different models. A description does not establish that a deployment is operating.

AI combines data, algorithms, and computing resources: training and model use are different stages, and plausible output requires verification. IoT incorporates connected devices; edge brings processing closer to data sources. Distributing components changes latency, dependencies, and failure points. Relate those decisions to architecture, access, and recovery without turning a trend into a requirement.

## Local practice: interpret a fictitious connection

Run Python 3. The address ranges are reserved for documentation; no packets are sent, names resolved, or other people's traffic inspected. First predict whether the destination requires a router.

```bash
python3 - <<'PY'
from ipaddress import ip_address, ip_network

network = ip_network('192.0.2.0/24')
host = ip_address('192.0.2.10')
gateway = ip_address('192.0.2.1')
destination = ip_address('203.0.113.20')
assert host in network and gateway in network
next_hop = destination if destination in network else gateway
assert next_hop == gateway
print('next hop:', next_hop)

def next_check(trace):
    if not trace['dns_answer']:
        return 'name resolution'
    if not trace['tcp_established']:
        return 'transport and route'
    if not trace['tls_validated']:
        return 'TLS validation'
    if trace['http_status'] == 403:
        return 'service permissions and policies'
    return 'interpret the application response'

trace = dict(dns_answer=True, tcp_established=True,
             tls_validated=True, http_status=403)
assert next_check(trace) == 'service permissions and policies'
print('check:', next_check(trace))
trace['tls_validated'] = False
assert next_check(trace) == 'TLS validation'
print('alternative case:', next_check(trace))
PY
```

**Validation:** output includes `192.0.2.1`, the policy check, and the TLS case. The second case reminds us that an HTTP observation attributed to an unvalidated connection does not resolve that problem. The program interprets a declared evidence set; it does not diagnose a real network. It only uses memory, released on termination.

**Assessment:** draw DORA and a DNS query, explain why correct DNS does not guarantee HTTPS, and assign three security tasks to consumer or provider under a specific service. As an extension, interpret a prepared, authorized teaching PCAP; justify each conclusion using the observed field and recognize what encryption does not let you see.

<!-- COMMON -->
## Fuentes / Sources

- [S1 · IETF, RFC 2131: Dynamic Host Configuration Protocol](https://www.rfc-editor.org/rfc/rfc2131).
- [S2 · IETF, RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034) y / and [RFC 3596: DNS Extensions to Support IP Version 6](https://www.rfc-editor.org/rfc/rfc3596).
- [S3 · IETF, RFC 9293: Transmission Control Protocol](https://datatracker.ietf.org/doc/html/rfc9293).
- [S4 · IETF, RFC 768: User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768).
- [S5 · IETF, RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110).
- [S6 · NIST SP 800-145, The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final).
- [S7 · Docker documentation, What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).
- [Python, ipaddress](https://docs.python.org/3/library/ipaddress.html) y / and [IETF, RFC 5737: IPv4 Address Blocks Reserved for Documentation](https://www.rfc-editor.org/rfc/rfc5737).

Material propio de estudio. Referencias consultadas el 18 de octubre de 2026. / Original study material. References checked on 18 October 2026.
