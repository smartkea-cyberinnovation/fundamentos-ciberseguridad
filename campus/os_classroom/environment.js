// Architecture-aware learning guidance; never installs or executes anything.
export const HOSTS=['windows-x64','windows-arm','linux-x64','linux-arm','mac-intel','mac-arm','tablet','unknown'];
export const TARGETS=['common','linux','windows','macos'];
export function routeFor(host,target){
 if(!HOSTS.includes(host)||!TARGETS.includes(target))throw Error('ENV');
 if(target==='common')return 'any';
 if(host==='tablet')return 'remote';
 if(host==='unknown')return 'identify';
 if(target==='macos')return host.startsWith('mac-')?'mac':'remote-mac';
 const arm=['mac-arm','windows-arm','linux-arm'].includes(host);
 if(target==='windows')return arm?'windows-arm':'windows-x64';
 return arm?'linux-arm':'linux-x64';
}
export function guidance(host,target,lang){
 const es=lang==='es',route=routeFor(host,target);
 const messages={
 any:[['Puedes seguir los fundamentos en cualquier dispositivo. Los ejercicios de archivos necesitan un entorno con permisos de usuario y datos ficticios.','You can read the foundations on any device. File exercises require a user-accessible environment and fictitious data.']],
 identify:[['Primero identifica tu SO y arquitectura en Información del sistema o Acerca de este Mac. No deduzcas ARM/x64 del tamaño o antigüedad del equipo.','First identify the OS and architecture in System Information or About This Mac. Do not infer ARM/x64 from device size or age.']],
 remote:[['Continúa teoría, predicciones y autoevaluación en la tableta. Para operaciones nativas utiliza un equipo del aula o laboratorio remoto asignado por el docente. No abras RDP/SSH doméstico a Internet.','Continue theory, predictions and self-checks on the tablet. For native operations, use an assigned classroom device or instructor-provided remote lab. Do not expose home RDP/SSH to the Internet.'],['Marca la práctica como bloqueo de entorno, no como completada. Exporta las marcas y abre el enlace de la lección en el portátil.','Mark the lab as an environment blocker, not completed. Export your record and open the lesson link on the laptop.']],
 'remote-mac':[['Para administrar macOS necesitas un Mac o un laboratorio macOS autorizado. Un contenedor Linux o PowerShell en otro SO no reproduce TCC, launchd o FileVault. No se propone una instalación macOS no autorizada en hardware ajeno.','Administering macOS requires a Mac or an authorized macOS lab. Linux containers or PowerShell on another OS do not reproduce TCC, launchd or FileVault. Unauthorized macOS installation on other hardware is not proposed.']],
 mac:[['Puedes observar tu Mac con cuenta estándar. Usa una cuenta o entorno docente separado y una recuperación probada para cambios. Comprueba versión, arquitectura, controles de privacidad y licencia antes de virtualizar macOS.','You can observe your Mac using a standard account. Use a separate educational account/environment and tested recovery for changes. Check version, architecture, privacy controls and licensing before virtualizing macOS.']],
 'windows-arm':[['Elige Windows 11 ARM64 y un hipervisor que soporte TU anfitrión y esa versión invitada. Fusion en Apple Silicon no virtualiza un SO Windows x86. La emulación de ciertas aplicaciones dentro de Windows ARM no cambia la arquitectura del invitado.','Choose Windows 11 ARM64 and a hypervisor supporting YOUR host and that guest version. Fusion on Apple Silicon does not virtualize an x86 Windows OS. Emulation of some applications inside Windows ARM does not change guest architecture.'],['Consulta las matrices de Fusion y VirtualBox; cumple requisitos de firmware/TPM y licencia. No uses bypass de requisitos. Para roles Windows Server, AD DS o utilidades no compatibles con ARM utiliza el laboratorio x64 docente autorizado.','Check Fusion and VirtualBox compatibility; meet firmware/TPM and licensing requirements. Do not bypass requirements. For Windows Server roles, AD DS or ARM-incompatible utilities use an authorized instructor x64 lab.']],
 'windows-x64':[['Para Windows nativo usa una VM x64 con edición adecuada o un equipo docente. VirtualBox es una opción en anfitriones compatibles; VMware Workstation/Fusion depende del anfitrión. Registra sus versiones y comprueba los requisitos de Windows, incluido TPM donde corresponda.','For native Windows use an x64 VM with the appropriate edition or a classroom device. VirtualBox is an option on compatible hosts; VMware Workstation/Fusion depends on the host. Record versions and verify Windows requirements, including TPM where applicable.']],
 'linux-arm':[['Selecciona una distribución e imagen ARM64 compatibles con el hipervisor. En Apple Silicon, Fusion o VirtualBox requieren invitados ARM admitidos. No cargues una ISO x86 suponiendo que el programa la convertirá.','Select a distribution and ARM64 image supported by the hypervisor. On Apple Silicon, Fusion or VirtualBox require supported ARM guests. Do not load an x86 ISO assuming it will be converted.']],
 'linux-x64':[['Usa una distribución Linux x64 con soporte vigente en VirtualBox, VMware o un laboratorio Linux asignado. WSL/contenedores sirven para algunas tareas, pero no sustituyen todos los ejercicios de arranque, discos, servicios y firewall.','Use a supported x64 Linux distribution in VirtualBox, VMware or an assigned Linux lab. WSL/containers cover some tasks but do not replace every boot, disk, service and firewall exercise.']]
 };
 const steps=[
 ['Define el objetivo de la práctica y qué requiere SO nativo; consulta la ficha de la lección.','Define the lab goal and which parts need a native OS; consult its environment record.'],
 ['Comprueba RAM, disco libre, arquitectura y soporte host/invitado. Reserva recursos al anfitrión; los mínimos del fabricante no son una garantía de rendimiento.','Check RAM, free disk, architecture and host/guest support. Reserve host resources; vendor minima do not guarantee performance.'],
 ['Descarga instalador e ISO desde sus fabricantes; compara el hash publicado cuando exista. Una descarga no concede automáticamente una licencia.','Download installer and ISO from their vendors; compare the published hash when available. Downloading does not automatically grant a license.'],
 ['Crea una VM identificada, usa el disco virtual nuevo y evita seleccionar discos físicos. Instala con las opciones admitidas, sin desactivar requisitos de seguridad.','Create an identified VM, use a new virtual disk and avoid selecting physical disks. Install with supported options without disabling security requirements.'],
 ['Desactiva por defecto carpetas compartidas, portapapeles y USB innecesarios. Usa red interna para ejercicios; NAT temporal para actualizaciones aprobadas. No utilices puente ni port forwarding como atajo.','Disable unnecessary shared folders, clipboard and USB by default. Use internal networking for exercises; temporary NAT for approved updates. Do not use bridging or port forwarding as a shortcut.'],
 ['Actualiza, crea cuenta estándar y conserva acceso administrativo de recuperación. Registra un snapshot base y comprueba una restauración con un archivo ficticio. Snapshot no equivale a backup externo.','Update, create a standard account and preserve recovery administration. Record a baseline snapshot and verify restoration of a fictitious file. A snapshot is not an external backup.'],
 ['Compara entorno esperado con observado. Si falta compatibilidad, guarda la pregunta y usa el laboratorio alternativo; no marques como ejecutada una simulación.','Compare expected and observed environments. If compatibility is missing, save the question and use the alternate lab; do not mark a simulation as executed.']
 ];
 return {route,notes:messages[route].map(x=>x[es?0:1]),steps:steps.map(x=>x[es?0:1]),links:[
 ['VirtualBox: descargas / downloads','https://www.virtualbox.org/wiki/Downloads'],
 ['VirtualBox: host / guest','https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html'],
 ['VMware Fusion: Apple Silicon','https://knowledge.broadcom.com/external/article/315602'],
 ['VMware Workstation / Fusion','https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion'],
 ['Windows 11 x64','https://www.microsoft.com/software-download/windows11'],
 ['Windows 11 ARM64','https://www.microsoft.com/software-download/windows11arm64'],
 ['Windows Server evaluation','https://www.microsoft.com/evalcenter/'],
 ['Ubuntu','https://ubuntu.com/download'],
 ['Apple Virtualization','https://developer.apple.com/documentation/virtualization']
 ]};
}
