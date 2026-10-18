# Introducción a la informática: comprender, practicar y explicar

Esta ruta conecta los fundamentos de primer curso con las prácticas de Linux y ciberseguridad del campus. Empieza por una tarea pequeña, explica el modelo que la hace posible y comprueba el resultado. El material desarrolla los contenidos contrastados con la propuesta docente del **8 de octubre de 2026** y la guía del **9 de octubre de 2026**, mediante explicaciones y ejercicios propios.

La asignatura de referencia tiene **6 ECTS**. El catálogo general M01–M32 ofrece **480 horas planificadas** para un recorrido profesional más amplio: sus módulos son recursos de los que seleccionar actividades, no la carga ni la programación oficial de esta asignatura. La [guía de cobertura](06-guia-cobertura.md) explica la correspondencia y los límites.

## Cómo empezar

1. Abre una terminal de tu laboratorio y completa el diagnóstico inicial de M01. Identifica sistema, shell y directorio de trabajo.
2. Lee [D26: mapa de informática](../itinerario-integral/01-computing.md) y [D27: historia](../itinerario-integral/02-history.md). Explica con tus palabras qué representa, procesa, almacena y comunica un ordenador.
3. Alterna las lecturas de esta carpeta con M02–M10. Antes de ejecutar un ejemplo, calcula su resultado a mano.
4. Conserva en tu cuaderno objetivo, predicción, comando, resultado, explicación y límite. Las prácticas nuevas no necesitan cuentas cloud, claves API ni permisos de administrador.
5. Utiliza el [test de **100 preguntas**](https://smartkea.com/introduccion-ciberseguridad/examen/), con intentos aleatorios de **20**, como ensayo. Consulta la explicación al corregir y vuelve a la lectura correspondiente. Una nota del ensayo no acredita la ejecución de una práctica ni sustituye la evaluación de la asignatura.

## Lecturas

| Recurso del campus | Lectura | Contenidos de referencia | Resultado observable |
|---|---|---|---|
| D41 | [Representación y codificación](01-representacion-codificacion.md) | T02–T03 | Conversiones, aritmética, bytes y estimación de tamaños |
| D42 | [Lógica digital](02-logica-digital.md) | T04 | Tabla de verdad, equivalencias y circuito con estado |
| D43 | [Arquitectura, memoria y entrada/salida](03-arquitectura-memoria-es.md) | T05–T07 | Recorrido de una instrucción, inventario y restauración |
| D44 | [Sistemas operativos y software](04-sistemas-software.md) | T08–T10 | Procesos, paginación, ficheros, permisos y procedencia |
| D45 | [Redes, virtualización y nube](05-redes-cloud.md) | T11–T12 | Diagnóstico por capas y responsabilidades de cada servicio |
| D46 | [Guía de estudio y cobertura](06-guia-cobertura.md) | T01–T12 | Selección de prácticas, evidencias y defensa del proyecto |

## Práctica y recuperación

Los bloques de terminal se ejecutan en **Bash o zsh con Python 3.8 o posterior** y los módulos estándar utilizados disponibles; en Windows puede utilizarse una distribución Linux de WSL ya preparada. No se instala software automáticamente. Los ejemplos trabajan en memoria o en un directorio temporal creado por `TemporaryDirectory`, que retira exclusivamente los archivos de ese ejercicio al finalizar. Una consulta del equipo puede devolver valores diferentes de los de otro alumno: hay que interpretar la diferencia.

Los controles `assert` comprueban un resultado concreto. Si fallan, conserva el mensaje y revisa la hipótesis; no elimines la comprobación para conseguir una salida satisfactoria. La demostración local de una propiedad no prueba seguridad completa, disponibilidad en Internet ni recuperación de una infraestructura real.

## Idiomas y mantenimiento

Las seis lecturas incluyen ediciones completas en español e inglés, con referencias comunes. Los delimitadores `ES`, `EN` y `COMMON` permiten que el campus seleccione el idioma. Los IDs D41–D46 son estables y las ampliaciones reutilizan los módulos existentes.

No se redistribuyen correos, adjuntos institucionales ni datos de alumnos. Las fuentes técnicas públicas se identifican al pie de cada lectura. Las decisiones de calendario, ponderaciones y evaluación oficial corresponden a la guía publicada para cada grupo.

## English study route

Begin with the laboratory diagnostic in M01, then read D26 and D27. Alternate D41–D45 with the selected Linux modules and use D46 to check coverage. Each reading contains a complete English teaching edition, worked examples, a bounded local exercise, expected results and assessment criteria. Predict the result before running a command and explain discrepancies afterwards.

The reference university subject carries **6 ECTS**. The wider M01–M32 catalogue has **480 planned hours** and supplies selectable resources; it is not the official workload of that subject. The [Spanish practice bank](https://smartkea.com/introduccion-ciberseguridad/examen/) contains 100 questions and selects 20 per random attempt. Immediate correction supports rehearsal; it does not record official grades or certify laboratory competence. Terminal examples require Bash or zsh, Python 3.8 or later, and the standard modules used by the examples.
