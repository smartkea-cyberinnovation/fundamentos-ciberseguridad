# SmartKEA · Fundamentos de ciberseguridad

**Wiktor Nykiel · Campus 3.0 · Informática, sistemas, redes, ciberseguridad, GRC, IA e innovación · Español e inglés**

**Campus público: [smartkea.com/introduccion-ciberseguridad/](https://smartkea.com/introduccion-ciberseguridad/)**

**Código: [smartkea-cyberinnovation/fundamentos-ciberseguridad](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad)**

Curso integral y progresivo para comprender cómo hemos llegado a la informática actual, construir y operar sistemas, protegerlos, gobernar su riesgo y conectar el aprendizaje con profesiones, instituciones, investigación e innovación. El itinerario evita imponer tiempos: se organiza por prerrequisitos, resultados de aprendizaje, práctica y evidencias.\n\nEl campus reúne lectura, presentación a pantalla completa, búsqueda, autoevaluación y progreso local exportable. El plan maestro y el itinerario integral se mantienen como fuentes curriculares versionadas; las referencias externas deben verificarse antes de cada edición.

## Ruta de estudio integral / Integrated study pathway

Empieza por [D26: mapa de informática](https://smartkea.com/introduccion-ciberseguridad/#/recurso/D26), luego historia y hardware, redes y servicios, controles y datos, identidad y profesiones. Las once lecturas tienen texto completo en español e inglés dentro de sus fuentes; el campus selecciona el idioma sin traducir comandos en ejecución.

| Recurso | Contenido desarrollado |
|---|---|
| [D26 · Informática](formacion/itinerario-integral/01-computing.md) | Representación, algoritmos, procesos, persistencia, red y evidencia |
| [D27 · Historia](formacion/itinerario-integral/02-history.md) | Computación, IA, Internet/Web, móvil y siete casos empresariales con fuentes |
| [D28 · Hardware](formacion/itinerario-integral/03-hardware.md) | Ciudad como analogía y sus límites; arquitectura, servidores, DC, IA y cuántica |
| [D29 · Redes](formacion/itinerario-integral/04-networks.md) | Capas, equipos, topologías, Wi-Fi6/6E/7, 5G y normalización 6G |
| [D30 · Arquitecturas web](formacion/itinerario-integral/05-web.md) | De estático/WordPress a aplicaciones empresariales, cloud y contenedores |
| [D31 · Seguridad y equipos](formacion/itinerario-integral/06-security.md) | CIA, CSF, responsabilidades, procedimientos y evidencia |
| [D32 · Información](formacion/itinerario-integral/07-information.md) | Clasificación, TLP, DLP, cifrado, ciclo de vida y privacidad |
| [D33 · Identidades](formacion/itinerario-integral/08-identity.md) | JML, entidad–centro–puesto, SoD, RBAC/ABAC/PAM y acceso efectivo |
| [D34 · Profesiones](formacion/itinerario-integral/09-careers.md) | Árbol funcional TIC/ciber, fuentes laborales, IA y portfolio |
| [D35 · Glosario](formacion/itinerario-integral/10-glossary.md) | 36 fichas ES/EN complementarias, capacidades y ejemplos abiertos/comerciales |
| [D36 · Fuentes](formacion/itinerario-integral/11-sources.md) | Referencias primarias, fechas, límites y método para noticias/profundización |\n| [D37 · Itinerario maestro](formacion/itinerario-integral/12-curriculum.md) | U00–U15: historia, sistemas, redes, desarrollo, ciber, GRC, regulación, instituciones, IA y carrera |\n| [D38 · Ecosistema](formacion/itinerario-integral/13-ecosystem.md) | CCN-CERT, INCIBE, CNI, CNPIC, FCSE, MCCE, ENISA, CERT-EU, OTAN, labs, conferencias e innovación |\n| [D39 · Biblioteca/videoteca](formacion/itinerario-integral/14-library.md) | Libros gratuitos/de pago, Amazon como vía de compra, TED/TEDx, universidades y conferencias |\n| [D40 · Glosario maestro](formacion/itinerario-integral/15-master-glossary.md) | Vocabulario transversal y pares conceptuales que no deben confundirse |

[Índice y alcance de la ampliación](formacion/itinerario-integral/README.md). INT-L01–INT-L18 son dieciocho diseños de actividades integradoras, no dieciocho ejecuciones acreditadas. Los árboles profesionales y el glosario son ampliables, no una lista de todos los títulos o fabricantes existentes.

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

La observación HTTP se puede repetir explícitamente con `python3 campus/audit_publication.py --output campus/qa/publication.json`: siete recursos públicos fijos, sin login ni cambios de cuenta. Una prueba del build no equivale a esa observación en producción. La ampliación contiene un [registro de revisión](docs/maintenance/2026-09-21-integral-curriculum.md); un commit integrado no se declara publicado hasta observarlo en el servicio.

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
python3 campus/build.py && python3 campus/check_release.py
node --test campus/tests/*.test.mjs
python3 formacion/plan-maestro/validar.py
```

Los workflows conservan aceptación Python/JavaScript, Chromium/WebKit, validación del plan maestro y comprobación del runtime estático. Los resultados corresponden al commit de cada ejecución; véanse [alcance y límites](campus/QA.md) y [lecturas operativas](formacion/sistemas-operativos/operacion/README.md).

## Materiales y estructura

| Necesidad | Recurso |
|---|---|
| Empezar y estudiar | [Guía de estudio](formacion/sistemas-operativos/COMO-ESTUDIAR.md) |
| Temario, prácticas, evaluación y fuentes | [Índice docente](formacion/sistemas-operativos/README.md) |
| Historia, hardware, redes, datos e identidades | [Itinerario integral D26–D36](formacion/itinerario-integral/README.md) |
| Control operativo de sistemas | [Lecturas D22–D25](formacion/sistemas-operativos/operacion/README.md) |
| Ampliación y continuidad | [Plan maestro](formacion/plan-maestro/README.md) |
| Editar fuentes y traducciones | [Guía de edición](campus/EDICION.md) |
| Aislamiento del laboratorio | [Entorno de prácticas](formacion/sistemas-operativos/LABORATORIO.md) |
| Copiar o trasladar progreso | [Progreso y privacidad](campus/PROGRESO.md) |
| Procedencia y alcance de este repositorio | [Migración](docs/MIGRATION.md) |

```text
campus/                        Web estática, compilador, ES/EN, pruebas y operación
formacion/sistemas-operativos/  Temario, lecciones, prácticas, kit y evaluación
formacion/itinerario-integral/   Once lecturas desarrolladas ES/EN y fuentes
formacion/plan-maestro/         Referencia curricular y continuidad
.github/workflows/             Validación y aceptación
wrangler.jsonc                 Worker y ruta pública
docs/MIGRATION.md              Origen del snapshot y alcance del traslado
```

Este repositorio comienza con una copia del contenido integrado en `main` del [repositorio original](https://github.com/WiktorNykiel/fundamentos-ciberseguridad), sin importar su historial ni la aplicación Next.js heredada. Se conserva la autoría de Wiktor Nykiel; la visibilidad pública no concede una licencia nueva.

El asistente orienta la práctica manual y el campus guarda el progreso en el navegador. No ejecuta comandos del alumno ni sincroniza cuentas. Exportar el progreso antes de cambiar de origen o dispositivo y mantener secretos y datos personales fuera de las notas.
