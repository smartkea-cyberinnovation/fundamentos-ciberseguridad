# SmartKEA · Fundamentos de ciberseguridad

**Wiktor Nykiel · Campus 2.4 · Linux, Windows y macOS · Español e inglés**

**Campus público: [smartkea.com/introduccion-ciberseguridad/](https://smartkea.com/introduccion-ciberseguridad/)**

**Código: [smartkea-cyberinnovation/fundamentos-ciberseguridad](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad)**

Curso para comprender, administrar, automatizar y proteger sistemas. Conserva **32 módulos, 96 fichas de laboratorio y 480 horas planificadas**: 168 de teoría y 312 de práctica. Español e inglés comparten IDs, prerrequisitos y progreso. Las ocho guías ampliadas y las fichas describen actividades; estas cifras no certifican ejecución ni acreditación.

El campus reúne lectura, presentación, búsqueda, autoevaluación y progreso local exportable. La biblioteca contiene **25 referencias**, incluidas las cuatro nuevas lecturas de control operativo. El [plan maestro](formacion/plan-maestro/README.md) añade una referencia de desarrollo de 18 áreas y 108 unidades propuestas, separada del catálogo activo.

## Sistemas operativos: control verificable

| Recurso | Contenido |
|---|---|
| [D22 · Identidades y bastionado](formacion/sistemas-operativos/operacion/01-identidad-bastionado.md) | Cuentas locales, LDAP/AD/Entra, ciclo de vida, privilegios, perfiles y política efectiva |
| [D23 · Redes y recursos](formacion/sistemas-operativos/operacion/02-redes-recursos.md) | ACL, shares SMB/Samba/NFS, segmentación y restauración con permisos |
| [D24 · Navegación y TLS](formacion/sistemas-operativos/operacion/03-navegacion-tls.md) | DNS/proxy/firewall, cuentas personales/corporativas, mensajería, inspección y privacidad |
| [D25 · Detección y aceptación](formacion/sistemas-operativos/operacion/04-deteccion-laboratorios.md) | Dieciséis controles, doce diseños de laboratorio, evidencias, triaje y recuperación |

[English teaching edition](campus/locales/en/operations-control.md). Las lecturas se enlazan desde los módulos pertinentes y la biblioteca; no añaden horas ni alteran el progreso. DNS no distingue todas las cuentas de un SaaS; inspección TLS no elimina E2EE. Los diseños no aplican restricciones a dispositivos reales ni acreditan una auditoría completa.

## Ruta pública y publicación

| Elemento | Configuración |
|---|---|
| URL del campus | `https://smartkea.com/introduccion-ciberseguridad/` |
| Entrada sin barra | `https://smartkea.com/introduccion-ciberseguridad` → redirección a la URL con barra, conservando parámetros |
| Worker | `fundamentos-ciberseguridad` |
| Ruta del Worker | `smartkea.com/introduccion-ciberseguridad/*` |
| Repositorio / rama de producción | `smartkea-cyberinnovation/fundamentos-ciberseguridad` / `main` |
| Workers Builds: raíz / build command | Raíz del repositorio / vacío |
| Deploy de producción | `python3 campus/cloudflare.py deploy` |
| Preview de otras ramas | `python3 campus/cloudflare.py preview` |
| Variables de build | `SKIP_DEPENDENCY_INSTALL=1`, `PYTHON_VERSION=3.13.3`, `NODE_VERSION=22.23.2` |
| Wrangler fijado | `4.132.0` |

El custom build de Wrangler compila, valida y prepara los activos antes de subirlos. La ruta sólo cubre el campus; la web corporativa conserva sus otras rutas. La redirección de barra final se configura por separado en la zona Cloudflare.

Consultar el commit servido en [build-info.json](https://smartkea.com/introduccion-ciberseguridad/build-info.json) y compararlo con la versión activa. [Publicación y recuperación](campus/WORKERS-RECOVERY.md) documenta la conexión Git, aceptación y rollback; [configuración de Cloudflare](campus/DEPLOY-CLOUDFLARE.md) incluye la alternativa portable de Pages.

La observación HTTP se puede repetir explícitamente con `python3 campus/audit_publication.py --output campus/qa/publication.json`: siete recursos públicos fijos, sin login ni cambios de cuenta. Una prueba del build no equivale a esa observación en producción.

## Compilar y comprobar

Desde la raíz, con Python 3.11 o posterior:

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
python3 campus/serve.py --port 8788
```

Abrir `http://127.0.0.1:8788`. La compilación y el servidor local no necesitan paquetes Python, cuentas, API keys ni dependencias npm. Node y Playwright se usan para pruebas; Node/npm también permite ejecutar Wrangler. `build` y `check` no publican; `dry-run` comprueba Wrangler sin subir activos; `deploy` publica y `preview` sólo sube una versión de prueba.

```sh
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
node --test campus/tests/*.test.mjs
python3 formacion/plan-maestro/validar.py
```

Los workflows conservan aceptación Python/JavaScript, Chromium/WebKit, validación del plan maestro y comprobación del runtime estático. Los resultados corresponden al commit de cada ejecución; véanse [alcance y límites](campus/QA.md) y [lecturas operativas](formacion/sistemas-operativos/operacion/README.md).

## Materiales y estructura

| Necesidad | Recurso |
|---|---|
| Empezar y estudiar | [Guía de estudio](formacion/sistemas-operativos/COMO-ESTUDIAR.md) |
| Temario, prácticas, evaluación y fuentes | [Índice docente](formacion/sistemas-operativos/README.md) |
| Control operativo de sistemas | [Lecturas D22–D25](formacion/sistemas-operativos/operacion/README.md) |
| Ampliación y continuidad | [Plan maestro](formacion/plan-maestro/README.md) |
| Editar fuentes y traducciones | [Guía de edición](campus/EDICION.md) |
| Aislamiento del laboratorio | [Entorno de prácticas](formacion/sistemas-operativos/LABORATORIO.md) |
| Copiar o trasladar progreso | [Progreso y privacidad](campus/PROGRESO.md) |
| Procedencia y alcance de este repositorio | [Migración](docs/MIGRATION.md) |

```text
campus/                        Web estática, compilador, ES/EN, pruebas y operación
formacion/sistemas-operativos/  Temario, lecciones, prácticas, kit y evaluación
formacion/plan-maestro/         Referencia curricular y continuidad
.github/workflows/             Validación y aceptación
wrangler.jsonc                 Worker y ruta pública
docs/MIGRATION.md              Origen del snapshot y alcance del traslado
```

Este repositorio comienza con una copia del contenido integrado en `main` del [repositorio original](https://github.com/WiktorNykiel/fundamentos-ciberseguridad), sin importar su historial ni la aplicación Next.js heredada. Se conserva la autoría de Wiktor Nykiel; la visibilidad pública no concede una licencia nueva.

El asistente orienta la práctica manual y el campus guarda el progreso en el navegador. No ejecuta comandos del alumno ni sincroniza cuentas. Exportar el progreso antes de cambiar de origen o dispositivo y mantener secretos y datos personales fuera de las notas.
