# M01 · Orientation, safe working and the laboratory

## Understand the environment before acting

A terminal is an interface, not permission to administer every reachable computer. Before a command, identify the host, operating system, account, current directory and intended effect. Distinguish observing state from changing it. An ordinary query may still create logs or update metadata; read-only does not mean forensically invisible.

A physical host, a virtual machine and a container are different execution boundaries. A snapshot is useful for rollback, but may share its failure domain with the original disk. A backup aims at recoverability; preserved evidence aims at traceable analysis. Keep the only copy of your notebook outside the machine you will restore.

## Outcomes and theory

No previous terminal experience is required. By the end, prepare an isolated environment, state the authorized scope, document a small intervention and restore its previous state.

1. Administrator, security analyst and investigator: different responsibilities and evidence requirements.
2. Host, guest, hypervisor, container and remote service: locate where code actually runs.
3. Standard and administrative identities; technical privilege versus authorization; operational and privacy risks.
4. Console, terminal, shell and interpreter: related but distinct components.
5. Snapshot, backup and original evidence: purpose, retention and limitations.
6. Technical notebook: time, version, action, observed output, interpretation and recovery.

Use the hypervisor interface, its network settings, a file manager, an editor and each system's terminal. Start with built-in help and queries for identity and working directory; do not modify the host network. Each ordinary module has 5 hours of theory and 9 of practice; each A/B/C laboratory has 3 hours. Follow [the laboratory contract](#/recurso/D01).

## Laboratories

**L01A · A reproducible starting assessment.** Environment: the assigned computer, standard account and a practice file. Tasks: identify OS/version; open the GUI and terminal; locate the file both ways; save the output of a harmless query; explain an invalid-path error. Evidence: an initial environment sheet and a minimal screenshot without personal information. Success: identify machine, account and location, and distinguish observations from interpretations. Recovery: close sessions and retain only course materials.

**L01B · Isolation and recovery.** Environment: an empty VM and an approved practice network. Tasks: describe adapters and routes; check a predefined allowed and denied flow to assigned destinations; take a snapshot; change a text file; restore it. Evidence: a network diagram and a before/after comparison. Success: demonstrate restoration and absence of unintended external exposure. Recovery: return to the baseline snapshot while retaining the notebook outside the VM.

**L01C · The first controlled intervention.** Environment: a synthetic directory tree. Tasks: write the objective and limits; make one reversible change; record time and action; ask another learner to reproduce the result; document discrepancies. Evidence: a change ticket, activity log and peer review. Success: another person can reproduce the task without verbal instructions. Recovery: undo only the approved change.

## Demonstrate understanding

Explain why restoring a snapshot can destroy incident evidence. Never operate on an unidentified machine. Stopping when scope is unclear is a professional decision, not a failed exercise.

# M02 · Information representation and hardware

## From meaning to bytes

A byte sequence, the text it represents and the way an application displays it are different things. Visually identical text can have different hashes because encoding, byte-order marks or line endings differ. A filename extension is a hint, not proof of its actual format. Hashing, compression and encryption serve different purposes.

Resources also need context: memory used as cache is not automatically evidence of a shortage, and virtual memory is not the same as resident physical memory. Compare like units and measurement windows before diagnosing a bottleneck. A VM reports assigned resources, which need not describe its physical host.

## Outcomes and theory

Prerequisite: M01. Relate information representation, hardware resources and observable symptoms without treating every size difference as an anomaly.

1. Bits, bytes, binary and hexadecimal; decimal versus binary units.
2. ASCII, Unicode, UTF-8, UTF-16, byte-order marks and LF/CRLF line endings.
3. CPU architecture, instructions, cores, threads, RAM, caches, buses and disks.
4. Logical and physical storage, blocks, latency, IOPS, capacity and introductory virtual memory.
5. Text and binary formats, extensions, compression, hashes and signatures.
6. Instantaneous use, averages, saturation and the denominator behind a metric.

