# Test de práctica · Introducción a la informática

[Abrir el simulador](https://smartkea.com/introduccion-ciberseguridad/examen/) · [Guía de los doce temas](https://smartkea.com/introduccion-ciberseguridad/#/recurso/D46) · [Banco de preguntas](../formacion/introduccion-informatica/banco-preguntas.json)

## Cómo practicar

Inicia una sesión de veinte preguntas. Lee el enunciado, elige una de las cuatro respuestas y contrasta la explicación que aparece inmediatamente. La primera elección queda registrada; consultar la solución no permite sumar otro acierto. Puedes volver a una pregunta para estudiar su razonamiento.

Al terminar, consulta aciertos, errores, preguntas pendientes y puntuación sobre diez. El resumen por tema indica qué reforzar dentro de ese intento, no una medida completa de competencia. Revisa los fallos y abre la lectura enlazada antes de iniciar otra sesión.

La selección utiliza el banco completo de cien preguntas sin repetición dentro del intento. El orden de las preguntas y las opciones se baraja. Distintos intentos pueden compartir preguntas; al ser un muestreo aleatorio, veinte preguntas no garantizan representar todos los temas en cada ocasión.

## Contenido y alcance

| Tema | Preguntas |
|---|---:|
| T01 · Informática, evolución y aplicaciones | 6 |
| T02 · Representación y aritmética binaria | 12 |
| T03 · Codificación y compresión multimedia | 10 |
| T04 · Lógica digital y álgebra de Boole | 10 |
| T05 · Arquitectura, CPU e instrucciones | 8 |
| T06 · Memoria, almacenamiento e integridad | 10 |
| T07 · Buses, periféricos y entrada/salida | 6 |
| T08 · Sistemas operativos y procesos | 8 |
| T09 · Memoria virtual, archivos y permisos | 8 |
| T10 · Software, licencias y mantenimiento | 6 |
| T11 · Redes, protocolos y protección | 8 |
| T12 · Virtualización, cloud y tecnologías actuales | 8 |
| **Total** | **100** |

Cada pregunta tiene una única respuesta correcta y explicación propia. Las respuestas numéricas precisan sus supuestos: bits o bytes, prefijos decimales o binarios, formato sin comprimir, cabeceras excluidas o aritmética limitada a ocho bits. Los casos operativos separan una observación de una atribución no demostrada.

El simulador está en español. El banco de respuestas es público porque su finalidad es ensayar; no incorpora vigilancia, verificación de identidad, certificación ni envío de notas oficiales. La puntuación es orientativa y no sustituye las prácticas, el proyecto o la evaluación aprobada para una asignatura.

## Estado local

El intento activo se conserva únicamente en el navegador cuando el guardado está disponible. La aplicación valida versión de banco, selección, opciones, respuestas e índices antes de restaurarlo. Si la copia no es compatible, informa y permite comenzar de nuevo. Si el navegador impide guardar o no puede coordinar las pestañas, la aplicación avisa y la sesión continúa en memoria.

Las pestañas de un mismo navegador combinan las respuestas del mismo intento y conservan la primera respuesta guardada de cada pregunta. Finalizar o sustituir un intento se refleja en las otras pestañas; una pestaña antigua no puede reabrirlo ni recuperar una selección sustituida.

Las claves del test son independientes del progreso del campus y del aula de sistemas. Cerrar o borrar almacenamiento puede eliminar la continuidad de un intento. No hay sincronización entre dispositivos ni recepción de respuestas por parte del docente.

## Editar el banco

Modifica `formacion/introduccion-informatica/banco-preguntas.json`. Conserva identificadores cuando el significado de la pregunta se mantenga. Cambia `version` cuando varíen enunciados, respuestas o reglas de evaluación para evitar restaurar un intento contra soluciones diferentes.

El contrato de cada pregunta es:

```json
{
  "id": "INF-001",
  "topic": "T01",
  "difficulty": "basico",
  "prompt": "Enunciado de una pregunta concreta",
  "options": [
    {"id": "a", "text": "Primera opción"},
    {"id": "b", "text": "Segunda opción"},
    {"id": "c", "text": "Tercera opción"},
    {"id": "d", "text": "Cuarta opción"}
  ],
  "correctOptionId": "b",
  "explanation": "Por qué se sostiene la respuesta, con sus límites.",
  "study": {"label": "D26 · Repasar", "url": "../#/recurso/D26"}
}
```

El ejemplo describe el formato y no forma parte del banco evaluable. Dificultades permitidas: `basico`, `intermedio`, `aplicacion`. El compilador exige cien preguntas, doce temas, cuatro opciones distintas, IDs únicos y referencias de estudio existentes. Evita preguntas de opinión con varias respuestas defendibles y distractores que resulten correctos bajo una interpretación razonable.

## Arquitectura y verificación

`campus/exam/` contiene HTML, CSS claro, controlador y modelo sin dependencias de producción. `campus/exam_build.py` valida y publica el banco y los activos en `campus/dist/examen/` antes de generar manifiesto y ZIP. El Worker los sirve bajo `/introduccion-ciberseguridad/examen/` con la CSP existente.

La escritura compartida se coordina con Web Locks y valida el intento vigente antes de combinarlo. Las regresiones incluyen escrituras simultáneas de dos pestañas, cierre y sustitución con una pestaña rezagada y funcionamiento en memoria cuando no hay coordinación disponible.

Desde la raíz:

```sh
python3 campus/cloudflare.py build
python3 -m unittest discover -s campus/tests -p 'test_intro_exam.py' -v
node --test campus/tests/exam.test.mjs
python3 campus/tests/browser_exam.py
```

La prueba de navegador requiere Playwright y el motor indicado en el workflow. No consideres un motor ausente como una aceptación superada. La verificación de producción comprueba además el commit público y el hash del banco en `build-info.json`, la descarga same-origin y el flujo real de contestar, corregir, reanudar y finalizar.
