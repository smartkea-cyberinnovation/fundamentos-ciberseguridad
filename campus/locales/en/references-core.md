# D01 · A reproducible and safe laboratory

## Architecture

Separate administration, practice systems and log analysis into three logical zones. Use internal or host-only networks for exercises. Temporary NAT may be used for approved software updates. Bridged networking to a shared home, work or classroom network is not the default. Host-only networking does not by itself protect the host: inspect its services and firewall too.

Define every approved flow by source, destination, protocol, port, purpose and owner. Only assigned systems may be contacted. Documentation addresses and `.test` names are examples, not targets. Do not accept unsolicited Internet traffic into the practice environment.

## Resources and platform coverage

Planning estimates, not vendor minimums: 16 GB RAM, four cores and 120 GB free storage can support sequential VM use; 32 GB/eight cores/250 GB supports several light guests; 64 GB and additional storage supports concurrent infrastructure. Reserve resources for the host and measure actual use. ARM/x86 and nested virtualization affect image compatibility.

Use a supported Debian/Ubuntu-family Linux VM and optionally an RPM-family VM for comparison. Record distribution, kernel, architecture, Bash, systemd and packages. Do not mix different package/firewall managers indiscriminately.

Windows requires a supported native edition with the chosen features. Record build, architecture, updates and shell versions. Server roles and evaluation licenses have specific availability and expiry conditions.

macOS requires permitted hardware and licensing. Record OS and architecture. Offline artifacts support interpretation, but native administration remains unevaluated without a Mac. Do not redistribute proprietary installers or images.

Containers are useful for disposable processes and synthetic data, not substitutes for native boot, filesystem, directory or platform-security exercises. Record the actual host/guest/container layer and keep host administration interfaces outside student containers.

## Reproducibility

For each image record official source, version/edition/architecture, published integrity checks where available, resources, network, packages, audit settings, fictional accounts, baseline snapshot and tested restoration. Keep instructions and configuration rather than licensed media or secrets in Git.

Use standard learner accounts and separate approved administrative access. Lab passwords must not be personal passwords and must not appear in scripts, screenshots or commits.

## Acceptance before practical work

1. Draw the network and verify adapters and routes on hosts and guests.
2. Check that no unintended external forwarding or listener is present.
3. Test one predefined allowed and denied flow between assigned endpoints.
4. Verify clock settings and receipt of a harmless event in the collector.
5. Restore a disposable VM and confirm other systems remain unaffected.
6. Disable shared folders, clipboard, USB and host disks unless their use is approved and documented.

Maintain console recovery for identity, firewall and remote-access changes. Verify encryption recovery before enabling encryption. A snapshot is not an external backup or automatically preserved evidence.

## Data and the common exercise contract

Separate local input, working, output, evidence and notes directories. Preserve original data. Use synthetic files, accounts and events. Real authorized evidence belongs in protected storage outside the public repository.

Every exercise defines objective, scope, versioned environment, ordered tasks, expected result, independent check, evidence and recovery. Ordinary A/B/C exercises take three hours each; M31 uses four hours and M32 ten. Seeded faults are benign configuration mistakes, such as a wrong path, stopped service or insufficient permission.

Stop when real data appears unexpectedly, another system is affected, scope becomes uncertain, exposure occurs or recovery is lost. Record observations and ask the instructor. State platform limitations honestly rather than presenting a simulation as native validation.

# D02 · Equivalent tasks across Linux, Windows and macOS

## Task equivalence is not syntax equivalence

Each utility retains its own arguments, permissions, format and side effects. Consult installed help. PowerShell pipelines carry objects between cmdlets; Unix pipelines generally carry bytes or text. A displayed table is not the original data object.

