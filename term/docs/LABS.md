# Laboratorios: terminal, Kali, HTTP y Docker

## 1. Qué vas a aprender y dónde se ejecuta cada comando

Hay dos espacios de trabajo. **La terminal del anfitrión** es una VM Linux dedicada a un alumno; desde ella se administran Docker, usuarios, paquetes y servicios. **La terminal Kali del contenedor** permite practicar Bash, ficheros, red, evidencias y reconocimiento del servicio `web`. Mantén claro el espacio antes de copiar un comando: `id`, `pwd` y `/etc/os-release` te ayudan a identificarlo.

| Componente | Función | Acceso inicial |
| --- | --- | --- |
| `web` | HTTP con datos sintéticos, sin subida de ficheros ni ejecución de comandos | `http://web:8080` desde Kali |
| `toolbox` | Kali minimal, Bash y herramientas seleccionadas | `docker compose run --rm toolbox` |
| `terminal` | Panel ttyd de observación de su propio contenedor | Perfil opcional, `127.0.0.1:7681`, lectura |
| `terminal-write` | Bash interactivo del contenedor | Perfil opcional y explícito, mismo puerto local |
| `web-local` | Segunda instancia HTTP para estudiar el navegador del anfitrión | Perfil opcional, `127.0.0.1:8088` |
| `learner_workspace` | Volumen persistente de una persona | `/workspace` |

La imagen Kali oficial es una base, no una instalación completa con todas las herramientas. El Dockerfile instala únicamente el conjunto necesario para estas prácticas. Un contenedor comparte el kernel del anfitrión; para ejercicios de administración y separación de alumnos utilizamos VMs dedicadas [S1, S2].

## 2. Requisitos y preparación

Necesitas Docker Engine con Compose v2 en una VM Linux o Docker Desktop para las prácticas sin administración del anfitrión. Reserva inicialmente 2 CPU, 4 GB de RAM y 15 GB de disco como presupuesto de clase; es una propuesta de dimensionamiento que debes ajustar a tus imágenes, retención y número de laboratorios. La construcción descarga imágenes y paquetes. En ejecución, la red de prácticas está declarada `internal: true` [S3].

Instala Docker siguiendo la documentación oficial para tu distribución [S2]; evita ejecutar instaladores copiados sin revisar. Antes de empezar, en el anfitrión:

```bash
docker version
docker compose version
docker info
```

Los miembros del grupo `docker` pueden controlar el daemon, lo que normalmente permite obtener privilegios equivalentes a root sobre ese anfitrión [S4]. En clase se concede ese control exclusivamente sobre la VM del alumno.

Todos los comandos siguientes se lanzan **desde la carpeta del módulo que contiene `labs/`**, salvo que se indique que van dentro de Kali.

```bash
docker compose -f labs/compose.yaml config --quiet
docker compose -f labs/compose.yaml build web toolbox
docker compose -f labs/compose.yaml up -d --wait web
docker compose -f labs/compose.yaml ps
docker compose -f labs/compose.yaml run --rm toolbox
```

Si otra práctica ya ocupa los puertos locales, compruébalo con `ss -lnt` y utiliza una VM diferente o para el servicio que ya conoces. No cambies el binding a `0.0.0.0` para resolver una colisión.

## 3. Primer recorrido dentro de Kali

```bash
id
pwd
cat /etc/os-release
printf 'Hola, terminal\n'
mkdir -p /workspace/notas
printf 'Primera evidencia\n' > /workspace/notas/inicio.txt
ls -la /workspace/notas
cat /workspace/notas/inicio.txt
```

El usuario es `learner`, UID/GID `10001:10001`. El sistema de ficheros de la imagen es de solo lectura. `/workspace` es escribible y persiste entre sesiones; `/tmp` y el home temporal del contenedor Compose se descartan al recrearlo. El volumen se inicializa con el propietario definido en la imagen. Si reutilizas un volumen antiguo con otro UID, crea un proyecto nuevo o migra su propiedad bajo supervisión; el contenedor nunca intenta arreglarla ejecutándose como root.

Herramientas incluidas: Bash, Dash, Coreutils, Findutils, `grep`, `sed`, `gawk`, `less`, `nano`, `vim-tiny`, manuales básicos, `ps`, `free`, `ip`, `ss`, `ping`, `dig`, `curl`, `wget`, `jq`, `file`, `tar`, gzip/zip, OpenSSL, Git, cliente OpenSSH, Netcat, Nmap, Python, ShellCheck, tmux y ttyd. La imagen guarda el inventario real de versiones en `/opt/lab/packages.tsv`.

