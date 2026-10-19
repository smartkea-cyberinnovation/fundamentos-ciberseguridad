# SmartKEA · Instrucciones completas para Figma Make

**Versión del encargo: 1.0.0 · Revisada el 19 de octubre de 2026.** Esta especificación sirve para diseñar, montar una versión revisable e integrar mejoras en el producto existente. El repositorio canónico es [smartkea-cyberinnovation/fundamentos-ciberseguridad](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad). Los contratos y el banco se adjuntan en JSON. El manifiesto identifica el snapshot utilizado; este documento no declara una publicación nueva ni sustituye la aceptación del despliegue.

## Prompt de trabajo

Actúa como un equipo de diseño de producto educativo, frontend y revisión de calidad. Mejora SmartKEA para que un estudiante pueda entender qué estudiar, avanzar con guía concreta, practicar en su entorno y ensayar preguntas con corrección inmediata. Trabaja sobre el producto y los datos existentes. Conserva los identificadores, las rutas canónicas, las respuestas correctas, las explicaciones y la continuidad de los registros locales.

El resultado debe ser un campus profesional, claro y funcional en escritorio, tableta y móvil. Prioriza lectura, práctica y siguiente acción. Entrega pantallas con estados completos y comportamiento comprobable, un registro de cambios y una ruta de integración en Git. Utiliza esta especificación y `producto.json` como contrato de producto; `catalogo-publico.json` inventaría las unidades reales; `muestras-contenido.json` aporta contenido largo real; `banco-preguntas.json` contiene las cien preguntas completas. Si un archivo del repositorio no está disponible en el entorno Make, indícalo por su ruta y conserva su interfaz; no inventes contenido, respuestas, servicios ni resultados de pruebas.

### Orden de autoridad

1. La petición del propietario del producto y las correcciones aceptadas durante el trabajo.
2. Contenido, contratos y comportamiento verificados del repositorio para el snapshot identificado.
3. Esta especificación y `producto.json` para las mejoras propuestas.
4. Preferencias genéricas del generador, únicamente donde no exista una decisión anterior.

Una propuesta de interfaz no cambia por sí sola el currículo ni la evaluación. Si un cambio exige modificar el significado de un identificador, una clave de progreso, una ruta o el esquema de un banco, presenta primero la migración concreta y sus casos de prueba dentro de la revisión de código.

## 1. Qué existe y qué se propone

| Superficie | Producto real que se conserva | Mejora de experiencia propuesta |
|---|---|---|
| Campus general | 32 módulos, 96 fichas de laboratorio, 46 recursos, siete bloques y 480 horas planificadas; ES/EN; biblioteca, búsqueda, presentación y continuidad local | Mejorar la orientación inicial, el acceso a lo último estudiado y la siguiente acción contextual |
| Aula de sistemas | 28 lecciones ES/EN: cuatro comunes, ocho Linux, ocho Windows y ocho macOS; 500 vistas; comprobaciones, guía de entorno, foco/pausa y registro opcional | Hacer más visible la relación entre objetivo, concepto, micropráctica, evidencia y recuperación |
| Examen de informática | Banco público de 100 preguntas en español; 20 aleatorias por intento; cuatro opciones; corrección inmediata; explicación; resumen y repaso | Perfeccionar la jerarquía de progreso, el tratamiento de estados y el enlace al estudio posterior |
| TERM | 16 módulos, 48 lecciones, 48 retos y 96 preguntas en español; aprender, practicar, resolver y comprobar; laboratorio opcional | Clarificar el paso actual, el contexto del comando y la diferencia entre ejemplo y resultado realmente observado |
| Rutas por perfil | Seis rutas profesionales y 26 etapas con objetivos, evidencias, fuentes y prerrequisitos; integración local revisada | Facilitar la elección de perfil y la siguiente etapa sin mezclar horas ni progreso |
| Asistencia | Guías, pistas, cuestionarios y orientación local, sin servicio de IA generativa | Añadir orientación por reglas sobre el contenido existente, explicando por qué sugiere cada siguiente paso |

Las cifras proceden de los catálogos generados, no de texto promocional. Las 480 horas no son asistencia, tiempo realmente estudiado ni carga oficial de una asignatura distinta. Los recorridos se solapan: no sumar sus horas ni convertir sus porcentajes en un único índice de competencia. D37–D40 conservan resumen en inglés y edición docente completa EN pendiente. D41–D46 sí tienen lecturas desarrolladas ES/EN en el snapshot. El examen y TERM siguen en español. [R-CATALOG] [R-OS] [R-EXAM] [R-TERM]

### Seis rutas profesionales de la integración revisada

La integración local ya incorpora `formacion/rutas/routes.json`, su validador `campus/learning_paths.py` y la página `rutas.html`. Se trata de una capacidad **existente en la integración revisada**; su publicación se confirma aparte con el SHA servido. El inventario generado incluye las seis rutas completas, sus 26 etapas, trece programas externos y 32 fuentes públicas. [R-PATHS] [R-PATHS-BUILD] [R-PATHS-TEST]

| ID | Perfil real | Etapas | Dedicación orientativa |
|---|---|---:|---|
| `no-tecnico` | No técnico · negocio y personas | 4 | 8 semanas · 32 h |
| `legal` | Jurídico · privacidad y contratación | 4 | 12 semanas · 72 h |
| `dpd` | DPD · gobierno de privacidad | 6 | 16 semanas · 128 h |
| `tecnico` | Técnico · soporte y operación | 4 | 14 semanas · 84 h |
| `informatico` | Informático · desarrollo y arquitectura | 4 | 14 semanas · 112 h |
| `ciber` | Ciberseguridad · defensa, GRC y auditoría | 4 | 14 semanas · 112 h |

