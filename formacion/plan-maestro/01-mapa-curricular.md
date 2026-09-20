# 01 · Mapa curricular: de la informática a la operación de ciberseguridad

[Índice](README.md) · [Arquitecturas](02-arquitecturas.md) · [Laboratorios](06-laboratorios.md) · [Continuación](08-continuacion.md)

## Secuencia y alcance

**Etapa I:** A01–A05, comprender y operar un equipo y una red. **Etapa II:** A06–A08, desplegar y mantener servicios. **Etapa III:** A09–A12, entender amenazas, protecciones, responsabilidades y decisiones de riesgo. **Etapa IV:** A13–A16, evaluar, observar, responder e investigar. **Etapa V:** A17–A18, utilizar IA de forma supervisada e integrar competencias.

La seguridad no se retrasa hasta la etapa III: desde A01 se trabaja con cuentas limitadas, datos sintéticos, ayuda local y recuperación. La etapa III formaliza conceptos ya experimentados. Los IDs Axx.Uxx son **unidades de planificación**, no nuevos módulos del catálogo activo. Cada área tiene seis unidades. Las referencias Mxx indican cobertura relacionada, no equivalencia curricular automática.

## A01 · Introducción a la informática / Computing fundamentals

**Resultado:** explicar cómo un dato se representa, procesa, almacena y comunica, y distinguir síntomas de causas. **Base:** M01–M04. **Entrada:** ninguna.

- **A01.U01. Información y representación:** bits/bytes, binario/hexadecimal, unidades SI/IEC, enteros, texto, Unicode, UTF-8 y finales de línea. Distinguir codificación, compresión, cifrado y hash.
- **A01.U02. Hardware:** CPU, ISA x86/ARM, núcleos, RAM, caché, almacenamiento, interfaces, firmware y dispositivos. Rendimiento, capacidad, latencia y consumo.
- **A01.U03. Software:** aplicación, biblioteca, runtime, sistema operativo, driver, API, licencia, instalación y procedencia. Código interpretado/compilado a nivel introductorio.
- **A01.U04. Datos y algoritmos:** variables, tipos, condiciones, bucles, funciones, estructuras sencillas, complejidad intuitiva y pseudocódigo. Un algoritmo correcto también debe gestionar entradas inválidas.
- **A01.U05. Trabajo digital:** rutas, extensiones y formato real; búsquedas; editores; formatos abiertos; documentación; Markdown; Git; tickets y colaboración.
- **A01.U06. Diagnóstico y ética:** formular hipótesis, repetir mediciones, reconocer sesgos, datos personales, alcance, copias y límites de autorización.

**Práctica:** comparar el mismo texto en UTF-8/UTF-16 y LF/CRLF; explicar tamaño/hash; inventariar un equipo sin números de serie personales. **Evidencia:** tabla de bytes, diagrama de ejecución y cuaderno reproducible. **Dominio:** explicar por qué una extensión, un hash o un porcentaje aislado no permiten concluir todo sobre un archivo o equipo.

## A02 · Terminal y automatización multiplataforma / Cross-platform CLI and automation

**Resultado:** resolver tareas equivalentes en Linux, Windows y macOS sin confundir sus intérpretes. **Base:** M04–M06, M11–M12, M14–M16, M21. **Entrada:** A01.

- **A02.U01. Modelo de terminal:** consola, emulador, shell, proceso hijo, prompt, ayuda, alias, PATH, entorno, perfil interactivo y sesión remota.
- **A02.U02. Archivos y flujos:** rutas, permisos, metadatos, globbing, quoting, stdin/stdout/stderr, pipes, exit codes, búsqueda y comparación.
- **A02.U03. Bash y zsh:** parámetros, arrays, funciones, condiciones, bucles, señales, temporales, regex y diferencias de versión/GNU/BSD.
- **A02.U04. CMD y BAT:** variables, expansión, parámetros, subrutinas, errorlevel, redirecciones, nombres difíciles y límites del legado.
- **A02.U05. PowerShell:** objetos y propiedades, providers, cmdlets, módulos, errores, funciones avanzadas, JSON/CSV/XML, CIM y remoting autorizado.
- **A02.U06. Automatización fiable:** contratos, validación, dry-run, idempotencia, logging minimizado, pruebas, timeouts, concurrencia y Python opcional como puente.