`ping` y las técnicas con sockets raw pueden no estar disponibles debido a las capabilities eliminadas. Practicamos Nmap con conexiones TCP (`-sT`). La resolución DNS interna de Docker permite consultar `web`; no interpretes `internal: true` como un sandbox perfecto contra un usuario con acceso al daemon o contra fallos del kernel.

## 4. HTTP: petición, respuesta y evidencia

Dentro de Kali:

```bash
curl --fail --silent --show-error http://web:8080/health | jq
curl --head http://web:8080/
curl --include http://web:8080/robots.txt
curl --include http://web:8080/no-existe
curl --fail --silent --show-error http://web:8080/catalog.json | jq '.items[] | {id,name}'
nmap -sT -Pn -sV --version-light --max-retries 1 --host-timeout 20s -p 8080 web
```

`/health` devuelve `{"status":"ok","service":"smartkea-lab-web","synthetic":true}`. GET y HEAD están disponibles. Las rutas desconocidas responden 404 y los métodos de modificación implementados responden 405. `robots.txt` menciona `/training-only` para explicar que las instrucciones a rastreadores no son controles de acceso; esa ruta responde 404.

El servidor utiliza la biblioteca estándar de Python dentro de una red de enseñanza. No se presenta como servidor de producción ni como máquina deliberadamente vulnerable. Solo ofrece recursos estáticos definidos en el código: no lee rutas del sistema ni tiene mecanismos de carga o ejecución. Limita conexiones concurrentes y tiempos de espera; el contenedor añade memoria, CPU y procesos limitados.

En el anfitrión, crea la evidencia sin mezclarla con credenciales:

```bash
umask 077
mkdir -p evidencia-http
docker compose -f labs/compose.yaml logs --no-color --no-log-prefix --since 5m web > evidencia-http/web.jsonl
jq -s '[.[] | select(.event == "http_request")] | group_by(.status) | map({status: .[0].status, count: length})' evidencia-http/web.jsonl
```

Los eventos `http_request` incluyen `timestamp`, `client`, `method`, `path`, `status` y `synthetic_service`. La primera línea de inicio es `event=ready`; fíltrala antes de contar peticiones. Las consultas URL, cabeceras y cuerpos de petición no se registran. `docker compose logs` necesita `--no-log-prefix` para que cada línea siga siendo JSON válido.

## 5. Prácticas de logs y Bash sin datos reales

Dentro de Kali:

```bash
/opt/lab/bin/make-fixtures.sh /workspace/evidence-synthetic
find /workspace/evidence-synthetic -type f
awk '{print $9}' /workspace/evidence-synthetic/logs/access.log | sort | uniq -c
rg --version 2>/dev/null || grep --version | head -n 1
grep -n 'Failed publickey' /workspace/evidence-synthetic/logs/auth-synthetic.log
/opt/lab/bin/verify-evidence.sh /workspace/evidence-synthetic
/opt/lab/bin/diagnose.sh > /workspace/diagnostic.txt
```

El generador rechaza destinos ya existentes y enlaces simbólicos en el destino para no sobrescribir trabajo. Las IP de los logs pertenecen a rangos de documentación y no son objetivos para escanear. El verificador admite exactamente los tres ficheros generados, rechaza rutas arbitrarias y confirma que sus bytes coinciden con el manifiesto. Un hash demuestra correspondencia con una referencia; no identifica por sí mismo al autor ni demuestra que la referencia sea fiable.

Reto de modificación controlada: cambia una palabra en `logs/access.log`, verifica de nuevo y explica por qué falla. Crea una nueva carpeta con el generador para repetir la práctica conservando ambas evidencias.

## 6. Terminal web local

Primero inicia la vista de observación:

```bash
docker compose -f labs/compose.yaml --profile terminal up -d web terminal
```

Abre `http://127.0.0.1:7681/` **en la misma máquina**. El panel representa actividad real de su contenedor y no muestra la shell de otra persona. La opción `--writable` de ttyd se omite, y `--check-origin` está activada [S5]. La conexión admite un solo cliente para evitar confundir múltiples sesiones.

Para practicar escribiendo, cambia explícitamente el perfil:

