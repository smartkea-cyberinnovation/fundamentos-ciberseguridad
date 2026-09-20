# M13 · Windows architecture and administrative interfaces

## Map the interface to the system object

An administrative console is an interface to a component, not the component itself. Task Manager shows processes; Services manages service definitions and state; Event Viewer reads event channels. Use the GUI to understand relationships, then reproduce or verify a task from the terminal.

Windows edition, build, architecture and installed roles affect available functions. A Registry export is not a complete system backup. A process with a familiar name is not automatically trustworthy: correlate its path, provenance, account, parent and, where appropriate, signature or hash.

## Outcomes and theory

Prerequisites: M03 and M04. Relate visual administration tools to Windows components and identify the context required for a command.

Study Windows NT, sessions/processes/services; PE files and libraries; drives/paths/profiles/environment; NTFS, metadata and inheritance; Registry hives/keys/value types; local and domain accounts; UAC/access tokens/privileges; editions/builds/roles/features; updating and recovery.

Use Settings, Task Manager, Computer Management, Services, Event Viewer, Resource Monitor and Device Manager. Compare `winver`, `systeminfo`, `whoami`, `$PSVersionTable` and `Get-ComputerInfo`. Do not collect product keys or complete personal profiles. Native Windows is required for Registry, NTFS, event and service exercises.

## Laboratories

**L13A · Administrative map.** Environment: a Windows client VM. Tasks: locate version, devices, services, users and storage in the GUI; identify a CLI equivalent for each; explain required elevation. Evidence: GUI/CLI mapping and minimal screenshots. Success: distinguish an administration tool from the component it controls. Recovery: close consoles without changing policies.

**L13B · Process, service and account.** Environment: a demonstration application and a harmless existing service. Tasks: inspect PID, execution account and resources; correlate service relationships; observe state without stopping critical components. Evidence: relationship table. Success: do not infer trust solely from the executable name. Recovery: close only the learner's application.

**L13C · Configuration and the Registry.** Environment: a synthetic export of an application's Registry key. Tasks: interpret value types; compare versions; identify user/machine scope; write a change and rollback plan without applying it to system keys. Evidence: diff and rationale. Success: explain why a partial export is not a complete Windows backup. Recovery: preserve the original export.

## Demonstrate understanding

Identify the exact OS and execution context before using administrative instructions. Do not assume every Windows edition supports the same roles or policies.

# M14 · CMD and native Windows utilities

## Use the shell you actually opened

`cmd.exe`, Windows PowerShell and PowerShell 7 are distinct command environments. Similar command names may resolve to built-ins, aliases or executables with different behavior. Use explicit executable names, such as `sc.exe`, when necessary to remove ambiguity.

CMD pipelines generally carry text. Localized output, encoding and unusual filenames can make text parsing brittle. Exit-code interpretation belongs to the producing utility: not every nonzero result means the same thing. Preview copy operations and understand options that can remove destination files.

## Outcomes and theory

Prerequisite: M13. Navigate and inspect Windows through CMD while respecting its own syntax and limitations.

Study internal/external commands, help and PATH; drive/current-directory behavior; `%VAR%`; quoted paths; text redirection/pipes; searching; file attributes; exit codes; bounded administrative queries; console localization and encoding.

Use `help`, `where.exe`, `cd /d`, `dir`, `type`, `more`, `findstr`, `fc`, `copy`, `move`, `mkdir`, `attrib`, `set`, `whoami`, `tasklist`, `ipconfig`, `route print`, `netstat`, `sc.exe query`, `schtasks /query` and `robocopy`. Use listing/preview modes before actual copying. Do not apply GNU options to Windows utilities by analogy.

## Laboratories

**L14A · Navigation and search.** Environment: learner-owned paths with spaces and two available drives. Tasks: change drive/directory; locate file types; inspect attributes/content; compare two versions. Evidence: sanitized transcript and outputs. Success: handle quoted paths correctly and explain `cd /d`. Recovery: do not change original files.

**L14B · CMD inventory.** Environment: native Windows and a standard account. Tasks: collect selected identity, process, service and network fields; separate outputs; document permission and localization limits. Evidence: a report without credentials or entire profiles. Success: do not treat access denied as proof an object does not exist. Recovery: protect or remove outputs according to course retention.