| Task | Linux | Windows | macOS |
|---|---|---|---|
| OS/version | `/etc/os-release`, `uname` | `Get-ComputerInfo`, `winver` | `sw_vers`, `uname` |
| Shell/motor | Bash version and current process | `$PSVersionTable`, `cmd /?` | zsh version and current process |
| Help | `man`, `info`, `--help` | `Get-Help`, `Get-Command`, `/?` | `man`, Terminal help |
| Resolve executable | `type`, `command -v` | `Get-Command`, `where.exe` | `type`, `command -v` |
| Current directory | `pwd` | `Get-Location`, `cd` | `pwd` |
| List/search files | `ls`, bounded `find` | `Get-ChildItem`, `dir` | `ls`, `find`, appropriate Spotlight queries |
| Read text | `less`, `cat`, `head`, `tail` | `Get-Content`, `type` | `less`, `cat`, `head`, `tail` |
| Copy/move | `cp`, `mv` | `Copy-Item`, `Move-Item`, `robocopy` | `cp`, `mv`, appropriate `ditto` |
| Search text | `grep`, `awk`, `sed` | `Select-String`, `findstr` | BSD `grep`, `awk`, `sed` |
| Compare data | `diff`, `cmp` | `Compare-Object`, `fc` | `diff`, `cmp` |
| Metadata | `stat`, `du`, `file` | `Get-Item`, file properties | `stat`, `du`, `file`, `ls -le@` |
| SHA-256 | `sha256sum` | `Get-FileHash -Algorithm SHA256` | `shasum -a 256` |
| Links | `ln`, `readlink` | links/reparse points, `Get-Item` | `ln`, `readlink`; Finder aliases differ |
| Identity/groups | `id`, `groups`, `getent` | `whoami`, LocalAccounts cmdlets | `id`, scoped `dscl` |
| Permissions | rwx and ACL tools | NTFS ACLs, `Get-Acl`, `icacls` | Unix permissions, ACLs and separate TCC |
| Privilege | groups and delegated sudo | access token, UAC and groups | groups/sudo and platform controls |
| Processes | `ps`, `top`, `pgrep` | `Get-Process`, `tasklist` | `ps`, `top`, Activity Monitor |
| Open resources | `lsof`, relevant `/proc` | approved handle/process inspection | `lsof`, subject to permissions |
| Services | `systemctl` on systemd | `Get-Service`, `sc.exe` | `launchctl`, Sharing settings |
| Scheduling | timers/cron | ScheduledTasks, `schtasks` | launchd |
| Software | distribution package manager | approved native/package tools | `softwareupdate`, approved managers |
| Storage | `lsblk`, `findmnt`, `df` | `Get-Disk`, `Get-Volume` | `diskutil`, `df`, Disk Utility |
| Volume encryption | chosen supported tool | BitLocker where supported | FileVault |
| IP/interfaces | `ip` | `Get-NetIPConfiguration`, `ipconfig` | `ifconfig`, `networksetup` |
| Routes | `ip route` | `Get-NetRoute`, `route print` | `route -n get default` |
| DNS | `getent hosts`, `resolvectl`, `dig` | `Resolve-DnsName`, `nslookup` | `scutil --dns`, installed DNS tools |
| Listeners | `ss` | `Get-NetTCPConnection`, `netstat` | `lsof -i`, native network tools |
| Firewall | existing nftables/ufw/firewalld | Windows Firewall profiles/rules | application firewall, separate PF |
| HTTP/TLS | `curl`, approved TLS queries | `curl.exe`, `Invoke-WebRequest` | installed `curl`/TLS tools |
| Remote session | SSH | approved RDP/WinRM/SSH | SSH or approved GUI sharing |
| Transfer | SFTP/SCP/rsync | available approved transfer clients | SFTP/SCP/rsync; check versions |
| Logs | journal/syslog/audit | Event Log, PowerShell, optional Sysmon | Unified Log, application logs |
| Configuration | files/environment/drop-ins | Registry/policies/files/environment | plist/profiles/preferences/environment |
| Backup | selected tool plus restore test | selected tool plus restore test | Time Machine/selected tool plus restore test |
| Structured data | appropriate parser, optional jq | objects and JSON/CSV/XML | appropriate parser, `plutil` |
| Automation | Bash, optional Python | PowerShell, BAT for legacy | zsh, declared Bash, optional Python |

Case sensitivity depends on the actual filesystem and configuration. Interactive shells, tasks and remote sessions may have different PATH/profile settings. GNU/BSD options and PowerShell encodings need explicit checks. Evaluate process identity through location, provenance and context rather than name alone.

# D03 · Terminal and verification quick reference

## Before working

Identify machine, account, current directory, OS/version, approved scope and intended effect. Read local help. For a change, preserve prior state and prepare recovery. A GUI action and a CLI action are both subject to system permissions.

## Linux and Bash

Quote paths, handle spaces and Unicode, distinguish literals/globs/regular expressions and check pipeline stages. Treat filenames as data. Validate arguments and constrain the operation's directory. Scheduled execution needs explicit paths/environment. Prefer filesystem-aware iteration rather than parsing a directory listing.

