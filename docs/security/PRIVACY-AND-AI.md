# Privacidad, datos de alumnos y asistencia con IA

Este documento describe decisiones de ingeniería y tareas de gobierno. No sustituye la validación del responsable y del delegado de protección de datos de la entidad que imparta el curso. Fecha de contraste de fuentes: 18 de octubre de 2026.

## Tratamiento actual

El campus no solicita cuenta, nombre, correo o matrícula. Lecturas, respuestas y notas se conservan en el navegador; el aula OS permite elegir guardar su registro. El alumno puede exportar una copia y borrar el estado mediante los controles de cada aplicación. Campus, OS, examen y TERM tienen registros independientes.

| Dato o evento | Ubicación y transmisión | Decisión de diseño |
|---|---|---|
| Lecturas y marcas | Almacenamiento del navegador | Progreso autodeclarado y recuperable, sin ranking público |
| Notas y evidencias escritas | Navegador y JSON exportado por el alumno | Pedir únicamente datos ficticios; la exportación puede contener las notas |
| Respuestas del test | Navegador | Corrección local; no se envían al profesor ni acreditan identidad |
| Temporizador OS | Navegador | Inicio explícito, pausas y trabajo externo separado; no inferir atención |
| Compartir una lección | URL elegida por el alumno | Sin respuestas, notas ni registro de estudio |
| Compartir progreso | Enlace generado y servicio de mensajería elegido | Excluye notas; el destinatario y el servicio pueden leer la copia completa |
| Petición al sitio | Infraestructura de entrega | Puede implicar IP, agente de usuario y logs del proveedor; no se confunde con los datos locales de la aplicación |
| Laboratorio TERM opcional | Infraestructura distinta, solo si se configura | Requiere autorización, aislamiento, identidad, política de logs y responsable propios |

La ausencia de una base de datos de alumnos reduce el alcance técnico. No elimina las responsabilidades sobre la entrega web, la organización docente, los proveedores o una copia que el alumno comparta. Tampoco convierte el almacenamiento del navegador en una caja fuerte: extensiones y scripts del mismo origen forman parte de su modelo de confianza.

## Matriz que debe completar la entidad antes de ampliar el servicio

| Decisión | Evidencia de cierre | Estado |
|---|---|---|
| Responsable y contacto de privacidad | Identidad y canal publicados y coherentes con el servicio impartido | Pendiente de validación institucional |
| Finalidad y base jurídica | Registro de cada finalidad y su justificación, sin usar una casilla genérica para todo | Pendiente si se incorporan alumnos identificados |
| Información al alumno | Aviso comprensible sobre datos, destinatarios, plazos y derechos | Revisar el aviso corporativo para el contexto docente |
| Proveedores y encargados | Servicios usados, contratos, subencargados y configuración efectiva | Revisar Cloudflare y cualquier plataforma añadida |
| Conservación | Plazos para logs, exportaciones, trabajos y posibles cuentas; procedimiento de borrado | Falta decisión organizativa documentada |
| Derechos y soporte | Canal, responsable de tramitación y procedimiento probado | Pendiente de asignación institucional |
| Transferencias | Ubicación y acceso real, con mecanismo aplicable cuando proceda | Verificar contratos y configuración, no inferir por una región comercial |
| Riesgo y EIPD | Análisis previo; evaluación de impacto cuando el tratamiento lo requiera | Reabrir antes de perfiles, supervisión o IA con datos personales |
| Incidentes | Detección, contención, responsables, registro y evaluación de notificación | Integrar con el procedimiento de la entidad |
| Cookies y almacenamiento | Inventario efectivo y finalidad; decisión documentada sobre información y consentimiento | No activar analítica o publicidad por defecto |

El RGPD exige definir finalidades y aplicar minimización, transparencia, seguridad y protección desde el diseño. Sus artículos 5, 6, 13, 25, 28, 32, 35 y 44 son referencias para las decisiones anteriores. La aplicación concreta depende de quién trate los datos y para qué; la revisión del código no determina por sí sola la base jurídica ni acredita cumplimiento. [Texto oficial del RGPD](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679).

La AEPD relaciona la protección por defecto con minimizar cantidad, alcance, conservación y accesibilidad. En este proyecto se traduce en conservar la ayuda local, evitar nuevos campos de identificación y revisar cualquier integración antes de activarla. [AEPD: protección de datos por defecto](https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/proteccion-de-datos-por-defecto).