Estimaciones de dedicación al itinerario por actividades seleccionadas. No se suman a las 480 h del curso ni equivalen a completar los módulos enlazados o a formación reconocida. Los módulos completos conservan horas y prerrequisitos propios.

Conserva entrada, objetivo, trabajo y evidencia de cada etapa, consulta de prerrequisitos, fuentes oficiales, filtro por perfil, modo presentación e impresión. Un enlace a certificación o programa externo conduce a sus condiciones oficiales; no acredita que el alumno lo haya obtenido ni que SmartKEA expida esa credencial. Las marcas de evidencia son opcionales, usan `smartkea.learning-paths.v1`, no incluyen notas o identidad personal y no alteran el progreso del campus. Su identidad técnica `recordId` distingue vidas del registro para coordinar pestañas; no representa a un alumno. [R-PATHS-UI] [R-PATHS-BROWSER]

### Ampliación existente: caso C99-DFIR

Los módulos M27, M28 y M29 enlazan la práctica **C99-DFIR · Una shell con una llamada oculta** del repositorio. Conserva sus diez actividades, guía de alumno ES/EN, escenario sintético, herramientas offline, informe, soluciones y rúbrica. Sus doce preguntas públicas pertenecen al caso y no al banco de cien del examen. Es una ampliación de los módulos existentes: no añade horas, módulos, nuevas marcas ni una ruta de servidor propia. La actividad usa evidencias inertes y, opcionalmente, una shell legítima en un contenedor local; no presenta la muestra sospechosa como software que el campus ejecute. Enlaza las fuentes y los entregables reales, sin inventar un incidente ni una máquina conectada. [R-FORENSIC-CASE] [R-FORENSIC-PRACTICE] [R-FORENSIC-QUESTIONS] [R-FORENSIC-INTEGRATION]

## 2. Usuarios y resultados de aprendizaje

El estudiante principiante necesita comprender vocabulario, relaciones y límites antes de ejecutar órdenes. Su éxito es explicar una idea con sus palabras, predecir un efecto y comprobarlo en un entorno adecuado. El estudiante con experiencia necesita localizar una laguna y practicarla sin recorrer de nuevo material que ya comprende. El docente necesita lecturas, retos, criterios y evidencia legible; la versión actual no recibe notas ni datos personales de alumnos.

Diseña tres entradas visibles usando contenidos existentes: **Comprender informática**, **Practicar sistemas** y **Dominar la terminal**. El examen es un acceso de ensayo, con una invitación a estudiar después de los fallos. Usa los mismos términos en navegación, encabezados y acciones. Una etiqueta como «Comprobado por ti» es más precisa que «Dominado» cuando no hay verificación externa.

No bloquees el aprendizaje por crear una cuenta. No fuerces un diagnóstico previo ni un temporizador. El alumno puede leer sin guardar progreso, cambiar de recorrido, volver atrás o ensayar de nuevo.

## 3. Recorrido guiado del estudiante

### A. Primera visita: elegir una tarea concreta

La primera pantalla explica en una frase cada recorrido y ofrece una acción principal: «Empezar por los fundamentos». Como acciones secundarias, «Continuar sistemas», «Abrir TERM» y «Practicar 20 preguntas», según la superficie. Si existe continuidad válida, muestra «Continuar» con el nombre real de la unidad y una acción separada para ver el temario. Si no hay datos guardados, evita porcentajes simulados, rachas o horas ficticias.

Para informática, enlaza la guía D46 y la secuencia D26/D27 → D41 → D42 → D43 → D44 → D45. La secuencia organiza el estudio; no convierte lecturas en obligaciones ni altera los prerrequisitos de los módulos. M01 sirve para preparar contexto y trabajo seguro. Conserva la biblioteca completa como salida directa.

### B. Preparación: reconocer el entorno

En el aula OS, mantén «Mi entorno» con opciones reales de sistema y arquitectura: Mac Intel/Apple Silicon; Windows y Linux x64/ARM; tableta. Explica qué puede hacerse desde ese equipo y qué necesita una VM o laboratorio autorizado. Leer desde una tableta no acredita ejecutar una tarea nativa de Windows o macOS.

En TERM, distingue la terminal local del alumno y el endpoint ttyd opcional. El snapshot no tiene una máquina vinculada. Muestra la preparación del laboratorio y permite estudiar y copiar comandos mientras se configura. Un iframe cargado no demuestra autenticación ni ejecución correcta. [R-OS] [R-TERM-ARCH]

### C. Aprender: una idea y una comprobación

Cada vista debe responder: «¿Qué voy a comprender?», «¿Qué ejemplo lo muestra?» y «¿Cómo compruebo que lo entendí?». Conserva el contenido docente y sus referencias. En las lecturas largas, usa tabla de contenidos y títulos anclables. En OS, respeta la alternancia de conceptos y microprácticas existente; no conviertas las 500 vistas en una pared de tarjetas. En TERM, mantén la fase Aprender y su paginación por concepto.

