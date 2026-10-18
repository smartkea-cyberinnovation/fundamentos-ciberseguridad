<!-- ES -->
# Arquitectura, memoria, almacenamiento y entrada/salida

Esta lectura D43 desarrolla los temas T05, T06 y T07. Conecta el inventario de hardware de D28 con una explicación de cómo se ejecuta una instrucción, se mueve un dato y se recupera un archivo. Continúa después con D44 para estudiar procesos, páginas y sistemas de archivos.

## Resultados de aprendizaje

Al terminar podrás distinguir un modelo de arquitectura de una implementación, explicar las funciones de los buses, comparar sondeo, interrupciones y DMA, situar cada memoria en su jerarquía y comprobar una recuperación con datos de prueba.

## De la instrucción al resultado

El modelo de **von Neumann** representa instrucciones y datos en una memoria común. **Harvard** separa sus memorias y caminos de acceso. Son modelos: un procesador moderno puede presentar un espacio de memoria unificado y mantener cachés separadas para instrucciones y datos. Esa combinación no se explica bien con una etiqueta sin matices.

En un ciclo conceptual, el contador de programa indica la siguiente instrucción. La CPU la obtiene, la decodifica, obtiene sus operandos, ejecuta la operación y guarda el resultado; después continúa o salta a otra dirección. Una suma puede leer registros, utilizar la unidad aritmética y escribir un registro. Los procesadores reales solapan trabajo y pueden reorganizar operaciones conservando el comportamiento exigido por su arquitectura [S1].

La **ISA**, como x86-64 o AArch64, define la interfaz de instrucciones y registros visible para el software. La microarquitectura implementa esa interfaz. Frecuencia, núcleos e hilos no permiten comparar rendimiento sin conocer la tarea. «64 bits» tampoco significa que todos los buses, instrucciones y direcciones físicas tengan exactamente esa anchura.

## Buses y entrada/salida

| Función conceptual | Información transportada | Ejemplo |
|---|---|---|
| Datos | Valores que se transfieren | Un bloque leído del disco |
| Direcciones | Posición o destino | Una dirección de memoria |
| Control | Operación y coordinación | Lectura, escritura, confirmación |

Un ejercicio con 32 bits de dirección y posiciones de un byte permite direccionar `2^32` bytes, es decir, 4 GiB. Es una hipótesis didáctica; no determina la RAM máxima de cualquier equipo etiquetado como «32 bits». Los interconectores actuales pueden codificar estas funciones en paquetes y compartir enlaces físicos.

En **sondeo**, la CPU consulta repetidamente el estado del dispositivo. Una **interrupción** notifica un evento que necesita atención. Con **DMA**, un dispositivo transfiere datos hacia o desde memoria sin que la CPU copie cada unidad: esta configura la operación y gestiona su finalización. Se pueden combinar DMA e interrupciones. Direcciones virtuales de CPU, físicas y de dispositivo no son necesariamente iguales; una IOMMU puede traducir y limitar accesos DMA [S2].

## Jerarquía y persistencia

| Nivel | Función | Precaución |
|---|---|---|
| Registros | Operandos y estado inmediato de CPU | Capacidad muy pequeña |
| Caché | Copias próximas de datos e instrucciones | Un acierto evita accesos más lentos |
| RAM convencional | Trabajo activo | Es volátil: pierde contenido sin alimentación |
| ROM y firmware en flash | Código de arranque o control persistente | La flash puede reprogramarse; no toda ROM es equivalente |
| Memoria virtual | Espacios de direcciones y traducción | No crea RAM física ni exige que todo esté en disco |
| HDD o SSD | Persistencia de archivos y bloques | Persistencia no equivale a recuperación garantizada |

Un fallo de página requiere intervención del sistema operativo, pero puede resolverse asignando una página nueva o compartiendo datos; no implica siempre lectura de disco [S3]. Si una aplicación está lenta, distingue presión de memoria, espera de almacenamiento y trabajo de CPU antes de proponer una ampliación.

