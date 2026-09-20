# 04 · Inventarios, controles y correspondencias CSF–RGPD–ISO–ENS

[Índice](README.md) · [Equipos](03-nist-equipos.md) · [Riesgos](05-gestion-riesgos.md) · [Fuentes](09-fuentes.md)

## Cuatro objetos distintos

**NIST CSF 2.0:** resultados para gestionar riesgo de ciberseguridad. **ISO/IEC 27001:2022:** requisitos de un sistema de gestión, incluyendo evaluación y tratamiento de riesgos; su anexo de referencia no debe separarse de los requisitos de gestión. **RGPD:** obligaciones sobre tratamientos de datos personales y derechos/libertades de las personas. **ENS:** requisitos y medidas para sistemas dentro de su ámbito, con categorización y aplicabilidad. Un certificado, una matriz o un perfil no reemplazan automáticamente ninguno de los otros. [S01, S05, S07, S08]

NIST publica referencias informativas propias y de terceros. Su presencia en OLIR no implica que NIST avale la exactitud de toda correspondencia externa. Registrar autor, versión, dirección, tipo de relación y fecha; no asumir simetría ni transitividad: A relacionado con B y B con C no acredita A equivalente a C. [S02]

## Modelo de información recomendado

Relacionar identificadores, no copiar todo en hojas inconexas:

`Servicio → activos/componentes → información/tratamientos → escenarios de riesgo → controles → implementaciones → pruebas/evidencias → hallazgos → decisiones y excepciones`.

Un control puede cubrir varios activos; una evidencia puede servir para varios requisitos, pero solo dentro de su alcance y vigencia. La misma política no demuestra la operación efectiva de un control en todos los sistemas.

| Inventario/registro | Campos mínimos |
|---|---|
| Servicios | ID, dueño, finalidad, usuarios, criticidad, dependencias, SLO, RPO/RTO |
| Activos | ID, servicio, tipo, dueño, ubicación, SO/versión, soporte, exposición y ciclo de vida |
| Software | Componente, versión, proveedor, licencia, procedencia, dependencias y mantenimiento |
| Identidades | ID, tipo humano/servicio, dueño, privilegios, caducidad y revisión; nunca secretos |
| Datos | Clasificación, origen, destino, conservación, acceso, ubicación y responsable |
| Tratamientos | Finalidad, categorías, base jurídica, destinatarios, conservación y medidas según aplicabilidad |
| Proveedores | Servicio, datos/accesos, criticidad, contrato, subcontratación, continuidad y salida |
| Riesgos | Escenario, activo, impacto, supuestos, estado inherente/actual/objetivo, dueño y decisión |
| Controles | Objetivo, tipo, dueño, alcance, implementación, prueba, evidencia y eficacia |
| Excepciones | Control, razón, impacto, compensación, aprobación, vencimiento y revisión |

El inventario de activos, la CMDB, el registro de tratamientos, el SBOM y la declaración de aplicabilidad son objetos relacionados pero diferentes. No deducir automáticamente la base jurídica de un tratamiento a partir de un inventario técnico. [S07]

## Correspondencia inicial de 12 familias

**Estado de todas las filas: propuesta pedagógica parcial, no equivalencia normativa ni conclusión de auditoría.** La columna ISO indica temas a contrastar con un ejemplar autorizado y con una referencia informativa versionada; deliberadamente no inventa citas de cláusulas o IDs no verificados. La columna ENS requiere revisar categoría, dimensiones, medidas y refuerzos aplicables del anexo II. Las citas RGPD identifican puntos de partida, no todas las obligaciones del tratamiento. [S02, S05, S07, S08]

| Familia | CSF: categorías de referencia | RGPD: artículos iniciales | ISO 27001: temas a verificar | ENS: ámbito de contraste | Evidencia reutilizable y límite |
|---|---|---|---|---|---|
| Gobierno y responsabilidad | GV.OC, GV.RR, GV.OV | 5.2, 24 | Contexto, liderazgo, roles y evaluación | Política, responsables y supervisión | Actas/política; no prueban aplicación técnica |
| Inventario y clasificación | ID.AM, PR.DS | 5, 30 cuando proceda | Inventario, información y clasificación | Activos, categorización y protección de información | Inventarios relacionados; CMDB no sustituye registro de tratamientos |
| Gestión de riesgos | GV.RM, ID.RA | 24, 25, 32, 35 cuando proceda | Evaluación/tratamiento de riesgos | Art. 14 y planificación | Escenarios, método y plan; riesgo empresarial no sustituye riesgo para personas |
| Identidad y acceso | PR.AA | 25, 32 | Identidades, autenticación y derechos | Control de acceso y mínimo privilegio | Prueba de alta/baja/revisión; no demuestra legitimidad del tratamiento |
| Configuración y vulnerabilidades | PR.PS, ID.RA | 32 | Configuración, cambios y vulnerabilidades | Integridad, actualización y explotación | Baseline y retest; versión instalada no basta |
| Cifrado y claves | PR.DS, PR.AA | 32.1.a | Criptografía y autenticación | Protección almacenada/en tránsito según aplicabilidad | Configuración y gestión de claves; cifrar no implica anonimizar |
| Redes y segmentación | PR.IR, DE.CM | 32 | Redes y separación | Interconexión, comunicaciones y monitorización | Flujos, reglas y pruebas; una VLAN no garantiza aislamiento efectivo |
| Registro y detección | DE.CM, DE.AE | 5.1.c/e, 32 | Logging y monitorización | Registro de actividad y monitorización | Eventos con tiempo/origen; proporcionalidad y conservación también importan |
| Incidentes | RS.MA, RS.AN, RS.CO, RS.MI | 33, 34 según condición | Preparación, respuesta y evidencia | Gestión y notificación de incidentes | Caso, decisiones y custodia; no toda alerta es una brecha notificable |
| Copias y recuperación | PR.DS, PR.IR, RC.RP | 32.1.b/c/d | Backup, continuidad y preparación TIC | Continuidad y copias, incluido mp.info.6 | Restauración y resultado medido; réplica no equivale a backup |
| Proveedores y cloud | GV.SC, GV.OC | 28, 32, 44–49 cuando proceda | Proveedores y servicios cloud | Servicios externos, requisitos contractuales y ámbito | Contrato y comprobación; una certificación ajena no cubre todo servicio |
| Desarrollo y privacidad por diseño | PR.PS, PR.DS, ID.RA | 25, 35 cuando proceda | Desarrollo seguro y pruebas | Adquisición/desarrollo y protección | Requisitos, revisión y pruebas; un escáner no demuestra cumplimiento |

