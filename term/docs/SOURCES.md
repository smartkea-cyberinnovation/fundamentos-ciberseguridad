# Fuentes primarias y decisiones técnicas

Documentación consultada el **7 de octubre de 2026**. Los enlaces sustentan comportamiento de productos; los presupuestos de recursos, tiempos de clase y decisiones de arquitectura son propuestas de este curso.

| ID | Fuente oficial | Uso en el módulo |
| --- | --- | --- |
| S1 | [Kali: imágenes oficiales Docker](https://www.kali.org/docs/containers/official-kalilinux-docker-images/) | Kali rolling como base; selección explícita de herramientas |
| S2 | [Docker Engine: instalación](https://docs.docker.com/engine/install/), [concepto de contenedor](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) | Instalación por distribución y Linux containers |
| S3 | [Docker: definición de redes](https://docs.docker.com/reference/cli/docker/network/create/) | Red interna del laboratorio |
| S4 | [Docker: tareas posteriores a la instalación](https://docs.docker.com/engine/install/linux-postinstall/) | Alcance de los permisos del grupo docker |
| S5 | [ttyd upstream: opciones](https://github.com/tsl0922/ttyd), [release 1.7.7](https://github.com/tsl0922/ttyd/releases/tag/1.7.7), [commit fijado](https://github.com/tsl0922/ttyd/commit/40e79c706be14029b391f369bee6613c31667abb) | `--writable`, `--check-origin`, `--max-clients` y código fuente de compilación |
| S6 | [Kernel Linux: no_new_privs](https://docs.kernel.org/userspace-api/no_new_privs.html) | Bit heredable y sin reversión antes de exec |
| S7 | [Docker: publicación de puertos](https://docs.docker.com/engine/network/port-publishing/) | Binding local en Compose y exposición de puertos en Swarm |
| S8 | [Cloudflare: aplicación self-hosted con Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/) | Crear Access antes de exponer el origen y validar tokens |
| S9 | [Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/) | Conexiones salientes desde la VM |
| S10 | [Cloudflare: parámetros del origen](https://developers.cloudflare.com/tunnel/reference/origin-parameters/) | Host header y validación de Audience mediante `originRequest.access` |
| S11 | [Cloudflare: túnel administrado localmente](https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/create-local-tunnel/) | Alta del conector, configuración y servicio |
| S12 | [Docker: desplegar un stack](https://docs.docker.com/engine/swarm/stack-deploy/) | Imágenes preconstruidas y formato de stack |
| S13 | [Docker: redes Swarm](https://docs.docker.com/engine/swarm/networking/), [overlay](https://docs.docker.com/engine/network/drivers/overlay/) | Redes privadas, DNSRR y cifrado overlay |
| S14 | [Docker: secretos Swarm](https://docs.docker.com/engine/swarm/secrets/) | Distribución de credenciales solo al servicio autorizado |
| S15 | [Docker: actualizar servicio](https://docs.docker.com/reference/cli/docker/service/update/) | `--limit-pids` y `--init` como configuración efectiva del servicio |
| S16 | [tmux: introducción oficial](https://github.com/tmux/tmux/wiki/Getting-Started), [manual upstream](https://github.com/tmux/tmux/blob/master/tmux.1) | Sesiones persistentes y cliente de observación en lectura |
| S17 | [Python: http.server](https://docs.python.org/3/library/http.server.html) | Uso de servidor estándar limitado al entorno de enseñanza |
| S18 | [Cloudflared: notas oficiales de release](https://github.com/cloudflare/cloudflared/blob/master/RELEASE_NOTES) | Disponibilidad del subcomando de comprobación `tunnel ready` |
| S19 | [Nginx: proxy WebSocket](https://nginx.org/en/docs/http/websocket.html) | Upgrade y proxy local opcional para incrustación |
| S20 | [ttyd: issue upstream #1566](https://github.com/tsl0922/ttyd/issues/1566) | Reporte abierto sobre check-origin y HTTP/2 directo; arquitectura con HTTP/1.1 hacia ttyd |

## Elecciones que requieren verificación operativa

Las bases Kali y Python de desarrollo no fijan un digest por defecto. La publicación de una clase congela los digests finales tras construir, escanear y probar. El inventario de paquetes permite explicar la versión utilizada, pero no sustituye la conservación de esa imagen final.

El tracker público de Kali consultado para `ttyd` no mostró un candidato verificable. Por eso el Dockerfile compila el código upstream fijado y obtiene de `dpkg-shlibdeps` los nombres de bibliotecas necesarios para esa ABI. Las opciones se verifican durante el build y el arranque. No se ha supuesto que la versión de un paquete de otra distribución funcione igual.

Las guías de Access y Tunnel definen el control que debe configurarse; el repositorio no contiene credenciales ni evidencia de que la zona de dominio, el proveedor de identidad o las VMs estén ya creados. La validación real debe incluir identidades autorizadas y denegadas, las cabeceras del WebSocket y la separación de trabajo entre VMs.
