# 06 · Laboratorios, casos y proyectos

[Índice](README.md) · [Programa](01-mapa-curricular.md) · [Arquitecturas](02-arquitecturas.md) · [Continuación](08-continuacion.md)

## Estado y contrato común

Los 24 escenarios siguientes son **diseños de referencia**. No sustituyen ni se suman automáticamente a los 96 laboratorios activos. Cada ejecución necesita una ficha de versión, plataforma, recursos, licencia, red, identidad, dataset y recuperación. Registrar por separado: diseñado, revisado, probado en entorno identificado y aprobado para cohorte. Ninguno se considera ejecutado por la mera existencia de este documento.

Todo laboratorio debe incluir objetivo, tareas, evidencia esperada, prueba positiva y negativa, límites, limpieza y criterio de éxito. Datos ficticios, cuentas del laboratorio y herramientas de origen verificado. Antes de cambiar usuarios, firewall, cifrado, discos o servicios, disponer de consola y recuperación. Las guías para móvil permiten leer y documentar; no simulan silenciosamente administración nativa.

Las estimaciones de tiempo se fijarán después del piloto. Las actividades se agrupan como guiada, semiguiada y reto, sin triplicar horas que ya están asignadas en el programa base.

## Catálogo de escenarios

| ID | Área principal | Tarea y evidencia | Éxito y recuperación |
|---|---|---|---|
| LAB-01 | A01 | Representar un texto en bytes, comparar codificación y hash | Explicar diferencias; conservar originales |
| LAB-02 | A01–A02 | Localizar y organizar archivos con espacios, Unicode y ocultos | Procesar cada archivo una vez; retirar solo copias propias |
| LAB-03 | A02 | Inventario equivalente en Bash/PowerShell; BAT legado y zsh declarados | Mismo contrato con errores; no escribir fuera de salida |
| LAB-04 | A03 | Alta, grupo, acceso mínimo, baja y auditoría | Prueba de acceso antes/después; restaurar ACL/cuentas de ensayo |
| LAB-05 | A03 | Tarea legítima en systemd/Task Scheduler/launchd | Identidad, entorno y log explícitos; retirar la tarea |
| LAB-06 | A04 | Diagnosticar DNS, ruta y servicio en hosts asignados | Identificar la capa; revertir el fallo sembrado |
| LAB-07 | A04 | Transferencia autorizada con manifiesto de integridad | Contenido y atributos contrastados; retirar acceso temporal |
| LAB-08 | A05 | VM en hipervisor elegido, snapshot y backup independiente | Aislamiento y restauración probados; recuperar baseline |
| LAB-09 | A06 | WordPress de prueba en servidor único y recuperación | Restaurar DB/archivos; sin datos reales ni panel público |
| LAB-10 | A06–A07 | Evolucionar a dos capas y comparar tres nubes mediante ADR | No exponer DB; justificar coste/dependencias; rollback |
| LAB-11 | A08 | Dockerfile y Compose para aplicación benigna | Usuario mínimo, persistencia y health check; retirar stack propio |
| LAB-12 | A08 | Misma aplicación en Swarm o Kubernetes asignado | Explicar red, permisos, actualización y recuperación; no borrar otros workloads |
| LAB-13 | A09–A14 | Caso DVWA/Juice Shop de análisis de controles y defensa | Aislamiento, evidencia, corrección y retest; desarrollo debajo |
| LAB-14 | A10 | WAF: solicitud normal y regla de prueba benigna | Diferenciar aceptar/bloquear/log; revertir solo la regla |
| LAB-15 | A11 | Perfil CSF actual/objetivo y RACI de un servicio | Resultado–dueño–evidencia enlazados; sin equivalencia automática |
| LAB-16 | A12 | Relacionar inventarios, riesgos y 12 familias de controles | Señalar cobertura parcial y lagunas; mantener fuentes originales |
| LAB-17 | A12 | Calcular R-001 y analizar sensibilidad | Unidades, línea base y coste incremental correctos |
| LAB-18 | A14 | Triaje de diez alertas sintéticas con diferente cobertura | Severidad y confianza justificadas; preservar conjunto original |
| LAB-19 | A14 | Investigación offline con hash, custodia y timeline | Hechos e hipótesis separados; repetir desde copia |
| LAB-20 | A15 | Normalizar indicadores y buscar coincidencias exactas | Positivos/negativos, caducidad y fuente; no consultas externas automáticas |
| LAB-21 | A16 | BIA, caída de proveedor y decisión de recuperación | Dependencias compartidas identificadas; retorno validado |
| LAB-22 | A17 | Revisar scripts/logs sintéticos con IA supervisada | Verificación independiente; ningún comando ejecutado por el modelo |
| LAB-23 | A18 | Proyecto técnico desde arquitectura hasta incidente | Puesta en marcha por tercero, logs y restauración |
| LAB-24 | A18 | Defensa ante dirección y entrega a operaciones | Impacto, coste, límites, responsabilidades y siguiente acción claros |

