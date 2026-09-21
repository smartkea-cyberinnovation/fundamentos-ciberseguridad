<!-- ES -->
# Profesiones TIC y ciberseguridad: tareas, evidencias y mercado

**Lectura D34 · Corte documental 2026-09-21.** Objetivo: comprender quién construye, opera y protege cada componente y preparar un portfolio demostrable. Las taxonomías y correspondencias siguientes son elaboración docente, no un listado universal de todos los títulos laborales. Fuentes C01–C06 en [D36](#/recurso/D36).

## 1. No confundir puesto, función y competencia

Un nombre como «ingeniero de seguridad» puede cubrir tareas distintas entre empresas. Define objeto de trabajo, decisiones, dependencias, entregables y nivel de autonomía. Una persona puede ejercer varias funciones; un equipo puede repartir un mismo rol. Las certificaciones son evidencia parcial de aprendizaje, no garantía de experiencia o empleo.

El marco ECSF de ENISA describe doce perfiles profesionales; NICE ofrece un lenguaje de tareas, conocimientos y habilidades. Son referencias complementarias, no árboles intercambiables ni equivalencias automáticas con una oferta [C05–C06]. Relacionar CSF con un puesto significa explicar qué resultados ayuda a conseguir, no afirmar una acreditación NIST.

## 2. Árbol funcional de informática

| Familia | Ejemplos de puestos | Objeto y entrega verificable |
|---|---|---|
| Soporte y puesto digital | Service desk, soporte de campo, EUC, UEM/MDM, accesibilidad | Equipo utilizable, incidencia resuelta, perfil y acceso documentados |
| Sistemas y plataforma | Sysadmin Linux/Windows/macOS, ingeniero de plataforma, virtualización | Configuración reproducible, servicio y restauración |
| Redes y comunicaciones | Redes LAN/WAN, Wi-Fi, telecomunicaciones, voz | Flujos, disponibilidad, segmentación y diagnóstico |
| Centro de datos y hardware | Técnico DC, almacenamiento, firmware, hardware/embedded | Inventario, mantenimiento, capacidad y recuperación |
| Cloud e infraestructura | Cloud engineer, arquitecto cloud, IaC, FinOps | Arquitectura, coste, identidad y automatización revisadas |
| Software y producto | Frontend/backend/full-stack, móvil, embedded, analista funcional | Código y requisitos con pruebas y documentación |
| Calidad y entrega | QA, automatización de pruebas, DevOps, release engineer | Pipeline, artefactos y criterios de aceptación |
| Fiabilidad y operación | SRE, observabilidad, incident commander, continuidad TI | SLO, alertas útiles, runbook y recuperación |
| Datos | DBA, data engineer, analytics, BI, data architect/steward | Modelo, calidad, lineage, permisos y respaldo |
| IA y cómputo avanzado | ML engineer, MLOps, científico de datos, HPC, investigación cuántica | Evaluación, datos/modelo versionados y límites |
| Arquitectura e integración | Enterprise/solution architect, integración/API, ERP/CRM | Decisiones, contratos y dependencias |
| Gestión y relación con negocio | Product/project/service manager, consultoría, preventa, formación | Prioridad, requisitos, comunicación y aceptación |

Hay especialidades y títulos locales no enumerados. Este árbol cubre objetos de trabajo para estudiar relaciones, no una estadística exhaustiva. «Senior» o «lead» requieren alcance y autonomía explícitos; no se deducen de años o número de herramientas.

## 3. Árbol de ciberseguridad conectado con informática

| Familia de seguridad | Qué revisa/protege de TI | Funciones CSF principales y evidencia |
|---|---|---|
| Gobierno/CISO/GRC | Decisiones, obligaciones, riesgos y terceros | Govern/Identify; políticas, escenarios, aceptación y seguimiento |
| Arquitectura de seguridad | Diseños e interconexiones | Identify/Protect; modelos de amenazas y decisiones |
| IAM/IGA/PAM | Personas, workloads, accesos y privilegios | Govern/Protect; lifecycle, revisiones y revocación |
| Seguridad de endpoint | Sistemas, móviles y perfiles | Protect/Detect; baseline, cobertura y pruebas |
| Seguridad de red | Flujos, WAN, acceso remoto y radio | Protect/Detect; segmentación y telemetría |
| Cloud/platform/container security | Infraestructura cloud, IaC, clústeres | Identify/Protect/Detect; políticas y evidencia de configuración |
| AppSec/product security/DevSecOps | Código, API, dependencias y entrega | Protect/Detect; requisitos, revisión y retest |
| Seguridad de datos/privacidad técnica | Datos, cifrado, acceso y salida | Govern/Protect; clasificación, controles y límites de tratamiento |
| SOC/detection engineering | Telemetría de sistemas/red/aplicación | Detect/Respond; reglas, triaje y escalado |
| Respuesta y DFIR | Incidentes, evidencia y recuperación confiable | Respond/Recover; cronología, alcance y restauración |
| CTI/exposición/vulnerabilidades | Amenazas y condiciones relevantes | Identify/Detect; confianza, priorización y recomendación |
| Evaluación autorizada/Purple Team | Eficacia de controles y superficie | Identify/Protect/Detect; alcance, prueba benigna y mejora |
| OT/IoT/embedded/seguridad física | Procesos industriales, dispositivos y entorno | Protect/Detect/Recover; disponibilidad y seguridad operacional |
| Continuidad, crisis y resiliencia | Dependencias de negocio y servicios | Govern/Respond/Recover; BIA, ejercicios y decisiones |
| Auditoría, formación e investigación | Criterios, competencias y nuevos métodos | Transversal; independencia, resultados y límites |

La asignación es muchos-a-muchos: una misma tarea puede contribuir a más de una función. El DPD tiene independencia y funciones legales propias; no debe convertirse automáticamente en responsable de toda operación de seguridad. No todos los puestos ciber son ofensivos ni requieren empezar por una herramienta de ataque.

## 4. Mercado: separar población, fecha y tipo de cifra

| Territorio y fuente | Dato observado o proyectado | Interpretación permitida |
|---|---|---|
| España, ONTSI [C01] | 4,8 % de especialistas TIC sobre empleo en 2025, frente a 5,0 % UE | Indicador de empleo TIC, no número de vacantes ciber |
| UE, Eurostat [C02] | Aproximadamente 10,45 millones de especialistas TIC en 2025; 5,0 % del empleo | Población TIC y año definidos; no todos son profesionales de ciberseguridad |
| EE. UU., BLS [C03] | Proyección de +21 % para information security analysts en 2025–2035 y unas 14.100 aperturas anuales medias | Proyección de una ocupación; las aperturas incluyen reemplazos y no son un conteo de anuncios hoy |
| Global, OIT [C04] | Estudio de exposición ocupacional a IA generativa publicado en 2025 | Exposición de tareas no equivale a empleos eliminados ni a una predicción individual |

No combinar porcentajes de países, años o denominadores distintos en un ranking. Una cifra de «brecha de talento» no es idéntica a vacantes financiadas. Salarios requieren país, moneda, fecha, experiencia, contrato, impuestos y muestra; esta edición no promete remuneraciones.

## 5. IA: oportunidades, riesgos y aprendizaje

La IA puede apoyar documentación, clasificación, generación de pruebas y análisis de datos sintéticos; también puede introducir errores, dependencia de proveedor, fuga de datos y pérdida de capacidad de revisión. La oportunidad profesional no consiste solo en pedir scripts: definir contratos, comprobar resultados y asumir responsabilidad siguen siendo tareas relevantes.

Evalúa por tarea: qué se automatiza, qué error tolera, quién revisa, qué dato sale y cómo se mide coste/calidad. El estudio OIT mide exposición potencial y destaca transformación de tareas; no autoriza a inferir el futuro de un alumno [C04]. No confundir productividad de una demo con operación segura repetida.

## 6. Itinerarios y portfolio

Entrada común: representación, hardware, SO, terminal, redes, datos, identidad y seguridad. Después profundiza según objeto: sistemas/plataforma; desarrollo/AppSec; datos/privacidad; SOC/DFIR; gobierno/riesgos; cloud/redes. No es necesario dominar todas las especialidades antes de optar a una posición inicial.

Portfolio privado por defecto: inventario sintético, script probado, matriz de acceso, diagrama de red, baseline con excepción, búsqueda de logs, restauración y explicación ejecutiva. Publicar solo tras eliminar secretos/datos de terceros y revisar licencia. Documenta qué está diseñado, ejecutado, simulado o pendiente. Un proyecto pequeño reproducible vale como evidencia concreta; una lista de marcas no demuestra dominio.

## Prácticas y criterios

**INT-L17: mapa de una oferta.** Elige dos ofertas públicas con fecha. Extrae tareas, objeto, conocimientos, autonomía, requisitos y condiciones sin guardar contactos personales. Relaciona con TI/ciber y un resultado CSF. Evidencia: matriz y tres habilidades demostrables. Éxito: distinguir requisito obligatorio, deseable y comercial, sin convertir la oferta en una estadística de todo el mercado.

**INT-L18: entrega técnica y ejecutiva.** Presenta una práctica existente en cinco minutos: problema, decisión, prueba, fallo encontrado, recuperación y límite. Un compañero reproduce una parte. Evidencia: README, resultados y revisión. Éxito: explicar sin depender de IA ni atribuir pruebas no realizadas.
<!-- EN -->
# ICT and cybersecurity careers: tasks, evidence and the market

**Reading D34 · Evidence cut-off 2026-09-21.** Understand who builds, operates and protects components, and create a demonstrable portfolio. The following taxonomies/mappings are teaching interpretations, not a universal list of every job title. Sources C01–C06 are in [D36](#/recurso/D36).

## 1. Job, function and competence differ

«Security engineer» can describe different work across organizations. Specify work objects, decisions, dependencies, deliverables and autonomy. One person can perform several functions and a team can share one role. Certifications provide partial learning evidence, not guaranteed experience or employment.

ENISA ECSF describes twelve professional profiles; NICE supplies a language of tasks, knowledge and skills. They complement rather than automatically translate into each other or into job adverts [C05–C06]. Mapping a role to CSF explains contributed outcomes, not NIST accreditation.

## 2. Functional ICT tree

| Family | Example roles | Work object and verifiable delivery |
|---|---|---|
| Support/digital workplace | Service desk, field support, EUC, UEM/MDM, accessibility | Usable endpoint, resolved ticket, documented profile/access |
| Systems/platform | Linux/Windows/macOS admin, platform engineer, virtualization | Reproducible configuration, service and restore |
| Networking/communications | LAN/WAN, Wi-Fi, telecoms, voice | Flows, availability, segmentation and diagnosis |
| Data center/hardware | DC technician, storage, firmware, embedded | Inventory, maintenance, capacity and recovery |
| Cloud/infrastructure | Cloud engineer/architect, IaC, FinOps | Reviewed architecture, cost, identity and automation |
| Software/product | Frontend/backend/full-stack, mobile, embedded, analyst | Code/requirements with tests and documentation |
| Quality/delivery | QA, test automation, DevOps, release engineer | Pipeline, artifacts and acceptance |
| Reliability/operations | SRE, observability, incident command, IT continuity | SLOs, useful alerts, runbooks and recovery |
| Data | DBA, data engineer, analytics, BI, architect/steward | Model, quality, lineage, access and backups |
| AI/advanced compute | ML engineer, MLOps, data scientist, HPC, quantum research | Evaluations, versioned data/models and limitations |
| Architecture/integration | Enterprise/solution architect, API, ERP/CRM | Decisions, contracts and dependencies |
| Management/business interface | Product/project/service manager, consulting, presales, teaching | Priorities, requirements, communication and acceptance |

Specializations and local titles extend this tree. It organizes work objects rather than claiming an exhaustive statistic. Seniority needs defined scope and autonomy, not merely years or tool counts.

## 3. Security tree linked to ICT

| Security family | ICT object protected/reviewed | Main CSF functions and evidence |
|---|---|---|
| Governance/CISO/GRC | Decisions, duties, risk and suppliers | Govern/Identify; policy, scenarios and acceptance |
| Security architecture | Designs/interconnections | Identify/Protect; threat models and decisions |
| IAM/IGA/PAM | People, workloads and privileges | Govern/Protect; lifecycle and revocation |
| Endpoint security | Systems, phones and profiles | Protect/Detect; baselines and coverage |
| Network security | Flows, WAN, remote/radio access | Protect/Detect; segmentation and telemetry |
| Cloud/platform/container security | IaC, cloud infrastructure and clusters | Identify/Protect/Detect; policy and configuration evidence |
| AppSec/product security/DevSecOps | Code, APIs, dependencies and delivery | Protect/Detect; requirements, review and retest |
| Data security/privacy engineering | Data, encryption, access and egress | Govern/Protect; classification and processing limits |
| SOC/detection engineering | Host/network/application telemetry | Detect/Respond; rules, triage and escalation |
| Response/DFIR | Incidents, evidence and trusted recovery | Respond/Recover; timeline, scope and restore |
| CTI/exposure/vulnerabilities | Relevant threats and conditions | Identify/Detect; confidence and prioritization |
| Authorized assessment/Purple Team | Control effectiveness and surface | Identify/Protect/Detect; scope, benign tests and improvements |
| OT/IoT/embedded/physical security | Industrial processes, devices and environment | Protect/Detect/Recover; availability and operational safety |
| Continuity/crisis/resilience | Business/service dependencies | Govern/Respond/Recover; BIA, exercises and decisions |
| Audit, education and research | Criteria, skills and methods | Cross-cutting; independence, results and limitations |

Mappings are many-to-many. A DPO has distinct legal functions and independence; do not automatically assign every security operation to that role. Cybersecurity careers are not all offensive and need not begin with attack tools.

## 4. Market evidence: population, date and measure

| Region/source | Observed or projected measure | Valid interpretation |
|---|---|---|
| Spain, ONTSI [C01] | ICT specialists were 4.8 % of employment in 2025, versus 5.0 % EU | ICT employment, not cybersecurity vacancies |
| EU, Eurostat [C02] | Approximately 10.45 million ICT specialists in 2025; 5.0 % of employment | Defined population/year, not all cybersecurity staff |
| USA, BLS [C03] | Information security analyst employment projected +21 % in 2025–2035; around 14,100 annual openings on average | Projection for one occupation; openings include replacement, not today's advert count |
| Global, ILO [C04] | Occupational exposure study for generative AI, published 2025 | Task exposure is not job loss or an individual forecast |

Do not combine different years, populations and denominators into a ranking. A talent-gap estimate is not funded vacancies. Salary comparisons require location, currency, date, experience, contract and sample; no salaries are promised here.

## 5. AI and professional development

AI can support documentation, classification, test generation and synthetic-data analysis; it can also introduce errors, vendor dependence, disclosure and weakened review skills. Professional value is not merely prompting for scripts: contracts, verification and accountability remain necessary.

Evaluate tasks: what is automated, what error is acceptable, who reviews, what data leaves and how quality/cost are measured. ILO exposure analysis concerns potential task transformation, not an individual student's future [C04]. A productive demonstration does not establish safe repeatable operations.

## 6. Pathways and portfolio

Common foundations: representation, hardware, OS, terminal, networks, data, identity and security. Specialize by work object: systems/platform; development/AppSec; data/privacy; SOC/DFIR; governance/risk; cloud/networking. An entry role does not require prior mastery of every specialty.

Default to a private portfolio: synthetic inventory, tested script, access matrix, network diagram, baseline/exception, log query, restore and executive explanation. Review secrets, third-party data and licences before publication. Label designed, executed, simulated and pending work accurately. A small reproducible project is concrete evidence; a brand list is not competence.

## Exercises and criteria

**INT-L17: map a job advert.** Choose two dated public adverts. Extract tasks, objects, knowledge, autonomy, requirements and conditions without retaining personal contact details. Map to ICT/security and a CSF outcome. Evidence: matrix and three demonstrable skills. Success: distinguish mandatory, desirable and promotional wording; do not generalize two adverts to the whole market.

**INT-L18: technical/executive handover.** Explain an existing lab in five minutes: problem, decision, test, observed failure, recovery and limitation. A peer reproduces part. Evidence: README, results and review. Success: explain independently of AI and claim only tests actually performed.
