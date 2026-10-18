# Despliegue en Docker Swarm

## Modelo del laboratorio

El stack incluye HTTP sintético, ttyd sin root y un conector cloudflared. Cada alumno tiene su propia VM, configuración de Access, credencial de Tunnel, volumen y restricción de ubicación. No concede al alumno control de un Swarm compartido: los ejercicios de administración del daemon se hacen en un Swarm de práctica dedicado a esa persona.

El [stack](../labs/stack.yaml) utiliza el formato legacy v3 para `docker stack deploy`, imágenes ya construidas, servicios con una réplica y `endpoint_mode: dnsrr`. Swarm no construye los Dockerfiles al desplegar [S12]. Las variables se suministran en el entorno del administrador; `docker stack` no carga automáticamente el `.env` de Compose.

No hay `ports` en este stack. Docker publica los puertos de servicios Swarm en todas las interfaces; el binding local de Compose no se traslada a Swarm. El Tunnel accede por una red overlay privada al servicio `terminal:7681` y es el único componente con red de salida [S7, S13].

## 1. Construir y publicar imágenes

Construye las imágenes mediante `labs/compose.yaml`, ejecuta `labs/scripts/smoke.sh` y publícalas en el registro autorizado de tu organización. Elige las arquitecturas de tus nodos y conserva los digests finales. Fija también una versión vigente y comprobada de la imagen oficial `cloudflare/cloudflared` por digest.

No se incluyen digests inventados ni se utiliza `latest` dentro del stack. Define valores reales, por ejemplo con esta forma:

```text
LAB_WEB_IMAGE=registro/organizacion/term-web@sha256:DIGEST_REAL
LAB_TOOLBOX_IMAGE=registro/organizacion/term-toolbox@sha256:DIGEST_REAL
LAB_CLOUDFLARED_IMAGE=cloudflare/cloudflared@sha256:DIGEST_REAL
LAB_STUDENT_ID=a01
LAB_TUNNEL_CONFIG=term-a01-cloudflared-v1
LAB_TUNNEL_SECRET=term-a01-tunnel-v1
```

Introduce esos valores en un entorno de despliegue privado y exporta las variables. Las palabras `DIGEST_REAL` son marcadores explicativos y no referencias ejecutables. Los nombres de configuración y secretos no contienen el valor secreto.

## 2. Preparar ubicación, config y secret

En el manager administrativo del laboratorio, etiqueta la VM asignada:

```bash
docker node update --label-add smartkea.term.student=a01 NODO_ASIGNADO_A01
```

Crea primero Access para el hostname exacto, tal como indica [CONEXION-TTYD.md](CONEXION-TTYD.md). Crea un Tunnel específico y guarda su JSON de credenciales fuera del repositorio. Adapta `labs/config/cloudflared.swarm.example.yml` en una ruta privada; contiene el UUID, hostname y Audience, y lee la credencial de `/run/secrets/lab_tunnel_credentials.json`.

```bash
docker config create term-a01-cloudflared-v1 /RUTA_PRIVADA/cloudflared-a01.yml
docker secret create term-a01-tunnel-v1 /RUTA_PRIVADA/UUID_REAL.json
```

Los secretos se entregan solamente a cloudflared con UID/GID 65532 y modo 0400. Docker los distribuye mediante sus mecanismos de Swarm; no se montan en el terminal ni en HTTP [S14]. Las configuraciones son distintas de los secretos: evita meter credenciales dentro de `docker config`.

## 3. Validar, desplegar lectura y establecer límites

Tras exportar los valores reales:

```bash
docker stack config -c labs/stack.yaml > /tmp/term-a01-stack-reviewed.yaml
docker stack deploy --with-registry-auth -c labs/stack.yaml term-a01
labs/scripts/swarm-limits.sh term-a01
docker stack services term-a01
docker stack ps --no-trunc term-a01
docker service inspect term-a01_terminal --format '{{json .Endpoint.Spec.Ports}}'
docker service inspect term-a01_terminal --format '{{json .Spec.TaskTemplate.Resources.Limits}}'
```

