# R07 · Un cambio mínimo, verificado y reversible

**L30C · 3 h.** Entrada: M30. Entorno: archivo ficticio en `salida`, no configuración real de un servicio. [Bastionado](../BASTIONADO.md) y [lección 06](../lecciones/06-evidencias.md). Objetivo: demostrar el ciclo de cambio y distinguirlo de conformidad integral del SO.

## Variante Linux

Copia `mi-laboratorio/datos/hola.txt` a `mi-laboratorio/salida/config.txt`. Comprueba ruta y propiedad antes de continuar. Desde la raíz del curso:

```bash
modo_inicial=$(stat -c '%a' mi-laboratorio/salida/config.txt)
printf 'Modo observado: %s\n' "$modo_inicial"
chmod 600 mi-laboratorio/salida/config.txt
stat -c '%a %U %G' mi-laboratorio/salida/config.txt
chmod "$modo_inicial" mi-laboratorio/salida/config.txt
stat -c '%a' mi-laboratorio/salida/config.txt
```

No uses sudo: es un archivo propio del ejercicio. No copies estas opciones GNU a macOS sin consultar su manual. Demuestra que el contenido sigue igual y que el modo final coincide con el inicial; no supongas que siempre comenzó en 644.

## Variante Windows/macOS

En Windows guarda la ACL del archivo de prueba con `Get-Acl`, inspecciona herencia en GUI y redacta el cambio mínimo. La modificación y restauración de ACL se realizan solo con aprobación docente y cuentas de práctica. En macOS, distingue permisos Unix, ACL y controles de privacidad; utiliza la sintaxis nativa de `stat` para leer el estado. Ninguna variante modifica políticas globales.

## Prueba negativa y alcance

Con una segunda cuenta ficticia preparada por el docente, comprueba el acceso permitido/denegado. Si solo tienes una cuenta, registra que esa parte no se ejecutó: leer la ACL no demuestra por sí solo una prueba negativa. No abras cuentas reales ni concedas acceso global para completar la entrega.

## Producto esperado

Ticket con estado inicial, objetivo, impacto, aprobación, copia, cambio, prueba funcional, prueba negativa —o pendiente—, rollback y riesgo residual. El permiso de este archivo es solo un control: no autoriza afirmar “máquina bastionada” o “conforme a CIS”.

## Recuperación

Restaura el estado inicial del archivo y contrasta contenido/permisos. Retira solo la copia después de evaluar. Las comprobaciones nativas de ACL, identidades y políticas necesitan validación por el docente; los tests del kit no las sustituyen.
