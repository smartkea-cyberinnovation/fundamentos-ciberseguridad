# Revisar, integrar y publicar el campus

## Fuentes de verdad

| Elemento | Ruta |
|---|---|
| Código y contenido canónicos | `https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad.git` |
| Rama publicada | `main` |
| Ramas y propuestas | [Branches](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/branches) y [Pull requests](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pulls) |
| Curso de informática | `formacion/introduccion-informatica/` |
| Banco editable | `formacion/introduccion-informatica/banco-preguntas.json` |
| Aplicaciones | `campus/assets/`, `campus/os_classroom/`, `campus/exam/`, `term/` |
| Publicación | `wrangler.jsonc`, `campus/cloudflare.py`, `campus/stage_worker.py` |
| Revisión y deuda | `docs/security/`, `docs/BACKLOG.md`, Issues y PR |

Los archivos `campus/dist`, `campus/worker-dist`, `term/dist` y los ZIP de publicación son derivados. La documentación privada, hilos de correo y enlaces del chat pertenecen al tracker de coordinación autorizado; no deben incorporarse a estos activos públicos.

## Plan de trabajo y estados

Una tarea pasa por **pendiente → en curso → en revisión → validada → integrada → desplegada → verificada en producción**. Solo se omiten las etapas que no apliquen y se explica el motivo. «Bloqueada» exige dependencia y siguiente acción; «cerrada» exige criterio de aceptación cumplido. Preparar una configuración y observarla aplicada son estados diferentes.

1. **Inventario.** Leer la rama remota y sus cambios; identificar propósito, propietario, dependencias y alcance. Comparar commits y contenido para detectar squash, snapshots e historias sin ancestro común.
2. **Integración.** Trabajar desde el último `main` en una rama aislada. Conservar IDs y formatos de progreso. Separar cambios funcionales, contenido y mantenimiento en commits revisables.
3. **Revisión.** Explicar problema, comportamiento resultante, riesgo material y pruebas. Resolver comentarios con evidencia; actualizar el head exige volver a evaluar los checks pertinentes.
4. **Aceptación.** Ejecutar las suites que ejercitan el cambio y los gates obligatorios de CI. Revisar SARIF y fallos; un proceso que terminó correctamente puede haber comunicado hallazgos.
5. **Merge.** Releer el SHA de la PR y usar ese SHA como condición de la integración. No forzar ramas compartidas ni borrar una fuente antes de comprobar su traslado.
6. **Publicación.** Dejar que Workers Builds publique el `main` seleccionado. Un build de preview no demuestra activación de producción.
7. **Comprobación.** Observar HTTP, procedencia, catálogos, test, aula, rutas, cabeceras y recursos desde la URL pública. Registrar hora UTC y SHA.
8. **Cierre.** Enlazar PR, ejecución, resultado y pendientes en el tracker; deprecar el origen solo cuando sus diferencias estén contabilizadas y la migración aceptada.

## Inicio local

```sh
git clone https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad.git
cd fundamentos-ciberseguridad
git fetch origin
git switch -c feat/descripcion-del-cambio origin/main
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
python3 campus/serve.py --port 8788
```

Python genera el sitio; el runtime de producción no necesita npm. CI utiliza Python 3.13 y Node 22. Para pruebas web, usar las versiones de Playwright y los motores especificados en cada workflow. No instalar dependencias de la antigua aplicación Next.js para compilar este campus.

## Validación según el cambio

| Cambio | Evidencia necesaria |
|---|---|
| Markdown, catálogo, traducción | Build, validación de enlaces/IDs, pruebas Python afectadas, navegación del recurso en los idiomas declarados |
| Modelo de progreso o examen | Pruebas JavaScript y regresiones de navegador: importación, almacenamiento bloqueado y varias pestañas |
| Aula OS | Modelo, catálogo y navegador en Chromium, Firefox y WebKit; conservar atribución de tiempo y vida del registro |
| CSS y navegación | Teclado, foco, contraste y reflujo; viewports usados por CI; no ocultar errores ni contenido obligatorio |
| Worker, rutas o empaquetado | Runtime estático, clean build, 404, MIME, prefijo, manifiestos y prueba pública del SHA desplegado |
| TERM o contenedores | Curso y laboratorio, configuración Compose/Swarm, aislamiento, usuario efectivo y regresiones del terminal |
| Actions o dependencias | Procedencia del SHA, permisos mínimos, CodeQL, suites consumidoras y rollback conocido |

