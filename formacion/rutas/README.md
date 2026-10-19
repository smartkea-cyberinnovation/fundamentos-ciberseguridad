# Rutas profesionales · SmartKEA

[Volver al repositorio](../../README.md) · [Awesome DPD · edición original](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/README.md) · [Datos de rutas](routes.json) · [Estudio y evaluación](ESTUDIO.md)

**Seis perfiles, un método: entender → practicar → demostrar → especializarse.**

Las rutas son propuestas editoriales de estudio con actividades ya definidas, no títulos ni cursos reconocidos para certificación. No alteran los **32 módulos, 96 prácticas y 480 horas planificadas** del currículo base ni convierten las 108 propuestas del plan maestro en contenidos impartidos.

| Perfil | Duración orientativa | Dedicación total estimada | Evidencia final |
|---|---:|---:|---|
| No técnico · negocio y personas | 8 semanas | 32 h | Reconocer un tratamiento, proteger el trabajo cotidiano y escalar correctamente. |
| Jurídico · privacidad y contratación | 12 semanas | 72 h | Traducir hechos y normas a recomendaciones aplicables y contratos verificables. |
| DPD · gobierno de privacidad | 16 semanas | 128 h | Construir y supervisar un programa de privacidad con independencia, evidencias y prioridades. |
| Técnico · soporte y operación | 14 semanas | 84 h | Operar equipos, identidades y recuperación de forma repetible y auditable. |
| Informático · desarrollo y arquitectura | 14 semanas | 112 h | Diseñar servicios con privacidad y seguridad comprobables desde requisitos hasta retirada. |
| Ciberseguridad · defensa, GRC y auditoría | 14 semanas | 112 h | Pasar de señales y controles técnicos a riesgos, decisiones y evidencias defendibles. |

## Cómo elegir sin equivocarse

**No técnico**: negocio, RR. HH., compras, dirección o reconversión; empieza sin terminal. **Legal**: derecho, contratos y derechos de personas, con puente tecnológico. **DPD**: supervisión de un programa y asesoramiento independiente; exige cerrar lagunas jurídicas o técnicas según procedencia. **Técnico**: soporte y operación. **Informático**: ingeniería de software y arquitectura. **Ciber**: defensa, GRC y auditoría.

Los títulos laborales se solapan. Se elige por tareas que se desea desempeñar, no por una supuesta jerarquía. Las referencias ECSF orientan competencias: no implican acreditación ENISA ni análisis de ofertas o salarios. Véanse [ECSF y fuentes](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/FUENTES.md).

## Puentes y prerrequisitos

Jurídico → tecnología: ciclo del dato, identidades, logs, copias, cifrado, API y arquitectura. Tecnología → DPD: hechos jurídicamente relevantes, ámbito, bases, derechos, proporcionalidad e independencia. No técnico → técnico: laboratorio seguro y M01–M04 antes de terminal avanzada.

**Los enlaces a M25, M27 o M31 no autorizan a saltarse sus prerrequisitos.** El navegador muestra la cadena pendiente del currículo. Para una actividad de lectura puede consultarse un extracto; para completar el módulo o su práctica hay que cubrir las dependencias. El tiempo extra necesario no está incluido automáticamente en las estimaciones de ruta.

## Certificaciones

[Catálogo comparado](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/CERTIFICACIONES.md). Elige una credencial principal únicamente después de definir objetivo, evidencia, elegibilidad, programa vigente y coste total. No es necesario obtener todas las opciones mostradas. La certificación AEPD-DPD es voluntaria; este material no constituye formación reconocida por una entidad de certificación.

## Navegador

`python3 campus/build.py` genera `campus/dist/rutas.html`: seis rutas, etapas, módulos, cadena de prerrequisitos, fuentes, certificaciones, impresión y progreso local opcional. No sube progreso, no tiene cuentas, no recoge datos de clientes y no expide certificados. El contenido nuevo de orientación es español; el campus troncal mantiene ES/EN.

## Procedencia e independencia

Rutas incorporadas desde `WiktorNykiel/fundamentos-ciberseguridad`, commit `5aba8b141d12507fad2d87a48cca98e8be433b88`. `sources.json` y `credentials.json` conservan únicamente identificadores, títulos y enlaces necesarios para estas etapas; el catálogo completo, casos y plantillas se mantienen en el repositorio independiente Awesome DPD. La compilación del campus funciona sin descargar ni ejecutar ese proyecto. El examen de informática y el aula de sistemas conservan sus propios registros.
