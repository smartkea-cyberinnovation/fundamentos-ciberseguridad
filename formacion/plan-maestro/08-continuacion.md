# 08 · Continuación, prioridades y requisitos del campus

[Índice](README.md) · [Mapa](01-mapa-curricular.md) · [Fuentes](09-fuentes.md) · [English overview](OVERVIEW.en.md)

## Estado que debe conservarse

Referencia basada en Campus 2.2 y commit `2f8b8d2614638d9a034e1cac92fb16c6e75bb6c5`. El curso activo conserva M01–M32, 96 fichas y 480 horas. Este directorio añade arquitectura curricular y diseños; no activa 108 unidades nuevas en el compilador ni declara ya traducido todo el campus.

**Entregado en esta ampliación:** 18 áreas, 108 unidades propuestas, ocho patrones de arquitectura, 22 categorías CSF con ejemplos, 12 familias de correspondencias parciales, un método de riesgos con caso numérico, 24 escenarios de laboratorio y 110 entradas de glosario. **Pendiente:** lecciones completas por unidad, traducción íntegra ES/EN, nuevas rutas de aprendizaje en la web y validación de ejecución nativa.

No reutilizar cifras de pruebas de una edición como si validaran la siguiente. Cada entrega debe registrar commit, archivos, comprobaciones ejecutadas, fallos, pruebas omitidas y límites.

## Orden recomendado de implementación

| Prioridad | Entrega | Criterio de aceptación |
|---|---|---|
| P0 | Contrato curricular y compatibilidad | Conservar M/L IDs y progreso; relacionar Axx.Uxx sin renumerar; distinguir horas existentes y ampliación |
| P1 | Informática y terminal A01–A03 | Teoría explicada, ejemplos y prácticas comparables; ES/EN completas en las unidades incorporadas |
| P2 | Redes, virtualización, web y cloud A04–A08 | Diagramas, variantes por recursos, versiones, costes, copias y pruebas de recuperación |
| P3 | Amenazas, protecciones, equipos y riesgos A09–A12 | Escenario–control–evidencia–dueño; cálculos y correspondencias parciales verificables |
| P4 | AppSec, Blue Team, CTI y resiliencia A13–A16 | Casos sintéticos, aislamiento, triaje, evidencia, retest y restauración |
| P5 | IA y proyectos A17–A18 | Evaluación independiente y defensa individual; no ejecución autónoma de órdenes |
| P6 | Continuidad entre dispositivos y cuentas opcionales | Requisitos de seguridad/privacidad aprobados y pruebas antes de activar backend |

La traducción y accesibilidad se trabajan en cada entrega, no se posponen hasta el final. La secuencia técnica puede variar por ruta profesional, pero no se omiten prerrequisitos sin prueba de nivel.

## Contrato de unidad y rutas

Cada unidad debe tener ID estable, slug, área, versiones de contenido, idioma, prerrequisitos, objetivos, términos de glosario, teoría, ejemplos, herramientas, laboratorio, evidencia, evaluación, fuentes y estado de revisión. Separar metadatos de interfaz y contenido. Registrar las horas solo después de decidir reutilización y pilotar actividades; no multiplicar automáticamente 108 por una duración estándar.

Rutas: inicial; administración Linux; Windows/identidad; macOS; cloud/plataforma; SOC/Blue; GRC/riesgos; CTI; DFIR; AppSec/Purple. Una ruta selecciona unidades y resultados, no crea copias divergentes del mismo material. El progreso puede mostrar área, módulo y unidad, manteniendo el historial de la edición anterior.

**Índices:** mapa general; índice por área; tabla de contenidos de cada unidad; índice de prácticas; glosario; biblioteca de fuentes; rutas por perfil y búsqueda. Los enlaces profundos deben abrir el recurso y apartado correctos y mostrar cómo volver a la ruta de estudio.

## Bilingüismo ES/EN completo: criterio, no etiqueta

Mantener los mismos IDs de unidad, laboratorio, evaluación y control en ambos idiomas. Traducir teoría, instrucciones, errores, botones, ayuda, feedback y referencias descriptivas. No traducir nombres de comandos, rutas técnicas ni valores que deban permanecer literales. La salida de ejemplo de una herramienta puede variar por locale y debe estar etiquetada.