Comprobaciones del campus después de generar los catálogos:

```sh
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
node --test campus/tests/*.test.mjs
python3 campus/tests/browser_bilingual.py
python3 campus/tests/browser_exam.py
python3 campus/tests/browser_os_study.py
```

Los workflows añaden los demás motores, el kit y la planificación. No declarar ejecutado un laboratorio Windows/macOS a partir de una prueba de navegador o una validación sintáctica.

## Cadena de suministro y revisión de código

Las Actions están fijadas a commits completos verificados en el repositorio del proveedor. Dependabot abre propuestas para revisarlas. Se conserva `contents: read` y `persist-credentials: false`; el job CodeQL recibe únicamente la escritura de eventos de seguridad que necesita para subir resultados. Los workflows de PR no usan `pull_request_target` para ejecutar código de la propuesta con credenciales de despliegue.

Wrangler 4.151.1 se instala desde `campus/tooling/package-lock.json` con `npm ci --ignore-scripts`. El wrapper verifica que el manifiesto, lockfile y binario local coinciden. CI audita dependencias y prueba `deploy --dry-run` y `versions upload --dry-run` desde un checkout sin activos generados. Al aceptar una actualización de Dependabot, actualizar también la constante `WRANGLER` y las referencias operativas; el runtime del alumno sigue sin paquetes npm.

CodeQL analiza Python, JavaScript/TypeScript y los workflows en PR, en `main` y semanalmente. Sus SARIF se conservan como evidencia durante 14 días. Revisar y clasificar cada hallazgo; no ocultar una regla para obtener un check verde. Los datos docentes sintéticos pueden requerir contexto, pero una exclusión debe justificar el límite exacto.

Las protecciones administrativas se documentan como configuración efectiva: exigir revisión y checks apropiados, impedir force-push y borrado accidental, revisar acceso de Actions/Cloudflare y mantener detección de secretos. No marcar una política como activa por haber escrito esta recomendación. Antes de exigir un check, comprobar su nombre y sus filtros para evitar bloquear PR válidas que no lo ejecutan.

## Aceptación en Cloudflare

| Servicio | URL canónica |
|---|---|
| Campus | [smartkea.com/introduccion-ciberseguridad/](https://smartkea.com/introduccion-ciberseguridad/) |
| Test | [smartkea.com/introduccion-ciberseguridad/examen/](https://smartkea.com/introduccion-ciberseguridad/examen/) |
| Aula OS | [smartkea.com/introduccion-ciberseguridad/sistemas/](https://smartkea.com/introduccion-ciberseguridad/sistemas/) |
| TERM | [www.smartkea.com/fundamentos-ciberseguridad/term/](https://www.smartkea.com/fundamentos-ciberseguridad/term/) |

La publicación principal usa el dominio sin `www`; TERM tiene su dominio canónico con `www` y redirección desde el dominio raíz. Mantener las rutas del Worker; no aplicar un fallback SPA a todo `smartkea.com`. Un recurso inexistente debe devolver 404 y un JavaScript válido su MIME correcto.

Contrastar el check **Workers Builds: fundamentos-ciberseguridad** del commit de `main` con `sourceCommit` y `sourceDirty: false` del `build-info.json` público. Confirmar el hash de `exam/questions.json`, 100 preguntas y 20 por intento. Verificar también la versión y el catálogo de TERM. Conservar esas observaciones fuera del checkout de fuentes para no alterar la procedencia calculada.

Si falla un criterio material, aplicar [WORKERS-RECOVERY.md](../../campus/WORKERS-RECOVERY.md): recuperar la versión anterior conocida y comprobarla; después corregir en una nueva PR con una regresión. No borrar el estado del alumno para resolver un fallo de código.

## Entrega desde Figma Make

Usar el paquete de `docs/figma-make/` como contrato. Verificar la capacidad vigente de Make antes de prometer sincronización con un repositorio existente. Una exportación debe llegar al repositorio canónico mediante una PR revisada, conservando la fuente docente, IDs, rutas y pruebas. La aplicación generada por Make no debe activar un backend, proveedor IA, autenticación o analítica por defecto.

Para el detalle operativo siguen vigentes [DEPLOY.md](../../DEPLOY.md), [la política de seguridad](../../SECURITY.md) y [el backlog](../BACKLOG.md).