## Windows

Distinguish CMD, BAT, Windows PowerShell 5.1 and PowerShell 7. Prefer object properties to formatted-table parsing. Export data before formatting. Interpret return values according to the producing utility. Consider ACL inheritance and effective identity.

## macOS

Record architecture/version and interpreter. BSD tools may differ from GNU tools. Verify extended attributes/ACLs separately from content. Filesystem permissions, TCC and platform protection have different roles; use the narrowest approved access.

## Diagnosis and evidence

Follow relevant layers: symptom/scope, host/resources, identity/permissions, network/routes, DNS, transport, TLS, application/dependencies, logs and a testable hypothesis. Apply a small approved correction, verify and retain rollback. Do not run every possible command without a question.

For remote work, define destination/purpose, verify identity, limit access, use the approved channel, compare results, close and review records. For evidence, preserve originals, analyze copies and document transformations. Exact indicator matches require field semantics, validity and corroboration; no match is not a system-health guarantee.

## Automation and AI

Define inputs, outputs, effects, limits and error states. Use tests and peer review. AI may explain and propose, but execution remains an explicit human decision. Keep personal data and production records out of classroom examples.

# D04 · Evidence-based and reversible hardening

## Procedure

Discover assets, purpose, data, dependencies, users, services, ports and recovery. Select a baseline for the actual product/version; distinguish requirements, recommendations, inapplicable controls and unverified controls. Plan priority, impact, approval, copies, verification and rollback.

Apply changes on a clone first, in small batches. Do not alter identity, firewall and remote access together without a recovery console. Verify effective behavior with both a functional and a negative test. Review drift and exception expiry after updates.

## Common controls and evidence

| Control | Minimum evidence | Pitfall |
|---|---|---|
| Supported software and updates | Version, source, test record | Blind or untested updates |
| Software ownership | Package, version, origin, owner | Uncontrolled repositories |
| Separate standard/admin accounts | Membership and effective-access tests | Permanent elevation |
| Minimal service identities | Required resources and logs | Overprivileged shared accounts |
| Restricted remote access | Approved flows, identity and revocation | Unrestricted listeners/trust |
| Necessary ports/services | Listener, purpose and firewall | Assuming installed means required |
| Data/configuration permissions | ACLs and account-specific tests | General write access |
| Protected credentials | Custody mechanism, never secret values | Sensitive values in Git or logs |
| Encryption and recovery | Status and tested recovery procedure | Unrecoverable encrypted data |
| Audit and retention | Known event, collection/access policy | Missing or overexposed telemetry |
| Backup | Usable restore, measured time/loss | Untested backup files |
| Application provenance | Approved source and relevant verification | Removing safety controls |
| Time | Zone, source and observed drift | Incorrect chronology |
| Exceptions | Rationale, owner, compensation, expiry | Permanent undocumented exceptions |

## Platform-specific review

Linux: packages/repositories; service identities; groups and delegated privileges; configuration/executable ownership; ACL masks; listeners/firewall; SSH trust/revocation; enabled platform controls; timers/cron/units; suitable unit restrictions; mounts, logs and encryption. Avoid universal configuration scripts. An automated score does not establish full baseline compliance.

Windows: edition/build/updates; local groups/inactive accounts/delegation; UAC and supported credential protection; scoped domain policy; NTFS/shares; service accounts/tasks; endpoint protection/firewall; remote channels; auditing and recovery. Treat PowerShell logging as potentially sensitive data requiring permissions and retention.

macOS: updates/hardware; administrative membership; FileVault/recovery; boot/integrity; application provenance; privacy permissions; approved management profiles; startup/launchd; Sharing/network controls; logs and restored backups. Distinguish centrally managed policy from a local preference.

Web/containers: dedicated identities, minimum document root, configuration validation, correct TLS, protected private keys, bounded requests/logs, explicit persistence, meaningful health checks and maintained images. Consider non-root operation, read-only filesystems and resource limits where compatible. Inspect orchestration networking and storage separately from local Compose behavior.

## Acceptance

A control is verified only with effective-state evidence and tests. Configured-but-unverified remains a separate status. Record residual risk, untested areas, owner and expiry of every exception. This course checklist is not a compliance certificate.

# D05 · Competencies, evidence and professional roles

## Interpretation

