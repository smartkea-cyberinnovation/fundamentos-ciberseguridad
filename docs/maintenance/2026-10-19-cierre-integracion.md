# Revisión de cierre de la integración · 19 de octubre de 2026

Esta revisión continúa el [inventario de migración](2026-10-19-migracion-repositorios.md) sin cambiar su corte histórico. [PR #21](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/21) se integró en `main` mediante [`f81f1c700a61140c25a848cba48e2aa38d7f19bd`](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/commit/f81f1c700a61140c25a848cba48e2aa38d7f19bd). La aceptación posterior detectó una pérdida real de marcas de rutas en WebKit. Este cambio corrige esa carrera e incorpora las cuatro actualizaciones de Actions propuestas después de la consolidación.

El merge, el éxito de sus pruebas y la publicación del SHA final se registran por separado. El historial de CI conserva también los fallos que motivan esta corrección; una ejecución verde anterior no los elimina.

## Ramas observadas

La API de GitHub devolvió **19 ramas** en el corte posterior a PR #21 del 19 de octubre. Quince heads, incluido `main`, son ancestros de la base `f81f1c7`; los otros cuatro pertenecen a las actualizaciones de Actions. Los 19 heads son ancestros de la combinación local revisada. La rama creada para publicar este cierre queda fuera de ese corte previo.

| Rama | Head observado | Decisión en este corte |
|---|---|---|
| `codex/repair-campus-deployment-20260922` | `ac3e6a92d93d941ad0a556dba9f858f14bbd2fe8` | Integrada en main f81f1c7 |
| `codex/stabilize-webkit-header-20260922` | `212f0909c4b09c1184e28c536062582b7b5c0977` | Integrada en main f81f1c7 |
| `curriculum-v3-introduccion-informatica-ciberseguridad` | `85d3d9492828e285087a4d243a067bc841dd3671` | Integrada en main f81f1c7 |
| `dependabot/github_actions/actions/checkout-7.0.1` | `1b9b2d3267c7743e68a5614a69fdbcc03f92bcae` | Integrada en esta revisión; pendiente del merge y sus gates |
| `dependabot/github_actions/actions/setup-node-7.1.0` | `0fe29fb4d7accd34d1fec242298ad5beb1e3ac06` | Integrada en esta revisión; pendiente del merge y sus gates |
| `dependabot/github_actions/actions/setup-python-7.0.0` | `0d99821d116671008899e22af9ec4ff898eae4b0` | Integrada en esta revisión; pendiente del merge y sus gates |
| `dependabot/github_actions/actions/upload-artifact-7.0.2` | `6e16968267cbf186113b65cb8f5ac6d28cfefde7` | Integrada en esta revisión; pendiente del merge y sus gates |
| `diagnostic/term-http-contract-20261019` | `0d89337070f624b10798cf29b83ecd1883e7bdee` | Integrada en main f81f1c7 |
| `feat/c99-forensic-case-20261019` | `ec5b1bfe62bf298126f46e9668ebd8d6290e52a5` | Integrada en main f81f1c7 |
| `feat/nebrija-integration-exam-20261018` | `e91c99ca40bee4a3e73846091da7d1f050727c05` | Integrada en main f81f1c7 |
| `feat/os-classroom-redesign-20260921` | `532e29f827bb818110323529b8f1a4682c079519` | Integrada en main f81f1c7 |
| `feat/os-study-assistant-20260921` | `2bf0af1647a3ea1ac7482bf1b8f0977a2ef016d0` | Integrada en main f81f1c7 |
| `feat/term-exact-public-assets-20261019` | `eebdaed07fbdfce64994d27238fb786352020ef1` | Integrada en main f81f1c7 |
| `feat/term-linux-course` | `d593b8a1e5639ef876007944e512f9ac697f0559` | Integrada en main f81f1c7 |
| `feat/term-reliability-20261019` | `5d14f0aa4bd214bdffe1132365bba3813f40160c` | Integrada en main f81f1c7 |
| `feat/unify-repositories-20261019` | `80339ad50e2ae6360e3718536d1c6323c5bdd953` | Integrada en main f81f1c7 |
| `fix/c99-lexer-r2-20261018` | `2bdb3a596e95a37c4cc1725b30027e1380705c3f` | Integrada en main f81f1c7 |
| `fix/nebrija-review-followup-20261018` | `205e49320605cddf7462962f70bafa2d793260bf` | Integrada en main f81f1c7 |
| `main` | `f81f1c700a61140c25a848cba48e2aa38d7f19bd` | Integrada en main f81f1c7 |

Las ramas originales se conservan. No hay force-push ni sustitución de commits compartidos. Tras integrar este cierre, comprobar de nuevo las refs remotas y sus ancestros; si aparece otra propuesta, registrarla con su SHA y estado propios.

## Corrección de marcas entre pestañas

La ejecución de Campus sobre `f81f1c7` falló en `test_11_simultaneous_pending_writes_merge_after_the_exclusive_lock`: esperaba cuatro marcas compatibles y solo persistían tres. La evidencia original está en [Actions, run 39289739195, job 118186957192](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/39289739195/job/118186957192).

La reproducción local con WebKit 26.0 registró la lectura y escritura reales de dos pestañas: B guardaba las etapas 1–4; A obtenía después el lock, pero su lectura de almacenamiento todavía devolvía 1–3. Al añadir su siguiente marca, A reemplazaba la copia y perdía la etapa 4. La notificación de almacenamiento de B llegaba después a A. El lock impedía solapar las operaciones de JavaScript; esa observación demostró que, por sí solo, no bastaba para actualizar la copia de almacenamiento del otro proceso a tiempo.

`campus/assets/routes.js` cede ahora una tarea dentro del lock **antes de leer**, tanto al guardar como al borrar. Conserva el cambio de tarea existente **después de escribir o borrar**. La sesión y el consentimiento se revalidan después de ceder antes de aplicar una escritura pendiente. El borrado sigue comparando la vida del registro que conocía.

Se conserva `smartkea.learning-paths.v1`, `schema: 1`, los datos anteriores sin `recordId`, el borrador local, la última intención por etapa y el fallback avisado sin Web Locks. No se solicita información del alumno ni se reinicia su progreso. El prompt Markdown y el contrato JSON de Figma Make incluyen la coordinación actual para que una mejora visual no la retire.

La regresión nueva alterna las **26 etapas reales** entre dos pestañas, pone las escrituras en cola detrás de un lock, libera la cola y comprueba la persistencia completa desde ambas pestañas y un tercer documento. La segunda ejecución de esa ráfaga reprodujo la pérdida antes del cambio; **20/20 ejecuciones con la corrección** conservaron todas las marcas. La suite completa pasó **25/25 en Chromium, 25/25 en Firefox y 25/25 en WebKit**. Incluye cancelaciones, borrados, recreaciones y fallos de almacenamiento. Un primer proceso Firefox sin resumen final no se contabiliza; el resultado acreditado corresponde a la ejecución posterior completa.

Estas pruebas locales verifican los dos archivos de la corrección. La unión con Actions requiere además su propia CI y publicación.

## Actions: cuatro propuestas conciliadas

| PR | Acción | Versión revisada | Commit oficial fijado |
|---|---|---|---|
| [#22](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/22) | `actions/setup-python` | 7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| [#23](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/23) | `actions/upload-artifact` | 7.0.2 | `cf430e030ddbb5b0abf93d22962f4752f3646cd9` |
| [#24](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/24) | `actions/setup-node` | 7.1.0 | `949feb2413d6458794dcd2491c4babbbce0c15c1` |
| [#25](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/25) | `actions/checkout` | 7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |

Se contrastaron las etiquetas oficiales, los `action.yml` de partida y destino y las entradas utilizadas por el proyecto. La unión modifica **49 referencias en 11 workflows**. El runtime interno de estas acciones pasa a Node 24; los jobs del proyecto conservan Node 22 y Python 3.13. `checkout` mantiene `persist-credentials: false`, y los permisos de cada job permanecen acotados.

No se utiliza la entrada `always-auth` retirada de setup-node. La caché automática nueva no se activa con la estructura actual. upload-artifact conserva el empaquetado ZIP con su valor predeterminado `archive: true`; los nombres, retención y filtros actuales se mantienen. El análisis combinado debe descargar y examinar sus SARIF reales para comprobar también el contrato de los artefactos.

Las cuatro PR superaron individualmente los workflows que les aplicaban y Workers preview. El workflow manual de diagnóstico HTTP de TERM no se ejecutó por abrir esas PR. La aceptación de la unión depende de sus propias pruebas, CodeQL y preview, seguida de main y de la comprobación pública del commit desplegado.

## Respaldo personal y separación de DPD

El respaldo completo del origen personal se verificó mediante bundle, clonación limpia y `git fsck`: **13 ramas, 0 tags, 86 commits, 403 blobs y 263 árboles**. El bundle completo del repositorio personal tiene SHA-256 `2af0391c236386ee12da6f2ec8ced76d01e04bbe268a6e0179d378af7a701c40` y no exige un repositorio alternativo ni prerrequisitos. Esto completa el respaldo que estaba pendiente en el corte anterior; no significa que el origen esté archivado.

La entrega de Awesome DPD sigue separada: 47 archivos y dos commits propios, head preparado `20eef967105f7ea436740f6d013785e6eb3e7f81`, con la licencia y atribución originales. Su nuevo repositorio público aún necesita una sesión de GitHub que permita crearlo. Se mantienen los enlaces a la edición original hasta verificar el destino y migrarlos mediante PR. El archivo del repositorio personal depende de esa verificación, además de la consolidación del campus y del respaldo ya comprobado.

## Cierre operativo

1. Revisar el diff y las regresiones de rutas en Chromium, Firefox y WebKit.
2. Revisar la CI de la unión, sus tres SARIF reales y el Worker preview del head exacto.
3. Fusionar con condición de SHA; verificar que los cuatro heads de Dependabot son ancestros del nuevo main y que sus PR reflejan la integración.
4. Confirmar Workers Builds de main, `sourceCommit`, `sourceDirty: false`, los hashes de catálogos y banco y el curso TERM publicado.
5. Completar la aceptación HTTP y la navegación del examen sobre ese mismo SHA. Registrar por separado los errores de disponibilidad de enlaces externos.
6. Regenerar los catorce archivos para Make y sus hashes desde el checkout limpio final; actualizar tareas y evidencia de entrega.

Los procedimientos estables están en [revisión y publicación](../engineering/REVIEW-AND-RELEASE.md), [despliegue](../../DEPLOY.md) y [backlog](../BACKLOG.md). Este informe solo contiene información pública del proyecto; las referencias de correo, Drive y coordinación se conservan en el tracker privado.
