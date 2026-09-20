# D11 · From a window to a system: terminals, bytes and files

## A visible action has a system context

Opening a terminal does not change your account or permissions. A terminal displays input/output; its shell interprets command syntax and starts programs. Identify the host, user, directory and interpreter before comparing GUI and CLI results. A command copied from another platform can fail because its syntax, program implementation or environment differs.

A path tells the system how to reach an object. Absolute paths start from a defined root; relative paths depend on the current directory. Spaces and metacharacters must reach programs as filename data rather than being split or interpreted by the shell. A file manager can hide dotfiles or extensions; that can explain a counting difference without any missing data.

## Content and representation

Text is encoded as bytes. UTF-8/UTF-16, a byte-order mark and LF/CRLF can make similar displayed text differ in size and SHA-256. A content hash says nothing by itself about preserved ACLs, ownership or all timestamps. An extension is not proof of file format. Apparent file length, allocated blocks and free filesystem space measure different things.

## Guided observation

Use the course's synthetic workspace, not personal folders. Inspect it through the file manager and terminal; enable hidden-file display; compare content byte counts; inspect the LF/CRLF files without editing them. Generate a manifest and compare with a second tool. Copy one source file into `salida`, alter only that copy and show that the source hash remains unchanged.

Keep commands and actual filenames unchanged between language editions. The `oslab.py` reference dataset contains eight files totaling 62 bytes; other teaching datasets may differ. Explain a discrepancy before changing permissions or attributes.

## Evidence and reflection

Submit an environment sheet, annotated commands, a name/size/hash table and a copy comparison. Test an invalid path and explain why more privilege cannot repair a misspelled name. Preserve originals and remove only identified trial copies. The learning outcome is a model of files and execution that transfers to other systems, not memorization of one listing command.

# D12 · Bash: from a useful command to reliable automation

## Define a contract first

State accepted arguments, required environment, output schema, effects, errors and limits. A shell script is a program whose correctness depends on expansion rules and the commands it invokes. Quote paths, use positional parameters deliberately and keep stdout data separate from diagnostics. Unknown or invalid input should not silently produce a plausible success report.

## Build incrementally

Start with a small read-only operation, then extract functions, validate arguments and add help. `bash -n` catches syntax problems but cannot prove correct behavior, file permissions or command availability. Review with local documentation and optionally an approved static checker. Every improvement should retain the reference output and known failures.

Test ordinary input, missing argument, invalid directory, spaces, hidden files and empty data. Consider how a glob behaves without matches and what a scheduled task inherits. Record the actual interpreter/version: zsh and different Bash versions are not automatically interchangeable.

## Robustness and safety

Idempotence, dry-run, timeouts, concurrency control, logging, temporary-file cleanup and atomic output are distinct features. A tiny example script does not automatically implement all of them. Add only what the contract needs and test failures explicitly. Review source/destination overlap before backup tasks. Limit cleanup to files created within the approved workspace.

## Practical product

For L11A/R02 read the supplied summary script, predict its result, check syntax and compare its count/bytes with the Python manifest. Add help and two tests in a learner copy. Explain why syntax validation and a single successful execution are insufficient. Submit the contract, diff, results and limitations, then remove only the trial copy.

# D13 · Windows: interfaces, languages and administrative objects

## Three command environments

CMD provides native text utilities and batch control structures. BAT is useful for reading legacy automation but has expansion and quoting limitations. PowerShell provides typed objects, providers and administrative modules. Windows PowerShell 5.1 and PowerShell 7 also differ. State which interpreter runs each example; changing the directory does not change the account or shell.

## Prefer the data model

Inspect PowerShell output with `Get-Member`. Filter by actual properties and export data before visual formatting. `Format-Table` belongs to presentation, not the middle of a data pipeline. Text from native commands can depend on OS language and encoding. Return codes also need tool-specific interpretation; a nonzero copy-tool result does not always mean the same failure.

## Administration and permissions

Map GUI tasks to processes, services, schedules, Registry values and NTFS ACLs. Inspect effective identity and inherited permissions before approving a change. `-WhatIf` only works where implemented and is not rollback. A scheduled task needs an explicit working directory, paths and identity. Preserve prior configuration and verify functional and denied cases.

## Native coverage

PowerShell on Linux can teach the language, but does not validate NTFS, Registry, Event Log or Windows remote-management behavior. Directory roles and features depend on the installed edition. Native exercises need their own environment/version/test records.

## Evidence

Solve a bounded inventory problem with CMD, BAT and PowerShell; compare error handling, data contracts and portability rather than just command count. Use synthetic names with spaces and invalid inputs. Document observed differences, a migration rationale and recovery. Never treat execution policy as proof that arbitrary scripts are safe.

# D14 · macOS is not Linux with a different appearance

