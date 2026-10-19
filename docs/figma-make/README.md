# SmartKEA · Paquete para Figma Make

**Markdown y JSON completos para diseñar, montar y revisar mejoras del campus existente.** Versión 1.0.0, revisada el 2026-10-19. Repositorio: [fundamentos-ciberseguridad](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad).

## Empezar

Abre un archivo Make destinado a esta revisión. Adjunta `FIGMA-MAKE.md`, `producto.json`, `banco-preguntas.json` y `catalogo-publico.json`. Pega este texto:

> Sigue FIGMA-MAKE.md y producto.json. Trabaja sobre SmartKEA y los IDs, rutas, contenido y modelos existentes. Empieza por orientación, tokens y una lección real; continúa con práctica guiada y el examen completo de 100 preguntas, 20 por intento. Conserva la corrección inmediata, las claves de progreso y la arquitectura estática. Distingue lo existente de lo propuesto. Devuelve una versión revisable y cambios integrables mediante PR al repositorio canónico. La guía asistida es local; no añadas un backend de IA, datos personales ni ejecución de comandos.

Para la iteración de contenido largo, incorpora `muestras-contenido.json`; para validar los contratos, incorpora los dos esquemas. Trabaja pantalla por pantalla con el contenido real y comprueba la integración al final. Figma documenta archivos de texto/Markdown/JSON de hasta 1 MB y hasta 10 adjuntos por prompt; cada archivo de texto de este paquete queda por debajo de ese límite. [Documentación de adjuntos](https://help.figma.com/hc/en-us/articles/31304529835671-Attach-files-to-a-prompt-in-the-Figma-agent-and-Figma-Make).

## Archivos

| Archivo | Uso |
|---|---|
| [FIGMA-MAKE.md](FIGMA-MAKE.md) | Prompt maestro completo: producto, recorrido, pantallas, diseño, accesibilidad, datos, privacidad, implementación, despliegue y aceptación |
| [producto.json](producto.json) | Contrato versionado y procesable: instrucciones completas, estados, rutas, reglas, criterios de aceptación y backlog |
| [producto.schema.json](producto.schema.json) | Esquema del contrato y sus invariantes principales; requiere también validación de referencias cruzadas |
| `banco-preguntas.json` · export generado | Las 100 preguntas completas, copiadas exactamente de la [fuente editorial](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/formacion/introduccion-informatica/banco-preguntas.json) |
| `BANCO-100-PREGUNTAS.md` · export generado | Las 100 preguntas con cuatro opciones, respuesta correcta, explicación y enlace de estudio; legible sin aplicación |
| `APUNTES-D41-D46.md` · export generado | Seis lecturas completas en español, ejercicios y fuentes; generadas de los bloques ES y COMMON originales |
| [banco-preguntas.schema.json](banco-preguntas.schema.json) | Esquema 2020-12 y reglas semánticas adicionales del banco |
| `catalogo-publico.json` · export generado | Inventario completo de 32 módulos, 96 fichas, 46 recursos, 28 lecciones OS, 48 lecciones TERM, 12 temas del examen, seis rutas profesionales y 26 etapas, con IDs/títulos/rutas; ampliación C99-DFIR identificada por separado |
| `muestras-contenido.json` · export generado | Contenido completo real de M02, D41, OS-L01, m01-l01 y una pregunta para revisar composición y estados largos |
| [FUENTES.md](FUENTES.md) | Referencias públicas fijadas al snapshot y documentación oficial |
| [exportar.py](exportar.py) | Generador reproducible de banco, apuntes, inventario, muestras y manifiesto; solo biblioteca estándar de Python |
| `manifest.json` · export generado | Versión, procedencia, tamaños y huellas SHA-256 del paquete |
| `validacion.json` · export generado | Comprobaciones realmente ejecutadas sobre los archivos de la entrega |

El JSON de producto incluye también el texto íntegro del prompt maestro. Los archivos cumplen funciones distintas: el contrato especifica comportamiento; el catálogo inventaría unidades; las muestras permiten componer pantallas reales; el banco es completo. Los cuerpos docentes restantes se obtienen del repositorio y sus catálogos generados. No presentar una preview que solo usa muestras como si ya incluyera todo el campus.

### Regenerar los descargables

Los documentos de contrato y el generador se mantienen en `docs/figma-make/`. Los exports completos se producen para cada entrega y se distribuyen juntos; no necesitan una segunda copia editable en Git. Desde la raíz del repositorio:

```sh
python3 campus/cloudflare.py build
python3 docs/figma-make/exportar.py --output /tmp/smartkea-figma-make --public-ref main
```

Si ejecutas el generador desde la carpeta descargada, añade `--repo /ruta/al/repositorio`. El generador lee las fuentes y catálogos, valida el banco y las seis rutas con los validadores del repositorio, comprueba el hash del banco compilado y escribe únicamente en una carpeta externa. Rechaza el repositorio, cualquier descendiente y los destinos enlazados por symlink dentro de él; tampoco genera bytecode de los validadores. No compila ni publica por su cuenta. Registra por separado el commit del catálogo y el head leído; si difieren, informa para poder recompilar cuando se necesite un snapshot único.

El Markdown del test conserva todas las preguntas y sus claves. El cuaderno D41–D46 conserva los bloques ES y COMMON de las fuentes, desplaza un nivel los encabezados y hace portables sus enlaces; mantiene los bloques de código. El manifiesto identifica cada origen y su SHA-256. La validación de los dos JSON Schema es una comprobación adicional al exportador de biblioteca estándar.

## Qué conserva la propuesta

El campus y OS conservan ES/EN; el examen y TERM siguen en español. Campus y examen mantienen rojo profundo, OS su rojo y TERM su azul. El objetivo es mejorar orientación, siguiente acción, consistencia de controles y legibilidad, preservando rutas, contenido y los registros separados de campus, OS, examen, TERM y rutas profesionales. La guía asistida propuesta utiliza contenido curado y reglas locales. Un servicio de IA generativa, las cuentas de alumno y las calificaciones oficiales quedan fuera del alcance activo.

El examen conserva 100 preguntas, 20 aleatorias por intento, opciones barajadas por ID, corrección al elegir, primera respuesta bloqueada, nota sobre 10, resumen por tema, repaso y enlaces. El muestreo no garantiza los 12 temas en cada intento. La nota es de práctica y no una acreditación.

Las marcas de rutas conservan su clave y `schema: 1`, con `recordId` aditivo para distinguir cada vida del registro. Las escrituras coordinadas mantienen marcas de varias pestañas y respetan cancelaciones y borrados; sin Web Locks o almacenamiento, el borrador permanece en la visita con aviso. TERM conserva su contrato de comparación y guardado: un conflicto ofrece exportar la sesión, descargar el original y recargarlo de forma explícita, con confirmaciones invalidadas si cambia la copia guardada. El prompt y el JSON describen estas conductas actuales.

El caso [C99-DFIR](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/formacion/casos/c99-forense/README.md) amplía M27–M29 mediante diez actividades, materiales sintéticos, guía ES/EN y doce preguntas propias. Mantiene el inventario y las horas del curso; sus fuentes y preguntas se enlazan por separado del banco de informática.

## Integrar con Git y Cloudflare

El repositorio enlazado arriba sigue siendo la fuente canónica. La integración estándar de Make con GitHub solo empuja hacia repositorios creados por Make y es unidireccional; no sincroniza este repositorio existente. Usa exportación o la capacidad de importación disponible, revisa el resultado y traslada los cambios a una rama con PR. [Documentación de GitHub en Make](https://help.figma.com/hc/en-us/articles/35463818346647-Push-from-Figma-Make-to-GitHub).

El curso real es estático y utiliza el Worker `fundamentos-ciberseguridad`. Conserva `wrangler.jsonc`, el generador Python y los prefijos `/introduccion-ciberseguridad/` y `/fundamentos-ciberseguridad/term/`. El prompt y el contrato especifican build/check/dry-run, las puertas de aceptación y la verificación del SHA servido después de desplegar. La preview de Make y el despliegue de Cloudflare son comprobaciones separadas. La consolidación utiliza Wrangler 4.151.1 con `campus/tooling/package-lock.json`, instalación `npm ci --ignore-scripts` y binario local; plan/build/check permanecen offline.

El procedimiento de mantenimiento está en [revisión y release](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/engineering/REVIEW-AND-RELEASE.md); las decisiones de datos y asistencia en [privacidad e IA](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/security/PRIVACY-AND-AI.md), y el seguimiento en [backlog](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/docs/BACKLOG.md) e [issue 4](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/issues/4). La integración local revisada incluye seis rutas profesionales y 26 etapas en [rutas.html](https://smartkea.com/introduccion-ciberseguridad/rutas.html). Su catálogo deriva de `formacion/rutas/routes.json`; las marcas opcionales usan `smartkea.learning-paths.v1`. La publicación se acepta por separado y sus horas no se suman a las 480 del curso.

## Procedencia y alcance

La plantilla usa como baseline público conocido `769c1ba947f5f092894a258974116e82a77a02f1` y describe la consolidación local revisada. La procedencia exacta de cada entrega está en `manifest.json` y en la sección `provenance` de su copia exportada de `producto.json`: SHA del build, head de las fuentes y referencia pública suministrada. El exportador actualiza esos valores sin anclar el contrato mantenido a un commit local. Después de publicar, regenera con `--public-ref` y el SHA remoto final; nunca uses un HEAD local no publicado como enlace público. La aceptación de producción compara `build-info.json` con el SHA definitivo de main.

El banco adjunto es una copia para importar y revisar. Al incorporar cambios, edita únicamente `formacion/introduccion-informatica/banco-preguntas.json` en el repositorio y regenera los derivados; no mantengas dos fuentes editoriales. Tampoco adjuntes exports de progreso reales de alumnos a Figma: pueden contener notas personales. Este paquete solo contiene especificaciones y material público del curso.
