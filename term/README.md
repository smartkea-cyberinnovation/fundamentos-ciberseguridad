# TERM · Aprende terminal Linux y seguridad

**Wiktor Nykiel · SmartKEA · Curso práctico en español · Edición 1.0**

Domina la terminal comprendiendo lo que hace cada comando, practicando en Linux y verificando el resultado. Este itinerario se centra en GNU/Linux, `sh`, Bash, shellscript, Kali, Docker y la operación de seguridad desde consola.

**Curso:** [smartkea.com/fundamentos-ciberseguridad/term/](https://smartkea.com/fundamentos-ciberseguridad/term/)

**Manual completo:** [lectura e impresión](https://smartkea.com/fundamentos-ciberseguridad/term/manual.html)

## Empieza aquí

1. Prepara una VM Debian, Ubuntu o Kali y una cuenta de alumno. Identifica equipo, usuario, ruta y red antes de actuar. [Guía de laboratorio](docs/LABS.md).
2. Empieza por el módulo 01. Cada lección tiene cuatro fases: **aprender, practicar, resolver y comprobar**.
3. Lee un concepto, predice el resultado y después ejecuta el paso en el entorno indicado. Algunos pasos comparten variables: conserva la misma terminal durante la práctica.
4. Guarda evidencia mínima: comando, contexto, salida relevante, interpretación y comprobación. Resuelve el reto sin mirar primero la solución.
5. Marca la lección como aprendida cuando puedas explicarla y repetirla. Exporta tu progreso y tus notas al cambiar de navegador o equipo.

El temporizador de 25 minutos ayuda a mantener una sesión enfocada. Las duraciones de las lecciones son orientativas y se calculan desde el contenido; puedes parar, repetir y avanzar a tu ritmo.

## Qué aprenderás

| Módulo | Habilidad principal |
|---|---|
| 01 · Linux y shell | Identificar el entorno, usar ayuda y distinguir terminal, shell, Bash y sh |
| 02 · Archivos y rutas | Navegar, copiar, localizar, comprender enlaces y conservar datos |
| 03 · Texto y pipelines | Conectar procesos, filtrar, usar expresiones regulares y procesar JSON |
| 04 · Identidad y permisos | Entender UID/GID, permisos de archivo/directorio, sudo y ACL |
| 05 · Procesos y servicios | Controlar trabajos, señales y unidades systemd con verificación |
| 06 · Paquetes y almacenamiento | Revisar procedencia, simular cambios y comprobar restauraciones |
| 07 · Bash | Variables, comillas, expansiones, condiciones y bucles |
| 08 · Shellscript robusto | Argumentos, funciones, errores, logs, ShellCheck y pruebas |
| 09 · Redes desde consola | Direcciones, rutas, DNS, sockets y TLS |
| 10 · Kali y reconocimiento | Seleccionar herramientas, reconocer el laboratorio y registrar alcance |
| 11 · Web | Interpretar HTTP, usar curl, revisar cabeceras y correlacionar logs |
| 12 · Docker | Imágenes, contenedores, red, volúmenes y ejecución de herramientas |
| 13 · Compose y Swarm | Reproducir servicios, comprobar salud y distinguir modos de despliegue |
| 14 · Bastionado | Revisar SSH, permisos, secretos y filtrado con pruebas antes del cambio |
| 15 · Triaje y evidencias | Recoger datos, conservar integridad y documentar un incidente sintético |
| 16 · Proyecto y diagnóstico | Integrar habilidades y entregar una operación reproducible |

**16 módulos, 48 lecciones, 48 retos resueltos y 96 preguntas explicadas.** Cada lección incluye objetivos, prerrequisitos, teoría desarrollada, comandos, entorno, resultado orientativo, verificación, precauciones, reversión, pistas, solución y criterios de aceptación.

## Cómo utilizar las vistas

- **Itinerario:** orden de estudio y acceso a cada módulo.
- **Aprender:** un concepto por vista, objetivos y fuentes primarias.
- **Practicar:** un paso por vista, comando copiable, explicación y comprobación.
- **Mesa de práctica:** salidas orientativas identificadas como tales y acceso opcional a ttyd.
- **Resolver:** reto, pistas, solución, rúbrica y nota personal.
- **Comprobar:** preguntas con respuesta razonada y repetición.
- **Comandos:** búsqueda de ejemplos con enlace a su contexto completo.
- **Mi progreso:** autoevaluación, estado de prácticas, exportación e importación con revisión previa.
- **Manual:** toda la formación en una lectura continua imprimible, disponible sin JavaScript.

La aplicación funciona en escritorio y móvil. El menú se puede contraer, y hay pantalla completa cuando el navegador lo permite. Los datos de aprendizaje permanecen en el navegador y no se envían a un servidor.

## Laboratorios y terminal real

El laboratorio utiliza una web de datos sintéticos y una caja de herramientas Kali en red interna. Docker se opera desde una VM propia. ttyd permite trabajar desde el navegador con un usuario sin privilegios dentro de su contenedor; no incorpora el socket Docker del anfitrión.

La conexión a una máquina se configura después de preparar el endpoint HTTPS y su política de acceso. La publicación sin endpoint muestra **ninguna máquina vinculada**. El curso puede estudiarse y practicarse con la terminal de la VM durante esa configuración.

- [Preparar y operar los laboratorios](docs/LABS.md).
- [Vincular ttyd y observar una sesión](docs/CONEXION-TTYD.md).
- [Arquitectura y límites de confianza](docs/ARQUITECTURA.md).
- [Guía docente y evaluación](docs/GUIA-DOCENTE.md).

## Fuentes y edición

Las referencias se incluyen en cada lección: GNU, Debian/Ubuntu, freedesktop/systemd, ShellCheck, Kali, Docker, Nmap, curl, OpenSSH, OpenSSL y OWASP, según el tema. Las distribuciones cambian: consulta también la ayuda local de la versión que utilizas.

El curso es una ampliación autónoma del [campus general](../README.md). Su código y contenido están en `term/`; los materiales anteriores conservan su estructura.

## Documentación de mantenimiento

[Publicación en Cloudflare](docs/DEPLOY.md) · [Seguridad](docs/SECURITY.md) · [Validación](docs/VALIDACION.md) · [Editar el curso](docs/EDICION.md) · [Derechos de uso](docs/LICENSE.md)

El README principal se orienta al alumno. Los comandos de despliegue y la administración de la terminal están en las guías técnicas.