**L14C · Controlled copy.** Environment: practice source and destination folders. Tasks: preview the transfer; identify preserved properties; copy synthetic data; interpret documented return codes; compare results. Evidence: plan, log and differences. Success: distinguish change, warning and error using the utility's semantics. Recovery: remove only the trial destination.

## Demonstrate understanding

Explain the interpreter, executable, encoding and return code behind an operation. Avoid mirror/delete options until their effects are understood and reversible.

# M15 · BAT and legacy automation

## Maintain and migrate deliberately

Batch files remain useful for understanding existing Windows operations, but they are not the best answer to every automation problem. Immediate and delayed expansion can produce surprising results inside blocks. Enabling delayed expansion can also alter valid filenames containing exclamation marks.

Before migration, state the script's input/output and error contract. Preserve intended behavior, not accidental quirks. A PowerShell rewrite should use objects where appropriate rather than reproducing brittle parsing line for line. The initial migration demonstration is revisited independently after PowerShell fundamentals in M16.

## Outcomes and theory

Prerequisites: M14 and M11. Read and maintain small batch scripts, identify their limitations and justify migration.

Study `.bat`/`.cmd`, `@echo off`, parameters and path modifiers, `setlocal/endlocal`, safe assignments, immediate/delayed expansion, `if`, `for`, `call`, labels/subroutines, `errorlevel`, redirection, metacharacters, Unicode and parsing limits.

Use `cmd.exe`, an editor and native batch control structures. Do not concatenate untrusted input into commands or place secrets in batch files. Turning echo off does not remove information from OS auditing.

## Laboratories

**L15A · Directory batch script.** Environment: synthetic files. Tasks: accept a directory; validate it; list files; provide usage help and meaningful exit status; test missing arguments and spaces. Evidence: script and test matrix. Success: input is not executed as code and source data is not modified. Recovery: remove only generated reports.

**L15B · Understand expansion.** Environment: an instructional batch loop with variables. Tasks: predict output; compare parse-time and delayed expansion; test exclamation marks; correct data loss. Evidence: explanation and observed outputs. Success: recognize when a safer solution requires another language. Recovery: retain revisions in Git.

**L15C · Justified migration.** Environment: the learner's own batch script and an instructor-led PowerShell demonstration. Tasks: specify the contract; express the task using objects; compare output, errors and maintenance; revisit the implementation independently after M16. Evidence: comparison and reusable tests. Success: preserve functional behavior while explaining which dependencies on localized text disappear. Recovery: retain the original as reference, not as an active scheduled task.

## Demonstrate understanding

Explain when `errorlevel` is checked and when variables expand. Choose a language from requirements, not familiarity alone.

# M16 · PowerShell objects, language and structured data

## Objects are not their printed tables

A cmdlet can emit typed objects with properties and methods. Inspect them with `Get-Member`, select the required properties, then export the data. `Format-Table` belongs at the presentation boundary: formatting objects before CSV/JSON export changes what is being exported.

Windows PowerShell 5.1 and PowerShell 7 differ in available modules, encodings and native-process behavior. PowerShell on Linux does not include Windows administrative APIs. Distinguish terminating/nonterminating errors and native exit codes. Execution policy is not a security boundary that makes arbitrary scripts safe.

## Outcomes and theory

Prerequisites: M13 and M15. Build object pipelines and functions with explicit parameters, validation, errors and structured output.

Study engines/modules/help; verb-noun cmdlets; types/properties/methods; pipelines/filtering/selection; arrays/hashtables/`PSCustomObject`; functions/parameters/validation; control flow/providers; error handling/exceptions; JSON/CSV/XML; depth/encoding/dates; native programs and `$LASTEXITCODE`.

Use `Get-Help`, `Get-Command`, `Get-Member`, `Select-Object`, `Where-Object`, `Sort-Object`, `Group-Object`, `Measure-Object`, `ForEach-Object`, `Import-Csv`, `Export-Csv`, `ConvertFrom-Json`, `ConvertTo-Json`, `Test-Path` and `Join-Path`. Keep data separate from messages intended for humans.

## Laboratories

**L16A · Text versus objects.** Environment: synthetic data and permitted process queries. Tasks: inspect types/properties; filter/group; export CSV/JSON; verify fields; compare display formatting with underlying values. Evidence: pipeline and serialized outputs. Success: use properties instead of parsing a visual table. Recovery: retain only sanitized results.

