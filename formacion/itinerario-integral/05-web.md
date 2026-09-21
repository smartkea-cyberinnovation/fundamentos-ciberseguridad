<!-- ES -->
# Arquitecturas web: de un servidor a una operación empresarial

**Lectura D30.** Objetivo: justificar componentes y controles, no acumular productos. Reutiliza M24–M26/M32 y [redes](#/recurso/D29). Casos y criterios son propuestas docentes. Referencias W01–W05/N01 en [D36](#/recurso/D36).

## 1. Antes del diagrama: servicio, usuarios y datos

Define qué hace la aplicación, para quién, con qué datos y qué ocurre si falla. Especifica volumen y concurrencia como supuestos, no cifras inventadas de producción. Aclara autenticación, autorización, disponibilidad requerida, pérdida de datos tolerable, latencia útil y responsable de operación. Un diagrama sin esas preguntas es un dibujo de productos.

Identifica frontend, backend, API, base de datos, archivos, colas, cachés e identidades. No todos son necesarios. Una página estática puede ser suficiente para material público; añadir una base de datos y cuentas crea obligaciones de seguridad, privacidad y recuperación.

## 2. Ocho patrones progresivos

| Patrón | Componentes | Decisión y prueba imprescindible |
|---|---|---|
| Web estática | Archivos, hosting/CDN y DNS | Fuente→build→versión activa; recursos y 404 correctos |
| WordPress en un servidor | Web/PHP, base de datos y archivos | Updates, plugins, permisos, TLS y restauración conjunta |
| Aplicación en dos capas | App y datos separados | Red y credenciales mínimas; fallo de una dependencia |
| Varias instancias | Balanceador y réplicas | Salud real, sesiones, archivos compartidos y consistencia |
| Aplicación empresarial | Servicios, API, identidad, cola, datos | Contratos, autorización por objeto, trazabilidad y fallos parciales |
| Contenedores | Imágenes, redes y volúmenes | Procedencia, secretos, usuario, datos persistentes y rollback |
| PaaS/serverless/edge | Servicios gestionados y funciones | Responsabilidad compartida, límites, residencia y coste |
| Híbrido/multirregión | Conexiones y dominios de fallo | Identidad, replicación, pérdida admisible y prueba de recuperación |

No es una escala de prestigio. Un diseño simple puede satisfacer mejor un requisito; varias regiones pueden introducir costes, dependencia y consistencia no resueltos. Los marcos Well-Architected de AWS, Azure y Google Cloud ayudan a formular revisiones por pilares; no hacen intercambiables sus servicios [W01–W03].

## 3. WordPress como caso completo de administración

En un laboratorio aislado, documenta SO, servidor web, runtime, base de datos, directorio de contenido y cuentas. Distingue cuenta administrativa del sistema, cuenta de la aplicación y cuenta de conexión a la base. Limita escritura al recurso necesario, restringe administración y selecciona plugins por finalidad, mantenimiento y procedencia.

La copia debe permitir restaurar contenido y base en un estado compatible. Una copia solo del HTML visible no restaura WordPress. La prueba incluye entrar como usuario autorizado, publicar un contenido sintético, recuperar una versión y comprobar permisos. No expongas aplicaciones deliberadamente vulnerables junto al sitio público del campus.

## 4. Qué cambia al separar capas

Separar base y aplicación requiere rutas, firewall, TLS cuando corresponda, autenticación, secretos y observabilidad. Añadir réplicas exige decidir dónde viven sesiones, uploads y tareas programadas. Una cola desacopla tiempos pero introduce reintentos, duplicados y orden. Un caché acelera lecturas pero puede servir datos obsoletos o privados si la clave está mal diseñada.

El alumno debe seguir una operación completa: solicitud, identidad, autorización, cambio en datos, respuesta y registro. Diseña timeouts y errores sin filtrar secretos. No reintentes automáticamente una operación con efectos sin comprender idempotencia. Una señal de salud debe comprobar una función suficiente, no solo un proceso vivo.

## 5. Seguridad por ubicación y propósito

| Control | Dónde aporta valor | Lo que no demuestra |
|---|---|---|
| Firewall y segmentación | Flujos entre clientes, app, datos y gestión | Autorización correcta dentro de una aplicación |
| Reverse proxy/load balancer | Enrutamiento, TLS y disponibilidad | Que el backend sea seguro |
| WAF/WAAP | Políticas de solicitudes web/API | Reparación universal de lógica o acceso por objeto |
| IAM/MFA/gestión de sesión | Identificar y limitar accesos | Que todo usuario autenticado deba ver cualquier dato |
| Desarrollo seguro/ASVS | Requisitos verificables de aplicación | Cumplimiento por instalar un escáner |
| SAST/SCA/SBOM | Código, componentes y procedencia | Ausencia de vulnerabilidades en ejecución |
| Logs/SIEM | Correlación, investigación y alertas | Bloqueo en línea por el mero hecho de centralizar logs |
| Backup y recuperación | Disponibilidad e integridad operativa | Preservación forense o ausencia de pérdida sin prueba |

ASVS proporciona una base de requisitos verificables de aplicaciones; no se sustituye por una lista de marcas [W04]. WAF, EDR, IDS, SIEM y DLP son capacidades distintas, aunque algunos productos las empaqueten.

## 6. Docker, Compose, Swarm y Kubernetes

Una imagen tiene origen, versión y dependencias; un contenedor tiene proceso, usuario, filesystem, red y límites. Un volumen no queda respaldado por existir en un manifiesto. Compose facilita una aplicación local de varios servicios. Swarm y Kubernetes añaden scheduling, replicación y reconciliación, con conceptos y manifiestos diferentes.

La documentación Docker distingue `docker stack deploy` de todas las funciones del Compose actual [W05]. En Swarm, revisa el modo de publicación y routing mesh; no asumas el bind local de una práctica Compose. En Kubernetes, Secret no significa cifrado por el hecho de codificarse en base64. Revisa autorización, almacenamiento de secretos, acceso de red, cuentas de servicio y backups. Estas son decisiones a verificar en laboratorio, no despliegues realizados por esta lectura.

## 7. Bare metal y cloud: responsabilidades que no desaparecen

Bare metal da control físico/lógico según contrato; IaaS añade gestión de invitado; PaaS reduce parte de esa operación; SaaS delega la aplicación, pero no elimina responsabilidad sobre cuentas, datos, configuración y contratos. AWS, Azure y Google Cloud son ejemplos, no requisitos de compra. Incluye OVHcloud u otro proveedor cuando la actividad lo justifique, con documentación de la modalidad concreta.

Separa red pública/privada, identidad de usuario/servicio, región/zona, copias, egress, cuotas y soporte. No inventes un SLA de la arquitectura multiplicando porcentajes de servicios sin modelar dependencias. Declara hipótesis de fallo, coste y recuperación y mide lo posible.

## Prácticas y criterios

**INT-L09: evolución de una web.** Parte de un sitio informativo y agrega entrega privada de documentos sintéticos. Compara estático, WordPress y app con API. Evidencia: requisitos, diagrama, matriz datos/roles y justificación. Éxito: explicar qué nueva obligación introduce cada componente; no desplegar por defecto todo en Internet.

**INT-L10: incidente de disponibilidad.** Con logs preparados, el frontend responde pero la base rechaza conexiones tras una rotación de secreto. Propón triaje, contención de impacto, recuperación, comprobación y lección aprendida. Evidencia: cronología y cambio mínimo. Éxito: no abrir la base a todos ni registrar la credencial para depurar.

Autoevaluación: ¿qué protege el WAF que no protege un firewall L3/L4 y qué no protege ninguno? Explica punto de control, datos visibles y una autorización de negocio. ¿Qué significa «desplegado»? Versión cargada, activada y servicio verificado son tres evidencias diferentes.
<!-- EN -->
# Web architectures: from one server to enterprise operations

**Reading D30.** Justify components and controls rather than collecting products. Reuses M24–M26/M32 and [networks](#/recurso/D29). Cases and criteria are teaching designs. References W01–W05/N01 are in [D36](#/recurso/D36).

## 1. Start with service, users and data

Define the function, audience, data and consequences of failure. Treat volumes/concurrency as assumptions, not invented production measurements. Specify authentication, authorization, required availability, tolerable data loss, useful latency and operational ownership. Without these, architecture is merely a product diagram.

Identify frontend, backend, API, database, files, queues, caches and identities. Not every component is necessary. Static pages can serve public material; adding accounts and a database creates security, privacy and recovery obligations.

## 2. Eight progressive patterns

| Pattern | Components | Essential decision/test |
|---|---|---|
| Static site | Files, hosting/CDN and DNS | Sources→build→active release; correct assets and 404 |
| Single-server WordPress | Web/PHP, database and files | Updates, plugins, permissions, TLS and joint recovery |
| Two-tier application | Separate app/data | Minimal network and credentials; dependency failure |
| Multiple instances | Balancer and replicas | Useful health checks, sessions, shared files and consistency |
| Enterprise application | Services, API, identity, queues and data | Contracts, object authorization, tracing and partial failures |
| Containers | Images, networks and volumes | Provenance, secrets, user, persistent data and rollback |
| PaaS/serverless/edge | Managed services/functions | Shared responsibility, limits, location and cost |
| Hybrid/multiregion | Links and failure domains | Identity, replication, acceptable loss and recovery tests |

This is not a prestige ladder. Simpler designs may meet requirements better; multiple regions can introduce unresolved cost and consistency problems. AWS, Azure and Google Cloud Well-Architected frameworks support structured review, not interchangeable services [W01–W03].

## 3. WordPress as an administration case

In an isolated lab, document OS, web server, runtime, database, content directory and accounts. Separate OS administrator, application administrator and database connection identity. Restrict writes, administration and plugins according to purpose, maintenance and provenance.

A backup must restore compatible application content and database state. Copying rendered HTML does not restore WordPress. Verify authorized login, publication of synthetic content, restoration and permissions. Never publish deliberately vulnerable training applications beside the public campus.

## 4. What separating tiers changes

Separate app/database tiers need routes, firewall, appropriate TLS, authentication, secrets and observability. Replicas require decisions about sessions, uploads and scheduled work. Queues decouple timing but introduce retries, duplicates and ordering. Caches can return stale or private data when their keys or policies are wrong.

Trace one complete operation: request, identity, authorization, data change, response and log. Design timeouts and errors without exposing secrets. Do not automatically retry side-effecting operations without understanding idempotence. Health checks must assess a useful function, not just a live process.

## 5. Security by placement and purpose

| Control | Contribution | What it does not establish |
|---|---|---|
| Firewall/segmentation | Flows between clients, app, data and management | Correct application authorization |
| Reverse proxy/balancer | Routing, TLS and availability | Secure backend behavior |
| WAF/WAAP | Web/API request policies | Universal business-logic or object-access repair |
| IAM/MFA/session controls | Identify and constrain access | Universal access for authenticated users |
| Secure development/ASVS | Verifiable application requirements | Compliance from installing a scanner |
| SAST/SCA/SBOM | Code, components and provenance | Absence of runtime vulnerabilities |
| Logs/SIEM | Correlation, investigation and alerting | Inline prevention merely by centralizing events |
| Backup/recovery | Operational availability/integrity | Forensic preservation or zero loss without testing |

ASVS supports verifiable application requirements rather than a shopping list [W04]. WAF, EDR, IDS, SIEM and DLP remain distinct capabilities even where one vendor packages them.

## 6. Docker, Compose, Swarm and Kubernetes

Images have origin, version and dependencies; containers have process, user, filesystem, network and limits. Declaring a volume does not back it up. Compose supports multi-service application definitions; Swarm/Kubernetes add scheduling, replication and reconciliation through different concepts and manifests.

Docker documents that `docker stack deploy` does not support every current Compose feature [W05]. Review Swarm publication and routing mesh instead of assuming a local Compose bind. Kubernetes Secret content is not encrypted merely because it is base64-encoded. Examine authorization, secret storage, network access, service accounts and backups. These are lab decisions to verify, not deployments performed by reading this chapter.

## 7. Bare metal and cloud responsibilities

Bare metal offers contract-dependent control; IaaS retains guest administration; PaaS reduces some operations; SaaS delegates the application without removing responsibility for identities, data, configuration and contracts. AWS, Azure and Google Cloud are examples, not purchasing requirements. Add OVHcloud or another provider when justified, using documentation for the specific offering.

Separate public/private networking, user/service identity, region/zone, backups, egress, quotas and support. Do not invent an architecture SLA by multiplying service percentages without modeling dependencies. Declare failure, cost and recovery assumptions and measure what can be tested.

## Exercises and criteria

**INT-L09: evolving a website.** Start with an information site and add private delivery of synthetic documents. Compare static hosting, WordPress and an API application. Evidence: requirements, diagram, role/data matrix and rationale. Success: explain obligations introduced by each component; do not expose everything by default.

**INT-L10: availability incident.** Prepared logs show a working frontend but rejected database connections after secret rotation. Propose triage, impact containment, recovery, checks and lessons. Evidence: timeline and minimal change. Success: do not open the database to everyone or log credentials for debugging.

Self-check: what can a WAF protect that a L3/L4 firewall cannot, and what does neither automatically protect? Explain placement, visibility and business authorization. What does «deployed» mean? Upload, activation and verified service require distinct evidence.