This is a pedagogical role mapping, not an official qualification. Level 1: understand and interpret; 2: perform with guidance; 3: perform, verify and explain independently in the lab. Red/Purple denotes approved review and control validation.

| Competency | SysAdmin | Blue/SOC | DFIR | Red/Purple | CTI |
|---|---:|---:|---:|---:|---:|
| OS architecture/resources | 3 | 2 | 3 | 3 | 1 |
| Terminal/documentation | 3 | 3 | 3 | 3 | 3 |
| Files/metadata/hashes | 3 | 3 | 3 | 3 | 2 |
| Text/search/data | 3 | 3 | 3 | 3 | 3 |
| Linux identity/permissions | 3 | 3 | 3 | 3 | 1 |
| Processes/services | 3 | 3 | 3 | 3 | 1 |
| Storage/recovery | 3 | 2 | 3 | 2 | 1 |
| Host networking | 3 | 3 | 2 | 3 | 2 |
| Bash | 3 | 3 | 2 | 3 | 3 |
| CMD/BAT | 2 | 2 | 2 | 2 | 1 |
| PowerShell/objects | 3 | 3 | 3 | 3 | 3 |
| Native Windows/directory | 3 | 3 | 3 | 3 | 1 |
| macOS/zsh | 3 | 2 | 3 | 2 | 1 |
| Remote administration | 3 | 3 | 2 | 3 | 1 |
| Segmentation/trust | 3 | 3 | 2 | 3 | 2 |
| Web/TLS | 3 | 3 | 2 | 3 | 2 |
| Cross-platform automation | 3 | 3 | 2 | 2 | 3 |
| Containers/orchestration basics | 2 | 2 | 1 | 2 | 1 |
| Baselines/exceptions | 3 | 3 | 2 | 3 | 1 |
| Time correlation | 2 | 3 | 3 | 3 | 3 |
| Preservation/triage | 2 | 3 | 3 | 2 | 2 |
| Indicators/hunting | 2 | 3 | 3 | 3 | 3 |
| Control validation | 3 | 3 | 2 | 3 | 2 |
| Supervised AI | 3 | 3 | 3 | 3 | 3 |
| Communication/limitations | 3 | 3 | 3 | 3 | 3 |

## Measurable outcomes

Understand an observation using OS concepts and an alternative hypothesis. Operate a scoped GUI/CLI task with a reproducible runbook. Automate with validated inputs, outputs and errors. Protect using a proportional change with positive/negative checks and rollback. Investigate through preserved inputs, bounded searches and contextual timelines. Communicate impact, priority and next action with independent verification of AI contributions.

## Portfolio

SysAdmin: inventory, service and restore. Blue/SOC: detection/query with coverage and false-positive tests. DFIR: preserved case and timeline. Red/Purple: approved scope, trust review, benign test and retest. CTI: indicators with provenance, confidence, validity and a decision-oriented recommendation. Use fictional data and review artifacts before publication. Completing a foundational course does not establish advanced mastery of an entire profession.

# D06 · Assessment, remediation and internal recognition

## Assessment model

The entry diagnostic is ungraded. Proposed weights: labs 40%, individual practical checks 20%, applied theory 10%, capstone 25%, notebook and professional review 5%. Avoid awarding the same artifact twice for the same criterion. Each route's required exercises are completed or receive a documented adaptation.

| Lab dimension | Weight | Competent evidence |
|---|---:|---|
| Understanding/planning | 15% | Objective, scope, system, permissions |
| Technical execution | 30% | Correct independently checked result |
| Security/privacy | 20% | Least privilege, synthetic data, scope |
| Evidence/reproducibility | 20% | Versions, steps, outcomes and errors |
| Recovery/reflection | 15% | Verified recovery and limits |

For each dimension use 0–4: absent; substantially incomplete; correct with guidance; independent/verified; or additionally demonstrates boundary cases and alternatives. Sum weight × level/4.

## Individual checkpoints

C1 after M04: help, navigation and documented Git change. C2 after M12: Linux service diagnosis and a script with invalid-path/permission tests. C3 after M19: native Windows, objects, ACLs and provider-scoped events. C4 after M23: native macOS, shell differences, controls and log limitations. C5 after M30: preservation, timeline, exact indicator matching, alternatives and retest. C6: integrated explanation, small new change and restoration.

Manuals are allowed; the learner must explain and adapt the solution rather than delegate all work to another person or AI.