Mostrar `lang` correcto para página y fragmentos. El selector de idioma conserva unidad, sección y progreso; no marca como completada una unidad por alternar idioma. Registrar `translation_status` y revisión por idioma; un resumen inglés no permite etiquetar todo el curso como bilingüe terminado. En esta edición únicamente existe una visión general en inglés y terminología bilingüe.

Pruebas: paridad de IDs, ausencia de textos de interfaz sin traducir, enlaces internos, citas, overflow con cadenas largas, fechas/números y estados de autoevaluación. La revisión humana de vocabulario técnico sigue siendo necesaria.

## Móvil, iPad y portátil

Objetivo de diseño: lectura cómoda y navegación funcional desde 320 píxeles CSS, teléfonos de aproximadamente 390, tabletas de 768/820, anchuras 1024 y escritorio, en vertical/horizontal y pantalla dividida. Estos tamaños son casos de prueba, no sustituyen probar navegadores/dispositivos reales. Incluir Safari/iPadOS y sus restricciones de almacenamiento, descarga y portapapeles; no atribuir validación iPad por pasar solo Chromium con viewport pequeño.

Patrones: una columna en móvil, índice plegable con ubicación visible, botones anterior/siguiente accesibles, área de acción sin tapar texto, tablas con scroll interno o tarjetas equivalentes, código con desplazamiento propio, tipografía ampliable, sin dependencias de hover y foco visible. Presentación y lectura deben tener salidas y navegación por teclado; no ocultar el final de una sección larga.

Tomar WCAG 2.2 AA como objetivo verificable: contraste, reflow, teclado, foco, nombres accesibles, tamaño/separación de controles y autenticación accesible, entre otros criterios. Ninguna captura o conjunto pequeño de tests acredita toda la conformidad. [S33]

El móvil sirve para leer teoría, planificar, seguir pasos y registrar notas. La práctica indica cuándo requiere VM, teclado o SO nativo. No mostrar «ejecutado» al copiar un comando ni marcar una competencia Windows/macOS por leer su ficha en teléfono.

## Diseño editorial independiente

Interfaz clara con blanco, grafito, grises suaves y un rojo de acento como dirección de diseño; el color nunca será la única señal de estado. Tipografía legible, jerarquía editorial, espacios amplios y tablas sobrias. Validar contraste antes de fijar tokens. No copiar ni incorporar logo, nombre, sello, fotografías institucionales o declaraciones de afiliación. La eventual autorización de identidad es una tarea independiente y no se da por concedida.

## Continuidad entre dispositivos: tres capacidades diferentes

| Modalidad | Qué transfiere | Requisito y límite |
|---|---|---|
| Compartir enlace a la lección | Ruta, idioma y apartado | No transfiere sesión ni necesariamente progreso; debe funcionar sin cuenta |
| Transferir progreso | Copia mínima de hitos y ruta; notas solo si se eligen expresamente | Importación validada y confirmación; no equivale a autenticación ni sincronización continua |
| Cuenta y sincronización | Identidad y estado asociado en un backend | Autorización por usuario, conflictos, retención, borrado, controles y operación |

**Primera entrega preferida:** mantener exportación/importación JSON existente y añadir un flujo claro «Continuar en otro dispositivo». Permitir compartir la URL de lectura mediante el sistema del dispositivo o copiarla; explicar que el archivo de progreso se transfiere por separado hasta que exista un mecanismo adicional seguro. No declarar que una URL transporta estado cuando solo apunta a una lección.

**Enlace de traspaso futuro:** no poner cookies, access tokens, refresh tokens, correo ni notas en texto claro en parámetros. Preferir una referencia opaca de uso limitado a un paquete mínimo, de caducidad corta y con recuperación/importación explícita. El receptor debe ver origen/fecha/resumen y confirmar; las vistas previas de correo o mensajería no deben consumir la operación mediante un GET. El enlace es una capacidad de acceso temporal y su reenvío tiene consecuencias: minimizar datos, limitar uso, registrar consentimiento e invalidación. La solución necesita modelo de amenazas y pruebas; no está implementada en esta referencia.

Una alternativa sin backend puede diseñar un paquete cifrado local, pero no resuelve por sí sola entrega segura de clave, revocación, tamaño de URL o permanencia del mensaje. No inventar criptografía ni presentar un fragmento URL como secreto automáticamente protegido. Mantener el método de archivo validado como alternativa.

