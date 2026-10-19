# C99: aprender análisis estático sin ejecutar una webshell

Caso `C99-20261018` · análisis inicial: 2026-10-18 · ampliación docente: 2026-10-19 · seguimiento: [issue #8](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/8).

## Caso práctico completo

**[C99-DFIR: investigación forense, descubrimiento y uso controlado de shells](../../../formacion/casos/c99-forense/README.md)** convierte el análisis en diez actividades: preservación, shell legítima en contenedor, descubrimiento, flujo del código, ofuscación, cronología, correlación, detección, recuperación e informe. Incluye evidencias sintéticas, guía inglesa, herramienta independiente de manifiestos/timeline, doce preguntas, soluciones y rúbrica. Se enlaza desde M27–M29 sin cambiar horas ni IDs de progreso.

La muestra real y el supuesto inventado están separados. No se incluye una C99 operativa ni se contacta con el receptor. [Índice de casos](../../../formacion/casos/README.md).

## Qué aprenderás del análisis original

Distinguir una cadena sospechosa de una operación alcanzable, separar capacidades del código de actividad observada, recuperar literales PHP con escapes hexadecimales/octales, seguir saltos `goto`, producir IOC contextualizados y documentar límites de atribución y detección.

Esta edición pública no contiene la webshell original, una shell funcional desofuscada, credenciales, logs de víctimas ni URL internas de correo, Drive, tracker o chat. El dossier completo neutralizado se conserva en el expediente privado bajo el mismo ID. No ejecutar ni desplegar la muestra.

## Ruta de estudio del análisis

1. Lee [el análisis y la revisión](REVISION.md). Anota qué está demostrado y qué queda pendiente.
2. Examina [los indicadores](inteligencia/ioc.json). El fichero público selecciona indicadores de alta especificidad; el dossier privado conserva los 22 registros de IOC y contexto.
3. Revisa [el triage offline](herramientas/triage_offline.py) y las observaciones de su revisión en [PR #12](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/12). Registra el commit y no lo trates como un parser completo.
4. Comprueba una copia de evidencia como bytes; no la incluyas con PHP ni la abras en un servidor web.
5. Diseña pruebas positivas y negativas para las reglas del dossier. Una regla escrita no es una regla validada en producción.

Desde este directorio:

```bash
python3 -m unittest discover -s pruebas -v
python3 herramientas/triage_offline.py /ruta/a/copia_de_evidencia --out resultado_nuevo.json
```

Python estándar, sin paquetes adicionales ni acceso de red. No requiere Docker, PHP, un backend ni infraestructura de laboratorio para el análisis estático. El analizador tiene límites expresos: no es un AST/CFG completo ni certifica ausencia de malware. El contenedor opcional del nuevo caso contiene sólo material sintético y una shell legítima.

## Hechos principales del caso

| Hecho estático | Evidencia | Límite |
|---|---|---|
| Notifica la URL completa a un receptor externo antes del login normal | QpRos, z2KH7, Q7vOx, SXetq | No prueba recepción ni ejecución en una víctima |
| Existe una rama alternativa de subida antes del control de acceso | uT50x, gJmPl | Requiere permisos de escritura; no implica root |
| Importa configuración de la petición mediante extract | nDYHe / c99shcook | Tiene antecedentes; no atribuirlo como novedad al ofuscador |
| Actualizador con descarga/escritura y rama eval | W2xGr / XxN72 | URL base inicialmente vacía; no es otro callback fijo activo |
| Deserializa una cookie y puede restaurar tiempos | mn75f; akNsc, cT0PQ | Impacto condicionado por entorno y ruta |

La respuesta del callback no se evalúa como PHP en ese bloque. Una URI que incluya secretos puede filtrarlos; eso es distinto de afirmar que el callback transmite todo el cuerpo POST o todas las cookies.

## Entregable del alumno

Un informe con hash, fuente, fecha de adquisición real, cadena fuente–transformación–destino, condiciones de alcanzabilidad, IOC específicos y contextuales, hipótesis refutables y tabla de pruebas. La [plantilla del caso](../../../formacion/casos/c99-forense/INFORME.md) separa evidencia estática, escenario sintético y observación local.