## Passing and remediation

The proposed full-course threshold is 70/100 overall, passed checkpoints, at least 70/100 on the capstone and no unresolved critical condition. These are internal teaching proposals, not external academic rules. Declare missing native-platform assessment explicitly.

Critical conditions include staying within scope, protecting student data and original evidence, maintaining recovery and recording actual rather than invented outcomes. Stop and remediate a failed critical condition before approval regardless of the arithmetic score.

Assign an equivalent task with different data to recover a missing competency. Require analysis of the original mistake, a repeatable check and a recorded assessment. Team roles rotate; commit counts and code volume do not prove individual understanding.

## AI and recognition

Declare tool/model, input categories, accepted output and independent tests. The instructor may ask for the same explanation without AI. An internal completion record identifies route, actual completed hours, natively assessed systems, demonstrated outcomes, date and responsible instructor. Local campus checkboxes do not issue an official certificate or measure study time.

# D07 · Work and evidence templates

## Environment sheet

Lab asset/image ID; OS/edition/version/architecture/patch; execution layer/resources; shell/motor/modules; fictional account and permitted rights; network/routes/approved flows; clock/zone/synchronization; log sources/retention; snapshot/backup and restore test; provenance/license; limitations.

## Lab submission

Exercise ID, learner/team and edition; objective/criteria; scope/assets/actions; preparation/permissions; ordered steps and explained commands; expected/observed results; errors and hypotheses; evidence names/origin/time/integrity checks; positive/negative tests; recovery; AI use and independent verification; limits and next improvement.

## Change or exception

ID/objective/owner; affected asset/service; observed state/evidence; desired state/reference; dependencies/impact/risk; approval/window; implementation; functional/restriction tests; prior copy/rollback; observed result/residual risk; exception, compensating control and expiration.

## Evidence manifest and custody

Record each item's ID, logical name/path, origin, size/format, hash algorithm/value, original time/zone, reception time, tool/version, operator, access controls, original/working-copy location and related items. Every custody transfer records who, when, purpose, item and integrity verification. This template does not guarantee legal admissibility.

## Timeline

| Original time | Zone | Normalized time | Host/source | Action | Fictional account | Evidence | Confidence/limits |
|---|---|---|---|---|---|---|---|

Retain original text, precision and any clock adjustment. Do not overwrite source timestamps.

## Indicator and search hypothesis

Type/original/normalized value; hash algorithm where relevant; source/received time/expiry; confidence/context; question; dataset/field/interval/coverage; exact/subdomain/pattern semantics; query/version; positive/negative controls; findings/corroboration; false positives/omissions; proposed action/reviewer.

## Script contract

Purpose/non-goals; interpreter/version; privileges; input types/limits; output/schema; exit codes; effects/files/network; sensitive-data handling; query/dry-run modes; timeout/concurrency; partial failures; temporary files; tests; rollback; dependencies/license/owner.

## AI record

Tool/model/version; local/remote mode; date/purpose; input categories/minimization; effective permissions; sanitized prompt; accepted/rejected output; independent tests; reviewer; measured cost/latency where available; retention/deletion.

## Finding and recovery

A finding records observed condition, evidence, possible consequence, alternatives, control reference, justified priority, correction/owner/date, success criteria, retest and limitations. Do not confuse plausible impact with observed impact.

A restoration record identifies service/data, recovery point, selected backup/integrity, protected recovery method, destination, steps, duration/loss, permissions, functional tests, differences and achieved versus target RPO/RTO. Store real authorized evidence outside the public repository.

# D08 · Primary sources and version control

## Source scope

The original curriculum's documentation review is dated 14 September 2026. This English teaching edition localizes that material; it is not a new vendor certification. Check installed versions and current official manuals before each cohort. A documented lab and an executed lab have different validation states.

