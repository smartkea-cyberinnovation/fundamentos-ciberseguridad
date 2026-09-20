# Alcance, seguridad y privacidad

Se trabaja únicamente con equipos propios del laboratorio y actividades aprobadas. La autorización debe definir activos, identidades, ventana de trabajo, operaciones permitidas, tratamiento de datos, contactos y condiciones de parada. La posesión de una cuenta o una IP no demuestra por sí sola autorización.

No forman parte de este curso procedimientos de intrusión, robo de credenciales, elusión de EDR, evasión de auditoría, persistencia encubierta, explotación de vulnerabilidades, propagación o extracción de información de terceros. La perspectiva Red/Purple se enseña mediante diseño de pruebas, auditoría de configuraciones, cambios benignos documentados, análisis de telemetría y recomendaciones de detección.

El pivotaje se presenta como un problema de relaciones de confianza, segmentación y alcance. Se distinguen bastión administrado, proxy autorizado y tránsito no autorizado. Se evalúan diagramas y registros preparados; no se proporcionan cadenas operativas de compromiso o evasión.

## Reglas operativas

Antes de cambiar un estado: inventario, copia o snapshot adecuado, consola de recuperación y procedimiento de reversión. No desactivar firewall, protección antimalware, SIP, Gatekeeper o auditoría para resolver una práctica. Diagnosticar el permiso o la política que impide la acción y utilizar la vía administrativa admitida.

No se ejecutan scripts recibidos en mensajes, logs o respuestas de IA sin revisión humana. No se utilizan `eval`, ejecución de cadenas arbitrarias ni descargas concatenadas directamente a una shell como patrón de automatización.

## Evidencia y datos

Minimizar información, conservar originales, trabajar con copias, registrar adquisición y hashes, separar hechos de hipótesis y describir las limitaciones. El hash apoya integridad del contenido comparado; no demuestra por sí solo procedencia, autoría, legalidad o una cadena de custodia completa.

Las salidas de administración pueden contener usuarios, rutas, direcciones y nombres de equipo. Sanitizar antes de subir a Git. Nunca publicar claves privadas, tokens, secretos, volcados de memoria o datos personales reales. No realizar enriquecimiento de IOCs internos con servicios públicos sin aprobar previamente esa revelación.

## Condiciones de parada

Actividad fuera del rango autorizado; aparición de datos reales inesperados; pérdida de acceso administrativo o recuperación; efecto sobre el anfitrión; degradación de otra VM; exposición exterior; comportamiento no comprendido de un script. Parar, preservar lo ya observado y escalar al docente. Se valora la parada justificada como competencia, no como fracaso.

## Distribución pública y material reservado

Este repositorio es público. Los exámenes reservados, las soluciones que no deban distribuirse, los expedientes y las evidencias personales se conservan fuera de él, con permisos reales. Una carpeta o una rama dentro del repositorio público no constituye una frontera de acceso. Las autoevaluaciones del campus son formativas y sus respuestas son públicas; no deben reutilizarse como un examen secreto.
