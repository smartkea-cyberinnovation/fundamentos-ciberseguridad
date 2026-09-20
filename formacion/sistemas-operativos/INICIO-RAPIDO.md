# Primera sesión y entrada al material práctico

Edición 1.1. No es necesario ejecutar la aplicación de la raíz del repositorio. Abre una terminal dentro de `formacion/sistemas-operativos`. No uses una terminal elevada ni tus carpetas personales como dataset. El curso sigue teniendo 480 horas; estas guías desarrollan actividades ya presupuestadas.

## Antes de escribir comandos

Identifica equipo, sistema, shell, directorio y usuario. Abre el explorador/Finder en la misma ubicación y comprueba que ves el mismo README. En Linux/macOS utiliza `pwd`; en PowerShell `Get-Location`; en CMD `cd`. No copies el símbolo de prompt `$`, `PS>` o `>` que pueda aparecer en otros manuales.

El kit requiere Python 3.11 o superior, sin paquetes adicionales. Comprueba `python3 --version` en Linux/macOS. En Windows utiliza el intérprete aprobado del laboratorio, por ejemplo `py -3 --version`. Tener Python no demuestra que una práctica nativa Windows/macOS se haya probado. Si no está instalado, el docente puede entregar previamente la carpeta sintética; la primera sesión no debe convertirse en una instalación improvisada.

## Crear un caso desechable

En Linux/macOS, desde el directorio del curso:

```bash
python3 kit/oslab.py init "mi-laboratorio"
python3 kit/oslab.py manifest "mi-laboratorio"
```

En Windows, desde PowerShell o CMD:

```powershell
py -3 kit/oslab.py init "mi-laboratorio"
py -3 kit/oslab.py manifest "mi-laboratorio"
```

Resultado esperado: `created`, `synthetic: true`, ocho archivos y ocho eventos; el manifiesto cuenta **8 archivos y 62 bytes**. El nombre puede contener espacios. Repetir `init` sobre la misma carpeta debe fallar: no se sobreescribe un trabajo anterior. Usa otro nombre para repetir. Los ocho archivos están en `datos`; las salidas propias se guardan en `salida`, nunca encima de `eventos.json` o `indicadores.json`.

El marcador `.oslab` evita usos accidentales: no es un aislamiento de seguridad ni una prueba de autorización. El kit está destinado a carpetas de un solo usuario sin modificaciones concurrentes. No utilizarlo como herramienta de adquisición forense en evidencia real.

## Sesión de 120 minutos

| Minutos | Trabajo | Demostración de aprendizaje |
|---|---|---|
| 0–15 | Identificar GUI, terminal, shell y usuario | Explicar dónde se ejecuta una orden |
| 15–30 | Ubicarse y obtener ayuda local | Distinguir ruta y argumento |
| 30–50 | Crear/recibir el caso sintético y navegar | Abrir por GUI y CLI el mismo archivo |
| 50–70 | Contar archivos, ocultos, bytes y líneas | Explicar LF/CRLF y Unicode sin confundir bytes/caracteres |
| 70–90 | Introducir un error de ruta; leer stdout/stderr | Reconocer el fallo sin elevar privilegios |
| 90–110 | Copiar un archivo a `salida`; comparar | Explicar diferencia entre copiar y mover |
| 110–120 | Entregar nota breve y hacer revisión cruzada | Registrar versión, resultado y limitación |

Esta es una propuesta de primera sesión seleccionada; no equivale a completar M01–M05 ni añade horas al calendario. La generación de fixtures es una ayuda de preparación, no contenido Python exigible al principiante.

## Continuar

Consulta [los ocho guiones prácticos](practicas/README.md), [las lecciones desarrolladas](lecciones/README.md), [el contrato técnico del kit](kit/README.md) y [la planificación verificable](planificacion/README.md). Las [pruebas](qa/RESULTADOS.md) distinguen ejecución de código, revisión documental y validación nativa pendiente.
