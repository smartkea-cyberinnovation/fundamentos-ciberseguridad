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
