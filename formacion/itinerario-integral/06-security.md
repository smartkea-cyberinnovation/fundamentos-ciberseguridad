<!-- ES -->
# Seguridad: propiedades, marcos y organización del trabajo

**Lectura D31.** Objetivo: convertir necesidades de seguridad en responsables, controles y evidencias. Referencias S01–S06 en [D36](#/recurso/D36). Complementa M27–M30 y el plan maestro; las correspondencias son docentes y parciales, no certificación ni asesoramiento jurídico individual.

## 1. Seguridad empieza por objetivos

La confidencialidad limita divulgación a sujetos autorizados; la integridad protege frente a cambios o destrucción indebidos; la disponibilidad permite acceso y uso oportunos. CIA no es una lista de productos. Añade autenticidad, trazabilidad y resiliencia según contexto. La privacidad requiere además finalidad legítima, transparencia y derechos: no se agota en secreto.

Ejemplo docente: una nómina debe ser accesible para su titular, no modificable por cualquiera y disponible cuando se necesita. Cifrarla sin conservar la clave puede proteger confidencialidad y destruir disponibilidad. La decisión exige equilibrar propiedades y responsabilidades, no maximizar un único control.

## 2. Amenaza, vulnerabilidad, riesgo y evidencia

Una amenaza puede ser maliciosa, accidental, ambiental o de proveedor. Una vulnerabilidad es una debilidad relevante para un escenario; su presencia no acredita explotación. El riesgo relaciona incertidumbre, probabilidad/frecuencia y consecuencias sobre objetivos. Evento, alerta e incidente son categorías diferentes y exigen criterios de interpretación.

Escribe el escenario: «un acceso no revocado permite modificar una cuenta de pago y produce pérdida financiera». Relaciona activo, actor/causa, condición, consecuencia, controles y dueño. Separa estado inherente, controles actuales y tratamiento objetivo. Un porcentaje de reducción sin prueba no es eficacia observada. El ejemplo del plan maestro permite practicar aritmética sin atribuirla a una empresa real.

## 3. NIST CSF como lenguaje de resultados

CSF 2.0 agrupa resultados en Govern, Identify, Protect, Detect, Respond y Recover [S01]. No son fases que se ejecutan una vez ni seis departamentos obligatorios. Un perfil actual/objetivo ayuda a decidir qué mejorar; los Tiers describen características de gestión, no una certificación universal de madurez.

| Función | Pregunta | Ejemplo de resultado y evidencia docente |
|---|---|---|
| Govern | ¿Quién decide y con qué criterios? | Política, dueños, riesgo aceptado y seguimiento |
| Identify | ¿Qué importa y de qué depende? | Servicios, activos, datos, terceros y escenarios |
| Protect | ¿Cómo se reduce la exposición? | Acceso mínimo, configuración, formación y pruebas |
| Detect | ¿Cómo se reconoce una anomalía? | Fuentes, reglas, cobertura y falsos positivos |
| Respond | ¿Cómo se analiza y limita impacto? | Triaje, autoridad de contención y comunicaciones |
| Recover | ¿Cómo se restablece de forma confiable? | Copia restaurada, dependencias y validación del servicio |

Una compra puede apoyar varios resultados; no equivale a cumplirlos. CSF no prescribe una marca ni convierte una puntuación de dashboard en garantía.

## 4. Equipo y flujo: asignar autoridad, no solo nombres

| Equipo/función | Trabajo principal | Dependencia y evidencia |
|---|---|---|
| Dirección y dueño de servicio/riesgo | Prioridad, recursos y aceptación | Impacto de negocio y decisiones documentadas |
| CISO/GRC | Gobierno, criterios, controles y coordinación | Inventarios, políticas, riesgos y excepciones |
| Arquitectura/ingeniería | Diseño seguro y patrones | Flujos, amenazas y revisiones de cambios |
| Sistemas/redes/cloud | Operación, parches y recuperación | Baselines, logs, disponibilidad y rollback |
| IAM/IGA/PAM | Ciclo de vida y privilegios | Aprobación, acceso efectivo y revocación |
| Desarrollo/AppSec/DevSecOps | Requisitos, código y entregas | Pruebas, componentes, secretos y retest |
| SOC/detection engineering | Visibilidad, detección y triaje | Reglas, fuentes, cobertura y casos escalados |
| CSIRT/DFIR/CTI | Respuesta, evidencia e inteligencia | Cronología, alcance, confianza y recomendaciones |
| Privacidad/legal | Obligaciones y riesgos para personas | Finalidad, evaluación y decisiones de tratamiento |
| Continuidad/comunicación | Recuperación y mensajes autorizados | BIA, pruebas, plan y lecciones |
| Auditoría | Evaluación respecto de criterios | Independencia apropiada y evidencias verificadas |

NIST SP 800-61 Rev. 3 integra preparación y respuesta con gestión del riesgo [S02]. Flujo docente: alerta→triaje→decisión de incidente→responsable→contención aprobada→investigación→recuperación→revisión. Hay bucles y trabajo paralelo. Un analista no debe aislar indiscriminadamente servicios críticos sin autoridad y valoración de impacto.

## 5. Documentos que no deben confundirse

Política: qué se exige y quién lo aprueba. Estándar interno: requisito concreto. Procedimiento: pasos y responsabilidades. Guía: recomendaciones contextualizadas. Playbook: decisiones y acciones de un escenario. Control: medida con objetivo, alcance, dueño e implementación. Evidencia: observación que sustenta una afirmación durante un periodo. Registro de excepción: desviación autorizada, riesgo, compensación, responsable y caducidad.

Ejemplo: «acceso de mínimo privilegio» es dirección. «La cuenta de servicio solo lee el directorio X» es requisito. Alta/aprobación/asignación/prueba/revisión es procedimiento. La prueba de denegación y su log son evidencia. El grupo llamado «seguro» no prueba nada por sí mismo.

## 6. CIS, ISO, NIST, ENS y RGPD

CIS Controls agrupa salvaguardas; CIS Benchmarks desarrolla referencias de configuración para productos/versiones [S03]. No aplicar todos los ajustes sin analizar función, impacto y recuperación. ISO/IEC 27001 establece requisitos de un sistema de gestión y su selección de controles se justifica; disponer de un documento no certifica la organización [S04]. No se reproduce la norma protegida ni se inventan identificadores de controles.

ENS categoriza sistemas y ajusta medidas al ámbito y a impactos sobre sus dimensiones; una categoría del sistema no es la etiqueta de un archivo. El RGPD regula tratamiento de datos personales y añade obligaciones que no se deducen de un benchmark técnico [S05–S06]. Una evidencia puede reutilizarse en varias revisiones, pero las equivalencias no son automáticas. NIST publica marcos/guías con finalidades distintas: CSF, NICE y SP 800-53 no son el mismo documento.

## 7. Medición útil y falsas seguridades

Define denominador y cobertura: «95 % parcheado» de qué equipos, con qué antigüedad, fuente y excepciones. Diferencia KPI operativo y KRI de riesgo. Más alertas no prueban mejor detección; cero incidentes registrados puede señalar poca visibilidad. Mide también restauraciones, tiempo hasta revocar accesos, controles sin dueño y fuentes que dejaron de emitir.

Una puntuación no sustituye evidencia. El control puede estar diseñado, implantado, operativo o probado; registra el estado real. La aceptación de un riesgo exige autoridad y revisión, no una casilla verde automática.

## Prácticas y rúbrica

**INT-L11: RACI de un incidente sintético.** Se detecta un cambio no previsto de permisos en una carpeta de práctica. Asigna quién analiza, autoriza contención, comunica, restaura y acepta el servicio. Evidencia: flujo, RACI sin ambigüedad de aprobación y dos fuentes de corroboración. Éxito: distinguir dueño de datos, administrador y auditor; no atribuir una persona solo por su cuenta.

**INT-L12: del requisito a la prueba.** Elige cinco resultados de la tabla CSF y relaciona riesgo, control, implementación, evidencia, propietario y excepción. Evidencia: matriz y prueba positiva/negativa diseñada. Éxito: no declarar conformidad con ISO/ENS/RGPD solo porque haya una correspondencia. Recuperación: ejercicio con datos sintéticos, sin cambios empresariales.

Rúbrica común: comprensión 25 %, decisión técnica 25 %, evidencia 25 %, límites y recuperación 25 %. Es una rúbrica docente, no un esquema de certificación externa.
<!-- EN -->
# Security: properties, frameworks and work organization

**Reading D31.** Turn security needs into owners, controls and evidence. References S01–S06 are in [D36](#/recurso/D36). Complements M27–M30 and the master plan. Mappings are partial teaching interpretations, not certification or individual legal advice.

## 1. Security starts with objectives

Confidentiality restricts disclosure to authorized subjects; integrity protects against improper change/destruction; availability supports timely access and use. CIA is not a list of products. Include authenticity, traceability and resilience where appropriate. Privacy also concerns legitimate purpose, transparency and rights, not merely secrecy.

Teaching example: payroll should be available to its recipient, resistant to unauthorized changes and accessible when needed. Encrypting it while losing the key may protect confidentiality but destroy availability. Decisions balance properties and responsibilities rather than maximizing one control.

## 2. Threats, vulnerabilities, risk and evidence

Threats can be malicious, accidental, environmental or supplier-related. A vulnerability is a weakness relevant to a scenario, not proof of exploitation. Risk relates uncertainty, probability/frequency and consequences for objectives. Events, alerts and incidents require different interpretation criteria.

Write a scenario: «unrevoked access permits changing a payment account and causes financial loss». Connect assets, actor/cause, conditions, consequences, controls and ownership. Separate inherent baseline, current controls and target treatment. Unsupported reduction percentages are not measured effectiveness. The master-plan numerical case permits arithmetic practice without claiming company-specific estimates.

## 3. NIST CSF as an outcome language

CSF 2.0 organizes outcomes into Govern, Identify, Protect, Detect, Respond and Recover [S01]. These are neither one-time phases nor six mandatory departments. Current/target profiles support priorities; Tiers describe management characteristics, not universal maturity certification.

| Function | Question | Teaching outcome/evidence |
|---|---|---|
| Govern | Who decides, against which criteria? | Policy, ownership, risk acceptance and follow-up |
| Identify | What matters and depends on what? | Services, assets, data, suppliers and scenarios |
| Protect | How is exposure reduced? | Minimum access, configuration, training and checks |
| Detect | How are anomalies recognized? | Sources, rules, coverage and false positives |
| Respond | How is impact analyzed and limited? | Triage, containment authority and communications |
| Recover | How is service restored confidently? | Restored backup, dependencies and service checks |

Purchases can support outcomes without satisfying them automatically. CSF does not prescribe brands or convert dashboards into guarantees.

## 4. Teams and flows require authority

| Team/function | Main work | Dependencies/evidence |
|---|---|---|
| Leadership/service and risk owner | Priorities, resources and acceptance | Business impact and recorded decisions |
| CISO/GRC | Governance, criteria, controls and coordination | Inventories, policies, risks and exceptions |
| Architecture/engineering | Secure design and patterns | Flows, threat models and change reviews |
| Systems/network/cloud | Operation, patching and recovery | Baselines, logs, availability and rollback |
| IAM/IGA/PAM | Lifecycle and privileges | Approval, effective access and revocation |
| Development/AppSec/DevSecOps | Requirements, code and delivery | Tests, components, secrets and retests |
| SOC/detection engineering | Visibility, detection and triage | Rules, sources, coverage and escalations |
| CSIRT/DFIR/CTI | Response, evidence and intelligence | Timeline, scope, confidence and recommendations |
| Privacy/legal | Duties and risks to people | Purpose, assessments and processing decisions |
| Continuity/communications | Recovery and authorized messages | BIA, exercises, plans and lessons |
| Audit | Evaluation against criteria | Appropriate independence and verified evidence |

NIST SP 800-61 Rev. 3 connects preparation/response with risk management [S02]. Teaching flow: alert→triage→incident decision→owner→authorized containment→investigation→recovery→review. Feedback loops and parallel work matter. Analysts should not indiscriminately isolate critical services without authority and impact assessment.

## 5. Different documents, different purposes

Policy states approved expectations. An internal standard specifies requirements. A procedure describes steps and ownership. Guidance provides contextual recommendations. A playbook supports scenario decisions/actions. A control has an objective, scope, owner and implementation. Evidence supports a claim over a stated period. Exceptions need authorization, risk, compensating measures, ownership and expiry.

Example: «least privilege» is direction; «this service account may only read directory X» is a requirement; request/approval/assignment/test/review is a procedure; a denied operation and its log provide evidence. A group named «secure» proves nothing on its own.

## 6. CIS, ISO, NIST, ENS and GDPR

CIS Controls groups safeguards; CIS Benchmarks provides product/version configuration references [S03]. Do not apply every setting without considering purpose, impact and recovery. ISO/IEC 27001 defines information-security management requirements and justified control selection; owning a document does not certify an organization [S04]. Protected standards are not reproduced and control numbers are not invented.

ENS categorizes systems and adjusts measures to scope and impact dimensions; a system category is not a document label. GDPR regulates personal-data processing and includes duties not derived from a technical benchmark [S05–S06]. Evidence can support several reviews without creating automatic equivalence. CSF, NICE and SP 800-53 have different purposes.

## 7. Useful measurement and false confidence

State denominators and coverage: «95 % patched» of which devices, as of when, from which source and with which exceptions? Separate operational KPIs and risk indicators. More alerts do not establish better detection; zero recorded incidents may indicate poor visibility. Include restore success, access-revocation delay, ownerless controls and missing telemetry sources.

Scores do not replace evidence. A control may be designed, implemented, operational or tested; record its actual state. Risk acceptance needs authority and review, not an automatic green checkbox.

## Exercises and rubric

**INT-L11: synthetic incident RACI.** An unexpected permission change occurs in a practice folder. Assign analysis, containment approval, communication, recovery and acceptance. Evidence: flow, unambiguous approval ownership and two corroborating sources. Success: distinguish data owner, administrator and auditor; do not identify a person solely from an account name.

**INT-L12: requirement to test.** Choose five CSF outcomes and connect risk, control, implementation, evidence, owner and exception. Evidence: matrix and designed positive/negative checks. Success: no ISO/ENS/GDPR compliance claim based merely on mapping. Recovery: synthetic exercise, no enterprise changes.

Common rubric: understanding 25 %, technical decision 25 %, evidence 25 %, limitations/recovery 25 %. This is an internal teaching rubric, not an external certification scheme.