**Práctica:** inventario de una carpeta en Bash y PowerShell; migración de BAT; adaptación explícita a zsh. **Evidencia:** mismo contrato funcional, casos límite y versiones probadas. **Dominio:** distinguir un pipeline de objetos de uno de texto, y no ejecutar entradas como código. La ejecución nativa Windows/macOS debe quedar registrada por separado.

## A03 · Sistemas operativos y administración / Operating systems and administration

**Resultado:** operar identidades, procesos, servicios y configuraciones con mínimo privilegio. **Base:** M03, M07–M10, M13, M17–M23. **Entrada:** A01–A02.

- **A03.U01. Arquitectura del SO:** kernel/user space, llamadas al sistema, procesos/hilos, IPC, memoria virtual, handles y sockets.
- **A03.U02. Arranque y servicios:** UEFI, arranque verificado, systemd, Windows Services, launchd, dependencias, tareas y rollback.
- **A03.U03. Identidades:** usuarios/grupos, SID/UID, ACL, herencia, sudo/UAC, cuentas de servicio, AD/LDAP/Kerberos y ciclo de vida.
- **A03.U04. Configuración y software:** paquetes, actualizaciones, Registro, plist, archivos, perfiles, gestión de cambios y compatibilidad.
- **A03.U05. Bastionado:** baseline aplicable, reducción de superficie, firewall, cifrado, protección endpoint, controles de Apple y excepciones.
- **A03.U06. Operación y registros:** inventario, salud, logs, retención, sincronización temporal, averías y recuperación.

**Práctica:** dar acceso mínimo a dos identidades ficticias, programar una tarea benigna y localizar su log en cada SO. **Evidencia:** matriz de permisos, configuración, prueba denegada y reversión. **Dominio:** resolver una denegación sin desactivar todos los controles.

## A04 · Redes y comunicaciones / Networking and communications

**Resultado:** seguir una conexión desde el host hasta la aplicación y justificar los límites de confianza. **Base:** M10, M18, M22, M24. **Entrada:** A01–A03.

- **A04.U01. Capas y direccionamiento:** Ethernet, MAC, ARP/NDP, TCP/IP, IPv4/IPv6, CIDR, subredes y MTU.
- **A04.U02. Conmutación y rutas:** switch/router, VLAN, routing, NAT, rutas de retorno, redes virtuales y segmentación.
- **A04.U03. Servicios de red:** DNS autoritativo/recursivo, TTL, DHCP, NTP, HTTP, TLS, correo y resolución local.
- **A04.U04. Acceso remoto:** SSH/SFTP, RDP/WinRM, VPN, bastiones, identidad de host, certificados y revocación.
- **A04.U05. Diagnóstico y observación:** interfaces, sockets, captura limitada, PCAP sintético, filtros, trazabilidad y privacidad.
- **A04.U06. Diseño de seguridad:** firewall, proxy, filtrado DNS, zonas, control de salida, Wi-Fi y conceptos de tránsito/pivotaje no autorizado.

**Práctica:** localizar un fallo DNS, uno de ruta y uno de aplicación; verificar dos flujos permitidos y uno denegado en la red asignada. **Evidencia:** matriz origen/destino/puerto/finalidad y explicación por capas. **Dominio:** no equiparar un puerto abierto con una aplicación operativa ni una conexión cifrada con autorización.

## A05 · Virtualización, almacenamiento y copias / Virtualization, storage and backup

**Resultado:** elegir y administrar un laboratorio virtual recuperable. **Base:** M01, M09; ampliación importante. **Entrada:** A03–A04.

