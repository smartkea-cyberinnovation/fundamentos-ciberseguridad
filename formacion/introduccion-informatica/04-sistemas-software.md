<!-- ES -->
# Sistemas operativos, archivos y software

Esta lectura D44 desarrolla T08, T09 y T10. Usa el lenguaje de D43 para conectar procesos, memoria y persistencia. M03, M07, M08 y M09 permiten practicar estos conceptos en los sistemas del laboratorio; D33 amplía identidad y control de acceso.

## Resultados de aprendizaje

Podrás seguir el ciclo de un proceso, explicar la relación entre páginas y memoria física, distinguir nombres de archivo y metadatos, interpretar permisos básicos y justificar decisiones sobre licencias, actualizaciones y dependencias.

## Programa, proceso e hilo

Un programa es código y datos preparados para ejecutarse. Un **proceso** es una instancia en ejecución, con recursos y contexto propios. Sus **hilos** comparten, normalmente, el espacio de direcciones y otros recursos del proceso, pero mantienen su propio estado de ejecución. Compartir memoria facilita colaborar y exige coordinar accesos concurrentes.

El núcleo administra recursos y ofrece llamadas al sistema. Una aplicación solicita servicios como abrir un archivo; no necesita controlar directamente cada dispositivo. El shell interpreta órdenes y una interfaz gráfica ofrece otra forma de interacción. Ninguno equivale al núcleo. Los sistemas de escritorio, servidor, móviles y empotrados adaptan estas responsabilidades a restricciones diferentes.

Un modelo de estados distingue preparado, ejecutándose, bloqueado por una espera y terminado. En Linux, `R` incluye ejecución o disposición para ejecutarse; `S` indica espera interrumpible, `D` espera no interrumpible y `Z` un proceso terminado cuyo estado aún no ha recogido su padre. Una letra aislada no diagnostica un fallo ni un incidente [S1].

**Ejemplo de planificación:** dos procesos A y B llegan en el instante cero y requieren tres y dos unidades de CPU. Con turnos de una unidad, un solo núcleo y sin esperas ni coste de cambio, la secuencia es A–B–A–B–A. B termina en el instante 4 y A en el 5. Cambiar estas hipótesis cambia el resultado; no es una predicción del planificador real [S2].

## Páginas y sistemas de archivos

La memoria virtual permite que cada proceso utilice direcciones que se traducen a recursos físicos. Con páginas de 4096 bytes, la dirección virtual `0x300A` se divide en página 3 y desplazamiento 10. El número de marco físico depende de la traducción; no se deduce de esa dirección. Un fallo de página puede deberse a asignación diferida, copia al escribir o datos que necesitan recuperarse. No significa siempre falta de RAM ni acceso inválido [S3].

Un sistema de archivos organiza datos y metadatos. En el modelo Unix, una entrada de directorio asocia un nombre con un **inode**. El inode contiene metadatos como tipo, propietario, permisos, tamaño y referencias a los datos; el nombre no forma parte del inode. Un enlace duro añade otro nombre para el mismo inode dentro del mismo sistema de archivos. Un enlace simbólico guarda una referencia a una ruta y puede quedar colgante [S4].

| Permiso | Archivo regular | Directorio |
|---|---|---|
| Lectura `r` | Leer contenido | Enumerar nombres |
| Escritura `w` | Modificar contenido | Modificar entradas, normalmente junto con `x` |
| Ejecución `x` | Solicitar ejecución | Recorrer el directorio y acceder a nombres conocidos |

El acceso efectivo depende también de directorios antecesores, ACL, identidades y otras políticas. Permisos no equivalen a cifrado. `640` representa lectura y escritura del propietario, lectura del grupo y ningún permiso para otros, en el modelo básico.

El **journaling** registra operaciones para recuperar coherencia tras una interrupción. En ext4, el modo habitual registra metadatos; no conserva todas las versiones del contenido ni sustituye una copia de seguridad [S5]. Una base de datos añade estructuras y reglas: una clave primaria identifica filas y las consultas parametrizadas separan los datos de las instrucciones SQL [S6].

## Software que podemos explicar y mantener

Distingue aplicaciones, utilidades, bibliotecas, entornos de ejecución y controladores. Una utilidad de copia depende del sistema operativo y puede usar bibliotecas; la seguridad de su conjunto incluye esas dependencias.

**Software libre** se refiere a libertades de uso, estudio, modificación y redistribución bajo su licencia; no significa necesariamente gratuito. El software libre puede ser comercial. Ver código sin una licencia que otorgue derechos suficientes no concede automáticamente esas libertades. Las licencias del programa y de sus componentes deben revisarse por separado [S7].

