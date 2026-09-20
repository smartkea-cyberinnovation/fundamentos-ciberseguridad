# Editorial design / Diseño editorial

## Español

Identidad independiente: fondo blanco, rojo profundo `#b0142f`, rojo de enlaces `#870b23`, texto carbón `#23252b`, texto secundario `#555b66` y superficie `#f7f6f4`. Se emplean fuentes del sistema y un símbolo genérico de terminal. No se incorporan logotipos, nombres, sellos, fuentes corporativas redistribuidas o afirmaciones de afiliación de terceros.

La prioridad es leer y localizar la siguiente acción: títulos jerárquicos; ancho de lectura limitado; interlineado amplio; teoría, fichas y evaluación con accesos separados; tareas en cinco fases; indicadores explícitos de estado; controles principales de al menos 44 px. Código y tablas se desplazan dentro de su bloque, no arrastran el documento completo. La altura real del encabezado se mide para que los enlaces internos no oculten el título tras el menú.

El menú lateral se convierte en panel desplegable en tabletas y móviles. A 760 px o menos, las cuadrículas pasan a una columna y el buscador usa una fila completa. Hay ajustes a 360 px, zonas seguras, texto ampliado, foco visible y reducción de movimiento. La presentación conserva contenido largo mediante desplazamiento interior en lugar de recortarlo.

Pruebas previstas: dos idiomas, todos los módulos/pestañas, índice, lector, asistente, progreso y compartir; anchuras 320, 360, 390, 768, 820, 1024 y 1440 px; Chromium y WebKit. Consultar la ejecución concreta en Actions: tener reglas responsive y contrastes calculados no constituye conformidad WCAG ni prueba física en iPad.

## English

Independent light editorial identity: white surfaces, deep red accents, charcoal text and system fonts. No third-party institution name, logo, seal or endorsement. Visual hierarchy prioritizes reading and the learner's next action rather than decorative effects.

The layout adapts from a persistent sidebar to a collapsible navigation panel. Cards become single-column on phones; code and tables scroll internally. Header measurement preserves anchor visibility when labels wrap or a tablet rotates. Large-text mode, visible focus, keyboard navigation, reduced motion and safe-area spacing support accessible use.

Automated contrast checks and responsive viewport tests are scoped evidence, not certification. Chromium and WebKit acceptance does not establish behavior on every Safari/iPadOS release or physical device. See [QA.md](QA.md) for executed checks and limits.