El campo de puertos debe estar vacío y el límite `Pids` debe ser 128. `swarm-limits.sh` aplica límites de procesos e init con las opciones oficiales `docker service update --limit-pids` y `--init` [S15]. Se usa este paso explícito porque el esquema que procesa `docker stack` no es idéntico al de Compose. Repite el script después de cada despliegue y verifica el resultado antes de habilitar acceso a alumnos.

Los servicios del stack tienen límites y reservas de CPU/memoria. Las imágenes HTTP y ttyd activan `no_new_privs` en su propio proceso de arranque; no se declara un `security_opt` que algunas versiones de `docker stack` ignoran. El daemon conserva su perfil seccomp predeterminado. Confirma el resultado real en el nodo con `docker inspect` y `/proc/1/status` antes de utilizarlo como control evaluado.

En el nodo de esa VM, el administrador puede localizar el contenedor de la terminal mediante la etiqueta de servicio:

```bash
TERM_CONTAINER=$(docker ps --filter label=com.docker.swarm.service.name=term-a01_terminal --format '{{.ID}}')
test -n "$TERM_CONTAINER"
docker exec "$TERM_CONTAINER" sh -c 'id; awk "/NoNewPrivs/{print}" /proc/1/status; test ! -S /var/run/docker.sock'
```

Debes observar UID 10001, `NoNewPrivs: 1` y ausencia del socket Docker. Comprueba además que la memoria y procesos de la VM completa quedan limitados por el hipervisor. No concedas capacidad para manipular el daemon compartido a quien se pretende aislar con contenedores.

Las redes `lab` y `terminal_origin` son internas y usan cifrado overlay. La red `tunnel_egress` permite salir al conector. Aplica las reglas de Swarm exclusivamente entre nodos confiables y controla la salida del conector mediante la política de tu red; no abras las interfaces de gestión de Swarm hacia Internet [S13].

## 4. Habilitar escritura cuando el recorrido esté validado

Verifica autenticación, origen, WebSocket y separación de alumnos con el modo lectura. Después aplica el overlay de escritura y reaplica límites antes de conceder acceso:

```bash
docker stack deploy --with-registry-auth -c labs/stack.yaml -c labs/stack.writable.yaml term-a01
labs/scripts/swarm-limits.sh term-a01
docker service inspect term-a01_terminal --format '{{json .Spec.TaskTemplate.ContainerSpec.Args}}'
docker service inspect term-a01_terminal --format '{{json .Spec.TaskTemplate.Resources.Limits}}'
```

Usa una ventana de cambio en la que solo acceda el instructor, porque el redeploy puede restablecer propiedades aplicadas con `service update`. Después valida que la escritura ocurre únicamente en la VM y usuario asignados.

## 5. Operación y recuperación

Conserva un volumen local por alumno y la restricción de nodo: ese volumen no migra mágicamente al mover una tarea a otra VM. Una VM perdida requiere restaurar su backup o reiniciar la práctica desde una base limpia. Para una clase es preferible explicar esta propiedad que simular alta disponibilidad que no existe.

Observa `docker service logs` para salud y errores del Tunnel, evitando registrar credenciales o contenido de terminales. Cada conector debe tener su propio secret versionado para poder rotarlo. Cerrar una sesión de Access no debe ser el único mecanismo para finalizar procesos ya conectados: al terminar el laboratorio para la terminal o retira la VM según la política de clase.

`docker stack rm term-a01` retira los servicios del stack. La gestión de los volúmenes, configs y secrets se hace deliberadamente después de conservar las evidencias necesarias. Ningún comando del curso elimina todo el Swarm ni purga los recursos de otras prácticas.

Consulta [VALIDATION.md](VALIDATION.md) para distinguir las comprobaciones estáticas ejecutadas de las pruebas que requieren Engine, un manager Swarm y credenciales reales. Fuentes: [SOURCES.md](SOURCES.md).
