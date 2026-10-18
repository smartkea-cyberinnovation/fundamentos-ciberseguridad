# Guía docente · Terminal Linux y seguridad

## Propósito y perfil de entrada

Formación para estudiantes de informática/ciberseguridad y profesionales que necesitan operar Linux con criterio. No presupone dominio previo de consola. Se espera manejo básico del equipo, capacidad para instalar o acceder a una VM asignada y disposición para registrar observaciones.

La primera sesión identifica qué es kernel, distribución, terminal y shell. A partir de esa distinción se construyen archivos, procesos, permisos, datos, scripts, servicios, red, contenedores y diagnóstico. Cada práctica culmina en evidencia explicada; memorizar un comando sin interpretar su efecto no basta para acreditar la habilidad.

## Resultados de aprendizaje observables

| Resultado | Demostración |
|---|---|
| Identifica contexto de ejecución | Registra sistema, shell, identidad, directorio y destino antes de actuar |
| Gestiona datos y acceso | Implementa permisos de una carpeta de laboratorio y prueba acceso permitido/denegado |
| Conecta herramientas | Construye un pipeline con prueba positiva, negativa y de error |
| Escribe Bash mantenible | Implementa argumentos, validación, salidas y gestión de errores con pruebas |
| Diagnostica servicios | Relaciona configuración, proceso, socket, logs y prueba funcional |
| Opera Docker | Explica imagen/contenedor/volumen/red y reproduce un servicio con Compose |
| Reconoce con alcance | Identifica activos del laboratorio sin extender el objetivo de la práctica |
| Conserva evidencia | Separa dato observado, inferencia, limitación y recomendación |
| Comunica una decisión | Presenta qué ocurre, por qué importa, cómo lo sabe y qué recomienda |

## Planificación adaptable

El itinerario suma las duraciones orientativas de sus 48 lecciones y las muestra en la web. Cada duración contempla lectura, práctica y comprobación del contenido de esa lección. La instalación del entorno, tutoría y profundización pueden requerir tiempo adicional. La planificación debe ajustarse al nivel del grupo y a la guía oficial de la asignatura.

- **Bloque de iniciación:** módulos 01–06. Entorno, archivos, texto, permisos, procesos, paquetes y copias.
- **Bloque de automatización:** módulos 07–08. Bash y shellscript robusto.
- **Bloque de operación de seguridad:** módulos 09–13. Redes, Kali, web, Docker y orquestación.
- **Bloque de criterio profesional:** módulos 14–16. Bastionado, evidencias, diagnóstico y proyecto final.

Una sesión enfocada puede usar 25 minutos de trabajo y 5 minutos de pausa. Es una ayuda de organización, no una obligación pedagógica ni una garantía de aprendizaje. Para clases largas, alterna bloques de demostración, práctica y conversación sobre evidencias.

## Estructura de la sesión

1. **Activación:** plantea una tarea realista y pide una predicción del resultado.
2. **Demostración:** ejecuta pocos comandos, explica elección de flags, entorno y criterio de salida.
3. **Práctica acompañada:** el alumno reproduce, registra y modifica una variable del caso.
4. **Transferencia:** un reto cambia los datos o el contexto para evitar una mera copia de la receta.
5. **Evaluación:** contrasta comandos, salida, interpretación, solución y prueba repetida.
6. **Cierre:** cada alumno explica una decisión, un error resuelto y una pregunta abierta.

## Evaluación propuesta

| Componente | Peso sugerido | Evidencia |
|---|---|---|
| Prácticas y registro | 40% | Comandos, contexto, criterios de aceptación y reversión |
| Proyecto final | 30% | Sistema reproducible, diagnóstico y documentación |
| Explicación y resolución de errores | 20% | Defensa oral breve y una variación no ensayada |
| Cuestionarios | 10% | Comprensión de conceptos y razonamiento |

Los pesos son una propuesta para adaptar. El test es una autoevaluación pública con respuestas disponibles; no debe presentarse como examen reservado ni usarse solo para certificar competencia.

## Rúbrica común de calidad

| Nivel | Indicador |
|---|---|
| 0 · Por preparar | No hay evidencia suficiente o se desconoce dónde se ejecutó la acción |
| 1 · Reproduce | Sigue los pasos y obtiene una salida, pero necesita ayuda para interpretarla |
| 2 · Verifica | Justifica la orden y contrasta un resultado positivo y uno negativo |
| 3 · Diagnostica | Resuelve una variación, reconoce límites y documenta la corrección |
| 4 · Transfiere | Otra persona reproduce el trabajo y entiende por qué se tomó cada decisión |

En acceso, red y cambios administrativos, una práctica fuera del alcance acordado exige detenerla, restaurar condiciones y volver a explicar el procedimiento antes de considerarla completada.

## Proyecto final

El equipo recibe una VM de laboratorio y una petición: publicar un servicio HTTP sintético, identificar su exposición, automatizar una comprobación de salud y entregar un informe reproducible.

Entregables: inventario del entorno; Compose y scripts; registro de pruebas; comparación antes/después de una mejora; informe ejecutivo de una página; anexo técnico; demostración de cinco minutos. No incluir secretos, datos personales, credenciales o transcripciones de terceros.

La defensa debe responder: qué servicio presta, dónde se ejecuta, quién lo puede usar, qué puede fallar, qué evidencia hay, qué cambio se propone y cómo se sabe que funcionó.

## Observación de terminal y privacidad

La observación docente se acuerda previamente. Usa una VM de un alumno o una VM de demostración; identifica quién escribe y quién observa. El modo ttyd de lectura no sustituye la separación de máquinas. Al terminar, cierra la sesión compartida, revisa procesos pendientes y aplica la retención acordada a las evidencias.

Un contenedor de práctica sin root no es el lugar para administrar el anfitrión. Las tareas de sudo, systemd y Docker se realizan desde la VM asignada. El socket Docker no se monta en la terminal web.

## Accesibilidad y apoyo

Hay navegación por teclado, texto seleccionable, vista móvil, menú ocultable y manual continuo sin JavaScript. El alumno puede copiar comandos o escribirlos. La solución se consulta tras un intento propio; el docente puede resolver el primer error en voz alta y pedir al alumno resolver el siguiente.

## Mantenimiento

Antes de cada cohorte, valida imágenes, herramientas, flags, dominios de Access y los comandos principales. Las distribuciones y Kali rolling evolucionan. Conserva versiones y digests utilizados en la clase junto con las pruebas. Las fuentes de cada lección apoyan esta revisión.