Un **HDD** usa superficies magnéticas y partes mecánicas; un **SSD** emplea memoria no volátil, habitualmente flash. **NVMe** es una familia de protocolos e interfaces para almacenamiento, no una forma física: no significa lo mismo que M.2 y también existe transporte sobre redes [S4]. Un **NAS** ofrece acceso a archivos mediante protocolos como SMB o NFS. Una **SAN** proporciona habitualmente acceso a bloques mediante tecnologías como iSCSI o Fibre Channel. El almacenamiento de objetos añade otra interfaz basada en objetos y claves.

## Integridad y recuperación comprobable

RAID mejora determinadas disponibilidades; una instantánea conserva un estado según sus condiciones. Ninguno sustituye por sí solo una copia independiente y recuperable. Un hash permite comparar contenido con una referencia fiable. No demuestra autoría: quien altera un archivo y su referencia puede recalcular ambos.

### Práctica local: romper una copia y restaurarla

Ejecuta con Python 3 en Bash o zsh. Solo crea datos ficticios dentro de un directorio temporal. Esta copia comparte almacenamiento con el original y sirve para ensayar el procedimiento, no para resistir la pérdida del disco.

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

def digest(data):
    return hashlib.sha256(data).hexdigest()

with TemporaryDirectory(prefix='intro-informatica-') as folder:
    root = Path(folder)
    original = root / 'original.json'
    original.write_text('{"equipo":"laboratorio","version":1}', encoding='utf-8')
    baseline = original.read_bytes()
    backup = root / 'copia.json'
    backup.write_bytes(baseline)
    damaged = root / 'danado.json'
    damaged.write_bytes(baseline[:-1])
    assert digest(damaged.read_bytes()) != digest(baseline)
    restored = root / 'restaurado.json'
    restored.write_bytes(backup.read_bytes())
    assert digest(restored.read_bytes()) == digest(baseline)
    assert json.loads(restored.read_text(encoding='utf-8'))['version'] == 1
    assert original.read_bytes() == baseline
    print('alteracion detectada; restauracion integra y utilizable')
