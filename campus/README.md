# Campus ES/EN · Fundamentos de ciberseguridad / Cybersecurity foundations

**Wiktor Nykiel · 2.3.0 · Independent learning · Light interface.**

## Español

Campus estático para estudiar, repasar en presentación y seguir prácticas guiadas. La edición activa conserva **32 módulos, 96 fichas, ocho guías ampliadas, 21 referencias y 480 horas planificadas**. Español e inglés son ediciones docentes paralelas con los mismos IDs, prerrequisitos y horas. Las cifras no equivalen a asistencia ni ejecución de laboratorios.

El selector ES/EN cambia interfaz, contenidos, fichas, autoevaluaciones y referencias sin reiniciar progreso. El índice filtra por texto, bloque y avance; la biblioteca y búsqueda conectan las lecturas. La presentación usa el contenido del módulo, no una segunda copia de diapositivas. Hay lectura continua sin JavaScript en `lectura.html` y `reading.en.html`.

**Continuidad:** las marcas y notas se guardan en este navegador; exportación/importación JSON para copia completa y enlace de progreso para una copia sin notas. La ruta de continuación se conserva por pestaña. Compartir una lección no comparte progreso. El enlace de progreso no es una cuenta ni transfiere autenticación. Leer [PROGRESO.md](PROGRESO.md) antes de compartir.

**Guía, no terminal remota:** identifica entorno, ejecuta manualmente, comprueba, documenta evidencia y recupera. Las consultas de identificación no convierten una práctica Linux en Windows o macOS. No se ejecuta texto suministrado por alumnos o IA.

## English

A static campus for reading, presentation-based review and guided lab work. The active course has **32 modules, 96 lab briefs, eight extended guides, 21 references and 480 planned hours**. English and Spanish editions retain the same learning IDs, prerequisites and planned hours. These are not attendance or lab-execution records.

The language selector changes the interface and learning material without resetting progress. Use the syllabus filters, internal index, search, library and previous/next navigation. Continuous reading is also available without JavaScript.

Learning records remain in the browser. JSON backups include notes; portable links exclude them and transfer only a snapshot of milestones and resume location. A link is not authentication, cloud synchronization or a certificate. Anyone holding the full link can read and import it. See [progress and transfer](PROGRESO.md).

The guide does not execute commands or connect to hosts. Complete native tasks manually inside the authorized lab; a mobile viewport is not a virtual operating system.

## Build and preview / Compilar y previsualizar

From the repository root, using Python 3.11 or later:

```sh
python3 campus/build.py
python3 campus/check_release.py
python3 campus/serve.py --port 8788
```

Open `http://127.0.0.1:8788/?lang=es` or `http://127.0.0.1:8788/?lang=en`. No npm installation, account, database or API key is required for the static campus. Node and Playwright are test tools. The independent legacy Next.js application remains in the original repository; this repository contains the static campus and teaching materials.

## Documentation / Documentación

| Topic | Document |
|---|---|
| Cloudflare Pages and existing Workers setup | [DEPLOY-CLOUDFLARE.md](DEPLOY-CLOUDFLARE.md) |
| Progress, transfers and privacy | [PROGRESO.md](PROGRESO.md) |
| Optional identity and OTP design, not enabled | [IDENTITY-OPTIONAL.md](IDENTITY-OPTIONAL.md) |
| Editorial design and accessibility scope | [DESIGN.md](DESIGN.md) |
| Content authoring and translations | [EDICION.md](EDICION.md) |
| Tests and limitations | [QA.md](QA.md) |
| Integration and acceptance | [INTEGRATION.md](INTEGRATION.md) |

The expansion master plan remains in `formacion/plan-maestro/` on the main branch: 18 areas and 108 proposed units, not 108 additional active bilingual lessons. Its English overview is not a complete translation of that separate reference. This release does not change the course hours, repository license, access policies or account settings. No institutional name, logo, endorsement or affiliation is used.
