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

## Lo que necesita ejecutarse en la VM de despliegue

En este entorno **no hay Docker Engine/CLI, ShellCheck, cloudflared ni ttyd instalados**. Por tanto no se ha ejecutado el build de imágenes, `docker compose config`, el smoke con contenedores, la conversión real de `docker stack config`, un servicio Swarm ni el recorrido Access/WebSocket. La revisión YAML no sustituye esos parsers y controles operativos.

Para completar la verificación en una VM Linux con Docker:

```bash
docker compose -f labs/compose.yaml config --quiet
labs/scripts/smoke.sh
docker compose -f labs/compose.yaml run --rm --no-deps -T toolbox bash -c 'shellcheck /opt/lab/bin/*.sh'
```

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
