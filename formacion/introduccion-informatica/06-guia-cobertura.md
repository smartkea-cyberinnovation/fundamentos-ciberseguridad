<!-- ES -->
# Guía de estudio y cobertura de los doce temas

D46 organiza lecturas, prácticas y autoevaluación de Introducción a la informática. La revisión del 18 de octubre de 2026 contrasta la propuesta del 8 de octubre, la guía del 9 de octubre de 2026 y la planificación práctica anterior. Aporta material propio y trazabilidad de cobertura.

La asignatura de referencia tiene **6 ECTS**. El itinerario M01–M32 del repositorio tiene **480 horas** planificadas de sistemas, ciberseguridad y desarrollo profesional: proporciona recursos seleccionables y no constituye la carga oficial de esta asignatura. Estas lecturas no añaden horas oficiales [S1].

## Cómo empezar y mantener el hilo

Comienza con M01 y un entorno Linux preparado. Observa archivos, terminal y recursos antes de administrar servicios. Lee D26 para relacionar componentes y D27 para situar su historia. Alterna después cada fundamento con una observación o experimento: bytes con D41, decisiones lógicas con D42, recursos y recuperación con D43, procesos y archivos con D44, comunicación y servicios con D45.

En cada sesión elige una pregunta, predice, ejecuta y explica. Registra hipótesis, entrada, procedimiento, resultado, interpretación, límite y limpieza. Si el resultado difiere, conserva el error y revisa la hipótesis. Una captura sin contexto no acredita comprensión.

Las referencias a módulos indican dónde continuar; no implican obligatoriedad de todo su contenido ni que una persona lo haya completado.

## Matriz de cobertura

**Desarrollado** significa que había una lectura explicativa relevante; **parcial**, contenidos repartidos o menciones por desarrollar. La última columna identifica lo **agregado** en esta revisión. D identifica lecturas y M, módulos [S1–S3].

| Tema de referencia | Evidencia previa | Estado previo | Aportación agregada |
|---|---|---|---|
| T01 · Concepto, historia y aplicaciones | D26, D27, M02 | Desarrollado | D46 ordena el recorrido y la evidencia |
| T02 · Sistemas de numeración y aritmética binaria | M02, D26 | Parcial | D41: octal, hexadecimal, complemento a dos, acarreo y desbordamiento |
| T03 · Codificación de caracteres, imagen, audio y compresión | M02, D26 | Parcial | D41: Unicode/UTF-8 y tamaños multimedia resueltos |
| T04 · Lógica digital y álgebra de Boole | Esquema D37 y condiciones en M11 | Parcial | D42: tablas, De Morgan, puertas, sumadores y estado |
| T05 · Von Neumann y CPU | D28, M02, M03 | Parcial | D43: Harvard, ciclo, ISA y microarquitectura |
| T06 · Jerarquía de memoria y almacenamiento | D28, M09 | Parcial | D43: niveles, persistencia, NAS/SAN y restauración |
| T07 · Buses, periféricos y entrada/salida | D28, M02 | Parcial | D43: datos/dirección/control, sondeo, interrupciones y DMA |
| T08 · Sistemas operativos I: funciones, tipos y procesos | D26, M03, M08 | Parcial | D44: proceso/hilo, estados y planificación resuelta |
| T09 · Sistemas operativos II: memoria, archivos y acceso | M03, M07, M09, D33 | Parcial | D44: páginas, inode, enlaces, journal y permisos |
| T10 · Aplicaciones, utilidades y licencias | D26, M04, M08 | Parcial | D44: libertades, dependencias y mantenimiento |
| T11 · Redes y servicios de Internet | D29, M10, M24 | Desarrollado | D45 precisa DHCP, DNS, transporte y diagnóstico por capas |
| T12 · Virtualización, cloud e IA | D28, D30, M26, M31 | Parcial | D45: modelos de servicio, responsabilidades y límites |

## Seis prácticas conectadas con el temario

| Práctica | Apoyo | Evidencia y validación esperadas |
|---|---|---|
| P01 · Representar información | D41, M02 | Conversiones manuales, bytes UTF-8 y recuperación tras compresión sin pérdida |
| P02 · Anatomía del equipo | D28, D43, M02 | Inventario razonado de CPU, memoria, almacenamiento e interfaces; separar dato observado de inferencia |
| P03 · Linux y recursos | D44, M05, M07, M08 | Archivo temporal y permisos, identidad de inode y explicación de procesos; administración de cuentas solo en el laboratorio preparado |
| P04 · Configuración y servicios de red | D45, M10, M24 | Prefijo, siguiente salto, resolución y transporte explicados con datos de práctica |
| P05 · Interpretación de tráfico | D29, D45 | PCAP docente autorizado: origen/destino, protocolo y límites de observación bajo cifrado |
| P06 · Integridad y recuperación | D43, M09 | Alteración detectada, copia restaurada, apertura funcional y limpieza confirmada |