| ID | Official reference | Purpose |
|---|---|---|
| S01 | [GNU Bash](https://www.gnu.org/software/bash/manual/bash.html) | Syntax, expansion and scripting |
| S02 | [systemd](https://systemd.io/) | Services, units, timers and journal |
| S03 | [Windows commands](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) | Native commands and batch files |
| S04 | [PowerShell 101](https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/01-getting-started) | Objects, engines and scripts |
| S05 | [Remoting requirements](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_requirements) | Transport and native prerequisites |
| S06 | [Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) | Configurable event collection |
| S07 | [Apple Platform Security](https://support.apple.com/guide/security/welcome/web) | Native integrity and protection |
| S08 | [OpenSSH manual](https://man.openbsd.org/ssh) | Remote identity and administration |
| S09 | [Docker Swarm](https://docs.docker.com/engine/swarm/) | Distributed service concepts |
| S10 | [NICE updates](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/about/nice-framework-latest-updates) | Tasks, knowledge and skills |
| S11 | [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Incident response and risk |
| S12 | [MITRE ATT&CK](https://attack.mitre.org/) | Behavior and detection vocabulary |
| S13 | [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) | Version-specific baselines |
| S14 | [Ollama CLI](https://docs.ollama.com/cli) | Optional local-model workflow |

## What must be verified locally

An online Bash manual does not establish the installed version; Bash and zsh are not interchangeable. PowerShell 5.1/7, remoting transport and available native modules differ. Apple controls depend on version/hardware. Role mappings are pedagogical rather than an exhaustive mapping of official identifiers. Select benchmarks and licenses for the actual product rather than assuming checklist completion establishes conformity.

Consult `man`, `info`, installed help and the actual distribution/vendor documentation. Add official manuals for Coreutils, text tools, zsh, the selected hypervisor, web server, orchestration, backup and log collector when teaching those units.

## Maintenance

Record product/version/architecture, official source, consultation date, support/license, verification commands, changes and affected modules. Review before each cohort and after material updates. Use explicit states: designed, documentation-reviewed, tested on an identified environment, approved for a cohort, blocked or retired. Updating a document date does not change its validation state.

# D09 · First session and practical entry point

## Prepare a small workspace

Read the laboratory rules and identify account, machine and working directory. Use a new disposable directory, not a personal document folder. The reference Python kit creates synthetic files without administrative privilege. A teacher may provide the dataset when a phone or tablet is used for reading.

From `formacion/sistemas-operativos/`:

```bash
python3 kit/oslab.py init mi-laboratorio
python3 kit/oslab.py manifest mi-laboratorio
```

On Windows select the approved interpreter, such as `py -3`, if appropriate. Keep actual command arguments and filenames unchanged when switching language. Existing workspaces are not silently replaced.

## Observe and compare

Open `datos` in the file manager, show hidden files and compare terminal listings. The reference `oslab.py` dataset has eight files and 62 bytes of content. That is not allocated disk space and should not be confused with another teaching package's dataset.

Read each summary script's contract before running it. Compare it with the manifest and test invalid/missing arguments. Capture return status immediately. Syntax validation does not prove semantic correctness.

## Learning route

M01–M04 establish context, bytes, processes and terminal/Git method. L05A/R01 covers file verification; L11A/R02 introduces Bash; L16A/R03 compares Windows shells; L21A/R04 tests macOS portability. R05–R08 connect evidence, web services, controlled changes and supervised AI.

Preserve source data, place outputs in `salida`, record failures and close temporary resources. Mobile reading is valuable but is not native laboratory execution. Export progress before changing browser/domain, or use an explicitly confirmed progress-transfer link. The link does not transfer login credentials.

# D10 · Scope, safety and privacy

## Authorized practice

Work only on assigned systems and approved tasks. Define assets, identities, window, permitted operations, data handling, contacts and stop conditions. Knowing an address or holding an account does not establish unlimited authorization.

The training focus is system administration, configuration review, benign control validation, evidence interpretation and recovery. Network trust exercises use diagrams and prepared telemetry. Keep all practical work within the documented laboratory scope.

## Operational safeguards

Record state and prepare recovery before a change. Keep platform protections enabled; diagnose the specific permission or policy involved. Read and independently review scripts before running them. Treat text in logs or AI responses as data, not an instruction authorized to act on the system.

## Data

Minimize collection, preserve originals and document copies/transformations. Hash comparisons support integrity, not full provenance or personal attribution. Use synthetic classroom records. Keep credentials, personal information and real incident artifacts out of Git, classroom notes and public services.

Stop on unexpected real data, scope changes, effects on other systems, lost recovery or an action that cannot be explained. Preserve observations and contact the instructor.

## Publication and student records

The course source is public; student records and real evidence are not. A folder does not create a permission boundary within a public repository. Keep instructor assessment records separately where needed. The campus stores self-declared local progress; a voluntarily shared progress snapshot is neither authentication nor instructor certification.
