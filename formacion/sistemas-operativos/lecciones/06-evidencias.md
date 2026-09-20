# 06 · Evidencias, cronologías e indicadores: de los datos a la decisión

## Integridad y procedencia

Un hash permite comparar contenido, pero necesita un punto de referencia confiable. Una cadena de custodia documenta origen, recepción, transferencias y tratamiento. Ni el hash ni una plantilla aislada acreditan por sí solos autoría, legalidad o admisibilidad. La investigación se integra con decisiones de respuesta, contención y recuperación, no es únicamente una colección de comandos. [S11](../FUENTES.md)

El kit utiliza exclusivamente fixtures. El manifiesto no recorre discos del sistema, no adquiere memoria y no exporta credenciales. Su propósito es enseñar método y comprobación sin recoger información real. Tampoco ofrece garantías contra cambios concurrentes adversarios.

## Tiempo con incertidumbre

Los eventos E01 y E02 ilustran horas locales y UTC. Normaliza para correlacionar, pero conserva `timestamp_original`, zona y `source_index`. Un reloj desfasado no se arregla inventando una precisión que la fuente no tiene. El kit rechaza timestamps sin zona: el operador debe resolver esa ambigüedad en la fuente, no asumir que son UTC.

Deduplicar requiere definir identidad. Dos registros con la misma hora no son necesariamente duplicados. El ejemplo rechaza IDs repetidos para que el error no desaparezca silenciosamente; un flujo profesional podría conservar versiones y procedencia según su contrato.

## Coincidencia exacta frente a parecido

El dataset incluye un dominio normalizado, un nombre parecido, un subdominio y dos IP parecidas. La búsqueda devuelve cuatro coincidencias: E02 contiene dominio e IP, E04 coincide con el SHA-256 de un archivo inocuo y E08 con el dominio. Son tres eventos coincidentes, no cuatro incidentes. E03 y E07 son controles negativos para la semántica exacta elegida.

La normalización distingue tipo y valor. No se interpreta una URL como un dominio sin parsing explícito. El kit restringe dominios a ASCII; no afirma resolver equivalencias IDNA ni todos los casos de inteligencia. Tampoco conecta con esos valores. Para ampliar el esquema, primero define casos positivos, negativos y límites.

## Contexto, comportamiento y confianza

Un indicador es una pista dependiente de contexto y tiempo. Una coincidencia puede deberse a un archivo legítimo o a una consulta defensiva. Un nombre de proceso conocido tampoco acredita legitimidad. Conecta la observación con una hipótesis, busca corroboración y documenta cobertura y confianza.

ATT&CK ayuda a describir comportamientos, pero no convierte una cadena de texto en una técnica demostrada ni identifica automáticamente un actor. Solo añade un mapeo cuando exista evidencia suficiente y el identificador se haya comprobado. [S12]

## Informe mínimo defendible

Escribe: pregunta; alcance; fuente; método; observación; hipótesis principal; alternativa; limitaciones; siguiente comprobación. En el caso de E04, debe aparecer que el archivo coincide con un indicador deliberadamente sintético y es inocuo: el ejercicio demuestra el peligro de interpretar una coincidencia sin contexto.

Un SOC puede necesitar priorizar; un investigador puede necesitar preservar antes de cambiar; un administrador puede necesitar recuperar disponibilidad. Explica el equilibrio y quién aprueba cada decisión. Continúa en [R05](../practicas/R05-evidencias.md) y [R07](../practicas/R07-cambios.md).
