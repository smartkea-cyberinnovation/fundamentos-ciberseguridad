# Kit reproducible 1.1 — datos sintéticos, shells y servicio web

## Contrato y dependencias

Python 3.11+, biblioteca estándar; no hay `pip install`, credenciales, telemetría externa ni llamadas a APIs. `oslab.py` no inspecciona procesos, usuarios, registro o logs reales. Solo `init` escribe archivos: crea un workspace nuevo cuyo padre debe existir y rechaza destinos existentes. Las demás operaciones leen el workspace y emiten JSON por stdout; los errores van a stderr y devuelven código 2. Éxito devuelve 0; una búsqueda correcta sin coincidencias también devuelve 0. El número de hallazgos no es un exit code.

| Orden | Entrada | Salida / resultado de referencia |
|---|---|---|
| `init RUTA` | Directorio nuevo | 8 archivos de texto, 8 eventos, 3 indicadores y ejemplo IA |
| `manifest RUTA` | `datos/` | 8 archivos, 62 bytes y SHA-256 por contenido |
| `timeline RUTA` | `eventos.json` | E01–E08; UTC y timestamps originales conservados |
| `match RUTA` | Eventos + indicadores | 4 coincidencias exactas sobre 3 eventos; no significa compromiso |
| `review RUTA` | `respuesta-ia.json` + eventos | Validez estructural, nunca veracidad certificada |

Se rechazan archivos individuales de más de 1 MiB, más de 128 entradas/filas, enlaces simbólicos o duros detectados por el lector, objetos no regulares, JSON con claves repetidas y números no finitos. El manifiesto no es recursivo. La búsqueda admite IP, dominio ASCII y SHA-256; no resuelve DNS, no visita URLs, no admite comodines ni incorpora todos los tipos STIX. La coincidencia de dominios es exacta: un subdominio no coincide con su dominio padre.

No es un sandbox contra usuarios concurrentes, un antivirus, un colector forense ni un verificador de cadena de custodia. La marca de workspace no autentica contenido. `read_small` comprueba algunos cambios durante lectura, pero no garantiza una instantánea forense. El modo binario evita traducir LF/CRLF al calcular bytes en Windows.

## Ejecución desde la raíz del curso

```bash
python3 kit/oslab.py init mi-laboratorio
python3 kit/oslab.py manifest mi-laboratorio
python3 kit/oslab.py timeline mi-laboratorio
python3 kit/oslab.py match mi-laboratorio
python3 kit/oslab.py review mi-laboratorio
python3 -m unittest discover -s kit -v
bash -n kit/resumen.bash
bash kit/resumen.bash mi-laboratorio
```

Windows usa su intérprete Python aprobado, por ejemplo `py -3`. No se recomienda cambiar políticas de ejecución para arrancar los scripts. Los ejemplos nativos son `resumen.bash`, `resumen.zsh`, `Resumen.ps1` y `resumen.cmd`: comparan el mismo dataset sin delegar toda la tarea a Python. Bash/zsh/PowerShell devuelven conteo y bytes; BAT solo conteo.

**Límites nativos:** los resúmenes son ejemplos docentes, no aplican todas las restricciones del lector Python. No usarlos sobre directorios no confiables o concurrentes. BAT tiene límites de encoding, tratamiento de nombres y distinción entre lista vacía/error; solo se usa con el dataset conocido. Se pide al alumno identificar esas limitaciones y justificar una migración a PowerShell, no ocultarlas.

## Servicio HTTP docente

```bash
python3 kit/web.py
```

Abre en el navegador el servidor local del puerto 8080 y consulta `/healthz`. Solo se sirven dos rutas fijas, no archivos del sistema. GET y HEAD son de lectura; POST/PUT/DELETE se rechazan. Otras funciones HTTP no se implementan. El log recoge ruta conocida y estado, no direcciones, cabeceras o query strings. El servicio no inicia sesiones, no recibe archivos ni ejecuta comandos. Interrumpir con Ctrl+C; no necesita un daemon permanente.

Este servicio enseña HTTP, errores, logs y health checks. **No implementa TLS ni autenticación y no debe publicarse en Internet.** Python advierte que `http.server` no es un servidor de producción. No lo conviertas en una aplicación empresarial añadiendo únicamente un contenedor. El ejercicio TLS del programa se valida por separado con un servidor apropiado. [S17](../FUENTES.md)

## Docker Compose

Desde `kit/`, en el host dedicado del laboratorio:

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose logs --tail 20 web
docker compose down
```

El acceso local es por el puerto **18080** del anfitrión, ligado a `127.0.0.1`; dentro del contenedor se usa 8080. La red declarada es interna, el usuario es 10001, el filesystem es de solo lectura y no hay volúmenes, secretos ni socket Docker. Se limitan recursos y rotación de logs. El health check prueba respuesta HTTP y contenido JSON. La imagen base por etiqueta facilita la práctica; el docente debe fijar un digest real revisado, registrar parches y reconstruir antes de usarla en una cohorte. No se ha inventado un digest.

## Docker Swarm

`swarm.yaml` es distinto de `compose.yaml`: formato 3.8, imagen preconstruida indicada mediante `OSLAB_IMAGE` y **sin puertos publicados**. El docente define una imagen autorizada, idealmente por digest, disponible para todos los nodos; valida `docker stack config -c swarm.yaml` y despliega únicamente en un clúster de prácticas ya preparado. No se inicializa ni modifica un clúster existente de producción.

La comprobación HTTP se hace desde un cliente autorizado conectado a la misma red overlay: no se incorpora un túnel ni un puerto exterior para eludir esta restricción. Registrar permisos de unión a esa red. Después retirar únicamente el stack de prueba. La protección Compose `security_opt` no se presenta como aplicada automáticamente por Swarm: verificar controles efectivos del runtime. Docker documenta diferencias de formato y de publicación entre ambas vías. [S09](../FUENTES.md)

## Qué se ha probado

Ver [resultados y límites](../qa/RESULTADOS.md). Los tests HTTP levantan un servidor temporal en loopback y lo cierran. No son un despliegue Docker, una validación Swarm ni una prueba Windows/macOS. El diseño incluye instrucciones de aceptación nativa en los guiones R03/R04/R06.
