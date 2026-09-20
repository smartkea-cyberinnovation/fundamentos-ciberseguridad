# R06 · Operar y observar una web local

**L25A · 3 h.** Entrada: M24 y preparación de M25. [Lección 05](../lecciones/05-servicios.md). El servicio es exclusivamente docente: HTTP, sin autenticación/TLS, sin datos reales y sin publicación exterior.

## Ejecución sin Docker

1. Desde la raíz del curso, ejecuta `python3 kit/web.py`. El listener por defecto es `127.0.0.1:8080`.
2. Abre la página en el navegador y consulta el endpoint con `curl --fail --silent --show-error http://127.0.0.1:8080/healthz`. En Windows, `curl.exe` evita ambigüedades de alias.
3. Comprueba el cuerpo `{"status":"ok","synthetic":true}` y las cabeceras con `curl -I http://127.0.0.1:8080/healthz`.
4. Consulta `http://127.0.0.1:8080/no-existe`. Debe devolver 404. Explica por qué existe conectividad aunque esa ruta falle.
5. Observa el log JSON de la terminal y asocia respuesta y estado. Comprueba que no incluye query strings ni datos de cliente.
6. Ejecuta `python3 -m unittest discover -s kit -p test_web.py -v`. Los tests levantan y cierran su propio servidor local, separado del servidor manual.

## Variante Compose

En host de laboratorio con Docker, sigue [las instrucciones del kit](../kit/README.md). Distingue puerto 18080 del anfitrión y 8080 del contenedor; interpreta `USER`, filesystem de solo lectura, red interna y health check. Valida con `docker compose config` antes de arrancar. No se monta el socket Docker ni se usa modo privilegiado.

## Variante Swarm de análisis

Revisa `swarm.yaml`: imagen previamente distribuida y ausencia de puertos publicados. Explica cómo comprobaría el docente el servicio desde un cliente autorizado en la red overlay y cómo retiraría solo el stack. No inventes un digest ni inicialices un clúster de producción para completar el ejercicio. La variante Swarm es una extensión opcional dentro del tiempo disponible; su despliegue necesita validación nativa aparte.

## Evidencia y criterio

Entrega estado/cabeceras/cuerpo/log para 200 y 404; diagrama de puertos; interpretación del health check y riesgo residual. Éxito: separar proceso, listener, HTTP y aplicación. No se permite presentar este ejemplo como servidor de producción o laboratorio TLS terminado.

## Cierre

Detén el servidor con Ctrl+C y comprueba que deja de responder. En Compose utiliza `docker compose down` sobre este proyecto, sin borrar volúmenes o recursos ajenos. **HTTP local probado; Docker/Swarm no ejecutados en el entorno de edición.**
