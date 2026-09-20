# 01 · De una ventana a un sistema: terminal, bytes y archivos

## El modelo antes del comando

Una terminal presenta entrada y salida. La shell interpreta la línea: separa palabras, expande algunas expresiones, prepara redirecciones y solicita ejecutar un programa. El kernel controla recursos y permisos. Un error puede pertenecer a cualquiera de esas capas; volver a ejecutar como administrador no explica cuál falló. En una VM hay además un anfitrión: la consola puede estar mostrando un sistema distinto al que crees. [S01](../FUENTES.md)

Haz esta explicación con una acción pequeña: abrir `hola.txt` en el explorador y después leerlo en terminal. La ubicación visible, la ruta usada, el proceso lector y el usuario son diferentes aspectos del mismo trabajo. Conserva esa distinción al pasar a servicios web, a una tarea programada y a una sesión remota.

## Bytes, caracteres y representación

El dataset tiene ocho archivos y 62 bytes de contenido. Ese tamaño no es el espacio asignado en disco, ni incluye el tamaño del nombre, ACL o directorio. `unicode.txt` contiene 19 bytes en UTF-8: la `ü` ocupa más de un byte. `lineas-lf.txt` ocupa 8 bytes; `lineas-crlf.txt`, 10. Se leen de forma parecida, pero sus hashes difieren. Este es un ejemplo creado para el curso, no un hallazgo de seguridad.

Distingue tres preguntas: ¿son iguales los bytes?, ¿representan el mismo texto?, ¿tienen los mismos metadatos? Cada pregunta requiere una comprobación diferente. Un algoritmo hash responde a la primera dentro de sus propiedades y del método de adquisición; no interpreta la intención del archivo.

## Rutas y argumentos

Desde `mi-laboratorio`, `datos/hola.txt` es una ruta relativa. Cambiar de directorio cambia su significado. Una ruta absoluta evita esa dependencia, pero puede incorporar nombres personales y dificultar compartir instrucciones. En un script se suele recibir una ruta como parámetro y validarla.

En Bash, las comillas de `"datos/con espacios.txt"` hacen que el programa reciba un argumento. Sin comillas, el espacio puede separar palabras. El archivo `-opcion.txt` enseña otro problema: algunos programas interpretan un nombre iniciado por guion como opción. Usar la ruta `datos/-opcion.txt` o un separador de opciones admitido por la utilidad evita ambigüedad. No todos los programas comparten el mismo convenio. [S01]

## Archivos visibles y ocultos

El dataset incluye `.nota.txt`. En Linux y macOS, un nombre iniciado por punto se suele omitir en listados ordinarios de shell; no está cifrado por ello. En Windows, nombre y atributo oculto no son la misma cosa. El manifiesto cuenta también ese archivo. Contrasta la GUI configurada para mostrar elementos ocultos con la lista CLI. No concluyas que un archivo es malicioso por estar oculto.

## Entradas, resultados y errores

stdout lleva resultados y stderr lleva diagnósticos según el contrato del programa. El código de salida informa cómo terminó. Una herramienta puede producir algo de salida y aun así fallar; conservar solo lo visible en pantalla puede ocultar el problema. En el kit, una búsqueda sin coincidencias termina correctamente con `count: 0`, mientras que un JSON inválido produce error y código 2. Es una decisión explícita de diseño.

Comprueba primero la orden correcta; después repítela con una ruta inexistente. Anota qué canal contiene cada dato y cuándo capturas el código de salida, porque la orden siguiente puede sustituirlo. No redirijas stdout sobre el mismo archivo que estás leyendo: la shell puede truncar el destino antes de que el programa abra la entrada. [S01]

## Cierre y transferencia a ciberseguridad

Un investigador necesita conocer el significado de bytes, rutas y metadatos antes de interpretar una diferencia. Un administrador necesita detectar una ruta incorrecta antes de cambiar permisos. Un analista SOC necesita separar resultado vacío y error de consulta. Entrega una página con esas tres explicaciones y un ejemplo propio sobre datos ficticios. Continúa en [R01](../practicas/R01-archivos.md).