**L16B · A safe function.** Environment: course files. Tasks: create a function accepting a path; validate it; inspect regular-file properties and SHA-256; handle exceptions; emit objects rather than mixed messages. Evidence: help and tests for empty, invalid and spaced paths. Success: explicit failure and machine-readable output. Recovery: read input files only.

**L16C · Data regression tests.** Environment: CSV and JSON with missing fields. Tasks: validate the agreed schema; preserve types as far as the format allows; test JSON depth, Unicode and dates; compare available engines. Evidence: tests and compatibility matrix. Success: document actual differences instead of claiming universal portability. Recovery: preserve original inputs.

## Demonstrate understanding

Explain object/data/format boundaries and errors from native programs. Never disable policy globally merely to make a classroom script run.

# M17 · Administer Windows with PowerShell

## Change the minimum necessary state

An inventory should collect fields that answer an operational question, not everything an API can return. Permission failures belong in the result and must not silently become negative findings. For a change, compare intended and effective permissions and verify the application still works.

`-WhatIf` is available only when implemented and is not a rollback mechanism. Preserve prior state and test restoration separately. A scheduled task needs an explicit account, working directory, trigger and log location; a service also has dependencies that must be considered before changing it.

## Outcomes and theory

Prerequisite: M16. Inventory Windows and make small, reversible changes with independent verification.

Study processes/services/dependencies; CIM/WMI queries; filesystem and Registry providers; NTFS/ACLs/SIDs/inheritance; scheduled tasks; package/update provenance; local accounts; effective policies; performance; `ShouldProcess`/`WhatIf`; transcription and error handling.

Use `Get-Process`, `Get-Service`, `Get-CimInstance`, `Get-ItemProperty`, `Get-Acl`, `Get-LocalUser`, `Get-LocalGroupMember`, `Get-ScheduledTask` and `Get-WinEvent`. Availability depends on Windows, architecture and modules. Do not require the removed `Get-WmiObject` cmdlet in PowerShell 7.

## Laboratories

**L17A · Normalized inventory.** Environment: a Windows VM. Tasks: select relevant system/service fields; export objects with time and source; handle access denied; compare GUI observations. Evidence: sanitized inventory and field contract. Success: avoid whole Registry or profile exports. Recovery: protect the output files.

**L17B · Effective permissions.** Environment: a fictional application folder and two practice accounts. Tasks: define expected access; inspect ACLs/inheritance; test effective permissions; plan and apply a minimal approved correction. Evidence: before/after state and a denied-access test. Success: avoid general full-control grants. Recovery: restore the original ACL and verify it.

**L17C · An auditable scheduled task.** Environment: a harmless task writing a summary to a dedicated directory. Tasks: declare identity, directory and trigger; run manually; schedule; observe logs and a controlled failure; compare GUI/CLI. Evidence: definition, results and removal procedure. Success: operation without unnecessary administrative privilege. Recovery: remove only the exercise task.

## Demonstrate understanding

Distinguish preview, implementation and rollback. Explain the identity and dependencies of a task or service before changing it.

# M18 · Windows identity, networking and remote administration

## Transport, identity and authorization

Encryption protects a communication channel, but does not authorize every action at its destination. A remote administrative workflow needs a trusted endpoint, verified identity, explicitly delegated permissions and an audit trail. Restrict listeners and sources; do not expose RDP or WinRM to the Internet to simplify a lab.

Local accounts, domain identities and policy application have different scopes. DNS, Kerberos and directory services interact, but a working network connection does not prove successful authentication. A delegated endpoint should reject actions outside its role; that rejection can be the correct result.

## Outcomes and theory

Prerequisites: M10 and M17. Operate an approved remote session and explain its network, trust and identity dependencies.

Study SIDs/groups/tokens; local versus domain accounts; AD DS, DNS, LDAP and Kerberos concepts; GPO scope; MFA and credential protection; firewall profiles; RDP transport; WinRM/PowerShell Remoting; SSH where supported; JEA constrained delegation; temporary access and session auditing.

Use `Get-NetIPConfiguration`, `Get-NetRoute`, `Get-NetTCPConnection`, `Resolve-DnsName`, `Test-NetConnection`, `Get-NetFirewallProfile`, `Get-NetFirewallRule`, `gpresult`, `Enter-PSSession` and `Invoke-Command` only against prepared endpoints. Do not introduce global TrustedHosts wildcards or unrestricted listeners.

