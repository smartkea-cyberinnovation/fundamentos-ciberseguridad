# M24 · Networking, remote administration and file transfer

## Verify the destination before connecting

A remote workflow has separate requirements for reachability, encryption, endpoint identity, user authentication, authorization and audit. Verify an unfamiliar SSH host key through an independent channel. Do not disable certificate or host-key validation merely to make a connection succeed.

A transfer can preserve bytes while changing ownership, permissions or timestamps. Choose a protocol from the task's requirements and compare source/destination manifests. An approved bastion has defined identities and flows; it does not authorize every possible onward connection. Study pivoting through trust diagrams and prepared telemetry, not operational intrusion chains.

## Outcomes and theory

Prerequisites: M10, M18 and M22. Verify an authorized session and file transfer, including trust, integrity, permissions and logs.

Study TCP/IP/IPv6, DNS/DHCP/routes, recursive/authoritative resolution and TTL; proxy/VPN/segmentation; SSH keys and host identity; SFTP/SCP/rsync and metadata; RDP/WinRM/SSH remoting; certificates/revocation/temporary access; bastions; tunnels/port forwarding/SOCKS concepts and risks; authorized versus unauthorized transit; egress controls and auditing.

Use approved SSH/SFTP/SCP/rsync, RDP and prepared PowerShell sessions; `curl`, DNS/socket queries and scoped captures on assigned interfaces only. Verify the installed SCP implementation's protocol and behavior. Never reuse the instructor's personal keys or place credentials in command arguments.

## Laboratories

**L24A · A trusted connection.** Environment: an administration station, two assigned hosts and practice identities. Tasks: verify host identity independently; connect as a standard account; query approved version/state information; close; inspect authentication records. Evidence: trust checklist and minimized logs. Success: recognize a changed identity rather than accepting it blindly. Recovery: revoke the temporary identity while preserving instructor access.

**L24B · An intact transfer.** Environment: a synthetic dataset and approved destination. Tasks: select a protocol; inventory sizes/hashes; transfer; verify content/permissions; handle interruptions or existing files; document metadata differences. Evidence: source/destination manifests and results. Success: no credentials in arguments and no claim that a checksum establishes full custody. Recovery: remove the destination copy under the agreed retention policy.

**L24C · Segmentation and a bastion.** Environment: prepared diagrams and allowed/denied connection logs. Tasks: map hops/trust boundaries; distinguish proxy, tunnel and remote session; identify an unintended flow; propose restrictions on identity, source, destination and auditing. Evidence: flow matrix and detection proposal. Success: explain the control and telemetry for each hop. Recovery: offline exercise, without opening tunnels or performing operational pivoting.

## Demonstrate understanding

Explain why encrypted traffic can still be unauthorized and why a permitted first hop does not authorize subsequent hops.

# M25 · Web services, TLS and secure operation

## A working port is not a working service

Trace a request through DNS, connection establishment, TLS, HTTP and application dependencies. A listener that accepts a TCP connection can still return incorrect data or fail a useful application transaction. A meaningful health check verifies a defined response and distinguishes healthy, unavailable and unknown states.

Service accounts, configuration ownership, document roots, private keys and logs need deliberate permissions. Validate configuration before reload, preserve a rollback path and test both legitimate access and an intended restriction. Treat a local CA as a scoped teaching resource, not a reason to disable trust verification.

## Outcomes and theory

Prerequisites: M12, M19, M23 and M24. Deploy a small service, diagnose failures and reduce exposure without breaking functionality.

Study HTTP methods/status/headers; DNS and virtual hosts; web server/reverse proxy/backend; Nginx/Apache/IIS alternatives; service identity/document root; TLS certificate/name/chain/trust/expiration; private-key custody; configuration validation/reload; access/error logs; request limits/timeouts/information exposure; backups and application-aware health checks.

Use the chosen server's official tools, service manager, browser, `curl`, logs and TLS inspection against lab hosts only. One server is the primary practical implementation; comparisons with other stacks do not imply specialization in all three within fourteen hours.

## Laboratories