- **A05.U01. Virtualización:** host/guest, hipervisor, emulación, arquitectura, virtualización anidada y recursos sobreasignados.
- **A05.U02. VirtualBox:** VM, disco, redes NAT/interna/host-only, snapshots, exportación y aislamiento; revisar licencia de componentes adicionales.
- **A05.U03. VMware:** Workstation/Fusion frente a vSphere/ESXi, plantillas, redes y gestión. No confundir productos ni condiciones de licencia.
- **A05.U04. Proxmox:** KVM frente a LXC, gestión web/CLI, almacenamiento, red, backups y fundamentos de clúster/quorum.
- **A05.U05. Persistencia:** bloque/archivo/objeto, RAID, LVM, ZFS/Ceph como ampliación, APFS/NTFS/ext4, cifrado y cuotas.
- **A05.U06. Recuperación:** snapshot frente a copia externa, retención, restauración, RPO/RTO, inmutabilidad y sanitización con límites SSD/COW.

**Práctica:** reproducir una VM en un hipervisor disponible, exportarla y restaurar un archivo desde una copia independiente. **Evidencia:** ficha del entorno, comprobación de aislamiento y tiempo de recuperación. **Dominio:** distinguir disponibilidad por réplica y recuperabilidad por backup.

## A06 · Arquitecturas web, aplicaciones y datos / Web, application and data architecture

**Resultado:** explicar el recorrido de una solicitud y evolucionar una arquitectura sin complejidad gratuita. **Base:** M25–M26. **Entrada:** A02–A05.

- **A06.U01. Web desde cero:** navegador, DNS, TLS, HTTP, HTML/CSS/JS, servidor, cookies, caché y estado.
- **A06.U02. Aplicación sencilla:** sitio estático y WordPress en servidor único; plugins, base de datos, permisos, actualizaciones y copias.
- **A06.U03. Capas y contratos:** frontend/backend/API, REST, OpenAPI, SQL, transacciones, índices, migraciones, NoSQL y calidad del dato.
- **A06.U04. Escalado:** proxy inverso, balanceo, CDN, sesiones externas, almacenamiento compartido, réplicas y health checks.
- **A06.U05. Empresa:** monolito modular, servicios, colas/eventos, cachés, SSO, multitenancy, aislamiento y observabilidad.
- **A06.U06. Decisiones:** ADR, requisitos, capacidad, SLI/SLO, coste, recuperación, despliegue y reversión.

**Práctica:** diseñar y verificar un sitio único y una variante de dos capas; justificar cuándo no usar microservicios. **Evidencia:** diagramas, matriz de flujos, decisiones y restauración. **Dominio:** diferenciar un patrón arquitectónico y un producto que lo implementa.

## A07 · Cloud e infraestructura como código / Cloud and infrastructure as code

**Resultado:** comparar responsabilidades y desplegar una carga sencilla bajo límites de coste y acceso. **Base:** M24–M26; ampliación. **Entrada:** A04–A06.

- **A07.U01. Modelos:** bare metal, alojamiento, IaaS/PaaS/SaaS, serverless, edge, regiones/zonas, responsabilidad compartida y residencia.
- **A07.U02. AWS:** cuentas, IAM, red, cómputo, almacenamiento, datos gestionados, registro, presupuestos y arquitectura bien diseñada.
- **A07.U03. Azure:** tenant/suscripción, identidades, red, máquinas/servicios gestionados, observabilidad y organización de recursos.
- **A07.U04. Google Cloud:** organización/proyecto, IAM, VPC, cómputo, datos, contenedores gestionados y políticas.
- **A07.U05. Alternativas:** Cloudflare Pages/Workers, OVHcloud, DigitalOcean y OpenStack según capacidades disponibles; evitar falsas equivalencias.
- **A07.U06. Operación declarativa:** IaC con herramienta aprobada, estado y secretos, cambios revisados, drift, FinOps, etiquetado, eliminación y recuperación.

**Práctica:** representar la misma aplicación en tres proveedores; ejecutar solo una variante aprobada o una simulación sin cuenta; registrar costes antes y después de retirar recursos. **Evidencia:** ADR, permisos, plan de cambios y verificación de cierre. **Dominio:** un presupuesto es una alerta, no garantía universal de tope de gasto.

## A08 · Docker, Compose, Swarm y Kubernetes / Containers and orchestration