Compare system information and resource-monitor GUIs with `lscpu`, `free`, `df`, `od`, `Get-ComputerInfo`, `Format-Hex` and scoped `system_profiler` queries where available. Do not collect hardware serial numbers or product keys for an ordinary course inventory.

## Laboratories

**L02A · Same text, different bytes.** Environment: learner-created files, no real records. Tasks: save accented text in two encodings; compare size and hexadecimal representation; change LF/CRLF; calculate hashes; explain equal meaning with unequal bytes. Evidence: encoding, size and hash comparison. Success: decode the text without losing characters and explain each difference. Recovery: preserve original samples and remove only disposable copies.

**L02B · A reasoned inventory.** Environment: one VM and its host, with query permission. Tasks: record CPU, RAM, storage and architecture; compare GUI and CLI; distinguish physical from allocated resources. Evidence: a minimized inventory without serial numbers. Success: explain two apparent discrepancies. Recovery: make no configuration changes and close monitoring tools.

**L02C · Diagnose resource pressure.** Environment: prepared CPU, memory and storage measurements, not unbounded load generators. Tasks: identify likely bottlenecks; explain missing measurements; propose low-impact verification. Evidence: hypotheses and a test plan. Success: avoid equating cached memory with exhaustion or comparing GB and GiB as identical units. Recovery: retain the original measurements for repeat analysis.

## Demonstrate understanding

Explain what a changed hash establishes and what it cannot establish about authorship, origin or an incident.

# M03 · OS architecture, boot and execution

## One system, several layers

Applications request services from the operating system rather than controlling hardware directly. The kernel mediates memory, devices and execution; user-space programs operate within identities and privileges. A process has an owner and resources even when it has no visible window.

Follow the relationships between a service manager, executable, process, parent, account, open file and socket. They are related objects, not interchangeable names. A container shares its host kernel; it is not a full independent operating system. Linux, Windows NT and Darwin implement similar responsibilities differently.

## Outcomes and theory

Prerequisite: M02. Build a model of execution, files, memory, identities and services that can be applied across all three platforms.

1. Kernel/user space, system calls, drivers, APIs and privilege boundaries.
2. Firmware/UEFI, verified boot, boot loader, kernel, services and login session.
3. Processes/threads, PID/PPID, scheduling, states, signals and process objects.
4. Virtual memory, paging, address spaces, isolation and resident usage.
5. Descriptors/handles, I/O, sockets, IPC, open resources and locks.
6. Filesystems, mounts, metadata, paths, journaling and copy-on-write.
7. Unix/Linux, Windows NT and Darwin/XNU: conceptual similarities and implementation differences.

Compare Task Manager, Activity Monitor and process tools with `ps`, `top`, `lsof`, Linux `/proc`, `Get-Process` and introductory `launchctl` inspection. Do not assume macOS provides Linux `/proc`.

## Laboratories

**L03A · An execution tree.** Environment: an editor and terminal under a standard account. Tasks: start a harmless program; observe PID, parent, user and resources; close it normally; confirm termination by GUI and CLI. Evidence: an explained process tree. Success: distinguish terminal, shell and child program. Recovery: close only processes created by the learner.

**L03B · Follow a file.** Environment: a practice volume. Tasks: trace a path from directory to volume; inspect ownership, size, permissions and metadata; open the file and inspect the resource if tooling permits. Evidence: a layer diagram. Success: distinguish path, file, descriptor and physical block. Recovery: do not unmount system volumes.

**L03C · Service versus session.** Environment: a VM with an instructor-managed demonstration service. Tasks: inspect its process and state; close an ordinary session; identify what remains running; examine a boot log. Evidence: a timeline and explanation. Success: distinguish configured autostart, current execution and visible applications. Recovery: reconnect without modifying security services.

## Demonstrate understanding

Explain where code runs and where authorization is enforced. Do not infer physical memory usage directly from virtual-memory size.

# M04 · Terminal method, documentation and Git

## Learn commands, not incantations

Read a command's help in the installed version. Identify options, operands, required privileges, standard streams, exit conditions and side effects. A shell alias may select a different implementation from the executable you intended. Working directory and PATH can explain a failure without any need for elevation.

