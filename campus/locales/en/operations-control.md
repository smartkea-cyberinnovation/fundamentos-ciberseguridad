# D22 · Operational control: identities, profiles and hardening

**Parallel ES/EN teaching edition · 21 September 2026.** Extends M07, M08, M17, M18, M19, M22 and M23 without adding planned hours or changing existing progress. Exercises require assigned lab devices and instructor approval. Reading is not execution.

[Networks and shared resources](#/recurso/D23) · [Browsing and TLS](#/recurso/D24) · [Detection and acceptance](#/recurso/D25)

## 1. What it means to control a system

The goal is not to observe a person's entire life. It is to know which devices and services we manage, who may do what, which policy is actually effective, how deviations are detected and how service is recovered. An unknown device does not become compliant because it emits no alerts.

For each device record an inventory ID, owner, purpose, OS/edition/version, support status, location, management state, directory identity, last observation, necessary exposure and recovery method. Relate devices to accounts, data, services, rules and log sources. Keep passwords, tokens and recovery secrets out of the inventory and Git.

Before acting, identify host, session, shell, version, working directory, privileges and scope. Afterwards verify effective state, record results and test recovery. A management console reports what its agent declared; an actual test from the affected identity provides additional evidence.

## 2. Local identity, LDAP, AD DS and Entra ID

A **local account** belongs to a device's identity authority. Identical usernames on two machines need not represent the same identity. Linux uses UID/GID and name resolution through NSS; Windows uses SIDs and access tokens; macOS combines local identities with platform-specific controls.

**LDAP** is a directory access protocol, subject to authentication and permissions. It is not by itself a Windows domain, MFA, Group Policy or complete governance system. Distinguish identity lookup, authentication and authorization: a successful bind does not grant access to every directory object.

**Active Directory Domain Services** provides directory and domain services. Study DNS, Kerberos, objects, groups, organizational units, computers, replication and delegation. An OU organizes objects and policy scope; it is not an authorization group. Permission to join a computer need not include domain administration.

**Microsoft Entra ID** is a cloud identity service, not an AD DS domain controller or a guarantee that a legacy LDAP application can connect directly. Distinguish registered, domain-joined, Entra-joined and hybrid devices. Document attribute authority and synchronization effects.

SSSD/realmd on a Linux AD client connect name resolution, authentication, access decisions and home-directory creation. DNS and time are identity dependencies. Ubuntu's official example permits credential caching: an offline login does not demonstrate recent validation by the domain controller. [Ubuntu: SSSD with AD](https://ubuntu.com/server/docs/how-to/sssd/with-active-directory/).

## 3. A testable joiner, mover and leaver lifecycle

**Joiner:** obtain resource-owner approval; create an individual identity; assign role-based groups; expire temporary access; choose authentication appropriate to the service; create a profile only where required. Test one permitted resource and one explicitly prohibited resource.

**Mover:** remove incompatible previous access when assigning the new role. Review nested groups and direct grants. Do not copy every permission from another employee, who may retain obsolete privileges or exceptions.

**Leaver:** inventory directory and local accounts, SaaS access, sessions, tickets, certificates, SSH keys, devices and associated service accounts. Disabling one account does not immediately invalidate every existing session or offline login. Define revocation windows and test new sessions, existing sessions, offline clients and reconnection. Access removal, data retention and profile deletion may have different schedules and owners.

**Non-human identities:** require an owner, purpose, allowed resources and rotation. Avoid interactive sign-in when unnecessary and do not place employee credentials inside scheduled tasks. Managed service accounts, managed identities and alternatives depend on the actual platform and application.

**Privilege:** separate ordinary and administrative identities, delegate narrowly, review grants and maintain audited emergency recovery. Windows LAPS manages local administrator passwords on supported systems; it is not a complete PAM deployment or an access review for the directory. Report management status, not the password itself. [Microsoft: Windows LAPS](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview).

## 4. Effective permissions and resulting policy

A valid login, group membership and effective access are different observations. Examine stable identity, direct/nested groups, current token or cache, ACLs, inheritance, rights and additional controls. A changed group may require a refreshed access context; a pre-existing session retaining rights does not alone prove that the change failed.

Linux checks may involve parent-directory permissions, ACL masks, sudo, capabilities and SELinux/AppArmor. Windows adds token groups, DACLs, logon rights, UAC and application policy. macOS also involves TCC, the process identity, management profiles and platform protections. Do not grant universal permissions or switch off protection to hide an access problem.

Separate local settings, GPO and MDM. Record the source, user/device scope, applicable precedence, conflicts, last update and effective result. Precedence between a particular GPO and MDM setting is not universal: inspect the actual configuration and device, not only the management console.

## 5. Five meanings of profile

| Profile | Meaning | What it does not establish |
|---|---|---|
| OS user profile | Home, preferences and session-related data | Not identical to a directory account or verified backup |
| Roaming, redirection or profile container | Location and persistence of part of the environment | Synchronization is not backup or universal version compatibility |
| Browser profile | Browser cookies, extensions, preferences and sessions | Not strong isolation from the owner of the same OS account |
| Configuration/MDM profile | Settings delivered to a device or user | Installation alone does not demonstrate effective settings |
| Network/firewall profile | Context used to apply host rules | Does not necessarily identify a person or SaaS tenant |

On shared computers verify that user B does not inherit user A's documents, sessions or autofill. Define sign-out, cleanup and intentional persistence. Do not copy real profiles to Git or a peer's device. Test recovery of synthetic data and preferences separately from secrets.

## 6. Role-specific baseline and hardening

Select a baseline for the OS, version and role: a teaching workstation and a domain controller have different needs. Use inventory → chosen baseline → deviation → impact → change in clone → functional/negative tests → recovery → staged rollout → drift detection.

Evaluate support/patches, privileged accounts, service permissions, allowed software, remote administration, encryption/recovery, firewall, auditing/time, backup/restore, endpoint protection/agent health, secrets and managed browser/network settings. Distinguish not applicable and not checked from passed.

A hardening score is not certification. Wazuh SCA illustrates open-source configuration checks whose results depend on policy, permissions and platform; one successful check does not validate the entire host. [Wazuh: SCA](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/index.html).

Do not change authentication, firewall and remote access simultaneously without recovery access. Custody of recovery material precedes encryption. Do not disable SIP, Gatekeeper, Defender, SELinux or auditing to complete an exercise.

## 7. Initial lab queries

These are read-oriented examples, not zero-impact forensic acquisition. Check local help and permissions; output may contain personal data. Missing tools or denied access are limitations, not proof that a control is absent.

```bash
# Linux: bounded context and state
id
uname -s
getent passwd "$(id -un)"
systemctl --failed
```

```powershell
# Windows: stable group SID rather than a localized group name
$PSVersionTable.PSVersion
whoami /user
Get-LocalGroup -SID 'S-1-5-32-544' | Get-LocalGroupMember
gpresult /r
```

```sh
# macOS: system, identity and enrollment status
sw_vers
id
profiles status -type enrollment
```

Success means explaining both provenance and a limitation. Installing PowerShell on Linux does not provide native Windows LocalAccounts or Group Policy APIs.

## 8. Self-check and deliverable

A disabled user can log in offline and read a previously downloaded document. Does this prove the directory ignored the account disable? No: distinguish cached authentication, local data, sessions/tickets and online revocation. Plan reconnection testing and device handling without destroying data needed for retention.

Deliver an identity–role–resource–action matrix, resulting-policy report and lifecycle record with positive and negative tests. Justify each permission and remove one while preserving legitimate administration. D25 supplies twelve acceptance designs.

# D23 · Operational control: networks, folders and shared resources

**Parallel ES/EN teaching edition · 21 September 2026.** Extends M07, M09, M10, M17, M18, M22 and M24. [Identity](#/recurso/D22) · [Browsing](#/recurso/D24) · [Detection](#/recurso/D25). Work only with assigned networks and accounts; the campus does not configure corporate systems.

## 1. Model access before configuring it

A share is more than a visible folder. Record service, server/NAS, protocol, data location, identity, groups, permissions, source network, encryption, auditing, backup and owner. All relevant layers contribute: a firewall rule allowing SMB does not grant file access.

Model person/account → session/groups → network path → service authentication → share permissions → object permissions → additional controls. Draw local and remote access separately because local access does not necessarily traverse a share ACL.

Windows SMB access must pass the applicable share and NTFS checks. This is not arithmetic addition: identity, token, inheritance and denials matter. Samba also involves Unix identity mapping and host permissions. [Samba: smb.conf](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html).

## 2. Role-based folder design

Use a fictional `curso.test` environment with ProjectReaders, ProjectEditors and ProjectCustodians. Readers open approved documents, editors change approved content, and custodians manage permissions using a separate identity. Avoid direct individual grants except documented exceptions.

| Resource | Readers | Editors | Custodians | Guests |
|---|---|---|---|---|
| Published material | Read | Read | Administer within role | Read only if public |
| Team submissions | Read authorized objects | Create/edit authorized objects | Recover and manage ACLs | No access |
| Restricted evidence | No general access | No general access | Explicitly approved individual access | No access |

This is a design, not an applied configuration. Define tests for listing, opening, creating, editing, renaming, deletion, ACL changes and direct-path access. Hiding a folder or share during enumeration is not equivalent to preventing direct access.

Check inheritance when moving data. Compare permissions before and after copies/moves within a volume, across volumes and through backups. Different tools may preserve owners, ACLs, labels and attributes differently.

## 3. Windows, Samba/NAS and NFS

**Windows/SMB:** record negotiated protocol, authentication, signing, encryption, identity and share. Signing protects message integrity/authenticity; encryption protects transport confidentiality. They are not interchangeable. Defaults and requirements vary by OS, edition and version. Do not disable signing or enable obsolete SMB to conceal an incompatibility. [Microsoft: SMB security](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security).

**Samba/NAS:** distinguish file server, domain member and Samba AD controller. Keep SID–UID/GID mapping stable, document ranges/backends before restore or domain changes, and account for server modules and Unix permissions. Test Windows/Linux/macOS clients rather than declaring equivalence because the folder appears in a file manager.

**NFS:** record version, export, allowed clients, identity, security mode and options. Trusting client-supplied UID/GID is not strong authentication. `root_squash` reduces one class of remote privilege but does not replace identity/authorization design. Evaluate Kerberos and transport protections for the actual service, using the chosen server's manual rather than universal options.

**Downloaded copies:** removing share access does not automatically remove data already stored locally. Classification, DLP, retention and device recovery address that separate risk. Decide evidence retention before cleanup.

## 4. Host networking and segmentation

Inventory physical/virtual interfaces, IPv4/IPv6, routes, DNS, time, proxies, managed tunnels, listeners and firewalls. Associate each listener with process, service, identity and purpose. Loopback exposure differs from all interfaces or a particular segment.

Define source zone/device, destination/service, transport/port, direction, state, justification, owner and logging for each flow. Separate administration, users, servers, guests/BYOD and lab networks. A VLAN alone does not specify every interconnection rule.

Permit necessary flows while retaining management/recovery. Check return paths and dependencies such as DNS, time, DHCP and authentication. Include IPv6 and virtual adapters instead of claiming isolation from IPv4-only checks.

Remote administration uses approved endpoints, restricted origins, verified authentication, least privilege and recorded closure. Do not publish SMB, RDP, WinRM or administration consoles to the Internet for convenience. Inbound filtering does not demonstrate controlled egress; see D24.

## 5. GUI and terminal evidence

These queries do not change policy. Use existing synthetic paths/share names, read local help and avoid uploading real identities in complete outputs.

```bash
# Linux: assigned lab host only
ip address
ip route
ss -lnt
getfacl -- ./datos-laboratorio
```

```powershell
# Windows: correlate GUI, service and filesystem state
Get-NetIPConfiguration
Get-NetFirewallProfile
Get-SmbShare -Name 'ProyectoLaboratorio'
Get-SmbShareAccess -Name 'ProyectoLaboratorio'
Get-Acl -LiteralPath 'C:\Laboratorio\Proyecto'
```

```sh
# macOS: inspect without changing networking or expanding privacy permissions
scutil --dns
scutil --proxy
route -n get default
ls -lde@ ./datos-laboratorio
```

`netsh winhttp show proxy` reports WinHTTP, not every Windows application or browser. A macOS proxy preference is not the same component as a managed network filter. Shell proxy variables do not guarantee every Linux service takes the same route.

Denied access limits observation. Do not automatically elevate or enumerate unrelated directories. Compare the product GUI, an actual access test and server-side logs.

## 6. Recovery that preserves security

Restore synthetic data to an alternative path. Verify content, size/hash, ownership, groups, ACL/inheritance, relevant attributes and functional access for each role. Document known backup-format limitations.

Measure time until useful service, not only until copying ends. Ensure recovery does not restore obsolete permissions or misassign data to a reused username. Keep stable identities and review orphaned ownership. Directory backup and file-server backup have separate dependencies and procedures.

Compare observed recovery against agreed RPO/RTO. Snapshot, replication, synchronization and independent backup serve different purposes. Operational restoration and forensic preservation should not be conflated.

## 7. Minimum acceptance

Use reader, editor, delegated administrator and guest lab identities. Establish a new session for updated groups and document existing sessions separately. Test each operation, then test one permitted and one prohibited client zone without scanning external ranges.

Deliver a diagram, permission matrix, sanitized ACL export, test identity, permitted/denied results, server event, configuration diff and rollback. Connection failure alone does not prove an ACL blocked access; identify the deciding layer.

Self-check: a user cannot see the share in a list but can open its direct path. No denial has been demonstrated. Visibility and authorization differ; fix access according to the approved design, not merely by hiding a name.

# D24 · Browsing control: DNS, firewall, proxy, accounts and TLS

**Parallel ES/EN teaching edition · 21 September 2026.** Extends M10, M18, M22, M24 and M25. [Identity](#/recurso/D22) · [Shares](#/recurso/D23) · [Detection and acceptance](#/recurso/D25).

## 1. Begin with the required outcome

“Block personal email” is not yet an implementation. Identify people, managed devices, web/native clients, allowed organizational accounts, guests, locations and protected data. It is not equivalent to blocking every service from a provider, inspecting private messages or controlling all use of a personally owned phone.

A rule contract records ID, purpose, subject/group, device posture, network, application/destination, operation, action, enforcement point, precedence, exceptions, minimum logs, owner, expiry and tests. Distinguish proposed, configured, delivered, effective and verified states. The teaching site does not apply these rules to its readers.

## 2. Layers are not interchangeable

| Layer | Possible decision | Limitation to test |
|---|---|---|
| Protective DNS | Name/category resolution | Not URL paths, same-SaaS accounts or content; account for caching and actual resolver |
| Host/network firewall | Flows, apps or identity depending on product | A shared IP/NAT is not a reliable individual identity; port 443 permission is not web authorization |
| Explicit proxy/PAC | Steering compatible clients | A PAC setting alone does not force every application through it |
| Secure web gateway | Browsing/application policy over traffic received | Depends on identity, client, transport, visibility and edition |
| Managed browser | Settings, extensions, profiles and supported accounts | Does not automatically govern other browsers/native apps |
| IdP/tenant/application | Identity, tenant, session and application operations | The corporate IdP does not control every unrelated personal service |
| DLP | Defined data use/egress in supported channels | Not all formats/apps; TLS inspection does not decrypt application E2EE |
| WAF | Requests reaching a published application | Not users' outbound browsing proxy |

There is no universal precedence for this table. Document each product's rule combination and interactions between independent layers. Firewall permission does not override application denial, and an inspection exception must not accidentally become unrestricted access.

## 3. Establish user and device context

Correlate authentication, group and device with the connection. Test consecutive users on a shared workstation and distinct devices behind one NAT. Do not attribute every connection from an IP to the last logged-in user. Include system traffic without a user session and services using another identity.

Separate managed classroom/corporate endpoints, managed remote endpoints, servers, BYOD and guests. Prefer network segmentation and resource access controls over an interception CA on unmanaged personal equipment. Institutional Wi-Fi rules do not govern a personal mobile connection outside that network. State this boundary in reports.

Review effective DNS, proxy and routes, managed VPN, IPv6, DoH/DoT, QUIC/HTTP3 and permitted extensions. These protocols are not inherently malware. Administrators define supported behavior and validate product/version capabilities; the lesson does not teach evasion. Do not assert that all QUIC traffic is uninspectable. [Cloudflare: HTTP/3 inspection](https://developers.cloudflare.com/cloudflare-one/traffic-policies/http-policies/http3/).

## 4. Organizational versus personal email

A shared domain may serve several identities. Blocking it can break organizational email, collaboration or device functions. Microsoft describes both the shared-hostname issue and collateral effects of blanket `login.live.com` blocking. [Microsoft: tenant restrictions](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/tenant-restrictions).

Use supported tenant/account restrictions, application settings and managed-browser controls. Check the current generation's clients, licensing and limitations instead of copying a historical header and claiming universal coverage. [Microsoft: tenant restrictions v2](https://learn.microsoft.com/en-us/entra/external-id/tenant-restrictions-v2).

Test the own tenant, an approved external tenant, an unapproved tenant, a personal test account, a pre-existing session and a native client. Where enforcement is unsupported, document the gap and choose a different control or disallow that client on managed equipment. Never request students' personal credentials for testing.

Service blocking and data protection are separate. Limited browser use may coexist with supported restrictions on uploads, synchronization or external accounts. A proxy cannot infer every tenant from a hostname alone.

## 5. WhatsApp and messaging applications

Decide whether the objective is service blocking, a support-team exception, corporate-file protection or limiting notifications during an activity. Distinguish web client, native application and personal device and test every declared surface.

On managed devices, combine application control, gateway policy and client management where supported. Domain lists require maintenance; do not block all shared vendor infrastructure indiscriminately. Exceptions need group, device, purpose and expiry.

TLS inspection does not remove WhatsApp's message end-to-end encryption. A gateway may observe or control transport and available metadata; it must not promise plaintext of participant-to-participant encrypted conversations. [WhatsApp: conversation protection](https://blog.whatsapp.com/introducing-advanced-chat-privacy).

Validate DLP with a synthetic file in a supported channel. Do not inspect private conversations or deploy covert software to demonstrate effectiveness. When content cannot legitimately or technically be observed, state the limitation and use access/application controls where appropriate.

## 6. TLS inspection is a trust design

Use TLS terminology even when a product retains “SSL inspection.” Authorized inspection creates separate client–inspector and inspector–destination connections. It requires correct trust distribution, CA protection and upstream certificate validation. Do not use `--insecure`, blind certificate acceptance or global validation disablement as a fix.

Lifecycle: approval/scope → managed pilot → relevant trust stores → inspection policy → canary validation → justified exceptions → monitoring → rotation/removal. Inventory applications that use system trust and those with their own store.

Test certificate pinning, mTLS, ECH, transport support and update behavior. A no-decrypt exception must retain authorization, proportional logging and applicable controls. Limitations are product-specific. [Cloudflare: TLS decryption](https://developers.cloudflare.com/cloudflare-one/traffic-policies/http-policies/tls-decryption/).

Verify separately that the approved client trusts the inspector and that an invalid lab-server certificate is still rejected upstream. Inspection must not conceal loss of destination validation.

Do not decrypt sensitive services or BYOD traffic by default. Document lawful basis, purpose, necessity, proportionality, notice, log access, retention, exceptions and impact assessment where required. Spain's LOPDGDD Article 87 provides employment-specific safeguards, not a universal authorization for students or personal devices. This lesson is not legal certification. [BOE: LOPDGDD](https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673#a87).

## 7. Example policy for a managed classroom

This fictional teaching template is not an applied policy for SmartKEA or any institution. Resource owners and privacy stakeholders must adapt and approve a real deployment.

| ID | Scope/objective | Designed action | Expected evidence |
|---|---|---|---|
| NAV-01 | Managed device, course services | Allow campus and approved dependencies | Reading, resources and downloads work |
| NAV-02 | Managed device, email | Permit supported approved accounts/tenants | Approved test account succeeds; unapproved account denied |
| NAV-03 | Personal email on managed device | Block use outside the declared policy | Web/native tests and uncovered channels recorded |
| NAV-04 | Classroom messaging | Deny except narrowly scoped support access | Denial and expiring exception tested |
| NAV-05 | General browsing | Categories according to risk and purpose | User/group correlated with effective rule |
| NAV-06 | Managed TLS pilot | Inspect only approved scope | Canary trust and invalid-certificate rejection |
| NAV-07 | BYOD/guests | Separate network, minimal access, no intrusive CA by default | No SMB/admin access; campus available |
| NAV-08 | System traffic | Preserve required management, updates, DNS, time and PKI | Updates and recovery remain usable |

## 8. Rollout, exceptions and self-check

Start with minimized observation, then pilot and deployment rings. Record false positives, latency, support impact and rollback. Define continuity when the client/gateway fails per service: neither fail-open nor fail-closed is universally correct.

Exceptions require ID, requester, approver, reason, assets, rule, compensation, expiry and removal test. Avoid permanent emergency wildcards. Reassess after changes to SaaS, browser, OS, network client or certificates.

Self-check: “A blocked domain stopped WhatsApp Web, therefore every phone is blocked and I can read messages.” Unsupported: native clients, alternative network paths and device scope are untested; transport TLS and E2EE are distinct layers. Limit conclusions to observed tests and coverage.

# D25 · Detection, control matrices and acceptance laboratories

**Parallel ES/EN teaching edition · 21 September 2026.** Complements [D22](#/recurso/D22), [D23](#/recurso/D23) and [D24](#/recurso/D24), particularly M19, M23 and M27–M29. It does not install sensors or enforce restrictions on readers.

## 1. From configured to demonstrated controls

Record protected assets, implementation and evidence. Separate approved policy, delivered configuration, effective state, recent observation and actual test. Missing data is not green; an accepted exception is not an effective control.

| ID | Control | Positive and negative verification | Operational owner |
|---|---|---|---|
| OS-01 | Inventory/ownership | Known device listed; uninstrumented device explicitly uncovered | Systems |
| OS-02 | Support/patches | Approved version works; baseline deviation recorded | Systems |
| OS-03 | Accounts/privilege | Standard user works; cannot administer unrelated resource | IAM/systems |
| OS-04 | Lifecycle | New role works; previous access removed and sessions reviewed | IAM/owner |
| OS-05 | Directory/authentication | Resolution/authentication work; failures do not weaken validation | IAM |
| OS-06 | Offline/cache | Approved case works; revocation window measured | IAM/systems |
| OS-07 | Shared profiles | Own environment available; B does not inherit A's session/data | Workplace IT |
| OS-08 | ACL/shares | Reader reads/editor edits; guest and ACL change denied | Data owner |
| OS-09 | Segmentation/firewall | Approved flow works; unapproved source cannot reach service | Networks/systems |
| OS-10 | Identified browsing | Allowed group succeeds; other group receives expected denial | Networks/IAM |
| OS-11 | SaaS accounts | Approved tenant works; unapproved/personal blocked where supported | IAM/apps |
| OS-12 | TLS/privacy | Canary inspected; invalid server rejected and exceptions limited | Networks/privacy |
| OS-13 | Sensor/telemetry | Benign event received; missing heartbeat reports loss of coverage | SOC/systems |
| OS-14 | Detection/triage | Prepared case detected; expected activity not blindly called an incident | SOC |
| OS-15 | Response/containment | Authorized action reduces impact and preserves recovery | CSIRT/systems |
| OS-16 | Recovery/review | Data/ACL/service restored; removed permissions do not reappear | Systems/data |

Evidence records control, fictional asset, version, test identity, time/timezone, configuration before/after, source, result, limitations, approval and rollback. Minimize it: no conversations, credentials, whole real profiles or corporate reports in Git.

## 2. OS threat detection

Distinguish event, record, alert and incident. First establish what was observed and with what coverage; then assess a hypothesis of unauthorized behavior. Process names, IPs and isolated hashes do not alone attribute an attack to a person.

Sources include authentication/group changes, administrative use, services/tasks/autostart, process execution, share access, firewall/DNS/proxy changes, sensor health and application/egress logs. Not all exist by default: record audit settings, provider/channel, version and retention.

Windows Event Log and Sysmon provide different telemetry; Sysmon is not a SIEM or automatically a prevention system. Linux journal/syslog/audit and endpoint events depend on deployment. macOS Unified Log and agent-accessible events may be restricted or redacted. [Microsoft: Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon).

Use synthetic detections: administrative group change outside a ticket, uninventoried task, changed proxy, unusual execution location, repeated share denials, policy-blocked upload or missing sensor. Corroborate identity, host, parent/provenance when available, ticket, time and a second source.

Real malware is unnecessary. A labeled legitimate lab task can test visibility. Simulate lost ingestion with fixtures or approved maintenance, not agent evasion.

## 3. Triage, containment and recovery

Triage validates source/time, scopes host/user/service, assesses impact and ongoing activity, considers alternative hypotheses, prioritizes and records escalation or closure. Distinguish false positive, real but authorized activity and insufficient evidence.

Choose host isolation, access revocation, flow restriction or service suspension according to authority and impact. Preserve management/recovery. EDR containment can interrupt collection or service: explain the trade-off.

Protect originals, use working copies, hashes and a log of actions. Live reading may change state or generate events. Decide retention before deleting profiles or clearing anything. Restore known-good data/configuration, verify functionality and permissions, watch for recurrence and close with control improvements. [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

## 4. Twelve testable laboratory designs

These are complementary designs, not executed native labs or additional hours. The instructor validates versions/resources first. All require synthetic data, assigned equipment, approved scope and recovery access.

### OPS-L01 · Inventory and baseline

Objective: separate coverage from compliance. Environment: VM and baseline sheet. Tasks: inspect version, identity, selected services, firewall and sensor; compare GUI/CLI; label missing data. Evidence: minimal inventory and two explained differences. Success: unknown never becomes passed. Recovery: no configuration changes; handle test reports under retention policy.

### OPS-L02 · Joiner, mover and leaver

Objective: verify lifecycle. Environment: isolated directory and fictional identities. Tasks: group-based provisioning, permitted/denied tests, role change removing former privileges, disable and new/existing-session checks. Evidence: access matrix and effective times. Success: no dependence on global administrator for ordinary tasks. Recovery: remove temporary accounts while retaining required evidence/data.

### OPS-L03 · Identity and offline cache

Objective: understand revocation limits. Environment: lab client with known cache policy. Tasks: record online access, instructor-prepared disconnection, disabled-account case and reconnection; never change a real directory. Evidence: sequence/windows. Success: distinguish account, ticket, cache and local file. Recovery: reconnect and preserve results before snapshot restoration.

### OPS-L04 · Shared profiles

Objective: separate configuration and personal state. Environment: two fictional users and a browser without real accounts. Tasks: create test document/preference, sign out, sign in as other user, verify isolation and compare OS/browser profiles. Evidence: persistence/access table. Success: B does not inherit A's sessions or data. Recovery: remove only test profiles through a documented procedure.

### OPS-L05 · Share and filesystem permissions

Objective: test both layers. Environment: synthetic folder with reader/editor/guest. Tasks: inspect ACLs, test read/write/permission changes locally and remotely, compare restored copy. Evidence: matrix/server logs. Success: denial attributed to an observed layer. Recovery: restore initial ACLs and remove the test share.

### OPS-L06 · Segmentation

Objective: test permitted/prohibited origins. Environment: two assigned clients and one test service. Tasks: document route/listener/rule, test only that destination/port, check IPv4/IPv6 and return path. Evidence: flow matrix/results. Success: administration remains available and service access matches scope. Recovery: remove the test rule using available console access.

### OPS-L07 · DNS and proxy

Objective: distinguish layers. Environment: `.test` names and a lab gateway. Tasks: compare resolution, connection and HTTP response; apply synthetic policy; observe identity/rule; distinguish browser proxy and WinHTTP where applicable. Evidence: positive/negative tests. Success: NXDOMAIN is not called HTTP inspection evidence. Recovery: restore initial settings.

### OPS-L08 · SaaS accounts

Objective: validate account/tenant policy. Environment: authorized test tenants/accounts or explicitly offline fixtures. Tasks: own tenant, approved external and unapproved account; web/native clients and prior session; document limits. Evidence: matrix identifying native versus simulated testing. Success: legitimate email preserved. Recovery: revoke test sessions and remove temporary assignments.

### OPS-L09 · Messaging and file egress

Objective: test the declared boundary. Environment: simulated classroom policy and harmless file. Tasks: distinguish application/domain/upload control, limited support permission and denied case; analyze synthetic metadata. Evidence: coverage table. Success: no claims of reading E2EE or controlling out-of-scope phones. Recovery: remove and verify expiry of the temporary exception.

### OPS-L10 · TLS canary

Objective: validate trust and limits. Environment: managed VM, lab CA and owned server, no personal accounts. Tasks: approve scope, observe uninspected channel, apply test profile, validate inspector certificate and upstream invalid-server rejection, test narrow exclusion. Evidence: public certificate properties/decisions, never private keys. Success: validation remains enabled. Recovery: remove test CA/profile from the stores used and confirm normal access while protecting CA material.

### OPS-L11 · Detection and data quality

Objective: test detection and coverage. Environment: labeled benign task and synthetic logs from three OSs. Tasks: predict event, follow source/collector, correlate ticket, add negative control and simulated ingestion gap. Evidence: rule/query, positives, false positives and measured delay. Success: silent sensor not reported healthy. Recovery: remove the task without erasing case logs.

### OPS-L12 · Incident and restore

Objective: decide with evidence and recover. Environment: synthetic permission/proxy-change case. Tasks: triage, preserve, choose containment, restore data/ACL/policy, test legitimate and prohibited identities, describe residual risk. Evidence: timeline, custody record and runbook. Success: functional recovery and proportionate conclusions. Recovery: return to baseline after acceptance and preservation.

## 5. Applied glossary and implementation examples

Examples illustrate documented capabilities, not purchase advice or universal equivalence. Record product, edition, license, OS and version before choosing a lab. No installation is claimed here.

| Term | Purpose and contrast | Examples to study |
|---|---|---|
| Directory | Identities/attributes; protocol is not a complete service | AD DS, FreeIPA; LDAP protocol |
| Identity client | Host lookup, authentication and access | SSSD/realmd; native Windows integration |
| Local administrator management | Host privilege with controlled recovery | Windows LAPS; delegated sudo |
| Configuration profile | Managed settings, not the user's home | Apple MDM profiles; Windows CSP/GPO as applicable |
| File share | Identity, ACL and protocol | Windows SMB, Samba, compatible NAS |
| SMB signing | Integrity, not confidentiality alone | Supported client/server SMB implementations |
| Protective DNS | Name/query control, not a SaaS account selector | Cloudflare Gateway DNS policy; lab resolvers |
| Secure web gateway | Outbound browsing with identity/visibility | Cloudflare Gateway, distinct from Cloudflare WAF |
| Tenant restriction | Supported account/instance control | Microsoft Entra tenant restrictions |
| TLS inspection | Separate connections under managed trust | Gateway decryption policy and controlled CA |
| End-to-end encryption | Participant protection beyond transport TLS | WhatsApp messaging; proxy TLS does not remove it |
| Security configuration assessment | State versus rules, not full certification | Wazuh SCA and selected policies |
| Telemetry | Data with source/coverage/time | Sysmon, journal, Event Log, Unified Log |
| Configuration drift | Deviation from approved state | Versioned inventory/periodic assessment |
| Exception | Scoped, expiring deviation | Owner's exception register |
| DLP | Data protection in supported channels | Endpoint/SaaS controls chosen after testing |

FreeIPA integrates Linux-oriented identity/policy capabilities; it is not taught as an identical AD DS clone. [FreeIPA: About](https://www.freeipa.org/page/About). Apple filtering/profile support depends on enrollment and payload constraints. [Apple: Filter content](https://support.apple.com/guide/deployment/filter-content-dep1129ff8d2/web). Wazuh SCA and Sysmon perform different jobs: configuration checking is not incident correlation or prevention by itself.

## 6. Metrics and closure

Use explicit denominators: recently reporting devices / expected devices; verified controls / applicable controls; timely revocations / evaluated leavers; expired exceptions / active exceptions; successful restores / drills. Separate not applicable, untested and noncompliant. Do not hide critical privilege or evidence gaps in an overall average.

Suggested rubric: scope/model 20%, correct operation 25%, security/privacy 20%, evidence 20%, recovery/limitations 15%. Critical conditions still apply: remain in scope, no unauthorized interception, no secret disclosure or destruction of originals. Mobile reading and simulations are useful but labeled according to what they demonstrate.
