<!-- ES -->
# Glosario maestro de informática y ciberseguridad

**Lectura D40.** Complementa D35. Las definiciones son docentes y deben enlazarse a la fuente normativa/técnica cuando el contexto lo requiera.

## Computación y datos
**bit** unidad binaria · **byte** ocho bits · **nibble** cuatro bits · **word** unidad natural de una arquitectura · **encoding** representación de símbolos · **ASCII/Unicode/UTF-8** estándares/codificación de texto · **endianness** orden de bytes · **integer/floating point** representaciones numéricas · **overflow** resultado fuera del rango · **algorithm** procedimiento finito · **data structure** organización de datos · **complexity** coste de recursos · **compiler/interpreter/runtime** traducción/ejecución/entorno · **API/ABI/ISA** contratos entre software, binarios y hardware.

## Hardware y sistemas
**CPU, core, thread, register, ALU, cache, RAM, ROM, bus, DMA, interrupt, GPU, NPU, SoC, NIC, SSD, NVMe, firmware, BIOS, UEFI, TPM, Secure Boot** · **kernel, syscall, process, thread, scheduler, virtual memory, page, filesystem, inode, ACL, service/daemon, package, repository, shell, environment variable, PATH, privilege, sandbox, hypervisor, VM, container, namespace, cgroup**.

## Redes
**LAN/WAN/PAN**, **Ethernet**, **MAC**, **ARP/NDP**, **switch**, **router**, **gateway**, **VLAN**, **IP/CIDR/subnet**, **route**, **NAT**, **TCP**, **UDP**, **QUIC**, **port/socket**, **DNS**, **DHCP**, **NTP**, **HTTP**, **TLS**, **SSH**, **SMTP/IMAP**, **proxy/reverse proxy**, **load balancer**, **CDN**, **VPN**, **Wi-Fi**, **SSID**, **BGP**, **ASN**, **latency/jitter/throughput/loss**.

## Desarrollo y cloud
**source code, repository, commit, branch, merge, CI/CD, artifact, dependency, package manager, SBOM, API, REST, JSON, database, SQL, transaction, index, cache, queue, event, microservice, monolith, serverless, IaaS/PaaS/SaaS, region/AZ, IaC, immutable infrastructure, orchestration, Kubernetes pod/deployment/service/ingress, observability, log/metric/trace, SLI/SLO/SLA, RTO/RPO**.

## Seguridad
**asset** activo · **threat** amenaza · **threat actor** actor de amenaza · **vulnerability** vulnerabilidad · **weakness** debilidad · **exploit** mecanismo que aprovecha una condición · **exposure** exposición · **likelihood** probabilidad · **impact** impacto · **risk** riesgo · **inherent/residual risk** antes/después de controles · **control/safeguard** medida · **attack surface** superficie de ataque · **CIA** confidencialidad/integridad/disponibilidad · **authenticity/accountability/non-repudiation/resilience** · **least privilege**, **need to know**, **defence in depth**, **zero trust**, **segmentation**, **hardening**, **patching**, **baseline**, **vulnerability management**, **penetration test**, **red/blue/purple team**.

## Criptografía e identidad
**plaintext/ciphertext**, **symmetric/asymmetric encryption**, **key**, **nonce**, **IV**, **hash**, **salt**, **HMAC**, **digital signature**, **certificate**, **CA**, **PKI**, **key rotation**, **crypto-agility**, **PQC** · **identity**, **account**, **authentication**, **authorization**, **MFA**, **SSO**, **federation**, **LDAP**, **Kerberos**, **SAML**, **OAuth 2.0**, **OpenID Connect**, **JWT**, **RBAC**, **ABAC**, **SoD**, **JML**, **IAM**, **IGA**, **PAM**, **JIT/JEA**.

## Operaciones de seguridad
**event**, **alert**, **incident**, **case**, **log source**, **telemetry**, **SIEM**, **SOAR**, **EDR/XDR/NDR**, **IDS/IPS**, **WAF**, **SOC**, **CSIRT/CERT**, **IOC**, **IOA**, **TTP**, **ATT&CK technique**, **threat intelligence**, **threat hunting**, **triage**, **containment**, **eradication**, **recovery**, **lessons learned**, **forensics**, **chain of custody**, **timeline**, **artifact**, **memory dump**, **PCAP**, **false positive/negative**, **detection engineering**.

