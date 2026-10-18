# Integración del campus y cobertura de Introducción a la Informática

Fecha de revisión: 18 de octubre de 2026. Repositorio: `smartkea-cyberinnovation/fundamentos-ciberseguridad`. Base observada: `b2429fd19f52b9269e6f33362755a9f5c42b96b7`.

## Ramas revisadas

| Rama existente | Referencia observada | Decisión |
|---|---|---|
| `main` | `b2429fd` | Base vigente; conservar curso TERM, documentación y correcciones recientes. |
| `codex/repair-campus-deployment-20260922` | `ac3e6a9` | Ya integrada en el historial de main. |
| `codex/stabilize-webkit-header-20260922` | `212f090` | Ya integrada; conservar corrección de cabecera. |
| `feat/term-linux-course` | `d593b8a` | Ya integrada; conservar también sus correcciones posteriores de rutas. |
| `curriculum-v3-introduccion-informatica-ciberseguridad` | `85d3d94` | Contenido integrado mediante squash en PR #3; reconciliar ascendencia conservando las correcciones de main. |
| `feat/os-classroom-redesign-20260921` | `532e29f` | Contenida en os-study-assistant; su ascendencia se incorpora con esa rama. |
| `feat/os-study-assistant-20260921` | `2bf0af1` | Integrar 28 lecciones, aplicación OS, pruebas y guías de estudio. |

No había PR abiertos en la primera observación. Las ramas existentes se conservan; integrar su historial no requiere borrarlas ni reescribir sus commits. La versión completa mantiene los IDs del catálogo general y el formato de su progreso.

## Contraste curricular

Se contrastaron la propuesta docente del 8 de octubre, la guía remitida el 9 de octubre y la planificación anterior de septiembre. La guía de octubre proporciona el mapa de doce temas. La revisión incorpora contenido propio y no publica mensajes, adjuntos ni enlaces privados de coordinación. No atribuye aprobación formal a una propuesta de ponderaciones o planificación.

El resultado se encuentra en [D46 · Guía de cobertura](../../formacion/introduccion-informatica/06-guia-cobertura.md). D26–D40 y M01–M32 conservan su significado; D41–D46 completan representación, codificación, lógica, arquitectura, memoria, entrada/salida, sistemas, software, redes y cloud con ejemplos y prácticas. La asignatura de referencia de 6 ECTS se distingue del catálogo ampliado de 480 horas.

## Cambios funcionales

- Aula OS en `/introduccion-ciberseguridad/sistemas/`: 28 lecciones y 84 conceptos en ES/EN, microprácticas, orientación de entorno y temporizador 25/5.
- Seis lecturas bilingües nuevas, D41–D46, con cobertura trazable de los doce temas.
- Banco de 100 preguntas en español y sesiones aleatorias de 20, cuatro opciones y corrección inmediata.
- Reanudación local validada, puntuación recalculada y repaso por tema; no se utiliza la nota como certificación.
- Navegación desde portada y menú, documentación de estudio y mantenimiento separadas.

## Correcciones de integración

El validador de release resuelve índices de directorio y activos relativos desde cada HTML. Las fuentes nuevas se incluyen en el watcher y en la comprobación de procedencia. Los artefactos de CI se crean fuera de las fuentes para que no falseen el estado limpio. Se preservan versión dinámica, TERM, CSP y las correcciones WebKit de main.

La revisión del aula corrige navegación de presentación mediante teclado, visibilidad de resultados filtrados y consulta de versión de PowerShell. Las pruebas correspondientes verifican comportamiento y no solo presencia de texto.

## Publicación y evidencia

La base de producción observada el 18 de octubre servía `b2429fd…`; el aula OS todavía devolvía 404. Workers Builds tenía un check satisfactorio asociado a ese commit y el campus y TERM declaraban la misma procedencia.

La aceptación final se registra en el PR y en las ejecuciones de GitHub Actions de la versión integrada. Tras fusionar, el check de Workers y los `build-info.json` públicos deben identificar el commit definitivo. El manifiesto y el SHA-256 del banco permiten contrastar lo servido con las fuentes. Una compilación local, una preview o un check de otro commit no se presentan como producción actualizada.

Pruebas necesarias: compilador, contratos, modelo de examen, conservación de progreso, navegadores de campus/aula/test, runtime local de Workers y comprobación HTTP de la publicación. La ejecución de las interfaces no acredita que se hayan realizado las prácticas nativas del alumno en Windows, macOS o Linux.

## Revisión posterior a la integración

La revisión de [PR #10](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/10) identificó cinco casos adicionales que se verifican con regresiones específicas:

- Dos pestañas del mismo intento conservan las respuestas ya registradas, y una pestaña antigua no puede recuperar un intento sustituido o volver a abrirlo tras finalizar.
- Reiniciar el registro del aula OS propaga el reinicio a otras pestañas; sus marcas y sesiones anteriores no reaparecen al guardar.
- Las fechas futuras de una copia del aula no pueden impedir una edición posterior.
- Un fallo de carga inicial del aula ofrece reintento y lectura continua; un cambio de idioma fallido conserva el selector del idioma que sigue visible.
- Las siete referencias compartidas de D46 se conservan también en inglés, incluidos sus enlaces internos a D27–D29 y los de las diapositivas. La navegación mantiene el idioma elegido.

La aceptación definitiva utiliza el último commit de main, incluidos estos ajustes, y vuelve a contrastarlo con los archivos públicos de Cloudflare.
