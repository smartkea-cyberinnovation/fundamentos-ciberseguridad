"""Apuntes originales de apoyo y autoevaluación pública. No son un examen reservado.

Cada entrada: título, modelo mental, aplicación, evidencia, pregunta, respuesta
correcta y dos distractores. El generador rota la posición de la respuesta.
Las fuentes ampliadas se conservan en FUENTES.md del curso.
"""
LESSONS = {
'M01': (
 'Tu primera herramienta es identificar dónde estás',
 'Una terminal es una interfaz con un intérprete; no identifica por sí sola el equipo sobre el que actúas. Una ventana puede controlar el anfitrión, una máquina virtual o una sesión remota. Antes de una orden, separa cuatro preguntas: qué equipo es, qué identidad utilizas, sobre qué ruta trabajas y qué efecto tendrá la operación. Tener permisos no equivale a tener autorización.',
 'Dibuja anfitrión, huésped y red. Abre el mismo archivo por GUI y terminal y explica cómo sabes que es el mismo. Crea un cambio reversible en una copia del archivo. Un snapshot facilita volver a un estado; no sustituye una copia independiente ni preserva automáticamente evidencia.',
 'Otra persona debe reproducir la intervención usando tu bitácora, sin instrucciones orales. Conserva la bitácora fuera de la máquina que vas a restaurar.',
 'Antes de copiar una orden de una guía, ¿qué necesitas confirmar?',
 'Equipo, identidad, ruta, alcance autorizado y efecto esperado.', 'Que la terminal tenga un color reconocible.', 'Que la orden haya funcionado en otra máquina.'),
'M02': (
 'Lo que lees y los bytes que existen no son lo mismo',
 'Un byte contiene ocho bits. Las unidades decimales y binarias no tienen la misma escala. Un texto visible se convierte en bytes mediante una codificación: UTF-8 y UTF-16 pueden representar el mismo mensaje de forma distinta. Un salto de línea también puede ocupar bytes diferentes. El tamaño lógico, los bloques ocupados y la memoria de un proceso describen magnitudes distintas.',
 'Compara dos copias de un texto con tildes, una con LF y otra con CRLF. Registra bytes y hash antes de abrirlas en un editor que pueda normalizar el formato. Para diagnosticar rendimiento, relaciona la medición con su intervalo, unidad y recurso: CPU, memoria o almacenamiento.',
 'Explica una diferencia de tamaño con los bytes observados. Un hash distinto acredita diferencia de contenido binario, no intención maliciosa ni autoría.',
 'Dos archivos muestran el mismo texto pero su SHA-256 es distinto. ¿Qué concluyes?',
 'Los bytes difieren; debo comprobar codificación y finales de línea.', 'Alguien ha manipulado necesariamente el equipo.', 'El algoritmo SHA-256 ha dejado de funcionar.'),
'M03': (
 'Sigue las relaciones: proceso, identidad, recurso',
 'El sistema operativo administra CPU, memoria, dispositivos y acceso a recursos. El kernel y el espacio de usuario tienen responsabilidades y privilegios distintos. Un proceso combina código, contexto de ejecución y recursos abiertos; un hilo es una unidad de ejecución dentro de ese proceso. La memoria virtual ofrece un espacio de direcciones, no una medición directa de RAM física consumida.',
 'Abre una aplicación propia y observa PID, proceso padre, usuario y recursos. Ciérrala normalmente y comprueba qué desaparece. Contrasta con un servicio administrado por el sistema, que puede seguir activo aunque cierres tu terminal. En un contenedor, localiza también el kernel y la capa de virtualización del anfitrión.',
 'Representa las relaciones sin confundir una ventana, una shell, un proceso y un servicio. No cierres procesos ajenos para demostrar la diferencia.',
 '¿Por qué puede continuar un servicio al cerrar tu terminal?',
 'Su ciclo de vida puede gestionarlo el sistema y no esa sesión.', 'Todo servicio es un proceso sin usuario.', 'Cerrar una terminal nunca termina procesos.'),
'M04': (
 'Convierte una orden en una operación reproducible',
 'El intérprete separa argumentos, expande variables y resuelve el programa que va a ejecutar. Las comillas y el directorio actual forman parte del significado. La salida normal, los errores y el código de retorno cumplen funciones diferentes. En Git, un commit registra una versión; un diff permite revisar exactamente qué se incorporará.',
 'Consulta la ayuda local antes de copiar ejemplos externos. Escribe propósito, entradas, salidas y permisos. Revisa git status y git diff antes de registrar una entrega. Evita carpetas personales, credenciales y evidencias reales: quitar un secreto del archivo actual no lo elimina del historial.',
 'Repite la tarea desde un directorio nuevo y otra sesión. Si depende de una variable o ruta no documentada, todavía no es reproducible.',
 'Un script funciona en tu terminal y falla programado. ¿Qué revisar primero?',
 'Identidad, directorio, PATH, entorno, dependencias y permisos.', 'El color de la consola.', 'Convertir automáticamente toda la ejecución a administrador.'),
'M05': (
 'Primero define qué archivos pertenecen a la tarea',
 'Una ruta identifica una posición en una jerarquía. Un nombre que empieza por punto puede ocultarse en la GUI sin dejar de existir. Un enlace y una copia no tienen las mismas relaciones con el objeto original. Las comillas preservan argumentos con espacios; recorrer todo el sistema no es una mejora si la pregunta solo abarca un directorio.',
 'En el dataset del kit integrado, compara lo que muestra la GUI con un listado que incluya ocultos. Define profundidad y tratamiento de enlaces. Escribe resultados fuera del directorio inventariado, para no cambiar el conjunto mientras lo estás midiendo.',
 'Entrega nombres, tamaños y hashes con el alcance declarado. Explica qué metadatos quedan fuera: el hash de contenido no valida ACL, propietario ni toda la historia del archivo.',
 '¿Por qué el inventario cambia al guardar su salida dentro del origen?',
 'La propia salida añade un archivo al conjunto que estoy midiendo.', 'Porque los archivos ocultos nunca se pueden contar.', 'Porque una ruta relativa siempre es incorrecta.'),
'M06': (
 'Un pipeline debe responder una pregunta concreta',
 'Cada etapa de un pipeline transforma una entrada en una salida. Una coincidencia literal, un glob y una expresión regular son mecanismos diferentes. Contar líneas no equivale siempre a contar eventos: puede haber duplicados, encabezados o registros multilínea. Los datos estructurados deben procesarse con un parser que entienda su formato.',
 'Define primero el campo, intervalo y semántica de coincidencia. Filtra un log sintético, cuenta y agrupa; después comprueba manualmente una muestra. Usa controles negativos como dominios que contienen una cadena parecida pero no son el mismo dominio.',
 'Distingue cero coincidencias, entrada inválida y ejecución fallida. Conserva el original para poder reconstruir cada transformación.',
 '¿Cómo buscar de forma fiable un dominio en eventos JSON?',
 'Interpretando JSON y comparando el campo normalizado con la semántica definida.', 'Buscando la cadena en cualquier parte del archivo y dando todos los resultados por válidos.', 'Eliminando las líneas que no entiendo antes de contar.'),
'M07': (
 'El permiso efectivo resulta de varias capas',
 'La identidad incluye usuario y grupos. Los permisos de un directorio no tienen exactamente el mismo significado que los de un archivo: atravesarlo, enumerarlo y modificar sus entradas son capacidades distintas. Las ACL, su máscara y los controles de acceso adicionales pueden cambiar el resultado que parecen indicar los bits tradicionales.',
 'Diseña una matriz de acceso para dos cuentas ficticias y una carpeta de equipo. Verifica una operación permitida y otra denegada con la identidad real de la prueba. No sustituyas el diagnóstico por permisos universales ni por ejecución permanente como root.',
 'Registra el estado previo, el cambio mínimo y la prueba de recuperación. Un informe de permisos no demuestra por sí solo una escalada de privilegios.',
 'Los bits de un archivo parecen correctos, pero se deniega la lectura. ¿Qué falta revisar?',
 'Identidad efectiva, directorios padres, ACL y controles adicionales.', 'Únicamente la extensión del archivo.', 'Cambiar todo el directorio de sistema a escritura global.'),
'M08': (
 'Distingue configuración, estado y causa',
 'Un servicio puede estar activo ahora y no estar habilitado para el próximo arranque, o al revés. Su identidad, ejecutable, dependencias, entorno y límites explican su comportamiento. Un gestor de paquetes administra procedencia y dependencias; actualizar no elimina la necesidad de probar el servicio.',
 'Relaciona una unidad con su proceso y sus logs. Para una tarea periódica, documenta rutas absolutas, usuario, entorno y destino de salida. Prueba un fallo benigno antes de programarla y verifica que el error no aparece como éxito.',
 'Antes de reiniciar repetidamente, localiza la causa y conserva la observación inicial. Registra una prueba funcional después de cualquier actualización.',
 '¿Activo y habilitado al arranque expresan el mismo estado?',
 'No: uno describe ejecución actual y el otro la configuración de inicio.', 'Sí, son sinónimos en todos los sistemas.', 'Solo importan si el servicio tiene interfaz gráfica.'),
'M09': (
 'Una copia útil es una copia que puedes restaurar',
 'Disco, partición, volumen y sistema de archivos son capas relacionadas, pero distintas. RAID, snapshots y backups resuelven problemas diferentes. RPO expresa la pérdida de datos tolerada; RTO, el tiempo objetivo de recuperación. Esos objetivos no se demuestran con la mera existencia de un archivo de copia.',
 'Restaura datos sintéticos en una ruta distinta del origen. Compara contenido, permisos y apertura por la aplicación. Registra duración y diferencias. En SSD y sistemas copy-on-write, sobrescribir un archivo no permite prometer una eliminación física universal de todas sus versiones.',
 'Distingue el objetivo acordado del resultado medido. Custodia por separado la información necesaria para recuperar un volumen cifrado.',
 '¿Qué demuestra mejor la recuperabilidad de una copia?',
 'Una restauración verificada, con tiempo, datos y permisos comprobados.', 'Que el archivo de copia tenga una fecha reciente.', 'Que la copia esté en el mismo disco que el original.'),
'M10': (
 'Diagnostica de la red al servicio, no por intuición',
 'La dirección del host, las rutas, la resolución de nombres, el transporte y la aplicación forman capas distintas. Que un nombre resuelva no demuestra que un puerto esté accesible. Que exista un listener tampoco demuestra accesibilidad desde cualquier red. IPv4 e IPv6 pueden tener rutas y reglas diferentes.',
 'Limita las pruebas al servidor asignado. Distingue fallo DNS, rechazo de conexión, timeout y respuesta HTTP incorrecta. Asocia sockets con procesos y usuarios según tus permisos. Define una matriz de flujos necesaria antes de modificar el firewall.',
 'Comprueba un flujo permitido y uno denegado sin perder la consola de recuperación. No desactives todo el firewall como método de diagnóstico.',
 'El nombre resuelve, pero no hay respuesta de la aplicación. ¿Qué significa?',
 'La resolución funciona; todavía debo verificar ruta, transporte, TLS y aplicación.', 'Toda la conectividad está demostrada.', 'El fallo solo puede estar en DNS.'),
'M11': (
 'Un script es un contrato, no una lista de órdenes',
 'El intérprete, los argumentos, los tipos de entrada y los códigos de salida forman el contrato del script. Bash realiza expansiones antes de invocar programas; sin comillas, una variable puede producir argumentos distintos de los previstos. El manejo de errores debe contemplar funciones, pipelines y fallos parciales.',
 'Construye primero una CLI de solo lectura sobre el dataset. Divide validación, procesamiento y presentación. Prueba carpeta vacía, nombre con espacios, ruta ausente y permiso denegado. Nunca construyas una orden ejecutable a partir de texto no confiable.',
 'Una opción como set -e no reemplaza pruebas ni una política completa de errores. Explica qué limpia un trap y por qué solo alcanza temporales propios.',
 '¿Qué mejora más la fiabilidad de una automatización Bash?',
 'Un contrato explícito, quoting correcto y pruebas de errores y casos límite.', 'Activar una opción y asumir que todos los fallos están controlados.', 'Concatenar la entrada del usuario dentro de una orden arbitraria.'),
'M12': (
 'Repetir debe ser una propiedad diseñada',
 'Idempotencia significa que repetir una operación definida no introduce cambios adicionales no deseados. No convierte todas las acciones en seguras: un backup repetido puede sobrescribir una copia útil. El modo de previsualización, los límites de tiempo y los bloqueos de concurrencia tienen que probarse.',
 'Define qué ocurre si la salida existe, el destino coincide con el origen, falta un comando o se interrumpe el proceso. Separa configuración y secretos, datos y logs. Publica un resumen de fallos parciales en lugar de ocultarlos.',
 'Ejecuta la prueba dos veces y compara estado, no solo mensajes. Conserva un caso de regresión por cada error corregido.',
 '¿Un modo dry-run demuestra por sí mismo que un script no cambia estado?',
 'No; hay que verificar las rutas de código y los efectos observados.', 'Sí, basta con que la opción se llame dry-run.', 'Solo si se ejecuta con privilegios máximos.'),
'M13': (
 'La GUI te ayuda a localizar el objeto; la CLI a describirlo',
 'Windows organiza procesos, servicios, sesiones, identidades y recursos con su propio modelo. El Registro contiene ámbitos y tipos de valores; no es intercambiable con un archivo de texto Unix. UAC y el token efectivo importan al interpretar privilegios. La edición y compilación condicionan las funciones disponibles.',
 'Construye una tabla que relacione Administrador de tareas, Servicios, Visor de eventos y configuración de red con su objeto y consulta CLI. Registra el motor PowerShell por separado de la versión de Windows.',
 'No declares confiable un ejecutable solo por su nombre. Relaciona ubicación, procedencia, firma cuando proceda, identidad y contexto de ejecución.',
 '¿Qué debe registrar una ficha de administración Windows?',
 'Edición, compilación, arquitectura, parches, motor y módulos pertinentes.', 'Solo el nombre comercial de Windows.', 'Solo si el escritorio está en modo claro.'),
'M14': (
 'CMD tiene reglas propias: no lo trates como Bash',
 'cmd.exe diferencia comandos internos y programas externos. La unidad y el directorio de trabajo, las variables y los metacaracteres afectan a la interpretación. La salida de muchas utilidades es texto localizado, no objetos tipados. Cada ejecutable define la semántica de sus códigos de retorno.',
 'Trabaja con una carpeta cuyo nombre incluya espacios. Usa la ayuda del ejecutable y verifica dónde se resuelve. Antes de copiar con opciones de sincronización o espejo, revisa el alcance y sus posibles borrados en un entorno desechable.',
 'Explica por qué un retorno no cero no significa lo mismo para todas las herramientas. En PowerShell, escribe el nombre completo del ejecutable cuando un alias pueda confundirse con él.',
 'Una utilidad devuelve un código no cero. ¿Qué haces?',
 'Consultar su semántica documentada y contrastar el resultado.', 'Marcar siempre toda la operación como fallo fatal.', 'Ignorar el código porque hubo texto en pantalla.'),
'M15': (
 'Mantén el legado sin convertirlo en deuda nueva',
 'BAT/CMD permite automatizar tareas pequeñas y mantener sistemas heredados. Su expansión de variables, especialmente dentro de bloques, difiere de otros lenguajes. La expansión diferida resuelve ciertos casos, pero también puede afectar a caracteres válidos en datos. Desactivar el eco no convierte una contraseña en secreta.',
 'Define un lote con parámetros validados y códigos de salida. Prueba argumentos ausentes y espacios. La migración a PowerShell se compara por comportamiento; se estudia de forma autónoma después de dominar objetos y funciones en M16.',
 'No traduzcas mecánicamente cada línea. Conserva un conjunto de pruebas que exprese qué debe seguir haciendo el programa.',
 '¿Cuál es una buena razón para migrar un lote a PowerShell?',
 'Necesitar datos estructurados, mejor validación y mantenimiento verificable.', 'Que ambos lenguajes interpreten todas las órdenes de la misma forma.', 'Poder evitar pruebas y tratamiento de errores.'),
'M16': (
 'Transporta datos; da formato al final',
 'Entre cmdlets, PowerShell suele transportar objetos con tipos, propiedades y métodos. Seleccionar una propiedad no equivale a cortar una columna de texto. El formato visual es una representación, no necesariamente el dato que necesitas exportar. Los programas nativos y sus retornos requieren un tratamiento diferenciado.',
 'Inspecciona el objeto con Get-Member, filtra por propiedades y exporta CSV o JSON antes de presentar una tabla. Prueba campos faltantes, profundidad de serialización, Unicode y fechas. Declara los parámetros de cada función y su contrato de errores.',
 'Diferencia Windows PowerShell 5.1 de PowerShell 7 y de los módulos propios de Windows. La execution policy no es una frontera de seguridad.',
 '¿En qué momento conviene aplicar Format-Table?',
 'Al final de una salida destinada a lectura humana, no antes de exportar datos.', 'Antes de cualquier filtro sobre objetos.', 'Siempre antes de ConvertTo-Json.'),
'M17': (
 'Consulta, cambia lo mínimo y comprueba el estado efectivo',
 'Una propiedad configurada no prueba por sí sola que un servicio la esté utilizando. Procesos, tareas, servicios, objetos CIM y ACL tienen ámbitos y permisos concretos. Un parámetro de previsualización solo tiene efecto si la herramienta lo implementa; no proporciona automáticamente una reversión.',
 'Exporta únicamente los campos necesarios de un inventario. Para una carpeta de aplicación ficticia, guarda la ACL inicial y compara acceso de dos identidades. Programa una tarea legítima con usuario, directorio y entorno definidos.',
 'Demuestra funcionalidad y restricción después del cambio. No exportes todo el Registro, perfiles personales o secretos para resolver una tarea acotada.',
 '¿Qué falta aunque un comando admita -WhatIf?',
 'Un estado previo preservado y un procedimiento de reversión verificado.', 'Nada: WhatIf crea un backup completo.', 'Desactivar UAC para que la previsualización sea realista.'),
'M18': (
 'Conectividad, identidad y autorización son controles distintos',
 'Un canal cifrado protege el transporte, pero no determina qué identidad puede utilizarlo ni qué operaciones están permitidas. Directorio, DNS, políticas y autenticación se relacionan sin ser lo mismo. RDP, WinRM y SSH tienen requisitos y mecanismos propios; no se intercambian solo cambiando el puerto.',
 'Utiliza un endpoint preparado con una identidad limitada. Comprueba una consulta permitida, una operación que debe rechazarse y los registros generados. Mantén el acceso administrativo en la red de gestión, sin exponerlo a Internet para simplificar el laboratorio.',
 'Documenta el alcance de la delegación y el cierre del acceso temporal. Una demostración con datos exportados no valida administración de un dominio real.',
 '¿Qué demuestra que un acceso remoto está correctamente delegado?',
 'Que la identidad puede hacer lo previsto y se le deniega lo no autorizado.', 'Que se establece cualquier conexión cifrada.', 'Que todos los equipos se incluyen en una lista global de confianza.'),
'M19': (
 'La ausencia de un evento también necesita contexto',
 'Los eventos pertenecen a proveedores y canales. Su generación depende de configuración, permisos, retención y condiciones de la fuente. Sysmon añade telemetría cuando se instala y configura; no convierte el registro en una visión completa de todo lo ocurrido. Un número de evento aislado no describe suficientemente la fuente.',
 'Selecciona canal, proveedor e intervalo y contrasta una acción benigna conocida. Revisa una baseline de actualización, cuentas, firewall, cifrado y protección. Prueba una restauración fuera de la ruta original sin confundir recuperación con preservación forense.',
 'Registra qué estaba activado, qué no era visible y qué pudo perderse por retención. No imprimas protectores de recuperación en el cuaderno o en Git.',
 'No encuentras un evento esperado. ¿Cuál es la conclusión correcta?',
 'Debo revisar cobertura, configuración, permisos y retención antes de concluir.', 'La acción no ocurrió.', 'La máquina está necesariamente limpia.'),
'M20': (
 'macOS es Unix, pero no es una distribución Linux',
 'Darwin y los componentes específicos de Apple conviven en macOS. APFS organiza contenedores y volúmenes; no todos se comportan como particiones independientes. Arquitectura, versión, opciones del volumen y controles de plataforma afectan a lo que observas. Un bundle de aplicación contiene una estructura, aunque Finder lo presente como un objeto.',
 'Localiza aplicación, configuración de máquina y configuración de usuario por Finder y Terminal. Compara una copia de contenido con otra que preserve los metadatos necesarios. Observa ACL y atributos extendidos sin retirarlos para facilitar la práctica.',
 'Explica lo que realmente has preservado. El hash de un archivo no verifica todos sus atributos ni la integridad de una aplicación completa.',
 '¿Qué diferencia debe documentarse al copiar un archivo en macOS?',
 'Contenido y metadatos preservados, incluidas ACL o atributos cuando sean relevantes.', 'Solo que el icono siga siendo parecido.', 'Ninguna si la extensión no cambia.'),
'M21': (
 'Declara intérprete y herramientas, no solo sistema operativo',
 'zsh y Bash están relacionados, pero sus opciones, expansión y arrays no son idénticos. Además, un script puede fallar por diferencias entre utilidades BSD y GNU, aunque su sintaxis de shell sea válida. El perfil de una shell interactiva tampoco equivale al entorno de una tarea.',
 'Porta un script de solo lectura sobre el dataset. Fija el intérprete, consulta su versión y prueba rutas con espacios, Unicode y patrones sin coincidencias. Valida un plist en una copia; una validación sintáctica no demuestra que la configuración sea adecuada.',
 'Documenta cada diferencia real. Un gestor de paquetes de terceros requiere procedencia, inventario y mantenimiento; no forma parte automáticamente de la plataforma base.',
 'El mismo script falla solo en macOS. ¿Qué revisar?',
 'Intérprete, versión, utilidades BSD/GNU, entorno, dependencias y permisos.', 'Suponer que todas las opciones Linux están disponibles.', 'Dar acceso completo al disco sin diagnosticar.'),
'M22': (
 'Una tarea necesita identidad, ámbito y entorno',
 'launchd organiza la ejecución en ámbitos que no deben confundirse. Un agente de usuario y un servicio de máquina responden a necesidades distintas. Las rutas, permisos, entorno y formato de configuración condicionan el resultado. En red, la configuración por servicios y la resolución efectiva pueden requerir varias consultas.',
 'Prepara una tarea benigna que escriba un resumen en una carpeta propia. Valida su configuración, identifica el dominio de ejecución y registra sus errores. Contrasta un problema de filesystem con una denegación de privacidad de la plataforma.',
 'Retira únicamente la tarea del ejercicio y verifica el estado posterior. No des por disponible el entorno de tu Terminal en una ejecución automática.',
 'Una tarea de launchd funciona a mano pero no programada. ¿Qué puede diferir?',
 'Usuario, ámbito, rutas, entorno y permisos efectivos.', 'Nada: ambas ejecuciones tienen siempre el mismo contexto.', 'Solo el nombre del archivo de salida.'),
'M23': (
 'Los controles de plataforma se diagnostican, no se eliminan',
 'Cifrado, integridad del sistema, procedencia de aplicaciones y permisos de privacidad protegen aspectos diferentes. Un control puede no aplicar igual a todo hardware. Unified Log puede presentar campos omitidos o redactados y conservarlos durante periodos distintos; un historial de shell tampoco registra necesariamente toda la ejecución.',
 'Audita el estado permitido de FileVault, integridad, aplicaciones y servicios remotos. Consulta logs de una ventana temporal y componente definidos. Usa archivos sintéticos para restauración y no extraigas secretos del llavero como método de inventario.',
 'Diferencia no conforme, no aplicable y no comprobable. Si una protección bloquea una acción, investiga la autorización mínima necesaria, no la desactivación global.',
 'Una herramienta no accede a una carpeta protegida. ¿Qué procede?',
 'Diagnosticar permisos y controles de privacidad, con autorización mínima.', 'Desactivar las protecciones de la plataforma por defecto.', 'Concluir que el archivo no existe.'),
'M24': (
 'Cada salto necesita una relación de confianza definida',
 'La administración remota combina transporte, verificación del destino, identidad, permisos y auditoría. Un bastión administra un límite de acceso; no autoriza cualquier tránsito. Los conceptos de túnel y proxy ayudan a razonar sobre segmentación, pero un diagrama no acredita que una política esté aplicada.',
 'Verifica la identidad del host por un canal independiente. Transfiere únicamente el dataset autorizado y compara contenido, permisos y metadatos pertinentes. Estudia saltos entre segmentos mediante matrices de flujos y registros preparados, sin cadenas de intrusión.',
 'Registra origen, destino, finalidad y cierre de la sesión. No desactives verificaciones de identidad para resolver una discrepancia inesperada.',
 '¿Por qué no basta con saber que una transferencia está cifrada?',
 'Porque también hay que verificar destino, identidad, autorización e integridad.', 'Porque el cifrado hace innecesarios los permisos.', 'Porque todos los protocolos remotos preservan los mismos metadatos.'),
'M25': (
 'Disponible significa útil para el cliente previsto',
 'Un proceso activo, un puerto abierto y una respuesta HTTP correcta son observaciones distintas. TLS añade confianza en nombre, cadena y vigencia, además de cifrado. Un proxy inverso y el servicio de aplicación tienen responsabilidades diferentes; sus logs permiten relacionar el síntoma con la capa que falla.',
 'Publica un sitio pequeño solo en el laboratorio, con identidad y directorio mínimos. Verifica respuesta funcional desde el cliente previsto. Ante un error de certificado, corrige nombre, cadena o confianza de laboratorio; no normalices omitir la verificación.',
 'Demuestra servicio útil, permisos limitados, logs y recuperación. Este campus estático no necesita exponer una shell ni montar el socket Docker.',
 '¿Qué debe comprobar un health check funcional?',
 'Una respuesta útil del servicio, no solo la existencia de un puerto.', 'Únicamente que el proceso tenga PID.', 'Solo que el dominio esté registrado.'),
'M26': (
 'Reproducible no significa aislado por definición',
 'Una imagen define un entorno; un contenedor utiliza recursos y una relación concreta con el kernel. Volúmenes, redes, identidad y capacidades pueden debilitar el aislamiento esperado. Compose, Swarm y Kubernetes comparten objetivos de descripción de servicios, pero no ejecutan sin cambios el mismo modelo.',
 'Separa datos, configuración y secretos. Declara recursos, permisos, estado y recuperación. El servicio web del curso puede servirse como archivos estáticos en Pages; un laboratorio con sistemas operativos reales necesita otra infraestructura, fuera de esa web.',
 'No entregues un socket de administración del anfitrión a alumnos. Verifica exposición y persistencia reales en lugar de dar por segura una solución por estar contenedorizada.',
 '¿Puede una web estática de Pages administrar por sí sola una VM del alumno?',
 'No; necesita un servicio de ejecución separado, autenticado y autorizado.', 'Sí, por el hecho de incluir un botón Ejecutar.', 'Sí, basta con guardar una clave SSH en el JavaScript público.'),
'M27': (
 'Una cronología fiable conserva la procedencia',
 'Normalizar eventos facilita compararlos, pero puede ocultar precisión, zona original o datos ausentes. Dos timestamps iguales no demuestran simultaneidad exacta. Los relojes, buffers y sistemas de ingestión pueden introducir desfases. Deduplicar debe conservar la relación con los registros recibidos.',
 'Guarda hora original, zona, hora normalizada, fuente, host y campo utilizado. Documenta cualquier ajuste. Genera una actividad benigna para comprobar su recorrido desde la fuente hasta la consulta y distinguir fallo de ingestión de ausencia de actividad.',
 'Entrega la cronología y una nota de cobertura: qué fuentes faltan, qué intervalos son incompletos y qué inferencias dependen de un desfase.',
 '¿Qué dato no debes perder al normalizar una fecha?',
 'Valor original, zona, precisión y cualquier ajuste aplicado.', 'Solo importa la hora final en UTC.', 'El nombre de la herramienta ya sustituye al timestamp original.'),
'M28': (
 'Preservar y recuperar persiguen objetivos distintos',
 'La investigación busca responder preguntas a partir de evidencia; la recuperación devuelve utilidad al servicio. Una actuación sobre un equipo vivo puede generar registros o cambiar metadatos. El hash ayuda a verificar contenido, pero no sustituye procedencia, custodia ni autorización.',
 'Define preguntas, fuentes y efecto esperado de cada adquisición. Conserva originales, trabaja sobre copias y registra herramientas, versiones, errores y transformaciones. Acota el triage; una recolección indiscriminada de perfiles puede introducir información sensible innecesaria.',
 'Separa hechos, inferencias y vacíos. Una cuenta en un log no identifica por sí sola a la persona que actuó ni acredita atribución a un actor.',
 '¿Qué debe acompañar a un hash en una investigación?',
 'Procedencia, contexto, registro de adquisición y cadena de custodia pertinente.', 'Nada: un hash demuestra automáticamente quién creó el archivo.', 'Una captura sin fecha ni origen.'),
'M29': (
 'Un indicador es una pista con contexto y caducidad',
 'Hashes, dominios, direcciones y rutas no tienen la misma semántica. La procedencia, vigencia y confianza condicionan su utilidad. Un indicador coincidente no equivale a un incidente confirmado. Los comportamientos y técnicas ayudan a formular hipótesis cuando cambian los valores concretos.',
 'Normaliza conservando la entrada original y valida el tipo. Define si buscas un dominio exacto o también subdominios. Prueba positivos, negativos y un indicador caducado. Antes de enriquecer mediante servicios públicos, evalúa qué revelas sobre una investigación o infraestructura.',
 'Entrega consulta, alcance, resultados corroborados y siguiente acción proporcional. Cero resultados no certifica que un sistema esté limpio.',
 '¿Qué diferencia hay entre alerta.test y no-alerta.test?',
 'Son dominios distintos; una búsqueda por subcadena puede producir un falso positivo.', 'Siempre deben tratarse como el mismo indicador.', 'El guion no forma parte del valor del dominio.'),
'M30': (
 'Convierte un hallazgo en una mejora verificable',
 'Una revisión de controles identifica condiciones observables y sus consecuencias plausibles. No convierte una configuración débil en una explotación demostrada. El trabajo Purple coordina observación, prueba benigna, detección, corrección y retest con un alcance común.',
 'Revisa identidades, listeners, permisos y relaciones de confianza del laboratorio. Selecciona un cambio administrativo aprobado y anticipa qué telemetría debería generar. Comprueba la detección y documenta los huecos sin desactivar protección para conseguir un resultado.',
 'Presenta evidencia, impacto razonado, corrección mínima, prueba funcional y restricción. Describe el riesgo residual, no solo una puntuación.',
 'Si observas un permiso excesivo, ¿qué puedes afirmar?',
 'Que existe esa condición y un riesgo a evaluar, no necesariamente explotación.', 'Que una persona concreta ya ha explotado el sistema.', 'Que toda la infraestructura está comprometida.'),
'M31': (
 'La IA puede proponer; los controles deben existir fuera del prompt',
 'Una herramienta de IA puede explicar, resumir y sugerir cambios sin comprender siempre el entorno real. Los logs y documentos son datos no confiables: una frase que ordene ejecutar algo dentro de ellos no adquiere autoridad. Un modelo local tampoco elimina la necesidad de permisos, control de red y revisión.',
 'Proporciona versión, shell, objetivo, contrato de salida y datos sintéticos. Pide hechos con referencias y separa hipótesis. Valida JSON, contrasta con herramientas deterministas y revisa manualmente cualquier código antes de probarlo de forma aislada.',
 'Registra qué salió del equipo, qué respuesta se descartó y qué comprobaste. El asistente de este campus es editorial y guiado: no llama a un modelo ni ejecuta órdenes.',
 'Un log contiene instrucciones que la IA intenta obedecer. ¿Qué haces?',
 'Lo trato como dato no confiable, rechazo la acción y reviso controles externos.', 'Le doy privilegios para que complete la instrucción.', 'Confío porque la respuesta usa lenguaje técnico.'),
'M32': (
 'Demuestra que otra persona puede operar y recuperar tu solución',
 'El proyecto integra administración, automatización, seguridad, observabilidad y comunicación. No se evalúa por cantidad de tecnologías o comandos, sino por resultados explicables. El funcionamiento normal, las restricciones y la recuperación deben estar cubiertos por pruebas diferentes.',
 'Construye el servicio interno, inventario y matriz de acceso. Aplica cambios de bastionado con reversión. Investiga una incidencia sintética, contrasta una explicación alternativa y restaura datos o servicio. Declara qué sistemas se han probado de forma nativa y qué partes solo se han diseñado.',
 'Defiende una decisión, un error y una recuperación sin delegar la explicación en la IA. Entrega instrucciones, evidencia trazable, límites y riesgo residual.',
 '¿Cuál es la mejor evidencia de un proyecto operable?',
 'Reproducción por otra persona, pruebas funcionales y negativas, y restauración demostrada.', 'Una presentación con muchos nombres de herramientas.', 'Un repositorio con muchas líneas, aunque no se pueda reproducir.')
}


def notes_and_quizzes():
    notes, quizzes = {}, {}
    for mid, values in LESSONS.items():
        title, model, application, evidence, question, answer, d1, d2 = values
        notes[mid] = f'## {mid} · {title}\n\n### Entender el mecanismo\n\n{model}\n\n### Llevarlo a una tarea\n\n{application}\n\n### Qué debes demostrar\n\n{evidence}\n\nConsulta los manuales de la versión instalada y las [fuentes del curso](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/formacion/sistemas-operativos/FUENTES.md).'
        options = [answer, d1, d2]
        shift = int(mid[1:]) % 3
        options = options[-shift:] + options[:-shift] if shift else options
        quizzes[mid] = {'question':question,'options':options,'correct':options.index(answer),
                        'explanation':answer+' '+evidence}
    return notes, quizzes
