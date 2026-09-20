# M24–M30 · Operación multiplataforma y ciberseguridad

Cada módulo tiene 14 h: 5 h teóricas y tres laboratorios de 3 h. Fuentes: [S02, S05–S13 y manuales oficiales de los productos elegidos](../FUENTES.md). Se aplican [el laboratorio](../LABORATORIO.md), [bastionado](../BASTIONADO.md) y [uso responsable](../USO-RESPONSABLE.md).

## M24 · Redes, administración remota y transferencias

**Entrada:** M10, M18, M22. **Resultado:** explicar y verificar una sesión administrativa y una transferencia autorizadas, considerando identidad, integridad, permisos y registros.

**Unidades:** repaso de TCP/IP, IPv6, DNS, DHCP y rutas; resolución recursiva/autoritativa y TTL; proxy, VPN y segmentación; SSH y verificación de host; SFTP/SCP/rsync y preservación de atributos; RDP/WinRM y remoting SSH; certificados/claves y revocación; bastiones y accesos temporales; túneles/port forwarding/SOCKS como conceptos y riesgos; tránsito autorizado frente a pivotaje no autorizado; controles de salida, inspección y auditoría.

**Herramientas:** `ssh`, `sftp`, `scp`, `rsync`, cliente RDP y sesiones PowerShell preparadas; `curl`, resolución DNS y consultas de sockets; herramientas de captura solo para interfaces/destinos y periodos aprobados. Comprobar versión y comportamiento real de SCP; no asumir que todas sus implementaciones usan el mismo protocolo. No desactivar verificación de host ni reutilizar claves personales del docente.

**L24A · Conexión confiable.** Entorno: estación de administración y dos hosts asignados, con claves/identidades de práctica. Tareas: verificar identidad del host por canal independiente; entrar como cuenta estándar; consultar versión/estado; cerrar; revisar registros de autenticación. Evidencia: ficha de confianza y log minimizado. Éxito: detectar una discrepancia de identidad sin aceptar el cambio a ciegas. Recuperación: revocar la identidad temporal prevista y conservar acceso docente.

**L24B · Transferencia íntegra.** Entorno: dataset sintético y destino autorizado. Tareas: elegir protocolo; inventariar tamaños/hashes; transferir; comprobar contenido y permisos; tratar interrupción o archivo ya existente; documentar diferencias de metadatos. Evidencia: manifiestos origen/destino y resultado. Éxito: no revelar credenciales en argumentos ni confundir checksum de contenido con custodia completa. Recuperación: retirar copia de destino según retención acordada.

**L24C · Segmentación y bastión.** Entorno: diagrama y registros preparados de conexiones permitidas/denegadas. Tareas: dibujar saltos y límites de confianza; distinguir proxy, túnel y sesión remota; identificar un flujo no previsto; proponer restricciones de identidad, origen/destino y auditoría. Evidencia: matriz de flujos y detección propuesta. Éxito: explicar qué control limita cada salto y qué telemetría se necesita. Recuperación: ejercicio offline, sin abrir túneles ni realizar pivotaje operativo.

**Dominio:** justificar canal y destino antes de conectar. **Error frecuente:** asumir que cifrado equivale a autorización o que un bastión convierte cualquier salto en permitido.

## M25 · Servicios web, TLS y operación segura

**Entrada:** M12, M19, M23, M24. **Resultado:** desplegar y operar un servicio pequeño, localizar errores y reducir exposición sin romper funcionalidad.

**Unidades:** HTTP, métodos/estados, cabeceras y contenido; DNS y virtual hosts; web server/reverse proxy/backend; Nginx/Apache/IIS como alternativas; cuenta de servicio y document root; TLS, certificado/cadena/nombre/confianza/expiración; claves privadas y permisos; configuración validada antes de recarga; logs de acceso/error; límites de solicitudes, timeouts, exposición de información y copias; estado de aplicación frente a disponibilidad del proceso.

**Herramientas:** consola del servicio/IIS y navegador; `curl`, validadores de configuración del producto, estado del servicio y logs; herramientas TLS de inspección sobre servidores del laboratorio. El docente elige un servidor principal y demuestra equivalencias de los otros: 14 horas no acreditan especialización en tres stacks completos.

**L25A · Web mínima operable.** Entorno: VM o contenedor dedicado con sitio estático claro, sin datos reales. Tareas: instalar/configurar por canal aprobado; usar identidad de servicio; limitar directorio y listener; documentar URL de laboratorio; comprobar respuesta desde cliente asignado. Evidencia: configuración, diagrama y pruebas. Éxito: servicio funcional sin paneles administrativos expuestos. Recuperación: procedimiento de parada y retirada aprobado.

