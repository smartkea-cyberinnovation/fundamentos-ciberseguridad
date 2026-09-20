# Sistemas operativos, administración y ciberseguridad

**Wiktor Nykiel · Formación independiente en español · Campus 2.2.**

[**Campus web: lectura, presentación y progreso**](../../campus/README.md) · [Desplegar en Cloudflare](../../campus/DEPLOY-CLOUDFLARE.md) · [Cómo estudiar](COMO-ESTUDIAR.md) · [Plan docente](PLAN-DOCENTE.md) · [Inicio práctico](INICIO-RAPIDO.md) · [Laboratorio](LABORATORIO.md)

Aprender a comprender, operar, proteger, automatizar e investigar Linux, Windows y macOS. La GUI sitúa cada objeto del sistema; la terminal permite reproducir y verificar. El curso enlaza decisiones, acciones, evidencias y recuperación.

## Itinerario: 480 horas planificadas

| Bloque | Módulos | Horas | Desarrollo |
|---|---|---:|---|
| Fundamentos y método | M01–M04 | 56 | [Información, hardware, SO, laboratorio, terminal y Git](modulos/01-fundamentos.md) |
| Linux y Bash | M05–M12 | 112 | [Archivos, búsquedas, permisos, servicios, red, copias y scripts](modulos/02-linux.md) |
| Windows, CMD, BAT y PowerShell | M13–M19 | 98 | [Arquitectura, Registro, objetos, NTFS, identidad, eventos y recuperación](modulos/03-windows.md) |
| macOS, Darwin y zsh | M20–M23 | 56 | [APFS, metadatos, preferencias, launchd, red y seguridad](modulos/04-macos.md) |
| Operación y ciberseguridad | M24–M30 | 98 | [Remoto, web/TLS, automatización, logs, DFIR, IOCs y CTI](modulos/05-operacion-seguridad.md) |
| IA desde terminal | M31 | 20 | [Contexto, privacidad y validación supervisada](modulos/06-ia.md) |
| Proyecto integrador | M32 | 40 | [Construir, proteger, investigar y recuperar](CAPSTONE.md) |
| **Total** | **32** | **480** | **168 h teoría · 312 h práctica.** |

Los cuatro primeros bloques suman 322 horas; los transversales, IA y proyecto, otras 158. Se mantienen 96 laboratorios diseñados y 240 sesiones de dos horas. Las rutas abreviadas de 60, 120 y 240 horas están diferenciadas en el plan.

## Leer, presentar y practicar

El [campus](../../campus/README.md) añade un apunte explicativo por módulo, autoevaluación formativa, índice lateral, prerrequisitos enlazados, búsqueda, anterior/siguiente, texto ampliable y notas. El índice completo permite filtrar por bloque, texto y avance, con contador y reinicio. El modo presentación utiliza el mismo contenido, con flechas y pantalla completa. Una versión continua permite lectura sin JavaScript e impresión.

Las 96 fichas se organizan en cinco fases: preparación, ejecución manual, comprobación, evidencia y recuperación. Las ocho guías detalladas R01–R08 del repositorio se integran cuando corresponden. El asistente no es una terminal ni un LLM: guía y contrasta respuestas manuales sobre datos sintéticos, sin ejecutar comandos o consultar equipos.

El progreso distingue lectura, autoevaluación y tres prácticas. Se guarda en el navegador y se exporta/importa en JSON. No mide horas reales, no sincroniza dispositivos y no certifica competencias.

La [lección de despliegue estático](DESPLIEGUE-ESTATICO.md), D21 en la biblioteca, utiliza este campus como actividad de consolidación de M25/M26: compilar, validar, distinguir Pages y Workers, publicar en un proyecto autorizado y comprobar la entrega. No añade horas ni se presenta como un laboratorio nativo ya ejecutado.

## Materiales del repositorio

[Lecciones desarrolladas](lecciones/README.md) · [Guías paso a paso](practicas/README.md) · [Kit oslab.py](kit/README.md) · [Planificación verificable](planificacion/README.md) · [Competencias](COMPETENCIAS.md) · [Evaluación](EVALUACION.md) · [Equivalencias](REFERENCIA-CRUZADA.md) · [Guías rápidas](CHEATSHEETS.md) · [Bastionado](BASTIONADO.md) · [Plantillas](PLANTILLAS.md) · [Fuentes](FUENTES.md) · [Uso responsable](USO-RESPONSABLE.md).

Para el docente: [guía de impartición](GUIA-DOCENTE.md), [banco inicial de preguntas](BANCO-PREGUNTAS.md) y [capstone](CAPSTONE.md). Las respuestas de referencia accesibles aquí son material público de aprendizaje. Cualquier examen reservado o expediente debe custodiarse fuera de este repositorio público.

## Estado de validación y distribución

Las pruebas del campus se ejecutan sobre el curso real y tienen sus propios informes en Actions. El kit integrado conserva su registro histórico en [qa/RESULTADOS.md](qa/RESULTADOS.md). La ampliación anterior `labkit.py` es otro conjunto; no mezclar sus datasets o sumar sus pruebas como cobertura única.

No se afirma haber ejecutado los 96 laboratorios completos ni validado los scripts nativos Windows/macOS, Docker/Compose/Swarm, modelos de IA o una cohorte. Cada práctica necesita su entorno y registro de prueba. El campus estático no depende de la aplicación de la raíz.

El repositorio es público. Un despliegue requiere configurar el producto de Cloudflare y comprobar su URL; no se deriva de la visibilidad de GitHub. La [guía actual](../../campus/DEPLOY-CLOUDFLARE.md) distingue Workers Static Assets del proyecto Pages. Ver también [Publicación](PUBLICACION.md), [Validación](VALIDACION.md) y [Edición del campus](../../campus/EDICION.md).

No se asigna automáticamente una licencia nueva. Los materiales propios y las referencias conservan sus derechos. No se redistribuyen instaladores, imágenes ni manuales completos de terceros.