## Shared concepts, different implementation

Darwin/XNU, Apple frameworks and application bundles coexist with Unix files, permissions and processes. APFS containers, volumes and snapshots differ from a simple partition model. Intel/Apple Silicon and OS versions affect tool and protection availability. Record the real platform before making comparisons.

## Shell and utility compatibility

Declare zsh or Bash explicitly. Login, interactive and scheduled contexts may load different files and PATH values. BSD versions of `stat`, `date`, `find` or `sed` may not implement GNU options. A portable script requires tested assumptions, not only a Unix-looking shebang.

## Configuration and protection

Inspect application bundles, `~/Library` versus `/Library`, plist syntax and extended attributes. A persisted preference does not always equal active state. Permissions, ACLs and TCC can independently affect access. launchd user agents and system daemons have different domains and lifecycle; use the smallest appropriate scope.

Audit FileVault/recovery, native integrity and application controls without disabling them to finish an exercise. Third-party package managers need provenance and maintenance review. Keychain is an approved secret store, not a source to dump into a class inventory.

## Practice and evidence

Compare Finder and Terminal, copy synthetic files and inspect content plus metadata, port a read-only summary to zsh and validate a synthetic plist. Analyze scoped Unified Log output while retaining original timestamps and acknowledging redaction/retention. Report native tests separately from offline reading. Preserve originals and remove only created trial resources.

# D15 · Operating a service: from host to useful result

## Trace a request

A user-facing failure may originate in DNS, route selection, transport, TLS, permissions, application logic or a backend dependency. A running process does not establish a useful response. Choose diagnostic steps that distinguish hypotheses and preserve the initial state before changing it.

## Service contract

Document identity, executable, configuration, working/data directories, listener, expected responses, dependencies, logs, start/stop behavior and recovery. Give configuration and private keys appropriate permissions. Validate server configuration before reload and confirm both legitimate access and a restriction.

A health endpoint is useful only if its meaning is defined. A TCP socket accepting connections may conceal application errors. Do not describe a classroom health check as comprehensive production monitoring.

## Packaging and recovery

A container can make dependencies reproducible, but it still depends on host isolation, networking and persistent storage. Explain what survives a restart and how it is backed up. Compose, Swarm and Kubernetes differ in publication and deployment semantics. Keep service data and credentials outside source images and public repositories.

## Laboratory

Run the local synthetic service on loopback, query its health and inventory routes, observe responses/logs, stop it and distinguish refusal from an application error. Restart and verify useful output. Optionally review Compose/Swarm files on a dedicated lab host, recording what has actually been run.

Submit a diagram, runbook, expected/observed responses, logs, negative test and restoration procedure. Avoid broad firewall changes or global permission grants as a troubleshooting shortcut. Production deployment needs additional identity, TLS, monitoring, backups and operational ownership beyond the demo.

# D16 · Evidence, timelines and indicators: from data to decisions

## Preserve and scope

Start with the investigative question and an inventory of available sources. Preserve originals and record hashes, receipt, tools, versions, identities and transformations. A hash comparison checks bytes; it does not independently prove origin, personal authorship or complete custody.

## Normalize without losing information

Keep original timestamps and zones alongside normalized UTC values. State resolution, clock drift and collection delay. Deduplicate records while retaining their source associations. Do not invent missing fields or treat an absent value as false. A timeline is an evidence-backed representation with uncertainty, not an omniscient sequence.

## Indicator semantics

Specify types, algorithms, exact fields, validity periods and match rules. Domain, URL, subdomain, process name and hash have different semantics. Confirm positive controls and test lookalike negatives. An IOC hit is a lead requiring context; no hits may reflect limited visibility. Public enrichment can disclose internal information and needs separate approval.

## Practice

Work on the provided synthetic event set. Build the timeline, explain duplicate events and clock representations, validate the indicator list and compare exact-domain matching with explicitly allowed subdomain matching. Preserve the result of invalid-input tests and note the selected time window.

## Report

Separate facts, inferences and alternative explanations. Link each claim to an evidence item and specify what additional source would distinguish alternatives. End with a proportional next action, confidence and coverage limits. Recovery of a service should not overwrite original evidence needed for this analysis.

# D17 · Terminal AI: proposal, verification and decision

## Select a bounded task

AI can help explain a command, suggest tests, review a learner script or summarize synthetic logs. State OS/version/shell, purpose, allowed data and output contract. Keep inference tools separate from execution permissions. A local model still requires licensing, resource and access review.

## Treat content as untrusted

A log, code comment or retrieved document may contain instruction-like text. It remains evidence to analyze, not authority to change the task or act on systems. Prompt wording is only one defense; effective account permissions, network scope, allowed paths, tool capabilities and human approval are independent safeguards.

