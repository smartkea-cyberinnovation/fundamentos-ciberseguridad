# Publicar TERM en Cloudflare Workers

## Integración existente

TERM forma parte de `smartkea-cyberinnovation/fundamentos-ciberseguridad`. Conserva el Worker existente `fundamentos-ciberseguridad` y su configuración de Workers Builds. La compilación del campus añade el curso Linux a una subruta propia.

| Ajuste | Valor |
|---|---|
| Rama de producción | `main` |
| Directorio raíz | Raíz del repositorio |
| Worker | `fundamentos-ciberseguridad` |
| Build hook de Wrangler | `python3 campus/cloudflare.py build` |
| Deploy de producción | `python3 campus/cloudflare.py deploy` |
| Preview de rama | `python3 campus/cloudflare.py preview` |
| Curso Linux | `https://smartkea.com/fundamentos-ciberseguridad/term/` |
| Campus general | `https://smartkea.com/introduccion-ciberseguridad/` |
| Activos | `campus/worker-dist` |
| Runtime | Static Assets; sin API de ejecución |

Los activos se guardan físicamente bajo el prefijo de URL, según el contrato de Static Assets. La configuración añade la ruta con barra y la entrada exacta sin barra. La redirección de la entrada exacta se genera en `_redirects`. Un registro DNS proxied y una zona activa son requisitos del proveedor para servir la ruta.

## Compilar y comprobar sin publicar

Desde la raíz del repositorio, con Python 3.11+ y Node 22+ para las pruebas JavaScript:

```sh
python3 term/build.py
python3 term/build.py --check
node --test term/tests/*.test.mjs
python3 -m unittest discover -s term/tests -p 'test_*.py' -v
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
```

La construcción del curso no necesita npm, tokens, datos personales ni una VM conectada. Para probarlo localmente:

```sh
python3 term/serve.py --port 8791
```

Abre `http://127.0.0.1:8791/fundamentos-ciberseguridad/term/`. El servidor es exclusivo de desarrollo, escucha solo en loopback y no interpreta comandos ni tiene endpoint de administración.

## Conectar una terminal

Primero despliega la VM, ttyd, Tunnel y Access siguiendo [la guía de conexión](CONEXION-TTYD.md). Después define **variables del build de Cloudflare**:

| Variable | Ejemplo de configuración del operador |
|---|---|
| `TERM_LAB_URL` | `https://term-a01.smartkea.com/` |
| `TERM_LAB_ALLOWED_ORIGINS` | `https://term-a01.smartkea.com` |
| `TERM_LAB_EMBED` | `0` para nueva pestaña; `1` tras verificar iframe y Access |

Estos valores no contienen contraseñas ni tokens. `term-a01.smartkea.com` es un ejemplo; debe sustituirse por el endpoint creado y comprobado. El origen debe ser distinto al del campus. Se rechazan comodines, credenciales en URL, query strings y fragmentos. Con URL vacía no se habilita ninguna conexión.

Las variables se leen durante el build y se convierten en `config.json` público y una CSP coherente. Cambiarlas requiere reconstruir y publicar. No basta añadir una variable de runtime a un Worker estático ya compilado.

En un grupo de alumnos, usa un portal de asignación existente o una publicación/configuración que dirija a cada endpoint autorizado. Una única URL estática no es un broker multiusuario ni provisiona VMs. El control efectivo de cada terminal sigue en Access y en la separación de VM por alumno.

## Subir y verificar

La conexión Git de Workers Builds publica los commits integrados en `main`, si continúa habilitada en la cuenta. Como alternativa, un operador con acceso autorizado puede ejecutar:

```sh
python3 campus/cloudflare.py dry-run
python3 campus/cloudflare.py deploy
```

El segundo comando modifica producción. La credencial se suministra por el mecanismo autorizado de Cloudflare, nunca se incorpora al repositorio. Se conserva la versión fijada de Wrangler ya adoptada por el campus.

Tras publicar, comprobar:

1. Entrada con y sin barra, index, CSS, JavaScript, `course.json` y `config.json`.
2. `build-info.json`: commit servido, hash de contenido, 16 módulos, 48 lecciones y 96 preguntas.
3. Una lección, sus cuatro vistas, copia de comandos, test y persistencia.
4. Manual, descargas, enlaces y una ruta inexistente con respuesta 404.
5. CSP y `nosniff` en respuestas HTTP reales. La salida orientativa debe seguir identificada.
6. La URL del campus general y una ruta corporativa ajena al curso.
7. Si hay ttyd, autenticar usuario permitido, denegar usuario ajeno y cerrar sesión/terminal.

El éxito de una compilación no acredita por sí mismo la publicación o la disponibilidad de la VM.

## Recuperación

Conserva la versión previa del Worker. Para revertir, restaura esa versión desde el historial del proveedor o publica el commit aceptado anterior. Exporta progreso antes de cambiar el origen. El despliegue de la web no elimina automáticamente las VMs, sus procesos ni sus registros: su cierre está en la guía de laboratorio.

## Uso autónomo

`term/dist` es una web estática portable que puede servirse desde la raíz de otro alojamiento. Para conservar el prefijo público en otro Worker, usa una salida de activos con la misma jerarquía `fundamentos-ciberseguridad/term/`. Evita crear otro Worker con rutas que compitan con el Worker ya integrado.

## Referencias

- [Rutas de Workers](https://developers.cloudflare.com/workers/configuration/routing/routes/).
- [Subdirectorios de Static Assets](https://developers.cloudflare.com/workers/static-assets/routing/advanced/serving-a-subdirectory/).
- [Workers Builds y GitHub](https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/github-integration/).
- [Cabeceras](https://developers.cloudflare.com/workers/static-assets/headers/).