Para una actualización, identifica origen, versión, integridad y autenticidad disponibles, compatibilidad y forma de recuperación. Registra dependencias y comprueba sus avisos. Fijar versiones mejora reproducibilidad, pero también exige revisarlas para no conservar vulnerabilidades. Una firma válida identifica una procedencia bajo determinadas claves; no demuestra que el programa carezca de defectos.

## Práctica local: nombres, permisos y una tabla

Requiere Python 3 y un sistema de archivos POSIX que admita enlaces duros, como el del laboratorio Linux. En Windows, utiliza el entorno Linux preparado. No modifica usuarios, servicios ni archivos ajenos.

```bash
python3 - <<'PY'
import os
import sqlite3
import stat
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix='intro-informatica-') as folder:
    root = Path(folder)
    document = root / 'nota.txt'
    document.write_text('dato ficticio\n', encoding='utf-8')
    document.chmod(0o640)
    alias = root / 'otro-nombre.txt'
    os.link(document, alias)
    assert document.stat().st_ino == alias.stat().st_ino
    assert document.stat().st_dev == alias.stat().st_dev
    renamed = document.rename(root / 'renombrado.txt')
    assert alias.read_bytes() == renamed.read_bytes()
    mode = stat.S_IMODE(renamed.stat().st_mode)
    assert mode == 0o640
    print('permisos:', format(mode, '03o'), '; dos nombres, un inode')
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE equipos (id INTEGER PRIMARY KEY, nombre TEXT)')
        db.execute('INSERT INTO equipos VALUES (?, ?)', (1, 'laboratorio'))
        row = db.execute('SELECT nombre FROM equipos WHERE id = ?', (1,)).fetchone()
        assert row == ('laboratorio',)
        print('consulta parametrizada:', row[0])
assert not root.exists()
print('limpieza: archivos y base temporal cerrados')
PY
```

**Validación:** deben aparecer `640`, la consulta `laboratorio` y la confirmación de limpieza. La comparación de dispositivo e inode comprueba la identidad del archivo. Este ensayo con una sola cuenta no demuestra qué acceso tendría otra identidad. La base reside en memoria, se cierra explícitamente y el directorio temporal se elimina [S6].

**Evaluación:** explica el ejemplo de turnos, descompón otra dirección en página y desplazamiento, diferencia enlace duro y simbólico y razona por qué `r` sin `x` tiene un efecto distinto en archivos y directorios. Añade un inventario de tres componentes con licencia, versión y método de actualización verificado.

<!-- EN -->
# Operating systems, files, and software

Reading D44 develops T08, T09, and T10. It uses the terminology from D43 to connect processes, memory, and persistence. M03, M07, M08, and M09 provide practice in the laboratory systems; D33 expands identity and access control.

## Learning outcomes

You will be able to trace a process lifecycle, explain the relationship between pages and physical memory, distinguish file names from metadata, interpret basic permissions, and justify decisions about licenses, updates, and dependencies.

## Program, process, and thread

A program is code and data prepared for execution. A **process** is a running instance with its own resources and context. Its **threads** normally share the process address space and other resources while maintaining their individual execution state. Sharing memory makes collaboration possible and requires coordination of concurrent accesses.

The kernel manages resources and provides system calls. An application requests services such as opening a file; it need not directly control every device. A shell interprets commands, while a graphical interface provides another means of interaction. Neither is the kernel. Desktop, server, mobile, and embedded systems adapt these responsibilities to different constraints.

A state model distinguishes ready, running, blocked while waiting, and terminated. On Linux, `R` includes running or ready to run; `S` means interruptible sleep, `D` uninterruptible sleep, and `Z` a terminated process whose parent has not yet collected its status. A single letter does not diagnose a failure or security incident [S1].

**Scheduling example:** processes A and B arrive at time zero and require three and two CPU time units. With one-unit turns, one core, no waits, and no switching cost, the sequence is A–B–A–B–A. B finishes at time 4 and A at time 5. Changing these assumptions changes the result; this does not predict a real scheduler [S2].

## Pages and file systems

Virtual memory lets each process use addresses that translate to physical resources. With 4096-byte pages, virtual address `0x300A` splits into page 3 and offset 10. The physical frame number depends on the translation and cannot be deduced from that address. A page fault can result from deferred allocation, copy-on-write, or data that must be retrieved. It does not always mean insufficient RAM or an invalid access [S3].