## Structured output and independent checks

Validate JSON structure, field types, limits and allowed actions. A syntactically valid result can still contain false claims or irrelevant conclusions. Compare every load-bearing finding with source lines and deterministic tests. Distinguish a confirmed defect from a hypothesis or abstention.

## Evaluation

Use small cases with reference answers and report successes, omissions, false positives, cost and latency where measured. Compare with the deterministic or manual method. Document which work can be completed without a model and when AI adds no value.

## Practical record

Record tool/model/version/settings, local/remote mode, sanitized input, output actually used, rejected suggestions, reviewer, independent tests and retention. Do not publish real private logs or credentials. In L31B/R08 an instruction-like synthetic line tests this separation: no proposed action is automatically executed. The web campus itself is a guided reader, not a model-backed terminal.

# D18 · From classroom practice to professional work

## Deliver a usable result

A professional artifact lets another person operate, verify or investigate without relying on its author's memory. Include scope, assumptions, versions, steps, expected outcomes, error interpretation, rollback and limitations. Use meaningful commits and review comments; line count is not a quality metric.

## Evidence of competence by role

A system administrator can hand over an inventory, service runbook and demonstrated restoration. A Blue/SOC analyst can explain a detection query, telemetry coverage and false positives. A DFIR learner can preserve a case, reconstruct a timeline and test alternative explanations. A control evaluator can define scope, identify a deviation, conduct a benign validation and retest. A CTI learner can normalize indicators and state confidence, expiry and a decision-oriented recommendation.

## Communication and teamwork

Use a short summary for decision-makers and a traceable technical appendix. Separate facts from assumptions and possible consequences. Rotate operator, observer and documenter roles. Each team member must explain a component they did not create alone. Asking for clarification on scope or stopping when recovery is uncertain is part of responsible practice.

## Portfolio and disclosure

Keep the learning portfolio private until reviewing personal data, secrets, evidence ownership and third-party licensing. Public course source is not permission to publish real incident artifacts. Describe training outcomes accurately; course completion is not a substitute for native experience or advanced professional certification.

## Final reflection

For each block explain the problem solved, how success was checked, what failed, how it was recovered and what remains uncertain. Record how AI contributed and how its output was independently checked. Prefer reproducible small demonstrations to a long list of tools with no evidence of understanding.

# D19 · Teaching plan and curriculum map

## Purpose and entry level

Build from genuine terminal beginners to practical intermediate administration across Linux, Windows and macOS. Learners need basic keyboard/file skills and an approved lab. The instructor diagnoses gaps in paths, installation, error reading and accessibility rather than presuming programming or networking knowledge.

The goal is to understand, operate, automate, protect, investigate and communicate. Proposed hours are a teaching plan, not an official university equivalence, vendor certification or automatically measured attendance.

## Load and sequence

| Block | Modules | Hours | Theory / practice |
|---|---|---:|---|
| Foundations and method | M01–M04 | 56 | 20 / 36 |
| Linux and Bash | M05–M12 | 112 | 40 / 72 |
| Windows and PowerShell | M13–M19 | 98 | 35 / 63 |
| macOS and zsh | M20–M23 | 56 | 20 / 36 |
| Operations and cybersecurity | M24–M30 | 98 | 35 / 63 |
| Terminal AI | M31 | 20 | 8 / 12 |
| Capstone | M32 | 40 | 10 / 30 |
| Total | 32 modules | 480 | 168 / 312 |

M01–M30 each contain five theory hours and three three-hour labs. M31's labs each take four hours; M32's three phases each take ten. Preparation, evidence, assessment and recovery are included, not added again. The complete calendar contains 240 two-hour sessions; holidays and breaks must be allowed for when assigning real dates.

## Pedagogy

Show a concrete task in GUI, explain the OS object, reproduce or verify it in CLI, ask for a prediction, run a bounded example, compare results and introduce a small variation. Most assessed practical work uses or verifies the terminal. Adapt interfaces and accessibility without relaxing evidence and safety requirements.

Before each lab identify machine/account/directory/effect, permissions and recovery. Afterwards use an independent check, record errors, minimize evidence and remove temporary changes. A command copied without understanding its effects does not establish competence.

## Alternative routes

A 120-hour introduction can select 20 foundation, 30 Linux, 10 Bash, 25 Windows/PowerShell, 15 macOS, 10 network/backup and 10 project hours. A 240-hour secure-administration route can allocate 28 foundations, 60 Linux/Bash, 56 Windows, 28 macOS, 32 network/web/automation, 20 hardening/logging and 16 project hours. A 60-hour sampler can allocate 12 foundations, 16 Linux, 8 scripting, 10 platform comparison, 6 network/security and 8 project hours. These routes are not equivalent to completing every full module.

