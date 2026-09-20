# R08 · IA: estructura válida no significa conclusión verdadera

**L31B · 4 h.** Entrada: M31 y R05. Puede completarse sin proveedor, suscripción o modelo: se utiliza `respuesta-ia.json` como salida simulada. [Lección 07](../lecciones/07-ia.md).

## Preparación

Identifica los ocho eventos y sus resultados de búsqueda. Lee E06 como dato no confiable. Trabaja sobre una copia del workspace si vas a editar. No entregues credenciales ni actives herramientas de ejecución para la IA.

## Recorrido

1. Lee la respuesta de ejemplo y ejecuta `python3 kit/oslab.py review mi-laboratorio`. Se espera `structurally_valid: true`, `semantically_verified: false` y `requires_human_review: true`.
2. En una copia, añade un campo superior `actions`. Repite la validación: debe fallar. El kit no ejecuta su contenido.
3. Restaura la respuesta de ejemplo y sustituye la referencia por `E999`. Debe fallar por referencia inexistente.
4. Vuelve al esquema válido y escribe una conclusión que cite E02, pero diga que demuestra por sí solo un compromiso. La estructura puede pasar; el alumno debe rechazar la conclusión por falta de sustento.
5. Propón una respuesta corregida con hecho observado, hipótesis, alternativa y siguiente comprobación. Comprueba cada referencia manualmente.

## Ampliación con CLI aprobada

El docente puede usar una CLI local o remota aprobada para obtener otra respuesta sobre los datos ficticios. Registra modelo, versión/configuración, destino, datos usados y comprobaciones. No descargar un modelo sin revisar recursos/licencia ni exponer logs reales. El flujo debe seguir sin capacidad de ejecutar órdenes. El kit no hace llamadas a modelos ni valida permisos del proveedor.

## Evaluación

Entrega tabla de tres errores: campo no admitido, referencia desconocida e inferencia no sustentada. Explica cuál detecta el programa y cuál exige criterio humano. No se aprueba por obtener JSON válido. Se mide si el alumno evita que una instrucción incrustada en datos cambie la finalidad del análisis.

## Cierre

Conserva solo respuestas sintéticas permitidas; retira accesos temporales de la herramienta opcional. No se han ejecutado modelos durante la validación del kit. Este guion no acredita resistencia general a prompt injection: demuestra controles y sus límites en un caso acotado.