Un ejemplo trabajado explica su supuesto, la acción y el resultado. Las pistas se revelan progresivamente con botones claros. La solución no reemplaza la oportunidad de intentarlo. El apoyo propuesto puede pedir una explicación breve o una predicción, conservada únicamente en memoria de la pestaña si el alumno decide escribirla.

### D. Practicar: contexto → predicción → acción → evidencia

La práctica presenta el entorno, requisitos, comando o pasos, efecto esperado, precauciones, verificación y reversión. Copiar es explícito; la web no ejecuta instrucciones ni se conecta a hosts por iniciativa propia. Identifica toda salida de muestra con «Resultado orientativo». La comprobación del alumno y la evidencia de laboratorio se muestran como declaraciones, sin sello de ejecución remota.

Ante un bloqueo, ofrece «Revisar entorno», «Ver una pista», «Anotar lo observado» y «Volver a la explicación». Conserva la separación entre el texto de ayuda y los datos introducidos por el estudiante. Las notas se tratan como texto; nunca se interpretan como HTML ni se añaden a comandos.

### E. Ensayar: veinte preguntas y corrección inmediata

La portada del examen explica: «20 preguntas al azar de un banco de 100. Tu primera respuesta queda registrada. Verás la explicación al elegir». Ofrece «Empezar 20 preguntas» o «Reanudar intento» cuando corresponda. Una nueva sesión que sustituye un intento activo requiere confirmación concreta, indicando que reemplaza esa selección.

En una pregunta muestra tema, posición, enunciado, cuatro opciones y progreso de respuestas. Al elegir, corrige inmediatamente, bloquea las cuatro opciones para puntuación y presenta: resultado textual, opción correcta, explicación y enlace de estudio. El alumno puede navegar hacia atrás; volver no permite sumar otro acierto. No introduzcas un botón «Corregir» que retrase el feedback, porque cambiaría la experiencia solicitada.

El resultado muestra aciertos, errores, pendientes y nota sobre diez; añade tabla por tema del intento, «Repasar fallos», «Revisar todo» y «Nueva sesión aleatoria». La nota es `10 × aciertos / 20`: diez aciertos y diez errores producen 5,0. Las no respondidas no suman puntos. No se aplica penalización negativa. No llamar aprobado/suspenso a un umbral que no está acordado.

### F. Continuar: una recomendación explicable

Propuesta local: después de un fallo, presentar la lectura ya vinculada y una acción concreta, por ejemplo «Repasar representación en D41». Si se añade un plan de repaso por reglas, utilizar solo fallos y pendientes del intento actual y declarar ese alcance. Orden estable: primero un tema con errores; después sus pendientes; a igualdad, orden T01–T12. No inferir una capacidad global con una o dos preguntas del tema. No hacer aparecer una puntuación histórica que no existe.

## 4. Arquitectura de navegación y enlaces

Conserva estas bases públicas:

| Producto | Base canónica |
|---|---|
| Campus | `https://smartkea.com/introduccion-ciberseguridad/` |
| Aula OS | `https://smartkea.com/introduccion-ciberseguridad/sistemas/` |
| Examen | `https://smartkea.com/introduccion-ciberseguridad/examen/` |
| TERM | `https://www.smartkea.com/fundamentos-ciberseguridad/term/` |
| Rutas por perfil | `https://smartkea.com/introduccion-ciberseguridad/rutas.html` |

Las rutas profesionales usan `rutas.html#ruta-no-tecnico`, `#ruta-legal`, `#ruta-dpd`, `#ruta-tecnico`, `#ruta-informatico` y `#ruta-ciber`; conserva esos IDs. El campus usa fragmentos como `?lang=es#/modulo/M02`, `#/recurso/D41` y `#/temario`. OS usa `?lang=es#OS-L01/0`, con índice de vista desde cero. TERM usa `#/leccion/m01-l01/concepto/0`; sus fases de URL son `concepto`, `practica`, `reto` y `test`. No sustituir esos segmentos por etiquetas traducidas. El examen tiene estado interno de intento y conserva su base sin inventar rutas de servidor para cada pregunta. `producto.json` contiene todas las plantillas de rutas y `catalogo-publico.json` los destinos concretos. [R-NAV] [R-OS-UI] [R-TERM-UI]

La página inglesa puede mantener su interfaz EN y enlazar a un recurso español identificado. No sustituir silenciosamente una lectura inglesa que no carga por la española. Al cambiar de idioma, conservar identificadores y progreso. Una nueva sesión del examen no afecta las claves del campus, OS o TERM.

Las sugerencias nuevas se integran en las pantallas actuales. No crear una nueva aplicación en la raíz del dominio, ni capturar todo `/fundamentos-ciberseguridad/*`, ni cambiar a rutas history sin un plan de servidor. La navegación por fragmentos permite conservar 404 reales para archivos ausentes.

## 5. Sistema visual

### Identidad y jerarquía

Mantén una interfaz editorial clara, con fondo blanco, superficies discretas, texto sólido y un acento dominante por superficie. Campus y examen utilizan rojo profundo; OS conserva su rojo actual; TERM mantiene su azul. La consistencia debe venir de la tipografía, ritmo, jerarquía, estados y componentes compartidos, no de recolorear todo de una vez. [R-DESIGN] [R-CSS] [R-OS-CSS] [R-EXAM-CSS] [R-TERM-CSS]

