# Fuentes, procedencia y límites

## Material del caso real

Base: análisis estático ya publicado en [docs/casos/c99-20261018](../../../docs/casos/c99-20261018/README.md), su revisión de procedencia y la muestra proporcionada durante la investigación. Variante canónica declarada: 395291 bytes; SHA-256 `1e07598c2e41b7827840ba6c8611912abd88c0344a5d1eff364eaabeccdc6420`. Publicación de referencia: repositorio `c99-shell/c99`, commit `ff62d07db6b99284ad90c2c97f143cd64fe51727`, blob `7f95818a5608c930b2c1fc27e7b824347a226053`. No se ha vuelto a adquirir la muestra operativa para preparar esta práctica.

El encabezado declara proyecto/autor/fecha/descripción. Son afirmaciones dentro de un fichero, no firma autenticada ni adquisición acreditada. La revisión previa también distingue una fecha interna del dossier de la fecha de revisión. No se atribuyen al ofuscador todas las funciones peligrosas ni se infiere titularidad del receptor desde un commit.

## Material nuevo de esta actividad

Todo `evidencias/` es sintético. La fecha 2026-10-01, web-01, las identidades, tickets y direcciones son invenciones docentes. Las fichas de webroot no son copias de PHP ni hashes de C99. Las decisiones y la cronología sólo resuelven ese supuesto. Los resultados de la herramienta pertenecen a la copia de entrada cuyo hash se informa.

La preparación de esta actividad no aporta nueva inteligencia DNS/RDAP/CT, telemetría de una víctima ni pruebas de recepción de una comunicación. Los dominios/IP de ejemplo no se publican como IOC de producción.

## Ampliación técnica consultada para la docencia

Referencias primarias consultadas el 19/10/2026. Sustentan terminología y semántica; no prueban que C99 se ejecutara en ningún entorno.

| ID | Fuente | Uso |
|---|---|---|
| S1 | https://attack.mitre.org/techniques/T1505/003/ | Concepto de webshell; clasificación de técnica, no atribución |
| S2 | https://www.php.net/manual/en/language.types.string.php | Reglas de escapes y comillas de PHP |
| S3 | https://www.php.net/manual/en/language.basic-syntax.comments.php | Comentarios y límites de bloques PHP |
| S4 | https://www.php.net/manual/en/function.stat.php | atime, mtime, ctime y diferencias de plataforma |
| S5 | https://www.php.net/manual/en/function.extract.php | Importación de variables y entrada no confiable |
| S6 | https://docs.docker.com/engine/containers/run/ | Identidad, límites, filesystem y red del contenedor |

Los problemas del lexer anterior se documentan en [PR #12](https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/pull/12). Su estado puede cambiar: registrar el commit leído. Esta práctica usa una herramienta independiente para manifiestos y cronologías y no depende de que ese PR esté fusionado.

## Condiciones de distribución

Se publican material propio, fichas sintéticas, código de análisis offline y referencias. No se publican muestras operativas, datos de alumnos, enlaces privados del expediente ni evidencias corporativas. No se eluden los controles de clasificación de un proveedor de almacenamiento. La licencia general del repositorio no modifica los derechos de las fuentes externas.
