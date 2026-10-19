# Integración de dependencias y correcciones del campus · 2026-09-15

## Alcance de los PR

Se consolidan #1 (minimatch), #4 (flatted), #5 (picomatch), #6 (brace-expansion), #10 (js-yaml), #11 (@humanfs/node), #12 (nanoid), #13 (baseline-browser-mapping), #14 (browserslist), #15 (Next/sharp) y #16 (Next). Sus commits se conservan como ancestros: no se sustituye su procedencia por una actualización sin historial.

Los cambios comunes se deduplican. Next 16.3.5, propuesto en #15, sustituye al 16.3.3 de #16; no se degrada la versión. eslint-config-next queda alineado con Next; React y React DOM quedan en 19.2.8 y sharp en 0.35.4. Las dependencias npm pertenecen a la aplicación de referencia de la raíz: el campus estático sigue sin dependencias npm de producción.

## Correcciones del campus 2.0.1

- Un evento `storage` recibido no vuelve a escribirse a `localStorage`: evita el intercambio repetitivo entre pestañas. Los cambios locales recuerdan su propia ruta sin sobrescribirla al renderizar un evento ajeno.
- Una práctica con las cinco fases confirmadas se reabre en el cierre; una incompleta se reanuda en la primera fase pendiente.
- La importación utiliza un límite de 1 MiB en bytes UTF-8, coherente con el archivo seleccionado. Permite recuperar las notas Unicode máximas admitidas por módulo.
- Se conservan el esquema y la clave de progreso v1. No se borran las marcas existentes ni se realiza una migración destructiva.

## Validación inicial del árbol candidato

El job `validate` del run [34906649882](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/actions/runs/34906649882) terminó correctamente: 22 pruebas del compilador, 22 de estado, 23 de Chromium, 12 de dependencias, 42 del kit y 8 de planificación; 129 en total. Pasaron además instalación reproducible, lint, tipos y build de Next. La auditoría de producción no reportó vulnerabilidades conocidas en esa ejecución.

El job posterior que intentó publicar la rama no pudo actualizar un workflow por falta del permiso `workflows` del token de Actions. Ese fallo de escritura no se presenta como éxito global del run. No se amplió dicho token: el árbol se integra mediante el conector autorizado de GitHub y una revisión normal.

El artefacto descargado `reviewed-integration-candidate` tiene SHA-256 `6d49c8fbe83b41e0215d5b0e46f215d4c8561928d958a830bc4b6ac49dfbd22a`. Contiene las diferencias, logs, comentarios/revisiones consultados y sitio compilado. Los PR no contenían solicitudes de cambios ni comentarios inline en la consulta.

## Hallazgos adicionales al auditar desarrollo

El primer control de todo el árbol, no solo producción, detectó `@babel/core` 7.29.0 y dos instancias de `brace-expansion` (1.1.13 y 5.0.5) afectadas por avisos. No se desactivó ese control para poder fusionar.

Se actualizó de manera acotada el lockfile de las familias Babel y brace-expansion, respetando los rangos existentes y sin `--force` ni scripts de instalación. Resultado: @babel/core 7.29.7, brace-expansion 1.1.21 y la instancia anidada 5.0.12, junto con dependencias coherentes de Babel. Se verificó que el diff solo cambiaba package-lock.json, las familias aprobadas y orígenes registry.npmjs.org.

El run [34907458106](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/actions/runs/34907458106) volvió a instalar, ejecutar lint/tipos, 12 comprobaciones de compatibilidad, build Next y auditoría completa con umbral bajo. El informe descargado contiene cero vulnerabilidades reportadas de cualquier severidad. Artefacto `reviewed-development-lock`, SHA-256 `a8cc75863d5c422e476e257c3f9b476833f7395df8b44c04ee360ed6579947da`.

Referencias primarias: [aviso de Babel](https://github.com/babel/babel/security/advisories/GHSA-4x5r-pxfx-6jf8) y [aviso de brace-expansion](https://github.com/juliangruber/brace-expansion/security/advisories/GHSA-rgw5-rvv9-x895). No se incluyen ni ejecutan reproducciones de explotación.

## Aceptación final y mantenimiento

Todos los workflows temporales y el script de preparación se eliminan de la revisión final. Permanecen dos controles de lectura: campus y aplicación heredada. El del campus también se ejecuta ante cambios del manifiesto o lockfile raíz. El de la aplicación comprueba instalación sin scripts de ciclo de vida, lint, tipos, pruebas de compatibilidad, build y auditorías de producción y conjunto completo, con umbral de rechazo alto/crítico.

Las pruebas comprueban versiones mínimas y coherencia entre paquetes relacionados, sin bloquear automáticamente cada parche futuro por una versión exacta incrustada en el test. Las versiones efectivas siguen fijadas en package.json y package-lock.json.

La revisión final se vuelve a validar en el PR #17 antes de fusionar. Su SHA y conclusión deben consultarse en Actions; no se atribuyen al nuevo commit resultados de uno anterior. Cero avisos en una auditoría no equivale a ausencia garantizada de vulnerabilidades.

Se elimina la descarga de fuentes de Google durante el build de la aplicación de referencia y se utilizan tipografías de sistema con presentación clara. No se modifican permisos, reglas de ramas, requisitos de revisión ni despliegues de Cloudflare. El contenido docente y la aplicación previa se conservan. Las pruebas web no acreditan ejecutar los 96 laboratorios nativos ni las prácticas Windows/macOS.
