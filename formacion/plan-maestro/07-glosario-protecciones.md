# 07 · Glosario ES/EN y capacidades de protección

[Índice](README.md) · [NIST y equipos](03-nist-equipos.md) · [Riesgos](05-gestion-riesgos.md) · [Fuentes](09-fuentes.md)

## Cómo utilizarlo

Glosario docente de **110 entradas** con finalidad y ejemplo o límite. No reproduce definiciones normativas literales: los términos CSF se contrastan con S01; riesgos con S03/S06; privacidad con S07/S09; infraestructura con S11–S17 y seguridad operativa con S04/S18–S32. Los productos se citan como ejemplos de categorías y no como equivalencias, certificación o recomendación de compra.

Cada futura ficha web debe enlazar el término con su primera lección, un caso práctico y la fuente correspondiente. Los acrónimos se desarrollarán en ambos idiomas cuando su traducción sea útil, manteniendo los nombres técnicos de productos y comandos.

## Informática y terminal

| ID | Término ES / EN | Qué significa, para qué sirve y ejemplo o límite |
|---|---|---|
| G001 | Bit / Bit | Unidad binaria de información. Permite representar estados; ocho bits forman un byte, pero un carácter puede ocupar varios bytes. |
| G002 | Byte / Byte | Grupo de ocho bits usado para medir datos. Distinguir capacidad decimal y binaria al comparar disco, memoria y archivos. |
| G003 | Codificación / Encoding | Regla para representar información como bytes. UTF-8 y UTF-16 pueden mostrar el mismo texto con hashes diferentes; no es cifrado. |
| G004 | Resumen criptográfico / Cryptographic hash | Huella calculada del contenido. Sirve para comparar integridad; no demuestra por sí sola autoría, procedencia o todos los metadatos. |
| G005 | Cifrado / Encryption | Transforma datos mediante un mecanismo y claves para proteger confidencialidad. La recuperación y custodia de claves son parte del diseño. |
| G006 | Firma digital / Digital signature | Mecanismo que vincula integridad y una clave de firma. Su interpretación exige validar cadena, política y contexto de identidad. |
| G007 | CPU / Processor | Ejecuta instrucciones. Arquitectura, núcleos y carga condicionan rendimiento; frecuencia de reloj aislada no permite comparar cualquier equipo. |
| G008 | RAM / Main memory | Memoria de trabajo de procesos y sistema. Caché ocupada no equivale necesariamente a falta de memoria útil. |
| G009 | Núcleo / Kernel | Componente privilegiado que gestiona recursos y aislamiento. Un contenedor suele compartir el kernel del host. |
| G010 | Proceso / Process | Instancia de ejecución con identidad y recursos. PID y nombre ayudan a observarlo, pero no acreditan legitimidad del ejecutable. |
| G011 | Hilo / Thread | Flujo de ejecución dentro de un proceso. Comparte parte de su contexto; no es sinónimo de núcleo de CPU. |
| G012 | Sistema de archivos / File system | Organiza contenido y metadatos. NTFS, APFS y ext4 tienen propiedades distintas de permisos, enlaces y recuperación. |
| G013 | Metadatos / Metadata | Información sobre un objeto: tamaño, tiempos, dueño o atributos. Copiar contenido no garantiza conservarlos. |
| G014 | Lista de control de acceso / ACL | Reglas de acceso asociadas a recursos. Verificar herencia y permiso efectivo; una entrada visible no explica toda autorización. |
| G015 | Terminal / Terminal | Interfaz para interactuar con una shell o programa. Abrirla no concede privilegios ni implica que se ejecute en el host esperado. |
| G016 | Intérprete de órdenes / Shell | Interpreta comandos y expansiones. Bash, zsh, CMD y PowerShell no comparten íntegramente sintaxis ni semántica. |
| G017 | Tubería / Pipeline | Conecta etapas de procesamiento. Entre cmdlets PowerShell suelen circular objetos; en herramientas Unix, bytes o texto. |
| G018 | Código de salida / Exit status | Resultado numérico de un programa. Su significado depende del contrato; no todos los ejecutables interpretan igual valores no cero. |
| G019 | Idempotencia / Idempotence | Repetir una operación mantiene el estado deseado sin efectos adicionales indebidos. No equivale a que cualquier repetición sea segura. |
| G020 | Commit / Commit | Instantánea versionada y metadatos del cambio en Git. Borrar un secreto del último archivo no lo borra automáticamente del historial. |