Los ejemplos nuevos usan memoria o archivos temporales. P02 aporta observación del sistema; P05 requiere un PCAP docente preparado. Una simulación enseña a razonar, pero no acredita conectividad fuera del entorno ensayado.

## Resultados y proyecto integrador

La correspondencia con los resultados de referencia guía la recogida de evidencia:

- **K1 y K7:** explicar componentes, representación y redes, y relacionarlos con decisiones de protección.
- **K2 y H5:** reconocer organización e integridad de datos; ensayar consultas parametrizadas, dependencias y cambios reproducibles.
- **H2:** interpretar herramientas y evidencias, identificando qué permiten concluir.
- **C2, C3 y C5:** integrar conocimientos, colaborar y presentar una justificación propia comprensible para otras personas.

Para el proyecto, elige un PC de laboratorio, servidor de práctica, servicio cloud preparado o dispositivo IoT autorizado. Entrega diagrama, inventario, recorrido de un dato, tres decisiones justificadas de protección y recuperación comprobada. Explica hardware, sistema, software, almacenamiento y comunicaciones. En equipo, distribuye tareas, conserva contribuciones y defiende individualmente una decisión.

## Ensayar con el test

El [test de práctica del campus](https://smartkea.com/introduccion-ciberseguridad/examen/) utiliza un banco de **100 preguntas en español** y sesiones aleatorias de **20 preguntas**. La corrección durante el ensayo y las explicaciones sirven para localizar dudas y volver a las lecturas. Antes de repetir, explica con tus palabras por qué una respuesta es correcta y qué hace incorrectos los distractores.

La puntuación mide ese intento sobre su selección de preguntas. No equivale a una calificación oficial ni sustituye prácticas, proyecto o defensa. La guía y las decisiones docentes vigentes determinan evaluación y pesos; esta revisión no convierte las propuestas de ponderación recibidas en acuerdos aprobados. El banco y sus respuestas forman parte de una aplicación de estudio accesible al cliente, de modo que el test se usa como herramienta formativa.

**Criterio de avance:** combina respuesta correcta, explicación causal y evidencia reproducible. Si solo recuerdas una opción, vuelve al ejemplo, cambia un dato y predice el nuevo resultado.

<!-- EN -->
# Study guide and coverage of the twelve topics

D46 organizes readings, practice, and self-assessment for Introduction to Computing. The review dated 18 October 2026 compares the proposal of 8 October, the guide of 9 October 2026, and the earlier practical plan. It provides original material and coverage traceability.

The reference subject carries **6 ECTS**. The repository's M01–M32 pathway has **480 planned hours** of systems, cybersecurity, and professional development: it provides selectable resources and is not this subject's official workload. These readings add no official hours [S1].

## Starting and maintaining continuity

Start with M01 and a prepared Linux environment. Observe files, the terminal, and resources before administering services. Read D26 to connect components and D27 to place their history in context. Then alternate each foundation with an observation or experiment: bytes with D41, logical decisions with D42, resources and recovery with D43, processes and files with D44, and communication and services with D45.

In each session, choose a question, predict, execute, and explain. Record the hypothesis, input, procedure, result, interpretation, limitation, and cleanup. If the outcome differs, preserve the error and revise the assumption. A screenshot without context does not establish understanding.

Module references identify where to continue; they do not imply that all their content is compulsory or that a person has completed it.

## Coverage matrix

**Developed** means a relevant explanatory reading already existed; **partial** means distributed content or mentions requiring development. The last column identifies material **added** in this review. D denotes readings and M denotes modules [S1–S3].

| Reference topic | Prior evidence | Prior status | Added contribution |
|---|---|---|---|
| T01 · Concept, history, and applications | D26, D27, M02 | Developed | D46 organizes the pathway and evidence |
| T02 · Number systems and binary arithmetic | M02, D26 | Partial | D41: octal, hexadecimal, two's complement, carry, and overflow |
| T03 · Character, image, audio, and compression coding | M02, D26 | Partial | D41: Unicode/UTF-8 and worked multimedia sizes |
| T04 · Digital logic and Boolean algebra | D37 outline and conditions in M11 | Partial | D42: tables, De Morgan, gates, adders, and state |
| T05 · Von Neumann and CPU | D28, M02, M03 | Partial | D43: Harvard, cycle, ISA, and microarchitecture |
| T06 · Memory and storage hierarchy | D28, M09 | Partial | D43: levels, persistence, NAS/SAN, and restoration |
| T07 · Buses, peripherals, and input/output | D28, M02 | Partial | D43: data/address/control, polling, interrupts, and DMA |
| T08 · Operating systems I: functions, types, and processes | D26, M03, M08 | Partial | D44: process/thread, states, and a worked scheduling example |
| T09 · Operating systems II: memory, files, and access | M03, M07, M09, D33 | Partial | D44: pages, inode, links, journal, and permissions |
| T10 · Applications, utilities, and licenses | D26, M04, M08 | Partial | D44: freedoms, dependencies, and maintenance |
| T11 · Networks and Internet services | D29, M10, M24 | Developed | D45 details DHCP, DNS, transport, and layered diagnosis |
| T12 · Virtualization, cloud, and AI | D28, D30, M26, M31 | Partial | D45: service models, responsibilities, and limitations |

## Six practices connected to the syllabus

| Practice | Support | Expected evidence and validation |
|---|---|---|
| P01 · Representing information | D41, M02 | Manual conversions, UTF-8 bytes, and recovery after lossless compression |
| P02 · Computer anatomy | D28, D43, M02 | Reasoned inventory of CPU, memory, storage, and interfaces; separate observation from inference |
| P03 · Linux and resources | D44, M05, M07, M08 | Temporary file and permissions, inode identity, and process explanation; account administration only in the prepared laboratory |
| P04 · Network configuration and services | D45, M10, M24 | Prefix, next hop, resolution, and transport explained with practice data |
| P05 · Traffic interpretation | D29, D45 | Authorized teaching PCAP: source/destination, protocol, and observation limits under encryption |
| P06 · Integrity and recovery | D43, M09 | Detected alteration, restored backup, functional opening, and confirmed cleanup |

The new examples use memory or temporary files. P02 provides system observation; P05 requires a prepared teaching PCAP. A simulation teaches reasoning but does not establish connectivity outside the tested environment.

## Outcomes and integration project

The correspondence with the reference outcomes guides evidence collection:

- **K1 and K7:** explain components, representation, and networks, connecting them with protection decisions.
- **K2 and H5:** recognize data organization and integrity; practice parameterized queries, dependency review, and reproducible changes.
- **H2:** interpret tools and evidence, identifying what they allow you to conclude.
- **C2, C3, and C5:** integrate knowledge, collaborate, and present your own reasoning clearly to other people.

For the project, choose a laboratory PC, practice server, prepared cloud service, or authorized IoT device. Submit a diagram, inventory, data journey, three justified protection decisions, and verified recovery. Explain hardware, system, software, storage, and communications. In a team, divide tasks, preserve contributions, and individually defend one decision.

## Rehearsing with the test

The [campus practice test](https://smartkea.com/introduccion-ciberseguridad/examen/) uses a bank of **100 questions in Spanish** and random sessions of **20 questions**. Correction during practice and explanations help identify uncertainties and return to the readings. Before trying again, explain in your own words why an answer is correct and what makes the distractors incorrect.

The score measures that attempt on its selected questions. It is not an official grade and does not replace practices, the project, or its defense. The current guide and teaching decisions determine assessment and weights; this review does not turn received weighting proposals into approved agreements. The bank and its answers form part of a study application available to the client, so the test serves a formative purpose.

**Progress criterion:** combine a correct answer, a causal explanation, and reproducible evidence. If you only remember an option, return to the example, change one input, and predict the new outcome.

<!-- COMMON -->
## Fuentes y trazabilidad / Sources and traceability

- S1 · [Planificación del itinerario M01–M32 / M01–M32 pathway planning](../sistemas-operativos/planificacion/README.md) y / and [currículo estructurado / structured curriculum](../sistemas-operativos/planificacion/curriculo.json).
- S2 · [Lecturas de fundamentos D26–D40 / Foundations readings D26–D40](../itinerario-integral/README.md), especialmente / particularly [historia / history](../itinerario-integral/02-history.md), [hardware](../itinerario-integral/03-hardware.md) y / and [redes / networks](../itinerario-integral/04-networks.md).
- S3 · [Índice y nuevas lecturas D41–D46 / Index and new readings D41–D46](README.md).
- Base de contraste académico: propuesta de 08/10/2026 y guía de 09/10/2026 consultadas en revisión privada. Se publica la correspondencia de contenidos y material original; los documentos y comunicaciones permanecen en sus canales de origen. / Academic comparison baseline: proposal dated 8 October 2026 and guide dated 9 October 2026 consulted in a private review. This publishes the content mapping and original material; documents and communications remain in their original channels.

Revisión de cobertura: 18 de octubre de 2026. / Coverage review: 18 October 2026.
