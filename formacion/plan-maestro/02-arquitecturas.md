# 02 · Arquitecturas, virtualización y cloud

[Índice](README.md) · [Programa](01-mapa-curricular.md) · [Laboratorios](06-laboratorios.md) · [Fuentes](09-fuentes.md)

## Método de diseño

Empezar por usuarios, operaciones, datos, disponibilidad, latencia, presupuesto, capacidades del equipo y restricciones. Dibujar flujos, identidades, puntos de fallo y fronteras de confianza antes de escoger productos. Documentar cada decisión en un ADR: problema, opciones, elección, razones, consecuencias, verificación y condición para revisarla. Los Well-Architected Frameworks de AWS, Azure y Google Cloud sirven para ordenar revisiones de calidad, no como equivalencia automática entre servicios ni como certificación. [S11–S13]

Para todos los ejemplos, responder: quién administra el SO; quién parchea el runtime; dónde residen los datos; cómo se autentican personas y servicios; dónde termina TLS; qué se registra; quién restaura; qué deja de funcionar si cae una dependencia; cómo se elimina el entorno y se verifica el coste remanente.

## Escalera de casos, no escalera obligatoria de complejidad

| ID | Patrón | Topología pedagógica | Qué enseña | Riesgo o límite principal |
|---|---|---|---|---|
| WEB-01 | Sitio estático | Navegador → DNS/CDN → activos | HTTP, caché, build, despliegue y rollback | No proporciona por sí mismo identidad, sincronización ni ejecución remota |
| WEB-02 | WordPress en servidor único | Navegador → TLS/web/PHP → base de datos local | Operación de un servicio completo con pocas piezas | Host como punto único de fallo; plugins y permisos; backup de DB y archivos |
| WEB-03 | Dos capas | Proxy/web/app → DB privada | Separación de responsabilidades, credenciales y puertos | Nueva dependencia de red; base de datos no expuesta públicamente |
| WEB-04 | Alta disponibilidad | Balanceador → dos instancias → datos/sesiones externas | Health checks, escalado y estado | Réplica no es backup; quórum y almacenamiento pueden seguir siendo SPOF |
| WEB-05 | Monolito modular empresarial | Front/API → aplicación por dominios → DB/caché/cola | Contratos, transacciones, trabajos asíncronos y SSO | Complejidad de consistencia, observabilidad y privilegios entre servicios |
| WEB-06 | Aplicación contenerizada | Registro → Compose o clúster → servicios/volúmenes | Build reproducible y gestión declarativa | Contenedor no sustituye recuperación del dato ni seguridad del host |
| WEB-07 | PaaS/serverless | Front/CDN → API/función/servicio gestionado → datos | Responsabilidad compartida y escala gestionada | Cuotas, egress, proveedor, observabilidad y permisos |
| WEB-08 | Híbrida/multirregión | Acceso corporativo → sitios/regiones con réplicas | Resiliencia, residencia y recuperación por región | Latencia, coste, consistencia y fallos correlacionados |

Cada caso tiene una alternativa mínima y otra ampliada. El alumno puede concluir justificadamente que un único servidor bien operado cubre mejor el encargo que un clúster. Alta disponibilidad, elasticidad, durabilidad, seguridad y recuperabilidad son propiedades diferentes.

## Caso desarrollado: WEB-02 → WEB-04

**Negocio ficticio:** portal informativo con contenido editorial, cuentas de editores y formularios de prueba. No se usan alumnos reales, pagos ni credenciales personales. El requisito inicial es publicar contenido, actualizarlo y restaurarlo dentro del objetivo acordado.

**Fase 1 — servidor único.** Inventariar SO, web server, runtime, base de datos, plugins, archivos y certificados. Separar cuenta administradora y de servicio. Solo publicar el servicio necesario en la red del laboratorio. Mantener DB local/privada, permisos mínimos y copias externas. Ensayar restauración en otro destino antes de afirmar que el respaldo sirve.

**Fase 2 — dos capas.** Trasladar la DB a una VM o servicio gestionado privado; restringir origen/destino; crear identidad de aplicación de alcance limitado; definir migración y rollback. Comprobar el recorrido de escritura y restauración. No asumir que separar la DB mejora todo: también añade conexión, latencia y operación.

**Fase 3 — dos instancias.** Resolver explícitamente archivos compartidos, sesiones, tareas programadas, escrituras concurrentes y migraciones. Definir qué comprueba el health check. Detener de forma controlada una instancia de prueba y observar el comportamiento del balanceador sin perder una transacción ficticia.

**Fase 4 — seguridad y evidencia.** Añadir WAF o proxy de prueba, registro de cambios, alertas de salud y un caso de autorización. Comparar acceso legítimo y restricción preparada. Verificar que la IP de origen se interpreta correctamente y no se confía sin criterio en cabeceras de proxy.

**Entregables:** diagramas de las tres versiones, ADR, matriz de flujos, roles, inventario de dependencias, plan de parcheo, backup, prueba de restauración, logs saneados y diferencias de coste. **Aceptación:** otra persona puede explicar el recorrido de una solicitud y restaurar un dato. No se considera aprobada una versión solo porque abre la portada.

## Equivalencias cloud por capacidad, no por identidad funcional

