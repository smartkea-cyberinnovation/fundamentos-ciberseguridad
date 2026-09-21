# Seguridad y datos / Security and data

## Alcance

El campus muestra material docente y ejemplos. No ejecuta comandos de alumnos, no conecta a equipos remotos, no solicita credenciales y no despliega políticas del SO desde el navegador. Las prácticas administrativas requieren activos y autorización específicos. No publicar sistemas vulnerables del laboratorio junto al campus.

## Datos del aula OS

El registro OS usa únicamente `smartkea.os.study.v1` y su clave de posición por pestaña. No se leen ni borran cookies o almacenamiento corporativos. Persistir el registro es opcional; compartir el enlace de una lección no comparte ese registro. JSON contiene marcas y tiempos autodeclarados o registrados, no tokens de autenticación. El progreso del campus anterior es otro conjunto de datos.

El almacenamiento local no está cifrado y no constituye una cuenta. No introducir datos personales, secretos, resultados reales de incidentes o contraseñas. Las notas de problemas se mantienen en memoria de la pestaña y se descargan explícitamente. No hay analítica remota, cámara, micrófono, telemetría del escritorio ni rastreo de navegación externa.

Los contadores no acreditan presencia o rendimiento académico. La página se pausa al ocultarse; los intervalos largos de suspensión no se suman. La estimación de esfuerzo pendiente es orientativa. Un control de interfaz no autentica que un alumno haya realizado la práctica.

## Controles técnicos

Contenido de usuario tratado como texto, imports JSON validados con límites, CSP local sin `unsafe-eval`, cabeceras de seguridad del campus, enlaces HTTPS a referencias y manifiestos de release. El temporizador usa Web Locks cuando el navegador los soporta; en otro caso se advierte que debe usarse una sola pestaña. No hay garantía de sincronización multidispositivo.

## Reportar un problema

No abrir un issue público con secretos, datos personales, enlaces de progreso o detalles de una vulnerabilidad no coordinada. Utilizar el mecanismo privado de advisories de GitHub si está habilitado. Si no lo está, solicitar al responsable un canal privado sin publicar el detalle sensible. No se inventa un buzón de seguridad ni un plazo de respuesta garantizado.

Incluir versión/commit, navegador, SO, pasos mínimos con datos ficticios, esperado/observado e impacto. No realizar pruebas fuera de los activos autorizados ni desactivar controles del navegador o red para obtener una captura.

## English

This is a static learning application, not a remote execution service. Native exercises require a separately authorized lab. OS learning records use a dedicated storage key and are optional, local and unencrypted. They are not authentication or certified learning evidence. Do not store secrets or personal data. Report sensitive problems privately through an available GitHub advisory channel or request a private channel from the maintainer without disclosing the issue publicly.