**L25A · An operable minimal website.** Environment: a dedicated VM/container with a light static site and synthetic data. Tasks: install through an approved channel; configure a service identity; limit root/listener; document the lab URL; test from the assigned client. Evidence: configuration, diagram and checks. Success: functional site without exposed administration panels. Recovery: approved shutdown and removal procedure.

**L25B · TLS and trust.** Environment: a lab certificate/CA without modifying production trust stores. Tasks: inspect names, chain, validity and public key; diagnose a prepared name/chain error; correct legitimate configuration; verify client/server behavior. Evidence: diagnosis and trust chain. Success: do not disable TLS validation. Recovery: remove test trust only where added and keep private keys outside Git.

**L25C · An operational incident.** Environment: a benign incorrect permission or stopped backend. Tasks: start from the symptom; inspect HTTP/log/process/permissions; form a hypothesis; correct minimally; repeat tests; propose preventive monitoring. Evidence: ticket, diff and logs. Success: no global access grants or unexplained restarts. Recovery: restore the baseline and verify availability.

# M26 · Cross-platform automation and containers

## Reproducibility is a property, not a product name

A common inventory schema lets different platforms answer the same questions without pretending their APIs are interchangeable. Preserve distinctions between missing, false, denied and unsupported fields. Use a format-aware parser and validate both syntax and meaning.

Containers package processes and dependencies but still rely on a host kernel and permissions. A mounted management socket can grant broad host control; do not give it to a student terminal. Compose, Swarm and Kubernetes have different deployment, networking, storage and secret semantics. Base64 representation is not encryption.

## Outcomes and theory

Prerequisites: M12, M16, M21 and M25. Package a repeatable task and explain container versus host boundaries.

Study Bash/PowerShell/optional Python selection; REST/authentication/JSON/YAML/CSV; Git/review; configuration/secrets/data; idempotence/dry-run; inventory/backup/health checks; images/containers/volumes/networks; Dockerfile/Compose/logs/cleanup; non-root/rootless options; Swarm services/replicas/secrets/configs/rolling update; Kubernetes Pods/Deployments/Services/ConfigMaps/Secrets/RBAC as a comparison; resources and kernel dependence.

Use approved local API calls with `curl` or `Invoke-RestMethod`. Docker/Compose uses a dedicated lab host, no privileged containers, management sockets, personal directory mounts or public student shells. Advanced Swarm/Kubernetes operations require additional training.

## Laboratories

**L26A · A common data contract.** Environment: three inventory exports and a fictional/local API. Tasks: define minimal fields; normalize OS/version/time/state; validate input; distinguish missing from false; produce a common report. Evidence: schema, conversion and tests. Success: comparable results without inventing values or contacting third parties. Recovery: preserve source exports.

**L26B · Service in Compose.** Environment: a dedicated lab host. Tasks: package the M25 site; declare configuration, ports, resources, identity and health check; start and inspect logs; test restart and intended persistence. Evidence: declarative files, runbook and checks. Success: approved lab exposure only, no secrets in images and no personal mounts. Recovery: stop/remove identified resources without indiscriminate volume deletion.

**L26C · Compare orchestration.** Environment: prepared manifests/output, optionally an instructor-controlled cluster. Tasks: map services/replicas/volumes/networks in Swarm/Kubernetes; explain updates/rollback; review secrets, permissions and storage paths; compare published-port behavior. Evidence: architecture mapping and manifest review. Success: do not assume a Compose file is interchangeable with a Swarm stack or Kubernetes manifest. Recovery: offline work, or remove only the practice stack/namespace.

# M27 · Logs, observability and time correlation

## A timeline depends on its clocks

Preserve original timestamps and time zones when normalizing to UTC. Resolution, clock drift and collection delay may prevent precise ordering. Equal normalized timestamps do not prove simultaneous events. Corrections must remain traceable rather than overwriting original values.

A normalized record is a working representation, not necessarily the complete original event. Collection policy, access, retention, redaction and ingestion failures affect coverage. Missing activity and missing telemetry are different operational conditions that require different responses.

## Outcomes and theory

Prerequisites: M19, M23 and M25. Build a reproducible timeline and state its coverage and quality limits.