| Token | Campus y examen | OS | TERM |
|---|---|---|---|
| Fondo principal | `#ffffff` | `#ffffff` | `#ffffff` |
| Superficie secundaria | `#f7f6f4` | `#f5f6f8` | `#f4f7fb` |
| Texto | `#23252b` | `#20242b` | `#152c43` |
| Texto secundario | `#555b66` | `#565e69` | `#53677c` |
| Acento | `#b0142f` | `#a61932` | `#075cc6` |
| Enlace/hover profundo | `#870b23` | conservar contraste del componente | `#084a9a` |
| Borde de superficie | `#dedfe3` | `#dce0e5` | `#dbe4ed` |

Usa fuentes del sistema y la pila existente. TERM enumera Inter como preferencia, pero no debe añadir una descarga de fuente remota. El código usa monospace local. No incorporar logotipos universitarios, sellos de certificación, fotografías de alumnos, neón, lluvia de código ni recursos de terceros sin licencia y atribución verificadas.

Propuesta de escala común: espaciado 4/8/12/16/24/32/48/64 px; texto de lectura 16–18 px, interlineado 1,65–1,8, ancho aproximado 68–76 caracteres; títulos H1 fluidos entre 32 y 52 px; H2 entre 24 y 32 px; H3 entre 20 y 24 px. Usa el tamaño mayor solo cuando la longitud del título y el viewport lo permitan. Conserva radios moderados de 5–10 px. Una sombra ligera puede separar un panel flotante; no sustituye un borde ni la jerarquía.

Cada vista tiene una acción principal identificable. Las secundarias usan borde o estilo discreto. Las acciones que reemplazan o eliminan datos quedan separadas del avance normal. Los números siempre llevan unidad: «7 de 20 respondidas», «25:00 de foco», «3 de 18 vistas revisadas». El porcentaje solo resume el registro que lo calcula.

### Componentes que deben quedar definidos

| Componente | Variantes y estados necesarios |
|---|---|
| Cabecera y navegación | ES/EN donde exista, ruta actual, menú cerrado/abierto, foco visible, texto largo |
| Tarjeta de recorrido o módulo | Sin comenzar, en curso y completado por el alumno; título, objetivo y CTA |
| Navegación de lección | Anterior, siguiente, posición, fin de lección; volver al índice |
| Bloque de lectura | Encabezados, listas, tablas, código, enlaces internos, fuentes y contenido largo |
| Bloque de práctica | Entorno, orden copiable, explicación, resultado orientativo, verificación, reversión |
| Panel de guía | Cerrado, abierto, ayuda disponible, sin guía para la duda, entorno incompatible |
| Opción de examen | Normal, hover, foco, elegida, correcta, incorrecta y bloqueada |
| Feedback | Correcta/incorrecta/sin responder, explicación y enlace; texto además de color |
| Progreso | Vacío, parcial, finalizado; distintas unidades y superficies sin mezclarlas |
| Guardado local | Disponible, pendiente, memoria temporal, copia corrupta y cambio en otra pestaña |
| Diálogo | Confirmar sustitución, finalizar con pendientes, importar, cancelar y devolver foco |
| Laboratorio TERM | No configurado, enlace externo autorizado y, solo si se habilita, iframe autorizado |
| Estado de carga/error | Cargando, archivo no disponible, datos inválidos, recurso inexistente y reintentar |

## 6. Pantallas de referencia y adaptación

Construye y revisa una muestra real de cada superficie antes de extender estilos. Usa `M02`, `D41`, `OS-L01` y `m01-l01`, con sus cuerpos reales, y las preguntas adjuntas. No recortes explicaciones largas para que encajen en una composición.

En escritorio a 1440 px, conserva navegación lateral y una columna de lectura limitada. Un panel de ayuda puede ocupar una columna secundaria si no comprime el enunciado o el código. A 1024 y 768 px, la navegación puede plegarse y la ayuda se convierte en panel accesible. A 390 y 320 px, usa una columna, botones de altura mínima 44 px, opciones a ancho completo y tablas/código con desplazamiento dentro del bloque. Evita dos barras fijas que oculten contenido o teclado.

Mantén la ruta y el estado al abrir/cerrar un panel o girar la pantalla. Las cabeceras adaptables necesitan margen de desplazamiento según su altura real. Un título enfocado debe quedar visible. En presentación, conserva desplazamiento interno para contenido largo y una salida accesible aunque el navegador deniegue fullscreen.

## 7. Accesibilidad como criterio de aceptación

El objetivo es cumplir los criterios aplicables de WCAG 2.2 AA; una maqueta, un cálculo de contraste o unas pruebas automáticas no constituyen certificación. Diseña semántica y comportamiento desde el principio. [F-WCAG]

Usa `header`, `nav`, `main`, títulos jerárquicos y un enlace para saltar al contenido. Marca ruta actual con `aria-current`. El examen usa `fieldset`, `legend`, radios nativos y etiquetas completas: se responde con teclado, sin arrastrar ni depender del ratón. Comunica feedback en una región `aria-live` y lleva el foco de forma previsible al resultado de la selección. No hagas que el lector de pantalla anuncie el temporizador cada segundo.

Los diálogos tienen título, descripción, foco inicial seguro, cierre por Escape cuando corresponda y devolución al control que los abrió. Nunca dejar el foco detrás de un panel modal. Al bloquear opciones tras la primera respuesta, conserva una representación textual legible de la elección y la correcta.

