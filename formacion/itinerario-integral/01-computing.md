<!-- ES -->
# Informática: mapa completo para comprender antes de operar

**Lectura D26 · Edición de ampliación 2026-09-21.** Complementa M01–M04; no añade horas ni certifica ejecución. Empieza aquí y consulta después [historia](#/recurso/D27), [hardware](#/recurso/D28) y [redes](#/recurso/D29). Las analogías y los ejercicios son elaboración docente; las fuentes externas se identifican en [D36](#/recurso/D36).

## Objetivos y pregunta inicial

Al terminar debes poder dibujar el camino de un dato desde un móvil hasta un servicio; separar representación, procesamiento y comunicación; formular un diagnóstico sin cambiar el sistema a ciegas; y distinguir una capacidad instalada de un resultado demostrado. Pregunta inicial: cuando guardas un documento «en la nube», ¿qué máquinas, identidades, ubicaciones, permisos y copias están implicados?

## 1. Qué estudia la informática

La informática estudia cómo representar, transformar, almacenar y comunicar información mediante sistemas computacionales. Usar una aplicación es una habilidad; explicar sus entradas, reglas, estado y resultados es otra. La tecnología es más amplia: incluye métodos, instrumentos, energía, organización y decisiones. Un procedimiento en papel puede ser tecnológico sin ser software; digitalizarlo no demuestra que sea adecuado.

Trabajaremos con ocho preguntas: qué dato entra; cómo se representa; qué programa lo procesa; dónde se ejecuta; quién puede actuar; qué comunicaciones requiere; qué estado permanece; y qué evidencia permite comprobarlo. Son preguntas transferibles entre Linux, Windows, macOS, un servicio cloud y una aplicación de IA.

## 2. Representación: los bytes no tienen significado por sí solos

Un bit representa una elección binaria y un byte tiene ocho bits. Un archivo es una secuencia de bytes interpretada según un formato. Texto, imagen, sonido y una clave criptográfica pueden almacenarse como bytes, pero no admiten las mismas operaciones. Una extensión orienta; no prueba formato ni legitimidad.

Distingue tamaño decimal y binario: 1 kB son 1.000 bytes y 1 KiB son 1.024. Un carácter visible no equivale siempre a un byte ni a un único punto de código. Un mismo texto puede tener codificaciones o normalizaciones diferentes. Un hash compara los bytes elegidos, no el significado ni todos los metadatos. Codificar no es cifrar; comprimir no es anonimizar. Consulta Unicode y la documentación de Python indicadas en D36.

## 3. Algoritmo, programa y contrato

Un algoritmo describe pasos; un programa los expresa para un entorno de ejecución. Su contrato define entradas válidas, resultado, errores y efectos. «Devuelve los usuarios» es ambiguo: ¿locales, del directorio o de una aplicación? ¿Activos, deshabilitados o con acceso efectivo? El contrato evita comparar salidas que responden a preguntas distintas.

Ejemplo docente: contar documentos de una carpeta sin modificarla. Define si incluye subcarpetas, ocultos, enlaces, archivos inaccesibles y nombres Unicode. Una salida cero y un permiso denegado no significan lo mismo. Introduce casos normales, vacíos, inválidos y límites antes de automatizar.

## 4. De instrucciones a procesos

El procesador ejecuta instrucciones; el sistema operativo administra recursos y aislamiento; los procesos mantienen estado, identidad y recursos abiertos. Un programa guardado no es un proceso en ejecución. Una terminal es una interfaz, no un permiso administrativo. Una sesión SSH puede mostrar una carpeta remota aunque el teclado sea local.

Antes de cualquier práctica registra host, sistema/arquitectura, shell, usuario, directorio y alcance. Después identifica proceso, servicio, puerto y fuente de logs cuando proceda. No traslades una opción de GNU a BSD o un cmdlet de Windows a Linux sin comprobar disponibilidad y semántica. [Comparación de sistemas](#/recurso/D02).

## 5. Memoria, persistencia y datos

La RAM es memoria de trabajo, el almacenamiento conserva datos y una caché retiene resultados para evitar trabajo repetido. La caché no es automáticamente una copia de seguridad. Un sistema de archivos organiza contenido y metadatos; una base de datos añade un modelo, consultas, transacciones y controles sobre información estructurada.

Una transacción agrupa operaciones con unas garantías concretas; no convierte toda aplicación distribuida en coherente por arte de magia. Al estudiar una base de datos pregunta por concurrencia, recuperación, índices, permisos y backups. Al estudiar un archivo pregunta por propietario, ACL, formato, tiempos y conservación. Los logs son datos sensibles y también pueden fallar o desaparecer.

## 6. Redes y aplicaciones como cadena de dependencias

Abrir una web puede implicar resolución DNS, rutas, conexión de transporte, confianza TLS, HTTP, autorización de la aplicación y acceso a datos. Una prueba de ping no valida toda esa cadena. Un puerto abierto no demuestra que la función de negocio sea correcta. El navegador, el proxy, el proveedor y el servidor no observan necesariamente lo mismo.

Dibuja los saltos y límites de confianza. Separa plano de datos, control y administración. Una VLAN no sustituye una política entre segmentos; una VPN no autoriza por sí sola acceso a todas las aplicaciones. [Redes](#/recurso/D29) y [arquitecturas web](#/recurso/D30).

## 7. Construir, publicar y operar

El código fuente se transforma en artefactos; las pruebas verifican propiedades; la publicación carga y activa una versión; la operación comprueba su servicio real. Son estados separados. El ejemplo del campus utiliza Markdown, catálogos JSON y activos estáticos: que GitHub contenga los fuentes no demuestra que la versión pública los sirva.

Conserva versión, manifiesto, pruebas, configuración y posibilidad de volver atrás. No confundas subir una preview con activar producción. Una lectura de estado debe tener fecha y método; los logs históricos de un fallo no prueban que siga fallando hoy. La recuperación incluye datos, permisos, claves y rutas, no solo código.

## 8. Seguridad, privacidad y valor

La seguridad protege objetivos frente a escenarios adversos; la privacidad trata también legitimidad, finalidad y derechos. Un dato correctamente cifrado puede estar tratado sin justificación. Una web disponible puede autorizar mal. Un registro abundante puede aumentar exposición si carece de minimización y acceso restringido.

Trabajaremos desde servicio y dato hacia riesgo, control, implementación, evidencia y responsable. Comprar un producto no cierra ese recorrido. La medición debe explicar población, ventana, cobertura y límites. [Seguridad y equipos](#/recurso/D31), [información](#/recurso/D32), [identidades](#/recurso/D33).

## 9. Situación actual y direcciones de evolución

La práctica contemporánea combina infraestructura clásica, virtualización, contenedores, servicios gestionados, identidades federadas y aceleración especializada. La IA añade modelos, datos de entrenamiento/inferencia y nuevas dependencias, pero sigue necesitando cómputo, memoria, red, energía y operación. No reemplaza automáticamente los fundamentos.

Para hablar de futuro separa investigación, borrador normativo, producto disponible y adopción medida. «6G», «cuántico» o «agente autónomo» no son garantías de madurez. Evalúa hipótesis mediante una tarea, un baseline y una prueba: exactitud, coste, latencia, energía, seguridad y recuperación. Las predicciones de un fabricante se atribuyen como tales; no se convierten en fechas aseguradas.

## 10. Mapa de aprendizaje sin duplicar el curso

| Pregunta de aprendizaje | Lectura y práctica existente | Evidencia que debes producir |
|---|---|---|
| ¿De dónde vienen estas ideas? | D27; M02 | Cronología con fuentes y criterios de «primero» |
| ¿Qué hay dentro del equipo? | D28; M02–M03 | Diagrama con analogía y límites |
| ¿Cómo lo observo? | M04–M06/M14/M16/M21 | Consulta explicada y entrada inválida |
| ¿Quién puede hacer qué? | D22/D33; M07/M17/M18 | Matriz de acceso y revocación |
| ¿Cómo se comunican? | D23/D29; M10/M24 | Flujo permitido y denegado |
| ¿Cómo se ofrece un servicio? | D30; M25–M26 | Arquitectura y recuperación |
| ¿Cómo se protege y detecta? | D24/D25/D31; M27–M30 | Control, evento y decisión |
| ¿Cómo se gestionan los datos? | D32; M09/M19/M23 | Clasificación y copia restaurada |
| ¿Qué profesión hace cada tarea? | D34 | Portfolio y mapa de responsabilidades |

## Prácticas de comprensión y criterio de corrección

**INT-L01: anatomía de guardar un documento.** En una cuenta y carpeta de práctica, crea un texto sintético. Dibuja aplicación, proceso, RAM, almacenamiento, permisos y copia. Compara guardar, sincronizar y respaldar. Evidencia: diagrama, dos hashes y explicación de qué no acreditan. Éxito: identificar el punto de fallo y una recuperación sin datos personales. Recuperación: borrar únicamente copias de ensayo, conservando el original hasta evaluar.

**INT-L02: diagnóstico antes de cambios.** El docente entrega cuatro síntomas: nombre que no resuelve, puerto rechazado, certificado no confiado y acceso denegado en la aplicación. El alumno propone una comprobación distinta por síntoma, con resultado esperado y alternativa. No realiza escaneos externos. Éxito: no resolver todas las situaciones desactivando firewall o validación TLS.

Autoevaluación: ¿por qué más RAM no arregla siempre una web lenta? Respuesta competente: identifica el cuello de botella y las mediciones necesarias, sin atribuir todo el tiempo a memoria. ¿Por qué una captura no demuestra recuperación? Porque faltan origen, pasos y prueba funcional. Se valora explicación, comprobación independiente y reconocimiento de límites.
<!-- EN -->
# Computing: a complete map for understanding before operating

**Reading D26 · Expansion edition 2026-09-21.** Complements M01–M04; adds no hours or execution certification. Continue with [history](#/recurso/D27), [hardware](#/recurso/D28) and [networks](#/recurso/D29). Analogies and exercises are original teaching material; external references are identified in [D36](#/recurso/D36).

## Objectives and opening question

Explain how data travels from a phone to a service; separate representation, processing and communication; propose a diagnosis before changing a system; distinguish an installed capability from a demonstrated outcome. When a document is saved «in the cloud», which machines, identities, locations, permissions and backups are involved?

## 1. What computing studies

Computing concerns representing, transforming, storing and communicating information with computational systems. Using an application is one skill; explaining its inputs, rules, state and outputs is another. Technology is broader: it includes methods, tools, energy, organization and decisions. A paper-based procedure can be technological without being software; digitizing it does not establish its suitability.

Ask eight questions: what enters; how it is represented; which program processes it; where it executes; who may act; what communication it needs; what state persists; and what evidence verifies the result. These transfer between Linux, Windows, macOS, cloud services and AI applications.

## 2. Representation: bytes do not explain their own meaning

A bit represents a binary choice and a byte contains eight bits. A file is a byte sequence interpreted according to a format. Text, pictures, sound and cryptographic keys can all be stored as bytes, but their valid operations differ. An extension is a hint, not proof of format or trustworthiness.

Distinguish decimal and binary sizes: 1 kB is 1,000 bytes and 1 KiB is 1,024. A visible character does not always equal one byte or one code point. Equivalent-looking text can have different encodings or normalization. A hash compares the chosen bytes, not their meaning or every metadata field. Encoding is not encryption; compression is not anonymization. Consult the Unicode and Python references in D36.

## 3. Algorithms, programs and contracts

An algorithm describes steps; a program expresses them for an execution environment. Its contract defines valid inputs, output, errors and effects. «Return the users» is ambiguous: local, directory or application users? Active, disabled or effectively authorized? A contract prevents comparisons between answers to different questions.

Teaching example: count documents in a directory without changing it. Decide whether to include subdirectories, hidden files, links, inaccessible files and Unicode names. Zero results and permission denied are different outcomes. Test ordinary, empty, invalid and boundary inputs before automation.

## 4. From instructions to processes

A processor executes instructions; the OS manages resources and isolation; processes have state, identity and open resources. A stored program is not a running process. A terminal is an interface, not administrative permission. An SSH session can show a remote directory while the keyboard remains local.

Before each exercise record the host, OS/architecture, shell, user, working directory and scope. Afterwards identify process, service, port and log source where relevant. Do not transfer GNU options to BSD or Windows cmdlets to Linux without checking availability and semantics. [Platform comparison](#/recurso/D02).

## 5. Memory, persistence and data

RAM provides working memory; storage persists data; caches retain results to avoid repeated work. A cache is not automatically a backup. A filesystem organizes contents and metadata; a database adds a model, queries, transactions and controls over structured information.

A transaction groups operations with specific guarantees; it does not make every distributed application consistent. For databases examine concurrency, recovery, indexes, permissions and backups. For files examine ownership, ACLs, format, timestamps and preservation. Logs are sensitive data and may also fail or disappear.

## 6. Networks and applications form a dependency chain

Opening a website may require DNS, routing, transport, TLS trust, HTTP, application authorization and data access. Ping does not validate the entire chain. A listening port does not prove that a business function works. Browser, proxy, provider and server do not necessarily observe the same information.

Draw hops and trust boundaries. Separate data, control and management planes. VLANs do not replace inter-segment policies; a VPN does not authorize access to every application. See [networks](#/recurso/D29) and [web architecture](#/recurso/D30).

## 7. Build, publish and operate

Sources become artifacts; tests verify properties; publication uploads and activates a version; operations checks the real service. These are distinct states. The campus uses Markdown, JSON catalogs and static assets: storing sources on GitHub does not prove the public version serves them.

Preserve version, manifest, tests, configuration and rollback. Uploading a preview is not production activation. A status observation needs a date and method; historical failure logs do not prove present failure. Recovery includes data, permissions, keys and routes, not just application code.

## 8. Security, privacy and value

Security protects objectives against adverse scenarios; privacy also concerns lawful purposes and rights. Correctly encrypted data may still be processed without justification. An available website can authorize incorrectly. Extensive logging can increase exposure when minimization and restricted access are absent.

Move from service and data to risk, control, implementation, evidence and owner. Buying a product does not complete this chain. Measurements state population, window, coverage and limitations. See [security teams](#/recurso/D31), [information](#/recurso/D32) and [identity](#/recurso/D33).

## 9. Current practice and future directions

Contemporary systems combine conventional infrastructure, virtualization, containers, managed services, federation and specialized acceleration. AI introduces models, training/inference data and further dependencies, but still requires compute, memory, networking, energy and operations. It does not remove the foundations.

Separate research, draft standards, available products and measured adoption. «6G», «quantum» and «autonomous agent» do not establish maturity. Test a hypothesis against a defined baseline: accuracy, cost, latency, energy, security and recovery. Attribute vendor forecasts rather than turning them into guaranteed dates.

## 10. Learning map without duplicating the course

| Learning question | Reading and existing module | Required evidence |
|---|---|---|
| Where did the ideas originate? | D27; M02 | Sourced timeline and criteria for «first» |
| What is inside a computer? | D28; M02–M03 | Diagram with analogy limitations |
| How do I observe it? | M04–M06/M14/M16/M21 | Explained query and invalid input |
| Who may do what? | D22/D33; M07/M17/M18 | Access and revocation matrix |
| How do systems communicate? | D23/D29; M10/M24 | Allowed and denied flow |
| How is a service delivered? | D30; M25–M26 | Architecture and recovery |
| How is it protected and observed? | D24/D25/D31; M27–M30 | Control, event and decision |
| How is information governed? | D32; M09/M19/M23 | Classification and restored backup |
| Which profession performs each task? | D34 | Portfolio and responsibility map |

## Understanding exercises and marking criteria

**INT-L01: anatomy of saving a document.** In a practice account and folder, create synthetic text. Draw application, process, RAM, storage, permissions and backup. Compare saving, synchronization and backup. Evidence: diagram, two hashes and limitations. Success: identify a failure point and recovery without personal data. Cleanup: remove only practice copies after assessment; preserve the original until then.

**INT-L02: diagnosis before change.** The teacher supplies four symptoms: a name fails to resolve, a port refuses a connection, a certificate is not trusted, and the application denies access. Propose a distinct check, expected result and alternative for each. No external scanning. Success: do not resolve everything by disabling firewall or TLS validation.

Self-check: why does more RAM not always fix a slow web service? A competent answer identifies bottlenecks and missing measurements instead of attributing all delay to memory. Why does a screenshot not establish recovery? It lacks provenance, procedure and functional verification. Assessment values explanation, independent checks and honest limitations.