Study events/logs/metrics/traces; Linux journal/syslog/audit; Windows Event Log/Sysmon; macOS Unified Log; web/DNS/authentication logs; schemas/providers/fields/severity; UTC/original zones/daylight saving/drift; rotation/retention/integrity; collection permissions; deduplication/correlation; loss/redaction; bounded queries and privacy.

Use `journalctl`, `Get-WinEvent`, `wevtutil`, `log show`, text/JSON parsers and optional instructor-selected collectors. A commercial SIEM is not mandatory. Do not erase logs as a classroom cleanup procedure.

## Laboratories

**L27A · Three systems, one schema.** Environment: synthetic Linux/Windows/macOS events. Tasks: preserve inputs; map original time, UTC, host, source, fictional account, action and result; validate types; mark missing fields. Evidence: dictionary and normalized output. Success: do not invent timestamp precision. Recovery: regenerate from originals.

**L27B · A corroborated timeline.** Environment: a case with different zones, a duplicate and known clock drift. Tasks: order events; deduplicate without losing provenance; calculate drift; distinguish observed/estimated order; corroborate with another source. Evidence: timeline and uncertainty statement. Success: preserve original timestamps and avoid local/UTC confusion. Recovery: retain original and normalized representations.

**L27C · Coverage and retention.** Environment: a lab host and collector. Tasks: generate a benign administrative action; follow ingestion; verify access/retention; examine a prepared collection gap; propose a missing-telemetry alert. Evidence: source/collector/query chain. Success: distinguish no activity from no visibility. Recovery: do not purge logs to trigger the alert.

# M28 · DFIR triage, preservation and analysis

## Preserve the ability to disagree

A defensible investigation lets another analyst repeat the work and test alternative explanations. Record source, acquisition method, tool version, time, permissions, transformations and custody. A matching hash supports byte-level integrity but does not independently prove provenance, authorship or legal admissibility.

Live response necessarily interacts with the system. Prioritize questions and sources, consider volatility and containment, and record the likely impact of each query. Offline analysis protects the original from repeated examination but may lack volatile information. Neither approach justifies collecting every secret or personal profile by default.

## Outcomes and theory

Prerequisites: M09 and M27. Perform proportionate triage and report conclusions supported by evidence.

Study preparation/identification/preservation/acquisition/analysis/reporting; incident-management context; logical/physical acquisition; live/offline methods; volatility/containment decisions; hashing/manifests/custody; evidence permissions; filesystem/timestamp limitations; processes/connections; legitimate autostart/configuration/history; Registry/Event Logs/macOS artifacts; timelines, alternative hypotheses and professional scope.

Use scoped native queries, hashes, bounded log export and approved parsers. Specialized forensic tools are extensions with their own licensing/version checks. No credential extraction or execution of malware is part of this course.

## Laboratories

**L28A · Preserve before analyzing.** Environment: a synthetic case package. Tasks: record receipt/scope; inventory and hash; create a working copy; protect originals; log custodians and transformations. Evidence: receipt record and manifest. Success: repeatable analysis and a precise explanation of each integrity claim. Recovery: replace working copies from originals, never modify originals.

**L28B · A live-response plan.** Environment: a clean VM and simulated incident. Tasks: prioritize questions/sources; estimate query effects; collect only approved version, process, connection and bounded-log information; record errors and permissions. Evidence: plan, activity log and sanitized output. Success: no mass profile/secret collection and no claim of impact-free acquisition. Recovery: preserve outputs before restoring the VM.

**L28C · A defensible report.** Environment: offline evidence containing benign changes and an ambiguous indication. Tasks: build a timeline; correlate files/events; test an alternative hypothesis; separate observation from attribution; identify additional evidence needed. Evidence: technical report and executive summary. Success: proportional, traceable conclusions. Recovery: maintain case custody and retention controls.

# M29 · Threat hunting, indicators and operational intelligence

## An indicator is a lead, not a verdict

Indicators require a type, original value, normalized representation, provenance, confidence, validity period and context. Domain, subdomain, URL and IP comparisons need explicit semantics. A filename or process name may be useful context but is weak evidence without corroboration.

