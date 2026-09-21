# Calidad docente, de producto y de operación / Quality contract

La calidad se comprueba con criterios y evidencias; no se declara por emplear una marca de consultoría o por contar archivos. Este documento define los criterios de revisión y no afirma que todos los entornos posibles hayan sido probados.

## Matriz de aceptación

| Dimensión | Criterio comprobable |
|---|---|
| Alcance | Fundamentos comunes y recorridos Linux/Windows/macOS; dependencias y límites identificados |
| Didáctica | Una idea central por vista; concepto seguido de micropráctica; teoría separada de ejecución |
| Ejemplos | Contexto, intérprete, entrada y resultado definidos; datos ficticios |
| Prácticas | Entorno, pasos, resultado esperado, evidencia, error frecuente y recuperación |
| Comprensión | Autoevaluación explicada y marca de repaso; respuesta correcta no equivale a examen oficial |
| Operación | Usuario autorizado, privilegio mínimo, prueba positiva/negativa y recuperación |
| Comunicación | Conclusión, evidencia, límite, opciones y siguiente responsable/acción |
| UX | Índice, anterior/siguiente, teclado, lectura sin JS, idiomas y escape de presentación |
| Accesibilidad | Foco visible, etiquetas, contraste, áreas táctiles y reflujo comprobados; sin afirmar certificación universal |
| Tiempo | Inicio explícito, pausas, suspensión, inactividad y separación medido/declarado |
| Datos | Claves locales independientes, importación limitada/validada, copia anterior preservada ante error |
| Publicación | Compilar, validar, subir y activar son etapas distintas; verificar commit público y reversión |

## Rúbrica de una práctica

Comprensión/objetivo 20 %, ejecución y comprobación 30 %, seguridad y recuperación 20 %, evidencias reproducibles 20 %, comunicación 10 %. Es una propuesta docente. Ninguna nota compensa actuar fuera de alcance, divulgar secretos o declarar pruebas inexistentes; esos puntos requieren remediación.

## Medición de aprendizaje

El timer observa intervalos iniciados en el navegador, no atención ni conocimiento. Se pausa al ocultarse la página y tras cinco minutos sin interacción; un hueco mayor de 15 segundos entre ticks se excluye como posible suspensión. Esto puede infracontar una lectura lenta o trabajo externo: el alumno puede continuar o declararlo en su categoría independiente.

Los 25/5 minutos son una configuración solicitada, no un óptimo científico. Las estimaciones de pasos pendientes son supuestos visibles y no sustituyen el criterio del alumno o docente. No hay puntuación de «tiempo no estudiado», comparación pública ni alertas de rendimiento de terceros.

## Gestión editorial

Mantener IDs, versiones, referencias y comandos originales por plataforma. Revisar la edición real antes de impartir una práctica; marcar cambios de proveedor o laboratorio. El core anterior conserva sus IDs y catálogos. Las lecciones del aula OS tienen IDs propios y no reciben automáticamente las marcas del itinerario anterior.

## Evidencias de software

La suite Python valida contenido y compilación; la suite JavaScript prueba modelo y controles de tiempo; Playwright prueba navegación real por motor. Capturas corresponden al commit y entorno registrados. Un test simulado no se presenta como navegador; un viewport emulado no se presenta como iPad físico. La aceptación nativa de los ejercicios Windows/macOS es independiente de la aceptación web.

## Referencias técnicas de este diseño

- [MDN Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API): visibilidad y throttling de tareas en segundo plano.
- [MDN Fullscreen API](https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API): disponibilidad limitada, petición explícita y salida.
- [VirtualBox 7.2](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html): combinaciones host/invitado.
- [Fusion Apple Silicon](https://knowledge.broadcom.com/external/article/315602): arquitectura de invitados y límites.
- [Windows ARM64](https://www.microsoft.com/en-us/software-download/windows11arm64): medios, requisitos y verificación.

Referencias de entorno consultadas el 21-09-2026. Las demás referencias por SO son destinos primarios para cada lección; no se afirma haber ejecutado cada combinación de versión/plataforma. No se redistribuyen instaladores o licencias de terceros.

## English

Acceptance is evidence-based: scope, one-concept learning, connected micropractice, explicit environment, expected outcomes, safe recovery, reproducible evidence and concise handover. Time is recorded activity, not proof of attention. Cross-browser tests, native OS labs and production verification are separate evidence types. No consulting or university affiliation is claimed.
