# Seguimiento público y criterios de cierre

Caso C99-20261018 · revisión R2: 2026-10-18. Fuente de tareas técnicas: [issue #8](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/8).

El [PR #9](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/9) se fusionó el 18/10/2026 a las 17:16:18 UTC, merge `f90b087fb1c4f64024f71c667ffe6d72420a70d5`. El material se confirmó en main `2f093d5f09ad9beaa32c799378ea41a7eb562008`. La revisión posterior detectó dos fallos del lexer y esta rama incorpora la corrección y 26 tests. Véase [CORRECCIONES_R2.md](CORRECCIONES_R2.md).

| ID | Acción | Estado R2 | Criterio de cierre |
|---|---|---|---|
| C99-T01 | Preservar dossier y verificar integridad | Hecha | Hash del ZIP y 42 hashes del manifiesto coincidentes; no certifica inocuidad |
| C99-T02 | Repetir pruebas offline y documentar fechas | Hecha | 10 tests originales y 26 con regresiones R2; fecha declarada separada de revisión |
| C99-T03 | Validar reglas y telemetría | Pendiente | Motores/versiones, positivos, negativos y falsos positivos documentados |
| C99-T04 | Actualizar inteligencia pasiva | Pendiente | Fuentes y timestamps UTC; incertidumbres y CDN separados |
| C99-T05 | Determinar alcance de posible ejecución propia | Bloqueada | Confirmar si hubo ejecución; evidencias sólo en expediente privado |
| C99-T07 | Corregir lexer y completar integración docente | En curso | Corrección revisada/fusionada y navegación del curso verificada; la fusión de #9 no basta |
| C99-T08 | Revisar disponibilidad y distribución documental | En curso | Entregable documental separado y legible; bloqueo del paquete de análisis tratado por la vía autorizada, sin eludir filtros |

C99-T06 se reserva al enlace privado de la conversación y continúa bloqueada. La ficha de recuperación no sustituye al permalink real. Los responsables operativos y referencias privadas permanecen en el tracker maestro con el mismo ID; no se duplican aquí.

Sin fecha límite acordada. No cerrar la investigación como incidente resuelto: no se ha demostrado un incidente real. No desplegar la webshell ni validar el callback mediante contacto activo. Existe un build de vista previa declarado por Cloudflare en #9; no se confunde con publicación navegable del caso ni con revisión de seguridad.
