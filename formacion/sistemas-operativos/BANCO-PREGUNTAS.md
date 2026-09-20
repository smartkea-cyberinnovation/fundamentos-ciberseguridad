# Preguntas de defensa y criterios de respuesta

Banco inicial para conversación técnica y evaluación aplicada. Se combina con las preguntas de cada módulo y la [rúbrica](EVALUACION.md). No sustituye las pruebas prácticas ni ofrece una respuesta única para todas las configuraciones.

| Pregunta | Criterio de respuesta competente |
|---|---|
| ¿Qué diferencia hay entre snapshot, backup y evidencia? | Explicar propósito, dominio de fallo, conservación y recuperación. |
| ¿Por qué dos textos visualmente iguales tienen distinto hash? | Considerar codificación, finales de línea y bytes; comprobar antes de concluir. |
| ¿Qué cambia al pasar de GUI a terminal? | La interfaz no elimina permisos, efectos ni necesidad de verificación. |
| ¿Por qué una tarea funciona de forma interactiva y falla programada? | Revisar identidad, directorio, entorno, dependencias y permisos. |
| ¿Cuándo elegir Bash, BAT o PowerShell? | Justificar plataforma, contrato de datos, mantenimiento y disponibilidad. |
| ¿Por qué no basta observar los permisos visibles? | Considerar identidad efectiva, herencia, ACL y controles adicionales. |
| ¿Un servicio activo está necesariamente accesible? | Separar proceso, listener, red, autenticación y funcionamiento de aplicación. |
| ¿Un backup reciente demuestra recuperación? | Exigir restauración, verificación funcional, tiempo y pérdida observados. |
| ¿Qué no verifica un hash de contenido? | No acredita por sí solo metadatos, origen, autoría o custodia completa. |
| ¿La ausencia de eventos demuestra ausencia de actividad? | Revisar configuración, permisos, retención, cobertura y fallos de ingestión. |
| ¿Qué debe conservar una normalización temporal? | Valor y zona originales, precisión, ajustes e incertidumbre. |
| ¿Una coincidencia con un indicador acredita incidente? | Exigir contexto, vigencia, semántica de búsqueda y corroboración. |
| ¿Cómo se diferencia una hipótesis de un hallazgo? | Identificar observación, inferencia y evidencia adicional necesaria. |
| ¿Qué demuestra que una corrección fue útil? | Prueba funcional y negativa, evidencia antes/después y riesgo residual. |
| ¿Por qué no basta confiar en una respuesta de IA? | Puede errar o incorporar instrucciones de datos no confiables; verificar fuera del modelo. |
| ¿Qué demuestra dominio del proyecto? | Reproducción por otra persona, explicación individual y recuperación. |

## Casos de integración

**Caso 1: solo funciona con permisos elevados.** El alumno debe revisar el contexto, identificar el acceso mínimo y verificarlo con usuario estándar. Respuesta insuficiente: mantener privilegios administrativos permanentes.

**Caso 2: copias iguales, contexto diferente.** El contenido coincide, pero cambian atributos y timestamps. Separar objetivos de integridad, preservación y disponibilidad; documentar lo no conservado.

**Caso 3: informe demasiado concluyente.** Un indicador aparece una vez en un conjunto limitado de logs. Explicar alcance, falso positivo posible y siguiente comprobación, sin atribuir un incidente no demostrado.

**Caso 4: automatización que hace más de lo solicitado.** Reducir alcance, revisar permisos, rechazar acciones innecesarias y volver a probar sobre datos sintéticos antes de aceptar cambios.

Puntuar razonamiento, comprobaciones pertinentes, seguridad y límites. Una lista de herramientas sin explicación no alcanza nivel competente.
