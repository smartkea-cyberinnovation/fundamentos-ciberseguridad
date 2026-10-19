# Guía docente, soluciones y rúbrica

**Las soluciones son públicas y sólo resuelven el supuesto sintético.** No convertirlas en informe de incidente real. No se necesita ejecutar C99 ni suministrar a los alumnos una shell troyanizada.

## Preparación

Revisar las guías, versiones y alcance. Probar la herramienta y, cuando se use, construir la imagen en un entorno de aula. La construcción requiere disponer de una imagen base; fijar su digest para una edición reproducible y conservar el ID de la imagen resultante. No introducir credenciales, montajes del host o acceso al socket Docker. No montar el dossier original dentro de este contenedor.

Se puede trabajar sólo con Python y ficheros. La alternativa Docker permite practicar una shell real, pero no convierte el contenedor en un entorno adecuado para ejecutar malware arbitrario. Este caso no implementa un backend web ni acceso remoto persistente. Las pruebas del repositorio comprueban herramientas/contenido; la ejecución del contenedor por el docente se registra por separado.

## Clave de resolución

| Actividad | Respuesta esperada y evidencia | Error que debe detectarse |
|---|---|---|
| A01 | Generar una línea base, verificarla, modificar sólo una copia y obtener diferencia; conservar commit y bitácora | Confundir hash coincidente con fichero seguro o manifiesto propio con firma autenticada |
| A02 | La shell real es /bin/sh del contenedor con uid 10001; documentar el resultado observado de las restricciones | Atribuir ese uid al host ficticio o dar por probadas las restricciones leyendo el YAML |
| A03 | cache.php.txt es candidato según ficha/ruta/contexto; health.php.txt tiene CHG-42; security-notes.txt es documentación | Clasificar por grep, nombre o extensión sin contexto |
| A04 | Relacionar QpRos/z2KH7/Q7vOx/SXetq y distinguir rama de subida inicial, login y actualizador | Afirmar que la respuesta del callback se evalúa, o que toda petición atraviesa la rama alternativa |
| A05 | Escapes no equivalen a cifrado; literales y flujo se reconstruyen por separado; encabezado no autentica autoría | Evaluar código para desofuscarlo o usar una regex como parser universal |
| A06 | Ordenar por UTC, conservar original y explicar empate E04/E05 | Tomar orden de IDs como causalidad o ctime como nacimiento del fichero |
| A07 | E03/E14 correlacionan escritura y respuesta de carga; E04/E05 relacionan petición y shell por identificadores sintéticos; E06/E07 muestran DNS y salida denegada | Inferir la vulnerabilidad inicial, persona responsable o recepción del POST |
| A08 | Especificar detección multifuente, campos, ventana y controles E02/E09/documentación | Considerar los nombres ficticios IOC reales o una regla escrita validación del motor |
| A09 | Contención limitada, copia preservada, autoridad y rollback; E13 sólo acredita comprobaciones funcionales del supuesto | Declarar erradicación por un 404 o borrar el candidato antes de preservar |
| A10 | Afirmaciones referenciadas, límites visibles y siguiente decisión | Reporte con certezas que las fuentes no sustentan |

## Cronología de referencia

Orden reproducible esperado: **E01, E02, E03, E14, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13**.

E04 (09:01:00Z) y E05 (11:01:00+02:00) coinciden. Su vínculo en el supuesto procede del request_id y de los identificadores de proceso suministrados, no de un orden temporal más preciso. La lista original sitúa E14 al final deliberadamente; ordenarla por posición sería incorrecto.

E03 y E14 describen escritura en uploads y respuesta 201 del mismo request_id. No está capturado el cuerpo de la carga ni se conoce la vulnerabilidad inicial: no se debe inventar un exploit. E05 tiene padre php-fpm y uid 33; la sesión E09 procede de sshd, uid 1001, con autorización LAB-01. Ambos pueden usar /bin/sh, pero no tienen el mismo contexto.

