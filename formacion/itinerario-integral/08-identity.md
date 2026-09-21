<!-- ES -->
# Identidades y usuarios: del alta a la revocación comprobada

**Lectura D33.** Objetivo: gobernar acceso efectivo durante todo el ciclo de vida. Complementa las lecturas operativas [D22](#/recurso/D22), [D23](#/recurso/D23), [D24](#/recurso/D24), [D25](#/recurso/D25) y M07/M17/M18. Fuentes P01–P06 en [D36](#/recurso/D36).

## 1. Persona, identidad, cuenta y perfil

Una persona puede tener varias identidades/cuentas; una cuenta de servicio no representa necesariamente una persona. Identidad, autenticador, sesión, grupo, rol, permiso y perfil son objetos distintos. Un perfil contiene preferencias y datos de usuario; eliminarlo no necesariamente revoca tokens o pertenencias del directorio.

Distingue cuentas locales, dominio/directorio, SaaS y aplicaciones. LDAP es un protocolo de directorio; AD DS integra directorio y otros servicios como autenticación y políticas. Microsoft Entra ID no es un controlador de dominio local con otro nombre. Una aplicación con SSO aún necesita autorización. FreeIPA y Keycloak son ejemplos abiertos de capacidades diferentes: integración de identidad de sistemas y servicios frente a federación/acceso de aplicaciones [P01–P03].

## 2. Fuente autoritativa y modelo entidad–centro–puesto

Diseña atributos de empleo o colaboración desde una fuente autorizada: identificador estable, entidad, centro, unidad, puesto, responsable, tipo de relación, fechas y estado. No uses correo o nombre visible como única clave permanente. Define quién corrige datos y cómo se reconcilian discrepancias.

El puesto puede sugerir un paquete de acceso, pero no concede automáticamente todo lo usado históricamente por el ocupante anterior. Relaciona rol empresarial, rol técnico, grupo y permisos específicos. El dueño del recurso decide necesidad; IAM implementa; seguridad revisa conflictos; auditoría verifica con independencia apropiada. Registra aprobaciones y excepciones.

## 3. Joiner, mover, leaver y variantes

| Evento | Flujo mínimo docente | Evidencia de éxito |
|---|---|---|
| Alta | Fuente válida→aprobación→cuenta→acceso mínimo→dispositivo→formación | Identidad correcta, permisos positivos/negativos y entrega registrada |
| Cambio | Nuevo puesto/centro→comparar acceso→retirar anterior→aprobar excepción temporal | Ausencia de acumulación no justificada |
| Baja | Fecha/urgencia→revocar acceso y sesiones→activos→datos/retención→verificar | Acceso rechazado y tareas/secretos reasignados |
| Ausencia/suspensión | Política temporal y responsable | Estado, plazo y restitución aprobada |
| Reincorporación | Validar relación y recalcular permisos | No reactivar privilegios antiguos a ciegas |
| Proveedor/visitante | Sponsor, propósito y caducidad | Expiración y revisión sin cuenta huérfana |
| Emergencia | Cuenta excepcional custodiada y vigilada | Uso justificado, alerta y revisión posterior |
| Cuenta no humana | Dueño, workload, secreto/certificado y rotación | Sin uso interactivo innecesario y revocación probada |

Deshabilitar una cuenta no garantiza invalidar todo token, sesión cacheada, clave SSH o credencial de integración. La baja debe comprobar los sistemas efectivos, respetando mecanismos y límites de cada plataforma. No se necesita extraer secretos para auditar su existencia, propietario y fecha de rotación.

## 4. RBAC, ABAC y combinaciones tóxicas

RBAC asigna permisos por roles; ABAC evalúa atributos de sujeto, recurso, acción y contexto mediante políticas [P04]. No son mutuamente excluyentes. Un modelo puede usar rol para el acceso básico y atributos para centro, sensibilidad o estado del dispositivo. Evita proliferación de roles y políticas imposibles de explicar.

Separación de funciones: solicitar y aprobar el mismo pago, desarrollar y aprobar sin revisión una entrega crítica, o asignarse y auditar el propio privilegio son conflictos a evaluar. «Tóxico» describe una combinación frente a un riesgo/criterio, no una propiedad moral del usuario. Define incompatibilidades, compensaciones, autoridad y caducidad. Una herramienta puede detectar conflictos configurados; no inventa por sí sola el modelo organizativo.

## 5. Permisos efectivos y recursos compartidos

En Linux/macOS compara dueño, grupos, permisos de directorios padres, ACL y controles adicionales; en Windows analiza NTFS, compartición, herencia, grupos y políticas. Para un acceso SMB intervienen permisos del recurso y del objeto; no sumar permisos como si fueran números. En nube/SaaS revisa enlaces, invitados, roles y permisos de la aplicación.

Diseña una matriz usuario/grupo/recurso/acción/contexto. Prueba una lectura permitida, escritura denegada y revocación con identidades ficticias. Una denegación de acceso a un log no demuestra ausencia de eventos. Los perfiles móviles, redirección de carpetas, OneDrive u otra sincronización requieren separación entre configuración, dato, caché, copia y retención. Reutiliza las fichas de D22/D23 en lugar de duplicar comandos incompatibles.

## 6. PAM y gestión de autenticadores

PAM puede abarcar bóveda, acceso temporal, aprobación, elevación controlada, proxy/registro de sesión y rotación. Una bóveda no equivale a todo PAM. CyberArk y BeyondTrust son ejemplos comerciales a evaluar por modalidad; gestores como KeePassXC pueden custodiar contraseñas, pero no ofrecen automáticamente el mismo control empresarial. No implantar un producto sin flujo de recuperación y operación.

La guía NIST SP 800-63B-4 permite enseñar longitud, bloqueo de contraseñas conocidas, limitación de intentos y autenticación resistente al phishing. Sus requisitos de longitud distinguen contraseña como factor único y como parte de MFA; no prescribe rotación periódica arbitraria ni reglas de composición como sustituto de los demás controles [P05]. No convertir estas recomendaciones en una modificación masiva sin contrastar política y ámbito.

Dos contraseñas no son dos factores. Correo OTP, passkey, TOTP y certificado tienen propiedades diferentes. Una passkey no elimina el problema de recuperación ni autoriza todo recurso. Nunca registrar valores de contraseñas, OTP, cookies, claves privadas o tokens para demostrar una práctica. El registro debe demostrar acciones y resultados sin exponer autenticadores.

## 7. Identidad, dispositivo y navegación

El objetivo no es «bloquear Internet», sino definir recursos y acciones permitidos por finalidad, identidad, dispositivo y dato. Diferencia acceso a correo corporativo y personal, navegación y aplicación nativa, red de oficina y móvil. DNS filtra nombres, firewall flujos y un SWG/proxy puede aplicar categorías o políticas HTTP según visibilidad; ninguno debe presentarse como control universal.

Para correo personal y WhatsApp, formula una política aprobada, excepciones y pruebas con cuentas/datos ficticios. Restringir un dominio puede afectar contenido legítimo o no cubrir la app/móvil. La inspección TLS solo observa lo que termina en esa capa, no descifra automáticamente E2EE. Certificados fijados, mTLS, QUIC, ECH y dispositivos no gestionados exigen diseño de cobertura, no desactivar validaciones indiscriminadamente. [D24](#/recurso/D24) contiene matriz, privacidad y límites; WhatsApp describe E2EE de mensajes personales [P06].

## 8. Métricas y controles de aceptación

Mide bajas revocadas en plazo, privilegios sin dueño, cuentas caducadas activas, excepciones vencidas, permisos retirados en cambios y cobertura de revisiones. Indica fuente, población y ventana. Revisión de acceso no significa que el aprobador comprendiera cada permiso: exige contexto y evidencia.

Antes de automatizar, implementa modo consulta, validación, registro, idempotencia, límites y rollback. Ningún script debe modificar masivamente un directorio porque una hoja de cálculo tenga una columna vacía. Una prueba de baja incluye sesión existente y nueva autenticación cuando el laboratorio y la plataforma lo permitan.

## Prácticas y evaluación

**INT-L15: proceso JML sintético.** Diseña alta, cambio y baja de tres identidades ficticias con entidad/centro/puesto y dos aplicaciones. Introduce una excepción de siete días y una combinación incompatible. Evidencia: RACI, matriz antes/después, expiración y comprobaciones. Éxito: no clonar todos los accesos de otro usuario ni confundir baja laboral con borrado inmediato de todos los datos.

**INT-L16: acceso por contexto.** Define para un grupo de laboratorio lectura corporativa permitida, subida de un documento sintético restringida y mensajería personal conforme a una política dada. Describe controles en dispositivo, identidad, red y aplicación, así como huecos de cobertura. Evidencia: pruebas positivas/negativas diseñadas y procedimiento de excepción. No interceptar tráfico de alumnos ni instalar certificados en equipos personales.

Autoevaluación: ¿es un usuario que cambia de puesto un alta nueva sin baja anterior? No: hay que recalcular y retirar accesos. ¿Es un perfil local la identidad del directorio? No. ¿Una bóveda de contraseñas demuestra PAM completo? No: verificar aprobación, alcance, sesiones, rotación y recuperación.
<!-- EN -->
# Identity lifecycle: from onboarding to verified revocation

**Reading D33.** Govern effective access throughout its lifecycle. Complements [D22](#/recurso/D22), [D23](#/recurso/D23), [D24](#/recurso/D24), [D25](#/recurso/D25) and M07/M17/M18. Sources P01–P06 are in [D36](#/recurso/D36).

## 1. Person, identity, account and profile

One person may have multiple identities/accounts; a service account need not represent a person. Identity, authenticator, session, group, role, permission and profile are different objects. Profiles contain preferences and user data; removing one does not necessarily revoke directory memberships or tokens.

Separate local, domain/directory, SaaS and application accounts. LDAP is a directory protocol; AD DS combines directory with authentication and policy capabilities. Microsoft Entra ID is not simply a renamed local domain controller. SSO applications still require authorization. FreeIPA and Keycloak illustrate different open-source capabilities: system/service identity integration versus application federation/access [P01–P03].

## 2. Authoritative source and entity–site–job model

Use approved workforce/collaboration attributes: stable ID, entity, site, unit, job, manager, relationship, dates and status. Email or display name should not be the only permanent identifier. Assign data correction and reconciliation responsibilities.

A job can suggest an access package without inheriting every historical permission of its former holder. Connect business role, technical role, group and specific permissions. Resource owners approve need, IAM implements, security examines conflicts and audit verifies with appropriate independence. Record approvals and exceptions.

## 3. Joiners, movers, leavers and variants

| Event | Minimum teaching flow | Success evidence |
|---|---|---|
| Joiner | Valid source→approval→account→minimum access→device→training | Correct identity, positive/negative access checks and recorded delivery |
| Mover | New job/site→access comparison→remove former rights→approve temporary exceptions | No unjustified accumulation |
| Leaver | Date/urgency→access/session revocation→assets→retention→verification | Denied access and reassigned work/secrets |
| Absence/suspension | Temporary policy and owner | State, expiry and approved reinstatement |
| Rehire | Validate relationship and recalculate access | No blind restoration of old privilege |
| Supplier/visitor | Sponsor, purpose and expiry | Expiration/review without orphan accounts |
| Emergency | Controlled exceptional identity | Justified use, alert and post-use review |
| Non-human account | Owner, workload, secret/certificate and rotation | No unnecessary interactive access; tested revocation |

Disabling an account does not guarantee invalidation of every token, cached session, SSH key or integration credential. Verify effective access systems within their documented mechanisms and limits. Auditing credential ownership/rotation does not require extracting secrets.

## 4. RBAC, ABAC and toxic combinations

RBAC assigns permissions through roles; ABAC evaluates subject, resource, action and environmental attributes through policies [P04]. They can coexist: roles may establish baseline access while attributes constrain site, sensitivity or device posture. Avoid unexplainable role proliferation and policy complexity.

Separation-of-duty conflicts include requesting/approving the same payment, independently developing/approving critical releases, or granting and auditing one's own privilege. «Toxic» describes a combination relative to a risk criterion, not a person's character. Define conflicts, compensation, authority and expiry. Tools detect modeled conflicts; they do not design governance automatically.

## 5. Effective permissions and shares

For Linux/macOS examine ownership, groups, parent-directory traversal, ACLs and additional controls; for Windows examine NTFS/share permissions, inheritance, groups and policy. SMB access involves both share and object permissions; permissions are not numbers to add. For SaaS/cloud examine links, guests, roles and application authorization.

Build a user/group/resource/action/context matrix. Test allowed reading, denied writing and revocation using fictional identities. Denied access to logs does not demonstrate no events. Roaming profiles, folder redirection and synchronization need distinctions between settings, data, cache, backup and retention. Reuse D22/D23 rather than duplicating incompatible commands.

## 6. PAM and authenticator management

PAM can include vaults, time-limited access, approvals, controlled elevation, session brokering/recording and rotation. A vault alone is not full PAM. CyberArk and BeyondTrust are commercial examples requiring offering-specific evaluation. Password managers such as KeePassXC may store credentials without supplying the same enterprise controls. Implementation needs recovery and operating procedures.

NIST SP 800-63B-4 supports teaching length, compromised-password blocklists, attempt throttling and phishing-resistant authentication. Length requirements distinguish single-factor passwords from passwords used within MFA; arbitrary periodic changes and composition rules do not replace other controls [P05]. Do not turn guidance into an unreviewed mass policy change.

Two passwords are not two factors. Email OTP, passkeys, TOTP and certificates have different properties. Passkeys do not remove recovery or authorize every resource. Never log passwords, OTPs, cookies, private keys or tokens to prove an exercise. Record actions/results without exposing authenticators.

## 7. Identity, device and browsing

Define permitted resources/actions by purpose, identity, device and data rather than simply «blocking the Internet». Separate corporate/personal mail, web/native apps and office/cellular access. DNS filters names; firewalls filter flows; SWGs/proxies can enforce categories/HTTP policies according to visibility. None universally covers all situations.

For personal mail and WhatsApp, define an approved policy, exceptions and tests with fictitious accounts/data. Domain blocking may affect legitimate services or miss native/cellular use. TLS inspection does not automatically decrypt E2EE. Pinning, mTLS, QUIC, ECH and unmanaged devices require coverage design, not indiscriminate disabling of validation. [D24](#/recurso/D24) covers matrices, privacy and limitations; WhatsApp documents personal-message E2EE [P06].

## 8. Metrics and acceptance

Measure timely leaver revocation, ownerless privileges, active expired accounts, expired exceptions, removed mover access and review coverage. State source, population and period. An approval checkbox does not prove that its reviewer understood each permission; provide context and evidence.

Before automation require read-only mode, validation, logging, idempotence, limits and rollback. No script should mass-modify a directory because a spreadsheet column is blank. Where the lab/platform permits, test both existing sessions and new authentication after revocation.

## Exercises and assessment

**INT-L15: synthetic JML process.** Design join/move/leave flows for three fictitious identities with entity/site/job attributes and two apps. Add a seven-day exception and one conflicting permission combination. Evidence: RACI, before/after access, expiry and checks. Success: no blind cloning of another person's rights or immediate deletion of all leaver data.

**INT-L16: contextual access.** For an assigned group define permitted corporate reading, restricted upload of a synthetic document and personal messaging under a supplied policy. Describe endpoint, identity, network and app controls plus coverage gaps. Evidence: designed positive/negative checks and exception procedure. Do not intercept student traffic or install certificates on personal devices.

Self-check: is a mover simply a new joiner without prior-access removal? No: recalculate and withdraw rights. Is a local profile the directory identity? No. Does a password vault prove complete PAM? No: examine approval, scope, sessions, rotation and recovery.