Comprueba contraste de texto normal al menos 4,5:1 y texto grande al menos 3:1, con sus excepciones aplicables. Controles y estados esenciales necesitan contraste no textual adecuado. El foco será claramente visible. Mantén el producto usable a 200 % de texto, con reflujo a 320 px y con reducción de movimiento. Los objetivos táctiles de 44 px son una decisión de diseño del producto; no los describas como el umbral único de WCAG 2.2 AA.

## 8. Contrato del examen de 100/20

La única fuente editable del banco está en `formacion/introduccion-informatica/banco-preguntas.json`. El archivo adjunto es una copia íntegra de esa fuente para el handoff. Cuando se integre una edición, modifica la fuente canónica y regenera; no mantengas dos bancos editables. `banco-preguntas.schema.json` describe el formato y enumera reglas semánticas adicionales.

| Tema | Preguntas | Lectura principal |
|---|---:|---|
| T01 · Informática, evolución y aplicaciones | 6 | D26 y D27 |
| T02 · Representación y aritmética binaria | 12 | D41 |
| T03 · Codificación y compresión multimedia | 10 | D41 |
| T04 · Lógica digital y álgebra de Boole | 10 | D42 |
| T05 · Arquitectura, CPU e instrucciones | 8 | D43 |
| T06 · Memoria, almacenamiento e integridad | 10 | D43 |
| T07 · Buses, periféricos y entrada/salida | 6 | D43 |
| T08 · Sistemas operativos y procesos | 8 | D44 |
| T09 · Memoria virtual, archivos y permisos | 8 | D44 |
| T10 · Software, licencias y mantenimiento | 6 | D44 |
| T11 · Redes, protocolos y protección | 8 | D45 |
| T12 · Virtualización, cloud y tecnologías actuales | 8 | D45 |

La aplicación valida 100 IDs únicos `INF-001`…`INF-100` en esta edición, los doce temas, cuatro IDs de opción a/b/c/d, textos distintos, una clave correcta, explicación y enlace interno válido. El muestreo usa Fisher–Yates con aleatoriedad criptográfica y selecciona veinte sin reemplazo dentro del intento. Las opciones se barajan preservando su ID. Intentos diferentes pueden compartir preguntas; veinte preguntas al azar no garantizan cubrir los doce temas. No introducir muestreo por cuotas bajo la misma etiqueta «aleatorio» sin documentar el cambio.

El estado tiene `schemaVersion`, `bankRevision`, `questionIds`, `optionOrders`, `answers`, `currentIndex`, `status`, `startedAt` y `finishedAt`. La corrección se deriva del banco, nunca de una puntuación persistida. La revisión del banco es una comprobación de compatibilidad, no una firma contra manipulación. El banco y las soluciones son públicos porque este es un ensayo formativo. [R-EXAM-MODEL]

Preserva la coordinación entre pestañas: combinar respuestas compatibles, conservar la primera guardada ante conflicto, no reabrir un intento finalizado y no permitir que una pestaña antigua sobrescriba una selección nueva o resucite una eliminada. La implementación actual usa Web Locks y un cambio explícito de tarea antes de liberar la escritura de localStorage. No simplificarlo a read/merge/write sin coordinación. Si faltan almacenamiento o coordinación, informar y continuar en memoria, sin sobrescribir la copia compartida.

## 9. Persistencia y privacidad

La política mantenida está en [Privacidad y asistencia con IA](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/security/PRIVACY-AND-AI.md) y la revisión técnica en [Security review](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/security/REVIEW-2026-10-18.md). Esta sección concreta sus consecuencias para la interfaz; los cambios de proveedor, finalidades y controles se documentan allí. [R-PRIVACY] [R-SECURITY]

| Superficie | Clave actual | Naturaleza |
|---|---|---|
| Campus | `fundamentos-ciberseguridad:progress:v1` | Lecturas, revisión, prácticas y notas; exportación/importación JSON |
| Aula OS | `smartkea.os.study.v1` | Persistencia opcional; marcas, sesiones declaradas/medidas y objetivo |
| Examen | `fundamentos-ciberseguridad:exam:v1` | Un intento y su selección/respuestas; reanudación explícita |
| TERM | `smartkea.term.progress.v1` | Lecciones, pasos, quiz, evidencia autodeclarada y notas |
| Rutas por perfil | `smartkea.learning-paths.v1` | IDs de etapas y `recordId` técnico; guardado opcional, sin notas ni identidad personal |

Las claves son independientes y dependen del origen. TERM usa canónicamente `www.smartkea.com`, mientras el campus usa `smartkea.com`; el almacenamiento no se comparte entre esos orígenes aunque aparezcan bajo una misma marca. La navegación en una pestaña no debe llevar a otra a una lección diferente. El registro OS diferencia identidad de vida (`recordId`) y reinicio dentro de esa vida (`generation`); borrar y recrear no permite recuperar sesiones obsoletas. Una importación es una decisión explícita del alumno con revisión previa. Conserva límites de tamaño y validaciones del código. [R-STATE] [R-OS-MODEL] [R-TERM-STATE]