## Laboratories

**L18A · Windows network diagnosis.** Environment: Windows and an assigned server. Tasks: inspect DNS/routes/ports; test the service by approved name and address; separate resolution from authorization. Evidence: diagnostic sequence. Success: identify what traffic each check sends and where. Recovery: restore only changed practice parameters.

**L18B · A delegated session.** Environment: an instructor-prepared endpoint and a limited account. Tasks: verify destination/authentication; perform an allowed query; confirm a disallowed operation is rejected; close the session; review records. Evidence: authorization/result matrix. Success: do not widen rights to defeat the intended restriction. Recovery: revoke temporary access.

**L18C · Directory and policy.** Environment: an optional isolated domain, or explicitly labeled synthetic exports. Tasks: map user/group/computer/GPO relationships; explain inheritance and DNS; analyze an applied policy; propose delegation. Evidence: architecture map and diagnosis. Success: distinguish native administration from offline interpretation. Recovery: make no directory changes outside the assigned practice organizational unit.

## Demonstrate understanding

Explain the difference between secure transport, authenticated identity and authorized action.

# M19 · Windows events, protection and recovery

## Events require collection context

An event number has meaning within its provider and channel. Audit policy, collector configuration, permissions and retention determine what can be observed. Missing events do not prove missing activity. Sysmon is an additional source with configurable coverage, not an all-seeing default feature.

Baseline reviews must protect availability and recovery as well as confidentiality. Verify updates, endpoint protection, firewall, accounts, logging and encryption. Never export recovery secrets into Git. Restoring business data and preserving incident evidence are related but different procedures.

## Outcomes and theory

Prerequisites: M17 and M18. Evaluate a Windows baseline, query scoped events and demonstrate recovery without disabling essential protections.

Study channels/providers/Event IDs and audit policy; Security/System/Application; PowerShell logging; optional Sysmon; Defender/firewall; BitLocker recovery; updates/exposure reduction; application control as an extension; backup/restoration/evidence; log permissions and retention.

Use Windows Security, Event Viewer and recovery settings, `Get-WinEvent`, `wevtutil qe/epl`, `auditpol /get`, appropriate `Get-MpComputerStatus`, BitLocker status and firewall queries. Do not publish recovery protectors or collect full profiles.

## Laboratories

**L19A · Contextual event analysis.** Environment: exports or a VM with known audit configuration. Tasks: select provider/channel/interval; locate a benign instructor-generated event; correlate account/time; explain expected collection gaps. Evidence: query and coverage sheet. Success: identify an event with its provider, not its number alone. Recovery: preserve the original export.

**L19B · A reasoned baseline.** Environment: a Windows clone. Tasks: review updates, accounts, services, firewall, encryption, logging and protection; prioritize five findings; correct one approved deviation; test functionality. Evidence: checklist and documented exceptions. Success: retain protection and administrative recovery access. Recovery: demonstrate rollback for the change.

**L19C · Recovery and evidence.** Environment: fictional documents and a backup. Tasks: preserve the initial case state; restore to another path; compare hashes, permissions and application opening; document what is not preserved. Evidence: a recovery record and test results. Success: distinguish operational restoration from forensic preservation. Recovery: return to the practice snapshot after evidence collection.

## Checkpoint C3

Administer native Windows, justify PowerShell versus BAT, verify access and interpret events within collection limits.

# M20 · macOS, Darwin, APFS and everyday operation

## Unix foundations, Apple-specific behavior

macOS has Unix foundations but is not a Linux distribution. Darwin/XNU, Apple frameworks, application bundles and platform security introduce their own behavior. Utilities may be BSD variants rather than GNU versions; similar command names do not guarantee identical options.

An APFS container, volume and physical disk are different layers. Copy-on-write and snapshots affect allocation. File content, ACLs and extended attributes require separate checks: a matching content hash does not verify every property. Finder aliases and symbolic links also have different semantics.

## Outcomes and theory

Prerequisites: M03 and M05. Explain macOS organization and operate through Finder and Terminal while respecting architecture and version differences.