Start a hunt with a question and a statement of visibility. Match within defined fields/time windows and use positive/negative controls. Enrichment can disclose an investigation: do not send internal domains, private URLs or incident artifacts to public APIs without authorization. Intelligence should end in a justified next action, not just a list of matches.

## Outcomes and theory

Prerequisites: M06, M16, M27 and M28. Normalize indicators, perform contextual exact searches and communicate a tested hypothesis.

Study IOC/IOA/TTP; hashes/IP/domains/URLs/paths/processes/services/tasks/configuration keys; confidence/provenance/expiry/false positives; safe offline defanging/refanging; domain semantics; hash algorithms; scoped local searches; YARA/Sigma and backend differences as extensions; ATT&CK behaviors; CTI questions/collection/evaluation/analysis/dissemination; authorized DNS/RDAP/certificate enrichment; JSON/CSV and STIX/TAXII concepts; privacy/egress.

Use format-aware parsers, native searches over copies, hashes, `Select-String` or appropriately bounded literal `grep`. Public API examples require approved public synthetic data; never automatically contact a potentially malicious indicator.

## Laboratories

**L29A · A quality indicator list.** Environment: synthetic values containing duplicates, invalid entries and multiple types. Tasks: validate type/algorithm; normalize while preserving original; distinguish domain/URL; record provenance/confidence/expiry; reject invalid entries. Evidence: JSON/CSV and tests. Success: `not-example.test` is not an exact match for `example.test`. Recovery: preserve the input.

**L29B · Offline matching and false positives.** Environment: synthetic logs/files with known positives. Tasks: specify fields and matching rules; run exact comparisons; confirm context; include negative controls; count false positives/omissions. Evidence: query/script, findings and coverage. Success: no compromise claim from one match alone. Recovery: analyze copies read-only.

**L29C · From finding to decision.** Environment: results from the previous exercise. Tasks: form a behavior hypothesis; relate sources and coverage; consult relevant ATT&CK documentation without forced mappings; propose a verifiable response; state permissible enrichment. Evidence: a one-page intelligence note and detection test. Success: an actionable next step with confidence and limitations. Recovery: no automatic external lookups.

# M30 · Technical audit and Red/Purple perspectives

## Evaluate controls without overstating findings

An excessive permission is an observed condition; exploitation is a different claim requiring evidence. Describe assets, trust relationships, exposure and plausible consequences without presenting hypothetical impact as a demonstrated compromise.

Purple validation aligns an authorized benign action with expected telemetry, a detection and a reversible change. Knowing what an action logs improves accountability; it is not a request to hide the action. Scope, stop conditions and coordination are part of the technical method.

## Outcomes and theory

Prerequisites: M24, M25, M28 and M29. Plan an authorized review, turn a deviation into a defensive test and verify a correction.

Study rules of engagement; local exposure inventory; identity/service/segment trust; executable/configuration permissions and service accounts; exposed-secret risk categories without extraction; legitimate startup mechanisms and abuse auditing; lateral movement/pivoting as conceptual models; expected telemetry/coverage; Red/Blue/Purple coordination; impact/evidence/mitigation/retest; technical and executive communication.

Use previously learned configuration queries, inventories, diagrams, control matrices and prepared events. This course does not provide exploitation, unauthorized lateral access, evasion or covert persistence workflows.

## Laboratories

**L30A · Surface review.** Environment: an owned snapshot with example configurations. Tasks: inventory listeners, privileged accounts, services and access; compare the baseline; choose three deviations; document impact and minimal evidence. Evidence: a precisely scoped report. Success: do not claim demonstrated exploitability from configuration alone. Recovery: query-only review.

**L30B · Benign Purple validation.** Environment: an identifiable approved change, such as a summary task. Tasks: predict telemetry; execute the legitimate administrative action; verify logs/detection; explain gaps; propose an improvement without disabling protection. Evidence: action/control/event/result matrix. Success: repeatable, attributable test activity. Recovery: remove the legitimate task with a record.

