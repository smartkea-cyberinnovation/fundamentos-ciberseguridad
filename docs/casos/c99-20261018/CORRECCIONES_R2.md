# C99 · Revisión R2 y regresiones del analizador

Revisión: 2026-10-18. Base inspeccionada: `2f093d5f09ad9beaa32c799378ea41a7eb562008`. El PR #9 fue fusionado a las 17:16:18 UTC; esta corrección es un cambio posterior y requiere su propia revisión.

## Dos hallazgos reproducidos

La revisión de Copilot del PR #9 señaló dos problemas P2 después de la fusión. Un resumen anterior de otro revisor sin hallazgos no los invalida.

1. [Terminadores y límites PHP](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/9#discussion_r4307949163): el lexer anterior buscaba sólo LF para finalizar comentarios de línea. Omitía un literal posterior a CR o al cierre y reapertura del bloque PHP. Además confundía texto HTML externo con literales PHP.
2. [Cadenas truncadas](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/9#discussion_r4307949194): una comilla de apertura al final de una evidencia podía producir un token inválido y abortar la generación del JSON. Una comilla final escapada podía tomarse por cierre real.

## Cambios

Se mantiene un estado explícito dentro/fuera de PHP, se reconocen CR/LF y cierre de bloque en comentarios de línea y se ignora HTML externo. Una bandera confirma el consumo de una comilla de cierre real. La entrada truncada genera una advertencia sin perder hashes ni hallazgos previos. Los backticks no se ejecutan ni se decodifican. Heredoc/nowdoc detiene explícitamente el escaneo reducido conservando resultados previos.

No se evalúan expresiones ni se amplían las funciones de la webshell. No se hace tráfico de red. El analizador sigue siendo una ayuda de triage, no un parser completo ni un veredicto de ausencia de malware. Las etiquetas PHP cortas dependientes de configuración y la interpolación compleja siguen fuera de alcance.

## Verificación reproducible

Desde `docs/casos/c99-20261018`:

```bash
python3 -m unittest discover -s pruebas -v
```

Resultado local R2: 26 tests superados, incluidos los 10 originales y 16 nuevos métodos de regresión con subcasos. Se prueban comentarios CR/LF/CRLF, ambos estilos de comentario, límites entre PHP/HTML, cadena truncada, comilla escapada, backticks, heredoc y salida CLI conservando el informe. No se ha ejecutado PHP ni la muestra original.

Los motores YARA/Suricata y la conversión Sigma a un backend real no se han validado por estas pruebas. Tampoco se acredita una ejecución de la webshell en un servidor propio.

## Despliegue: precisar el alcance

En el PR #9 existe un comentario del bot de Cloudflare que declara una vista previa construida para `ca61ed5`. Esa declaración acredita el resultado reportado del build de preview, no la navegación del caso C99 en producción ni una validación del contenido. Esta revisión no dispara un despliegue manual.

## Fuentes primarias de semántica

- https://www.php.net/manual/en/language.basic-syntax.comments.php
- https://www.php.net/manual/en/language.basic-syntax.phptags.php
- https://www.php.net/manual/en/language.types.string.php

Seguimiento del caso: [issue #8](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/8). El expediente de gestión y sus referencias privadas no se publican en este repositorio.