**Resultado:** empaquetar una aplicación y distinguir la orquestación de un host y de un clúster. **Base:** M26; ampliación sustancial. **Entrada:** A02–A07.

- **A08.U01. Contenedores:** imagen/capa/digest/registro, namespace/cgroup, procesos, volúmenes, redes y diferencia respecto de una VM.
- **A08.U02. Dockerfile:** construcción reproducible, usuario no root, permisos, multistage, dependencias, SBOM y secretos fuera de la imagen.
- **A08.U03. Compose:** servicios, health checks, configuración, perfiles, redes, volúmenes, arranque, logs y ciclo de vida local.
- **A08.U04. Swarm:** manager/worker, quorum, servicios/réplicas, routing mesh, configs/secrets, scheduling, update y rollback.
- **A08.U05. Kubernetes:** control plane, Pod, Deployment, Service, ingress/gateway según implementación, ConfigMap, Secret, PVC, RBAC y políticas de red.
- **A08.U06. Operación segura:** límites, probes, observabilidad, cadena de suministro, backup del estado, recuperación y coste operacional.

**Práctica:** contenerizar una web benigna, definir Compose y diseñar su equivalente Swarm/Kubernetes; probar un rollback en el entorno disponible. **Evidencia:** manifiestos, explicación de persistencia, pruebas de salud y exposición. **Dominio:** base64 no cifra un Secret y Compose no es un manifiesto Kubernetes; las políticas de red requieren soporte efectivo del entorno.

## A09 · Introducción a la ciberseguridad y amenazas / Cybersecurity and threats

**Resultado:** distinguir activo, amenaza, vulnerabilidad, evento, incidente y riesgo. **Base:** M01, M28–M30. **Entrada:** A01–A04.

- **A09.U01. Propiedades:** confidencialidad, integridad, disponibilidad, autenticidad, trazabilidad, privacidad y seguridad de personas.
- **A09.U02. Escenarios:** actores externos/internos, error humano, fraude, ransomware, fallos de proveedor, energía, incendio y pérdida de dispositivo.
- **A09.U03. Superficie:** identidades, endpoints, redes, aplicaciones, datos, cloud, terceros y entorno físico.
- **A09.U04. Modelos de amenaza:** activos, flujos, fronteras de confianza, abuso y dependencias; STRIDE como vocabulario complementario.
- **A09.U05. Vulnerabilidades:** CVE, severidad, explotabilidad, exposición, priorización y verificación de remediación, sin confundir CVSS con riesgo empresarial.
- **A09.U06. Defensa en profundidad:** prevención/detección/respuesta/recuperación, controles humanos/técnicos/físicos y límites de un producto.

**Práctica:** modelar amenazas de la aplicación de A06 y contrastar tres hipótesis benignas/adversas con evidencia sintética. **Dominio:** describir un escenario con consecuencia, no entregar únicamente una lista de herramientas.

## A10 · Elementos de protección / Protection capabilities

**Resultado:** seleccionar capacidades según amenaza, activo y evidencia de eficacia. **Base:** M07, M19, M23, M25, M30. **Entrada:** A09.

- **A10.U01. Identidad:** IAM, MFA, SSO, PAM, IGA, gestión de secretos, federación y cuentas de emergencia.
- **A10.U02. Endpoint:** EPP/EDR, MDM/UEM, cifrado, configuración, actualización y controles de aplicaciones.
- **A10.U03. Red:** firewall/NGFW, IDS/IPS, NDR, NAC, VPN/ZTNA, DNS, correo y segmentación.
- **A10.U04. Aplicación:** WAF/WAAP, API gateway, autorización de negocio, validación, limitación de abuso y desarrollo seguro.
- **A10.U05. Datos y cloud:** DLP, KMS/HSM, clasificación, backup, CSPM/CWPP/CIEM y gestión de postura.
- **A10.U06. Eficacia:** alcance, diseño, implantación, operación, falsos positivos, excepciones y costes totales de propiedad.

**Práctica:** ficha de selección de WAF en nube/appliance/software; comparar capacidad y responsabilidad, no marcas por popularidad. **Evidencia:** prueba funcional, restricción esperada, fuente de log y limitación. [Desarrollo](07-glosario-protecciones.md).

