# R05 · Cronología y búsqueda exacta sobre evidencia sintética

**L27B · 3 h.** Refuerza M28–M29 sin duplicar carga. Entorno: kit Python y ocho eventos creados para el curso; no son exportaciones originales EVTX/journal/Unified Log. [Lección 06](../lecciones/06-evidencias.md).

## Pasos y resultados

1. Calcula el hash de `eventos.json` con la utilidad nativa del SO. Registra fuente y zona. Trabaja con el dataset ficticio, nunca con logs empresariales.
2. Ejecuta `python3 kit/oslab.py timeline mi-laboratorio`. Debe ordenar E01–E08. E01 conserva `2026-09-14T10:00:00+02:00` y normaliza a `2026-09-14T08:00:00+00:00`.
3. Localiza `source_index` y el objeto `original`. Explica por qué conservarlos ayuda a reproducir la transformación.
4. Ejecuta `python3 kit/oslab.py match mi-laboratorio`. Debe producir cuatro coincidencias: E02/domain, E02/ip, E04/sha256 y E08/domain.
5. Comprueba que E03 —parecidos— y E07 —subdominio— no aparecen. El contrato usa identidad exacta, no coincidencia por fragmentos ni inclusión automática de subdominios.
6. Confirma que el hash de `eventos.json` sigue igual. Esa comparación verifica el contenido observado, no sustituye la custodia de un caso real.

## Variante

Copia el workspace a otro directorio nuevo. Quita la zona de un timestamp o repite un ID de evento en la copia. La herramienta debe rechazar la entrada; no inventar UTC ni eliminar el duplicado silenciosamente. Registra el fallo y restaura solo la copia.

## Interpretación esperada

No hay cuatro incidentes: hay cuatro coincidencias en tres eventos. El SHA-256 de E04 pertenece al archivo inocuo `hola.txt`. Los indicadores son didácticos; no se conectará a sus dominios o IP. Redacta una hipótesis, una alternativa benigna y una comprobación adicional. No atribuyas actor ni compromiso.

## Éxito y recuperación

Entrega manifiesto del caso, timeline, matcher, controles negativos y nota de cobertura. Éxito: diferenciar dato, normalización y conclusión. Conservar el original; borrar la copia únicamente cuando termine la evaluación. La práctica no acredita adquisición física, memoria, análisis EVTX ni una pericial completa.
