# Práctica C99-DFIR · Investigar antes de ejecutar

[Índice del caso](README.md) · [English](PRACTICA.en.md) · [Fuentes y semántica](FUENTES.md)

## 1. Encargo y reglas de trabajo

Eres analista del equipo de respuesta de una organización ficticia. Se ha localizado un fichero inesperado en el directorio de cargas de `web-01`. Debes determinar qué indicios justifican investigarlo, qué actividad se puede reconstruir y qué información falta. El supuesto no acredita un incidente real: todos los registros de `evidencias/` son sintéticos. No se utilizarán credenciales, sistemas ni direcciones de terceros.

El caso se inspira en el análisis estático de una variante C99 con SHA-256 `1e07598c2e41b7827840ba6c8611912abd88c0344a5d1eff364eaabeccdc6420`. Ese hash pertenece a la variante del análisis, no a las fichas o al JSON de esta práctica. La distribución docente no incluye la muestra operativa. Consulta [la revisión de procedencia](../../../docs/casos/c99-20261018/REVISION.md) para las limitaciones de adquisición y fechas.

Trabaja con una copia, registra lo que haces y no abras un fichero sospechoso a través de Apache/PHP. No pruebes el receptor externo. No elimines evidencias para simular limpieza. Las únicas ejecuciones previstas son la herramienta de análisis propia, comandos administrativos benignos en el contenedor y las pruebas automáticas.

## 2. Resultados de aprendizaje

Al terminar podrás justificar una priorización, reconstruir el flujo de un fragmento ofuscado sin evaluarlo, distinguir presencia de un IOC de actividad real, correlacionar al menos tres fuentes, documentar integridad y límites, y defender una decisión de contención reversible. Deberás explicar qué shell ejecutó cada comando y con qué identidad.

Prerrequisitos: archivos/rutas, permisos, procesos, HTTP, DNS, hashes, JSON y comandos básicos de terminal. Roles sugeridos: custodio de evidencias, analista, responsable de respuesta y revisor. Una persona puede asumir varios roles, pero debe distinguir en su informe las acciones de cada uno.

## 3. Terminal, shell y acceso remoto

| Concepto | Qué es y qué no demuestra |
|---|---|
| Terminal | Interfaz de entrada/salida; no es por sí misma un mecanismo de acceso remoto |
| Shell local | Intérprete que ejecuta instrucciones con la identidad y permisos del proceso |
| SSH | Canal autenticado que puede proporcionar una shell; también permite otros usos |
| Webshell | Componente del servidor accesible mediante peticiones web que puede proporcionar ejecución o administración; no implica automáticamente root |
| Bind/reverse shell | Describen qué extremo espera o inicia una conexión; no son sinónimos de webshell ni de exfiltración |

El objetivo de uso es comprender el contexto de ejecución, no instalar una puerta de acceso. En el laboratorio se abre una shell legítima mediante Docker. Las funciones de C99 se estudian en las evidencias y en el análisis previo, no se activan. La clasificación de webshell tiene una referencia específica en MITRE ATT&CK T1505.003 [S1].

## A01 · Preservar antes de inspeccionar

Desde el directorio del caso crea `trabajo/`, registra fecha UTC, sistema, versión de Python y commit. Genera un manifiesto de `evidencias/` con `herramientas/forense.py manifest`. Compruébalo con `verify`. La herramienta abre ficheros como bytes, no ejecuta su contenido y rechaza enlaces simbólicos y archivos no regulares dentro de su alcance.

```sh
umask 077
mkdir -p trabajo
{ date -u; python3 --version; git rev-parse HEAD; } > trabajo/entorno.txt
python3 herramientas/forense.py manifest evidencias > trabajo/manifest.json
python3 herramientas/forense.py verify evidencias trabajo/manifest.json
```

Copia `evidencias/` a `trabajo/copia-prueba/`. Modifica sólo la ficha `security-notes.txt` de esa copia y repite la verificación contra el manifiesto original. Debe informar de una diferencia y devolver código de salida 1. El original debe seguir verificando correctamente. No se exige que los mtime de tu checkout coincidan con los tiempos inventados del escenario.

Entregable: manifiesto, commit, registro de custodia y resultado positivo/negativo. Límites: un hash vincula contenido, no demuestra autoría ni certifica que un fichero sea inocuo. Leer un sistema vivo puede alterar tiempos y generar actividad; aquí se trabaja sobre material sintético ya preparado.

## A02 · Usar una shell real sin salir del laboratorio

Abre la sesión opcional indicada en el README. Dentro del contenedor ejecuta:

```sh
id
pwd
printf 'shell=%s pid=%s\n' "$0" "$$"
ls -la /lab/evidencias/webroot
cat /etc/os-release
cat /proc/self/status | head -n 8
```

Explica que `id` pertenece al usuario del contenedor, no al servidor ficticio `web-01`; `/proc/self/status` en ese comando describe el proceso que abre el fichero, no necesariamente tu shell interactiva. No mezcles esas observaciones locales con el JSON del supuesto.

Comprueba el aislamiento sin contactar con destinos:

