# Notas de integración de m09–m16

## Entregable

`security.json` contiene exactamente `{ "modules": [...] }`, con 8 módulos, 24 lecciones, 98 pasos y 48 preguntas. Tiempo orientativo: 1.355 minutos (22 h 35 min), incluyendo retos y proyecto. Cada lección incluye objetivos, prerrequisitos, 3–4 secciones sustanciales, 4–5 pasos completos, reto resuelto con rúbrica, 2 preguntas, 3 conclusiones y fuentes oficiales enlazadas. El texto explicativo sin bloques de comando supera las 850 palabras por lección; las posiciones correctas del test están equilibradas (12 por índice).

`build_security.py` conserva el contenido original editable. Regenera el JSON con `python3 term-staging/build_security.py`. Solo `security.json` es necesario para la aplicación; el generador, estadísticas y verificador son auxiliares de autoría.

## Contrato acordado con lab_platform

- Ejecución desde la raíz `term/`: `docker compose -f labs/compose.yaml ...`.
- `web` responde en `http://web:8080` dentro de la red del laboratorio. Construcción inicial: `docker compose -f labs/compose.yaml build web toolbox`.
- `toolbox` admite `run --rm --no-deps -T toolbox COMANDO`; usa UID/GID 10001, no tiene sudo ni acceso al socket Docker, y conserva trabajo en `/workspace` mediante volumen del proyecto.
- `/health`: `{"status":"ok","service":"smartkea-lab-web","synthetic":true}`; también se utilizan `/`, `/robots.txt`, `/catalog.json`, `/no-existe` y `/training-only` (las dos últimas devuelven 404). GET y HEAD están previstos.
- `web-local`, perfil `web-local`, publica únicamente `127.0.0.1:8088` en la VM. Se utiliza en bastionado y en el proyecto final; es una instancia distinta de `web`.
- Logs HTTP JSON por stdout con `timestamp`, `event=http_request`, `client`, `method`, `path`, `status`, `synthetic_service`; el evento inicial `ready` carece de campos de petición. Las lecciones no asumen que todas las líneas representan solicitudes del alumno: el healthcheck añade registros.
- Swarm usa `labs/stack.yaml` y `labs/stack.writable.yaml`. El curso distingue el stack completo de una muestra que solo se valida con `docker stack config`.

## Decisiones pedagógicas y técnicas

- Todos los objetivos de reconocimiento son localhost o servicios propios de Compose. No se examina smartkea.com ni ninguna dirección externa.
- Las descargas al preparar imágenes/paquetes se distinguen del alcance del reconocimiento.
- Nmap usa TCP connect (`-sT`), puertos explícitos, `-Pn`, `-n` y límites temporales. No se necesitan paquetes raw ni exploraciones agresivas para los objetivos del curso.
- La captura de paquetes tiene lugar en loopback de la VM propia, con contenido sintético, filtro, tiempo máximo y snaplen declarado; no se conceden capacidades de captura a toolbox.
- TLS se demuestra con un certificado efímero SAN localhost/127.0.0.1 y `--cacert`, conservando verificación; no se enseña `-k` como solución.
- SSH se valida con un candidato fuera de `/etc/ssh`, `sshd -t` y `sshd -T -C`. Se explican consola, dos sesiones, comprobación de autenticación y reversión antes de aplicar cualquier cambio real.
- nftables usa `-c` y una cadena ordinaria sin hook para demostrar validación sin modificar ni conectar una política de tráfico. Se explica la diferencia entre validar y probar filtrado efectivo.
- Se separan imagen/contenedor/proceso, usuario del contenedor/modo del daemon, salud/reinicio, dependencia de arranque/recuperación continua, volumen/copia de seguridad y hash/autenticidad.
- Kali contempla fuentes actuales deb822 (`kali.sources`) y `sources.list` heredado. No mezcla repositorios de distribuciones.
- El script final se genera como sh, tiene dos URL locales permitidas, límites de duración y tamaño, temporales privados, limpieza precisa, comprobación de HTTP y de JSON, y estados 0/2/3/4/64 documentados.
- Las dos pruebas de incidente se distinguen: dataset inventado con fechas explícitas y ensayo real de parar/recuperar el servicio didáctico. Ninguno se presenta como incidente de un tercero.

## Validación realizada

`security-validation.json` contiene los resultados de `verify_security_material.py`:

- 158 comprobaciones correctas.
- 98 bloques de comando validados con la shell declarada; 11 comandos de shell anidados validados adicionalmente.
- Script sh exacto de la lección probado contra el manejador HTTP real de `labs/web/app.py` servido solo en loopback: éxito 0, 404 → 2, entrada inválida → 64, contrato JSON incorrecto → 2 y servicio detenido → 3.
- Filtro curl/jq anidado de la lección web ejecutado correctamente, adaptando únicamente URL al loopback de prueba y ruta temporal.
- Comandos exactos del caso TSV ejecutados con rutas temporales: seis campos por fila, nueve eventos, dos respuestas 200 y dos 503, manifiesto SHA-256 conservado y comprobado.
- Certificado OpenSSL creado: SAN esperado, rechazo con confianza predeterminada (curl 60) y éxito con CA explícita, sin desactivar comprobación.

Límites de esta validación: el entorno no dispone de Docker Engine/Compose ni de ShellCheck. No se ejecutaron contenedores, Swarm, cambios de servicio SSH ni reglas del firewall del host. Esas pruebas corresponden al procedimiento y CI de la plataforma; las lecciones no afirman que se hayan desplegado en el entorno del autor. El manejador HTTP se usó directamente en una prueba local y no acredita los controles de un contenedor.

## Fuentes primarias consultadas

El JSON enlaza las fuentes concretas por lección. La documentación se consultó el 7 de octubre de 2026; las opciones usadas se han contrastado con fuentes oficiales, no con recetas de terceros. Referencias principales:

- Kali: repositorios, imágenes oficiales y usuario ordinario, `kali.org/docs` y `kali.org/blog/kali-default-non-root-user/`.
- Docker: ejecución, seguridad, rootless, puertos, volúmenes, Compose config/run/up, dependencias, secretos, Swarm y stack config, `docs.docker.com`.
- Nmap: técnicas, puertos y salida, `nmap.org/book`.
- curl y OpenSSL: opciones, certificados, req y s_server, `curl.se/docs` y `docs.openssl.org`.
- OpenSSH: manuales upstream de sshd y sshd_config, `man.openbsd.org`.
- nftables: manual del proyecto, `netfilter.org/projects/nftables/manpage.html`.
- systemd: documentación y manual original en su repositorio; para journalctl, la página oficial de la versión 255 cubre las opciones usadas.
- GNU: Coreutils, SHA-2 y Bash; jq y ShellCheck en sus sitios/repositorios originales.
- OWASP: WSTG 4.2 para inventario de puntos de entrada y Logging Cheat Sheet para registro útil y minimizado.
- Linux man-pages/iproute2 y manuales distribuidos por Debian para getent, ip, ss y tcpdump.

No se han copiado párrafos de las fuentes: teoría, ejercicios, datos sintéticos, retos y soluciones son redacción original.