Specialization follows demonstrated prerequisites. SysAdmin deepens services/automation; SOC focuses logs/detection; DFIR emphasizes preservation/timelines; CTI focuses structured indicators; Red/Purple emphasizes approved control validation. Do not double-count reused hours.

## Longitudinal deliverables and checkpoints

Maintain a versioned notebook, minimized inventory, network/access diagrams, reviewed scripts/tests, change/exception log, synthetic evidence manifest, uncertain timeline, demonstrated recovery and two-page executive report. Use C1–C6 after the designated blocks to assess independent reasoning, not memorized flags. A learner remediates a missing competency through an equivalent new exercise.

# D20 · How to study: theory, practice and evidence

## Choose a starting point

New learners should begin at M01 and follow prerequisites. Experienced learners can use the full index and search to find a competency, while checking prerequisite concepts. The platform does not lock content based on checkboxes. Planned hours guide effort; they do not measure actual time studied.

## One lesson, three views

Theory contains explanations, tools, references and a notebook. Presentation divides the same content into sections for teaching or focused review; arrows navigate and Escape exits. Guided practice organizes preparation, manual execution, checking, evidence and recovery. A slide or checkbox does not replace practical evidence.

## A repeatable study session

Identify the module objective and context. Read the theory and predict the result of a small example. Use local help to resolve uncertainties. Attempt the formative quiz and review its explanation. Open the linked lab and work only in the assigned environment. Record expected versus actual results, include a negative test, preserve evidence and restore the environment.

On a phone or tablet, read, navigate, answer checks and prepare the worksheet. System-administration commands still run manually on the authorized computer; the web page does not open a terminal or administer the device. Continue later from a laptop for native practice.

## Keep your progress

Reading confirmations, quiz milestones, favorites, lab phases and notes are local to the browser. The same stable IDs are used in Spanish and English, so changing language does not reset them. Export a full JSON backup for your own storage; it can contain notes and must be handled carefully.

Use the explicit progress-transfer feature to move only milestones, preferences and resume location to another device. It excludes notes, identities and login credentials. Review the import preview before merging. A shared copy is not automatic synchronization; new work on one device does not update the other until transferred again.

## Demonstrate and reflect

Explain what changed, why the check is meaningful and what cannot be concluded. Separate genuine observations from assumptions. State any AI assistance and independent verification. Revisit weak prerequisites and keep a concise list of unresolved questions. Completion is self-declared and is not an instructor assessment or professional certification.

# D21 · From source to deployment: static sites, Pages and Workers

## Deploy the correct application

The original repository contained a static campus and an independent legacy Next.js application. This repository retains the campus and teaching material; the legacy application remains in the original repository. The campus is generated from teaching sources into `campus/dist`. It does not need the legacy application's dependencies, OpenNext, an R2 cache or a self-reference service binding. A root-level generic Wrangler command without the intended configuration can select the wrong application.

The supplied September build logs show two different failures: an automatically configured Next.js deployment referenced an absent `frontend` service, and a later version-upload command did not specify a script or asset directory. These are deployment-target/configuration errors, not evidence that the static course requires a Next.js adapter.

## Pages through Git

Select the repository and `main`, framework none, root directory `campus`, build command `python3 build.py && python3 check_release.py`, output directory `dist`. Set `SKIP_DEPENDENCY_INSTALL=1` and the documented Python version. Keep previews separate from production. Do not use the Next.js preset for this campus.

The generated ZIP can be used for a manual Pages Direct Upload. The ZIP must have `index.html` at its root, not an extra parent directory. A Direct Upload project and a Git-integrated project have different management paths; choose Git integration initially when ongoing rebuilds are wanted.

## Static Workers

The repository's explicit static-assets configuration points to `./campus/dist`. Use `python3 campus/cloudflare.py plan` to inspect the workflow, `build` or `check` for local validation, and the documented `dry-run` to exercise packaging without publication. Approved `deploy` publishes; `preview` uploads a version without promoting it. No credentials belong in source or the browser.

## Validate what was built

`check_release.py` verifies the expected assets, catalog, HTTP security headers, routes, SHA-256 manifest and ZIP/directory agreement. Build provenance should identify the actual source commit only when the input tree can be verified. Generated outputs are not an independent source of truth.

After deployment inspect the homepage, full index, search, theory, a lab, presentation, progress export/import and both languages. Check phone/tablet layouts and a real two-device progress transfer on the final origin. Changing origin changes browser storage, so export before migration.

## Limits and rollback

A passing local build is not proof of deployment to an account. Report the actual URL and tested revision only after checking them. Restore the previously known-good published version if acceptance fails. Authentication or email OTP requires an explicitly configured identity service and, for continuous progress synchronization, a separate protected storage service; adding an access gate alone does not synchronize local browser data.
