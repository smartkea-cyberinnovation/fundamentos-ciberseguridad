<!-- ES -->
# Hardware como una ciudad: componentes, servidores y cómputo especializado

**Lectura D28.** Objetivo: pasar de una analogía comprensible a un diagrama técnico y una prueba. Reutiliza M02–M03/M09. Las analogías son originales y no describen literalmente la electrónica. Referencias técnicas T01–T03 en [D36](#/recurso/D36).

## 1. Una ciudad útil, pero no literal

| Componente | Analogía inicial | Realidad y límite que hay que explicar |
|---|---|---|
| CPU | Taller que ejecuta órdenes | Instrucciones, registros y ejecución; más GHz no compara cualquier arquitectura |
| Núcleo e hilo | Puesto de trabajo y secuencia de tareas | Un hilo software no es un núcleo físico; existen planificación y concurrencia |
| Registros y cachés | Mesa y almacenes próximos | Jerarquías de pequeña capacidad y baja latencia; no son discos persistentes |
| RAM | Zona de trabajo de la ciudad | Memoria accesible por procesos mediante el SO; no conserva todo al apagar |
| SSD/NVMe | Archivo o almacén persistente | NVMe es un protocolo; SSD un tipo de dispositivo. Capacidad no equivale a rendimiento |
| HDD y cinta | Archivo de otra tecnología | Latencia, acceso, coste y uso distintos; no toda copia debe estar en el mismo medio |
| Placa, buses y PCIe | Calles e intersecciones | Enlaces y topología con capacidad compartida; no todos conectan directamente con todos |
| Controlador de memoria/NUMA | Gestor de almacenes y barrios | La proximidad de memoria importa; dos accesos pueden tener distinta latencia |
| GPU/NPU | Fábrica especializada | Paralelismo y operaciones específicas; trasladar datos y soportar software también cuesta |
| NIC y transceptor | Puerta de mercancías y medio de transporte | Interfaz de red, MAC, medio físico y controlador; un conector no asegura velocidad útil |
| Firmware/UEFI | Procedimiento de apertura de la ciudad | Inicializa y verifica componentes; es software persistente y necesita mantenimiento |
| TPM/elemento seguro | Custodia especializada | Protege operaciones/material según diseño; no hace seguro todo el equipo |
| Fuente/UPS y refrigeración | Electricidad y climatización | Sin energía o disipación no hay servicio; redundancia debe probar dominios de fallo |
| BMC y consola fuera de banda | Acceso de mantenimiento | Administración independiente y privilegiada; aislarla de redes de usuario e Internet |

La CPU no es un alcalde que lo decide todo ni la GPU una CPU siempre superior. La analogía sirve para preguntar por colas, distancias y capacidad; se abandona cuando oculta concurrencia, coherencia, interrupciones o aislamiento.

## 2. Recorrido de una operación

Un editor pide abrir un archivo. El SO comprueba acceso y obtiene bloques desde almacenamiento o caché; dispone memoria para el proceso; la CPU ejecuta código y procesa eventos; el controlador y el dispositivo realizan entrada/salida; la interfaz muestra el resultado. Si el archivo es remoto se añade protocolo de red, autenticación y permisos del servidor. Una aplicación no debería tener acceso irrestricto a toda RAM o a todos los dispositivos.

Dibuja la ruta y marca dónde esperarías un error: disco lleno, memoria insuficiente, permiso, latencia de red, CPU ocupada o dispositivo defectuoso. Identificar el componente evita resolver cualquier fallo comprando más memoria. Registrar el tiempo total de la tarea y el recurso relevante importa más que una captura aislada de utilización.

## 3. Arquitecturas y compatibilidad

Distingue arquitectura de instrucciones (por ejemplo x86-64 o Arm), microarquitectura, sistema en chip, firmware y sistema operativo. Que dos equipos ejecuten la misma aplicación puede requerir binarios distintos o emulación. La virtualización y la emulación no son sinónimos; tampoco un contenedor aporta por sí mismo una CPU o kernel compatibles.

Estudia 32/64 bits como anchuras y modelos de direccionamiento, no como una nota universal de calidad. Introduce endianess, interrupciones y DMA con diagramas; no se necesita escribir controladores para comprender por qué drivers y firmware forman parte de la superficie de seguridad. Se distinguen interfaces de datos, de control y de mantenimiento.

## 4. Ordenador personal, servidor y centro de datos

«Servidor» puede designar función, proceso o equipo. Un PC puede servir una web de laboratorio, pero operación empresarial exige evaluar disponibilidad, soporte, repuestos, memoria y almacenamiento adecuados, energía, refrigeración y administración. Un rack no convierte sus componentes en redundantes por sí solo.

El centro de datos incluye racks, redes de acceso/agregación, almacenamiento, cableado, transceptores, distribución eléctrica, UPS, generación de respaldo donde proceda, refrigeración, protección física y operación. Define qué fallo soporta: fuente, enlace, switch, rack, sala, zona o proveedor. Dos fuentes conectadas al mismo circuito conservan ese punto de fallo. Un clúster comparte también dependencias de identidad, DNS, tiempo y gestión.

Inventario mínimo: función y dueño, modelo/arquitectura, ubicación, firmware, soporte, interfaces, dependencia eléctrica/red, datos tratados, método de administración y recuperación. No publiques números de serie, credenciales de BMC ni topologías reales del centro de datos en Git.

## 5. Virtualización y contenedores

VirtualBox, familias de productos VMware y Proxmox son ejemplos para estudiar hipervisores y operación; la edición, licencia y soporte se revisan antes de la cohorte. El objetivo no es instalar tres productos sin necesidad. Compara invitado, red virtual, almacenamiento, snapshot y restauración. Un snapshot no reemplaza una copia independiente.

Docker empaqueta procesos y dependencias dentro de un modelo de aislamiento; Compose describe aplicaciones de varios servicios; Swarm y Kubernetes coordinan servicios o cargas sobre nodos. Enseñar esos nombres sin kernel, almacenamiento, red y permisos produce falsa confianza. Mantén los ejercicios de M26 y la arquitectura de [D30](#/recurso/D30). No habilites contenedores privilegiados o el socket del host para facilitar tareas del alumnado.

## 6. Hardware para IA

Distingue entrenamiento e inferencia, CPU/GPU/NPU, memoria del acelerador, interconexión, almacenamiento y refrigeración. Un modelo debe caber en el esquema de memoria elegido y sus transferencias pueden dominar la latencia. Precisión numérica, cuantización, batch y longitud de contexto cambian coste y resultados; comparar solo TOPS, FLOPS o número de chips no compara un servicio completo.

Ejercicio de estimación, no benchmark: un modelo de P parámetros con b bytes por parámetro necesita aproximadamente P×b bytes solo para esos parámetros; activaciones, cachés, runtime y entrenamiento añaden memoria. Para 8.000 millones de parámetros y 2 bytes, el cálculo base es 16.000 millones de bytes, no una promesa de funcionar en una GPU de «16 GB». La capacidad libre y el formato real deben medirse.

## 7. Cuántica sin magia

Un qubit, una puerta y una medición no equivalen a bits clásicos acelerados. NIST introduce superposición y entrelazamiento; IBM explica que la QPU necesita infraestructura clásica y no sustituye al ordenador de propósito general [T02–T03]. La lectura de un resultado no entrega todas las posibilidades de una superposición.

Separa qubits físicos/lógicos, ruido, corrección de errores, fidelidad, profundidad del circuito y utilidad de una tarea. No uses el recuento bruto de qubits como ranking universal. Las tecnologías físicas difieren y no todas requieren la misma refrigeración. La criptografía poscuántica se ejecuta en equipos clásicos y es distinta de comunicaciones cuánticas. Las hojas de ruta de fabricantes son objetivos declarados, no garantías de fechas.

## 8. Bastionado desde debajo del SO

El enfoque de NIST SP 800-193 organiza resiliencia del firmware en protección, detección y recuperación [T01]. Tradúcelo a una ficha: procedencia de actualizaciones, acceso de administración, arranque verificado según plataforma, configuración, registro de cambios y recuperación soportada. No flashear firmware como práctica improvisada.

Separa red de gestión/BMC, limita identidades y conserva consola de recuperación. Revisa puertos físicos, medios extraíbles, periféricos, suministro y retirada. Cifrar un disco no impide abuso de una sesión ya desbloqueada. La sanitización debe considerar medio, cifrado y procedimiento; sobrescribir un archivo no demuestra borrado físico en SSD/COW.

## Prácticas y resultados

**INT-L05: del dibujo al inventario.** Sobre tu VM o equipo de laboratorio, relaciona diez componentes con la ciudad y con una consulta GUI/CLI. Evidencia: tabla con función real, analogía y límite, sin identificadores personales. Éxito: explicar por qué caché, RAM y almacenamiento no son intercambiables. No realizar cambios de firmware.

**INT-L06: diseñar recuperación por fallo.** El docente entrega un servicio ficticio con dos fuentes, dos NIC y un único almacenamiento. Dibuja dominios de fallo y elige una mejora justificada. Evidencia: dependencias y prueba de restauración diseñada. Éxito: no llamar «alta disponibilidad» a la mera duplicación de piezas. La prueba física queda pendiente hasta disponer de laboratorio aprobado.
<!-- EN -->
# Hardware as a city: components, servers and specialized computing

**Reading D28.** Move from an accessible analogy to a technical diagram and a test. Reuses M02–M03/M09. Analogies are original teaching devices, not literal descriptions of electronics. Technical references T01–T03 are in [D36](#/recurso/D36).

## 1. A useful but imperfect city

| Component | Initial analogy | Reality and required limitation |
|---|---|---|
| CPU | Workshop executing orders | Instructions, registers and execution; GHz cannot compare every architecture |
| Core and thread | Workstation and sequence of tasks | A software thread is not a physical core; scheduling and concurrency matter |
| Registers and caches | Desk and nearby stores | Small low-latency hierarchies, not persistent disks |
| RAM | Working area | Process memory mediated by the OS; not fully retained after power loss |
| SSD/NVMe | Persistent archive | NVMe is a protocol and SSD a device type; capacity is not throughput |
| HDD and tape | Alternative archives | Different latency, access patterns and cost; independent backup media matter |
| Board, buses and PCIe | Roads and junctions | Links and topology share capacity; not everything directly connects to everything |
| Memory controller/NUMA | Storage managers and districts | Memory locality affects latency |
| GPU/NPU | Specialized factory | Parallel/specialized operations; data movement and software support also cost |
| NIC/transceiver | Loading gate and carrier | Network interface, MAC, physical medium and driver; a connector guarantees no useful rate |
| Firmware/UEFI | Opening procedure | Initializes/checks components; persistent software needs maintenance |
| TPM/secure element | Specialized custody | Protects particular operations/material, not the entire system automatically |
| Power/UPS/cooling | Electricity and climate | Service depends on power and heat removal; redundancy needs failure-domain tests |
| BMC/out-of-band console | Maintenance entrance | Independent privileged administration; isolate it from user networks and the Internet |

The CPU is not an all-knowing mayor, and a GPU is not always a superior CPU. Use the analogy for queues, distance and capacity; abandon it when it hides concurrency, coherence, interrupts or isolation.

## 2. Follow an operation

An editor requests a file. The OS checks access, obtains blocks from storage or cache, provides memory to the process and coordinates input/output. CPU execution, drivers, devices and interface updates contribute to the result. A remote file adds network protocols, authentication and server permissions. Applications should not have unrestricted access to every memory page or device.

Draw the path and mark likely failure locations: full storage, insufficient memory, access denial, network delay, CPU contention or a failed device. Identify the component instead of buying RAM for every symptom. Measure task duration and relevant resources rather than relying on one utilization screenshot.

## 3. Architecture and compatibility

Distinguish instruction-set architecture such as x86-64/Arm, microarchitecture, system-on-chip, firmware and OS. The same application may need different binaries or emulation. Virtualization is not emulation; a container does not independently supply a compatible CPU or kernel.

Study 32/64-bit properties as widths and addressing models, not universal quality scores. Introduce endianness, interrupts and DMA through diagrams. Driver development is not required to understand why firmware and drivers form part of the security surface. Separate data, control and maintenance interfaces.

## 4. Personal computer, server and data center

«Server» may mean a function, a process or a physical machine. A PC can host a practice website; enterprise operation requires evaluation of availability, support, spares, memory/storage, power, cooling and administration. Rack mounting does not create redundancy.

A data center includes racks, access/aggregation networks, storage, cabling, transceivers, power distribution, UPS, backup generation where appropriate, cooling, physical protection and operations. Define tolerated failures: power unit, link, switch, rack, room, zone or provider. Two power supplies on one circuit preserve that common failure. Clusters also depend on identity, DNS, time and management.

Minimum inventory: purpose/owner, model/architecture, location, firmware, support, interfaces, power/network dependencies, data, administration and recovery. Do not publish real serial numbers, BMC credentials or production topology in Git.

## 5. Virtualization and containers

VirtualBox, VMware product families and Proxmox are examples for examining hypervisors and operations. Check edition, licence and support before teaching. Installing all three is not the objective. Compare guest, virtual network, storage, snapshot and restore. A snapshot does not replace an independent backup.

Docker packages processes and dependencies within an isolation model; Compose describes multi-service applications; Swarm and Kubernetes coordinate services or workloads across nodes. Teaching names without kernel, storage, networking and permissions creates false confidence. Reuse M26 and [D30](#/recurso/D30). Do not grant privileged containers or the host socket to simplify student tasks.

## 6. AI hardware

Separate training/inference, CPU/GPU/NPU, accelerator memory, interconnect, storage and cooling. A model must fit the chosen memory scheme; transfers can dominate latency. Numerical precision, quantization, batching and context length affect cost and output. TOPS/FLOPS or chip counts alone do not compare complete services.

Illustrative estimate, not a benchmark: P parameters at b bytes each require roughly P×b bytes for the parameters alone. Activations, caches, runtime and training add requirements. Eight billion parameters at two bytes imply sixteen billion bytes as a base calculation, not a guarantee of running on a «16 GB» GPU. Measure actual formats and free capacity.

## 7. Quantum without magic

Qubits, gates and measurements are not simply faster classical bits. NIST introduces superposition/entanglement; IBM explains that a QPU depends on classical infrastructure and does not replace a general-purpose computer [T02–T03]. Measuring an output does not reveal every possibility in a superposition.

Separate physical/logical qubits, noise, error correction, fidelity, circuit depth and useful task performance. Raw qubit counts are not a universal ranking. Physical technologies differ and need not share cooling requirements. Post-quantum cryptography runs on classical computers and differs from quantum communication. Vendor roadmaps are declared goals, not guaranteed delivery dates.

## 8. Hardening below the OS

NIST SP 800-193 organizes firmware resilience around protection, detection and recovery [T01]. Turn this into a record of update provenance, administrative access, platform-appropriate verified boot, configuration, change logs and supported recovery. Do not improvise firmware flashing exercises.

Separate management/BMC networks, constrain identities and preserve a recovery console. Examine physical ports, removable media, peripherals, supply chain and retirement. Disk encryption does not prevent misuse of an unlocked session. Sanitization depends on media, encryption and procedure; overwriting one file does not establish physical erasure on SSD/COW storage.

## Exercises and outcomes

**INT-L05: diagram to inventory.** On an assigned VM or lab device, relate ten components to both the city and a GUI/CLI observation. Evidence: actual function, analogy and limitation, without personal identifiers. Success: explain why cache, RAM and storage are not interchangeable. No firmware changes.

**INT-L06: recovery by failure domain.** A fictional service has two power supplies, two NICs and one storage system. Draw failure domains and justify one improvement. Evidence: dependencies and a designed restore test. Success: do not call duplicated parts «high availability». Physical execution remains pending until an approved lab is available.