```sh
python3 -c 'import os,socket; print("uid",os.getuid()); print("interfaces",socket.if_nameindex())'
if touch /lab/evidencias/NO-DEBE-CREARSE 2>/dev/null; then
  printf 'FALLO: evidencias escribibles\n'
else
  printf 'OK: escritura denegada\n'
fi
```

La configuración declara ausencia de red externa y filesystem de sólo lectura. Registra el resultado real; no lo des por conseguido por leer el YAML. Puedes escribir apuntes temporales en `/tmp`; desaparecen al cerrar la sesión. Conserva capturas o salida de terminal antes de salir. No pruebes escapadas del contenedor, elevación de privilegios o acceso al host.

Entregable: tabla comando → proceso/contexto → resultado → límite. Control negativo: escritura denegada. Recuperación: `exit`; `--rm` retira el contenedor. No hace falta borrar la imagen para cerrar la práctica.

## A03 · Descubrir candidatos sin ejecutarlos

Inspecciona exclusivamente las fichas de `evidencias/webroot`. `cache.php.txt` representa un candidato inventado; la extensión `.txt` identifica el formato de la ficha, no una técnica para publicar PHP. `health.php.txt` representa una comprobación legítima. `security-notes.txt` contiene una cadena de interés como documentación: es un control negativo.

```sh
find evidencias/webroot -type f -print
grep -RInE 'c99shcook|curl_exec|goto|eval' evidencias/webroot
```

Clasifica cada resultado según ruta original declarada, propietario, cambio autorizado, tipo de contenido y posible operación. No cuentes coincidencias como incidentes: una guía de seguridad también puede contener un IOC. No uses únicamente el nombre `c99.php`, una extensión o la presencia de Base64 para decidir.

Entregable: inventario priorizado con motivos y alternativa benigna. Éxito: identificar el candidato y explicar por qué `security-notes.txt` no demuestra ejecución. Recuperación: ninguna modificación de evidencias.

## A04 · Leer el código como evidencia

El análisis previo documenta estas relaciones de etiquetas en la variante C99. Son puntos de partida para revisar esa variante, no resultados producidos por el escenario sintético:

| Pregunta | Etiquetas o marcador | Conclusión limitada |
|---|---|---|
| ¿Qué dato se prepara? | QpRos, z2KH7 | Esquema + HTTP_HOST + REQUEST_URI, dentro del campo url |
| ¿Dónde se intenta enviar? | Q7vOx, SXetq | Inicialización y ejecución de cURL hacia el destino fijado en el código |
| ¿Hay una ruta previa al login? | uT50x, gJmPl | Rama alternativa de subida anterior al control normal; no presupone root |
| ¿Se puede modificar configuración desde la petición? | nDYHe, c99shcook | Uso de extract con entrada no confiable |
| ¿Se evalúa la respuesta del callback? | xReAN | No en ese bloque; la rama eval del actualizador es distinta |
| ¿Por qué no basta con mirar fechas? | akNsc, cT0PQ | Determinadas escrituras pueden restaurar tiempos anteriores |

Dibuja la cadena fuente → transformación → operación → condición de acceso. Conserva las etiquetas y distingue flujo de control de orden físico del fichero. No elimines `goto` a mano y declares equivalencia sin comprobar todos los destinos. En la rama inicial de subida, el flujo termina antes de llegar al callback; no es correcto afirmar que todas las peticiones recorren ambos caminos.

El destino de la variante se registra como `hxxps://svgflow[.]digital/sz/log.php`. No se usa en el laboratorio. El nombre ficticio `collector.training.invalid` del JSON no es un nuevo IOC de esa muestra ni una observación de DNS actual.

Entregable: grafo de arranque anotado y tres afirmaciones con nivel de confianza. Éxito: separar capacidad de envío, ejecución alcanzable y prueba de recepción. La presencia de `curl_exec` no demuestra que haya tenido éxito.

## A05 · Entender la ofuscación sin evaluarla

Identifica escapes hexadecimales y octales, nombres opacos, minificación y reordenación con saltos. Como ejemplo de semántica, en un literal PHP entre comillas dobles `\x68\164` representa los caracteres `ht`. Las comillas simples no tienen las mismas reglas. La decodificación de cadenas no resuelve por sí sola llamadas dinámicas ni el grafo de control [S2].

El encabezado de la muestra se presenta como una afirmación de quien la publicó: contiene una descripción de ofuscación y una fecha. No autentica autor, herramienta concreta, intención ni fecha de adquisición. Tampoco la cuenta de un commit identifica automáticamente al operador del receptor.

