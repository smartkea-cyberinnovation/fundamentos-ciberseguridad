# Estado, validación y mantenimiento

Edición **1.1**, 2026-09-14. El diseño curricular se conserva y se añade un kit ejecutable sobre datos sintéticos. Las pruebas de código y la ejecución completa de una práctica nativa son evidencias diferentes.

## Evidencias disponibles

El [informe de pruebas](qa/RESULTADOS.md) registra 42 pruebas del kit y del servidor HTTP local, más ocho de planificación. Se ejecutaron en Linux con Python 3.13.5 y Bash 5.2.37. La sintaxis Bash también se comprobó. Los archivos de resultados y sus límites se conservan con el material.

**No se ejecutaron Windows/CMD/BAT/PowerShell, macOS/zsh, Docker, Compose ni Swarm.** Sus ejemplos y manifiestos son material preparado para validación posterior. No se utilizaron modelos de IA ni se hicieron consultas a indicadores externos para probar el kit.

No se afirma que los 96 laboratorios estén realizados, ni que la formación completa esté validada para una cohorte. La resolución de funciones offline, una prueba HTTP y el análisis de un ejemplo no acreditan administración nativa, adquisición forense o un despliegue seguro en producción.

## Coherencia de carga

30 módulos de 14 h, uno de 20 h y otro de 40 h: 480 h. Teoría 168 h; práctica 312 h. La planificación verifica 240 sesiones y 96 laboratorios con minutos asignados. Los ocho runbooks desarrollan laboratorios existentes, sin incrementar duración ni atribuir dominio adicional.

## Registro antes de impartir

Por laboratorio: ID, fecha, revisor, SO/edición/versión/arquitectura, shell, herramientas, dataset, pasos, resultados, errores, prueba negativa, duración real, permisos, aislamiento, recuperación y dictamen. Windows/macOS requieren equipo nativo para validar sus controles; una captura o parser en otro SO debe etiquetarse como análisis offline.

Estados: diseñado; revisado documentalmente; implementación parcial probada; probado en entorno nativo identificado; aprobado para cohorte; bloqueado; retirado. No cambiar de estado por actualizar fecha o tener un test de sintaxis.

## Límites de seguridad

El marcador del workspace evita errores accidentales de alcance, pero no acredita procedencia o autorización ni crea una sandbox contra un adversario. Las herramientas están orientadas a archivos pequeños, sintéticos, estáticos y bajo control del alumno. No son un colector forense ni un analizador hostil de producción.

Los scripts nativos son ejemplos didácticos de alcance menor que el validador Python. BAT mantiene limitaciones explícitas de parsing y errores. El servicio HTTP no sirve archivos arbitrarios, pero carece de autenticación/TLS y no debe exponerse fuera del laboratorio. La imagen base debe revisarse y fijarse por digest autorizado antes de una cohorte que utilice Docker.

## Bloqueo y mantenimiento

Bloquear una práctica si falta licencia, función nativa, recuperación o procedencia verificable; si exige privilegios injustificados, datos reales o desactivación de protección; si afecta al anfitrión; o si el resultado no es reproducible. Registrar alternativa y no dar por superada la competencia afectada.

Mantener changelog, versiones, evidencia de pruebas y revisión de soporte. Ante una actualización, repetir las comprobaciones afectadas; una versión fijada necesita mantenimiento. Antes de compartir, revisar datos e historial, derechos y separación de soluciones/expedientes. Esta edición sigue privada y no constituye certificación oficial.
