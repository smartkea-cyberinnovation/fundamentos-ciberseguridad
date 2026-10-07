# Validación del laboratorio

## Comprobaciones ejecutadas el 7 de octubre de 2026

Se ejecutó el siguiente comando en el entorno de trabajo del desarrollo:

```bash
python3 -m unittest discover -s labs/tests -v
```

Resultado: **23 pruebas consideradas, 22 correctas y 1 omitida por una limitación del entorno**. El runner tiene UID 0 pero no permite cambiar a un UID sin privilegios; por eso se omitió únicamente el arranque de un proceso HTTP separado como usuario sin privilegios y la inspección de su `NoNewPrivs`. No se modificaron los permisos del entorno para forzar esa comprobación.

Las pruebas ejecutadas cubren:

| Área | Evidencia comprobada |
| --- | --- |
| HTTP real en loopback | GET/HEAD, contrato JSON de `/health`, rutas desconocidas, robots, longitud de cuerpo y 405 para modificaciones |
| Entrada HTTP | Rechazo de rutas de filesystem y ausencia de reflexión de parámetros |
| Logs | No aparecen Authorization ni query strings, con registros JSON estructurados |
| Concurrencia | Límite de conexiones y rechazo de capacidad excedida |
| Bash | Sintaxis de todos los scripts; generador con espacios en rutas; permisos; rechazo de sobrescritura y symlinks |
| Evidencias | Verificación de hashes, fallo tras alteración y rechazo de entradas de manifiesto fuera de la práctica |
| Launchers | Rechazo explícito de root y de argumentos no admitidos antes de llamadas externas |
| YAML | Lectura sintáctica y reglas de configuración para aislamiento, perfiles, usuario, recursos y bindings de loopback |
| Swarm | Ausencia de publicación de puertos, imágenes exigidas, restricción de alumno y secretos entregados solo al conector |
| Tunnel | Validación Access en cada regla, Host consistente y fallback 404 |
| Paquete público | Inventario explícito de fuentes sin volúmenes, evidencias o secretos |

También se comprobaron la compilación sintáctica Python y los enlaces relativos de la documentación. Las pruebas no necesitan objetivos externos: utilizan loopback y datos generados.

## Evidencia de GitHub Actions

El [run 37644072310](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/37644072310), sobre el commit `e2c3f53c25b26003cd5791c3bc0ea7629e393a31`, completó el build de ambas imágenes, `docker compose config` y el smoke real. El [job de laboratorio](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/actions/runs/37644072310/job/112870134650) confirmó HTTP saludable, Nmap contra el único objetivo sintético, integridad de evidencias y `NoNewPrivs: 1`.

También confirmó ttyd en lectura y escritura: HTTP, rechazo de un Origin incorrecto, WebSocket válido, PTY y comprobaciones de entrada/ejecución. La suite consideró 23 pruebas: 22 correctas y una omisión esperada del rechazo de root en el runner sin privilegios. Las pruebas de navegador del mismo run superaron Chromium y WebKit en 1440, 768, 390 y 320 px, con las 48 lecciones y sin solicitudes externas.

## Verificación de la VM de despliegue

El entorno local de desarrollo no disponía de Docker Engine/CLI, ShellCheck, cloudflared ni ttyd. El build y el smoke con contenedores se ejecutaron después en GitHub Actions, como se documenta arriba. Quedan por comprobar sobre la infraestructura elegida el servicio Swarm, ShellCheck y el recorrido público con Cloudflare Access/Tunnel. La revisión YAML no sustituye esos parsers y controles operativos.

Para completar la verificación en una VM Linux con Docker:

```bash
docker compose -f labs/compose.yaml config --quiet
labs/scripts/smoke.sh
docker compose -f labs/compose.yaml run --rm --no-deps -T toolbox bash -c 'shellcheck /opt/lab/bin/*.sh'
```

`smoke.sh` crea un proyecto temporal propio y elimina únicamente sus contenedores y volúmenes al terminar. Además de HTTP, herramientas y evidencias, arranca de verdad los servicios Compose `terminal` y `terminal-write` mediante `compose run`, sin publicar sus puertos en el host. Un cliente Python de biblioteca estándar conecta a `127.0.0.1:7681` dentro de cada contenedor. Comprueba el índice HTTP, rechaza un `Origin` distinto, completa un handshake WebSocket válido e inicia un PTY usando el protocolo de ttyd 1.7.7. En lectura comprueba UID 10001, ausencia de eco al enviar entrada y continuidad del monitor; en escritura ejecuta una comprobación inocua de UID, `NoNewPrivs`, `/workspace` escribible, `/etc` protegido y ausencia del socket Docker. La salida esperada se construye en dos partes para distinguir ejecución de un simple eco del comando.

La prueba está verificada en CI y se debe repetir en la VM de destino. No verifica el proveedor de identidad, una sesión Access, nginx ni el recorrido público del túnel, que requieren las comprobaciones de despliegue de `CONEXION-TTYD.md`.

Para ejecutar pruebas fuera de la imagen Kali, prepara un entorno Python local:

```bash
python3 -m venv .venv-lab-tests
.venv-lab-tests/bin/python -m pip install -r labs/tests/requirements.txt
.venv-lab-tests/bin/python -m unittest discover -s labs/tests -v
```

En un runner no root se omite la prueba de rechazo de root; en el paquete ZIP puede omitirse la comprobación del inventario de empaquetado, porque ese inventario pertenece al repositorio y no se auto-incluye. El resto de resultados debe ser correcto. Para comprobar la elevación y el arranque efectivo del proceso ejecuta la suite en una VM donde el usuario pueda arrancar normalmente procesos sin privilegios.

Antes de conceder escritura por navegador completa [CONEXION-TTYD.md](CONEXION-TTYD.md), y para Swarm, [SWARM.md](SWARM.md). Deben quedar registrados el commit desplegado, digests efectivos, salida de healthchecks, usuario, `NoNewPrivs`, límites y comportamiento de al menos una identidad permitida y una denegada.

## Alcance de las garantías

La implementación prepara aislamiento y controles por defecto y sus pruebas detectan regresiones concretas. No acredita ausencia absoluta de vulnerabilidades, disponibilidad de una VM, alta de dominio, permisos de Cloudflare, aislamiento frente a un administrador del daemon ni una auditoría de la infraestructura del usuario. El control de una VM dedicada y la publicación del endpoint se completan con la evidencia del entorno real.
