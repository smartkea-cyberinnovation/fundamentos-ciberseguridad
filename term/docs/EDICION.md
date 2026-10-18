# Editar y ampliar TERM

## Fuentes de contenido

`content/core.json` contiene módulos 01–08 y `content/security.json` módulos 09–16. Cada módulo tiene ID estable y tres lecciones. El generador crea la web y el manual a partir de la misma fuente, por lo que la corrección de un comando se refleja en ambas vistas.

Campos de la lección: ID, título, minutos orientativos, resumen, objetivos, prerrequisitos, secciones, pasos, reto, cuestionarios, ideas clave y fuentes. Un paso tiene comando, shell, explicación, salida esperada, verificación, reversión, entorno y precauciones.

## Criterios editoriales

1. Un concepto por sección. Conectar definición con una operación y su evidencia.
2. Comandos con entorno explícito y datos sintéticos. No usar un dominio real como objetivo de escaneo.
3. Distinguir prueba local, demostración, ejercicio diseñado y ejecución acreditada.
4. Preguntas con cuatro opciones y explicación de la opción correcta.
5. Retos con pistas, solución razonada y rúbrica observable.
6. Referencias primarias con URLs HTTPS; consultar la documentación de la versión instalada.
7. Mantener IDs publicados para conservar enlaces y progreso.

No incluir HTML activo en el contenido. El renderizado escapa el texto; se admiten únicamente pequeñas convenciones visuales para código en línea y negrita.

## Validaciones

El build exige los 16 módulos completos, 48 lecciones y 96 preguntas. Los tests comprueban sintaxis de comandos sin ejecutarlos y controles de importación, URLs y empaquetado. Las pruebas de navegador recorren vistas y acciones críticas. Las pruebas Docker se ejecutan en un anfitrión habilitado; la ausencia de Docker no se registra como éxito.

Los archivos del zip de laboratorio se enumeran en `labs/public-files.json`. Añadir una herramienta requiere revisar su Dockerfile, compatibilidad y alcance antes de añadir su ruta al inventario.

## Cómo conservar independencia

Todo lo propio de Linux TERM está en `term/`. El campus usa un adaptador de construcción para integrar la salida bajo su prefijo. Se puede publicar la salida estática de TERM por separado. Una futura formación PowerShell/CMD/BAT tendrá su propio contenido, identificadores y namespace de progreso para evitar mezclar recorridos.
