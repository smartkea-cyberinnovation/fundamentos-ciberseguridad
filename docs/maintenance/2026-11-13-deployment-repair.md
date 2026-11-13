# Reparación de CI y publicación · 13 de noviembre de 2026

## Diagnóstico comprobado

El PR #34 actualizaba Wrangler de 4.154.0 a 4.158.0, pero no estaba integrado. `main` seguía en `a86caf07350de3e2ef6c60de1f174f2eb4377271`.

- El [run del campus del 9 de noviembre](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/42587293487) terminó durante la instalación de navegadores: `ubuntu-latest` resolvió a Ubuntu 26.04 y Playwright 1.55.0 rechazó ese sistema. La compilación y las pruebas unitarias anteriores habían pasado.
- El wrapper mantenía un segundo literal `WRANGLER = '4.154.0'`, incompatible con el manifiesto y lockfile actualizados por Dependabot. El [run de Cloudflare](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/42587293493) falló antes de la auditoría y del runtime local.
- El verificador público esperaba como máximo doce intentos separados por diez segundos. En la entrega anterior la comprobación había terminado antes de la publicación de Workers Builds. Compilar, generar un artefacto y publicar son estados distintos.

La aceptación HTTPS del commit de octubre se volvió a ejecutar el 13 de noviembre y pasó en el [run 40723809521](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/40723809521). Esto verifica aquella edición de TERM; no acredita aún esta reparación ni todas las rutas del dominio.

## Correcciones

Los cinco workflows de aceptación/publicación usan `ubuntu-24.04`. Se conserva la cobertura de navegadores, Docker/ttyd, ShellCheck, configuración Swarm, CodeQL y auditoría de dependencias: no se omiten pruebas.

Wrangler toma su versión exacta del manifiesto. El wrapper comprueba también las declaraciones del lockfile v3, la URL del registro npm y los metadatos de integridad; ejecuta `npm ci --ignore-scripts` y comprueba la versión realmente instalada. No admite rangos, versiones preliminares, fuentes externas ni dependencias directas adicionales.

TERM se valida también cuando cambian el wrapper o el tooling. La aceptación pública permite hasta sesenta intentos y conserva el historial. Mientras no aparece el SHA esperado solo consulta los metadatos. Un fallo de hash, CSP o esquema detiene la comprobación inmediatamente; no se convierte en éxito por repetirlo.

El workflow del campus genera los catálogos una sola vez antes de las pruebas JavaScript y conserva los informes de compilación y validación. No se modifica el temario ni el almacenamiento de progreso.

## Validación y cierre

Validación local: 204 pruebas Python del campus, 25 Python de TERM, 162 Node del campus y 17 Node de TERM: **408 correctas**. Se añaden dieciséis regresiones. Compilación y staging correctos; los hashes de ambos catálogos del campus y del curso TERM se mantienen.

Estos resultados locales no son una publicación. Para cerrar la entrega, deben terminar correctamente los workflows del PR y comprobarse el SHA integrado por HTTPS tras Workers Builds. La evidencia final se registra en el PR #34 y en sus runs, no se anticipa aquí.

La incidencia #31 de guardado multipestaña en WebKit permanece abierta y no se considera resuelta por esta reparación. No se despliega una VM de alumnos ni se modifica Access/Tunnel. No se añade un segundo publicador automático ni se requieren credenciales en el chat.