**L30C · Correction and retest.** Environment: one finding from L30A. Tasks: design a minimal correction and rollback; obtain approval; apply; verify functionality and intended restriction; communicate residual risk. Evidence: before/after state, negative test and executive summary. Success: demonstrated improvement without exaggerated conclusions. Recovery: retain the approved state or restore the baseline as specified.

## Checkpoint C5

Turn configuration and telemetry into verifiable decisions. Keep administration, investigation and offensive evaluation conceptually separate.

# M31 · Terminal AI and supervised automation

## A proposal is not permission to execute

A model can explain commands, suggest tests, review a script or summarize synthetic logs, but its output requires independent verification. A convincing answer without evidence is not a successful analysis. Keep tools and permissions outside the prompt: a read-only review does not require a shell executor, management socket or credential store.

Treat logs, source comments, retrieved documents and tool output as untrusted data. They may contain text that attempts to redirect an assistant. Minimizing input, validating a structured output schema and obtaining human approval are complementary controls; instructions in a prompt alone are not a reliable security boundary.

## Outcomes and theory

Prerequisites: M12, M16, M21, M28 and M29. Use AI for explanation and review while preserving privacy, testing and human control. This module has 8 theory hours and three four-hour laboratories.

1. Models, context, tokens, inference settings, resource needs and measured performance.
2. CLI, local/remote API and tool-using agents: different capabilities and risks.
3. Local model provenance, licensing, download/update and resource compatibility; local is not automatically secure.
4. Useful bounded tasks: command explanation, script review, synthetic-log summaries, hypotheses and documentation.
5. Minimum context: OS/version/shell, identity, purpose, allowed data and output contract.
6. Structured JSON, schema validation and rejection of unexpected actions or fields.
7. Prompt injection through untrusted logs, comments and retrieved text.
8. Privacy, secret redaction, egress, retention, provider terms and budgets.
9. Tool use, MCP and retrieval-augmented generation as concepts; sources are not automatically authoritative.
10. Separation of proposal, human approval, isolated test and manual operation.
11. Evaluation datasets, correctness, false positives, abstention, cost and latency.
12. Traceability: model/version/settings, sanitized input/output, independent test and final decision.

The safe flow is: synthetic data → minimization → inference without execution tools → structured proposal → validator → human review → isolated test → approved operation. An optional local CLI, such as an instructor-approved model runner, must fit hardware and licensing; there is no mandatory subscription or automatic download. Do not connect model output directly to a shell.

## Laboratories

**L31A · Script reviewer, not executor.** Environment: an approved model and three synthetic scripts with known defects. Tasks: write a human analysis first; request structured review; verify every claim with documentation and tests; identify hallucinations; propose a patch; test only after review in isolation. Evidence: finding/verification/test table, sanitized prompt and diff. Success: no automatic execution of model output and defensible changes. Recovery: revert trial patches, never modify production scripts.

**L31B · Log analyst with boundaries.** Environment: synthetic events with two anomalies and one instruction-like untrusted line. Tasks: define the question; minimize fields; ask for evidence-linked facts and hypotheses; compare deterministic filtering; confirm untrusted text grants no permission. Evidence: reviewed summary, false positives and abstentions. Success: no disclosure, execution or invented attribution. Recovery: apply the agreed retention policy to model context and outputs.

**L31C · An evaluated assisted workflow.** Environment: ten small cases with reference answers. Tasks: define a schema; validate responses; reject invalid format/out-of-scope actions; measure successes, omissions and time; compare manual work; define when not to use AI. Evidence: reproducible evaluation and adoption decision. Success: justified benefit/cost without increased model privilege. Recovery: revoke temporary access and stop local trial services.

## Demonstrate understanding

Explain what left the device, what remains unverified and which task can be completed without AI. The web campus itself does not run an AI model or remote commands.

# M32 · Capstone: operate, protect, investigate and recover

## A system another person can operate

A fictional small organization needs an internal web service, an administration station and Linux, Windows and macOS users. It must inventory assets, manage access, inspect health, recover data and explain unusual activity. Use synthetic identities/data and internal networks only. Declare native coverage accurately: screenshots do not replace hands-on macOS administration.

