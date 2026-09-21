<!-- ES -->
# Glosario conectado: conceptos, capacidades y ejemplos

**Lectura D35.** Complemento de 36 fichas breves ES/EN; no sustituye ni renumera otros glosarios. Las definiciones son paráfrasis docentes, no citas normativas. Fuentes por dominio en [D36](#/recurso/D36). No todos los conceptos necesitan un fabricante; los ejemplos no son recomendaciones de compra ni equivalencias funcionales completas.

## Informática, hardware y red

| ID | Concepto ES / EN | Definición, ejemplo y límite |
|---|---|---|
| INT-G01 | Bit / bit | Elección binaria; ocho bits forman un byte. No tiene un fabricante equivalente. |
| INT-G02 | Codificación / encoding | Representación de datos; UTF-8 no es cifrado. |
| INT-G03 | Proceso / process | Ejecución con estado y recursos; nombre/PID no prueban legitimidad. |
| INT-G04 | Perfil / user profile | Preferencias/datos de una cuenta en un entorno; no equivale a toda su identidad. |
| INT-G05 | Arquitectura de instrucciones / ISA | Contrato de instrucciones, como x86-64/Arm; no es la microarquitectura completa. |
| INT-G06 | Caché / cache | Reutiliza datos/resultados; puede estar obsoleta y no sustituye backup. |
| INT-G07 | NUMA / non-uniform memory access | Topología donde la localidad de memoria afecta acceso; no toda RAM tiene idéntica latencia. |
| INT-G08 | GPU/NPU / accelerator | Procesamiento especializado; capacidad bruta no compara una tarea completa. |
| INT-G09 | Qubit / qubit | Unidad de información cuántica; medir no entrega todas las posibilidades simultáneamente. |
| INT-G10 | Switch / network switch | Reenvía tramas y puede integrar routing; no confundir todos los modelos o planos. |
| INT-G11 | Router / router | Reenvía entre redes según rutas; necesita retorno y política. |
| INT-G12 | VLAN / virtual LAN | Segmentación lógica de enlace; no garantiza aislamiento entre redes por sí sola. |
| INT-G13 | DNS / domain name system | Registros y resolución de nombres; filtrado DNS no inspecciona todo payload. |
| INT-G14 | TLS / transport layer security | Protege un canal según configuración y confianza; no toda protección E2EE termina en el proxy. |
| INT-G15 | QUIC / QUIC | Transporte multiplexado sobre UDP con seguridad; no es «HTTP inseguro por usar UDP». |
| INT-G16 | 6G/IMT-2030 / 6G | Programa de evolución y normalización; objetivos y borradores no son despliegue comercial universal. |

## Información, identidades y gobierno

| ID | Concepto ES / EN | Definición, ejemplo y límite |
|---|---|---|
| INT-G17 | Clasificación / classification | Política o régimen de tratamiento según contexto; no convertir automáticamente entre autoridades. |
| INT-G18 | TLP / traffic light protocol | Límites de difusión; no clasificación legal ni licencia de publicación. |
| INT-G19 | DLP / data loss prevention | Controles sobre salida/uso de datos en canales definidos; necesita cobertura y pruebas. |
| INT-G20 | UEM/MDM / endpoint/device management | Gestión de configuración y postura; no equivale a toda prevención de fuga. |
| INT-G21 | LDAP / lightweight directory access protocol | Protocolo de directorio; no es sinónimo de AD, Kerberos o SSO. |
| INT-G22 | AD DS / Active Directory Domain Services | Servicios de dominio de Microsoft; no intercambiable con Entra ID. |
| INT-G23 | IAM/IGA / identity management/governance | Operación de identidades y gobierno de acceso; incluye ciclo de vida, no solo login. |
| INT-G24 | JML / joiner–mover–leaver | Alta, cambio y baja; mover debe retirar accesos que ya no corresponden. |
| INT-G25 | RBAC / role-based access control | Permisos por rol; evitar acumular roles sin justificación. |
| INT-G26 | ABAC / attribute-based access control | Políticas con atributos de sujeto/recurso/acción/contexto; exige datos fiables. |
| INT-G27 | SoD / separation of duties | Separación de funciones frente a conflictos; incompatibilidad debe tener criterio y compensación. |
| INT-G28 | PAM / privileged access management | Control de privilegios, concesión y uso; una bóveda aislada no equivale a todo PAM. |
| INT-G29 | MFA / multi-factor authentication | Factores de categorías distintas; dos secretos memorizados no son dos factores. |
| INT-G30 | Evidencia / evidence | Observación que sustenta una afirmación acotada; un dashboard no certifica toda operación. |
| INT-G31 | Riesgo residual / residual risk | Lo que permanece tras los controles considerados; distinguir actual de objetivo estimado. |
| INT-G32 | Perfil CSF / organizational profile | Resultados actuales/objetivos según contexto; no es un perfil de usuario del SO. |

## Operación y arquitectura

| ID | Concepto ES / EN | Definición, ejemplo y límite |
|---|---|---|
| INT-G33 | WAF / web application firewall | Política sobre tráfico web/API visible; no corrige toda lógica de negocio. |
| INT-G34 | SIEM / security information and event management | Reúne/correlaciona eventos; no equivale a un firewall en línea. |
| INT-G35 | EDR / endpoint detection and response | Telemetría y respuesta del endpoint; depende de sensores, configuración y permisos. |
| INT-G36 | SLO / service-level objective | Objetivo medible del servicio; no es una garantía contractual automática. |

## Ejemplos de implementación: comparar capacidad y alcance

| Capacidad | Proyectos/alternativas abiertas | Ejemplos comerciales o fabricantes | Prueba docente y cautela |
|---|---|---|---|
| Identidad de sistemas y aplicaciones | FreeIPA, Keycloak | Microsoft AD DS/Entra ID | Son funciones diferentes; probar alta y revocación, no comparar solo login [P01–P03] |
| Contraseñas y privilegios | KeePassXC como gestor; no suite PAM completa | CyberArk, BeyondTrust | Identificar bóveda, aprobación, JIT y sesión por edición; referencias adicionales antes de instalar |
| Datos sensibles y DLP | Presidio como componente de identificación/redacción | Microsoft Purview, Forcepoint DLP, Symantec/Broadcom DLP | Biblioteca no equivale a cobertura endpoint/correo/cloud [I05–I09] |
| Cifrado de datos | LUKS/dm-crypt, VeraCrypt | BitLocker de Microsoft; FileVault de Apple | Elegir capa y probar recuperación; no producto contra usuario autenticado [I10–I11] |
| WAF | OWASP CRS como reglas con motor compatible; Coraza como ejemplo de motor | Cloudflare WAF, Akamai App & API Protector, Imperva, FortiWeb | Distinguir SaaS/appliance físico/virtual y edición; prueba de solicitud y función legítima [V01–V04] |
| Red y endpoint | Suricata/Zeek como observación de red; Wazuh como plataforma de seguridad | Microsoft Defender, CrowdStrike, Palo Alto Networks, Fortinet | No afirmar que todos son EDR o que un sensor ve todo el tráfico; comprobar función y documentación [V05–V07] |
| Inteligencia | MISP, OpenCTI | Plataformas CTI comerciales según caso | Procedencia, confianza, caducidad y uso, no «más IOCs = mejor» [V08–V09] |
| Infraestructura y entrega | Docker, Kubernetes, Proxmox | VMware/Broadcom, AWS, Azure, Google Cloud | Edición/licencia y responsabilidad; no equivalencia ni requisito de compra [W01–W05] |

Las referencias V01–V09 amplían documentación de proyectos y ejemplos seleccionados, no prueban instalación de todos los productos citados. Para un fabricante sin referencia específica en esta edición, la selección e instalación quedan pendientes de verificación del producto/edición. No se inventan prestaciones, licencias, precios o resultados comparativos.

## Cómo ampliar una ficha

Añade identificador estable, nombre ES/EN, definición, para qué sirve, primera lección, ejemplo sintético, error frecuente, fuente/versionado y prueba. Mantén conceptos distintos aunque una suite los venda juntos. Para noticias, registra fecha del hecho y de publicación, evidencia y si es un anuncio o resultado observado. [Método de fuentes](#/recurso/D36).

Ejercicio: elige un término y explica una afirmación falsa frecuente, una implementación y una prueba que podría refutarla. Se corrige el razonamiento y la trazabilidad, no la cantidad de marcas citadas.
<!-- EN -->
# Connected glossary: concepts, capabilities and examples

**Reading D35.** Thirty-six short ES/EN entries supplement existing glossaries without renumbering them. Definitions are teaching paraphrases, not normative quotations. Domain sources are in [D36](#/recurso/D36). Not every concept needs a vendor; examples are neither purchasing recommendations nor complete functional equivalents.

## Computing, hardware and networking

| ID | Concept | Definition, example and limitation |
|---|---|---|
| INT-G01 | Bit | Binary choice; eight bits form a byte. No equivalent manufacturer is needed. |
| INT-G02 | Encoding | Data representation; UTF-8 is not encryption. |
| INT-G03 | Process | Execution with state/resources; name/PID do not prove legitimacy. |
| INT-G04 | User profile | Environment-specific account preferences/data, not the whole identity. |
| INT-G05 | ISA / instruction-set architecture | Instruction contract such as x86-64/Arm, not the complete microarchitecture. |
| INT-G06 | Cache | Reuses data/results; can be stale and is not a backup. |
| INT-G07 | NUMA / non-uniform memory access | Memory locality affects access; latency need not be uniform. |
| INT-G08 | GPU/NPU / graphics or neural processing unit | Specialized acceleration; raw capacity does not compare a complete task. |
| INT-G09 | Qubit | Quantum information unit; measurement does not reveal all possibilities at once. |
| INT-G10 | Switch | Frame forwarding, sometimes routing; models and planes differ. |
| INT-G11 | Router | Forwarding between networks using routes; return paths/policy matter. |
| INT-G12 | VLAN / virtual local area network | Logical link-layer segmentation, not automatic inter-network isolation. |
| INT-G13 | DNS / domain name system | Name records/resolution; DNS filtering does not inspect every payload. |
| INT-G14 | TLS / transport layer security | Channel protection according to configuration/trust; not all E2EE terminates at a proxy. |
| INT-G15 | QUIC | Secure multiplexed transport over UDP, not inherently insecure HTTP. |
| INT-G16 | 6G/IMT-2030 | Evolution/standardization effort; goals/drafts are not universal commercial deployment. |

## Information, identity and governance

| ID | Concept | Definition, example and limitation |
|---|---|---|
| INT-G17 | Classification | Context-specific handling policy/regime; authorities do not map automatically. |
| INT-G18 | TLP / traffic light protocol | Sharing restrictions, not legal classification or a publication licence. |
| INT-G19 | DLP / data loss prevention | Data-use/egress controls on defined channels; coverage and tests matter. |
| INT-G20 | UEM/MDM / unified endpoint or mobile device management | Device configuration/posture management, not complete leakage prevention. |
| INT-G21 | LDAP / lightweight directory access protocol | Directory protocol, not a synonym for AD, Kerberos or SSO. |
| INT-G22 | AD DS / Active Directory Domain Services | Microsoft domain services, not interchangeable with Entra ID. |
| INT-G23 | IAM/IGA / identity and access management or identity governance and administration | Identity operations/access governance; lifecycle extends beyond login. |
| INT-G24 | JML / joiner–mover–leaver | Join/move/leave; movers require removal of obsolete rights. |
| INT-G25 | RBAC / role-based access control | Role-based permissions; avoid unjustified accumulation. |
| INT-G26 | ABAC / attribute-based access control | Subject/resource/action/context policies requiring trustworthy attributes. |
| INT-G27 | SoD / separation of duties | Conflicting duties require criteria, separation or compensation. |
| INT-G28 | PAM / privileged access management | Privilege approval/control/use; a standalone vault is not the entire capability. |
| INT-G29 | MFA / multi-factor authentication | Different factor categories; two memorized secrets are not two factors. |
| INT-G30 | Evidence | Observation supporting a bounded claim; dashboards do not certify all operations. |
| INT-G31 | Residual risk | Risk remaining after considered controls; current and estimated target differ. |
| INT-G32 | Organizational CSF profile | Contextual current/target outcomes, not an OS user profile. |

## Operations and architecture

| ID | Concept | Definition, example and limitation |
|---|---|---|
| INT-G33 | WAF / web application firewall | Policies over visible web/API traffic, not universal business-logic repair. |
| INT-G34 | SIEM / security information and event management | Event collection/correlation, not an inline firewall. |
| INT-G35 | EDR / endpoint detection and response | Endpoint telemetry/response dependent on sensors, settings and permissions. |
| INT-G36 | SLO / service-level objective | Measurable service objective, not automatically a contractual guarantee. |

## Implementation examples: compare capabilities and scope

| Capability | Open projects/alternatives | Commercial examples/vendors | Teaching test and caution |
|---|---|---|---|
| System/application identity | FreeIPA, Keycloak | Microsoft AD DS/Entra ID | Different functions; test onboarding/revocation rather than login alone [P01–P03] |
| Passwords/privileges | KeePassXC password manager, not complete PAM | CyberArk, BeyondTrust | Identify vault, approval, JIT and sessions per edition; further verification before installation |
| Sensitive data/DLP | Presidio identification/redaction components | Microsoft Purview, Forcepoint DLP, Symantec/Broadcom DLP | Libraries do not equal full endpoint/email/cloud coverage [I05–I09] |
| Data encryption | LUKS/dm-crypt, VeraCrypt | Microsoft BitLocker, Apple FileVault | Select layer and test recovery; not protection against every authenticated action [I10–I11] |
| WAF | OWASP CRS rules with a compatible engine; Coraza as an engine example | Cloudflare WAF, Akamai App & API Protector, Imperva, FortiWeb | Distinguish SaaS/physical/virtual appliances and editions; test policy and legitimate function [V01–V04] |
| Network/endpoint | Suricata/Zeek network observation; Wazuh security platform | Microsoft Defender, CrowdStrike, Palo Alto Networks, Fortinet | These are not all EDR or universally visible; verify purpose/documentation [V05–V07] |
| Intelligence | MISP, OpenCTI | Case-specific commercial CTI platforms | Provenance, confidence, expiry and use, not merely IOC volume [V08–V09] |
| Infrastructure/delivery | Docker, Kubernetes, Proxmox | VMware/Broadcom, AWS, Azure, Google Cloud | Edition/licence and responsibility; no equivalence or purchasing requirement [W01–W05] |

V01–V09 reference selected projects/examples, not tested installations of every named product. Product-specific selection/installation remains pending when a dedicated reference is absent. No invented features, licences, prices or comparative performance.

## Extending an entry

Add stable ID, ES/EN name, definition, purpose, first lesson, synthetic example, common error, versioned source and test. Keep concepts separate even where suites bundle them. For news preserve event/publication dates, evidence and distinction between announcement and observation. See [source method](#/recurso/D36).

Exercise: select one term, explain a common false claim, identify an implementation and propose a test that could refute the claim. Assessment rewards reasoning and traceability, not brand count.
