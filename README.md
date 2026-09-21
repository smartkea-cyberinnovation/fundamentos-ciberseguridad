# SmartKEA · Fundamentos de informática y ciberseguridad

**Aprende a comprender sistemas, construirlos, diagnosticarlos, protegerlos y explicar tus decisiones.**

[Entrar al campus](https://smartkea.com/introduccion-ciberseguridad/) · [Ruta curricular](formacion/itinerario-integral/12-curriculum.md) · [Guía de estudio](formacion/sistemas-operativos/COMO-ESTUDIAR.md) · [Biblioteca](formacion/itinerario-integral/14-library.md)

Este repositorio es, ante todo, **un entorno de aprendizaje**. El README explica cómo estudiarlo y cómo sacarle partido. La operación del software, el despliegue y la seguridad del proyecto se documentan por separado.

> No intentes memorizar el repositorio. El objetivo es construir un modelo mental, practicarlo, equivocarte de forma segura, diagnosticar el error y conservar evidencia de que sabes hacerlo.

## Empieza en cinco minutos

1. Abre el [campus web](https://smartkea.com/introduccion-ciberseguridad/).
2. Empieza por **D26 · Informática** para construir el mapa general.
3. Elige un único objetivo: «al terminar podré explicar o hacer X».
4. Trabaja un bloque de aproximadamente 25 minutos sin cambiar de tema.
5. Cierra la lectura e intenta reconstruir la idea con tus palabras.
6. Haz la micropráctica relacionada o crea un ejemplo mínimo.
7. Comprueba el resultado y registra la duda que quede.
8. Continúa sólo cuando puedas explicar qué ocurrió y por qué.

El tiempo es una herramienta de atención, no una nota. Si un problema te bloquea, no saltes directamente a copiar una solución: aprende a diagnosticarlo.

## Cómo estudiar

Usa este ciclo para cada concepto:

**Objetivo → concepto → recuperación activa → práctica → evidencia → explicación → revisión.**

Una sesión típica puede ser:

- **2 min** · define qué quieres comprender o conseguir;
- **20–25 min** · lectura, análisis o práctica concentrada;
- **3–5 min** · recuerda sin mirar y escribe lo esencial;
- **5 min** · compruébalo con una práctica, pregunta o ejemplo;
- **pausa breve** · después decide si continuar, revisar o profundizar.

No necesitas respetar exactamente esos minutos. Ajusta el ciclo al tipo de tarea y a tu capacidad de concentración.

### Cuando te atasques

Un ingeniero no se mide por no tener problemas, sino por aprender a reducirlos.

1. Reproduce el fallo.
2. Lee el mensaje exacto.
3. Identifica qué cambió.
4. Formula una hipótesis.
5. Observa estado, configuración y logs.
6. Cambia una sola variable.
7. Vuelve a probar.
8. Documenta causa, solución y cómo evitar la regresión.

Si sigues bloqueado, busca primero documentación primaria y después pide una pista. La solución completa debe ser el último nivel de ayuda, no el primero.

## Qué debes conseguir

Al avanzar por el itinerario deberías poder conectar cinco capas:

| Capa | Pregunta que debes poder responder |
|---|---|
| Fundamentos | ¿Qué está ocurriendo realmente debajo de la interfaz? |
| Construcción | ¿Cómo lo implemento de forma reproducible? |
| Operación | ¿Cómo sé que funciona y cómo diagnostico un fallo? |
| Seguridad y riesgo | ¿Qué puede salir mal, qué control aplico y qué evidencia tengo? |
| Negocio y profesión | ¿Qué valor aporta, quién decide, cuánto cuesta y cómo lo comunico? |

Leer es sólo una parte. El aprendizaje se demuestra con explicaciones, prácticas, decisiones justificadas y resultados reproducibles.

## Ruta principal

La ruta recomendada construye dependencias en lugar de acumular siglas:

| Orden | Recurso | Pregunta principal |
|---:|---|---|
| 1 | [D26 · Informática](formacion/itinerario-integral/01-computing.md) | ¿Qué es realmente un sistema informático? |
| 2 | [D27 · Historia](formacion/itinerario-integral/02-history.md) | ¿Cómo llegamos hasta la tecnología actual? |
| 3 | [D28 · Hardware](formacion/itinerario-integral/03-hardware.md) | ¿Qué ocurre físicamente cuando ejecutamos software? |
| 4 | [D29 · Redes](formacion/itinerario-integral/04-networks.md) | ¿Cómo se comunican los sistemas? |
| 5 | [D30 · Web y cloud](formacion/itinerario-integral/05-web.md) | ¿Cómo se construye y publica un servicio moderno? |
| 6 | [D31 · Seguridad](formacion/itinerario-integral/06-security.md) | ¿Qué protegemos, de qué y con qué evidencia? |
| 7 | [D32 · Información](formacion/itinerario-integral/07-information.md) | ¿Cómo gobernamos los datos durante su ciclo de vida? |
| 8 | [D33 · Identidades](formacion/itinerario-integral/08-identity.md) | ¿Quién puede hacer qué, sobre qué y por qué? |
| 9 | [D34 · Profesiones](formacion/itinerario-integral/09-careers.md) | ¿Cómo se convierte el conocimiento en trabajo profesional? |
| 10 | [D37 · Itinerario maestro](formacion/itinerario-integral/12-curriculum.md) | ¿Qué me falta y en qué orden debería profundizar? |
| 11 | [D38 · Ecosistema](formacion/itinerario-integral/13-ecosystem.md) | ¿Qué instituciones, comunidades y entornos existen? |
| 12 | [D39 · Biblioteca](formacion/itinerario-integral/14-library.md) | ¿Dónde profundizo con fuentes de calidad? |
| apoyo | [D35](formacion/itinerario-integral/10-glossary.md) / [D40](formacion/itinerario-integral/15-master-glossary.md) | ¿Qué significa cada término y qué conceptos no debo confundir? |
| método | [D36 · Fuentes](formacion/itinerario-integral/11-sources.md) | ¿Cómo verifico una afirmación y mantengo el conocimiento actualizado? |

No es obligatorio consumir todos los recursos de una vez. Usa D37 como mapa y vuelve a D35/D40/D36 cuando aparezca una laguna.

## Teoría que termina en práctica

Cada concepto importante debería acabar en una acción observable: explicar, configurar, programar, medir, diagnosticar, comparar, recuperar o justificar.

Para sistemas operativos existe una ruta operativa específica:

| Recurso | Práctica conceptual |
|---|---|
| [D22 · Identidad y bastionado](formacion/sistemas-operativos/operacion/01-identidad-bastionado.md) | usuarios, privilegios, perfiles y política efectiva |
| [D23 · Redes y recursos](formacion/sistemas-operativos/operacion/02-redes-recursos.md) | permisos, recursos compartidos, segmentación y restauración |
| [D24 · Navegación y TLS](formacion/sistemas-operativos/operacion/03-navegacion-tls.md) | DNS, proxy, firewall, TLS, cuentas y privacidad |
| [D25 · Detección y aceptación](formacion/sistemas-operativos/operacion/04-deteccion-laboratorios.md) | controles, evidencia, triaje y recuperación |

Antes de una práctica, identifica siempre **objetivo, entorno, riesgo, rollback y evidencia esperada**.

## Si tu ordenador no coincide con la práctica

No abandones una competencia porque utilices otro sistema operativo.

- Si el objetivo es aprender **Windows** desde macOS o Linux, utiliza una máquina virtual compatible o un laboratorio autorizado.
- Si necesitas **Linux** desde Windows o macOS, una VM suele ser la opción más fiel para estudiar el sistema completo.
- Los contenedores son excelentes para aplicaciones y servicios, pero no sustituyen una VM cuando el concepto depende de kernel, arranque, drivers o determinadas políticas del sistema.
- En Apple Silicon, Windows/ARM, x86 y otras combinaciones, comprueba arquitectura y compatibilidad antes de descargar una imagen.
- Usa documentación oficial vigente del hipervisor y del sistema operativo; evita imágenes de procedencia dudosa.

Consulta [Entorno de laboratorio](formacion/sistemas-operativos/LABORATORIO.md). La competencia importante no es «seguir estos clics», sino saber preparar un entorno, comprobar requisitos, aislar el riesgo y recuperarte si algo falla.

## Tu progreso

No confundas progreso con páginas abiertas. Considera un concepto consolidado cuando puedas:

- explicarlo sin leer;
- reconocer cuándo se aplica y cuándo no;
- completar una práctica pequeña;
- interpretar el resultado;
- detectar al menos un error frecuente;
- guardar una evidencia reproducible;
- relacionarlo con un sistema o problema real.

El campus conserva progreso local exportable. Antes de cambiar de dispositivo u origen, exporta tu estado. No guardes secretos, contraseñas ni datos personales en las notas.

[Cómo funciona el progreso y su privacidad](campus/PROGRESO.md).

## Profundizar sin perderse

Usa tres niveles:

**Core** — lo que necesitas para continuar.  
**Práctica** — lo que convierte la teoría en competencia.  
**Profundización** — papers, RFC, estándares, libros, certificaciones, tecnologías o casos avanzados.

Cuando una fuente externa contradiga el material, no elijas por autoridad aparente: compara fecha, alcance, versión, fuente primaria y contexto.

## Estudiar para trabajar

No optimices el aprendizaje únicamente para aprobar un examen o acumular certificaciones. Construye evidencia profesional:

- repositorios limpios y explicables;
- diagramas y decisiones de arquitectura;
- scripts pequeños pero probados;
- laboratorios reproducibles;
- análisis de riesgos;
- informes de incidentes sintéticos;
- restauraciones verificadas;
- presentaciones técnicas para públicos no técnicos;
- documentación en inglés;
- reflexiones sobre errores y mejoras.

[D34 · Profesiones](formacion/itinerario-integral/09-careers.md) conecta el conocimiento con familias profesionales. El plan maestro amplía esa relación con ciberseguridad, GRC, IA, investigación e innovación.

## Usar IA para aprender

La IA puede ayudarte a formular preguntas, explicar alternativas, generar casos de prueba, revisar una explicación o encontrar documentación. No debe sustituir la comprensión.

Una secuencia útil es:

1. intenta explicar o resolver;
2. pide una pista, no la respuesta;
3. contrasta con documentación primaria;
4. ejecuta o verifica;
5. explica por qué la solución funciona;
6. registra qué error cometiste.

Nunca pegues secretos, datos personales, evidencias de clientes o información restringida en una herramienta que no esté autorizada para tratarlos.

## El campus web

El campus está diseñado para lectura, búsqueda, presentación a pantalla completa, autoevaluación y seguimiento local. La evolución de producto sigue estos principios:

- un concepto principal por vista;
- teoría seguida de práctica corta;
- navegación usable en móvil, tableta y escritorio;
- modo de concentración y pantalla completa;
- progreso basado en evidencias, no sólo visitas;
- ayuda gradual cuando el alumno se atasca;
- temporización de sesiones como apoyo, no como vigilancia;
- accesibilidad y funcionamiento sin cuenta para las funciones básicas.

La especificación de producto educativo está en [docs/LEARNING-DESIGN.md](docs/LEARNING-DESIGN.md). Algunas capacidades descritas allí son objetivos de evolución y no deben interpretarse como funciones ya publicadas.

## Para docentes y contribuidores

Antes de añadir contenido, pregunta:

- ¿qué resultado de aprendizaje produce?;
- ¿qué prerrequisito necesita?;
- ¿qué práctica lo consolida?;
- ¿cómo sabremos que el alumno lo entiende?;
- ¿qué error frecuente debe aprender a diagnosticar?;
- ¿qué fuente primaria lo respalda?;
- ¿cuándo debe revisarse?;
- ¿es fundamento estable, tecnología cambiante o normativa fechada?

Recursos de mantenimiento:

- [Diseño de aprendizaje](docs/LEARNING-DESIGN.md)
- [Guía de edición](campus/EDICION.md)
- [QA](campus/QA.md)
- [Seguridad](SECURITY.md)
- [Despliegue](DEPLOY.md)
- [Licencia y condiciones](LICENSE.md)
- [Migración y procedencia](docs/MIGRATION.md)

## Estructura del repositorio

```text
campus/                         aplicación web, compilación, ES/EN, pruebas y operación
formacion/sistemas-operativos/  lecciones, prácticas, laboratorio y evaluación
formacion/itinerario-integral/  fundamentos, historia, redes, seguridad, carrera y fuentes
formacion/plan-maestro/         mapa curricular, marcos y continuidad
docs/                           diseño, mantenimiento y procedencia
.github/workflows/              validación y aceptación
SECURITY.md                     política de seguridad
LICENSE.md                      condiciones de uso
DEPLOY.md                       operación y publicación
```

## Seguridad y límites

Practica únicamente en sistemas propios, laboratorios aislados o entornos para los que exista autorización explícita. No introduzcas secretos ni datos personales reales en repositorios, notas o laboratorios.

Este repositorio conserva la autoría indicada y no concede una licencia abierta por el mero hecho de ser público. Consulta [LICENSE.md](LICENSE.md).

---

**Wiktor Nykiel · SmartKEA CyberInnovation**  
Informática · Ciberseguridad · GRC · IA · Investigación · Innovación