## Acceso opcional por correo OTP, sin contraseña

Tratarlo como **nuevo componente de identidad**, no como un ajuste cosmético de Pages. Preferir un proveedor o biblioteca mantenida, con envío de correo autorizado, antes que implementar autenticación propia apresurada. Definir alcance del usuario y datos mínimos; acceso público a teoría debe seguir siendo posible cuando no requiera cuenta.

Requisitos de aceptación propuestos: códigos impredecibles y de un solo uso, caducidad breve, vinculación al intento, límites de envío/intentos por contexto, respuesta que no enumere cuentas, protección frente a reenvíos/reutilización, almacenamiento adecuado de verificadores y logs sin códigos. Las sesiones deben gestionarse con cookies y atributos apropiados, protección CSRF/origin y revocación/cierre. Los tokens de sesión no se comparten por WhatsApp/Telegram/correo para «arrastrar sesión».

El control del buzón no prueba identidad civil ni implica resistencia al phishing. Separar recuperación de cuenta, cambio de correo y acceso normal. Definir tratamiento de errores de entrega, cuentas duplicadas y eventual acceso de menores antes de publicar. Estos son requisitos propuestos de ingeniería y privacidad, no una autenticación ya validada.

**Backend y sincronización:** API con autorización por propietario en cada lectura/escritura; sin confiar solo en IDs enviados por el cliente. Versionar estado, reconciliar conflictos y borrados, probar dos dispositivos simultáneos y exportar/eliminar datos. Proteger secretos en el servicio, no en JavaScript distribuido. Evaluar finalidad, base jurídica, encargado, ubicación/transferencias, conservación y derechos conforme al tratamiento. [S07]

## Cloudflare: separar la publicación de contenidos y el laboratorio

Para la web estática, conservar la guía vigente `campus/DEPLOY-CLOUDFLARE.md`. Pages puede servir HTML estático; los flujos de Workers y Pages tienen configuraciones diferentes. [S34] No añadir OpenNext o desplegar la aplicación Next.js de referencia solo para mostrar Markdown.

Los logs históricos aportados mostraban una autodetección de Next.js y errores de configuración de Worker, no una prueba de que el campus actual estuviera desplegado. No copiar esos logs íntegros al repositorio público ni publicar identificadores de cuenta. Antes de afirmar éxito, comprobar la URL real, commit servido, recursos, cabeceras y recorrido de estudiante. Esta ampliación no cambia cuentas ni despliega recursos.

La identidad/sincronización opcional puede requerir funciones/API y almacenamiento; el laboratorio de sistemas requiere otra infraestructura aislada. Ninguno se introduce ocultamente como dependencia del sitio estático.

## Definición de terminado por entrega

Contenido ES/EN de las unidades incluidas; fuentes trazables; práctica con evidencia/rollback; pruebas positivas/negativas; controles de seguridad; navegación/índices correctos; compatibilidad del progreso; pruebas de dispositivos declarados; paquetes de publicación verificados; documentación de lo que no se ejecutó. Si falta una parte, indicar exactamente su estado sin etiquetar toda la entrega como «completa».

## Instrucción de continuidad para la próxima interacción

> Continuar desde `formacion/plan-maestro/README.md` y `08-continuacion.md` del repositorio `smartkea-cyberinnovation/fundamentos-ciberseguridad`. Leer primero main y cambios pendientes. Desarrollar A01 y A02 con teoría explicada, ejemplos GUI/CLI, prácticas, pruebas y evaluación en ES/EN, reutilizando M01–M06/M11–M16/M21 sin romper IDs ni progreso. Diseñar la incorporación gradual de A03–A18. Mantener identidad visual independiente y clara. Validar lectura, presentación, índices y asistente en móvil/tableta/portátil. Separar compartir una lección, transferir progreso y autenticación OTP. No exponer aplicaciones vulnerables ni ejecutar comandos del alumno desde el campus. Actualizar el catálogo y registrar pruebas y límites reales antes de integrar.

Para elegir otra prioridad, basta indicar el área Axx o la capacidad; el resto de requisitos queda guardado aquí y no necesita repetirse.
