# 04 · macOS no es Linux con otra apariencia

## Capas y almacenamiento

Darwin proporciona una base Unix, pero macOS incorpora componentes propios, políticas y herramientas específicas. Relaciona Finder con rutas, Monitor de Actividad con procesos y Utilidad de Discos con APFS. Un volumen APFS no debe tratarse automáticamente como una partición independiente con espacio totalmente reservado. La configuración y el hardware condicionan controles de arranque e integridad; no transfieras sin verificar una conclusión entre Intel y Apple Silicon. [S07](../FUENTES.md)

Distingue contenido y contexto: una copia puede conservar bytes sin conservar todos los atributos extendidos o ACL. También puede cambiar qué fecha representa cada campo. Antes de usar un procedimiento en investigación, define qué debe preservarse y cómo se verifica.

## Intérprete y herramientas

`zsh`, Bash y las utilidades del sistema tienen versiones independientes. El shebang selecciona intérprete; lanzar un script explícitamente con otro puede ignorar esa elección. Que la terminal interactiva use zsh no convierte un archivo Bash en zsh. Las opciones de programas BSD/GNU tampoco son intercambiables por pertenecer a entornos Unix.

El resumen zsh usa una expansión con calificadores para incluir ocultos y tratar un patrón sin resultados como lista vacía. El ejemplo Bash usa opciones de shell distintas. Ambos persiguen contar el mismo dataset, no demostrar que los lenguajes son idénticos. [S16]

## launchd y entorno

Un LaunchAgent se relaciona con el ámbito de una sesión/usuario; un LaunchDaemon tiene otro contexto. Empieza interpretando una definición, su identidad y sus rutas antes de programar tareas. El PATH interactivo no debe asumirse en launchd. Una preferencia escrita tampoco demuestra que un proceso ya la haya aplicado.

En la práctica avanzada del módulo, el docente autoriza un agente benigno con rutas concretas, log propio y baja documentada. No se utilizan mecanismos de autoinicio para ocultar actividad. La falta de ejecución se investiga con configuración y registros, no quitando controles de seguridad.

## Controles que se complementan

Permisos de archivo, TCC, Gatekeeper, firma/notarización, SIP, FileVault y controles de arranque atienden problemas distintos. Un acceso denegado puede ser el resultado correcto de un control. Identifica la capa y el permiso mínimo; no concedas acceso completo al disco para resolver cualquier fallo. Nunca retires cuarentena o desactives integridad como preparación genérica del laboratorio. [S07]

FileVault debe estudiarse junto con recuperación y custodia: una casilla marcada no resuelve todo el ciclo de vida de los datos. Keychain se aborda como almacén protegido, no como fuente que volcar en un inventario.

## Logs y cobertura real

Unified Log requiere seleccionar ventana, componente y contexto; parte de la información puede estar redactada o no conservarse. No supongas que el historial de shell enumera toda la ejecución del equipo. Para la práctica offline se aportan eventos JSON claramente sintéticos: no se presentan como exportaciones nativas del sistema.

Completa [R04](../practicas/R04-macos.md) en un Mac autorizado. Sin Mac, puedes razonar sobre la sintaxis y analizar datos, pero la administración nativa queda pendiente. Esa limitación debe aparecer en el expediente, no desaparecer en la nota final.