## Redes, web y arquitectura

| ID | Término ES / EN | Qué significa, para qué sirve y ejemplo o límite |
|---|---|---|
| G021 | Dirección IP / IP address | Identifica una interfaz lógica para comunicación. Una IP observada no identifica por sí sola una persona ni un equipo permanente. |
| G022 | Prefijo CIDR / CIDR prefix | Representa una red y su longitud de prefijo. Permite calcular subredes y alcance de rutas/reglas. |
| G023 | DNS / Domain Name System | Resuelve nombres y otros datos mediante registros. Distinguir resolución recursiva, autoridad, caché y TTL. |
| G024 | DHCP / Dynamic Host Configuration Protocol | Distribuye configuración de red a clientes. Obtener una dirección no demuestra conectividad a una aplicación. |
| G025 | Enrutamiento / Routing | Selecciona el siguiente salto hacia redes. Deben existir rutas de ida y retorno para el flujo esperado. |
| G026 | VLAN / Virtual LAN | Separa dominios lógicos de capa de enlace. Requiere políticas de interconexión; crear VLAN no garantiza aislamiento completo. |
| G027 | NAT / Network Address Translation | Traduce direcciones o puertos. No sustituye políticas de firewall, identidad o segmentación. |
| G028 | TCP y UDP / TCP and UDP | Transportes con propiedades distintas. La elección depende de la aplicación; un socket abierto no confirma una respuesta funcional. |
| G029 | TLS / Transport Layer Security | Protege un canal y autentica según configuración. Validar nombre, cadena y vigencia; desactivar validación no corrige confianza. |
| G030 | PKI / Public Key Infrastructure | Organiza certificados, claves, autoridades y revocación. Emitir un certificado implica gestionar su ciclo de vida. |
| G031 | HTTP / Hypertext Transfer Protocol | Intercambio de solicitudes y respuestas web. Método, estado y cabeceras necesitan contexto de aplicación. |
| G032 | API / Application Programming Interface | Contrato de interacción entre componentes. Debe definir datos, errores, autorización, versiones y límites. |
| G033 | Proxy inverso / Reverse proxy | Recibe solicitudes en nombre de servicios internos. Puede terminar TLS o enrutar; no es automáticamente un WAF. |
| G034 | Balanceador / Load balancer | Distribuye trabajo entre destinos. La alta disponibilidad depende también de datos, sesiones, salud y dependencias. |
| G035 | CDN / Content Delivery Network | Distribuye contenido y cachés cerca de usuarios. La caché puede alterar visibilidad o exponer datos si se configura mal. |
| G036 | Hipervisor / Hypervisor | Administra ejecución de máquinas virtuales y recursos. Diferenciar producto, modalidad y responsabilidades del anfitrión. |
| G037 | Máquina virtual / Virtual machine | Sistema invitado con recursos virtualizados. Snapshot, backup y exportación tienen finalidades distintas. |
| G038 | Contenedor / Container | Empaqueta ejecución con aislamiento a nivel de sistema. No aporta kernel independiente ni elimina riesgos del host por defecto. |
| G039 | Orquestador / Orchestrator | Coordina workloads, scheduling y estado deseado. Swarm/Kubernetes requieren operación, permisos y recuperación propios. |
| G040 | Infraestructura como código / Infrastructure as Code | Describe infraestructura de forma revisable y repetible. El estado, los secretos y el drift necesitan gestión separada. |

