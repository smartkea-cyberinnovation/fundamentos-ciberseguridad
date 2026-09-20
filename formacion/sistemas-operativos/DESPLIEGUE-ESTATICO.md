# Del código al despliegue: sitio estático, Pages y Workers

**Aplicación de M25 y M26 · Actividad de consolidación, sin aumentar las 480 horas.**

## Objetivo

Distinguir el código fuente, la compilación, los activos publicados, la versión subida y el despliegue que sirve tráfico. Utilizar este campus como caso de administración: identificar exactamente qué aplicación se está publicando, comprobar su integridad y diagnosticar un error sin ampliar permisos ni instalar componentes innecesarios.

El resultado es un paquete verificable y un registro de la prueba. No se considera publicado por terminar una compilación. La URL, el commit y la respuesta HTTP deben corresponder a la misma entrega.

## El modelo de ejecución

El repositorio original contenía dos aplicaciones independientes; este repositorio conserva el campus estático y los materiales docentes. `campus/` transforma el temario Markdown y el catálogo curricular en HTML, CSS, JavaScript y JSON. El navegador presenta el contenido y conserva el progreso local. La aplicación Next.js de `src/` permanece en el repositorio original: su directorio `.next` no es la salida del curso.

Python se ejecuta **durante la compilación**, no como servidor de producción del campus. El paquete generado está en `campus/dist/`. El asistente de prácticas no ejecuta comandos del sistema: indica qué debe revisar y hacer manualmente el alumno en su laboratorio.

Cloudflare Pages puede alojar esos archivos. Workers Static Assets también puede servirlos sin un script de backend: la configuración declara el directorio `assets.directory`. No necesita Next.js, OpenNext, R2, una base de datos ni un servicio que se llame `frontend` para este campus. [Referencia oficial de activos](https://developers.cloudflare.com/workers/static-assets/binding/).

## Preparación: identificar antes de publicar

Trabaja desde una copia actual del repositorio. Comprueba rama y estado antes de actualizarla; no sobreescribas cambios locales. Anota el commit con `git rev-parse HEAD`. Python 3.11 o posterior basta para compilar; Node/npm se necesita únicamente cuando se utiliza Wrangler para previsualizar o publicar en Workers.

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
```

`plan` muestra los destinos y los argumentos previstos sin construir ni publicar. `build` construye y valida. Consulta `campus/dist/build-info.json`, `campus/dist/SHA256SUMS.txt` y el informe del validador. El manifiesto verifica contenido, no acredita por sí solo autoría o seguridad integral.

## Práctica: separar cada fase

**1. Compilar y comprobar.** La salida debe identificar 32 módulos, 96 fichas y 480 horas. Confirma la presencia de `index.html`, `course.json`, hojas de estilo, scripts y `404.html`. El ZIP y el directorio deben contener los mismos activos públicos.

**2. Previsualizar sin publicar.** Abre el campus con `python3 campus/serve.py --port 8788` y consulta el índice, M05, una práctica y una autoevaluación. Revisa una entrada inexistente. No uses `file://`: los módulos JavaScript y las peticiones de contenido necesitan un origen HTTP.

**3. Validar el adaptador de alojamiento.** `python3 campus/cloudflare.py dry-run` ejecuta Wrangler con la configuración estática y `--dry-run`. Puede descargar la versión fijada de la herramienta, pero no sube una versión ni configura una cuenta. El build y la validación se repiten antes del comando.

**4. Publicar solo en el proyecto autorizado.** Para el Worker ya creado, sigue la [guía de configuración](../../campus/DEPLOY-CLOUDFLARE.md). `deploy` publica producción; `preview` sube una versión de prueba sin promoverla a producción. No son intercambiables. Para Pages se usa el ZIP o la integración Git, no los comandos de versiones de Workers.

**5. Verificar lo que realmente sirve.** Abre la URL devuelta por el proveedor y `/build-info.json`; comprueba commit y contenido. Verifica el índice completo, los filtros, la presentación, el registro de una lectura y la recuperación del progreso tras recargar. Comprueba HTTP 404 en una ruta inexistente y la política CSP en respuestas estáticas. Conserva únicamente evidencia sin datos personales ni credenciales.

## Interpretar dos fallos sin confundirlos

`WORKER_SELF_REFERENCE references Worker frontend which was not found`: el paquete estaba intentando enlazar un servicio inexistente. En este caso la ruta de publicación había detectado la aplicación Next.js en vez del campus. No crear un Worker ficticio para esconder el síntoma: revisar aplicación, configuración y bindings.

`Missing entry-point to Worker script or to assets directory`: no había un script o directorio de activos definido en la configuración utilizada. En un sitio estático la respuesta es declarar y generar los activos, no inventar un backend.

Los avisos de instalación, los conflictos de dependencias y el error final se anotan por separado. Un aviso anterior no demuestra ser la causa del fallo. Una compilación de Next.js correcta tampoco demuestra que se haya compilado el curso esperado.

## Evidencias y criterio de éxito

Entregar commit de fuente, salida de build y validación, hash del ZIP, configuración sin secretos, proveedor y tipo de proyecto, versión subida, resultado HTTP, prueba positiva y negativa, y procedimiento de reversión. Una captura de la portada sin commit o comprobación de contenido es evidencia insuficiente de la versión desplegada.

Exporta el progreso antes de cambiar de dominio: el almacenamiento pertenece al origen del navegador. No copies notas personales a incidencias públicas. Ante un fallo, conserva el error minimizado, detén la promoción y vuelve a una versión conocida. No borres buckets o servicios existentes como parte automática de la recuperación.

## Lecturas de contraste

[Workers Builds: configuración y diferencia entre despliegue y preview](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/). [Cabeceras de activos estáticos](https://developers.cloudflare.com/workers/static-assets/headers/). [Versiones y despliegues](https://developers.cloudflare.com/workers/versions-and-deployments/). Consulta documental: 16 de septiembre de 2026. Las opciones del panel deben comprobarse en la cuenta donde se ejecute la prueba.