Deliver an operable system with documented boundaries, not just screenshots. A teammate should reproduce installation and an investigator should repeat analysis from preserved inputs. The capstone has 10 seminar hours and three ten-hour practical phases; these are included in the course total.

## Seminars and scope

Prerequisites: M01–M31 and checkpoints C1–C5. Work in teams of two or three with an individual defense.

Allocate two seminar hours each to architecture/threats, operation/hardening, evidence/response, recovery/communication and technical review. Choose a light static site, local inventory API or status portal. Do not publish it on the Internet or collect real personal information. Docker/Compose is optional packaging; Swarm/Kubernetes are architectural extensions, not hidden graduation requirements.

## Laboratories

**L32A · Construction and operation.** Environment: internal lab networks, a Linux server, Windows client/administrator and a permitted Mac where available; independent log collection or controlled exports. Tasks: define assets, users, data and flows; pin versions; create the repository/runbook; configure the service with least privilege and lab DNS/TLS; automate inventory; compare GUI/CLI; prepare and test backup before incidents. Evidence: diagram, sanitized inventory, access matrix, secret-free configuration, functional checks, reviewed source and at least six tests including invalid input, plus fresh-environment instructions. Success: a teammate reproduces operation, only intended flows are exposed, identities are separate and no credential enters Git. Recovery: verified backup/snapshot and shutdown procedure, with evidence outside restored VMs.

**L32B · Hardening and observability.** Environment: the infrastructure from L32A and approved benign changes. Tasks: assess at least ten baseline controls with evidence/applicability; correct at least three approved deviations; test authorized/unauthorized use; configure minimum log fields/retention; generate normal activity and a documented action such as legitimate account creation or summary scheduling; verify detection and gaps. Evidence: baseline, exceptions, diffs, functional/negative tests, correlated logs, detection hypothesis, rollback and residual risk. Success: explain both observed and unobservable activity, retain protection, availability and recovery. Recovery: remove temporary accounts/tasks with records; do not clear case logs.

**L32C · Investigation, recovery and defense.** Environment: two instructor-selected benign incidents: incorrect permission, stopped service, replaced synthetic file, contextual IOC match, clock drift or ingestion gap; include an alternative benign explanation. Tasks: define triage scope; preserve originals/manifests; build a timeline; search indicators on copies; corroborate/disprove; perform approved recovery; measure duration and loss; prepare reports and demonstrate. Evidence: receipt/custody record, reproducible queries, timeline with zones/uncertainty, technical report, two-page executive summary, verified restoration, tests, AI-use record and individual defense. Success: traceable proportional conclusions and repeatable analysis; service and permissions work after recovery. Recovery: close access, apply retention and remove resources only after evaluation.

## Project rubric

| Dimension | Points | Required evidence |
|---|---:|---|
| Architecture and reproducibility | 15 | Versions, flows, installation and limitations |
| Three-system administration | 15 | Consistent GUI/CLI and declared native coverage |
| Scripting quality | 15 | Contracts, errors, safety, tests and review |
| Hardening and secrets | 15 | Least privilege, baseline and verified exceptions |
| Observability and detection | 10 | Sources, intervals, correlation and coverage |
| DFIR interpretation | 15 | Originals, hashes, custody and proportional conclusions |
| Recovery | 10 | Demonstrated restoration, measured time and loss |
| Communication and AI use | 5 | Clear individual defense and independent verification |
| Total | 100 | No unresolved critical requirement |

Pass proposal: at least 70/100, satisfactory individual defense and all critical conditions met. A platform without native evaluation remains explicitly pending rather than receiving a full cross-platform credential.

## Critical conditions and individual defense

Do not expose the lab, commit secrets/real personal data, destroy originals, act outside scope, disable essential protection without an approved legitimate procedure, invent test results or make AI the sole executor/verifier. A critical failure requires remediation and a repeat of the affected assessment regardless of the arithmetic score.

The instructor asks for a small unannounced change on synthetic data, an explanation of access, a log interpretation and a partial restoration. Each learner explains a component they did not build alone. Manuals are permitted: reasoning, verification and recovery matter more than memorizing flags.
