# R03 · CMD, BAT y PowerShell sobre el mismo problema

**L16A · 3 h.** Entrada: M13–M15. Requiere Windows real y motores aprobados; no basta un contenedor Linux. [Lección 03](../lecciones/03-windows.md).

## Preparación y alcance

Registra edición/build, `$PSVersionTable`, directorio y usuario. Prepara el workspace con Python aprobado o recíbelo del docente. Usa cuenta estándar. Si una política impide ejecutar el archivo, sigue el procedimiento del docente; no la desactives ni añadas opciones de bypass.

## Tareas

1. En CMD, lee `kit\resumen.cmd` con `type`; identifica variables, expansión y `errorlevel`. Ejecuta `kit\resumen.cmd mi-laboratorio`. El caso base devuelve `{"count":8}`.
2. En PowerShell, inspecciona `Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force | Get-Member`. Explica tipo y propiedad `Length`.
3. Ejecuta el archivo revisado en su motor aprobado: `powershell.exe -NoProfile -File kit\Resumen.ps1 -Workspace mi-laboratorio`, o `pwsh` cuando sea la variante prevista. Debe devolver conteo 8 y bytes 62. Registra cuál se utilizó; no atribuyas el resultado al otro motor.
4. Selecciona `Name`, `Length` y `Attributes`, y exporta solo esos datos a un archivo nuevo de `salida`. No pases por `Format-Table` antes de exportar.
5. Ensaya workspace ausente y marcador incorrecto en una copia del caso. Diferencia ejecución de script, salida JSON y estado de proceso.

## Análisis crítico

BAT usa un listado de nombres y tiene límites con encoding, nombres especiales y errores de enumeración. No se puntúa ocultarlos. Indica qué tareas migrarías a PowerShell y por qué. El ejemplo de PowerShell no acredita administración de Registro, eventos, servicios o directorio: esas competencias se evalúan en sus módulos nativos.

## Evidencia, éxito y cierre

Entrega salidas de ambos motores, una tabla texto/objetos y explicación de un caso negativo. Éxito: equivalencia funcional declarada y limitaciones explícitas. Conserva originales y retira solo exportaciones desechables. **Estado de la edición: guion y código preparados; ejecución nativa Windows pendiente.**
