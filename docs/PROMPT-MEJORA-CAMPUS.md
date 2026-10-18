# Prompt de mejora del campus

Actua como responsable de producto educativo y de ingenieria del repositorio
`smartkea-cyberinnovation/fundamentos-ciberseguridad`. Entrega cambios pequenos,
probados y revisables. Primero confirma el estado actual: este documento recoge
la revision del 22 de septiembre de 2026, no una garantia sobre estados futuros.

## Objetivo y alcance

Convertir el campus en una experiencia de estudio clara y progresiva que conserve
el contenido, los identificadores y el progreso existente. La ruta publica es
`https://smartkea.com/introduccion-ciberseguridad/`; el Worker es
`fundamentos-ciberseguridad`, cuenta `d64eb5b583d2da3db04bbffffb424f94`.
Mantener la ruta exclusiva `smartkea.com/introduccion-ciberseguridad/*` y comprobar
que `/`, `/legal` y `/privacidad` conservan su comportamiento. No cambiar DNS,
correo, identidad, pagos o licencia para completar una mejora del campus.

## Estado que debes reconciliar

- El PR #3 integrado en `89c06d1` dejo un salto de linea literal en Python,
  cuatro documentos con formato EN incompleto, contratos de 36 recursos pese a
  incorporar 40 y versiones contradictorias entre interfaz y metadatos.
- La reparacion de despliegue de esta revision restaura esos contratos y declara
  D37-D40 como esquemas ES con resumen EN. D26-D36 conservan sus controles de
  contenido desarrollado en ambos idiomas. Completar ingles sigue pendiente.
- El nucleo sigue teniendo 32 modulos, 96 fichas, 8 guias ampliadas y 480 horas
  planificadas. No presentar fichas como practicas ejecutadas o acreditadas.
- El PR #5 propone README para alumnos, `docs/LEARNING-DESIGN.md`, `DEPLOY.md`,
  `SECURITY.md` y `LICENSE.md`. Revisar el contenido y resolver solapamientos con
  esta reparacion antes de integrarlo; conservar la decision de licencia actual.
- Hay trabajo en `feat/os-study-assistant-20260921` y
  `feat/os-classroom-redesign-20260921`. Comparar con main, inventariar que aporta
  cada rama y recuperar solo piezas verificadas. El ultimo CI de os-study fallo
  primero por la sintaxis heredada y despues intento navegadores sin Playwright.
- El issue #4 contiene la evolucion hacia sesiones de estudio y ayuda gradual.
  Reutilizarlo; no crear un roadmap paralelo ni declarar funciones implementadas
  solo porque aparecen en un documento.
- Main no tenia proteccion ni checks obligatorios en la revision. Proponer una
  politica concreta de PR, checks requeridos y publicacion despues de aceptacion.
  Las pruebas locales, CI, subida de version y activacion son hechos distintos.

## Prioridades

1. **Publicacion reproducible.** Compilar desde checkout limpio; validar esquema,
   contenido ES/EN, URLs, version, manifiesto y paquetes antes de publicar. Anadir
   comprobacion posterior que compare main, build-info y version activa al 100%.
   Registrar el SHA y los resultados reales. Corregir filtros de workflows para
   que toda fuente que cambie el sitio ejecute la aceptacion necesaria. Evitar
   publicar un commit por el mero hecho de que otra version responde HTTP 200.
   Mantener rollback a una version identificada y verificarlo sin ejecutarlo
   innecesariamente. No anadir un backend solo para activar observabilidad: el
   Worker actual sirve activos estaticos y el panel limita sus metricas/logs.

2. **Contenido honesto y bilingue.** Desarrollar D37-D40 en ingles con la misma
   profundidad y estructura que ES, manteniendo IDs y enlaces. Sustituir la
   etiqueta de resumen solo al verificar paridad. Convertir listas de vocabulario
   en definicion, ejemplo, distincion y fuente cuando corresponda. Mapear cada
   resultado de aprendizaje a explicacion, practica, evaluacion y evidencia.
   Decidir expresamente como conviven el itinerario sin tiempos impuestos y el
   catalogo historico de 480 horas, sin borrar progreso ni inventar horas cursadas.

3. **Experiencia de estudio.** Reconciliar primero las ramas existentes. Priorizar
   continuidad, un objetivo por vista, micropractica, recuperacion activa y ayuda
   gradual. Separar leido, practicado y comprobado. Mantener notas y progreso
   locales, exportacion/importacion y compatibilidad con copias anteriores.
   El temporizador debe distinguir pausa, tiempo activo y sesion; no convierte
   permanencia en aprendizaje. No incorporar telemetria ni cuentas obligatorias.

4. **Accesibilidad y presentacion.** Verificar teclado, orden y retorno del foco,
   Escape, botones de presentacion y lectores de pantalla en ES/EN. Revisar que
   Space active un boton enfocado sin que el atajo global lo convierta en avance
   de diapositiva. Traducir etiquetas accesibles y evitar solapamientos a 320,
   390, 768 y 1440 px, incluido texto ampliado. Medir tamano de catalogos y tiempo
   de carga antes de introducir particion de datos, cache o modo offline.

5. **Fuentes y practicas.** Inventariar enlaces con fuente primaria, fecha de
   revision, idioma y estado. Verificar afirmaciones cambiantes sobre normativa,
   instituciones, certificaciones y productos antes de ampliarlas. Practicas
   defensivas, de administracion y diagnostico con datos sinteticos; sin flujos
   ofensivos, explotacion de terceros ni ejecucion autonoma de comandos. Distinguir
   claramente VM, contenedor y equipo nativo al explicar lo que cada uno permite.

## Metodo y aceptacion

- Inspeccionar remoto, rama, cambios locales, PRs, CI y Cloudflare antes de editar.
  Usar una rama de trabajo; conservar cambios ajenos y evitar force-push.
- Orden de comprobacion: tests Python, build, check_release, tests JavaScript,
  navegadores y runtime Workers. Respetar dependencias de artefactos generados.
  No suprimir pruebas ni rebajar umbrales para convertir un fallo en exito.
- Probar Chromium y WebKit, movil y escritorio, navegacion de los 40 recursos,
  busqueda M05 exacta, cambio de idioma, progreso, exportacion/importacion y
  lectura sin JavaScript. Para redisenos, probar migracion de datos anteriores.
- Validar GET/HEAD, redireccion con query, MIME, CSP, nosniff, 404 y rechazo de
  metodos no soportados. Comprobar recursos publicos y su huella contra el build.
- Mantener el alcance del cambio pequeno; proponer PRs sucesivos con riesgos,
  criterios de aceptacion y evidencia. Esperar CI real, no solo checks creados.
- Entregar informe priorizado P1/P2/P3, cambios y archivos, enlaces a PRs,
  resultados con SHA, version publicada, pendientes y siguiente paso concreto.
  Coste: separar tokens medidos de estimaciones; no inventar tarifas ni consumo.

Empieza por reconciliar Git y la publicacion actual; despues ejecuta la primera
mejora pendiente con mayor impacto y menor riesgo. Revisa este prompt contra el
estado vivo para no reabrir problemas que ya esten resueltos.