## LAB-13 · Caso integrado con DVWA y OWASP Juice Shop

**Propósito:** conectar arquitectura, amenaza, controles, observación y remediación en aplicaciones intencionalmente inseguras. DVWA y Juice Shop sirven para formación controlada; no deben mezclarse con la web pública del curso. La advertencia de DVWA sobre no exponerla a Internet se toma como requisito de diseño del laboratorio. [S19–S20]

**Estación:** Linux de administración o Kali preparada con herramientas seleccionadas. Kali no concede autorización ni sustituye una metodología. La selección didáctica usa navegador, herramientas de desarrollo, consulta de código/configuración, verificación de hashes y análisis de registros/capturas suministrados. [S18]

**Topología:** estación del alumno; VM/entorno privado de aplicaciones; observador/colector. Red interna sin entrada desde Internet, sin modo puente por defecto y sin montajes del anfitrión. Las actualizaciones requieren una ventana de salida aprobada; después se vuelve al aislamiento. No se publica una aplicación vulnerable en Pages, Workers ni un túnel público.

**Datos:** dos usuarios ficticios, documentos sintéticos, configuración inicial, eventos normales y eventos anómalos preparados por el docente. No malware, secretos reales ni credenciales reutilizadas. El caso de análisis adverso se entrega como evidencia offline y revisión de fuentes, no como instrucciones para comprometer un sistema.

### Fase A — Preparar y entender

Identificar versión, arquitectura, runtime, base de datos, rutas, dependencias y cuentas. Dibujar flujo de solicitud y fronteras de confianza. Verificar alcance de red, consola, snapshot/copia y reloj. Elaborar tres preguntas de seguridad y tres funciones de negocio que no deben romperse.

**Evidencia:** ficha de laboratorio y mapa de flujos. **Éxito:** cada integrante distingue aplicación, proxy, base de datos, host y contenedor, y sabe dónde se registra cada acción.

### Fase B — Observar comportamiento normal

Realizar navegación, autenticación válida y operaciones ordinarias sobre datos propios de práctica. Observar petición/respuesta y registros, sin automatizar exploraciones fuera del alcance. Describir sesión, autorización, validación y tratamiento de errores. Registrar qué no es visible por cifrado o configuración.

**Evidencia:** tres transacciones legítimas correlacionadas por hora/ID. **Éxito:** no confundir cookie con contraseña ni un estado HTTP con prueba suficiente de autorización.

### Fase C — Analizar debilidades y evidencia preparada

Revisar fragmentos de código y configuración seleccionados por el docente. Comparar el comportamiento esperado con los eventos sintéticos del incidente: acceso rechazado, cambio de configuración, recurso ausente o validación incorrecta. Formular hipótesis alternativas; usar vocabulario de amenaza y, cuando encaje, una referencia de comportamiento.

**Evidencia:** hallazgo con condición, impacto plausible y evidencia concreta. **Éxito:** no afirmar explotación o atribución sin datos; distinguir una condición vulnerable de una intrusión demostrada. No se proporcionan cargas de ataque, extracción de credenciales ni cadenas de pivotaje/evasión.

### Fase D — Proteger y detectar

