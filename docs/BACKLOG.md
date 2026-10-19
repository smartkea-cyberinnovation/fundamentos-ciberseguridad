# Plan de mantenimiento y siguientes tareas

Este registro público contiene decisiones técnicas. Los hilos de correo, documentos de coordinación y el enlace de la conversación se mantienen en el tracker privado autorizado. Los estados reflejan evidencia; no deben convertirse en «hecho» por disponer de un plan.

## Trabajo de esta consolidación

| ID | Estado | Resultado o criterio de aceptación |
|---|---|---|
| INT-01 | Integrado, PR10 | Ramas originales de SmartKEA reconciliadas, aula OS recuperada y contenido curricular incorporado |
| EDU-01 | Integrado, PR10 | D41–D46 y matriz de doce temas; 6 ECTS diferenciados de las 480 horas del itinerario general |
| EDU-02 | Integrado, PR10/11 | Banco de 100, intentos de 20, corrección inmediata, explicación y persistencia entre pestañas probada |
| FIX-01 | Integrado, PR11 | Reinicio/borrado/recreación del registro OS y enlaces ingleses D46 corregidos |
| INT-02 | Preparado para aceptación de la consolidación | Diferencias del personal contabilizadas, recorridos por rol portados y ramas pendientes revisadas; véase la matriz en [Migración](MIGRATION.md) |
| INT-03 | Código preparado; publicación pendiente de acceso a GitHub | Awesome DPD separado en 47 archivos con atribución, licencia conservada, lockfile, pruebas y bundle Git independiente; verificar el nuevo repositorio público antes de retirar el origen |
| DOC-01 | Preparado y validado; exportación final ligada al commit publicado | Paquete Figma Make Markdown/JSON, esquemas, inventario y banco completo contrastados con el código; generar la entrega con `docs/figma-make/exportar.py` |
| FIX-02 | Integrado, PR12 | Escáner C99 offline acotado, sin ejecutar muestras; 27 regresiones y preview de Workers correctos sobre el head revisado |
| SEC-01 | Implementado; CI pendiente de esta PR | Actions fijadas a SHA y propuestas de actualización gestionadas por Dependabot |
| SEC-02 | Configurado; primera ejecución pendiente | CodeQL Python/JavaScript/Actions; revisar SARIF y documentar cualquier hallazgo |
| REL-01 | Pendiente del commit final | Workers Build correcto y SHA, banco, rutas, idiomas y cabeceras observados en producción |
| INT-04 | Depende de INT-02/03 y REL-01 | Aviso visible en el origen y archivo/deprecación conservando recuperación e historial |

La PR de consolidación y el tracker registran los cierres posteriores a este documento. Los checks y el `build-info.json` del commit concreto son la evidencia de ejecución y despliegue.

## Pendientes que requieren continuidad

| ID | Prioridad | Responsable por función | Tarea | Dependencia y evidencia de cierre |
|---|---|---|---|---|
| [GOV-01](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/13) | P1 antes de datos identificados | Responsable docente + DPD | Completar responsable, finalidades, base jurídica, información, retención, derechos y proveedores | Matriz [privacidad e IA](security/PRIVACY-AND-AI.md) aprobada y configuración contrastada |
| [SEC-03](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/14) | P1 | Mantenedor GitHub | Verificar protección de main, revisión/checks exigidos, force-push, permisos y detección de secretos | Captura o lectura de configuración efectiva y PR de comprobación; evitar exigir checks omitidos por filtros |
| [SEC-04](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/15) | P2 | Responsable de seguridad | Asociar entorno del campus en Codex Security y ejecutar análisis solicitado | Entorno con el repo correcto, run ID, estado final y hallazgos triados; no reutilizar un entorno ajeno |
| [SEC-05](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/16) | P2 | Responsable de laboratorios | Fijar imágenes por digest para cada edición y revisar componentes | Inventario, digest aprobado, pruebas de laboratorio y actualización documentada |
| [SEC-06](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/16) | P2 | Mantenedor del kit OS | Limitar concurrencia del servidor HTTP local antes de un uso compartido | Prueba de saturación acotada y regresiones HTTP, sin abrir puertos públicos |
| [EDU-03](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/17) | P2 | Editor ES/EN | Completar traducción docente de D37–D40 | Ediciones paralelas revisadas, mismos IDs y enlaces, sin presentar resúmenes como traducciones completas |
| [EDU-04](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/17) | P2 | Docente por plataforma | Ejecutar prácticas nativas en Windows, macOS y Linux de la edición elegida | SO/versión/arquitectura, resultado, evidencia y recuperación; no basta viewport emulado |
| [EDU-05](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/17) | P2 | Coordinación docente | Confirmar guía de asignatura, propuesta de evaluación y actualización de fuentes | Aprobación institucional y fecha, separadas del test formativo |
| [UX-01](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/4) | P2 | Diseño + accesibilidad | Revisar lectura con lector de pantalla y dispositivos reales | Recorridos concretos, problemas y correcciones; las pruebas automatizadas son complementarias |
| [MAINT-01](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/4) | P2 | Mantenedor frontend | Dividir y dar formato a las vistas históricas más compactas por componente | PR pequeñas con mismo contrato de rutas, progreso y navegador; sin reescribir el producto a la vez |
| AI-01 | P1 solo si se propone IA externa | Producto + seguridad + DPD | Definir proveedor, minimización, autorización, límites, evaluación y control humano | Matriz de IA aprobada, amenazas y pruebas negativas; no activar servicios por defecto |
| DPD-01 | P2 | Responsable del catálogo DPD | Localizar la entrega ampliada mencionada en el handoff histórico si se desea incorporarla | Archivo o commit real verificado; no reconstruir como si existieran 119 archivos/180 preguntas no hallados en Git |
| OPS-01 | P2 | Coordinación del proyecto | Mantener tracker con URL, estado, dependencia, responsable y evidencia | Filas sin duplicados, referencias accesibles y actualización después de cada release |

## Definición de cierre

Cada tarea debe enlazar una modificación o decisión, su criterio comprobado y un resultado. Los responsables por función son propuestas de asignación, no personas que hayan aceptado trabajo. Establecer fechas con la coordinación; no inventar vencimientos ni firmas. Un bloqueo conserva el siguiente paso y el responsable de resolver la dependencia.

Antes de iniciar una nueva fase, leer [revisión y publicación](engineering/REVIEW-AND-RELEASE.md) y [el informe técnico](security/REVIEW-2026-10-18.md).