## Gobierno, NIST y riesgo

| ID | Término ES / EN | Qué significa, para qué sirve y ejemplo o límite |
|---|---|---|
| G041 | Activo / Asset | Recurso con valor para objetivos: dato, equipo, servicio o conocimiento. Debe relacionarse con dueño y dependencias. |
| G042 | Servicio / Service | Capacidad entregada a usuarios o negocio. Su criticidad ayuda a priorizar activos y recuperación. |
| G043 | Amenaza / Threat | Fuente o causa potencial de daño. Puede ser maliciosa, accidental, física o de proveedor. |
| G044 | Vulnerabilidad / Vulnerability | Debilidad relevante para un escenario. Su existencia no demuestra que haya sido explotada. |
| G045 | Evento / Event | Hecho observado o registrado. Puede ser normal; interpretación y cobertura deben explicarse. |
| G046 | Alerta / Alert | Señal generada por una condición de detección. Requiere triaje; no es automáticamente un incidente. |
| G047 | Incidente / Incident | Situación que cumple criterios de impacto o amenaza sobre seguridad/operación establecidos. Su gestión exige autoridad y coordinación. |
| G048 | Riesgo / Risk | Incertidumbre sobre objetivos expresada mediante escenarios y consecuencias. Una puntuación sin supuestos no basta para decidir. |
| G049 | Riesgo inherente / Inherent risk | Valoración sobre una línea base explícita antes de descontar los controles definidos. La línea base debe quedar registrada. |
| G050 | Riesgo actual / Current risk | Valoración con controles existentes y eficacia observada. No debe incluir mejoras todavía no implantadas. |
| G051 | Riesgo objetivo / Target risk | Estimación después de un tratamiento propuesto. Debe verificarse cuando se implemente. |
| G052 | Riesgo residual / Residual risk | Riesgo que permanece tras los controles considerados. Indicar si es residual actual o una previsión objetivo. |
| G053 | Control o salvaguarda / Control or safeguard | Medida humana, técnica u organizativa que modifica un riesgo. Debe tener objetivo, alcance, dueño y prueba. |
| G054 | Política / Policy | Expectativa y dirección aprobadas. Necesita procedimientos y evidencia de aplicación. |
| G055 | Estándar interno / Internal standard | Requisito técnico u operativo concreto que desarrolla políticas. No confundirlo con toda norma externa. |
| G056 | Procedimiento / Procedure | Secuencia y responsabilidades para ejecutar una tarea. Su uso debe ser verificable y mantenerse actualizado. |
| G057 | Apetito de riesgo / Risk appetite | Orientación sobre tipos y magnitud de riesgo que se asumen al perseguir objetivos. Debe traducirse en decisiones. |
| G058 | Tolerancia / Risk tolerance | Límites aceptables según el contexto y los criterios elegidos. No se deduce de un color sin definición. |
| G059 | Propietario del riesgo / Risk owner | Responsable con autoridad definida para tratar y escalar el riesgo. No tiene por qué operar todos sus controles. |
| G060 | Excepción / Exception | Desviación autorizada con justificación, compensación y plazo. No elimina el riesgo ni reemplaza revisión. |
| G061 | Evidencia / Evidence | Información que sustenta una afirmación dentro de un alcance. Debe tener origen, periodo, método y límites. |
| G062 | Auditoría / Audit | Evaluación sistemática respecto de criterios. Requiere evidencia y la independencia apropiada; no es solo ejecutar un escáner. |
| G063 | GRC / Governance, Risk and Compliance | Coordinación de gobierno, riesgo y cumplimiento. Relaciona decisiones, obligaciones, controles y seguimiento. |
| G064 | Núcleo CSF / CSF Core | Estructura de resultados del marco. No es por sí misma un catálogo de herramientas o de configuraciones. |
| G065 | Función CSF / CSF Function | Agrupación superior: Govern, Identify, Protect, Detect, Respond y Recover. No equivale a seis departamentos aislados. |
| G066 | Categoría CSF / CSF Category | Agrupa resultados relacionados dentro de una función. Por ejemplo PR.AA trata identidad, autenticación y acceso. |
| G067 | Subcategoría CSF / CSF Subcategory | Resultado más específico que se usa en perfiles y correspondencias. Su ID debe conservarse con la versión del marco. |
| G068 | Perfil / Organizational Profile | Describe resultados actuales u objetivos según misión y riesgo. Una comparación identifica prioridades y lagunas. |
| G069 | Tier / CSF Tier | Caracteriza el rigor de prácticas de gobierno y gestión del riesgo. No es una certificación ni una nota universal de madurez. |
| G070 | Declaración de aplicabilidad / Statement of Applicability | Documenta selección y justificación de controles en el marco pertinente. Los documentos ISO y ENS no son intercambiables sin análisis. |