Git records changes, not just final files. Review a diff before staging and committing. Removing a secret in the newest revision does not remove it from history; do not commit credentials in the first place. Reproducible notes describe assumptions and failed attempts as well as the successful command.

## Outcomes and theory

Prerequisite: M03. Perform reproducible terminal operations and preserve documentation without uploading sensitive material.

1. Prompt, command, arguments, options, paths, working directory and completion.
2. Help syntax, examples, version scope, limitations and exit codes.
3. stdin/stdout/stderr, redirection and pipelines; text versus objects.
4. Environment, PATH, aliases, profiles and executable resolution.
5. Git working tree, staging area, commit, diff, log, branches, merging and review.
6. Markdown, README files, issues, logbooks, licenses and pre-commit privacy review.

Use `man`, `help`, `type`, `command -v`, `Get-Help`, `Get-Command`, `git status`, `git diff`, `git add`, `git commit`, `git log` and `git switch`. Do not treat forced pushes as the default way to resolve conflicts.

## Laboratories

**L04A · Learn an unfamiliar command.** Environment: a practice directory. Tasks: define a goal; consult local help; identify version and syntax; test on a synthetic file; separate stdout/stderr; inspect exit status. Evidence: an annotated recipe. Success: reproduce it without running unexplained copied commands. Recovery: remove only identified temporary outputs.

**L04B · A versioned notebook.** Environment: a local learner repository. Tasks: create a README and submission tree; inspect diffs; make three meaningful commits; create a branch; correct a documentation error; compare versions. Evidence: history and rationale. Success: no credentials, binary evidence or personal data in commits. Recovery: retain history and demonstrate a deliberate reversal rather than deleting it.

**L04C · Peer review.** Environment: a test repository with no production access. Tasks: follow another learner's instructions; detect a nonportable absolute path and an unstated privilege requirement; propose corrections; resolve a simple text conflict. Evidence: review comments, diff and reproduction test. Success: instructions work in a fresh directory. Recovery: leave a clean, documented working branch.

## Checkpoint C1

Navigate, obtain help, identify effects and document an operation without unnecessary privileges. Explain a result rather than reciting a memorized command.

# M05 · Linux files, directories and the shell

## Paths and file objects

A path describes how to reach an object; it does not identify its content permanently. A rename, copy, hard link and symbolic link have different effects. Inspect content and metadata separately: matching content hashes do not establish that ownership, ACLs or timestamps were preserved.

Shell expansion occurs before a utility receives its arguments. Quotes, spaces, wildcards and leading hyphens affect how a filename is interpreted. Confirm the working directory before recursive operations and constrain searches to the part of the filesystem required by the task.

## Outcomes and theory

Prerequisite: M04. Locate, create, copy, compare and organize files safely while interpreting paths and metadata.

Study `/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/run`, `/proc` and `/sys`; absolute and relative paths; hidden names; quoting and globbing; hard/symbolic links; regular files versus devices; size, ownership, timestamps and permissions; safe editing and pre-replacement comparison.

