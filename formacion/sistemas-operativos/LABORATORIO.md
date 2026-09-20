# Laboratorio reproducible y seguro

## Arquitectura lógica

Tres zonas: administración; sistemas de práctica; colección/análisis de logs. Las redes de práctica son internas o host-only. Una interfaz NAT temporal puede habilitarse exclusivamente para actualizaciones e instalación revisada. No utilizar modo puente hacia una red doméstica, empresarial o docente compartida como configuración por defecto. Host-only no impide por sí solo el acceso al anfitrión: también se revisan sus servicios y firewall.

La estación de administración puede conectar a los equipos expresamente asignados. El servidor de logs recibe únicamente los flujos establecidos. Los sistemas de práctica no reciben entrada desde Internet. Se documentan origen, destino, protocolo, puerto, finalidad y responsable de cada flujo. Los ejemplos de inteligencia utilizan dominios `.test` e IP de documentación; no son objetivos para conectarse.

## Perfiles de recursos: estimaciones de planificación

| Perfil | Recursos orientativos del anfitrión | Uso |
|---|---|---|
| Reducido | 16 GB RAM, 4 núcleos y 120 GB libres | Una VM activa y conjuntos de datos offline; cobertura secuencial |
| Estándar | 32 GB RAM, 8 núcleos y 250 GB libres | Dos o tres VMs ligeras; reservar recursos al anfitrión |
| Avanzado | 64 GB RAM y almacenamiento adicional | Infraestructura concurrente, colector, directorio y orquestación |

No son mínimos oficiales de los productos. Se mide el uso real antes de asignar imágenes y se adaptan RAM, disco y concurrencia. Apple Silicon/x86, virtualización anidada y soporte del hipervisor condicionan las imágenes; no asumir que una VM x86 se comporta como ejecución nativa ARM.

## Sistemas

**Linux L1.** Distribución estable con soporte vigente, familia Debian/Ubuntu, GUI opcional y systemd en VM. **Linux L2.** Familia RPM compatible con ejercicios SELinux/firewalld. Los ejercicios indican cuándo basta una familia; no instalar todos los gestores simultáneamente. Registrar `/etc/os-release`, kernel, arquitectura, Bash, systemd y herramientas instaladas.

**Windows W1.** Cliente con soporte vigente y edición compatible con las funciones elegidas. Registrar compilación, edición, arquitectura, parches y PowerShell. **Windows W2 opcional.** Servidor de evaluación/licencia válida para roles, IIS, directorio y GPO. No dar por disponibles esos roles en cualquier edición cliente. Las evaluaciones de proveedor tienen condiciones y caducidad: comprobarlas antes del curso.

**macOS A1.** Mac permitido por las condiciones aplicables, físico o virtualizado sobre hardware admitido. Consultar licencia y documentación de virtualización vigente antes de desplegar; no distribuir imágenes ni proponer instalaciones no autorizadas. Sin acceso a macOS, pueden analizarse capturas y archivos sintéticos, pero se registra la competencia de administración nativa como no evaluada.

**Contenedores.** Útiles para Bash, datos y servicios desechables; no sustituyen el arranque del SO, kernel independiente, firewall completo, usuarios del host, Registro o controles nativos. Docker Desktop y WSL tienen capas adicionales: documentar dónde se ejecuta realmente cada proceso. No montar el socket Docker ni el filesystem del anfitrión en un terminal de alumno.

## Preparación reproducible

El docente prepara una ficha por imagen: identificador local, procedencia oficial, fecha, versión/edición/arquitectura, hash del instalador cuando se publique por canal verificable, recursos, red, paquetes, configuración de auditoría, usuarios ficticios, snapshot base, permisos y procedimiento de restauración. Se guardan instrucciones, no instaladores propietarios ni claves.

Cada alumno utiliza cuenta estándar y una identidad administrativa separada para tareas justificadas. Las credenciales de laboratorio son únicas y no reutilizan contraseñas personales. Nunca se escriben contraseñas en scripts, commits, capturas o historial. Una contraseña de ejemplo en un documento no debe transformarse en credencial común de la cohorte.

## Prueba de aislamiento previa

1. Dibujar redes y verificar adaptadores y rutas en hipervisor y huéspedes.
2. Comprobar que no hay puertos reenviados desde el exterior ni servicios de práctica escuchando en interfaces ajenas al laboratorio.
3. Ejecutar solamente pruebas de conexión a equipos asignados; comprobar un flujo permitido y uno denegado previamente definidos.
4. Revisar sincronización horaria y recepción de un evento benigno en el colector.
5. Restaurar una VM de prueba y demostrar que no afecta a otras máquinas.
6. Confirmar que carpetas compartidas, portapapeles, USB y discos del anfitrión están desactivados salvo necesidad documentada.

La prueba no es un escaneo de redes externas. No se inicia una práctica de cambios hasta que el docente acepta los resultados.

## Datos y evidencias

Estructura local de trabajo: `entrada/`, `trabajo/`, `salida/`, `evidencias/` y `notas/`. Los originales no se editan. Las copias forenses o logs reales, si alguna vez se autorizan, permanecen en un almacenamiento con acceso restringido fuera de Git. Git contiene documentación y fixtures sintéticos, no imágenes de disco, memorias, perfiles personales, cookies o bases de credenciales.

Datos iniciales por grupo: 20 archivos pequeños, nombres con espacios y Unicode, un archivo vacío, un enlace simbólico donde el SO lo admita, dos versiones de una configuración y 30 eventos sintéticos con hora explícita. Los errores sembrados son benignos: permiso insuficiente, ruta incorrecta, variable ausente, DNS de laboratorio erróneo, servicio detenido o certificado local no confiado. No se distribuye malware.

## Contrato común de laboratorio

Cada ficha A/B/C de los módulos hereda estos requisitos: objetivo y alcance; entorno versionado; tareas en orden; evidencia con nombre de fichero y timestamp; resultado esperado; comprobación independiente; y restauración. A/B/C duran 3 horas salvo M31 y M32. La ejecución se hace sobre los equipos propios del curso, con consola de recuperación disponible.

En prácticas que alteren usuarios, servicios, firewall, cifrado, particiones o políticas, primero se documenta el plan y se obtiene la validación docente. El cifrado se prueba solo tras custodiar la recuperación. La restauración de snapshot no sustituye una copia externa ni preserva automáticamente evidencia.

## Licencias y herramientas opcionales

El curso no obliga a comprar licencias ni enviar datos a servicios externos. Si una función no está disponible, se proporciona una alternativa y se distingue demostración de dominio práctico. Capturas de GUI deben corresponder a la versión instalada. Las herramientas de terceros se inventarían con versión, firma/procedencia, mantenimiento y permisos. No se permite instalar ejecutando indiscriminadamente scripts descargados con privilegios.
