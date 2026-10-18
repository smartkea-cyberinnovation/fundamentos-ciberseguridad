# Aula de Sistemas Operativos / Operating Systems classroom

[Empezar en español](https://smartkea.com/introduccion-ciberseguridad/sistemas/?lang=es) · [Start in English](https://smartkea.com/introduccion-ciberseguridad/sistemas/?lang=en) · [Cómo estudiar](../../docs/ESTUDIAR.md)

El aula separa una idea por vista y alterna comprensión, explicación propia y práctica. No es una terminal remota. Contiene cuatro lecciones comunes y ocho por Linux, Windows y macOS. Las 28 lecciones reutilizan el trabajo previo de sistemas y tienen edición completa ES/EN.

## Itinerario

| Ruta | Secuencia |
|---|---|
| Común C01–C04 | Función del SO; contexto y laboratorio; diagnóstico; entrega y decisiones |
| Linux L01–L08 | Archivos; identidad/permisos; procesos/servicios; almacenamiento; redes/SSH; Bash; logs; bastionado/recuperación |
| Windows W01–W08 | Contexto; archivos/ACL/perfiles; PowerShell; CMD/BAT; servicios/eventos; AD/GPO; redes/navegación; protección/recuperación |
| macOS A01–A08 | Darwin/APFS; zsh; identidad/TCC; launchd; red; seguridad de plataforma; Unified Log; copias y operación |

Cada lección empieza por una pregunta. Tres conceptos se intercalan con tres microprácticas; después aparecen esquema, ejemplo, preparación, pasos de laboratorio, autoevaluación, evidencia, recuperación y entrega. El cierre exige explicar resultado, opciones, impacto, límites y siguiente acción.

## Cómo usar el asistente

Marca comprobado, repaso o bloqueo de entorno de forma explícita. El cuestionario explica la respuesta. Las operaciones nativas no se marcan realizadas sin tu confirmación de ejecución en el SO correspondiente. La aplicación no certifica que esa declaración sea cierta.

«Mi entorno» distingue Mac Intel/Apple Silicon, Windows/Linux x64/ARM y tableta. Consulta arquitectura, compatibilidad, licencia, imagen oficial y recuperación antes de instalar. El alumno con una tableta puede leer y predecir; necesita un equipo o laboratorio autorizado para completar las operaciones nativas.

El foco es de 25 minutos y la pausa de cinco; ambos empiezan manualmente. Al cambiar de vista, ocultar página, detectar suspensión o cinco minutos sin interacción, se pausa para evitar atribuir actividad no observada. El trabajo externo se añade como tiempo declarado, no medido. El bloqueo es un subconjunto del foco y no se suma dos veces.

No existe una medida fiable de «tiempo no estudiado» a partir de esta web. El panel muestra objetivo restante del día, puntos revisados y una estimación visible de esfuerzo pendiente; no infiere atención ni promete una duración exacta.

El registro OS es independiente del campus general. Persistencia opcional en un único origen; exportación/importación JSON con confirmación. Comparte una URL para abrir una lección. Las notas de problema están solo en la pestaña y se descargan aparte. No hay cuentas, OTP, analítica remota o sincronización automática.

## Fuentes y edición

- `schema.py`: contrato explícito de contenido bilingüe.
- `common.py`, `linux.py`, `windows.py`, `macos.py`: fuentes docentes.
- `sources.py`: referencias primarias y nombres de consulta.
- `build.py`: genera datos y lectores sin JavaScript bajo `sistemas/`.
- `study.js`, `model.js`, `environment.js`: navegación, registro, temporizador y orientación.
- `study.css`: diseño claro, presentación y reflujo.

Los IDs y comandos se mantienen entre idiomas. Para ampliar, añade contenido que declare objetivo, entorno, fuente, evidencia y recuperación. No cambies silenciosamente el significado de un ID ya usado por el progreso.

## Pruebas y límites

Consultar [QUALITY](../../docs/QUALITY.md), [SECURITY](../../SECURITY.md) y el workflow de esta versión. La existencia de una prueba no demuestra que haya pasado. Las pruebas web no equivalen a ejecución nativa en Windows/macOS, ni a aceptación de una versión particular de un hipervisor. No se atribuye aval universitario o de consultoría ni conformidad WCAG universal.

## English

Follow Shared Foundations, then your OS path. Each lesson alternates a concept with a micropractice, then moves through a diagram, worked example, lab setup, steps, self-check, evidence, recovery and professional handover. The assistant tracks explicit self-checks, review needs and environment blockers. It never runs commands.

Optional 25/5 focus and break intervals record activity, not attention. Hidden pages, long scheduling gaps, inactivity and view changes pause the timer. External work is declared separately. Progress persistence is optional and separate from the older campus record. JSON transfer requires confirmation; lesson links carry no credentials. Problem notes stay in the tab and are downloaded separately.

Use My environment for architecture-aware, officially sourced preparation. A Windows ARM guest is not an x86 server and a container is not a native macOS lab. Full-window presentation works independently of whether native fullscreen is granted by the browser. See the release's actual test evidence for accepted engines and viewports.