A file system organizes data and metadata. In the Unix model, a directory entry associates a name with an **inode**. The inode contains metadata such as type, owner, permissions, size, and references to the data; the name is not part of the inode. A hard link adds another name for the same inode within the same file system. A symbolic link stores a reference to a path and can become dangling [S4].

| Permission | Regular file | Directory |
|---|---|---|
| Read `r` | Read contents | List names |
| Write `w` | Modify contents | Modify entries, normally together with `x` |
| Execute `x` | Request execution | Traverse the directory and access known names |

Effective access also depends on ancestor directories, ACLs, identities, and other policies. Permissions are not encryption. `640` represents owner read and write, group read, and no permissions for others in the basic model.

**Journaling** records operations to restore consistency after an interruption. The usual ext4 mode journals metadata; it does not preserve every content version or replace a backup [S5]. A database adds structures and rules: a primary key identifies rows, and parameterized queries separate data from SQL instructions [S6].

## Software we can explain and maintain

Distinguish applications, utilities, libraries, runtimes, and drivers. A backup utility depends on the operating system and can use libraries; securing the complete system includes those dependencies.

**Free software** concerns freedoms to use, study, modify, and redistribute under its license; it does not necessarily mean zero price. Free software can be commercial. Viewing code without a license granting sufficient rights does not automatically grant those freedoms. The licenses of the program and its components must be reviewed separately [S7].

For an update, identify its source, version, available integrity and authenticity checks, compatibility, and recovery procedure. Record dependencies and check their advisories. Pinning versions improves reproducibility but requires review to avoid retaining vulnerabilities. A valid signature identifies provenance under particular keys; it does not demonstrate that the program has no defects.

## Local practice: names, permissions, and a table

This requires Python 3 and a POSIX file system supporting hard links, such as the Linux laboratory environment. On Windows, use the prepared Linux environment. It does not modify users, services, or other people's files.

```bash
python3 - <<'PY'
import os
import sqlite3
import stat
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix='intro-informatica-') as folder:
    root = Path(folder)
    document = root / 'note.txt'
    document.write_text('fictitious data\n', encoding='utf-8')
    document.chmod(0o640)
    alias = root / 'another-name.txt'
    os.link(document, alias)
    assert document.stat().st_ino == alias.stat().st_ino
    assert document.stat().st_dev == alias.stat().st_dev
    renamed = document.rename(root / 'renamed.txt')
    assert alias.read_bytes() == renamed.read_bytes()
    mode = stat.S_IMODE(renamed.stat().st_mode)
    assert mode == 0o640
    print('permissions:', format(mode, '03o'), '; two names, one inode')
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE devices (id INTEGER PRIMARY KEY, name TEXT)')
        db.execute('INSERT INTO devices VALUES (?, ?)', (1, 'laboratory'))
        row = db.execute('SELECT name FROM devices WHERE id = ?', (1,)).fetchone()
        assert row == ('laboratory',)
        print('parameterized query:', row[0])
assert not root.exists()
print('cleanup: files removed and temporary database closed')
PY
```

**Validation:** output should include `640`, the query result `laboratory`, and confirmation of cleanup. Comparing device and inode verifies file identity. This single-account experiment does not demonstrate the access another identity would have. The database resides in memory and closes explicitly; the temporary directory is removed [S6].

**Assessment:** explain the turn-taking example, split another address into page and offset, distinguish hard and symbolic links, and explain why `r` without `x` has different effects on files and directories. Add an inventory of three components with their license, version, and verified update method.

<!-- COMMON -->
## Fuentes / Sources

- [S1 · Linux man-pages, proc_pid_stat(5)](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html).
- [S2 · Linux man-pages, sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html).
- [S3 · Linux kernel documentation, Memory Management Concepts](https://docs.kernel.org/admin-guide/mm/concepts.html).
- [S4 · Linux man-pages, inode(7)](https://man7.org/linux/man-pages/man7/inode.7.html).
- [S5 · Linux kernel documentation, ext4 Journal](https://docs.kernel.org/filesystems/ext4/journal.html).
- [S6 · Python, sqlite3](https://docs.python.org/3/library/sqlite3.html), [pathlib](https://docs.python.org/3/library/pathlib.html) y / and [tempfile](https://docs.python.org/3/library/tempfile.html).
- [S7 · Free Software Foundation, What is free software?](https://www.fsf.org/about/what-is-free-software).

Material propio de estudio. Referencias consultadas el 18 de octubre de 2026. / Original study material. References checked on 18 October 2026.