**Rutas por perfil.** Conserva `schema: 1` y añade únicamente la identidad técnica de vida `recordId`: una copia anterior sin ese campo se interpreta como `legacy`; crear una copia tras su eliminación genera un UUID. Cada marca o desmarca se reconcilia con el registro vigente bajo Web Lock exclusivo, conservado hasta un cambio de tarea para publicar el almacenamiento de Firefox. La última intención local de cada etapa sigue visible mientras terminan las escrituras anteriores. Cancelar el guardado invalida callbacks pendientes; una eliminación antigua solo puede retirar la vida que conocía. Si otra pestaña elimina o recrea el registro, las marcas pendientes quedan en la visita y requieren activar el guardado otra vez. Una pestaña que no lo ha activado no adquiere ese consentimiento por un evento remoto. Sin Web Locks o almacenamiento, muestra que el borrador es temporal; no sobrescribas la copia compartida ni afirmes haberla eliminado si no fue posible. [R-PATHS-UI] [R-PATHS-BROWSER]

**TERM.** Mantén el modelo `createProgressStore`: compara los bytes guardados con el snapshot leído por la pestaña y escribe bajo Web Lock, con adquisición limitada a cinco segundos. Si detecta una copia diferente o corrupta, conserva ambos estados y muestra «Exportar esta sesión», «Descargar copia guardada» y «Recargar copia guardada». No inventes una mezcla automática de notas o respuestas: la recuperación se decide explícitamente. Importar o reiniciar usa los bytes `expectedRaw` observados al abrir la confirmación; un cambio posterior impide sustituir la copia. Las notas y mensajes indican si el guardado tuvo éxito o si los cambios solo existen en memoria. Sin almacenamiento o Web Locks, el alumno puede seguir y exportar. La navegación actualiza `lastLesson` en memoria y lo incorpora en la siguiente edición o exportación; abrir una lección no exige escribir todo el registro. [R-TERM-STATE] [R-TERM-UI] [R-TERM-PERSISTENCE] [R-TERM-VALIDATION]

No recopilar correos, nombres, identificadores académicos, claves, capturas privadas o telemetría. No incluir conversaciones, Gmail, Drive ni propuestas privadas dentro del repositorio o los adjuntos públicos. Los archivos de progreso que exporta un alumno pueden contener sus notas: no adjuntarlos a Make como datos de demostración. Usa un contexto limpio y datos sintéticos en pruebas.

Un enlace de lección comparte una ruta. La transferencia de progreso del campus es otra función y puede transportar un snapshot sin notas; no equivale a una cuenta ni a autenticación. No extender esa transferencia al registro OS, al examen o TERM sin un contrato separado. Eliminar un registro debe indicar cuál elimina y no ejecutar `localStorage.clear()` para borrar todos los recorridos.

## 10. Guía asistida: alcance implementable ahora

La opción preferente es una **Guía de estudio local**, integrada en la lección, con acciones acotadas: «Explicar el concepto», «Dar una pista», «Revisar el entorno», «Qué evidencia necesito» y «Qué repasar». Las respuestas proceden del contenido y reglas explícitas; muestran el título y enlace de la fuente. No simular conversación con un modelo ni escribir «la IA ha comprobado tu equipo».

Propuesta de contrato: entrada con superficie, idioma disponible, ID de unidad, fase y acción solicitada; salida con texto curado, referencias y una siguiente acción. Puede utilizar los fallos del intento actual para ordenar lecturas. Ante contexto inválido, guía ausente o idioma no disponible, devuelve una explicación honesta y un enlace de estudio. No generar órdenes desde el texto libre del estudiante. No guardar nuevas preferencias sin explicarlas.

Una futura asistencia generativa queda fuera de esta entrega activa. Requeriría un servicio real, manejo de credenciales en servidor, controles de acceso y coste, consentimiento específico y evaluación pedagógica. Su diseño no habilita cuentas, endpoints, tokens ni envío de notas. Cualquier interfaz exploratoria de esa opción debe figurar como propuesta y permanecer desactivada en la versión actual.

## 11. Datos e implementación

El campus de producción es HTML/CSS/JavaScript estático, generado mediante Python. No requiere base de datos, API key ni dependencias de producción. Reutiliza los modelos, validadores y estilos antes de duplicar lógica. Si Make utiliza React en su preview, considera esa representación un adaptador de prototipo: no reemplaza automáticamente el generador Python, los módulos vanilla, el staging o el esquema de progreso.

Los catálogos del build son `course.json`, `course.en.json`, `sistemas/course.es.json`, `sistemas/course.en.json`, `examen/questions.json` y el `course.json` de TERM. Usa archivos locales al producto desplegado, sin fetch a GitHub desde el navegador como dependencia de ejecución. Mantén IDs y semántica; deriva la UI de los datos. El inventario adjunto tiene títulos y enlaces de todas las unidades, pero no pretende reemplazar esos cuerpos completos. Las muestras reales sirven para revisar contenido largo mientras se incorpora el conjunto completo desde el repositorio.

Mantén el tratamiento de entradas: validar JSON y longitudes, rechazar IDs desconocidos, representar notas como texto, impedir URLs `javascript:` y evitar HTML de usuario. No añadir CDN, fuentes remotas, analítica, `eval`, ejecución de comandos ni una clave de proveedor en el frontend. La CSP actual limita scripts, estilos y conexiones al propio origen; cualquier cambio necesita una justificación concreta dentro del PR. [R-CATALOG] [R-INTEGRATION]

## 12. Trabajo por entregas en Make

**Primera entrega: orientación y diseño.** Lee los adjuntos. Presenta el mapa de las cuatro superficies, las decisiones existentes que se conservan y las mejoras concretas. Construye la portada, el temario y una lección real con los tokens actuales. Revisa 1440/768/390/320 px. No declarar el curso completo hasta incorporar sus catálogos.