Consulta los dos defectos del analizador documentados en el [PR #12](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/12): terminadores de comentarios y literales truncados. Un parser que termina mal puede omitir indicadores aunque una batería anterior pase. PHP termina los comentarios de línea al finalizar la línea o el bloque PHP; `?>` dentro de un comentario de línea tiene consecuencias distintas de dentro de una cadena [S3].

Entregable: mini glosario de transformaciones y un caso negativo del parser. No se necesita ejecutar PHP. Si empleas el triage anterior, registra su commit y el estado de la corrección; la herramienta nueva de esta práctica no importa ese lexer.

## A06 · Construir la cronología

`evidencias/escenario.json` agrupa fuentes normalizadas para que no sea necesario disponer de un SIEM. No es una exportación nativa de auditd o de un producto EDR. Cada evento tiene ID, hora con zona, host, fuente, tipo y detalles. La precisión declarada es de un segundo; eventos empatados no permiten establecer un orden causal.

```sh
python3 herramientas/forense.py timeline evidencias/escenario.json > trabajo/timeline.json
```

Conserva `time_original` y revisa `time_utc`. E04 y E05 representan el mismo segundo con zonas diferentes. La herramienta ordena por hora UTC e ID para reproducibilidad; ese desempate no prueba que uno causase el otro. Ordena de nuevo a mano cinco eventos para verificar el resultado.

En E10 se describe un mtime anterior con ctime posterior. En el contexto Unix de esta ficha, ctime es cambio de estado del inode, no fecha de creación. No llames a ambos «fecha del fichero» [S4]. Los valores del JSON son las evidencias del supuesto; el mtime real de `escenario.json` en tu ordenador es otra cosa.

Entregable: cronología con fuentes, empatados y lagunas. Éxito: no inventar precisión subsegundo ni compensaciones de reloj que no se hayan medido.

## A07 · Correlacionar, no adivinar

Relaciona la carga observada, el fichero candidato, la petición HTTP, el proceso hijo, DNS y la decisión de egress. Utiliza ID de petición, identificador de proceso y ruta cuando existan. Proximidad temporal y misma IP no son identidad personal.

En el supuesto hay una consulta DNS y un flujo TCP/443 denegado. Esto no demuestra un POST HTTP entregado. DNS no revela el cuerpo HTTP; SNI tampoco revela por sí solo ruta, query o cuerpo. Un 401 posterior no demuestra que no se ejecutara lógica previa a la autenticación. Conserva por separado lo que describe la muestra y lo que aporta cada fuente sintética.

La sesión administrativa de E09 está autorizada por un ticket ficticio. Un proceso shell no es automáticamente una webshell. El árbol padre/hijo, la identidad, el canal y el cambio autorizado ayudan a discriminarlo.

Entregable: tres hipótesis, evidencias a favor/en contra y observación adicional necesaria. Éxito: concluir intento de salida bloqueado para E07, no exfiltración consumada; mantener explícito que no se conoce el alcance fuera del dataset.

## A08 · IOC y detecciones

Separa IOC de muestra real, indicadores exclusivos del ejercicio y contexto compartido. No añadas `collector.training.invalid` a inteligencia de producción. No bloquees rangos de CDN porque una instantánea antigua los relacione con un dominio. Fecha de revisión no es first_seen ni last_seen.

Diseña dos detecciones: cambio de fichero inesperado en uploads seguido de ejecución de shell desde proceso web, y consulta al destino de interés seguida de intento de salida. Define ventana, campos, retención, fuentes, tratamiento de datos ausentes y alternativas benignas. Usa E02/E09 y `security-notes.txt` como controles negativos.

Entregable: especificación de regla, matriz de pruebas y límites de visibilidad. No declares YARA, Suricata o Sigma validados sólo por escribir una regla: deben probarse con su motor/backend y un conjunto positivo/negativo. Las pruebas Python de esta actividad no sustituyen esos motores.

## A09 · Contener y recuperar

Propón la acción más limitada que reduzca el riesgo conservando administración y evidencias. En el supuesto se deshabilita la ruta afectada, se mantiene la denegación de salida y se restaura contenido desde una referencia conocida. Un 404 o una home que funciona no demuestran erradicación completa.

Define quién aprueba, el efecto esperado, posible impacto, verificación y reversión. Examina permisos de uploads, interpretación de contenido, configuración del servidor, credenciales potencialmente expuestas y alcance temporal. No borres logs, reinstales sin preservar ni utilices la opción de autoeliminación de la shell como plan de respuesta.

Entregable: acta de decisión y pruebas de recuperación funcional y de seguridad. En la práctica se documentan decisiones; no se cambia un servidor de terceros. La limpieza sólo afecta al directorio de trabajo y contenedores del alumno una vez exportadas las evidencias necesarias.

## A10 · Comunicar y defender

Completa [INFORME.md](INFORME.md). El resumen ejecutivo debe expresar impacto posible, hechos demostrados, límites y siguiente decisión; el anexo técnico incluye hashes, cronología, fuentes, métodos y reproducibilidad. Toda afirmación importante referencia un ID de evento o un punto del análisis estático. No presentes el escenario como un incidente real ni atribuyas la inyección al ofuscador sin una versión anterior comparable.

Defiende oralmente cinco cuestiones: por qué se priorizó el fichero; qué shell ejecutaste realmente; qué información podría ir en una URI; qué evidencia demostraría una entrega efectiva; y por qué el hash y el mtime no bastan para atribuir autoría.

Consulta las soluciones después del primer intento. La rúbrica valora el razonamiento y la evidencia, no la cantidad de herramientas ni el número de alertas. Las doce preguntas de `preguntas.json` sirven para autoevaluación y reutilización en el campus.