## Protecciones, operación y respuesta

| ID | Término ES / EN | Qué significa, para qué sirve y ejemplo o límite |
|---|---|---|
| G071 | IAM / Identity and Access Management | Gestiona identidades y acceso. Incluye ciclo de vida y permisos, no solo una pantalla de login. |
| G072 | MFA / Multi-Factor Authentication | Combina factores de categorías distintas. Dos contraseñas no constituyen dos factores; la resistencia al phishing varía. |
| G073 | SSO / Single Sign-On | Permite acceder a servicios mediante una identidad federada. Reduce inicios separados, pero concentra dependencia de identidad. |
| G074 | PAM / Privileged Access Management | Gestiona accesos privilegiados, su concesión y registro. Comprar una bóveda no revisa por sí solo todos los privilegios. |
| G075 | Confianza cero / Zero Trust | Principios de acceso contextual y mínimo privilegio sin confianza implícita por ubicación. No es un único producto. |
| G076 | Firewall / Firewall | Aplica reglas de tráfico según capacidades. Debe relacionarse con flujos permitidos y pruebas, no solo listas de puertos. |
| G077 | WAF / Web Application Firewall | Analiza tráfico web y aplica políticas. Complementa desarrollo seguro; no corrige toda autorización de negocio. |
| G078 | WAAP / Web Application and API Protection | Agrupa capacidades de protección web/API según proveedor. Confirmar componentes, alcance y licencias concretas. |
| G079 | IDS/IPS / Intrusion Detection or Prevention System | Detecta patrones o puede actuar sobre tráfico según modo. Diferenciar sensor pasivo y componente en línea. |
| G080 | EDR / Endpoint Detection and Response | Recoge telemetría y facilita detección/respuesta en endpoints. La cobertura depende de sensores, configuración y plataformas. |
| G081 | EPP / Endpoint Protection Platform | Conjunto de controles preventivos de endpoint. No es idéntico a EDR aunque un producto pueda integrar ambos. |
| G082 | SIEM / Security Information and Event Management | Centraliza y analiza eventos de seguridad. Datos sin calidad, reglas ni operación no generan detección útil automáticamente. |
| G083 | SOAR / Security Orchestration, Automation and Response | Coordina tareas de respuesta. Las acciones con impacto necesitan permisos, controles y aprobación adecuados. |
| G084 | NDR / Network Detection and Response | Analiza actividad de red para detectar y responder según capacidades. El cifrado y puntos ciegos condicionan visibilidad. |
| G085 | NAC / Network Access Control | Controla admisión/acceso de dispositivos a la red. Requiere diseño para equipos no gestionados y recuperación. |
| G086 | DLP / Data Loss Prevention | Detecta o limita usos/divulgación de datos definidos. Necesita clasificación, contexto, excepciones y respeto de privacidad. |
| G087 | KMS/HSM / Key Management Service/Hardware Security Module | Servicios o dispositivos para custodiar/usar claves. Sus garantías, administración y recuperación no son idénticas. |
| G088 | MDM/UEM / Mobile Device/Unified Endpoint Management | Gestiona configuración y ciclo de vida de dispositivos. Tener enrolamiento no garantiza conformidad efectiva. |
| G089 | CSPM / Cloud Security Posture Management | Identifica desviaciones de postura cloud. Necesita alcance y permisos; un hallazgo no equivale a incidente. |
| G090 | SAST/SCA / Static Application Security Testing/Software Composition Analysis | Analizan código o componentes con objetivos distintos. Deben integrarse con revisión y pruebas; no certifican ausencia de fallos. |
| G091 | SBOM / Software Bill of Materials | Inventario de componentes de software. Facilita trazabilidad; requiere versión, alcance y actualización. |
| G092 | CTI / Cyber Threat Intelligence | Información evaluada y contextualizada para decisiones sobre amenazas. Una lista de IP sin fuente ni pregunta no es suficiente. |
| G093 | IOC / Indicator of Compromise | Dato usado para buscar indicios: hash, dominio o ruta. Coincidencia aislada exige contexto y vigencia. |
| G094 | TTP / Tactics, Techniques and Procedures | Describe comportamiento adversario. ATT&CK ofrece un vocabulario; no debe forzarse cada evento a una técnica. |
| G095 | Triaje / Triage | Evaluación inicial para priorizar y decidir el siguiente paso. Distinguir severidad del efecto y confianza de la señal. |
| G096 | Contención / Containment | Limita efectos o propagación del incidente. Debe considerar impacto en negocio, evidencia y recuperación. |
| G097 | Cadena de custodia / Chain of custody | Registro de manejo, transferencias e integridad de evidencia. Un hash por sí solo no constituye toda la cadena. |
| G098 | BIA / Business Impact Analysis | Analiza efectos de interrupción en procesos y dependencias. Sirve para acordar prioridades y necesidades de recuperación. |
| G099 | RPO / Recovery Point Objective | Objetivo de punto de recuperación, relacionado con pérdida de datos tolerable. Debe contrastarse con la restauración conseguida. |
| G100 | RTO / Recovery Time Objective | Objetivo de tiempo para recuperar una capacidad. No es el tiempo medido hasta que se realiza un ensayo real. |
| G101 | Copia de seguridad / Backup | Copia destinada a recuperación con retención y restauración. Sin prueba de lectura/restauración no se demuestra su utilidad. |
| G102 | Recuperación ante desastre / Disaster recovery | Estrategia y procedimientos para restablecer capacidades tras interrupción grave. Necesita personas, dependencias y pruebas. |
| G103 | SLI/SLO / Service Level Indicator/Objective | Medida y objetivo de calidad de servicio. Fijar ventana y condiciones; no confundirlos con un acuerdo contractual completo. |
| G104 | OTP / One-Time Password | Código de uso único para una operación de autenticación. Requiere caducidad, límites y vínculo con el intento; no es una sesión permanente. |
| G105 | Cookie / Cookie | Dato gestionado por el navegador para un origen y alcance. Puede transportar referencia de sesión; proteger atributos y contenido. |
| G106 | Sesión / Session | Contexto de interacción autenticada o de trabajo. Compartir un enlace de lección no debe transferir automáticamente credenciales de sesión. |
| G107 | CVE / Common Vulnerabilities and Exposures | Identificador de una vulnerabilidad publicada. Su presencia en un componente exige comprobar versión, exposición y contexto. |
| G108 | CVSS / Common Vulnerability Scoring System | Describe severidad técnica mediante un modelo versionado. No equivale por sí solo al riesgo de negocio. |
| G109 | Inyección SQL / SQL injection | Debilidad al confundir datos y estructura de una consulta. Se estudia mediante diseño seguro, parametrización y revisión de código, no cargas de explotación. |
| G110 | Autorización API / API authorization | Decide si la identidad puede realizar una operación sobre un recurso concreto. Un login válido no autoriza acceder a todos los objetos. |

