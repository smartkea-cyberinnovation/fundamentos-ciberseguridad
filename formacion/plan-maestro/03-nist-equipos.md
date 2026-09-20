# 03 · NIST CSF: funciones, equipos y operación

[Índice](README.md) · [Controles](04-controles-correspondencias.md) · [Riesgos](05-gestion-riesgos.md) · [Fuentes](09-fuentes.md)

## Qué se enseña del CSF 2.0

Usar el CSF como vocabulario de resultados de ciberseguridad: Core, funciones, categorías y subcategorías; perfil actual y objetivo; prioridades y contexto de riesgo. Sus seis funciones son concurrentes. El CSF no prescribe un organigrama ni obliga a comprar una familia de productos. Los Tiers caracterizan el rigor de las prácticas de gobierno/gestión del riesgo; no se convertirán en una nota automática de madurez o cumplimiento. [S01]

Las correspondencias, ejemplos y asignaciones de este documento son **elaboración pedagógica propia**. Las denominaciones en español se usan para enseñar y deben contrastarse con la traducción oficial si se necesita reproducirla literalmente. No se copia íntegramente el Core ni se adjudica aval de NIST al programa.

## Seis funciones y entregables observables

| Función | Pregunta del equipo | Ejemplo de responsabilidad | Entregable demostrable |
|---|---|---|---|
| GOVERN / Gobernar | ¿Qué importa, quién decide y cuánto riesgo aceptamos? | Dirección, CISO y propietarios de negocio | Política, criterios de riesgo, responsabilidades y revisión de proveedores |
| IDENTIFY / Identificar | ¿Qué tenemos y qué escenarios pueden afectarlo? | Activos, arquitectura, GRC y dueños de servicios | Inventario relacionado con criticidad, riesgos y dependencias |
| PROTECT / Proteger | ¿Cómo limitamos exposición e impacto? | IAM, sistemas, red, AppSec, datos y plataforma | Accesos mínimos, baseline, restauración, capacitación y pruebas |
| DETECT / Detectar | ¿Qué observamos y cuándo merece atención? | SOC, ingeniería de detección, CTI y operaciones | Cobertura de logs, reglas evaluadas, triaje y salud de sensores |
| RESPOND / Responder | ¿Cómo coordinamos y limitamos el incidente? | CSIRT, DFIR, operaciones, legal y comunicaciones | Caso de incidente, decisiones, contención y evidencia |
| RECOVER / Recuperar | ¿Cómo volvemos a un servicio confiable? | Negocio, continuidad y responsables de sistemas | Restauración verificada, prioridad de servicios y comunicación |

## Las 22 categorías en contexto

| ID | Concepto docente ES / EN | Ejemplo de actividad para aprender |
|---|---|---|
| GV.OC | Contexto organizativo / Organizational Context | Relacionar misión, partes interesadas y dependencias de un portal |
| GV.RM | Estrategia de riesgos / Risk Management Strategy | Definir umbral, escalado y periodicidad de revisión |
| GV.RR | Responsabilidades y autoridad / Roles, Responsibilities and Authorities | Identificar quién aprueba una excepción y quién opera el control |
| GV.PO | Política / Policy | Convertir una expectativa en política y procedimiento verificable |
| GV.OV | Supervisión / Oversight | Revisar resultados y corregir una desviación de objetivos |
| GV.SC | Riesgo de cadena de suministro / Cybersecurity Supply Chain Risk Management | Evaluar proveedor, dependencia y plan de salida |
| ID.AM | Activos / Asset Management | Vincular servicio, aplicación, equipo, identidad y datos |
| ID.RA | Evaluación de riesgos / Risk Assessment | Formular un escenario y sus consecuencias |
| ID.IM | Mejora / Improvement | Transformar una prueba fallida en una acción con responsable |
| PR.AA | Identidad, autenticación y acceso / Identity Management, Authentication and Access Control | Verificar alta, permiso y revocación |
| PR.AT | Concienciación y formación / Awareness and Training | Resolver un caso de decisión segura y medir comprensión |
| PR.DS | Seguridad de datos / Data Security | Clasificar, restringir y recuperar un conjunto ficticio |
| PR.PS | Seguridad de plataformas / Platform Security | Aplicar baseline y confirmar que el servicio funciona |
| PR.IR | Resiliencia de infraestructura / Technology Infrastructure Resilience | Analizar capacidad, continuidad técnica y fallo de dependencia |
| DE.CM | Monitorización continua / Continuous Monitoring | Comprobar recepción y pérdida de logs de un origen |
| DE.AE | Análisis de eventos adversos / Adverse Event Analysis | Correlacionar un indicio con contexto y decidir escalado |
| RS.MA | Gestión del incidente / Incident Management | Asignar severidad, autoridad y objetivos de respuesta |
| RS.AN | Análisis del incidente / Incident Analysis | Delimitar alcance con hipótesis y evidencias |
| RS.CO | Comunicación de respuesta / Incident Response Reporting and Communication | Redactar aviso interno con hechos y límites |
| RS.MI | Mitigación del incidente / Incident Mitigation | Elegir una contención proporcionada y comprobarla |
| RC.RP | Ejecución de recuperación / Incident Recovery Plan Execution | Restaurar un servicio y comprobar integridad y funcionalidad |
| RC.CO | Comunicación de recuperación / Incident Recovery Communication | Comunicar estado, restricciones y vuelta al servicio |

Los ejemplos no agotan las subcategorías ni sustituyen su texto. Para un perfil formal, cargar los identificadores exactos desde la edición oficial y mantener la versión de la fuente. [S01–S02]

