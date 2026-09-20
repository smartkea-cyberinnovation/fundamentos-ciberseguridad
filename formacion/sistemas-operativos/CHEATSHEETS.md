# Guías rápidas de consulta y comprobación

Estas fichas son recordatorios conceptuales. Las herramientas por tarea están en [la referencia cruzada](REFERENCIA-CRUZADA.md); el desarrollo y las prácticas están en los módulos. No se entrega un script que modifique automáticamente un sistema.

## Antes de trabajar

Identificar equipo, sistema, versión, usuario, permisos, directorio y alcance. Formular el resultado esperado. Consultar ayuda de la herramienta instalada. Para cambios, preparar copia y reversión. Distinguir observación de modificación.

## Linux y Bash

Revisar rutas y expansiones; considerar nombres con espacios y Unicode; distinguir texto literal y patrones; separar datos de errores; comprobar resultados de cada etapa. No presuponer que el entorno de una tarea programada coincide con una sesión interactiva. Validar argumentos y limitar operaciones al directorio previsto.

## Windows y PowerShell

Identificar motor, módulo y edición. Distinguir CMD, BAT y PowerShell. Preferir propiedades de objetos frente a texto de tablas. Formatear al final, no antes de exportar datos. Verificar permisos efectivos y contexto de ejecución. Interpretar los códigos de retorno según la herramienta concreta.

## macOS

Identificar arquitectura y versión. Separar zsh y Bash; distinguir utilidades GNU y BSD. Revisar metadatos además del contenido cuando importe la preservación. Diferenciar permisos de archivos, controles de privacidad y seguridad de plataforma. No considerar un contenedor Linux una validación nativa.

## Diagnóstico

Síntoma y alcance; estado del host; recursos; identidad y permisos; red y resolución; transporte; confianza TLS; aplicación; dependencias; logs. Seleccionar comprobaciones según hipótesis, no ejecutar todas indiscriminadamente. Aplicar el cambio mínimo y verificarlo mediante una segunda observación.

## Acceso y transferencia

Definir destino y propósito; verificar identidad; limitar permisos; utilizar canal aprobado; comprobar integridad y atributos; cerrar sesión; revisar registro y retirar acceso temporal cuando corresponda. Las credenciales nunca forman parte de la documentación entregada.

## Evidencias e indicadores

Conservar original, crear copia de trabajo y registrar transformaciones. Normalizar sin perder el valor original. Buscar sobre campos explícitos, probar controles positivos y negativos, corroborar coincidencias y explicar cobertura. Una coincidencia aislada no acredita compromiso.

## Automatización e IA

Contrato de entrada/salida, errores explícitos, pruebas y revisión. La IA propone, no aprueba ni ejecuta automáticamente. Minimizar datos, validar salida estructurada y contrastar con evidencia independiente. Registrar límites y resultados no comprobados.