Study Darwin/XNU; Intel/Apple Silicon; boot/recovery/system volumes; APFS containers/volumes/snapshots/case sensitivity; `/Applications`, `/System`, `/Library`, `~/Library`, `/Users`, `/Volumes`; application bundles; metadata, links and extended attributes.

Use Finder, System Settings, Disk Utility and Activity Monitor; `sw_vers`, `uname`, scoped `system_profiler`, `diskutil list`, `df`, `du`, `stat`, `file`, `ls -le@`, read-only `xattr` and `open`. Do not modify protected system volumes or remove quarantine attributes to run course software. Native Apple hardware/licensing requirements remain applicable.

## Laboratories

**L20A · Map the Mac.** Environment: a lab Mac and standard user. Tasks: identify OS/architecture; locate an application, system-wide settings and user settings; compare Finder/Terminal; inspect a bundle without modifying it. Evidence: paths/functions map. Success: distinguish global and personal directories. Recovery: query only.

**L20B · Metadata and copying.** Environment: synthetic documents. Tasks: inspect permissions, ACLs and attributes; copy using different methods; compare content and metadata; explain discrepancies. Evidence: preservation matrix. Success: do not equate a content hash with complete metadata preservation. Recovery: retain original files.

**L20C · Volumes and free space.** Environment: disk queries and a prepared practice volume. Tasks: map disk/container/volume; compare apparent allocation; interpret snapshots and COW using observations. Evidence: diagram and two limitations. Success: do not treat all volumes as independent partitions. Recovery: do not unmount or modify the boot volume.

## Demonstrate understanding

Identify what is shared with Unix and what is Apple-specific. Hidden, protected and encrypted are not synonymous.

# M21 · zsh, files and macOS automation

## Declare and test portability

A script's interpreter is part of its contract. Bash and zsh differ in expansion, arrays and options; noninteractive execution may not read the same initialization files as a login shell. The Bash included with a Mac may lack features from a recent GNU/Linux installation.

Separate shell syntax from the options of external commands. A plist can be syntactically valid without representing a meaningful or active configuration. Third-party package managers need their own provenance, permissions and maintenance review; do not use elevation to conceal a broken installation model.

## Outcomes and theory

Prerequisites: M11 and M20. Automate learner-owned tasks on macOS and identify relevant shell and BSD/GNU differences.

Study login/interactive/noninteractive shells; startup files; PATH; quoting/globbing/expansion; arrays/options; functions/arguments/errors; structured data; plist/preferences; software updates; Homebrew as a third-party ecosystem; explicit portability tests.

Use `zsh`, `man`, `command -v`, `type`, `printf`, `find`, `grep`, `sed`, `awk`, `shasum -a 256`, `plutil`, `defaults read` and `softwareupdate --list`. Use `brew list/info` only for an already approved installation. Do not assume all GNU options exist locally.

## Laboratories

**L21A · Port without assumptions.** Environment: a learner Bash script that only reads files. Tasks: record interpreter/version; run in the declared shell; adapt to zsh; test arrays, unmatched globs and external-command options. Evidence: compatibility matrix. Success: correct shebang and no untested universal portability claims. Recovery: preserve separate versions.

**L21B · Inspect plist data.** Environment: synthetic preference copies, not real profiles. Tasks: validate syntax; convert a copy for inspection; query keys; compare revisions; distinguish stored configuration from effective state. Evidence: expected/missing-key report. Success: do not modify real preferences or equate a persisted value with active behavior. Recovery: preserve source files.

**L21C · zsh directory inventory.** Environment: filenames with spaces and Unicode. Tasks: accept/validate a directory; generate names, sizes and hashes; handle errors; record tool versions. Evidence: script and tests for invalid/empty paths. Success: do not follow links outside scope without an explicit decision. Recovery: remove only generated trial outputs.

## Demonstrate understanding

Explain whether an incompatibility belongs to the shell, utility, filesystem, architecture or permissions.

# M22 · macOS identities, launchd, services and networking

## Match the task to its execution domain

A LaunchAgent runs in a user-related context; a LaunchDaemon serves a different lifecycle and privilege model. The correct domain, account, absolute paths and environment matter as much as the executable. A successful manual run does not establish correct scheduled behavior.

File permissions, ACLs and privacy permissions can all affect access. Full Disk Access is not a universal fix. Network services, interfaces, DNS and packet-filtering layers also differ from Linux. Inspect the controls actually enabled on the assigned Mac.