**L25B · TLS y confianza.** Entorno: certificado y CA de laboratorio, sin modificar almacenes de producción. Tareas: comprobar nombre, cadena, fechas y clave pública; observar un error de nombre/cadena preparado; corregir configuración legítima; verificar cliente y servidor. Evidencia: diagnóstico y cadena de confianza. Éxito: no usar desactivación de validación TLS como solución. Recuperación: retirar confianza de prueba únicamente donde se añadió y custodiar claves fuera de Git.

**L25C · Incidente operativo.** Entorno: servicio con un permiso incorrecto o backend detenido de forma benigna. Tareas: partir del síntoma; revisar HTTP/logs/proceso/permisos; formular causa; corregir; repetir prueba; documentar monitorización preventiva. Evidencia: ticket, diff y log. Éxito: no otorgar permisos globales ni reiniciar sin diagnóstico. Recuperación: volver a configuración base y verificar disponibilidad.

**Dominio:** correlacionar DNS/TLS/HTTP/aplicación. **Error frecuente:** health check que comprueba un puerto abierto pero no una respuesta válida.

## M26 · Automatización multiplataforma y contenedores

**Entrada:** M12, M16, M21, M25. **Resultado:** empaquetar una tarea repetible y distinguir el aislamiento de contenedores de la administración del host.

**Unidades:** elección Bash/PowerShell/Python según contrato y SO; REST, autenticación, JSON/YAML/CSV y validación; Git y revisión; configuración/secreto/dato; idempotencia y dry-run; inventario/backups/health checks; imagen/contenedor/volumen/red; Dockerfile, Compose, logs y limpieza; usuario no root, rootless cuando proceda y permisos; Swarm: servicio, réplica, secrets/configs y rolling update; Kubernetes: Pod/Deployment/Service/ConfigMap/Secret/RBAC como introducción comparativa; límites de recursos y dependencia del kernel.

**Herramientas:** shells previas, Python opcional, `curl` o `Invoke-RestMethod` en API de laboratorio; Docker/Compose y, en entorno opcional, `docker service` o `kubectl`. No montar socket Docker, no usar contenedores privilegiados ni exponer terminales de alumno públicamente. Swarm/Kubernetes son una introducción; su administración avanzada pertenece a ampliaciones.

**L26A · Contrato común.** Entorno: tres exportaciones de inventario y API ficticia/local. Tareas: fijar esquema mínimo; normalizar OS/versión/hora/estado; validar entradas; distinguir faltante de falso; generar informe común. Evidencia: contrato, conversión y pruebas. Éxito: resultados comparables sin inventar campos ni consultar terceros. Recuperación: no alterar fuentes.

**L26B · Servicio en Compose.** Entorno: host dedicado al curso. Tareas: empaquetar el sitio de M25; declarar configuración, puertos, límites, usuario y health check; arrancar y revisar logs; probar parada/arranque sin perder los datos previstos. Evidencia: archivos declarativos, instrucciones y pruebas. Éxito: únicamente puertos de laboratorio, sin secretos en imagen y sin montar directorios personales. Recuperación: detener servicios y retirar recursos identificados; no borrar volúmenes indiscriminadamente.

**L26C · Orquestación comparada.** Entorno: manifiestos y salidas preparadas; clúster propio opcional bajo control docente. Tareas: representar servicio/réplicas/volumen/red en Swarm y Kubernetes; explicar actualización y rollback; revisar secretos, permisos y rutas de almacenamiento; documentar diferencias de publicación de puertos. Evidencia: mapa y revisión de manifiestos. Éxito: no asumir que Compose se ejecuta sin cambios como stack de Swarm o manifiesto Kubernetes. Recuperación: análisis offline o retirada solo del namespace/stack de práctica.

**Dominio:** reproducibilidad y aislamiento explicados, no afirmados por usar Docker. **Error frecuente:** denominar secreto a un valor que está en texto claro o base64 en Git.

## M27 · Logs, observabilidad y correlación temporal

**Entrada:** M19, M23, M25. **Resultado:** construir una cronología reproducible y describir su cobertura y calidad.

**Unidades:** evento/log/métrica/traza; Linux journal/syslog/audit cuando esté configurado; Windows Event Log y Sysmon; macOS Unified Log; logs web/DNS/autenticación; esquema, proveedor, campos y severidad; UTC, zona original, horario estacional y desfase; retención/rotación/integridad; centralización y permisos; deduplicación y correlación; pérdida/redacción de eventos; consultas y rendimiento; privacidad.

**Herramientas:** `journalctl`, `Get-WinEvent`, `wevtutil`, `log show`, `grep`, `jq`, PowerShell y CSV/JSON; colector o visor de elección docente, sin dependencia obligatoria de un SIEM comercial. No borrar logs para limpiar una práctica.

