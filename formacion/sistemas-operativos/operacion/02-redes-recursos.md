# Control operativo: redes, carpetas y recursos compartidos

**D23 · Edición docente ES/EN · 21 de septiembre de 2026.** Profundiza M07, M09, M10, M17, M18, M22 y M24. Consultar [identidades](#/recurso/D22), [navegación](#/recurso/D24) y [detección/pruebas](#/recurso/D25). Las configuraciones se estudian en redes y cuentas asignadas; no se modifica una red corporativa desde el campus.

## 1. Modelar el acceso antes de configurar

Un recurso compartido no es solo una carpeta visible. Identificar servicio, servidor/NAS, protocolo, ubicación de datos, identidad de acceso, grupos, permisos, red de origen, cifrado, auditoría, backup y responsable. El acceso depende de todas las capas relevantes; una regla de firewall que permita SMB no concede lectura de archivos.

Modelo: persona/cuenta → sesión y grupos → ruta de red → autenticación del servicio → permiso del recurso compartido → permiso del objeto → controles adicionales. Dibujar por separado el acceso local al archivo y el remoto: el acceso local no atraviesa necesariamente la ACL del recurso compartido.

Para Windows SMB, analizar conjuntamente permisos de compartición y NTFS; un acceso remoto necesita superar ambos controles. No reducirlo a una suma aritmética de permisos: importan identidad, token, herencia y denegaciones aplicables. En Samba también intervienen identidad Unix, mapeo y permisos del host. [Samba: smb.conf](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html).

## 2. Diseño de carpetas por roles

Ejemplo sintético: `curso.test`, grupos LectoresProyecto, EditoresProyecto y CustodiosProyecto. Lectores abren documentos; editores modifican contenido permitido; custodios administran permisos con identidad separada. Evitar permisos concedidos directamente a individuos salvo excepción documentada.

| Recurso | Lectores | Editores | Custodios | Invitados |
|---|---|---|---|---|
| Material publicado | Leer | Leer | Administrar según rol | Leer solo si es público |
| Entregas de equipo | Leer lo autorizado | Crear/modificar lo autorizado | Recuperar y gestionar ACL | Sin acceso |
| Evidencia restringida | Sin acceso general | Sin acceso general | Acceso nominal aprobado | Sin acceso |

La tabla es un diseño, no una configuración aplicada. Para cada celda, definir qué operaciones concretas se prueban: listar, abrir, crear, modificar, renombrar, borrar, cambiar ACL y acceder por ruta directa. Ocultar una carpeta o un share en la enumeración no equivale a impedir acceso directo.

La herencia reduce trabajo, pero debe revisarse al mover datos. Comparar permisos antes y después de copiar o mover dentro de un volumen, entre volúmenes y mediante herramientas de backup. No asumir que todos los métodos preservan propietario, ACL, etiquetas o atributos de la misma forma.

## 3. Windows, Samba/NAS y NFS

**Windows/SMB.** Registrar versión negociada, autenticación, firma y cifrado efectivos, identidad y recurso. Firma protege integridad/autenticidad de los mensajes; cifrado protege confidencialidad del transporte. No son intercambiables. Los requisitos y valores predeterminados varían por SO, edición y versión; comprobar los extremos. No desactivar firma o habilitar SMB antiguo para ocultar una incompatibilidad. [Microsoft: seguridad SMB](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security).

**Samba/NAS.** Distinguir servidor de archivos, miembro de dominio y controlador Samba AD. Mantener mapeo SID–UID/GID estable y documentar backend/rangos antes de restaurar o cambiar dominio. Una ACL mostrada por un cliente puede interactuar con permisos Unix y módulos del servidor. Probar desde clientes Windows/Linux/macOS; no afirmar equivalencia porque la carpeta aparece en el explorador.

**NFS.** Registrar versión, export, clientes admitidos, identidad, modo de seguridad y opciones. La confianza en UID/GID transmitidos por el cliente no equivale a autenticación fuerte. `root_squash` reduce una clase de privilegio remoto, pero no sustituye el diseño de identidades y autorizaciones. Evaluar Kerberos y protección de transporte conforme al servicio. Las opciones concretas se validan con el manual del servidor elegido, no con una receta universal.

**Datos ya descargados.** Retirar permiso del share impide accesos futuros conforme al mecanismo, pero no borra automáticamente copias locales. La clasificación, DLP, retención y retirada de dispositivos responden a ese riesgo distinto. La conservación de evidencias se acuerda antes de limpiar equipos.

## 4. Red del host y segmentación

Inventariar interfaces físicas/virtuales, IPv4/IPv6, rutas, DNS, hora, proxy, túneles administrados, listeners y firewall. Asociar cada puerto a proceso, servicio, identidad y finalidad. Un listener en loopback, todas las interfaces o una VLAN concreta tiene exposición distinta.

Definir una matriz de flujos: origen por zona/dispositivo, destino y servicio, transporte, puerto, dirección, estado, justificación, propietario y registro. Separar gestión, usuarios, servidores, invitados/BYOD y laboratorio. Una VLAN por sí sola no define todas las reglas de interconexión.

Permitir solo lo requerido para el caso de uso y conservar rutas de gestión/recuperación. Verificar ida y retorno, DNS, sincronización, DHCP cuando corresponda y dependencias de autenticación. Incluir IPv6 y adaptadores virtuales en el alcance: no certificar aislamiento basándose únicamente en reglas IPv4.

El acceso remoto se hace mediante endpoints autorizados, origen restringido, autenticación verificada, mínimo privilegio y cierre registrado. No publicar SMB, RDP, WinRM o consolas de administración en Internet para simplificar una práctica. El bloqueo de entrada no demuestra que las salidas estén controladas; estudiar D24.

## 5. Evidencia GUI y terminal

Las siguientes consultas no cambian políticas. Ajustar rutas y nombres a un recurso sintético existente y consultar el manual. No subir salidas completas con identidades reales a Git.

```bash
# Linux: ejecutadas en el host de laboratorio propio
ip address
ip route
ss -lnt
# Elegir un directorio del ejercicio antes de consultar su ACL
getfacl -- ./datos-laboratorio
```

```powershell
# Windows: comparar seguridad avanzada/SMB con objetos del sistema
Get-NetIPConfiguration
Get-NetFirewallProfile
Get-SmbShare -Name 'ProyectoLaboratorio'
Get-SmbShareAccess -Name 'ProyectoLaboratorio'
Get-Acl -LiteralPath 'C:\Laboratorio\Proyecto'
```

```sh
# macOS: consulta; no cambiar la red ni ampliar TCC para evitar errores
scutil --dns
scutil --proxy
route -n get default
ls -lde@ ./datos-laboratorio
```

En Windows, `netsh winhttp show proxy` describe WinHTTP, no necesariamente el navegador ni todas las aplicaciones. En macOS una preferencia proxy y un filtro de red administrado son componentes distintos. En Linux las variables de proxy de una shell no garantizan el enrutamiento del tráfico de cada servicio.

Un fallo del comando por permisos es un límite de observación. No elevar automáticamente ni enumerar directorios ajenos. Comparar con la GUI del producto, una prueba real de acceso y el registro del servidor.

## 6. Restauración que conserva la seguridad

Ensayar restauración en una ruta alternativa con datos ficticios. Verificar contenido, tamaño/hash, propietario, grupos, ACL/herencia, atributos relevantes y acceso funcional desde cada rol. Registrar las diferencias conocidas del formato de backup.

Medir el tiempo hasta servicio útil, no solo hasta terminar de copiar. Comprobar que restaurar no resucita permisos de antiguos miembros ni cuentas eliminadas con nombres reutilizados. Mantener identidades estables y revisar propietarios huérfanos. El respaldo del directorio y el del servidor de ficheros tienen procedimientos y dependencias propios.

RPO y RTO son objetivos acordados; los resultados observados deben contrastarse con ellos. No confundir snapshot, réplica, sincronización y backup independiente. Una restauración operacional y una preservación forense responden a objetivos diferentes.

## 7. Prueba de aceptación mínima

Utilizar cuatro identidades de laboratorio: lector, editor, administrador delegado e invitado. Abrir una sesión nueva para verificar grupos, registrar la existente por separado y ejecutar la matriz de operaciones. Probar además un cliente en zona permitida y otro en zona denegada, sin escanear rangos externos.

Evidencia exigida: diagrama, matriz de permisos, ACL exportada saneada, identidad de prueba, resultado permitido/denegado, evento del servicio, diferencia de configuración y reversión. Un fallo de conectividad no acredita que la ACL haya bloqueado el acceso: identificar qué capa decidió.

Autoevaluación: un usuario no ve el recurso en la lista pero accede por su ruta directa. ¿La protección ha funcionado? No se ha demostrado denegación: visibilidad y autorización son controles diferentes. Corregir permisos según diseño, no solo ocultar el nombre.
