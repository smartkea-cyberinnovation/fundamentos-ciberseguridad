# Competencias, evidencias y perfiles

Matriz pedagógica inspirada en la separación tarea/conocimiento/habilidad de NICE [S10](FUENTES.md). No es una equivalencia oficial ni una acreditación de puestos. Red/Purple se entiende aquí como evaluación autorizada de controles y revisión técnica, no formación de explotación.

Escala: **1** comprender/interpretar; **2** ejecutar con guía; **3** ejecutar, validar y explicar con autonomía en el laboratorio. La matriz expresa objetivos de utilización por perfil, no calificaciones obtenidas por alumnos.

| Competencia | SysAdmin | Blue/SOC | DFIR | Red/Purple | CTI | Módulos/evidencia |
|---|---:|---:|---:|---:|---:|---|
| Arquitectura y recursos de SO | 3 | 2 | 3 | 3 | 1 | M01–M03, mapa y diagnóstico |
| Terminal y documentación | 3 | 3 | 3 | 3 | 3 | M04, cuaderno reproducible |
| Archivos, metadatos y hashes | 3 | 3 | 3 | 3 | 2 | M05/M09/M14/M20, manifiesto |
| Texto, búsquedas y datos | 3 | 3 | 3 | 3 | 3 | M06/M16/M29, consultas probadas |
| Linux: identidades y permisos | 3 | 3 | 3 | 3 | 1 | M07, matriz y pruebas negativas |
| Linux: procesos y servicios | 3 | 3 | 3 | 3 | 1 | M08, ficha de servicio |
| Almacenamiento y recuperación | 3 | 2 | 3 | 2 | 1 | M09/M19/M23, restauración |
| Redes del host | 3 | 3 | 2 | 3 | 2 | M10/M18/M22, diagnóstico |
| Bash seguro | 3 | 3 | 2 | 3 | 3 | M11–M12, script y pruebas |
| CMD/BAT heredado | 2 | 2 | 2 | 2 | 1 | M14–M15, mantenimiento/migración |
| PowerShell y objetos | 3 | 3 | 3 | 3 | 3 | M16–M17, salida estructurada |
| Windows nativo y directorio | 3 | 3 | 3 | 3 | 1 | M13/M17–M19, políticas y eventos |
| macOS y zsh | 3 | 2 | 3 | 2 | 1 | M20–M23, checklist nativo |
| Acceso remoto y transferencia | 3 | 3 | 2 | 3 | 1 | M24, confianza y manifiestos |
| Segmentación y confianza | 3 | 3 | 2 | 3 | 2 | M24/M30, matriz de flujos |
| Servicio web y TLS | 3 | 3 | 2 | 3 | 2 | M25, servicio y validación |
| Automatización multiplataforma | 3 | 3 | 2 | 2 | 3 | M26, contrato e idempotencia |
| Contenedores/orquestación básica | 2 | 2 | 1 | 2 | 1 | M26, comparación documentada |
| Baseline y excepciones | 3 | 3 | 2 | 3 | 1 | Bloques SO/M30, cambios verificados |
| Correlación temporal | 2 | 3 | 3 | 3 | 3 | M27, timeline y cobertura |
| Preservación y triage | 2 | 3 | 3 | 2 | 2 | M28, acta y límites |
| Indicadores y threat hunting | 2 | 3 | 3 | 3 | 3 | M29, positivos/negativos |
| Validación de controles | 3 | 3 | 2 | 3 | 2 | M30, prueba y retest |
| IA supervisada | 3 | 3 | 3 | 3 | 3 | M31, validación independiente |
| Comunicación y límites | 3 | 3 | 3 | 3 | 3 | M32, informe y defensa |

## Resultados transversales medibles

**RA1 — Comprender.** Explicar una observación del SO mediante procesos, permisos, filesystem o red. Evidencia: diagrama y diagnóstico con una hipótesis alternativa.

**RA2 — Operar.** Cumplir una tarea GUI/CLI con identidad, destino y efectos definidos. Evidencia: runbook que otra persona reproduce.

**RA3 — Automatizar.** Implementar contrato de entrada/salida y errores; probar casos válidos/invalidos. Evidencia: código, tests y revisión.

**RA4 — Proteger.** Proponer baseline proporcional, ejecutar cambio mínimo y verificar funcionalidad. Evidencia: antes/después, prueba negativa y rollback.

**RA5 — Investigar.** Preservar, buscar, correlacionar y concluir sin sobrepasar lo observado. Evidencia: manifiesto, timeline y límites.

**RA6 — Decidir y comunicar.** Traducir un hallazgo en impacto, prioridad y siguiente acción; explicar la IA utilizada. Evidencia: informe y defensa individual.

## Portfolio por perfil

SysAdmin presenta inventario, servicio y restauración; Blue/SOC muestra consulta y detección con cobertura; DFIR aporta caso preservado y timeline; Red/Purple aporta alcance, revisión de confianza, prueba benigna y retest; CTI presenta indicadores normalizados, confianza, vigencia y recomendación. Todos utilizan datos ficticios y documentación revisada antes de cualquier publicación futura.

No se atribuye dominio avanzado de una especialidad completa por superar únicamente este curso de base operativa. La progresión posterior debe profundizar en sus métodos, herramientas y marcos específicos.
