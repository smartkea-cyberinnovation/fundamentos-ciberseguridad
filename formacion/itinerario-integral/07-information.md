<!-- ES -->
# Gestión de información: clasificar, proteger y demostrar

**Lectura D32 · Revisión 2026-09-21.** Objetivo: diseñar el ciclo de vida de información y comprobar controles sin confundir etiquetas, productos y obligaciones. Reutiliza M09/M19/M23, [gobierno](#/recurso/D31) y [navegación](#/recurso/D24). Referencias I01–I11/S05–S06 en [D36](#/recurso/D36). No constituye asesoramiento jurídico individual.

## 1. El dato necesita contexto y dueño

Gestionar información incluye identificarla, asignar propietario, evaluar calidad y sensibilidad, definir finalidad, acceso, uso, conservación, transferencia y retirada. Un inventario de ordenadores no sustituye el inventario de datos o de tratamientos. Relaciona servicio, dataset, ubicación, copia, destinatarios, custodio y obligaciones.

Define quién decide clasificación, quién implementa permisos, quién autoriza divulgación y quién revisa. El custodio técnico no es automáticamente propietario del dato; «responsable del tratamiento» tiene un significado jurídico específico, distinto de administrador o dueño de servicio. Una retención sin fin aumenta exposición; borrar precipitadamente puede incumplir conservación o destruir evidencia.

## 2. Cuatro planos de clasificación que no se convierten automáticamente

| Plano | Propósito y autoridad | Ejemplo y límite |
|---|---|---|
| Clasificación corporativa | Política aprobada por la organización | Pública, interna, confidencial y restringida son un esquema docente, no categorías legales universales |
| Información clasificada por autoridad | Régimen jurídico y procedimientos específicos | ONS/CNI y sistemas UE u OTAN requieren autoridad, habilitación y reglas pertinentes; no basta etiquetar un archivo |
| CUI estadounidense | Información no clasificada con requisitos de salvaguarda/difusión definidos | NARA mantiene el programa/registro; no es una etiqueta corporativa intercambiable |
| TLP | Límites de difusión establecidos por quien comparte | FIRST TLP 2.0 no reemplaza clasificación formal, licencia o reglas criptográficas |

FIRST utiliza TLP:RED, TLP:AMBER, TLP:GREEN y TLP:CLEAR; AMBER+STRICT restringe AMBER a la organización. Mantén las etiquetas originales y consulta las reglas antes de reenviar. TLP no concede por sí mismo derecho a divulgar datos personales [I01]. Las categorías ENS BAJA/MEDIA/ALTA corresponden a sistemas y su evaluación, no a niveles de secreto de cualquier documento [S05].

Las fuentes CNI/ONS, UE y NARA se emplean para explicar sus respectivos ámbitos, sin crear una equivalencia «confidencial corporativo = EU CONFIDENTIAL» [I02–I04]. CCN-CERT/CISA ofrecen guías operativas; identifica la guía concreta, su audiencia, versión y autoridad antes de adoptar sus marcas. No inventes un esquema único «CCN/CNI/CISA/EU».

## 3. Política corporativa de manejo: ejemplo original

| Nivel docente | Acceso y circulación | Almacenamiento, transferencia y retirada |
|---|---|---|
| Pública aprobada | Publicación con dueño y revisión | Integridad, versión y derechos de uso; publicación no significa ausencia de controles |
| Interna | Personal autorizado por función | Repositorios gestionados; acceso externo aprobado; retención definida |
| Confidencial | Necesidad de conocer y propietario | Grupos revisados, cifrado adecuado, destinatarios verificados y registro proporcional |
| Restringida | Autorización nominativa o por atributo, revisiones frecuentes | Entorno y canales aprobados, acceso temporal, controles de salida y recuperación probada |

Esta política es un caso sintético. Define también excepciones, reclasificación, documentos compuestos, exportaciones, copias y metadatos. Evita inferir sensibilidad únicamente del nombre del archivo o de un patrón. La etiqueta debe vincularse a reglas de manejo; un color sin efecto no protege información.

## 4. DLP: política, punto de control y cobertura

DLP puede descubrir contenido sensible, reconocer etiquetas y aplicar acciones sobre canales definidos. Distingue detección, aviso, justificación, bloqueo y respuesta. Una coincidencia no acredita fuga; la ausencia de alerta no acredita control de todos los canales. Diseña falsos positivos/negativos y pruebas con datos ficticios.

Microsoft Purview Endpoint DLP aplica a plataformas y actividades documentadas, con diferencias entre Windows y macOS [I05]. Intune administra dispositivos/aplicaciones y puede apoyar despliegue y postura; no es equivalente a todo Purview DLP [I06]. Forcepoint DLP y las modalidades Symantec DLP de Broadcom son otros ejemplos comerciales; verificar edición, licencia, sistema, canal y agente antes de prometer cobertura [I07–I08].

En código abierto, Microsoft Presidio ofrece análisis y anonimización/redacción de datos sensibles; no es por sí solo una plataforma completa de control de correo, endpoint y nube [I09]. Puede servir en un ejercicio de clasificación con textos sintéticos. No se fuerza una equivalencia entre una biblioteca, un motor de reglas y una suite empresarial.

Ficha de prueba: canal, aplicación, usuario, dispositivo, tipo de dato, acción permitida, acción denegada, evento esperado, excepción, responsable y rollback. Incluye copia a USB, correo, subida web y sincronización solo si la herramienta realmente cubre esos canales. No pruebes con datos personales reales ni con cuentas personales de alumnos.

## 5. Cifrado por capas

Cifrado en reposo protege medios o datos bajo condiciones definidas; en tránsito protege un canal; E2EE pretende limitar acceso al contenido a los extremos autorizados. Son capas distintas. Un proxy que termina TLS no necesariamente puede leer un payload con cifrado de extremo a extremo. Una sesión desbloqueada conserva capacidad de leer datos aunque el disco esté cifrado.

Gestiona algoritmo/configuración aprobados, claves, recuperación, revocación y acceso. Distingue cifrado de volumen, contenedor de archivos y aplicación. BitLocker, FileVault, LUKS/dm-crypt y VeraCrypt responden a entornos y modos diferentes; revisar soporte y documentación local. No habilitar cifrado sin custodiar y probar recuperación. BitLocker es una capacidad de cifrado de volúmenes Windows; no sustituye ACL, DLP o seguridad de la sesión [I10]. VeraCrypt documenta modos y límites que deben elegirse para el caso [I11].

El laboratorio puede utilizar un volumen virtual desechable con archivo sintético, nunca cifrar el único disco de trabajo. Comprueba copia y restauración en un destino distinto. Las claves de recuperación no se suben al repositorio ni se colocan en una captura. Destrucción de clave y sanitización física requieren procedimientos adecuados al medio; no atribuyas borrado verificable a un simple `rm`.

## 6. RGPD, normativa y vigilancia laboral

Identifica ámbito, finalidad, base jurídica, minimización, destinatarios, conservación y derechos antes de desplegar monitorización. RGPD, LOPDGDD, LSSI y regímenes sectoriales tienen objetos distintos; una conformidad técnica no resuelve todas las obligaciones [S06, I12–I13]. En España, el artículo 87 de LOPDGDD regula intimidad y dispositivos digitales en el trabajo, incluyendo criterios de uso e información a las personas trabajadoras [I12].

La inspección TLS, las capturas y los logs pueden tratar contenido sensible. Diseña necesidad, proporcionalidad, exclusiones, control de administradores, acceso, retención y consulta a privacidad/legal. No presentar el consentimiento laboral como solución universal ni instalar una CA de inspección en dispositivos personales sin un esquema legítimo, transparente y autorizado. El curso estudia arquitectura y datos sintéticos, no vigilancia oculta.

## 7. Incidente y restauración de información

Si un documento sintético se comparte con un destinatario indebido, registra qué se sabe: versión, destinatarios, acceso confirmado o potencial, permisos y registros disponibles. Limita acceso sin destruir evidencia; decide comunicaciones mediante responsables. Revocar un enlace no garantiza borrar copias ya descargadas.

Recuperar implica contenido, consistencia, permisos y validación del servicio. Diferencia backup de sincronización y conservación forense. Las métricas útiles incluyen porcentaje de datasets con dueño y retención, permisos revisados, cobertura real DLP, falsos positivos y restauraciones comprobadas.

## Prácticas y autocorrección

**INT-L13: clasificación y manejo.** El docente entrega doce documentos ficticios: folleto público, inventario, nómina sintética, configuración sin secretos y una alerta TLP. Asigna esquema aplicable, propietario, destinatarios y retención; explica tres decisiones ambiguas. Evidencia: matriz y excepción. Éxito: no convertir TLP en autorización legal ni confundir categoría ENS con etiqueta.

**INT-L14: prueba de protección de datos.** Sobre un volumen/carpeta de ensayo, verifica lectura permitida, denegación, cifrado elegido y restauración. Una segunda parte usa eventos DLP sintéticos para clasificar verdadero/falso positivo. Evidencia: pruebas, log minimizado y recuperación. Éxito: no exponer claves ni afirmar que se ejecutó una suite no disponible.

Autoevaluación: ¿impide BitLocker que un usuario ya autenticado adjunte un archivo autorizado a su correo? No por sí solo: hace falta analizar permisos, canal y política de salida. ¿Significa TLP:CLEAR «sin derechos de autor ni datos personales»? No. ¿Es Intune un sustituto completo de DLP? No; clasifica capacidades y cobertura.
<!-- EN -->
# Information management: classify, protect and demonstrate

**Reading D32 · Reviewed 2026-09-21.** Design an information lifecycle and test controls without confusing labels, products and legal duties. Reuses M09/M19/M23, [governance](#/recurso/D31) and [browsing](#/recurso/D24). References I01–I13/S05–S06 are in [D36](#/recurso/D36). Not individual legal advice.

## 1. Data needs context and ownership

Information management covers identification, ownership, quality, sensitivity, purpose, access, use, retention, transfer and disposal. A computer inventory is not a data or processing inventory. Link service, dataset, location, copies, recipients, custodian and obligations.

Assign classification, permission implementation, disclosure approval and review. Technical custody does not automatically confer data ownership. A GDPR controller has a specific legal meaning, distinct from system administrator or service owner. Indefinite retention increases exposure; premature deletion can breach retention duties or destroy evidence.

## 2. Four different classification planes

| Plane | Purpose/authority | Example and limitation |
|---|---|---|
| Corporate classification | Organization-approved policy | Public, internal, confidential and restricted are teaching labels, not universal legal categories |
| Officially classified information | Specific legal regimes and procedures | ONS/CNI, EU and NATO arrangements require appropriate authority and handling, not merely file labels |
| US CUI | Unclassified information with defined safeguarding/dissemination requirements | NARA maintains the program/registry; it is not an interchangeable corporate label |
| TLP | Originator-defined sharing boundaries | FIRST TLP 2.0 does not replace formal classification, licences or encryption rules |

FIRST uses TLP:RED, TLP:AMBER, TLP:GREEN and TLP:CLEAR; AMBER+STRICT further restricts sharing to the organization. Keep original labels and check dissemination rules. TLP alone does not authorize disclosure of personal data [I01]. ENS low/medium/high categories concern evaluated systems, not universal document secrecy labels [S05].

Use CNI/ONS, EU and NARA sources for their own scope; do not map corporate confidential automatically to EU CONFIDENTIAL [I02–I04]. CCN-CERT/CISA operational guidance needs a specific document, audience, version and authority. There is no single universal «CCN/CNI/CISA/EU» classification scheme.

## 3. Original corporate handling example

| Teaching level | Access/distribution | Storage, transfer and disposal |
|---|---|---|
| Approved public | Publication with ownership and review | Integrity, version and usage rights still apply |
| Internal | Authorized personnel by function | Managed repositories, approved external sharing and retention |
| Confidential | Need-to-know and owner approval | Reviewed groups, appropriate encryption, verified recipients and proportionate logs |
| Restricted | Named/attribute-based authorization and frequent review | Approved environment/channels, time-limited access, egress controls and tested recovery |

This is a synthetic policy. Define exceptions, reclassification, compound documents, exports, copies and metadata. Filenames or patterns alone cannot reliably determine sensitivity. Link labels to handling rules; a color without an operational effect does not protect data.

## 4. DLP requires policy, placement and coverage

DLP can discover sensitive content, recognize labels and apply actions on supported channels. Distinguish detection, warning, justification, blocking and response. A match is not proof of leakage, and no alert does not prove universal coverage. Design positive/negative checks using fictitious data.

Microsoft Purview Endpoint DLP supports documented platforms and activities, with Windows/macOS differences [I05]. Intune manages devices/applications and can support deployment/posture; it is not the entire Purview DLP capability [I06]. Forcepoint DLP and Broadcom Symantec DLP offerings provide commercial examples; check edition, licence, OS, channel and sensor [I07–I08].

Microsoft Presidio supplies sensitive-data analysis and anonymization/redaction components, not a complete email/endpoint/cloud enforcement platform by itself [I09]. Use it for synthetic-text classification exercises. A library, rule engine and enterprise suite are not equivalent products.

Test record: channel, app, user, device, data type, allowed/denied action, expected event, exception, owner and rollback. Include USB, email, web upload and synchronization only when actually supported. Do not use students' personal accounts or real personal data.

## 5. Encryption layers

At-rest encryption protects media/data under defined conditions; transport encryption protects a channel; end-to-end encryption aims to restrict content access to authorized endpoints. TLS termination does not necessarily expose an independently E2EE-protected payload. An unlocked session can read data despite disk encryption.

Manage approved configurations, keys, recovery, revocation and access. Separate volume, file-container and application encryption. BitLocker, FileVault, LUKS/dm-crypt and VeraCrypt address different environments and modes: verify support and local documentation. Never enable encryption without custodial and recovery planning. BitLocker protects Windows volumes, not all permissions, egress or unlocked-session behavior [I10]. VeraCrypt modes and limitations must be selected for the case [I11].

Use disposable virtual volumes and synthetic files, never the only working disk. Verify backups and restore elsewhere. Recovery keys must not enter Git or screenshots. Cryptographic erasure and media sanitization require suitable procedures; ordinary file removal does not prove physical sanitization.

## 6. Privacy law and workplace monitoring

Establish scope, purpose, legal basis, minimization, recipients, retention and rights before monitoring. GDPR, Spain's LOPDGDD, LSSI and sector rules address different issues; technical conformity is not universal legal compliance [S06, I12–I13]. LOPDGDD article 87 concerns privacy and digital devices at work, including usage criteria and informing workers [I12].

TLS inspection, captures and logs may process sensitive content. Assess necessity, proportionality, exclusions, administrator access, retention and privacy/legal review. Employee consent is not a universal shortcut. Do not install inspection CAs on personal devices outside a legitimate, transparent and authorized arrangement. Exercises use synthetic data, not covert surveillance.

## 7. Information incidents and restoration

For an incorrectly shared synthetic document, record known version, recipients, confirmed/potential access, permissions and available logs. Restrict access while preserving evidence and involve communication owners. Revoking a link does not guarantee deletion of downloaded copies.

Recovery includes content, consistency, permissions and service checks. Separate backups, synchronization and forensic preservation. Useful metrics include datasets with owners/retention, reviewed access, actual DLP coverage, false positives and tested restores.

## Exercises and self-checks

**INT-L13: classification and handling.** Classify twelve fictional documents, including a brochure, inventory, synthetic payroll, non-secret configuration and TLP alert. Identify applicable scheme, owner, recipients and retention; explain three ambiguous decisions. Evidence: matrix and exception. Success: no automatic TLP/legal or ENS/document-label equivalence.

**INT-L14: data-protection acceptance.** On a disposable volume/folder, verify allowed/denied reads, selected encryption and restoration. Classify synthetic DLP events as true/false positives. Evidence: checks, minimized logs and recovery. Success: no key disclosure and no claim to have tested unavailable products.

Self-check: does BitLocker alone prevent an authenticated user emailing a readable file? No: examine permissions, channel and egress policy. Does TLP:CLEAR mean no copyright or personal data? No. Is Intune a full DLP substitute? No: describe the actual capabilities and coverage.