## Gobierno, riesgo y cumplimiento
**governance**, **policy/standard/procedure/guideline**, **GRC**, **risk owner**, **asset owner**, **risk appetite/tolerance**, **risk register**, **treatment**, **accept/avoid/transfer/mitigate**, **KPI/KRI**, **audit**, **assurance**, **evidence**, **control objective**, **maturity**, **NIST CSF profile/tier**, **ISMS/SGSI**, **third-party risk**, **supply-chain risk**, **business continuity**, **BCP**, **DRP**, **BIA**, **crisis management**.

## Privacidad y regulación
**personal data**, **special-category data**, **controller**, **processor**, **data subject**, **processing**, **purpose limitation**, **data minimisation**, **retention**, **lawful basis**, **consent**, **DPO/DPD**, **DPIA/EIPD**, **privacy by design/default**, **breach**, **international transfer**, **pseudonymisation/anonymisation** · **ENS, NIS2, DORA, CRA, AI Act, CER, eIDAS2**, distinguiendo siempre norma, estándar, guía y contrato.

## Amenazas
**malware**, **virus**, **worm**, **trojan**, **ransomware**, **spyware**, **rootkit**, **botnet**, **phishing**, **spear phishing**, **smishing/vishing**, **BEC**, **credential stuffing**, **password spraying**, **brute force**, **session hijacking**, **injection**, **XSS**, **CSRF**, **SSRF**, **path traversal**, **deserialization**, **memory corruption**, **privilege escalation**, **lateral movement**, **persistence**, **exfiltration**, **DoS/DDoS**, **supply-chain compromise**, **insider threat**. Estudiar para reconocer/prevenir/detectar; la práctica ofensiva requiere laboratorio autorizado.

## IA y cuántica
**AI/ML/DL**, **training/inference**, **dataset**, **feature**, **embedding**, **transformer**, **LLM**, **token/context window**, **prompt**, **RAG**, **agent/tool**, **hallucination**, **evaluation**, **guardrail**, **prompt injection**, **data poisoning**, **model extraction**, **adversarial example**, **AI RMF** · **qubit**, **superposition**, **entanglement**, **quantum gate/circuit**, **Shor/Grover**, **QKD**, **post-quantum cryptography**, **crypto inventory**.

## Carrera e innovación
**NICE work role**, **ECSF profile**, **competency/skill/knowledge**, **portfolio**, **CTF**, **bug bounty**, **responsible disclosure**, **CVE/CWE/CVSS**, **paper/preprint/peer review**, **TRL**, **MVP**, **PoC**, **pilot**, **product-market fit**, **startup**, **incubator/accelerator**, **venture capital**, **grant**, **public procurement**, **dual-use**, **technology transfer**, **IPR**.

## Pares que no deben confundirse
Internet ≠ Web · encoding ≠ encryption · hashing ≠ encryption · authentication ≠ authorization · backup ≠ replication ≠ snapshot · vulnerability ≠ risk · event ≠ alert ≠ incident · SIEM ≠ SOC · IDS ≠ IPS · EDR ≠ antivirus · compliance ≠ security · privacy ≠ secrecy · CSIRT/CERT ≠ SOC · policy ≠ procedure · KPI ≠ KRI · RTO ≠ RPO · CVE ≠ CWE ≠ CVSS · AI model ≠ agent · quantum computing ≠ PQC ≠ QKD.

<!-- EN -->
# Master computing and cybersecurity glossary

**English summary.** The full English teaching edition is pending; the expanded Spanish outline is available in the linked source.

**Reading D40.** Extends D35 with a domain-wide vocabulary spanning computing, operating systems, networks, development, cloud, security, cryptography, identity, SecOps, GRC, privacy, threats, AI, quantum, careers and innovation. Stable English terms are included in the Spanish edition so learners can search primary documentation without translation ambiguity.