## A11 · Gobierno, funciones y equipos / Governance, functions and teams

**Resultado:** conectar resultados del CSF con personas, procesos y decisiones. **Base:** M30, M32. **Entrada:** A09–A10.

- **A11.U01. CSF 2.0:** Core, funciones, categorías/subcategorías, perfiles y Tiers; separar resultados de implementación.
- **A11.U02. Govern:** contexto, apetito de riesgo, políticas, responsabilidades, supervisión y cadena de suministro.
- **A11.U03. Identify/Protect:** activos, escenarios, mejora, identidades, datos, plataformas e infraestructura.
- **A11.U04. Detect/Respond/Recover:** observación, análisis, gestión del incidente, comunicaciones y restauración.
- **A11.U05. Organización:** CISO, GRC, arquitectura, IAM, AppSec, SOC, CSIRT, CTI, DFIR, plataformas, continuidad, legal/DPD y auditoría.
- **A11.U06. Gestión del servicio:** RACI, catálogo de capacidades, tickets, escalados, KPI/KRI, presupuesto, proveedores y comités.

**Práctica:** construir perfil actual/objetivo y asignar responsables de ocho resultados; demostrar una evidencia por resultado. **Dominio:** las seis funciones son concurrentes y no seis departamentos ni fases exclusivamente sucesivas. [Desarrollo](03-nist-equipos.md).

## A12 · GRC, riesgos y correspondencias / GRC, risk and control mapping

**Resultado:** documentar y tratar riesgos con supuestos y evidencias explícitos. **Base:** M30–M32; ampliación. **Entrada:** A09–A11.

- **A12.U01. Gobierno y obligaciones:** alcance, partes interesadas, políticas, contratos, riesgo corporativo y responsabilidad.
- **A12.U02. Inventarios:** servicios, activos, software, datos, tratamientos, proveedores, identidades y controles relacionados por IDs.
- **A12.U03. Métodos:** ISO 31000/27005, NIST 800-30 y 8286 como lecturas, MAGERIT/PILAR, FAIR y EBIOS RM como ampliaciones verificables.
- **A12.U04. Análisis:** escenarios, probabilidad/frecuencia, impacto, escalas ordinales, incertidumbre, riesgo inherente/actual/objetivo y dependencias de controles.
- **A12.U05. Tratamiento:** reducir, evitar, compartir/transferir y aceptar; plan, propietario, coste, plazo, evidencia, excepción y revisión.
- **A12.U06. Correspondencias:** CSF, ISO 27001, RGPD y ENS; aplicabilidad, cláusula/control/resultado, requisitos no cubiertos y auditoría.

**Práctica:** registro de riesgos del mismo servicio web, ejemplo numérico y matriz de 12 correspondencias parciales. **Dominio:** el riesgo para personas en RGPD no se reduce al coste financiero de la empresa. [Riesgos](05-gestion-riesgos.md) · [Controles](04-controles-correspondencias.md).

## A13 · AppSec, DevSecOps y evaluación autorizada / AppSec and authorized assessment

**Resultado:** revisar seguridad de una aplicación y convertir hallazgos en correcciones verificables. **Base:** M25–M26, M30. **Entrada:** A06–A12.

- **A13.U01. Ciclo seguro:** requisitos, diseño, revisión de código, pruebas, entrega y gestión de dependencias.
- **A13.U02. Herramientas:** SAST, SCA, secret scanning, revisión IaC, SBOM, firma/procedencia y DAST como categoría.
- **A13.U03. Kali:** distribución de herramientas y estación de análisis; selección y permisos; no confundir sistema operativo y metodología.
- **A13.U04. DVWA/Juice Shop:** laboratorio privado, modelos de aplicación y análisis de controles sobre fuentes y telemetría preparadas.
- **A13.U05. Red/Purple Team:** reglas de intervención, inventario autorizado, revisión de confianza, evidencia y coordinación con detección.
- **A13.U06. Cierre:** priorización, causa raíz, ticket reproducible, retest y riesgo residual sin exagerar explotabilidad.

