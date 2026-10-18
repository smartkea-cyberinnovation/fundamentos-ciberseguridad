# C99: aprender análisis estático sin ejecutar una webshell

Caso `C99-20261018` · revisión documental y de herramientas: 2026-10-18 · seguimiento: [issue #8](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/8).

## Qué aprenderás

Distinguir una cadena sospechosa de una operación alcanzable, separar capacidades del código de actividad observada, recuperar literales PHP con escapes hexadecimales/octales, seguir saltos `goto`, producir IOC contextualizados y documentar límites de atribución y detección.

Esta edición pública no contiene la webshell original, una shell funcional desofuscada, credenciales, logs de víctimas ni URL internas de correo, Drive, tracker o chat. El dossier completo neutralizado se conserva en el expediente privado bajo el mismo ID. No ejecutar ni desplegar la muestra.

## Ruta de estudio

1. Lee [el análisis y la revisión](REVISION.md). Anota qué está demostrado y qué queda pendiente.
2. Examina [los indicadores](inteligencia/ioc.json). El fichero público selecciona indicadores de alta especificidad; el dossier privado conserva los 22 registros de IOC y contexto.
3. Revisa [el triage offline](herramientas/triage_offline.py) y ejecuta las pruebas con datos sintéticos.
4. Comprueba una copia de evidencia como bytes; no la incluyas con PHP ni la abras en un servidor web.
5. Diseña pruebas positivas y negativas para las reglas del dossier. Una regla escrita no es una regla validada en producción.

Desde este directorio:

```bash
python3 -m unittest discover -s pruebas -v
python3 herramientas/triage_offline.py /ruta/a/copia_de_evidencia --out resultado_nuevo.json
```

Python estándar, sin paquetes adicionales ni acceso de red. No requiere Docker, PHP, un backend ni infraestructura de laboratorio. El analizador tiene límites expresos: no es un AST/CFG completo ni certifica ausencia de malware.

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

Un informe breve con hash, fuente, fecha de adquisición real, cadena fuente–transformación–destino, condiciones de alcanzabilidad, IOC específicos y contextuales, una hipótesis refutable y una tabla de pruebas. Resolver: ¿qué evidencia adicional demuestra un POST exitoso? ¿Qué dato permite atribuir una modificación a un autor? ¿Por qué una IP de CDN no identifica al receptor real?