**L27A · Tres sistemas, un esquema.** Entorno: eventos sintéticos de Linux/Windows/macOS. Tareas: conservar entradas; mapear hora original, UTC, host, fuente, usuario ficticio, acción y resultado; validar tipos; marcar campos ausentes. Evidencia: diccionario de datos y salida. Éxito: no introducir precisión temporal que la fuente no tiene. Recuperación: regenerar desde originales.

**L27B · Línea temporal contrastada.** Entorno: un caso con zonas distintas, un duplicado y un reloj desfasado conocido. Tareas: ordenar; identificar duplicados sin perder origen; calcular desfase; separar orden observado y estimado; contrastar con segundo evento. Evidencia: timeline y nota de incertidumbre. Éxito: no confundir hora local con UTC ni alterar timestamps originales. Recuperación: conservar las dos representaciones.

**L27C · Cobertura y retención.** Entorno: VM/colector de práctica. Tareas: generar una acción administrativa benigna; seguir su recepción; comprobar acceso y retención; simular con datos preparados un hueco de ingestión; redactar alerta de ausencia de telemetría. Evidencia: cadena fuente/colector/consulta. Éxito: diferenciar falta de actividad y falta de observación. Recuperación: no purgar registros para probar la alerta.

**Dominio:** registrar procedencia y límites. **Error frecuente:** equiparar un evento normalizado con la evidencia original completa.

## M28 · DFIR: triage, preservación y análisis

**Entrada:** M09, M27. **Resultado:** realizar un triage proporcionado y defender una conclusión técnica sin contaminar innecesariamente la evidencia.

**Unidades:** preparación/identificación/preservación/adquisición/análisis/informe; NIST y gestión del incidente; adquisición lógica frente a física; live response frente a análisis offline; volatilidad y decisiones de contención; hashes y manifiestos; cadena de custodia; permisos y seguridad de la evidencia; filesystem/timestamps y límites; procesos/conexiones; historial/configuraciones/autoinicio legítimo; Registro/Event Logs/artefactos macOS; timeline; hipótesis alternativas y alcance pericial.

**Herramientas:** utilidades nativas de solo lectura, hash, exportación acotada de logs y parsers aprobados; herramientas forenses especializadas como ampliación según licencia y versión. Se explica que leer un sistema vivo puede generar logs o alterar metadatos. No se incluye extracción de credenciales ni análisis de malware ejecutándolo.

**L28A · Preservar antes de analizar.** Entorno: paquete sintético del caso. Tareas: registrar recepción y alcance; inventariar; calcular hashes; crear copia de trabajo; proteger original; documentar custodios y transformaciones. Evidencia: acta/manifiesto. Éxito: poder repetir el análisis y explicar qué acredita cada hash. Recuperación: restaurar copia de trabajo desde original, no modificar el original.

**L28B · Plan de live response.** Entorno: VM limpia y situación simulada. Tareas: priorizar preguntas y fuentes; evaluar impacto de cada consulta; recopilar solo versión, procesos, conexiones y logs acotados aprobados; registrar errores y permisos. Evidencia: plan, bitácora y resultados sanitizados. Éxito: no ejecutar colecciones masivas de perfiles/secretos ni afirmar que la adquisición fue sin impacto. Recuperación: preservar salidas antes de restaurar la VM.

**L28C · Informe defendible.** Entorno: evidencia offline con cambios administrativos benignos y un indicio ambiguo. Tareas: construir cronología; asociar archivos/eventos; contrastar una hipótesis alternativa; separar hallazgo y atribución; formular necesidad de evidencia adicional. Evidencia: informe técnico y resumen ejecutivo. Éxito: conclusiones proporcionales y trazables. Recuperación: conservar cadena y retención del caso.

**Dominio:** hechos, inferencias y vacíos de evidencia explícitos. **Error frecuente:** atribuir una acción a una persona exclusivamente por un nombre de cuenta.

## M29 · Threat hunting, IOCs y CTI operativa

**Entrada:** M06, M16, M27, M28. **Resultado:** buscar indicadores de forma exacta y contextual, validar una hipótesis y producir inteligencia útil sin revelar información interna.

**Unidades:** IOC/IOA/TTP y contexto; hashes/IP/dominios/URLs/rutas/nombres de procesos/servicios/tareas/claves de configuración; procedencia, confianza, vigencia y falsos positivos; normalización/refanging seguro sin conexión; dominios exactos y subdominios; hashes por algoritmo; búsqueda local acotada; YARA/Sigma como ampliación y límites de traducción a backend; ATT&CK para comportamiento; CTI: pregunta, colección, evaluación, análisis y difusión; DNS/RDAP/certificados y enriquecimiento autorizado; JSON/CSV, STIX/TAXII conceptual; privacy y egress.

