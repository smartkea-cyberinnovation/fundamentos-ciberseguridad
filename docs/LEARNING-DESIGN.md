# Diseño de aprendizaje del campus

## Principio rector

El campus debe ayudar al alumno a **comprender, practicar, comprobar, explicar y transferir** un concepto. La navegación, el progreso y la interfaz son medios; el resultado es evidencia de aprendizaje.

## Unidad mínima de experiencia

Cada vista docente debe intentar responder una sola pregunta principal y contener, en este orden:

1. **Qué vas a poder hacer.**
2. **Qué necesitas saber antes.**
3. **Concepto.**
4. **Ejemplo o demostración.**
5. **Micropráctica segura.**
6. **Comprobación inmediata.**
7. **Error frecuente y cómo diagnosticarlo.**
8. **Evidencia que debes conservar.**
9. **Siguiente concepto o ampliación.**

Un tema largo debe dividirse en vistas enlazadas en lugar de convertirse en una pared de texto.

## Ciclo de estudio

Ciclo recomendado, configurable:

- 2 min: definir el objetivo de la sesión;
- 20–25 min: trabajo concentrado;
- 3–5 min: recuperación activa sin mirar apuntes;
- 5 min: micropráctica o explicación;
- pausa breve;
- al terminar un bloque: registrar evidencia y dudas.

El temporizador debe ayudar, no penalizar. El alumno puede cambiar duración, pausar y continuar. Debe distinguirse tiempo de sesión, tiempo efectivo de estudio y tiempo bloqueado en un problema.

## Regla de atasco

El campus debe enseñar a diagnosticar antes de dar la solución:

1. reproducir el problema;
2. leer el mensaje exacto;
3. identificar qué cambió;
4. formular una hipótesis;
5. observar estado, logs o configuración;
6. cambiar una sola variable;
7. verificar;
8. documentar la causa.

Tras un umbral configurable de trabajo sin progreso, sugerir pistas graduales: pregunta orientadora → documentación relevante → ejemplo mínimo → solución explicada. Evitar mostrar la respuesta completa demasiado pronto.

## Progreso útil

No reducir el progreso a «páginas visitadas». Registrar localmente, cuando el alumno lo decida:

- concepto leído;
- recuperación activa realizada;
- práctica iniciada/completada;
- evidencia guardada;
- autoevaluación;
- nivel de confianza;
- duda pendiente;
- ampliación recomendada;
- última revisión;
- tiempo aproximado de trabajo.

El progreso debe poder exportarse/importarse y borrarse. No introducir cuentas o telemetría obligatoria para una función que puede ser local.

## Práctica frecuente

Cada bloque teórico debe tener una práctica pequeña antes de una práctica integradora. La práctica debe indicar objetivo, entorno, riesgo, pasos de recuperación y evidencia esperada.

La misma competencia puede ofrecer variantes por plataforma:

- Linux nativo;
- Windows/PowerShell;
- macOS;
- máquina virtual;
- contenedor, cuando sea conceptualmente equivalente;
- laboratorio remoto/autorizado.

No fingir equivalencia cuando una tecnología dependa de un sistema concreto. En ese caso, explicar por qué y proporcionar una ruta de laboratorio.

## Compatibilidad del alumno

Antes de una práctica, mostrar:

- sistemas soportados;
- CPU/arquitectura relevante;
- RAM/almacenamiento aproximados;
- privilegios necesarios;
- software requerido;
- alternativa segura.

Para Windows desde macOS/Linux, o Linux desde Windows/macOS, priorizar una VM cuando el objetivo sea aprender el sistema completo. Contenedores no sustituyen una VM para conceptos de kernel, arranque, drivers o determinadas políticas del sistema.

Las guías de VMware, VirtualBox u otros hipervisores deben enlazar documentación oficial vigente y señalar limitaciones de arquitectura, licencias y compatibilidad.

## Interfaz

Objetivos de producto:

- un concepto principal por vista;
- diseño claro y legible;
- responsive real en móvil, tableta y escritorio;
- modo pantalla completa/presentación;
- navegación por teclado;
- estado visible de módulo, concepto y progreso;
- búsqueda;
- reanudación;
- modo de lectura sin distracciones;
- controles accesibles;
- contraste y tipografía adecuados;
- funcionamiento razonable sin cuenta.

## Asistente

El asistente debe priorizar preguntas y diagnóstico sobre respuestas inmediatas. Debe poder:

- explicar un concepto a distinta profundidad;
- proponer una práctica segura;
- adaptar una práctica al sistema del alumno;
- sugerir documentación primaria;
- generar preguntas de recuperación;
- revisar una explicación del alumno;
- ofrecer pistas graduales;
- relacionar teoría con una competencia profesional.

No debe ejecutar acciones en el equipo del alumno ni asumir autorización para probar sistemas externos.

## Calidad del contenido

Cada unidad debe tener propietario, fecha de revisión, fuentes, nivel, prerrequisitos, resultados de aprendizaje, práctica, evaluación y criterios de actualización.

Separar:

- fundamentos relativamente estables;
- tecnologías que requieren revisión periódica;
- normativa/certificaciones/precios que requieren fecha de corte y verificación frecuente.

## Métricas educativas

Priorizar métricas de aprendizaje sobre métricas de consumo:

- prácticas completadas con evidencia;
- mejora entre intento y revisión;
- conceptos recuperados sin apoyo;
- capacidad de explicar y transferir;
- tiempo hasta diagnosticar un problema;
- revisiones espaciadas completadas.

Minutos de pantalla o páginas abiertas no demuestran aprendizaje.
