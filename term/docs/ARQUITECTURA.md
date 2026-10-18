# Arquitectura de TERM

## Tres componentes

| Componente | Responsabilidad | Estado que conserva |
|---|---|---|
| Curso estático en Cloudflare Workers | Servir contenido, manual, recursos y JavaScript de aprendizaje | Archivos de la versión publicada |
| Navegador del alumno | Navegar, buscar, responder, tomar notas y gestionar su progreso | LocalStorage de este origen; copia JSON exportable |
| Laboratorio Linux con ttyd | Ejecutar procesos reales y mostrar su terminal | VM, archivos del alumno y registros configurados por el operador |

El curso no incorpora un endpoint de ejecución de comandos ni hace de proxy de SSH. La copia de una orden es una acción explícita. El alumno decide cuándo pegarla en su terminal. La salida orientativa de cada paso es contenido docente y siempre se identifica como ejemplo.

## Flujo de ejecución real

El navegador abre el origen HTTPS configurado para ttyd. Cloudflare Access autentica al usuario; el Tunnel conecta con la VM y valida la política según la configuración de su ingress. ttyd inicia la shell bajo el usuario fijado en el contenedor. La VM es la frontera de separación entre alumnos para las prácticas administrativas.

Una sesión de iframe se habilita solo si el operador declara el origen concreto en el build y permite explícitamente esa presentación. Abrir una pestaña independiente es el modo de conexión inicial porque los proveedores de identidad pueden limitar su autenticación en marcos. El navegador no deduce una conexión correcta de un evento `load` del iframe.

## Separación de privilegios

- El alumno usa su VM para sudo, gestión de servicios, paquetes y Docker.
- El contenedor ttyd no recibe `docker.sock`, red de anfitrión, modo privilegiado ni montajes del sistema.
- El laboratorio web y la caja de herramientas comparten una red interna de ejercicios.
- Los contenedores comparten kernel con su anfitrión; no ofrecen la misma separación que VMs dedicadas.
- Una política Access autoriza el acceso al endpoint. Por sí sola no crea usuarios Linux ni separa archivos dentro de una VM compartida.

## Publicación y rutas

El repositorio conserva el Worker `fundamentos-ciberseguridad` y su campus general en `/introduccion-ciberseguridad/`. La compilación añade los archivos de TERM bajo `/fundamentos-ciberseguridad/term/`, con una ruta específica del Worker. No se captura la raíz del dominio.

El staging conserva el contenido original del campus y valida por separado la salida TERM. Cada conjunto tiene manifiesto SHA-256; el manifiesto exterior cubre ambos. Las cabeceras del campus se restringen a su prefijo y TERM recibe su propia CSP. Esto evita que dos políticas CSP coincidentes impidan el iframe autorizado.

## Datos y persistencia

Las notas admiten hasta 6.000 caracteres por lección. La importación limita el tamaño a 2 MB, comprueba identidad del curso, IDs, opciones y tipos, y requiere revisar la sustitución de datos locales. El texto se escapa al mostrarlo y no se interpreta como HTML.

El porcentaje representa lecciones que el alumno marca como aprendidas. Los pasos y niveles de evidencia también son declaraciones del alumno. El docente contrasta la evidencia real durante la evaluación. El producto no emite certificados ni afirma comprobar automáticamente el sistema remoto.

## Alcance de la primera edición

Incluye curso, manual, ejercicios, cuestionarios, progreso, cuaderno, scripts y despliegue de laboratorio. Una máquina nueva requiere que el operador facilite infraestructura, nombre DNS, Tunnel y política Access. La primera publicación no configura una máquina no identificada ni abre un shell público.

## Referencias técnicas

- [Cloudflare Static Assets en una subruta](https://developers.cloudflare.com/workers/static-assets/routing/advanced/serving-a-subdirectory/).
- [Cabeceras de Static Assets](https://developers.cloudflare.com/workers/static-assets/headers/).
- [ttyd: opciones oficiales](https://github.com/tsl0922/ttyd).
- [Seguridad de Docker Engine](https://docs.docker.com/engine/security/).
