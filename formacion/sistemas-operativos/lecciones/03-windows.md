# 03 · Windows: interfaz, lenguaje y objetos administrativos

## CMD y BAT no son PowerShell

CMD interpreta comandos y lotes de texto. PowerShell añade un lenguaje con objetos y cmdlets. Un script BAT pequeño sigue siendo útil para entender entornos heredados; no debe obligarse a resolver en BAT una tarea con JSON, errores complejos y APIs administrativas. Microsoft recomienda PowerShell para automatización Windows moderna. [S03](../FUENTES.md)

El ejercicio `resumen.cmd` cuenta archivos del dataset conocido. El equivalente PowerShell recibe una ruta literal, inspecciona objetos y suma su propiedad `Length`. No invoca el script Python para simular administración. Su resultado debe compararse con la referencia, pero no se afirma haberlo ejecutado en Windows durante esta edición.

## Entender los objetos antes del pipeline

Desde el directorio del curso, en una VM Windows:

```powershell
Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force | Get-Member
Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force |
    Select-Object Name, Length, Attributes
```

La primera orden permite estudiar tipos y miembros. La segunda selecciona propiedades: no convierte la tabla visual en un formato de intercambio. Si se necesita CSV o JSON, se exportan los objetos antes del formato final. Cuando se ejecuta un programa nativo puede producirse texto: no atribuyas automáticamente propiedades estructuradas a cualquier salida que atraviese `|`. [S04]

## Versiones y contextos

Registra `$PSVersionTable` y qué módulo proporciona cada cmdlet. PowerShell instalado en Linux no hace aparecer los servicios, Registro, NTFS o APIs de un Windows inexistente. Windows PowerShell 5.1 y PowerShell 7 pueden diferir en codificaciones y disponibilidad de módulos; los scripts y tests deben reflejar el motor usado. El kit emite JSON con caracteres escapados para que sus datos de referencia no dependan del aspecto de la consola.

La execution policy ayuda a controlar las condiciones en que se ejecutan scripts, pero Microsoft no la define como frontera de seguridad. No se resuelve una práctica cambiando a una política global permisiva. El docente debe proporcionar un mecanismo de ejecución aprobado, respetando firma, procedencia y políticas existentes. [S04]

## Permiso declarado y permiso efectivo

Una ACL contiene reglas, pero la autorización también depende de identidad, grupos, herencia y ámbito. Observar `Get-Acl` no sustituye una prueba con el usuario previsto. Antes de cambiar permisos, identifica carpeta, usuario y necesidad. Usa una copia de laboratorio y conserva el estado anterior. No practiques con la raíz del disco ni con perfiles reales.

En servicios y tareas, separa identidad de configuración y estado de ejecución. Que una tarea esté definida no garantiza que se haya ejecutado; que un proceso siga activo no implica que su servicio responda correctamente. La GUI ayuda a visualizar la relación; la CLI y el log permiten documentarla.

## Eventos con contexto

Para una consulta nativa, selecciona canal, proveedor e intervalo. Un Event ID sin esos datos no es una evidencia completa. Ausencia de eventos puede significar política no activada, falta de permiso o retención insuficiente. Sysmon aporta telemetría adicional cuando está instalado y configurado; no se da por presente en todas las máquinas. [S06]

Completa [R03](../practicas/R03-windows.md). En la defensa explica por qué un conteo correcto del dataset no acredita dominio de AD, WinRM o administración completa del endpoint.