**Práctica:** caso completo de análisis y defensa en LAB-13; pruebas benignas y revisión de eventos sintéticos, sin guía de explotación. **Dominio:** distinguir fallo observado, hipótesis de abuso y explotación acreditada.

## A14 · Blue Team, incidentes y forense / Blue Team, incident response and DFIR

**Resultado:** transformar una alerta en una decisión, preservar evidencia y recuperar con criterio. **Base:** M19, M23, M27–M28. **Entrada:** A03–A04, A09–A12.

- **A14.U01. Observabilidad:** fuentes, cobertura, esquema, relojes, retención, ingestión, SIEM y salud de sensores.
- **A14.U02. Detección y triaje:** casos de uso, severidad, confianza, enriquecimiento, falso positivo, escalado y criterios de incidente.
- **A14.U03. Contención:** opciones reversibles, autoridad, impacto en negocio, acceso de recuperación y registro de decisiones.
- **A14.U04. Investigación:** hipótesis, alcance, fuentes volátiles/no volátiles, adquisición lógica, hash, custodia y timeline.
- **A14.U05. Erradicación y recuperación:** corregir causa, restaurar, verificar integridad y servicio, vigilar recurrencia.
- **A14.U06. Coordinación:** comunicaciones, legal/DPD, conservación, lecciones aprendidas y actualización de riesgos/controles.

**Práctica:** incidente simulado con eventos de tres SO, evidencia contradictoria y restauración. **Evidencia:** ticket, cronología, decisión de contención, manifiesto y informe. **Dominio:** no confundir apagar con contener ni ausencia de log con ausencia de actividad. [S04 en fuentes](09-fuentes.md).

## A15 · CTI, exposición y búsqueda de amenazas / CTI, exposure and hunting

**Resultado:** responder una pregunta de inteligencia con fuentes, confianza y acción. **Base:** M06, M16, M29. **Entrada:** A09, A14.

- **A15.U01. Ciclo CTI:** requerimientos, colección, evaluación de fuentes, análisis, difusión y retroalimentación.
- **A15.U02. Indicadores:** tipos, normalización, fechas, caducidad, contexto, IOC frente a IOA/TTP y confianza.
- **A15.U03. Búsqueda local:** campos exactos, hashes, dominios, URLs, eventos, controles negativos y cobertura.
- **A15.U04. Exposición y vulnerabilidad:** inventario propio, CVE, priorización por activo, fuentes públicas permitidas y prueba de corrección.
- **A15.U05. Intercambio:** MISP/OpenCTI, STIX/TAXII como formatos/protocolos, clasificación y restricciones de difusión.
- **A15.U06. Producto de inteligencia:** hipótesis ATT&CK, informe operativo/ejecutivo, límites de atribución y decisión recomendada.

**Práctica:** normalizar un feed ficticio y probar coincidencias exactas sobre copias offline. **Dominio:** no revelar dominios internos ni una investigación al enriquecer datos en servicios públicos.

## A16 · Resiliencia y riesgos no exclusivamente ciber / Resilience and wider risks

**Resultado:** identificar fallos que afectan al servicio aunque no haya atacante. **Base:** M09, M28, M32. **Entrada:** A05–A12.

- **A16.U01. BIA:** procesos críticos, dependencias, impacto temporal, recursos mínimos, RPO/RTO y límites tolerables.
- **A16.U02. Continuidad/DR:** estrategias, copias, redundancia, degradación, comunicación, proveedores y pruebas.
- **A16.U03. Crisis:** autoridad, decisiones bajo incertidumbre, ejercicio de mesa, comunicación y vuelta a normalidad.
- **A16.U04. Entorno físico/humano:** energía, climatización, incendios, errores, fraude, absentismo y concentración de conocimiento.
- **A16.U05. OT/IoT:** disponibilidad y seguridad física, legacy, ventanas de cambio, segmentación, acceso remoto y observación pasiva.
- **A16.U06. Riesgo sistémico:** fallos correlacionados, proveedor/región, dependencias comunes, cuarta parte y transferencia con límites.

