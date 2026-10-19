# Seguridad del proyecto

Este repositorio publica material docente y una aplicación web estática. La seguridad del alumno y de terceros forma parte del diseño del curso.

## Reportar una vulnerabilidad

No publiques detalles explotables, credenciales, datos personales ni pruebas contra sistemas de terceros en Issues, Discussions o Pull Requests.

Si detectas una vulnerabilidad en el campus, en el proceso de build o en la cadena de publicación, notifícala de forma privada al mantenedor/organización mediante los canales privados disponibles en GitHub. Incluye, cuando sea posible:

- componente y versión/commit afectado;
- impacto observado;
- pasos mínimos de reproducción en un entorno propio;
- evidencia no sensible;
- mitigación propuesta.

No se autoriza por este documento a probar infraestructura, cuentas, dominios o servicios que no sean propios o para los que no exista autorización explícita.

## Laboratorios

Las prácticas deben ejecutarse en máquinas propias, laboratorios aislados o entornos expresamente autorizados. Antes de modificar permisos, red, cifrado, identidad, firewall o almacenamiento, el alumno debe conocer el rollback y conservar una copia recuperable.

Nunca deben introducirse en el repositorio secretos, tokens, contraseñas, claves privadas, datos personales reales ni evidencias de clientes.

## Dependencias y publicación

Los cambios de código deben pasar las validaciones existentes antes de integrarse. La integración en `main` y la publicación en producción son estados distintos: un commit no se considera desplegado hasta que la versión servida haya sido observada.

Consulta [DEPLOY.md](DEPLOY.md) para operación y recuperación.

## Alcance

Este documento describe la política del proyecto. No constituye autorización para realizar pruebas de seguridad sobre terceros ni sustituye los procedimientos de divulgación responsable de los proveedores afectados.

## Aula OS y test de práctica

El aula y el simulador son aplicaciones estáticas. No ejecutan los comandos mostrados ni envían respuestas, notas o progreso a un servidor. El registro de OS y el intento del test utilizan claves locales independientes; la restauración valida formato, catálogo e identificadores antes de usar los datos. Bloquear almacenamiento no debe impedir practicar en memoria.

El banco incluye respuestas y explicaciones como material docente público. No lo uses para evaluar identidad, certificación o calificaciones oficiales. Los ejemplos se ejecutan manualmente sobre datos de laboratorio; los enlaces de repaso del test se limitan a contenido del campus.

## Revisión continua y privacidad

La revisión del 18-10-2026 documenta los límites de entrada/salida, almacenamiento, empaquetado, laboratorios y CI en [el informe técnico](docs/security/REVIEW-2026-10-18.md). Las Actions se fijan a commits completos; CodeQL analiza Python, JavaScript y los workflows, y conserva resultados SARIF. Revisar los resultados del commit concreto antes de cerrar una tarea: ejecutar un detector no equivale a acreditar ausencia de vulnerabilidades.

Las decisiones sobre alumnos identificados, proveedores, retención y una futura IA externa se detallan en [privacidad e IA](docs/security/PRIVACY-AND-AI.md). El runtime actual no habilita un backend de alumnos ni envía sus notas a un modelo. Las rutas del mismo dominio no aíslan el almacenamiento frente a otros scripts del mismo origen.

Consulta [el backlog](docs/BACKLOG.md) para controles pendientes y [el procedimiento de revisión](docs/engineering/REVIEW-AND-RELEASE.md) para evidencias y recuperación.