## Cómo convertir una fila en una correspondencia verificable

1. Fijar versión y texto de origen/destino, alcance organizativo y sistema. Identificar si se relacionan resultado, obligación, control o evidencia.
2. Elegir el tipo de relación: contribuye, cubre parcialmente, coincide en tema, contiene o requiere otra condición. Dejar desconocido cuando no haya apoyo.
3. Escribir una justificación que señale qué parte queda cubierta y qué parte no. Registrar dirección de la relación.
4. Asociar implementación concreta y evidencia vigente: activo, entorno, periodo, método y revisor.
5. Revisar aplicabilidad y excepciones con los responsables pertinentes. Mantener decisión y caducidad.
6. Probar el control y revisar la correspondencia cuando cambie la norma, el servicio, la configuración o el tratamiento.

**Formato de registro:** mapping_id, source_framework, source_version, source_id, target_framework, target_version, target_reference, relation_type, direction, rationale, uncovered_requirements, scope, control_ids, evidence_ids, source_url, reviewed_at, reviewer y status.

## Ejemplo: revocación de un usuario

**Resultado perseguido:** impedir que una cuenta dada de baja siga accediendo al servicio. **Implementación:** baja de identidad y revisión de grupos/sesiones pertinentes en un entorno ficticio. **Pruebas:** acceso válido antes, rechazo después y registro de la acción; verificar también identidades de servicio no afectadas.

Contribuye a PR.AA y a medidas de acceso. Puede apoyar obligaciones de seguridad de datos personales, pero no demuestra finalidad lícita, información al interesado, minimización, derechos o legalidad de una transferencia internacional. La evidencia pertenece al servicio, periodo y proveedor realmente probados; no se propaga a todos los sistemas de la empresa. [S01, S07]

## Particularidades del ENS

Determinar primero si el sistema entra en el ámbito; el sector privado puede estar incluido por los supuestos previstos y la relación contractual. Identificar responsables de información, servicio, seguridad y sistema. Valorar las dimensiones de seguridad pertinentes y categorizar el sistema según anexo I; después seleccionar medidas/refuerzos del anexo II, documentar aplicabilidad y justificar compensatorias cuando correspondan. No marcar todas las medidas como idénticamente obligatorias para cualquier organización o categoría. [S08]

La declaración de aplicabilidad debe reflejar selección y justificación; su denominación similar a un documento ISO no la convierte en el mismo documento ni en una equivalencia de conformidad. Las medidas adicionales pueden responder a riesgos que no queden suficientemente reducidos por el mínimo.

## Particularidades de privacidad

Preguntar qué daño podría sufrir una persona por acceso, alteración, indisponibilidad, uso excesivo, inferencia, discriminación o divulgación. Incluir expectativas, vulnerabilidad de colectivos y efectos fuera de la empresa. Una EIPD se determina por los criterios aplicables y no porque una matriz de ciberseguridad arroje un color.

Las condiciones y plazos de comunicación/notificación dependen de la norma, el rol y el caso. El ejercicio utilizará un árbol de decisión validado contra artículos 33/34 y no una regla «todo incidente se notifica igual». Los controles técnicos tampoco reemplazan información, base jurídica, derechos, acuerdos o límites de conservación. [S07, S09]

## Ejercicios y aceptación

El alumno entrega inventario de un servicio ficticio, tres riesgos, cinco controles, dos pruebas y una matriz de correspondencias. Debe identificar al menos una relación falsa y tres obligaciones de privacidad que no pueda demostrar con logs o un producto. Se evalúa la precisión de alcance, la calidad de evidencia y la identificación de lagunas, no el número de casillas verdes.