Use a file manager/editor and `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `stat`, `file`, `readlink`, `ln`, `diff`, `cmp`, `du`, `find` and `sha256sum`. Explain options before recursion. Never practise writing to `/dev`, `/proc` or `/sys`. Consult the [cross-platform reference](#/recurso/D02).

## Laboratories

**L05A · Find the missing file.** Environment: a synthetic tree of 20 files. Tasks: navigate by GUI/CLI; search by name, type and depth; handle hidden files and spaces; justify relative/absolute paths. Evidence: an inventory and annotated commands. Success: find the targets without unnecessary whole-system searches. Recovery: return to the original working directory without changing source files.

**L05B · Copy without confusion.** Environment: two learner-owned directories. Tasks: copy and compare files; create links on the practice volume; observe renaming and metadata; explain what each operation preserves. Evidence: before/after table with hashes. Success: distinguish a copy, a link and a broken reference. Recovery: remove only links and copies created for the exercise.

**L05C · A configuration change.** Environment: a fictional application's configuration file with no system effect. Tasks: back up; edit one key; review the diff; validate syntax; demonstrate restoration. Evidence: original, diff and verification. Success: no change outside the authorized file and reproducible rollback. Recovery: restore the initial version.

## Demonstrate understanding

Work with spaces and Unicode, explain recursion and option parsing, and avoid treating metadata as conclusive evidence of authorship.

# M06 · Text processing, searching and pipelines

## A pipeline is a data contract

Each stage receives a representation and emits another. Know whether you are processing bytes, lines, delimited fields or structured data. A successful final command can conceal an earlier failure unless errors are checked. Zero matches, an empty file and permission denied are distinct outcomes.

Literal strings, shell globs and regular expressions have different meanings. Normalize only what the task permits and preserve original values and provenance. A substring that resembles a domain or IP is not necessarily an exact indicator match. Use a structured parser for structured formats rather than regular expressions for nested JSON.

## Outcomes and theory

Prerequisite: M05. Build bounded, repeatable searches and transformations, then verify their counts and assumptions.

Study streams and redirection; literals/globs/regex; filtering, grouping and aggregation; sorting and locale; delimiters and filenames containing newlines; empty inputs and errors; structured versus free-form data.

Use `cat`, `less`, `head`, `tail`, `wc`, `cut`, `tr`, `sort`, `uniq`, `grep`, `sed`, `awk`, `find`, `xargs` and `tee`; add `jq` when approved. Prefer NUL-delimited filename handling where supported; do not parse `ls` output as a filename API.

## Laboratories

**L06A · Activity summary.** Environment: 30 synthetic log lines. Tasks: filter by interval/event; count results; group by a defined field; preserve the original input. Evidence: pipeline, output and a manual control count. Success: consistent totals and explicit distinction between no matches and failure. Recovery: retain the original log.

**L06B · Difficult filenames.** Environment: names with spaces, leading hyphens and Unicode. Tasks: compare naive and safe traversal; pass names as arguments, never code; explain quoting and separators. Evidence: a positive test and a boundary case. Success: every file is processed exactly once. Recovery: remove only the learner's dataset after documenting results.

**L06C · A difference report.** Environment: two synthetic exports. Tasks: normalize specified fields; deduplicate while retaining provenance; compare; classify changes in order, representation and meaning. Evidence: deterministic output and normalization rules. Success: cleaning does not erase substantive differences. Recovery: rerun from original inputs to demonstrate repeatability.

## Demonstrate understanding

Justify the pattern, search field, time window and denominator. Include negative controls rather than judging correctness from plausible-looking output.

# M07 · Linux users, permissions and privilege

## Verify effective access

An account's UID, groups, directory traversal rights, file permissions, ACL mask and mandatory access controls can all affect an operation. A directory's execute permission governs traversal, not program execution in the same sense as an executable file. Explain effective access through a permitted and a denied test.

Separate human administrators from service identities. A service should receive the resources it needs, not a personal account's entire privileges. Broad writable permissions may appear to fix an application while creating a new security problem. Investigate the failed control rather than disabling it.

## Outcomes and theory

Prerequisite: M05. Design, apply and verify least-privilege access without breaking authentication or disclosing secrets.

Study UID/GID; local/service identities; identity resolution; rwx and directory semantics; umask; ACLs and masks; ownership/groups; sudo delegation; PAM/NSS architecture; capabilities and special bits as audit topics; AppArmor/SELinux; account lifecycle.

Use GUI account settings, `id`, `getent`, `groups`, `stat`, `namei`, `getfacl`, `setfacl`, `chmod`, `chown`, `umask` and `sudo -l`. Account creation/removal commands are distribution-specific and used only for fictional accounts under supervision. Audit capabilities without privilege-escalation exercises.

## Laboratories

**L07A · A team directory.** Environment: a VM with two fictional accounts. Tasks: define read/write requirements; configure a dedicated group and directory permissions; verify both identities and parent traversal. Evidence: access matrix and positive/negative tests. Success: collaboration without global write permissions. Recovery: restore original ACLs and remove practice accounts under instructor control.

**L07B · Privilege review.** Environment: a snapshot with sample permissions. Tasks: inventory administrative memberships, delegated rules and application-directory permissions; distinguish functional need from excess; propose a minimal correction. Evidence: finding, impact and responsible owner. Success: justify least privilege without attempting exploitation. Recovery: do not modify authentication rules during this inspection.

**L07C · Controlled onboarding and offboarding.** Environment: a disposable VM. Tasks: define request, approval and expiration; create a lab account; verify assigned access; disable it without destroying required data. Evidence: lifecycle record and verification. Success: no unexplained residual privileges and a documented data-retention decision. Recovery: restore the snapshot or remove the account using the approved plan.

## Demonstrate understanding

Explain why visible rwx bits alone may not determine access. Never replace diagnosis with unrestricted permissions.

# M08 · Linux processes, packages, services and scheduling

## Configuration is not current state

A service can be enabled for boot yet stopped now, or running now without being enabled. A process can outlive an interactive shell because a system service manager owns its lifecycle. Map unit, executable, process, identity, dependencies and logs before deciding to restart.

Scheduled tasks run in a different context from interactive sessions. Set working directories, executable paths, environment and output permissions deliberately. A task that silently fails can create an operational blind spot; record success and failure separately. Package provenance and repository trust are part of service management.

## Outcomes and theory

Prerequisites: M06 and M07. Diagnose and operate services, software and scheduled tasks with traceable changes.

Study processes/signals/jobs/resources; signed repositories, packages and dependencies; systemd services, units, timers and sockets; start/stop versus enable/disable; unit files and overrides; cron's restricted environment; boot/journal diagnosis; dedicated service accounts and isolation.

Use a process monitor/package GUI, `ps`, `top`, `pgrep`, `jobs`, `wait`, `systemctl`, `journalctl` and `crontab`; choose `apt/dpkg` or `dnf/rpm` according to the distribution. Do not stop security components or other users' processes.

## Laboratories

**L08A · Process or service?** Environment: a VM with a harmless demonstration service. Tasks: associate unit, process, user, executable and log; compare running and boot-enabled states; explain dependencies. Evidence: a service inventory sheet. Success: explain execution without a visible interface. Recovery: retain original boot configuration.

**L08B · Controlled software update.** Environment: a VM clone. Tasks: inventory versions; review repository origin; preview package changes; apply an approved update; test the service and available rollback. Evidence: change ticket and functional test. Success: no unapproved repositories or assumption that every update is risk-free. Recovery: restore the clone if acceptance fails.

**L08C · A legitimate periodic task.** Environment: a learner script producing a summary without secrets. Tasks: run manually; declare paths, account and environment; schedule with a timer or cron; demonstrate normal execution and a controlled failure. Evidence: definition, timestamps and logs. Success: least privilege and no duplicate executions. Recovery: remove only the schedule created for the exercise.

## Demonstrate understanding

Use logs to identify causes before repeatedly restarting. Explain why a command may work in a terminal and fail in a task.

# M09 · Linux storage, backups and recovery

## Recoverability must be demonstrated

An archive's existence is not evidence that a service can be restored. Recover into a separate destination and verify content, permissions and application usability. Measure elapsed recovery time and actual data loss, then compare them with agreed RTO and RPO rather than presenting objectives as measurements.

Filesystems expose different metadata and preservation features. Copy-on-write snapshots and RAID have useful roles but are not independent backups. On SSDs and copy-on-write storage, overwriting one filename cannot universally guarantee sanitization; device behavior, snapshots and encryption-key management matter.

## Outcomes and theory

Prerequisites: M07 and M08. Explain storage layers and restore practice data while separating integrity, availability and evidence preservation.

Study devices, partitions, volumes, filesystems, inodes and capacity; mounts/options; LVM/RAID concepts; ext4/XFS/Btrfs as applicable; quotas and encryption; archives/compression; full/incremental backup; RPO/RTO; retention and external copies; TRIM/COW and deletion limitations.

Use a disk-management GUI, `lsblk`, `findmnt`, `df`, `du`, `stat`, `tar`, `gzip` and `rsync`. Filesystem checks or repair require a separately identified practice medium and the product's documented procedure, never indiscriminate repair of a live system disk.

## Laboratories

**L09A · Storage map.** Environment: a VM and an instructor-identified extra virtual disk. Tasks: inventory devices/mounts; distinguish apparent, allocated and free space; inspect mount options; diagnose prepared inode-exhaustion data. Evidence: layer map and diagnosis. Success: unambiguous identification of the practice disk. Recovery: leave the system disk unchanged.

**L09B · Verifiable backup.** Environment: synthetic documents. Tasks: produce a manifest and backup; restore to a different path; compare content/permissions; describe metadata differences between formats. Evidence: manifest, checks and recovery duration. Success: demonstrate a usable restoration, not just a backup file. Recovery: preserve originals and remove the trial restoration.

**L09C · Loss rehearsal.** Environment: a disposable copy, never the original dataset. Tasks: simulate a missing document; choose a recovery point; restore; measure potential loss and duration; propose retention and encryption with recovery. Evidence: runbook and measured RPO/RTO. Success: distinguish agreed targets from observations. Recovery: return to the documented baseline.

## Demonstrate understanding

Explain why `rm`, a single overwrite and a snapshot are not universal sanitization or backup guarantees. Test restoration before depending on it.

# M10 · Linux host networking and exposure

## Diagnose by layer

A successful DNS lookup does not establish a working TCP connection, and an open TCP port does not establish healthy HTTP behavior. A timeout, explicit refusal, DNS failure, certificate problem and application error are different observations. Choose the next check to distinguish hypotheses rather than running every network tool indiscriminately.

A listening socket is not necessarily reachable from another machine. Interface binding, host firewall, routes and intermediate controls all affect exposure. Associate a listener with its process, user and service purpose. IPv6 deserves the same review as IPv4.

## Outcomes and theory

Prerequisite: M08. Diagnose connectivity systematically and justify which service ports should be accessible.

Study interfaces, addressing/CIDR, loopback, IPv4/IPv6; ARP/NDP; routes; DNS and local resolution; DHCP; TCP/UDP, sockets/states; host firewall; proxies/VPN concepts; scoped packet capture and privacy; listening versus effective reachability.

Use network settings and `ip`, `ss`, `ping`, `tracepath` if installed, `getent hosts`, `resolvectl` where present, optional `dig` and `curl`. Use the existing firewall stack: nftables, ufw or firewalld. Do not manage overlapping layers without understanding their interactions.

## Laboratories

**L10A · Diagnose a connection failure.** Environment: two assigned VMs. Tasks: check link/address, route, DNS, the approved destination port and application response; distinguish the results. Evidence: a diagnostic decision tree. Success: explain timeout, refusal, resolution failure and application failure. Recovery: restore only the instructor's deliberately changed parameter.

**L10B · Listener inventory.** Environment: the learner's VM. Tasks: associate sockets with processes/accounts where permitted; distinguish loopback from all-interface binding; compare with expected services. Evidence: service/interface/port/purpose matrix. Success: justify each listener without scanning external networks. Recovery: query only; make no changes.

**L10C · A minimal firewall rule.** Environment: a clone with console access and a recovery administration path. Tasks: define the required flow; review rules; apply one approved restriction for a test service; test an authorized and an unauthorized client. Evidence: configuration diff and both tests. Success: required service and administration remain available. Recovery: restore the known-good policy from the console if needed.

## Demonstrate understanding

Separate name resolution, routing, transport, trust and application behavior. Disabling the entire firewall is not a diagnostic solution.

# M11 · Structured Bash programming

## Inputs are data, not commands

A script needs a contract: accepted inputs, produced outputs, permissions, effects and failure states. Quote paths, validate arguments and use arrays where their semantics fit the installed Bash version. Do not turn user-controlled strings into executable code through `eval` or command concatenation.

Error handling must be designed and tested. `set -e` is context-dependent, not a universal exception mechanism. Check pipelines, functions and native exit codes explicitly. Temporary-file cleanup must be restricted to files the script created; debugging traces must not expose secrets.

## Outcomes and theory

Prerequisites: M06 and M08. Write a small CLI with validation, structured functions and explainable success/failure behavior.

Study shebang/interpreter; positional parameters and `getopts`; variables/expansion/quoting; arrays/version limits; conditions, `case`, loops and functions; command substitution; arithmetic; standard streams; exit codes; scope/environment; signals; safe reading, temporary files and cleanup.

Use Bash, an editor and `bash -n`; approved ShellCheck can supplement review. Explain every expansion and its possible word splitting. stderr does not universally mean fatal failure; interpret the producing command's contract.

## Laboratories

**L11A · Directory-inventory CLI.** Environment: the M05 dataset. Tasks: accept a directory; validate existence; count files and sizes; separate error output; return coherent exit status. Evidence: source, usage help and three tests. Success: handle spaces, empty directories and invalid paths. Recovery: read practice data only.

**L11B · Functions and parsing.** Environment: a simple CSV and prepared JSON. Tasks: specify the contract; separate functions; choose a format-aware parser; validate missing fields; retain provenance. Evidence: expected outputs and invalid-input cases. Success: distinguish syntactic validity from meaningful valid data. Recovery: leave all source inputs unchanged.

**L11C · Controlled errors.** Environment: a learner script with simulated permission failure and missing executable. Tasks: handle errors; clean owned temporaries using `trap`; inspect pipeline statuses; prevent secret logging. Evidence: failure/result matrix. Success: no false success and no deletion outside the temporary scope. Recovery: remove only identified owned temporary files.

## Demonstrate understanding

Explain quoting, parameter expansion and each exit condition. A copied script that works once is not yet a validated automation.

# M12 · Robust and secure Bash automation

## Repeatability includes failure

Idempotence means that repeating an operation converges on its intended state rather than creating accidental duplicates or cumulative damage. A dry-run should describe actions without performing them; its own code paths need tests. Check invalid paths, overlapping source/destination directories, concurrent starts and partial failures.

Separate configuration, credentials and generated data. Bound execution time and concurrency, give output files appropriate permissions and write results so interrupted operations are distinguishable from completed ones. A useful health report distinguishes OK, warning, error and unavailable observations rather than treating missing values as healthy.

## Outcomes and theory

Prerequisites: M09, M10 and M11. Build an automation that can be reviewed, repeated and stopped safely.

Study idempotence; read-only/dry-run modes; version requirements; input/path validation; partial errors; timeouts/concurrency/locks; structured logs; temporary writes and controlled replacement; permissions; static review; regression testing; packaging and documentation. Use Bash, `getopts`, `mktemp`, `trap`, optional `jq` and platform-compatible locking. Do not assume GNU tools or `flock` are installed on macOS.

## Laboratories

**L12A · Host health report.** Environment: the learner's Linux VM. Tasks: collect version, space, selected service states and an approved local port; apply timeouts; emit structured output; omit a full environment-variable dump. Evidence: source, sanitized example and tests. Success: distinct OK/WARN/ERROR states and visible partial failure. Recovery: create report output only.

**L12B · Automated backup.** Environment: practice source and destination. Tasks: validate both paths; implement dry-run; reject dangerous overlaps; run a backup; verify restoration; simulate a second start. Evidence: idempotence and recovery tests. Success: do not overwrite originals or count repetition as an independent backup. Recovery: remove only rehearsal data.

**L12C · Adversarial input review.** Environment: learner code and synthetic inputs. Tasks: test spaces, hyphens, empty fields, permission denied and partial output; assess reporting; obtain peer review; correct and document findings. Evidence: regression cases and a diff. Success: inputs never become commands and failures are not hidden. Recovery: preserve the previous version in Git.

## Checkpoint C2

Administer and diagnose Linux without global privileges. Defend a repeatable script with invalid-input tests, bounded effects and verified recovery.
