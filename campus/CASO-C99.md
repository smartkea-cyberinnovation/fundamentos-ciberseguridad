# Integración del caso C99-DFIR

Fuente docente: [formacion/casos/c99-forense](../formacion/casos/c99-forense/README.md). Fecha de edición: 2026-10-19.

`operations.related_reading` añade enlaces explícitos a la guía española o inglesa desde M27, M28 y M29. Son enlaces al material público en GitHub; no una ruta de ejecución de PHP ni un terminal remoto del campus. El README del análisis previo y el nuevo índice de casos conducen al mismo recurso.

Se preservan los identificadores M01–M32, L01A–L32C y D01–D46 y las 480 horas del catálogo. No se migra almacenamiento local ni se marcan competencias completadas. Las doce preguntas del caso son un banco independiente, no se añaden silenciosamente al examen general de 100 preguntas.

## Material y seguridad

Guía del alumno y guía inglesa, diez actividades, catorce eventos sintéticos normalizados, tres fichas inertes de webroot, herramienta de manifiestos y cronología, plantilla de informe, soluciones, rúbrica y doce preguntas. El contenedor opcional proporciona una shell legítima efímera, sin red, sin root ni montajes de host. No contiene C99 ejecutable ni descarga la muestra.

Las fichas y eventos no son logs reales ni sustituyen la evidencia del análisis previo. Los IOC reales se referencian por separado. El encabezado y las fechas internas no se presentan como atribución o adquisición acreditadas. No se incluyen enlaces privados de correo, Drive, tracker o conversación.

## Validación

`campus/tests/test_c99_case.py` comprueba el helper, cronología, errores, integridad, guías, banco de preguntas y enlaces ES/EN. El workflow `C99 - forensic classroom case` añade construcción Docker y comprobación de UID, denegación de escritura y ausencia de interfaces externas. El workflow general conserva sus pruebas y añade el directorio de casos al snapshot de fuentes y a sus filtros de cambios.

```sh
python3 -m unittest discover -s campus/tests -p 'test_c99_case.py' -v
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
python3 campus/build.py
python3 campus/check_release.py
```

Estos son procedimientos de verificación, no una declaración anticipada de resultado. Consultar logs, commit y conclusión de cada workflow para saber qué se ejecutó. El entorno local de edición no pudo ejecutar pruebas en esta sesión; la validación se ha preparado para GitHub Actions. Un PR o build de preview no equivale a publicación comprobada en producción. La corrección independiente del lexer del PR #12 no se fusiona como efecto secundario de este caso.