E07 deniega un flujo hacia TCP/443 y declara cero bytes de aplicación reenviados para ese flujo sintético. No aporta una captura HTTP ni confirma recepción en el destino. Tampoco permite descartar comunicaciones fuera del periodo/fuentes incluidos. Un 401 posterior no deshace operaciones ya realizadas por una aplicación.

E10 muestra un mtime anterior y ctime posterior en el modelo Unix. Es compatible con cambios posteriores y exige correlación; por sí solo no atribuye una técnica, un autor o la hora exacta de cada modificación. Los tiempos del archivo descargado por el alumno son ajenos a esos valores del supuesto.

## Ejemplo de resumen ejecutivo

En el escenario sintético se observa un fichero inesperado en cargas y una shell hija de un proceso web. La correlación justifica preservar, investigar y limitar la ruta afectada. Hay un intento de salida denegado; no está demostrada la entrega de un POST ni la exfiltración. No se conoce la vulnerabilidad inicial ni un responsable humano. Se propone comprobar configuración de cargas, contexto de ejecución y registros adicionales, preservando la administración y la evidencia. El análisis estático de C99 explica una capacidad relevante, pero no convierte el escenario en un incidente real.

## Diseño de detecciones: propuesta de corrección

Primera detección: cambio no autorizado en un directorio de cargas que pueda ser interpretado por el servidor, seguido de creación de shell con padre web en una ventana documentada. Requiere mapa de procesos, identidad del servicio, cobertura del filesystem y excepciones revisadas. Positivos: E03/E04/E05; negativos: E01/E02 y E09. La ventana temporal es un parámetro del ejercicio, no un valor universal.

Segunda detección: consulta de un nombre de interés y flujo de salida relacionado. Separar alerta de intento y de transferencia acreditada. E06/E07 debe clasificarse como intento bloqueado. Exigir el campo de decisión y tratar ausencia de telemetría como desconocido. DNS/SNI sin descifrado no permite comprobar el campo url ni el cuerpo del POST.

No se dan por compiladas reglas YARA/Suricata ni convertida Sigma: ese trabajo conserva su criterio de cierre independiente en el expediente C99. Los alumnos pueden proponerlas, pero deben adjuntar versión, backend, entradas positivas/negativas y resultados para afirmar validación.

## Rúbrica de 100 puntos

| Dimensión | Puntos | Evidencia de logro |
|---|---:|---|
| Alcance, ética, custodia e integridad | 20 | Copias, bitácora, manifiesto y prueba negativa; sin contacto con receptor |
| Descubrimiento y contexto de shell | 15 | Diferencia candidatos/documentación y local/SSH/web; observa identidad real de su sesión |
| Análisis estático y límites de ofuscación | 20 | Explica fuente-transformación-destino y distingue autenticación, callback y actualizador |
| Cronología y correlación | 20 | Zonas, empate, identificadores, lagunas e hipótesis alternativas |
| Detección, contención y recuperación | 15 | Casos positivos/negativos, autoridad, reversión y riesgo residual |
| Comunicación ejecutiva y técnica | 10 | Afirmaciones proporcionadas y referencias recuperables |

Publicar secretos, ejecutar la muestra troyanizada en un entorno no previsto o contactar con su receptor invalida la ejecución práctica hasta repetirla con alcance seguro. No se compensa con más capturas o más herramientas. Para evaluación formativa se valora que el alumno identifique y corrija sus errores.

## Ampliaciones opcionales

Comparar un parser reducido con un tokenizador PHP confiable que lea bytes sin incluir/evaluar la muestra, siempre dentro de un laboratorio diseñado por el docente. Elaborar un modelo de amenazas del propio analizador. Medir cobertura con fixtures benignos. Crear un informe ejecutivo de una página y defender una hipótesis alternativa. Estas ampliaciones no equivalen a capacidades ya implementadas por la herramienta.

## Validación y publicación

El recurso se añade a GitHub con referencias desde M27–M29. No cambia M01–M32, L01A–L32C ni las 480 horas del catálogo. La corrección del lexer anterior sigue en su PR independiente. El estado real de CI, fusión y despliegue debe consultarse en GitHub; este documento no declara pruebas locales o despliegues que no se hayan observado.
