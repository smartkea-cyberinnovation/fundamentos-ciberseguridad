# Seguridad del curso y del laboratorio

## Modelo de confianza

TERM es una aplicación estática de aprendizaje. No ofrece una API que ejecute comandos, no ingesta transcripciones de ttyd y no acepta tokens de acceso en formularios. Las demostraciones son textos orientativos; la ejecución real ocurre en una VM asignada.

El contenido del repositorio es código revisado. Las notas y ficheros de progreso importados son entradas no confiables: se validan, se limitan y se muestran como texto. La importación solicita revisar una sustitución antes de modificar el progreso local.

## Controles de la web

- Scripts y estilos propios, sin dependencias de runtime ni recursos de terceros.
- CSP sin `unsafe-inline` ni `unsafe-eval`, con scripts/estilos del mismo origen.
- `frame-src 'none'` por defecto; la incrustación requiere una lista exacta de orígenes HTTPS.
- `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'none'` y `nosniff`.
- URL ttyd validada en build y comprobada de nuevo en cliente; sin credenciales, query ni fragmentos.
- No se permite reutilizar el origen del campus como terminal incrustada.
- Notas limitadas por lección e importación limitada a 2 MB, sin ejecución de HTML o comandos.
- Inventario explícito de descargas; no se empaquetan carpetas locales, volúmenes o secretos.

## Controles del laboratorio

Una VM por alumno es la opción prevista para tareas administrativas. Access controla quién llega a cada endpoint; Linux controla usuario, archivos y privilegios. Deben funcionar ambas capas.

Los perfiles ttyd distinguen lectura y escritura. Se usan usuario no root, capacidades reducidas, límites, filesystem restringido y puertos solo loopback en el laboratorio local. Swarm no publica los puertos de terminal mediante ingress; se accede por la ruta interna prevista y Tunnel.

Nunca se entrega el socket del daemon Docker a la shell web ni se usan montajes del anfitrión para darle privilegios. Si el alumno necesita Docker o sudo, usa su VM. Un usuario con permiso sobre Docker en el anfitrión debe tratarse como altamente privilegiado.

## Acceso del docente

La observación compartida está limitada a una sesión didáctica con participantes conocidos. Documenta cuenta, VM, objetivo, duración y quién escribe. El modo lectura evita entrada por esa conexión, pero no establece separación entre usuarios del sistema ni entre procesos que comparten archivos.

## Evidencias y datos

Usar datos sintéticos en ejercicios y notas. Mantener originales y copias derivadas, registrar hash, hora y procedencia. Un hash no acredita por sí solo autoría, momento de adquisición o integridad de toda la cadena. La verificación de un control no demuestra ausencia de toda vulnerabilidad.

Las notas locales pueden contener información que el alumno escriba. La exportación las incluye; revisar el fichero antes de compartirlo. El campus no añade analítica ni sincronización de esas notas.

## Notificar un problema

Para errores de contenido o interfaz, abrir una incidencia del repositorio sin información sensible. Para una exposición real del laboratorio, detener la sesión afectada, conservar la evidencia necesaria y comunicarla al operador por el canal acordado de la organización. Evitar publicar secretos en issues o capturas.

## Fuentes primarias

- [Seguridad de Docker Engine](https://docs.docker.com/engine/security/).
- [ttyd](https://github.com/tsl0922/ttyd).
- [Cloudflare Access con aplicaciones self-hosted](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/).
- [CSP de recursos estáticos](https://developers.cloudflare.com/workers/static-assets/headers/).