**Segunda entrega: aprendizaje y práctica.** Completa una lectura larga D41, el recorrido OS-L01 y las fases de m01-l01. Incluye entorno, pistas, evidencia, reversión y estados de laboratorio no configurado. Prueba teclado, contenido largo y cambio de idioma donde exista.

**Tercera entrega: examen completo.** Incorpora las cien preguntas adjuntas y reutiliza el modelo. Demuestra selección de veinte, opciones barajadas, corrección, bloqueo, reanudación, nota, repaso, enlaces y nueva sesión. Añade los estados de memoria, copia inválida y pestaña antigua.

**Cuarta entrega: revisión e integración.** Revisa cambios de archivos, rutas, accesibilidad y persistencia. Devuelve el código y el registro de cambios para integrarlo mediante una rama y PR del repositorio canónico. Mantén las pruebas que protegen las decisiones anteriores.

Make permite adjuntar Markdown y JSON como contexto. Para este paquete, comienza con este documento, `producto.json`, `banco-preguntas.json` y `catalogo-publico.json`; incorpora esquema y muestras en la iteración correspondiente. Todos los adjuntos de texto del paquete se mantienen por debajo de 1 MB. [F-ATTACH]

La integración estándar «Push to GitHub» documentada por Figma crea y actualiza repositorios propios de Make, empuja a la rama por defecto y es unidireccional. No puede tratarse como sincronización con este repositorio existente. Utiliza exportación o importación de proyecto por la capacidad disponible y revisa el resultado mediante PR al repositorio canónico. No publicar un repositorio alternativo como si fuera la fuente oficial. Un enlace de preview Make es una revisión de diseño, no el despliegue en Cloudflare. [F-GITHUB]

## 13. Publicación correcta en Cloudflare Workers

El procedimiento mantenido de integración y release está en [REVIEW-AND-RELEASE.md](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/engineering/REVIEW-AND-RELEASE.md). Aplica sus gates y registra allí o en el PR la evidencia; esta especificación no crea un proceso alternativo. [R-ENGINEERING]

Conserva el Worker `fundamentos-ciberseguridad`, el `wrangler.jsonc` de la raíz y `campus/cloudflare.py`. El campo `assets.directory` es `./campus/worker-dist`; el hook de compilación ejecuta `python3 campus/cloudflare.py build`. Los prefijos del campus y TERM se componen en staging. La aplicación es estática: no seleccionar preset Next.js, OpenNext ni inventar un binding `frontend`. [R-WRANGLER] [R-WRAPPER]

