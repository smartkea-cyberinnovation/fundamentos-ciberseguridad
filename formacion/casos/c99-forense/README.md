# C99-DFIR · Una shell con una llamada oculta

**Caso práctico de investigación forense, descubrimiento y uso controlado de shells.** Edición docente: 19 de octubre de 2026. Expediente de origen: C99-20261018. [English guide](PRACTICA.en.md).

[Empezar la práctica](PRACTICA.md) · [Soluciones y rúbrica](DOCENTE.md) · [Plantilla de informe](INFORME.md) · [Escenario sintético](evidencias/escenario.json) · [Autoevaluación](preguntas.json) · [Análisis previo de C99](../../../docs/casos/c99-20261018/README.md)

## Qué vas a demostrar

Localizar indicios sin ejecutar un fichero sospechoso; diferenciar terminal, shell local, SSH y webshell; trabajar con una shell real dentro de un contenedor de aula; preservar y verificar copias; seguir la relación entre entrada, transformación y salida del código; construir una cronología con zonas horarias; distinguir intento de comunicación de entrega; elaborar un informe técnico y un resumen para dirección.

## Tres materiales que no se deben mezclar

| Material | Naturaleza | Qué permite afirmar |
|---|---|---|
| Análisis C99 referenciado en docs/casos | Evidencia estática de la variante identificada | Capacidades presentes en ese código; no ejecución en una víctima |
| evidencias/escenario.json y webroot | Datos sintéticos creados para esta actividad | Resolver el supuesto del aula; nunca un incidente real de SmartKEA o de terceros |
| Resultados obtenidos por el alumno | Observaciones de su ejecución local | Qué herramienta, copia y entorno utilizó; no sustituyen a las fuentes originales |

No se distribuye aquí C99 operativo, no se descarga automáticamente la muestra y no se conecta con su receptor. La práctica de shell utiliza `/bin/sh` en un contenedor legítimo, sin red ni privilegios administrativos. Los ficheros `.txt` del webroot son fichas inertes, no PHP ejecutable.

## Empieza desde la raíz del repositorio

Python 3.10 o posterior y biblioteca estándar. No se necesita PHP, un servidor web, un SIEM ni credenciales.

```sh
cd formacion/casos/c99-forense
mkdir -p trabajo
python3 herramientas/forense.py manifest evidencias > trabajo/manifest.json
python3 herramientas/forense.py verify evidencias trabajo/manifest.json
python3 herramientas/forense.py timeline evidencias/escenario.json > trabajo/timeline.json
```

El manifiesto generado documenta tu copia en ese momento: no es una firma del autor ni prueba de una adquisición anterior. Conserva también `git rev-parse HEAD`, la fecha UTC y la bitácora. No guardes tus entregas en `evidencias/` ni las publiques en GitHub.

## Laboratorio opcional con shell real

Desde este directorio:

```sh
docker compose -f compose.laboratorio.yaml build
docker compose -f compose.laboratorio.yaml run --rm --no-deps lab
docker compose -f compose.laboratorio.yaml run --rm --no-deps --entrypoint /bin/sh lab
```

El build puede descargar una imagen; la ejecución de aula usa `network_mode: none`. Registra el ID de la imagen construida. La etiqueta base no es un digest inmutable; el docente puede fijarlo mediante `BASE_IMAGE`. No es una jaula para ejecutar malware: se usa exclusivamente con las evidencias sintéticas incluidas. No publica puertos, no monta el socket de Docker ni carpetas del host y no instala persistencia. No se despliega en Swarm porque este ejercicio es una sesión local efímera, no un servicio remoto.

## Organización docente

Diez actividades con entregables verificables, prueba negativa y cierre. Puede dividirse en preservación/descubrimiento, análisis/correlación y comunicación/recuperación. El avance depende de evidencias, no de un cronómetro obligatorio. Las soluciones y las doce preguntas son públicas para aprender; no constituyen un examen acreditativo ni una prueba con respuestas reservadas.

La ampliación se enlaza desde los módulos M27, M28 y M29 del campus. No añade módulos, horas o marcas de progreso, ni convierte este escenario sintético en un laboratorio de malware nativo ya ejecutado.