Proponer corrección en una aplicación de ejemplo segura o una copia de código de práctica: validación/parametrización, comprobación de autorización, permisos mínimos y tratamiento de errores. Diseñar una regla de detección sobre los registros entregados. Si se prueba un WAF, usar una regla benigna identificable, por ejemplo el rechazo de una ruta ficticia de entrenamiento; no presentar esa prueba como cobertura de todos los ataques.

**Evidencia:** diff o plan de cambio, pruebas funcionales/negativas, regla y falsos positivos. **Éxito:** la función legítima continúa operativa; no resolver el ejercicio desactivando protección o concediendo permisos generales.

### Fase E — Responder e investigar

Abrir incidente simulado, asignar severidad/confianza, definir autoridad y valorar contención. Preservar el conjunto de evidencia, calcular manifiesto y construir timeline. Evaluar consecuencias de aislar aplicación/host/identidad y registrar la opción elegida. La contención real, cuando se practique, afecta únicamente a recursos desechables asignados.

**Evidencia:** ticket, decisiones, custodia y cronología. **Éxito:** explicar impacto y lagunas; mantener una vía de recuperación.

### Fase F — Recuperar, reevaluar y cerrar

Restaurar el servicio benigno o la copia de práctica; verificar contenido, permisos y funcionamiento. Reevaluar el riesgo con eficacia observada, no con un porcentaje inventado. Entregar informe ejecutivo y técnico; retirar cuentas/recursos temporales sin eliminar evidencia antes de su evaluación.

**Éxito global:** se puede repetir el análisis, demostrar la corrección y explicar el riesgo remanente. El número de retos o banderas resueltos no sustituye esos resultados.

## LAB-14 · WAF sin depender de un fabricante

Definir activo, ruta y función que se protege. Registrar ubicación del WAF y dónde se ve HTTP descifrado. En entorno de práctica, establecer una regla benigna sobre una ruta de entrenamiento; comprobar solicitud legítima permitida y ruta denegada; contrastar acción en el log. Evaluar una excepción temporal con propietario y vencimiento; medir que no afecta al resto. Revertirla y documentar.

Comparar después el diseño conceptual cloud, appliance físico/virtual y software administrado por el equipo: quién mantiene reglas, escalado, TLS, logs, continuidad y actualizaciones. No afirmar que ModSecurity/CRS tenga el mismo alcance que una suite WAAP completa. [S21–S25]

## LAB-18–19 · Caso Blue Team

Preparar eventos de autenticación, web, servicio y red con una acción benigna y una anómala. Entregar una laguna de cobertura intencional y un desfase de reloj conocido. El alumno debe decidir qué es evento, alerta o incidente; correlacionar; pedir evidencia adicional; diseñar contención con impacto; preservar; restaurar y comunicar.

Criterios: origen/proveedor/campo/tiempo identificados, hipótesis alternativa, confianza, copia original intacta, consulta repetible, decisión proporcional y prueba funcional posterior. La referencia metodológica es la integración de respuesta y gestión del riesgo de NIST SP 800-61 Rev. 3, no una secuencia mecánica aplicada igual a todos los casos. [S04]

## Proyectos por perfil

**SysAdmin/Cloud:** servicio operable, automatización, baseline y recuperación. **SOC/Blue:** fuentes, calidad, detección, triaje y escalado. **DFIR:** paquete preservado, hipótesis, timeline e informe. **GRC:** contexto, activos, riesgos, controles, evidencia y decisión. **CTI:** pregunta, fuentes, confianza, indicadores y producto útil. **Red/Purple autorizado:** alcance, revisión de controles, telemetría de acciones benignas y retest. Todos añaden comunicación y límites.

## Rúbrica común

Comprensión/plan 15 %, ejecución o análisis 25 %, seguridad/privacidad 20 %, evidencia/reproducibilidad 20 %, recuperación/decisión 15 %, comunicación 5 %. El caso debe superar además requisitos críticos de alcance, protección de datos, conservación de originales y honestidad sobre lo ejecutado. Las ponderaciones son propuestas docentes, no una norma externa.