Desde la raíz del repositorio, preparar y comprobar sin publicar:

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
python3 campus/cloudflare.py dry-run
```

La preview usa `python3 campus/cloudflare.py preview`; producción usa `python3 campus/cloudflare.py deploy`, cuando el proceso de revisión del repositorio autorice publicar. Las credenciales se gestionan en el entorno del proveedor, nunca en adjuntos, código, JSON del producto o navegador del alumno. La revisión de consolidación fija Wrangler 4.151.1 y su lockfile dedicado en `campus/tooling/package-lock.json`. El wrapper instala con `npm ci --ignore-scripts` y ejecuta el binario local; plan/build/check siguen funcionando offline. Conserva estos wrappers y el lockfile, sin recuperar instrucciones antiguas de npx ni actualizar dependencias incidentalmente durante un retoque visual.

El staging debe conservar lectores sin JavaScript, descargas, catálogos, examen y TERM. `assets.not_found_handling` se mantiene en `404-page`: un archivo ausente devuelve 404, no HTML 200 que parezca un JSON válido. Las cabeceras del campus se aplican a su prefijo y las de TERM al suyo. Solo una configuración explícita del operador puede admitir el origen de la terminal opcional; no abrir `frame-src *`. [R-INTEGRATION] [F-WORKERS]

Tras publicar, verificar la URL real y el `sourceCommit` de `build-info.json` contra el SHA final de main, además de los hashes de los catálogos y banco. Abrir campus, aula OS, examen, TERM y rutas profesionales, ambas lenguas donde existan, lectores, un recurso nuevo, ensayo completo, progreso y descargas. Una compilación local o una preview exitosa no demuestra que producción haya servido esa versión.

TERM incorpora `python3 term/verify_public.py --expected-commit COMMIT_COMPLETO --output term/qa/public-release.json`. Conserva esta auditoría de GET HTTPS: compara el commit limpio, todos los activos del manifiesto, 16 módulos, 48 lecciones, 194 pasos y 96 preguntas, cabeceras, entradas con y sin barra y un 404 real; relee metadatos al terminar para detectar una publicación concurrente. Comprueba los bytes de los activos públicos, no solo el nombre de un archivo o el éxito del build. El verificador no abre ttyd ni acredita acceso a una máquina. [R-TERM-VERIFY] [R-TERM-VALIDATION]

Guardar el commit y artefactos de la versión aceptada para poder volver a publicarla. Una reversión no debe limpiar el almacenamiento del alumno. Cambiar de dominio u origen altera el alcance del almacenamiento: antes debe existir una vía explícita de exportación.

## 14. Criterios de aceptación

La entrega se acepta cuando sus cambios cumplen los siguientes resultados observables, junto con las pruebas actuales del repositorio:

1. Las bases canónicas y rutas.html abren su aplicación y cada enlace del inventario conserva su ID.
2. Se conservan 32 módulos, 96 fichas, 46 recursos, 28 lecciones OS, 48 lecciones TERM, el banco de 100, seis rutas profesionales y 26 etapas; no se mezclan sus métricas. El caso C99-DFIR mantiene sus diez actividades y doce preguntas como ampliación separada.
3. La siguiente acción es visible en cada pantalla y utiliza título y destino reales.
4. Un alumno puede completar aprender → practicar → comprobar → repasar sin depender de cuenta, IA externa o laboratorio aún no vinculado.
5. Cada intento contiene veinte preguntas únicas, opciones a/b/c/d sin pérdida de identidad y una única solución por pregunta.
6. Elegir corrige inmediatamente; una segunda selección, navegación atrás o una pestaña obsoleta no suma puntos.
7. Diez aciertos de veinte producen 5,0; pendientes, fallos y desglose por tema concuerdan con los IDs del intento.
8. Reanudar, sustituir y finalizar tienen estados claros; las confirmaciones necesarias son concretas y cancelables.
9. Dos pestañas no pierden respuestas compatibles ni resucitan un intento eliminado; sin coordinación se usa memoria temporal avisada.
10. Reinicios, borrados, recreaciones e importaciones OS no recuperan sesiones antiguas ni atribuyen una acción a otra lección.
11. Cambiar idioma o abrir un panel conserva ruta y registro; EN no oculta una carga fallida sustituyendo contenidos.
12. Todo el flujo funciona con teclado y foco visible; los diálogos y el feedback se anuncian de forma útil.
13. A 320 px no hay desplazamiento horizontal del documento; tablas y código se desplazan dentro de su bloque.
14. No aparecen solicitudes de analítica, fuentes remotas, API de IA ni conexiones a máquinas no configuradas.
15. Las notas y JSON inválidos no se interpretan como HTML; importaciones respetan los límites y muestran revisión previa.
16. El laboratorio sin endpoint muestra su estado real; una salida orientativa o una marca del alumno no se presenta como ejecución comprobada.
17. La compilación y dry-run funcionan desde checkout limpio; no dependen de carpetas dist ya presentes.
18. La versión real publicada acredita SHA y hashes correctos, cabeceras previstas, MIME adecuado y 404 reales.
19. Dos pestañas de rutas conservan sus marcas compatibles; cancelaciones y borrados no resucitan otra vida del registro. Sin coordinación, las marcas quedan en memoria con aviso.
20. TERM conserva el original ante corrupción o conflicto, distingue el guardado efectivo de la sesión temporal e invalida un reemplazo si cambia la copia durante la confirmación.

Documenta qué pruebas se ejecutaron, sobre qué commit, motor y viewport, y qué limitaciones quedan. No describas una prueba escrita como si hubiera pasado ni una propuesta como función ya desplegada. `producto.json` amplía estos criterios con casos concretos y prioridades.

## 15. Prioridades de mejora

El seguimiento canónico está en [docs/BACKLOG.md](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/BACKLOG.md) y el [issue4 de UX y aprendizaje](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/4). Las prioridades siguientes especifican el trabajo en Make; enlaza sus resultados al backlog existente para evitar dos trackers divergentes. [R-BACKLOG]

**P0 · Integridad.** Mantener rutas, bancos, idiomas, guardado y validadores; resolver cualquier regresión de navegación, teclado o corrección antes de pulir decoración. Todas estas protecciones son condiciones de integración.

**P1 · Orientación.** Mostrar continuación real, objetivo de la sesión, enlace a la guía D46 y próximos pasos por recorrido. Agrupar acciones secundarias para reducir ruido. Añadir guía local por reglas solo cuando su contenido y fallback estén completos.

**P1 · Claridad de práctica.** Dar más visibilidad a entorno, predicción, evidencia y recuperación. Mantener «Resultado orientativo» junto a cada salida y estado honesto de ttyd.

**P2 · Consistencia visual.** Compartir escala de espacio, foco, controles y composición; preservar las paletas actuales. Mejorar densidad de tablas, navegación móvil y tipografía de bloques largos mediante cambios acotados.

**Fuera del alcance actual.** Cuentas, OTP, sincronización entre dispositivos, calificaciones oficiales, certificados, vigilancia de estudiantes, asistentes generativos, ejecución automática y nuevos backends. Estas opciones necesitan un encargo y contrato propios; no son requisitos para completar el campus actual.

## 16. Entrega que debes devolver

Devuelve el resultado visible o preview de Make, el mapa de pantallas implementadas y una lista breve de cambios respecto al producto existente. Aporta código exportable y explica cómo trasladarlo a los archivos del repositorio; distingue adaptadores del preview y cambios listos para integración. Incluye evidencias de pruebas, defectos pendientes y el procedimiento de compilación/publicación preservado. No declares que Cloudflare ha cambiado hasta comprobar la URL final y su SHA.

### Fuentes públicas y trazabilidad

Los identificadores `[R-…]` y `[F-…]` resuelven en `producto.json → sources` y en `FUENTES.md`. La plantilla identifica el baseline público 769c1ba y las fuentes nuevas de la consolidación mediante rutas main. El producto JSON exportado registra build, head y referencia pública específicos de cada entrega; el manifiesto conserva las huellas de origen. Los commits locales del manifiesto no son enlaces publicados. Las referencias F apuntan a documentación oficial consultada el 18 de octubre de 2026. Los adjuntos no incluyen mensajes privados ni archivos de progreso de estudiantes.