**Práctica:** caída de proveedor y pérdida de administrador clave simultáneas. **Dominio:** reconocer dependencias compartidas y no sumar riesgos como si fueran independientes.

## A17 · IA, privacidad y asistencia por terminal / AI, privacy and CLI assistance

**Resultado:** utilizar IA para explicar o revisar sin ceder ejecución ni datos sensibles. **Base:** M31. **Entrada:** A02, A12, A14.

- **A17.U01. Fundamentos:** modelos, inferencia, contexto, límites, licencia, coste y evaluación.
- **A17.U02. Uso CLI:** modelo local o API aprobada, entradas minimizadas y salidas estructuradas.
- **A17.U03. Aplicaciones:** revisión de scripts, resumen de logs sintéticos, documentación y generación de casos de prueba.
- **A17.U04. Agentes/MCP/RAG:** herramientas permitidas, confianza de fuentes, inyección de instrucciones y separación de datos/instrucciones.
- **A17.U05. Privacidad:** minimización, destino/retención, secretos, perfiles de acceso, evaluación de impacto cuando proceda y trazabilidad.
- **A17.U06. Validación:** esquema, comprobación humana, sandbox, comparación determinista, errores y rechazo seguro.

**Práctica:** comparar una revisión humana y una asistida en diez casos sintéticos. **Dominio:** no conectar texto generado a una shell ni utilizar el mismo modelo como verificador único.

## A18 · Proyecto, comunicación y desarrollo profesional / Capstone and professional practice

**Resultado:** defender una solución operable y sus límites ante perfiles técnicos y directivos. **Base:** M04, M32. **Entrada:** rutas previas aplicables.

- **A18.U01. Encargo:** requisitos, usuarios, datos, alcance y criterios de aceptación.
- **A18.U02. Construcción:** arquitectura, versionado, automatización y despliegue reproducible.
- **A18.U03. Protección:** inventario, riesgos, controles, coste y evidencias.
- **A18.U04. Incidente:** observación, triaje, investigación, recuperación y mejora.
- **A18.U05. Comunicación:** informe ejecutivo/técnico, presentación, handover, colaboración, entrevista y portfolio saneado.
- **A18.U06. Emprendimiento:** problema/cliente, propuesta de valor, servicio gestionado, piloto, límites contractuales y medición, sin confundir venta con evidencia técnica.

**Práctica:** demostrar el servicio, un fallo benigno, su detección y recuperación; defensa individual y revisión cruzada. **Dominio:** otra persona puede reproducir el trabajo y el alumno declara exactamente qué no se probó.

## Reutilización y ampliación sin duplicación

| Base activa | Tratamiento propuesto |
|---|---|
| M01–M04 | Ampliar fundamentos y método A01; mantener IDs y resultados demostrados |
| M05–M12 | Reutilizar Linux/Bash A02–A05; añadir prácticas comparativas, no copiar lecciones |
| M13–M19 | Reutilizar Windows; ampliar directorio, identidad y detección con alcance explícito |
| M20–M23 | Reutilizar macOS; registrar qué requiere equipo nativo y qué se puede leer desde móvil |
| M24–M26 | Convertir las introducciones en rutas separadas de red, web, cloud y orquestación |
| M27–M30 | Profundizar observabilidad, DFIR, CTI y evaluación de controles; añadir gobierno/riesgos |
| M31 | Mantener IA supervisada y ampliar evaluación/privacidad |
| M32 | Conservar proyecto original; ofrecer proyectos por perfil y una integración más amplia |

## Temas adicionales que no deben quedar fuera

Identidad como plano de control; PKI y ciclo de vida de certificados; calidad y clasificación de datos; SQL/APIs; cadena de suministro/SBOM; gestión de vulnerabilidades con contexto; desarrollo seguro; terceros; continuidad/BIA; OT/IoT; seguridad física y humana; FinOps; accesibilidad; privacidad; comunicación; automatización declarativa; ética y evidencia de autorización. Las regulaciones sectoriales o territoriales se incorporarán tras determinar aplicabilidad y verificar su estado, no como lista universal de obligaciones.