| Necesidad | AWS: ejemplo de familia | Azure: ejemplo de familia | Google Cloud: ejemplo de familia | Alternativa o cuestión local |
|---|---|---|---|---|
| VM | EC2 | Virtual Machines | Compute Engine | Proxmox/KVM o hipervisor autorizado |
| Red privada | VPC | Virtual Network | VPC | VLAN, bridges, routing y firewall |
| Objetos | S3 | Blob Storage | Cloud Storage | Almacenamiento de objetos compatible elegido tras revisión |
| DB gestionada | RDS/Aurora según motor | Azure SQL o servicios de PostgreSQL según caso | Cloud SQL según motor | PostgreSQL/MariaDB administrado por el equipo |
| Kubernetes gestionado | EKS | AKS | GKE | Clúster propio: mayor responsabilidad operacional |
| Aplicación/funciones | ECS/Fargate/Lambda según patrón | App Service/Container Apps/Functions | Cloud Run y servicios de funciones | VM, Compose o Swarm según requisitos |
| Observabilidad | CloudWatch/CloudTrail según función | Azure Monitor y registros pertinentes | Cloud Monitoring/Logging/Audit Logs | Colector propio y política de retención |
| Identidad | IAM y organización de cuentas | Entra ID y Azure RBAC con alcances distintos | Cloud IAM y organización/proyectos | Directorio y políticas propias |

Tabla didáctica para orientar búsquedas en los catálogos oficiales, no guía de compra. Validar disponibilidad regional, límites, nombres, soporte y licencia en la versión del laboratorio. Un tenant no es una suscripción; una cuenta no equivale exactamente a un proyecto; un servicio de contenedores no equivale a una función. [S11–S13]

**Otros proveedores:** Cloudflare para publicación estática/edge; OVHcloud y DigitalOcean para comparar VM/red/datos gestionados; OpenStack para estudiar cloud privado. No se presupone crédito gratuito, cuenta educativa, capacidad comercial concreta o derecho de uso. La práctica tiene variante offline mediante diagramas y exportaciones sintéticas.

## VirtualBox, VMware y Proxmox

La comparación debe cubrir GUI y CLI: crear VM, asignar CPU/RAM, conectar red interna, manejar discos, snapshot, exportar, restaurar y registrar cambios. VirtualBox y las líneas de escritorio VMware se estudian como entornos de alumno; las plataformas VMware empresariales y Proxmox como gestión de infraestructura. No trasladar licencias o funciones de un producto a otro.

Proxmox integra KVM y LXC; la máquina virtual y el contenedor comparten responsabilidades de forma distinta. Las prácticas deben identificar kernel, almacenamiento y límites reales. La topología del curso utilizará exclusivamente hardware y versiones admitidos. [S17]

Para cada imagen: origen, versión/arquitectura, firma o hash publicado cuando exista, licencia, recursos estimados, red, usuario, snapshot inicial, recuperación y fecha de prueba. Las condiciones de uso de hipervisores, extensiones y sistemas invitados deben revisarse antes de distribuir material; se entregan instrucciones y datos sintéticos, no imágenes propietarias.

## Progresión Docker → Compose → Swarm → Kubernetes

**Docker:** comprender qué contiene la imagen, qué conserva un volumen y quién es propietario de los datos. Probar una imagen mínima de aplicación benigna, sin socket Docker del host ni permisos privilegiados. Registrar digest y política de actualización.

**Compose:** describir varios servicios de un entorno, redes privadas, health checks, recursos, dependencias y persistencia. El orden de inicio no sustituye la disponibilidad de la aplicación. Separar configuración, secreto y datos. La práctica comienza con publicación solo local o en red autorizada. [S14]

**Swarm:** explicar gestores/trabajadores, quorum, scheduling, servicio/réplica, redes overlay, secrets/configs, actualización y reversión. Verificar el alcance de los puertos publicados y el routing mesh; no trasladar sin comprobar la semántica de binding local de Compose. [S15]

**Kubernetes:** introducir manifiestos a partir del mismo contrato funcional. Relacionar Pod, Deployment, Service, almacenamiento persistente y RBAC. Diferenciar liveness/readiness/startup; comprobar soporte real de políticas de red y gestión de secretos. No presentar Kubernetes como requisito para servir una web pequeña. [S16]

**Prueba transversal:** fallo de una instancia benigna, conservación de estado, degradación observada, rollback y restauración. El criterio es el resultado funcional y el riesgo, no el número de recursos desplegados.

## Observabilidad, costes y retiro

Registrar métricas de disponibilidad, latencia y errores con ventana temporal; correlacionar logs sin guardar datos sensibles por defecto. Definir alertas de presupuesto y alarmas técnicas por separado. Comprobar recursos persistentes, direcciones, discos, snapshots, almacenamiento, logs y DNS al retirar el laboratorio. Guardar prueba de eliminación o coste residual. El borrado de un clúster no garantiza eliminar todo recurso dependiente.

## Relación con el campus Cloudflare

El campus activo y un laboratorio de sistemas son dos productos distintos. Mantener separadas sus guías y sus permisos. Pages publica contenido estático; Workers puede incorporar activos y APIs si se diseña esa arquitectura, pero una web de estudio no necesita ejecutar comandos del alumno. El traspaso de progreso y una futura identidad por OTP se especifican en [08](08-continuacion.md); no forman parte de un servidor vulnerable.