## Ficha desarrollada: WAF

**Qué es:** control situado en el recorrido del tráfico web que inspecciona solicitudes y, según producto/configuración, respuestas y contexto para aplicar políticas. **Para qué sirve:** limitar determinadas solicitudes no deseadas y aportar visibilidad. **Qué no es:** sustituto universal de desarrollo seguro, IAM, parcheo, protección endpoint o control de acceso a datos. [S21–S25]

**Ejemplo de uso:** un portal necesita publicar HTTP(S) y registrar bloqueos relevantes sin exponer administración. El equipo define qué rutas, hosts y métodos espera; ajusta reglas y excepciones; mide falsos positivos y conserva los registros proporcionados al caso. Antes de bloquear, ensaya funciones legítimas y una condición benigna identificable del laboratorio. Esa prueba valida el recorrido de la regla, no una tasa universal de detección.

### Modalidades y ejemplos

| Modalidad | Ejemplos de producto o proyecto | Qué evaluar |
|---|---|---|
| Servicio cloud/edge | Cloudflare WAF; Akamai App & API Protector; Imperva Cloud WAF | Integración DNS/proxy, terminación TLS, acceso al origen, reglas, logs, ubicación de datos, capacidad y contrato |
| Appliance físico o virtual | Fortinet FortiWeb; ofertas de WAF de centro de datos de Imperva según modalidad vigente | Capacidad, HA, certificados, parcheo del appliance, licencias, soporte, continuidad y responsabilidad de operación |
| Software administrado por el equipo | OWASP CRS con un motor compatible, como ModSecurity | Motor frente a reglas; integración con web/proxy; actualizaciones, pruebas, recursos, logs y mantenimiento |

