# Planificación verificable

El [plan docente](../PLAN-DOCENTE.md) sigue siendo la explicación pedagógica. `curriculo.json` conserva sus 32 módulos y prerrequisitos. `generar.py` deriva las sesiones y laboratorios sin inventar fechas, alumnos ni resultados de evaluación.

Desde el directorio del curso:

```bash
python3 planificacion/generar.py --check
python3 planificacion/generar.py > planificacion-local.json
python3 -m unittest discover -s planificacion -v
```

En Windows, utilizar el ejecutable Python instalado (`py -3` o `python` según el entorno). El fichero generado contiene 240 sesiones de dos horas y 96 laboratorios. No contiene credenciales ni información del equipo. La redirección puede sobrescribir `planificacion-local.json`: elegir una salida nueva o revisar antes de repetir.

## Qué se verifica

IDs únicos y ordenados; prerrequisitos ya disponibles; duración de cada sesión; reparto de práctica A/B/C; 480 horas totales, 168 teóricas y 312 prácticas. M01–M30 tienen siete sesiones y tres laboratorios de tres horas; M31 tiene diez sesiones y tres laboratorios de cuatro horas; M32 tiene veinte sesiones y tres fases prácticas de diez horas.

En una sesión pueden coexistir el final de un laboratorio y el inicio del siguiente. El JSON conserva los minutos de cada parte para evitar contar dos veces las horas. Los ocho runbooks nuevos desarrollan laboratorios existentes: no añaden ocho laboratorios a los 96.

## Qué no se verifica

No valida que la duración propuesta sea suficiente para una cohorte concreta; eso requiere piloto docente. Tampoco demuestra ejecución de laboratorios, competencia de alumnos, disponibilidad de equipos, licencias o calendario lectivo. El estado de las prácticas permanece separado de la planificación.

Las ocho pruebas de este generador son adicionales a las 42 pruebas del kit. Ver [resultados](../qa/RESULTADOS.md). Cualquier cambio del catálogo debe actualizarse también en el plan docente y superar las pruebas antes de aprobar una nueva edición.
