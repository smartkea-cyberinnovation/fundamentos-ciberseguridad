# Evaluación, recuperación y acreditación interna

## Modelo general

Diagnóstico inicial no calificable. Evaluación continua: laboratorios 40 %, pruebas prácticas individuales 20 %, teoría aplicada 10 %, proyecto final 25 % y cuaderno/revisión profesional 5 %. Suma 100 %. Se aplica además un umbral propio al capstone y requisitos críticos: una media alta no compensa una práctica insegura sin corregir.

La evaluación del bloque puede basarse en una muestra anunciada de evidencias A/B/C, pero todos los laboratorios definidos para la ruta deben completarse o recibir adaptación documentada. Evitar puntuar dos veces el mismo artefacto: laboratorio evalúa proceso; cuaderno evalúa calidad documental longitudinal; proyecto evalúa integración.

## Rúbrica común de laboratorio

| Dimensión | Peso | Nivel competente |
|---|---:|---|
| Comprensión y planificación | 15 % | Objetivo, alcance, sistema y permisos identificados |
| Ejecución técnica | 30 % | Resultado correcto y verificable |
| Seguridad y privacidad | 20 % | Mínimo privilegio, datos sintéticos y límites respetados |
| Evidencia y reproducibilidad | 20 % | Versiones, pasos, resultados y errores trazables |
| Recuperación y reflexión | 15 % | Rollback/restauración y límites explicados |

Escala por dimensión: 0 ausente/no ejecutado; 1 incompleto y requiere ayuda sustancial; 2 correcto con guía; 3 autónomo, verificable y seguro; 4 además prueba casos límite, justifica alternativas y reconoce incertidumbre. La puntuación final es la suma de `peso × nivel/4`.

## Checkpoints y pruebas individuales

**C1, tras M04.** Obtener ayuda, navegar y registrar un cambio en Git sin datos sensibles. Prueba sobre un directorio diferente al utilizado en clase.

**C2, tras M12.** Explicar servicio/usuario/puerto en Linux; corregir un fallo benigno aprobado; defender un script ante ruta con espacios, ausencia de permisos y entrada inválida.

**C3, tras M19.** Resolver una tarea Windows con CLI; diferenciar objetos/texto; verificar ACL y consultar evento con proveedor, intervalo y política conocida.

**C4, tras M23.** Localizar configuración y servicio en macOS; distinguir zsh/Bash; comprobar un control de seguridad y explicar una limitación de log. Requiere ejecución nativa para acreditación de administración.

**C5, tras M30.** Preservar un dataset, construir timeline, detectar coincidencia exacta de un indicador y justificar una hipótesis alternativa. Diseñar una corrección y retest.

**C6, tras M32.** Defensa integrada, cambio pequeño no anunciado y restauración demostrada. Ver rúbrica detallada en [capstone](CAPSTONE.md).

Las pruebas se realizan con ayuda y manuales disponibles. No se permite delegar toda la solución a un compañero o IA. El docente verifica comprensión mediante preguntas y pequeñas variaciones del problema.

## Condiciones de superación

Ruta completa: media al menos 70/100, checkpoints superados, capstone al menos 70/100 y sin requisitos críticos pendientes. Las rúbricas y umbrales son propuestas internas de esta edición, no normativa académica externa.

Incumplimientos críticos: actuar fuera del alcance, exponer el laboratorio, introducir secretos/datos reales en Git, destruir originales, desactivar controles esenciales sin formar parte de un procedimiento legítimo autorizado, ejecutar salida no revisada de IA o atribuir pruebas no realizadas. Se detiene y remedia la práctica; el alumno repite la competencia afectada.

## Recuperación

Identificar el resultado no demostrado; proporcionar un ejercicio alternativo equivalente con distinto dataset; exigir análisis del fallo y una nueva comprobación; registrar fecha, evidencia y evaluación. No basta corregir una captura. Un alumno con dificultades en shell puede demostrar comprensión mediante pasos guiados y progresar hacia autonomía; no se rebaja la seguridad.

## Trabajo en equipo

Roles rotatorios: operador, observador de seguridad y documentador. La aportación se acredita por cambios, revisiones y defensa, no por número de líneas de código ni commits. Cada integrante explica un componente ajeno a su responsabilidad principal.

## Uso de IA

Permitido para estudiar y proponer, con declaración de herramienta, datos usados, salida aprovechada y validación. El docente puede pedir la misma explicación sin IA. No se puntúa el estilo convincente de un informe si sus hechos no están sustentados.

## Acreditación interna propuesta

Denominación: «Aprovechamiento en administración de sistemas operativos y fundamentos operativos de ciberseguridad». Registrar titular, edición/ruta, horas efectivamente cursadas, sistemas evaluados de forma nativa, competencias demostradas, fecha, responsable y referencia verificable al expediente. No emitir automáticamente un certificado por existir el repositorio.

Para rutas abreviadas o ausencia de sistema nativo, el texto debe indicar exactamente ese alcance. No afirmar equivalencia con certificaciones oficiales, formación reglada o experiencia profesional.