```bash
docker compose -f labs/compose.yaml --profile terminal stop terminal
docker compose -f labs/compose.yaml --profile terminal-write up -d web terminal-write
```

El puerto es el mismo a propósito: nunca hay dos modos simultáneos en esa dirección. `terminal-write` abre Bash como `learner`, con rootfs de lectura, sin `sudo`, sin Docker daemon, sin socket del anfitrión y sin red host. El launcher rechaza root, argumentos adicionales y modos desconocidos; fija el comando que ejecuta ttyd, activa la comprobación de origen y no permite argumentos recibidos desde la URL. Además activa `no_new_privs` a nivel de proceso antes de abrir ttyd, de forma heredable por sus shells [S6].

La comprobación de salud de ttyd confirma que el listener TCP responde. Las verificaciones de HTTP, Access, WebSocket y aislamiento se realizan en la guía de conexión: un listener vivo no acredita por sí solo todo el recorrido del navegador.

## 7. Acceso al HTTP desde el navegador local

```bash
docker compose -f labs/compose.yaml --profile web-local up -d web-local
curl --fail http://127.0.0.1:8088/health
```

Abre `http://127.0.0.1:8088/`. Es otra instancia del mismo servidor y genera sus propios logs; para estudiar tráfico entre contenedores sigue utilizando `web:8080`. Docker documenta limitaciones históricas del aislamiento de puertos ligados a localhost en versiones anteriores a Engine 28; usa un Engine actualizado [S7].

## 8. Persistencia, reinicio y limpieza

Salir de Bash con `exit` elimina la instancia temporal de `toolbox`, pero mantiene el volumen. Parar los servicios conserva el trabajo:

```bash
docker compose -f labs/compose.yaml --profile terminal --profile terminal-write --profile web-local down
```

Para exportar una copia antes de reiniciar la práctica, desde el anfitrión:

```bash
umask 077
docker compose -f labs/compose.yaml run --rm --no-deps -T toolbox tar -C /workspace -czf - . > workspace-backup.tar.gz
tar -tzf workspace-backup.tar.gz | head
```

El backup puede contener tus notas e historial. Revisa su contenido antes de compartirlo. El borrado permanente del trabajo se hace con `down --volumes`, **solo cuando hayas decidido descartar los volúmenes de ese proyecto**. El curso no lo ejecuta automáticamente.

Para varios ejercicios locales puedes definir `--project-name alumno-a01`; los nombres de volumen y red quedan separados por proyecto. Esto organiza contenedores, pero no sustituye VMs para alumnos que tienen acceso administrativo al daemon.

## 9. Imágenes, versiones y comprobaciones

El código de ttyd está fijado al commit oficial `40e79c706be14029b391f369bee6613c31667abb`, release 1.7.7. Se compila porque la consulta al tracker de Kali no ofrecía un candidato de paquete verificable. Se comprueba en construcción y arranque que existen `--writable` y `--check-origin`; no se asume que una versión antigua disponga de ellos [S5].

Las referencias predeterminadas de Kali y Python permiten construir con actualizaciones del proveedor, por lo que no representan una reconstrucción bit a bit. Para preparar una entrega controlada:

```bash
umask 077
labs/scripts/lock-images.sh > labs/base-images.lock.env
docker compose --env-file labs/base-images.lock.env -f labs/compose.yaml build --pull web toolbox
docker compose -f labs/compose.yaml run --rm --no-deps -T toolbox cat /opt/lab/packages.tsv > packages-build.tsv
```

Conserva el commit del curso, los digests de las bases, el inventario de paquetes y los digests finales del registro. Kali rolling y sus repositorios de paquetes evolucionan; para repetir exactamente una entrega utiliza la imagen final previamente construida y fijada por digest. Un manifiesto de versiones no congela por sí solo el repositorio APT.

Pruebas locales con Docker, cuando esté disponible:

```bash
labs/scripts/smoke.sh
```

La prueba utiliza un proyecto temporal con nombre propio, construye las imágenes, consulta HTTP, verifica UID y filesystem, hace un reconocimiento TCP del único puerto de `web`, genera evidencias y comprueba `no_new_privs`. Limpia únicamente sus contenedores y volúmenes temporales al terminar. Para las pruebas sin daemon, consulta [VALIDATION.md](VALIDATION.md).

Las referencias `[Sx]` se resuelven en [SOURCES.md](SOURCES.md).