## Catálogo de capacidades y equipos

| Capacidad | Trabajo ordinario y responsabilidad | Herramientas de ejemplo | Evidencia y métrica útil |
|---|---|---|---|
| Gobierno/GRC | Alcance, políticas, riesgos, excepciones, relación con auditoría | Registro versionado; PILAR para análisis MAGERIT según licencia; plataforma GRC evaluada por requisitos | Riesgos con dueño y tratamiento; excepciones vencidas |
| Inventario y arquitectura | Activos, servicios, flujos y dependencias | Consultas nativas, inventario JSON y repositorio de arquitectura | Cobertura con denominador conocido; activos sin responsable |
| IAM/PAM | Alta/cambio/baja, privilegios, acceso de servicios y emergencia | Directorio/IAM aprobado; herramientas nativas de SO; plataforma PAM como categoría | Prueba de revocación; cuentas privilegiadas sin revisión |
| Sistemas y endpoint | Parches, configuración, protección y recuperación | Herramientas nativas; Microsoft Defender for Endpoint como ejemplo comercial [S31] | Cumplimiento efectivo de baseline; latencia de remediación |
| Seguridad de red | Segmentación, exposición y diagnóstico | Firewall; Suricata y Zeek en funciones distintas [S26–S27] | Flujos justificados, cobertura de observación, cambios revisados |
| AppSec/DevSecOps | Diseño, código, dependencias y pipeline | Revisión Git; SAST/SCA/SBOM por categoría; CRS/WAF para otro nivel de control [S25] | Hallazgos corregidos/reabiertos; cobertura de revisión |
| SOC/detección | Ingestión, reglas, triaje y escalado | Microsoft Sentinel como ejemplo comercial; Zeek/Suricata como fuentes, no SIEM equivalentes [S26–S27, S30] | Tiempo de triaje por severidad; calidad/cobertura, no volumen bruto de alertas |
| CSIRT/DFIR | Coordinar, contener, investigar y preservar | Logs nativos, herramienta de casos elegida, parsers/forense autorizados | Decisiones registradas, evidencia reproducible, alcance conocido |
| CTI/hunting | Preguntas de inteligencia, contexto y búsquedas | MISP y OpenCTI [S28–S29]; consultas de logs | Indicadores con procedencia/vigencia; decisiones apoyadas |
| Continuidad/DR | BIA, copias, pruebas de restauración y crisis | Gestor de backup elegido, runbooks y ejercicios de mesa | Restauración conseguida frente a RPO/RTO |
| Datos/privacidad | Tratamientos, acceso, retención y derechos | Inventario de datos, registro de tratamientos y herramienta de evaluación | Cumplimiento de retención; trazabilidad de decisiones |
| Auditoría | Revisar diseño y eficacia sin operar el control auditado | Muestreo, entrevistas, consultas y evidencia verificable | Hallazgos sustentados y seguimiento independiente |

Es un modelo adaptable: una pequeña organización puede concentrar tareas en varias personas, sin perder separación de decisiones y supervisión. SOC L1/L2/L3 son convenciones organizativas, no funciones normativas de NIST. Un CSIRT interno, servicio gestionado o proveedor no desplaza automáticamente la responsabilidad de negocio. NICE y ECSF son referencias para perfilar competencias; esta tabla no equivale a una certificación de puestos. [S32]

## RACI mínimo para un caso de riesgo del portal

R = ejecuta; A = responde/aprueba; C = consultado; I = informado. Debe existir un A claro por decisión, aunque los roles puedan corresponder a la misma persona en un entorno pequeño. La adecuación de esa concentración debe analizarse.

| Decisión/tarea | Propietario del servicio | CISO/GRC | Plataforma/AppSec | SOC/CSIRT | Legal/DPD |
|---|---|---|---|---|---|
| Definir impacto y aceptar riesgo dentro de autoridad | A/R | C | C | I | C |
| Diseñar control y prueba | C | A | R | C | C |
| Aplicar cambio técnico aprobado | A | C | R | I | I |
| Triaje y propuesta de contención | C | C | C | A/R | C |
| Autorizar parada con impacto en negocio | A | C | R | R | C |
| Valorar obligaciones sobre datos personales | A | C | C | R para aportar hechos | C/R según responsabilidades formales |
| Restaurar y aceptar retorno al servicio | A | C | R | C | I |

El DPD asesora y supervisa en su ámbito; no debe convertirse por defecto en dueño del tratamiento, dueño técnico de todos los controles o decisor de negocio. La responsabilidad legal se determina por el rol y el tratamiento, no por esta tabla docente. [S07]

## KPI, KRI y sesgos

Definir numerador, denominador, origen, ventana, severidad, latencia y responsable. Ejemplos: porcentaje de activos críticos con logs recibidos en plazo; cambios de privilegios sin aprobación; restauraciones completas/ensayos; controles críticos cuya evidencia caducó; riesgos por encima de tolerancia sin plan.

Medir mediana y percentiles de tiempos cuando importe la cola; documentar cuándo comienza y termina el reloj. No utilizar una media de cierre de tickets para asegurar que los incidentes se contienen bien. Evitar clasificar como mejora una reducción de alertas que se deba a pérdida de ingestión.

## Ejercicio integrado

Partir de un servicio, escoger ocho resultados del CSF relevantes, definir estado actual/objetivo y evidencia, asignar responsable y propuesta de tratamiento, medir la situación y repetir una prueba tras un cambio. Entregar perfil y plan priorizado con supuestos. Una marca verde por existencia de un producto sin configuración o evidencia de uso no es aceptación.
