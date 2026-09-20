# Content authoring / Edición del campus ES/EN

## Canonical identifiers

Keep M01–M32, L01A–L32C, references D01–D21 and the existing progress v1 key stable. New content must not silently reorder milestones or change what a saved ID means. `build.py` builds Spanish from `formacion/sistemas-operativos/`; `bilingual.py` reads the English teaching edition in `campus/locales/en/` and checks parity.

English inputs: `foundations-linux.md`, `windows-macos.md`, `operations-capstone.md`, `references-core.md`, `references-learning.md`, `guides.md` and `quizzes.tsv`. Module headers use `# M01 · Title`; labs use `**L01A · Title.**` followed by Environment, Tasks, Evidence, Success and Recovery. Keep the paragraph format understood by the compiler. A missing or extra translated module, lab, guide or reference fails the build; do not substitute a different language silently.

Interface strings live in `assets/i18n.js`. Command text and filenames are technical data, not strings to translate by global replacement. Every new interface key requires its ES/EN entries and a regression test. Keep generated `dist`, ZIPs and QA logs out of source commits.

## Calidad docente

Cada unidad explica una pregunta, resultado, prerrequisitos, mecanismo, ejemplo, tarea GUI/CLI cuando corresponda, evidencia esperada, prueba negativa, recuperación y límites. La versión inglesa debe mantener significado y dificultad, no limitarse a cambiar encabezados. Las comprobaciones automáticas de IDs y longitud no sustituyen revisión lingüística/técnica.

Las referencias enlazadas y las preguntas formativas son públicas. No se deben introducir soluciones reservadas, expedientes, credenciales, logs reales ni datos personales de alumnos. El plan maestro documenta ampliaciones pendientes y no debe aumentar automáticamente las 480 horas o cambiar la finalización de un alumno.

## Acceptance commands

```sh
python3 campus/build.py
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
node --test campus/tests/*.test.mjs
python3 campus/build.py
python3 campus/check_release.py
python3 campus/tests/browser_bilingual.py
```

For WebKit, install its Playwright engine and repeat with `CAMPUS_BROWSER=webkit`. Do not count an unavailable browser as passed. Review both languages, small screens, the real source commit and actual release artifact. [QA.md](QA.md) describes the scopes.