assert not root.exists()
print('limpieza: directorio temporal eliminado')
PY
```

**Resultado:** dos líneas confirman detección, restauración utilizable y limpieza. Los `assert` verifican el experimento; una excepción exige investigar, no ignorarla. El contexto temporal elimina sus archivos incluso al salir por una excepción ordinaria [S5].

**Entrega y evaluación:** dibuja el recorrido dispositivo → memoria → CPU, señalando dónde intervienen DMA e interrupción. Justifica una ubicación para cada nivel de memoria. Explica por qué el hash y la lectura JSON prueban cosas diferentes, y qué copia adicional necesitarías si fallara el almacenamiento completo.

<!-- EN -->
# Architecture, memory, storage, and input/output

Reading D43 develops topics T05, T06, and T07. It connects the hardware inventory in D28 with an explanation of how an instruction executes, data moves, and a file is recovered. Continue with D44 to study processes, pages, and file systems.

## Learning outcomes

After this reading, you will be able to distinguish an architectural model from an implementation, explain bus functions, compare polling, interrupts, and DMA, place each type of memory in its hierarchy, and verify a recovery using test data.

## From instruction to result

The **von Neumann** model represents instructions and data in a common memory. **Harvard** separates their memories and access paths. These are models: a modern processor can expose a unified memory address space while maintaining separate instruction and data caches. A single unqualified label does not adequately explain this combination.

In a conceptual cycle, the program counter identifies the next instruction. The CPU fetches it, decodes it, obtains its operands, executes the operation, and stores the result; it then continues or branches to another address. An addition can read registers, use the arithmetic unit, and write a register. Real processors overlap work and may reorder operations while preserving the behavior required by their architecture [S1].

An **ISA**, such as x86-64 or AArch64, defines the instruction and register interface visible to software. A microarchitecture implements that interface. Frequency, cores, and threads cannot establish comparative performance without knowing the workload. “64 bit” also does not mean that every bus, instruction, and physical address has precisely that width.

## Buses and input/output

| Conceptual function | Information carried | Example |
|---|---|---|
| Data | Values being transferred | A block read from a disk |
| Address | Location or destination | A memory address |
| Control | Operation and coordination | Read, write, acknowledgment |

A teaching example with 32 address bits and one byte per location can address `2^32` bytes, or 4 GiB. This is a stated assumption; it does not establish the maximum RAM of every computer labeled “32 bit.” Modern interconnects can encode these functions in packets and share physical links.

With **polling**, the CPU repeatedly checks device status. An **interrupt** reports an event requiring attention. With **DMA**, a device transfers data to or from memory without the CPU copying each unit: the CPU configures the operation and handles completion. DMA and interrupts can work together. CPU virtual addresses, physical addresses, and device addresses are not necessarily identical; an IOMMU can translate and restrict DMA accesses [S2].

## Hierarchy and persistence

| Level | Function | Caution |
|---|---|---|
| Registers | Immediate CPU operands and state | Very limited capacity |
| Cache | Nearby copies of data and instructions | A hit avoids slower accesses |
| Conventional RAM | Active working data | Volatile: contents are lost without power |
| ROM and firmware in flash | Persistent boot or control code | Flash can be reprogrammed; not all ROM is equivalent |
| Virtual memory | Address spaces and translation | Creates no physical RAM and does not require everything to be on disk |
| HDD or SSD | Persistent files and blocks | Persistence does not guarantee recovery |

A page fault requires operating system intervention, but it can be resolved by allocating a new page or sharing data; it does not always involve a disk read [S3]. When an application is slow, distinguish memory pressure, storage waits, and CPU work before recommending an upgrade.

An **HDD** uses magnetic surfaces and mechanical parts; an **SSD** uses nonvolatile memory, usually flash. **NVMe** is a family of storage protocols and interfaces, not a physical form factor: it is not synonymous with M.2, and network transports also exist [S4]. A **NAS** offers file access through protocols such as SMB or NFS. A **SAN** commonly provides block access through technologies such as iSCSI or Fibre Channel. Object storage adds another interface based on objects and keys.

## Verifiable integrity and recovery

RAID improves certain forms of availability; a snapshot preserves a state under its particular conditions. Neither independently replaces a separate, recoverable backup. A hash compares content against a trusted reference. It does not demonstrate authorship: someone who changes both a file and its reference can recalculate both.

### Local practice: damage one copy and restore it

Run Python 3 from Bash or zsh. This creates only fictitious data in a temporary directory. The backup shares storage with the original and rehearses the procedure; it cannot survive the loss of that disk.

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

def digest(data):
    return hashlib.sha256(data).hexdigest()

with TemporaryDirectory(prefix='intro-informatica-') as folder:
    root = Path(folder)
    original = root / 'original.json'
    original.write_text('{"equipo":"laboratorio","version":1}', encoding='utf-8')
    baseline = original.read_bytes()
    backup = root / 'copy.json'
    backup.write_bytes(baseline)
    damaged = root / 'damaged.json'
    damaged.write_bytes(baseline[:-1])
    assert digest(damaged.read_bytes()) != digest(baseline)
    restored = root / 'restored.json'
    restored.write_bytes(backup.read_bytes())
    assert digest(restored.read_bytes()) == digest(baseline)
    assert json.loads(restored.read_text(encoding='utf-8'))['version'] == 1
    assert original.read_bytes() == baseline
    print('change detected; restored data intact and usable')
assert not root.exists()
print('cleanup: temporary directory removed')
PY
```

**Expected result:** two lines confirm detection, a usable restoration, and cleanup. The `assert` statements verify the experiment; an exception calls for investigation. The temporary context removes its files even when an ordinary exception causes it to exit [S5].

**Submission and assessment:** draw the path device → memory → CPU, indicating where DMA and interrupts participate. Justify a location for each memory level. Explain why the hash and JSON read verify different things, and what additional backup would be necessary if the entire storage device failed.

<!-- COMMON -->
## Fuentes / Sources

- [S1 · MIT OpenCourseWare, Building the Beta](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c13/c13s1/).
- [S2 · Linux kernel documentation, DMA API HOWTO](https://docs.kernel.org/core-api/dma-api-howto.html).
- [S3 · Linux kernel documentation, Memory Management Concepts](https://docs.kernel.org/admin-guide/mm/concepts.html).
- [S4 · NVM Express specifications](https://nvmexpress.org/specifications/).
- [S5 · Python, tempfile](https://docs.python.org/3/library/tempfile.html) y / and [hashlib](https://docs.python.org/3/library/hashlib.html).

Material propio de estudio. Referencias consultadas el 18 de octubre de 2026. / Original study material. References checked on 18 October 2026.