Las fuentes de fabricante describen ofertas comerciales y no constituyen una comparación independiente. No se presupone que todas las funciones estén incluidas en cualquier plan, modalidad o versión. FortiWeb contempla opciones appliance/virtuales; las ofertas concretas de Imperva deben confirmarse en su catálogo al diseñar la práctica. [S21–S25]

### Decisiones y límites

Determinar dónde se descifra HTTP, quién custodia claves y si el tráfico puede evitar el control llegando directamente al origen. Definir qué direcciones/cabeceras del proxy son fiables. Comprobar APIs, cargas grandes, ficheros, sesiones, timeouts y disponibilidad según el caso, no mediante una configuración universal.

Una regla excesiva puede bloquear funciones legítimas; una excepción amplia puede ocultar actividad relevante. Registrar propietario, razón, alcance y caducidad de las excepciones. Los logs pueden contener datos personales o secretos: minimizar campos, acceso y retención. La operación requiere parcheo, revisión, monitorización y ensayo de recuperación.

**Evidencia de control:** configuración vigente, cobertura de hosts/rutas, prueba permitida y denegada, log correlacionado, responsables y limitaciones. **Relación CSF orientativa:** PR.PS/PR.IR y DE.CM/DE.AE según el resultado y la implementación; no existe una equivalencia automática «WAF comprado = categoría cumplida». [S01]

## Otras fichas que deben desarrollarse con el mismo patrón

IAM/MFA/PAM, firewall/segmentación, EDR, SIEM, SOAR, NDR, DLP, gestión de vulnerabilidades, backup, KMS, seguridad de correo, MDM y controles cloud. Cada ficha debe identificar amenaza, activo, mecanismo, modalidad, producto/proyecto de ejemplo, límites, responsable, coste, logs y prueba. MISP/OpenCTI ilustran gestión de inteligencia; Zeek/Suricata aportan observación/detección de red; Microsoft Sentinel y Defender for Endpoint ilustran otras capacidades. No se presentan como sustitutos intercambiables. [S26–S31]
