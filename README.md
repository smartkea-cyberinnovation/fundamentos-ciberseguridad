# SmartKEA · Aprende informática y ciberseguridad

**Comprende una idea. Comprueba un ejemplo. Resuelve una tarea. Explica la evidencia.**

[Campus](https://smartkea.com/introduccion-ciberseguridad/) · [Aula de Sistemas Operativos](https://smartkea.com/introduccion-ciberseguridad/sistemas/?lang=es) · [English classroom](https://smartkea.com/introduccion-ciberseguridad/sistemas/?lang=en) · [Guía de estudio](docs/ESTUDIAR.md)

Este repositorio es tu mapa de aprendizaje, cuaderno de referencia y biblioteca de prácticas. Puedes empezar sin instalar la aplicación: abre el campus, elige una lección y comprueba sus prerrequisitos. Para las prácticas nativas utiliza un entorno propio del curso; leer una explicación no equivale a haber ejecutado el ejercicio.

## Empieza por aquí

| Tu situación | Primer paso | Qué debes poder demostrar |
|---|---|---|
| Empiezas desde cero | Aula de Sistemas: **Fundamentos comunes C01–C04** | Explicar aplicación, proceso, SO, identidad, archivo y evidencia |
| Quieres administrar Linux | Recorrido Linux L01–L08 | Archivos, permisos, servicios, red, Bash, logs y recuperación |
| Quieres administrar Windows | Recorrido Windows W01–W08 | CMD/BAT separados de PowerShell, ACL, servicios, AD y controles |
| Quieres administrar macOS | Recorrido macOS A01–A08 | zsh, APFS, permisos/TCC, launchd, red, protección y recuperación |
| Vienes con móvil/tableta u otro SO | **Mi entorno** en el aula | Ruta compatible de práctica o bloqueo de entorno explícito |
| Necesitas el mapa general | [Itinerario integral](formacion/itinerario-integral/README.md) y [plan maestro](formacion/plan-maestro/README.md) | Seleccionar objetivos y sus dependencias, sin intentar hacerlo todo a la vez |

## Cómo estudiar una lección

1. **Define tu objetivo.** Lee la pregunta inicial y predice un resultado antes de abrir la solución.
2. **Comprende un concepto.** Una vista contiene una idea principal. El esquema no sustituye la explicación, sino que conecta sus piezas.
3. **Haz la micropráctica.** Explica la idea sin mirar y di qué observarías para comprobarla. Marca lo que necesitas repasar.
4. **Trabaja el ejemplo y la práctica.** Verifica sistema, versión, identidad y ruta. Ejecuta manualmente sobre datos ficticios; compara resultado esperado y observado.
5. **Cierra profesionalmente.** Conserva evidencia mínima, explica el límite de tu conclusión y comprueba la recuperación. Indica la siguiente acción o la pregunta que sigue abierta.

No avances solo porque el botón lo permite. La marca «lo he comprobado» es una declaración tuya, no una certificación. Una autoevaluación correcta debe poder explicarse; un bloqueo de entorno se registra aparte, sin penalizarlo como falta de capacidad.

## Planifica una sesión, no una carrera contra el reloj

El aula ofrece **foco de 25 minutos y pausas de 5**, ambos de inicio manual. Una primera propuesta es un ciclo para entender y otro para practicar y explicar; adáptala a tu experiencia. La preparación de una VM puede necesitar una sesión separada. No se impone una duración nueva al itinerario.

El panel distingue estudio registrado, práctica, pausas y tiempo de problema. El bloqueo es parte del tiempo de foco, no se suma dos veces. Al ocultar la página se pausa; suspensiones y huecos grandes no cuentan. El trabajo fuera del navegador puede declararse por separado. No se infiere cuánto tiempo «no estudiaste» ni se vigila tu actividad fuera del aula.

Si llevas varios intentos sin aprender nada nuevo, abre **Resolver un problema**: esperado, observado, hipótesis, una prueba y siguiente acción. La nota de ayuda se descarga aparte; no guardes secretos o datos personales.

## GitHub y web: dos entradas al mismo trabajo

| Necesidad | Recurso |
|---|---|
| Estudiar con una idea por vista | [Aula OS](https://smartkea.com/introduccion-ciberseguridad/sistemas/) |
| Leer o imprimir sin JavaScript | Lectura continua ES/EN, enlazada desde el aula |
| Consultar las lecciones fuente | [Fuentes de Sistemas Operativos](campus/os_classroom/README.md) |
| Laboratorio original y guías ampliadas | [Material de sistemas](formacion/sistemas-operativos/README.md) |
| Vocabulario, bibliografía, itinerario y ecosistema | Índice y biblioteca del campus; [plan maestro](formacion/plan-maestro/README.md) |
| Aprender a documentar y entregar resultados | [Método de estudio y resolución](docs/ESTUDIAR.md) |

Los IDs anteriores M01–M32, L01A–L32C y los recursos de biblioteca se conservan. El aula OS utiliza IDs propios OS-C/L/W/A para una secuencia didáctica más clara; no suma sus lecturas a las horas históricas del catálogo ni transfiere automáticamente antiguas marcas a competencias nuevas.

## Continuar y compartir

Compartir una lección abre la misma vista e idioma, sin enviar credenciales. El registro del aula puede guardarse **por elección** en el navegador y exportarse/importarse como JSON para cambiar de equipo. Es independiente del progreso del campus general: cada exportación identifica su curso y no se puede aplicar al otro por error. No hay cuenta ni sincronización automática.

Las notas de problemas permanecen en la pestaña y solo salen mediante descarga explícita. Exporta el registro antes de cambiar de origen, borrar almacenamiento o usar otro navegador. El modo privado puede no conservar datos al cerrar.

## Para docentes

Expón una idea, pide una predicción y alterna con una actividad breve. En presentación la idea central ocupa la vista y la explicación se abre aparte. Hay modo de ventana completa incluso si el navegador rechaza pantalla completa nativa. Verifica accesibilidad y el hardware real del grupo antes de impartir; una emulación no sustituye un iPad físico.

Utiliza la [rúbrica de calidad](docs/QUALITY.md): comprensión, comprobación, seguridad, evidencia, recuperación y comunicación. El curso no está afiliado a ninguna universidad o consultora ni promete una certificación automática.

## English · How to use this course

Start with Shared Foundations C01–C04, then choose Linux, Windows or macOS. Each concept is followed by a short retrieval task; the worked example leads to a native lab with expected outcomes, evidence and recovery. Use the environment guide when your device cannot run the required OS. A simulation is not a completed native lab.

Plan an optional 25-minute focus interval and a five-minute break. Time is recorded activity, not proven attention or competence. Hidden pages pause; external practice is declared separately. Record expected/observed results, hypotheses and one safe test when stuck. Finish with a concise, evidence-based handover.

The classroom supports English throughout. Local storage is optional; JSON export/import transfers its own learning record without accounts or automatic synchronization. The earlier campus record remains separate and unchanged.

## Documentación para mantener el proyecto

El alumno no necesita desplegar para estudiar. La operación técnica se mantiene separada:

[Despliegue](DEPLOY.md) · [Seguridad y datos](SECURITY.md) · [Estado de licencia](LICENSE.md) · [Calidad y aceptación](docs/QUALITY.md) · [Migración y procedencia](docs/MIGRATION.md) · [Edición técnica](campus/EDICION.md)

**Autoría:** Wiktor Nykiel · SmartKEA. La visibilidad pública no concede por sí sola una licencia adicional sobre materiales propios o de terceros.
