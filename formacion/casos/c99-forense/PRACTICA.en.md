# C99-DFIR · Investigate before executing

[Case index](README.md) · [Spanish guide](PRACTICA.md) · [Sources and provenance](FUENTES.md)

## Brief, scope and learning outcomes

You are investigating an unexpected upload-directory file on the fictional host web-01. Every record under evidencias/ is synthetic classroom material, not victim telemetry. Do not contact the real sample's receiver, deploy C99, access third-party systems or publish student information. The real sample is referenced through its existing static analysis, not shipped as executable code in this exercise.

The canonical sample SHA-256 in that analysis is `1e07598c2e41b7827840ba6c8611912abd88c0344a5d1eff364eaabeccdc6420`. This is not the hash of the JSON scenario or the inert inventory cards. The sample header and internal dossier dates are claims that require provenance, not verified acquisition times or attribution.

You will demonstrate evidence preservation, controlled use of a legitimate shell, candidate discovery, static source-to-sink reasoning, timeline normalization, multi-source correlation, detection design, reversible response and proportionate reporting. Prerequisites are basic files, permissions, processes, HTTP, DNS, JSON and hashes. Suggested roles are evidence custodian, analyst, incident lead and reviewer.

## Shell concepts

A terminal is an input/output interface. A local shell interprets commands with its process identity and permissions. SSH is an authenticated transport that can provide a shell or other functions. A webshell is server-side functionality exposed through web requests; it does not automatically imply root. Bind and reverse describe connection direction, not proof of data theft. MITRE's relevant webshell classification is T1505.003 [S1].

The hands-on session uses a legitimate /bin/sh inside the provided container. C99 capabilities are examined as evidence, not activated. The lab is not a general-purpose malware sandbox.

## A01 · Preserve before inspection

From the case directory create a separate workspace and record UTC time, Python version and the repository commit. Generate and verify a local content baseline:

```sh
umask 077
mkdir -p trabajo
{ date -u; python3 --version; git rev-parse HEAD; } > trabajo/entorno.txt
python3 herramientas/forense.py manifest evidencias > trabajo/manifest.json
python3 herramientas/forense.py verify evidencias trabajo/manifest.json
```

Copy the evidence directory into a separate test directory. Modify only security-notes.txt in that copy and verify it against the original manifest. Expect a mismatch and exit code 1; the original must still verify. A locally generated manifest does not authenticate an earlier acquisition. A matching hash proves neither safety nor authorship. Preserve command outputs and custody records; do not publish them to GitHub.

Deliver: manifest, commit, custody table and positive/negative results. The helper reads bytes and rejects symlinks/non-regular files within its bounded scope. It is not an acquisition agent for a live hostile filesystem.

## A02 · Use a real shell in the classroom container

Build and open the optional shell using compose.laboratorio.yaml. Building can download the base image; runtime has network_mode none, a read-only root, an unprivileged user and no host/socket mounts. Record the built image ID; BASE_IMAGE may be set to an approved digest because a tag is mutable.

```sh
docker compose -f compose.laboratorio.yaml build
docker compose -f compose.laboratorio.yaml run --rm --no-deps --entrypoint /bin/sh lab
```

Inside the container run id, pwd, `printf 'shell=%s pid=%s\n' "$0" "$$"`, ls on /lab/evidencias/webroot and read /etc/os-release. Explain that the resulting identity belongs to the container, not fictional web-01. Reading /proc/self/status through cat describes the reader process, not necessarily the interactive shell.

```sh
python3 -c 'import os,socket; print("uid",os.getuid()); print("interfaces",socket.if_nameindex())'
if touch /lab/evidencias/NO-DEBE-CREARSE 2>/dev/null; then
  printf 'FAIL: evidence is writable\n'
else
  printf 'PASS: write denied\n'
fi
```

No network probe is required. Observe the actual output rather than claiming that YAML configuration proves runtime isolation. Temporary notes under /tmp disappear when the container is removed; retain terminal output beforehand. Deliver a command/context/result/limitation table. Exit to finish the ephemeral session. Do not attempt container escape or privilege escalation.

## A03 · Discover candidates without execution

The .txt files in evidencias/webroot are inert inventory cards, not PHP. cache.php.txt represents the suspicious fictional path; health.php.txt represents an approved health check. security-notes.txt mentions detection terms as documentation and is a negative control.

```sh
find evidencias/webroot -type f -print
grep -RInE 'c99shcook|curl_exec|goto|eval' evidencias/webroot
```

Prioritize using declared original path, ownership, approved change, content and possible operation. Do not equate a keyword, filename, extension or Base64 with compromise. Deliver a candidate table including a plausible benign alternative. Do not modify evidence.

## A04 · Follow the static evidence