**Herramientas:** parsers de datos, búsquedas nativas en copias, hash, `Select-String`, `grep` con literales y límites; API solo sobre datos públicos de ejemplo previamente autorizados. No se realiza enriquecimiento automático de dominios internos, incidentes reales ni indicadores que pudieran activar un recurso malicioso.

**L29A · Lista de indicadores de calidad.** Entorno: lista sintética con duplicados, valores inválidos y distintos tipos. Tareas: validar tipo/algoritmo; normalizar conservando original; distinguir dominio y URL; anotar fuente/confianza/vigencia; rechazar inválidos. Evidencia: JSON/CSV y pruebas. Éxito: no transformar `no-ejemplo.test` en coincidencia de `ejemplo.test`. Recuperación: conservar la entrada original.

**L29B · Barrido offline y falsos positivos.** Entorno: logs/archivos sintéticos con coincidencias conocidas. Tareas: definir campos de búsqueda; ejecutar coincidencias exactas; confirmar hallazgos con contexto; incluir controles negativos; medir falsos positivos y omisiones. Evidencia: consulta/script, resultados y cobertura. Éxito: no afirmar compromiso por una coincidencia aislada. Recuperación: solo lectura de copias.

**L29C · De hallazgo a decisión.** Entorno: resultado del laboratorio anterior. Tareas: formular hipótesis de comportamiento; asociar fuente y cobertura; consultar documentación ATT&CK pertinente sin forzar equivalencias; redactar recomendación verificable; explicar qué enriquecimiento sería legalmente y operativamente apropiado. Evidencia: nota CTI de una página y prueba de detección. Éxito: siguiente acción concreta, confianza y límites. Recuperación: sin consultas automáticas externas.

**Dominio:** saber qué no se observó y por qué. **Error frecuente:** indicadores sin caducidad, búsqueda por subcadenas y enriquecimiento que filtra una investigación.

## M30 · Auditoría y perspectiva Red/Purple Team

**Entrada:** M24, M25, M28, M29. **Resultado:** planificar una evaluación autorizada y convertir una desviación técnica en una prueba defensiva y una corrección medible.

**Unidades:** alcance y reglas de intervención; inventario de superficie local; confianza entre identidades, servicios y segmentos; permisos de ejecutables/configuraciones, rutas y cuentas de servicio; exposición de secretos como categoría de riesgo sin extracción; autoinicio legítimo y auditoría de abuso; movimiento lateral/pivotaje como modelos conceptuales; telemetría esperada y cobertura; Red/Blue/Purple y coordinación; hallazgos, impacto, evidencia, mitigación y retest; comunicación técnica y ejecutiva.

**Herramientas:** inventarios y consultas de configuración ya aprendidos, diagramas, matrices de control, eventos sintéticos y revisión de permisos. No se ejecutan exploits, acceso lateral no autorizado, evasión ni persistencia encubierta. La competencia consiste en identificar condiciones, explicar riesgo, diseñar controles y verificar su funcionamiento.

**L30A · Revisión de superficie.** Entorno: snapshot propio con configuraciones de ejemplo. Tareas: inventariar listeners, cuentas administrativas, servicios y accesos; comparar baseline; seleccionar tres desviaciones; asignar impacto y evidencia mínima. Evidencia: informe con alcance exacto. Éxito: no inferir explotabilidad demostrada cuando solo se observa configuración. Recuperación: auditoría de consulta, sin explotación.

**L30B · Validación Purple benigna.** Entorno: cambio autorizado identificable, por ejemplo una tarea de resumen del curso. Tareas: anticipar telemetría; ejecutar la acción administrativa permitida; verificar logs/detección; explicar huecos; proponer ajuste sin desactivar protección. Evidencia: matriz acción/control/evento/resultado. Éxito: prueba reproducible y distinguible de actividad no autorizada. Recuperación: retirar la tarea legítima con registro.

**L30C · Retest y reporte.** Entorno: un hallazgo del laboratorio A. Tareas: diseñar corrección y rollback; aplicar bajo aprobación; comprobar funcionamiento y restricción; presentar riesgo residual y cobertura. Evidencia: antes/después, prueba negativa y resumen para responsable no técnico. Éxito: mejora demostrada sin sobreafirmaciones. Recuperación: conservar cambio aprobado o restaurar baseline conforme al objetivo.

**Checkpoint C5:** convertir configuración/telemetría en decisiones verificables, sin confundir administración, investigación y prueba ofensiva.