## Outcomes and theory

Prerequisites: M10 and M21. Diagnose execution/connectivity and configure a legitimate, auditable task in the appropriate scope.

Study users/groups/elevation; Unix permissions, ACLs and TCC; LaunchAgents/LaunchDaemons; launchd domains/session/identity; service plist files; paths/environment; sharing/remote access; per-service networking/DNS; application firewall versus packet filtering; reversible configuration.

Use Users & Groups, Sharing, Login Items and network settings; `id`, scoped `dscl`, `launchctl print`, `plutil`, `ps`, `lsof -i`, `networksetup -listallnetworkservices`, `scutil --dns`, `route -n get default` and `ifconfig`. SSH requires a prepared, limited endpoint. Check local documentation rather than copying obsolete launchd commands.

## Laboratories

**L22A · Identity and access.** Environment: two fictional users on a lab Mac. Tasks: define shared-folder access; inspect permissions/ACLs; verify reading/writing; distinguish filesystem permissions from TCC authorization. Evidence: matrix and tests. Success: no blanket Full Disk Access grant. Recovery: restore practice-directory permissions.

**L22B · Auditable user agent.** Environment: a learner account and a harmless summary script. Tasks: write and validate a plist; specify absolute paths; activate through the documented launchd mechanism; check output and logs. Evidence: task definition and verification. Success: user scope without concealment or unnecessary administrative rights. Recovery: deactivate and remove only the created agent using local help.

**L22C · Connectivity and sharing.** Environment: a Mac and an assigned server. Tasks: identify network service/interface; query DNS/routes; test the approved port/application; inspect Sharing; propose removal of unnecessary exposure without automatic changes. Evidence: diagnosis and change plan. Success: explain platform differences. Recovery: reverse only approved temporary settings.

## Demonstrate understanding

Identify the execution account and launchd domain before troubleshooting a task. Do not assume the interactive environment exists in scheduled execution.

# M23 · macOS protection, logging and evidence

## Respect platform boundaries

FileVault, recovery mechanisms, system integrity, boot protections, application provenance and privacy permissions have distinct roles. Their availability depends on hardware and OS version. A status query is not proof that every related control has been tested.

Unified Log may redact fields, restrict access or retain events for a limited period. Shell history is useful context, not a complete or authoritative activity record. Minimize collection and never extract Keychain secrets as an inventory exercise. Preserve original data before attempting recovery.

## Outcomes and theory

Prerequisites: M19 and M22. Audit macOS controls and collect proportionate evidence without weakening platform protections.

Study FileVault/recovery; SIP/signed system volume/boot; Gatekeeper/notarization/XProtect; signing/provenance; TCC; Keychain as a secret store, without extraction; updates/sharing; Unified Log/retention; history and execution artifacts with limitations; Time Machine/restoration.

Use Privacy & Security, FileVault and Console; `fdesetup status`, `csrutil status`, supported `spctl --status`, read-only `codesign` inspection of approved apps, bounded `log show`, scoped `log stream` and read-only `tmutil`. Check local capabilities. Do not disable SIP/Gatekeeper or strip quarantine attributes.

## Laboratories

**L23A · Mac baseline.** Environment: the assigned Mac. Tasks: inspect updates, encryption, integrity protection, remote services and users; classify deviations; document justified exceptions or inapplicability. Evidence: checklist without recovery keys. Success: distinguish noncompliant, not applicable and not verifiable. Recovery: do not change platform protections during inspection.

**L23B · Bounded Unified Log query.** Environment: harmless course activity in a known time window. Tasks: query by interval/component; compare Console/CLI; identify redacted/missing fields; normalize times while retaining originals. Evidence: minimized excerpt and coverage statement. Success: do not equate missing events with absence of activity. Recovery: retain or erase extracts under the agreed policy.

**L23C · Restore and investigate.** Environment: synthetic file versions and prepared logs. Tasks: hash sources; build a change sequence; restore to another path; distinguish restoration from investigation; explain shell-history limitations. Evidence: manifest, timeline and limitations. Success: preserve originals and do not extract Keychain secrets. Recovery: remove only the rehearsal restoration.

## Checkpoint C4

Administer macOS through GUI and CLI, identify architecture/version limitations and respect native protection mechanisms. Offline screenshots alone do not establish native administration competence.