The existing C99 analysis identifies QpRos and z2KH7 as preparation of scheme + HTTP_HOST + REQUEST_URI inside the url field, followed by Q7vOx/SXetq for the hardcoded cURL destination. The initial uT50x/gJmPl upload branch precedes normal authentication and exits before that callback. nDYHe imports untrusted request configuration through c99shcook. The callback response is not evaluated as PHP in that block; the conditional updater is separate. Certain write paths can restore earlier timestamps.

Draw source → transformation → operation → access condition. Physical file order is not execution order in goto-obfuscated code. Keep original labels and do not claim equivalence after deleting jumps. The real destination is represented as `hxxps://svgflow[.]digital/sz/log.php` for evidence only. The scenario's collector.training.invalid is fictional, not a new IOC or live DNS observation.

Deliver an annotated startup flow and three claims with confidence/limits. A reachable call does not prove successful delivery or execution on a victim.

## A05 · Understand obfuscation without evaluating it

Recognize hexadecimal/octal escapes, opaque identifiers, minification and reordered blocks. In a double-quoted PHP literal, `\x68\164` represents ht; single quotes have different rules [S2]. String decoding does not resolve dynamic calls or the entire control-flow graph.

The sample's header does not authenticate its author, exact obfuscator or acquisition date. A publishing account does not prove ownership of the receiver. Review the previous analyzer's comment-boundary and truncated-literal defects in PR #12; passing earlier tests does not establish universal parser correctness. PHP line comments end at a line or PHP-block boundary, whichever comes first [S3]. Do not execute PHP to perform this exercise.

Deliver a transformation glossary and a parser negative case. Record the commit of any analyzer used. The new manifest/timeline helper does not import the earlier reduced PHP lexer.

## A06 · Build a timeline

The scenario is a normalized teaching schema, not a native auditd or EDR export. Each event has an ID, zoned timestamp, host, source, kind and details.

```sh
python3 herramientas/forense.py timeline evidencias/escenario.json > trabajo/timeline.json
```

Compare time_original and time_utc. E04 and E05 represent the same second in different zones. Sorting by ID only makes ties deterministic; it does not prove causation. Independently sort five records and identify the intentionally out-of-order record. No unmeasured clock corrections are invented.

E10's Unix-like metadata uses ctime for inode status change, not birth time [S4]. These fictional timestamps are distinct from the checkout times on your own computer. Deliver a sourced timeline with equal timestamps and missing coverage explicitly marked.

## A07 · Correlate instead of guessing

Correlate the upload response, file write, HTTP request, child process, DNS query and egress decision using request/process identifiers and paths where available. Temporal proximity and an IP address do not identify a person.

DNS followed by a denied TCP/443 flow does not prove a delivered HTTP POST. DNS or SNI alone does not reveal the request path or body. A later 401 does not prove that no pre-authentication logic ran. E09 has a different SSH parent, identity and authorized ticket; shell execution alone is not a malicious verdict.

Deliver three hypotheses, supporting/opposing evidence and the next observation required. E07 supports a denied attempt for the recorded synthetic flow, not exfiltration. Activity outside the dataset remains unknown.

## A08 · Separate indicators and test detections

Keep real-sample IOC, fictional exercise names and shared infrastructure context separate. Do not export collector.training.invalid as production threat intelligence, or treat review time as first_seen. Historical shared-CDN addresses must not become automatic blocklists.

Specify two multi-source detections: an unexpected upload-directory file followed by a shell child of a web process, and a query to a name of interest followed by egress activity. State fields, window, coverage, retention, missing-data behavior and false positives. Use E02/E09/security-notes.txt as negative controls.

Deliver a rule specification and positive/negative matrix. Writing YARA/Suricata/Sigma syntax is not engine validation; record actual engine/backend versions and results before making that claim. Python helper tests do not validate those products.

## A09 · Contain and recover

Choose a limited, authorized and reversible response while preserving evidence and administration. The scenario disables an affected route, retains egress denial and restores known content. A working home page or 404 is not proof of eradication.

Record approver, expected effect, possible impact, validation and rollback. Consider upload interpretation, permissions, potentially exposed secrets and temporal scope. Do not delete logs or invoke a webshell's self-removal as a response plan. Deliver a decision record and functional/security acceptance plan. No real third-party server is changed.

## A10 · Report and defend

Use INFORME.md as the report structure: executive summary; scope/authorization; custody; reproducible methods; timeline; claims with evidence and alternatives; indicators/detections; response and residual risk. Label synthetic, static-sample and local-container observations separately.

Defend why the file was prioritized, which shell you actually used, what URI data could be exposed, what would establish delivery, and why hashes/timestamps do not establish authorship. Consult DOCENTE.md only after your first attempt. It provides the solution key and a 100-point rubric: preservation 20, discovery/shell context 15, static reasoning 20, correlation 20, response/detection 15, communication 10. The twelve Spanish self-check questions are public formative material, not a private exam.

This supplementary case does not add hours, module IDs or completion milestones to the existing course. Source semantics, synthetic scenario design and actual validation results remain separate.
