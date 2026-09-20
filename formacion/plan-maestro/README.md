# Plan maestro de ampliación / Curriculum expansion master plan

**Responsable: Wiktor Nykiel · Referencia editorial 1.0 · 18 de septiembre de 2026.**

## Qué es esta entrega

Base de trabajo para ampliar el curso desde introducción real a la informática hasta administración, arquitectura, operación y gestión de la ciberseguridad. Contiene un mapa de **18 áreas y 108 unidades propuestas**, casos, diseños de laboratorio, un modelo de riesgos, correspondencias orientativas de controles y un glosario bilingüe. No equivale a 108 unidades ya impartidas o publicadas en el campus.

La base revisada es **Campus 2.2**, commit `2f8b8d2614638d9a034e1cac92fb16c6e75bb6c5`: 32 módulos M01–M32, 96 fichas y 480 horas planificadas. Esta referencia **no renumera esos módulos, no borra progreso, no modifica el compilador y no suma automáticamente horas**. Las nuevas áreas reorganizan y amplían contenidos que se solapan; antes de asignar una nueva duración se decidirá qué reutilizar, ampliar o convertir en especialización.

## Índice de trabajo

| Documento | Qué resuelve |
|---|---|
| [01 · Mapa curricular](01-mapa-curricular.md) | Secuencia, 18 áreas, unidades, resultados, prácticas y reutilización de módulos existentes |
| [02 · Arquitecturas e infraestructura](02-arquitecturas.md) | De una web estática o WordPress a servicios empresariales, cloud, virtualización y orquestación |
| [03 · Funciones, equipos y NIST CSF](03-nist-equipos.md) | Seis funciones, 22 categorías, responsabilidades, evidencias, herramientas y métricas |
| [04 · Controles y correspondencias](04-controles-correspondencias.md) | Relación razonada CSF–RGPD–ISO 27001–ENS, inventarios y evidencias reutilizables |
| [05 · Gestión de riesgos](05-gestion-riesgos.md) | Método, riesgo inherente/actual/objetivo, cálculos ilustrativos y tratamiento |
| [06 · Laboratorios y proyectos](06-laboratorios.md) | Escenarios guiados, seguridad, evaluación y caso DVWA/Juice Shop orientado a análisis y defensa |
| [07 · Glosario y protecciones](07-glosario-protecciones.md) | Términos ES/EN, finalidad, ejemplo, límites y ficha WAF con productos |
| [08 · Continuación y requisitos del campus](08-continuacion.md) | Orden de implementación; idiomas, móvil/tableta, progreso, enlaces de traspaso y OTP |
| [09 · Fuentes y vigencia](09-fuentes.md) | Fuentes primarias, límites de consulta, versiones y criterios de revisión |
| [English overview](OVERVIEW.en.md) | Resumen y decisiones en inglés; no se presenta como traducción completa del curso |
| [Catálogo del plan](catalogo.json) | Identificadores, unidades, relaciones y estado de desarrollo para futuras herramientas |
| [Ejemplo de riesgo](riesgo-ejemplo.json) | Datos sintéticos y resultados numéricos verificables |

## Modelo docente

Cada unidad desarrollada debe contener: pregunta inicial; objetivos medibles; prerrequisitos; teoría explicada con un ejemplo; vista GUI y alternativa CLI cuando proceda; práctica guiada; reto con menos ayuda; prueba positiva y negativa; evidencia; recuperación; errores frecuentes; autoevaluación; fuentes y limitaciones. El alumno debe poder explicar **qué cambia, con qué permisos, qué registro deja y cómo se comprueba**.

Cuatro niveles separados: **comprender**, **operar con guía**, **operar y verificar con autonomía**, **analizar y decidir**. La lectura desde un móvil acredita lectura, no ejecución de un laboratorio. Una captura de pantalla no demuestra por sí sola una competencia. Los productos comerciales se utilizan como ejemplos de capacidades, no como requisitos de compra ni recomendaciones universales.

## Separación de contenido y ejecución

Las aplicaciones deliberadamente vulnerables nunca se publican con el campus ni dentro de Pages/Workers públicos. El curso podrá enlazar con un laboratorio privado autorizado, pero no ejecutará órdenes generadas por alumnos o IA en un host compartido. Las actividades de seguridad de esta referencia abarcan revisión, pruebas funcionales acotadas, observación y respuesta; no incluyen cadenas de explotación, extracción de credenciales o evasión.

La expresión del encargo «juicybox» se interpreta provisionalmente como **OWASP Juice Shop**. Se conserva esta decisión para no sustituir silenciosamente un nombre ambiguo. Su confirmación puede hacerse al preparar la cohorte; no impide desarrollar el resto del programa.

## Estado y uso en la siguiente interacción

**Hecho aquí:** estructura de referencia, objetivos, diseños, criterios y fuentes. **Pendiente:** desarrollo didáctico integral por unidad, traducción completa ES/EN, integración de las nuevas rutas en la web y validación nativa de cada laboratorio. La lista priorizada está en [08](08-continuacion.md).

No se incorpora nombre, logo, sello ni identidad de una institución educativa. El diseño editorial futuro será claro y accesible, con identidad independiente. No se cambia la licencia del repositorio ni se redistribuyen normas ISO, instaladores o imágenes de terceros.