Para aplicaciones educativas, el centro debe examinar la información del servicio, sus proveedores, datos y garantías. Esta guía no debe usarse para asumir que cualquier app de uso personal está autorizada en el aula. [AEPD: orientaciones para evaluar aplicaciones con datos de alumnos](https://www.aepd.es/guias/guia-orientaciones-apps-datos-alumnos.pdf).

## Asistencia guiada que ya puede utilizarse

Las explicaciones, pistas progresivas, enlaces de repaso, pasos esperados y preguntas permiten acompañar al alumno sin enviar sus entradas a un modelo remoto. Un recorrido por rol orienta la selección del contenido; no necesita perfilar a la persona ni bloquearle otras rutas. Las recomendaciones deben explicar qué práctica o resultado pendiente las origina.

El profesor mantiene el criterio sobre objetivos, evaluaciones y adaptaciones. El simulador de 100 preguntas ofrece 20 al azar con corrección inmediata; no sirve para decisiones académicas de alto impacto. Las horas del itinerario general y los 6 ECTS de la asignatura son magnitudes de contextos distintos.

## Condiciones para una futura IA externa

No se activa un proveedor generativo en esta revisión. Si se propone uno, la PR deberá responder de forma concreta a estas condiciones:

1. **Finalidad acotada.** Definir qué ayuda presta, qué datos necesita y qué alternativas locales existen. No habilitar clasificación de capacidad, vigilancia o calificación automática como efecto lateral de un chat.
2. **Datos mínimos.** Trabajar con contenido docente y ejemplos sintéticos. Evitar notas, identidades, expedientes, credenciales y material de terceros sin autorización. Quitar un nombre no garantiza anonimización si el contexto identifica a alguien.
3. **Proveedor revisado.** Documentar contrato, retención, entrenamiento, región, accesos, subencargados y condiciones de borrado; no asumir que una cuenta comercial resuelve estas decisiones.
4. **Frontera de servidor.** Si hay secretos o consumo facturable, protegerlos fuera del cliente; imponer autorización, cuotas, límite de coste, tiempo y tamaño. No colocar claves en JSON, JavaScript, URL o repositorio.
5. **Entrada no confiable.** Validar esquema y límites. Separar instrucciones del sistema, petición del alumno y documentos recuperados. Un correo, PDF o página no puede autorizar llamadas, envíos ni ejecución.
6. **Salida no confiable.** Renderizar como texto o mediante un formato permitido. Validar enlaces, citas, herramientas y argumentos. Ninguna respuesta debe ejecutar código, publicar cambios o modificar datos sin un control específico.
7. **Explicación verificable.** Mostrar fuentes del curso y límites de la respuesta, permitir abrir la lectura original y expresar incertidumbre. No inventar citas, normas o resultados de prácticas.
8. **Control humano y errores.** Permitir descartar la ayuda y continuar estudiando. Definir respuestas ante falta de red, cuota, contenido desconocido e instrucciones maliciosas; probar esos casos antes de publicar.
9. **Registro mínimo.** Medir disponibilidad y errores sin almacenar por defecto conversaciones completas. Fijar plazos y accesos antes de activar logs.
10. **Aceptación y reversión.** Comparar calidad con casos docentes revisados, comprobar filtraciones e inyección y poder desactivar la integración sin perder contenido ni progreso.

Estas condiciones son criterios de implementación futuros, no funcionalidades actuales. La AEPD advierte sobre datos personales y confidencialidad en prompts y sobre la necesidad de encuadrar el uso organizativo del proveedor. [AEPD: prompts, datos personales y confidencialidad](https://laboratorio.aepd.es/blog/prompts-datos-personales-y-confidencialidad-el-nuevo-perimetro-de-riesgo-de-la-ia-generativa).

## Cierre y mantenimiento

Las tareas de esta matriz se cierran con documentos, configuración y pruebas observadas, no con una declaración genérica de «GDPR compliant». Mantener las referencias privadas de coordinación en el tracker autorizado, fuera del repositorio público. Antes de cada edición, revisar las fuentes y registrar qué ha cambiado en datos, proveedores y finalidades.

Véanse [política de seguridad](../../SECURITY.md), [revisión técnica](REVIEW-2026-10-18.md), [progreso y traspaso](../../campus/PROGRESO.md) y [backlog](../BACKLOG.md).
