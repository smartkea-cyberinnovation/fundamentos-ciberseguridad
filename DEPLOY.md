# Despliegue, validación y recuperación

Este documento es para mantenedores. El README principal está orientado al alumno y explica cómo estudiar.

## Producción

- Repositorio: `smartkea-cyberinnovation/fundamentos-ciberseguridad`
- Rama de producción: `main`
- Campus: `https://smartkea.com/introduccion-ciberseguridad/`
- Worker: `fundamentos-ciberseguridad`
- Ruta: `smartkea.com/introduccion-ciberseguridad/*`

La configuración técnica detallada se mantiene en [campus/DEPLOY-CLOUDFLARE.md](campus/DEPLOY-CLOUDFLARE.md) y la recuperación en [campus/WORKERS-RECOVERY.md](campus/WORKERS-RECOVERY.md).

## Flujo recomendado

1. Crear una rama de trabajo.
2. Modificar fuentes, no artefactos derivados cuando el build los genere.
3. Ejecutar validaciones locales.
4. Abrir Pull Request con alcance, riesgos y evidencias.
5. Revisar que los cambios docentes y de interfaz preservan accesibilidad, navegación y progreso.
6. Integrar en `main`.
7. Publicar mediante el flujo documentado.
8. Comprobar la versión servida y registrar la observación.
9. Revertir si falla un criterio de aceptación.

## Validación local

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
python3 campus/cloudflare.py check
python3 -m unittest discover -s campus/tests -p 'test_*.py' -v
node --test campus/tests/*.test.mjs
python3 formacion/plan-maestro/validar.py
```

Servidor local:

```sh
python3 campus/serve.py --port 8788
```

Abrir `http://127.0.0.1:8788`.

## Publicación

`build` y `check` no publican. `preview` prepara una versión de prueba y `deploy` publica según la configuración vigente:

```sh
python3 campus/cloudflare.py preview
python3 campus/cloudflare.py deploy
```

No ejecutes `deploy` como prueba exploratoria.

## Criterios mínimos de aceptación

- build y validadores correctos;
- navegación y contenido principal disponibles en español e inglés cuando aplique;
- experiencia usable en móvil, tableta y escritorio;
- presentación/pantalla completa sin pérdida de navegación;
- progreso existente no destruido por una migración accidental;
- ausencia de secretos y datos personales;
- enlaces críticos y recursos del campus accesibles;
- commit/versionado de producción identificable;
- rollback conocido antes del despliegue.

## Observación de producción

La observación HTTP acotada puede ejecutarse con:

```sh
python3 campus/audit_publication.py --output campus/qa/publication.json
```

Una ejecución de CI, un build correcto o un merge no demuestran por sí solos que producción esté sirviendo la versión esperada.

## Recuperación

Ante una regresión, priorizar recuperación del servicio y del progreso del alumno. Seguir [campus/WORKERS-RECOVERY.md](campus/WORKERS-RECOVERY.md), documentar el incidente y convertir la causa en una prueba de regresión.
