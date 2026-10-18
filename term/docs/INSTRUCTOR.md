# Guía del instructor: observar, explicar y evaluar

## Una persona, una VM y una evidencia

La clase debe relacionar cada acción con su resultado: el alumno anticipa qué espera, ejecuta el comando, observa stdout/stderr y el código de salida, interpreta el resultado y guarda una evidencia breve. No necesita capturar cada tecla. El feedback útil distingue la hipótesis, el hecho observado y la conclusión.

Una secuencia de demostración de 25 minutos puede dedicar 5 minutos a situarse en el sistema, 8 a ficheros y pipes, 8 a una petición HTTP y logs, y 4 a explicar lo aprendido. Estos tiempos son una propuesta docente. La evaluación valora que el alumno identifique el espacio de ejecución, limite el objetivo y pueda repetir el resultado.

## Qué observa cada modo

| Modo | Lo que muestra | Sesión compartida |
| --- | --- | --- |
| ttyd del contenedor, lectura | Estado del contenedor y salud HTTP | No; no muestra comandos de otro terminal |
| ttyd del contenedor, escritura | Una shell real con el usuario learner | Un cliente máximo; el volumen persiste |
| ttyd nativo de VM, lectura | Diagnóstico del anfitrión del alumno | No |
| ttyd nativo de VM, escritura | Sesión tmux `smartkea-lab` | Solo dentro de la VM/cuenta asignadas |
| ttyd observer nativo | La sesión tmux anterior, sin entrada | Sí, observación deliberada del instructor |

Por defecto la interfaz no afirma que está viendo los comandos del alumno. Para observar exactamente la sesión interactiva, habilita el modo tmux explícito de una sola VM y explica al alumno qué se comparte.

## Observar tmux en lectura

La guía [CONEXION-TTYD.md](CONEXION-TTYD.md) prepara el modo nativo. El alumno abre la terminal writable y se crea `smartkea-lab`. Desde esa cuenta comprueba:

```bash
tmux list-sessions
```

El modo de observación usa `tmux attach-session -r`: el cliente es de lectura [S16]. Además ttyd omite `--writable`, sumando una restricción de entrada en la capa web. Para iniciar el observer, en la VM como la misma cuenta del alumno:

```bash
install -m 0600 labs/config/ttyd-observer.service "$HOME/.config/systemd/user/ttyd-observer.service"
systemctl --user daemon-reload
systemctl --user start ttyd-observer.service
```

El observer escucha únicamente en `127.0.0.1:7682`. Asigna un hostname diferente, por ejemplo `observe-a01.smartkea.com`, con **su propia aplicación Access restringida al instructor**, Audience y regla ingress de Tunnel que apunten al puerto 7682. Conserva `httpHostHeader` igual a ese hostname. No agregues una política amplia de toda la clase a ese endpoint.

El proceso de observación se ejecuta como el mismo usuario de la VM para alcanzar su socket tmux; la autorización de quién llega por navegador reside en Access. No compartas el socket tmux con otros alumnos ni amplíes sus permisos. La sesión puede contener comandos, rutas o datos del alumno: utiliza datos sintéticos, informa del alcance y para la observación al acabar. No se activa grabación automática.

La unidad limita su vida a tres horas. Si la sesión tmux no existe o ya terminó, el observer no puede mostrarla; pide al alumno que abra su sesión y vuelve a conectar. Si el administrador termina el servicio writable puede terminar también procesos de su cgroup; conserva los cambios de los ejercicios antes de cerrar.

## Rúbrica práctica sugerida

| Criterio | Evidencia suficiente | Peso propuesto |
| --- | --- | --- |
| Entiende el contexto | Identifica usuario, directorio, distro y anfitrión/contenedor | 15 % |
| Maneja ficheros y permisos | Crea una estructura ordenada, explica rutas y umask | 20 % |
| Compone comandos | Pipeline legible, quoting, stderr y códigos de salida | 20 % |
| Observa y contrasta | Compara HTTP, puerto y logs sin convertir suposiciones en hallazgos | 20 % |
| Automatiza con criterio | Bash con argumentos validados, errores útiles y objetivo acotado | 15 % |
| Comunica y conserva | Evidencia reproducible y conclusión breve, con límites explícitos | 10 % |

En un reto final, pide que diagnostique una respuesta 404, la relacione con un log, distinga disponibilidad del puerto y existencia del recurso, automatice la comprobación de `/health` y entregue un resumen de cinco líneas. Un código de salida esperado y una explicación acertada valen más que un escaneo amplio.

## Fallos frecuentes que conviene enseñar

`sudo` no existe en la caja Kali: el ejercicio de privilegios pertenece a la VM. Docker dentro del terminal no tiene daemon: la administración se hace en el anfitrión. Un puerto 8080 abierto no demuestra una vulnerabilidad. Un 404 en `robots.txt` o en una ruta no es una brecha. Cambiar una etiqueta de imagen no actualiza un contenedor que sigue ejecutándose. Cerrar el navegador no garantiza que hayan terminado todos los procesos de una sesión persistente.

Estas diferencias son oportunidades para practicar un diagnóstico estructurado, no motivos para eliminar controles de aislamiento. Fuentes: [SOURCES.md](SOURCES.md).
