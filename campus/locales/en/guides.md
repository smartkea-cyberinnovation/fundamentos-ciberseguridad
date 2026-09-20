# L05A · R01: directories, names, bytes and verification

## Preparation

Three hours; prerequisites M01–M04. Read the terminal lesson and the reference kit instructions. Work from `formacion/sistemas-operativos/` under a standard account. Create a new synthetic workspace, never a personal directory:

```bash
python3 kit/oslab.py init mi-laboratorio
```

Use the approved Windows interpreter, such as `py -3`, when appropriate. The instructor may provide a pre-generated workspace. Do not silently reuse or overwrite an existing one.

## Guided sequence

1. Open `datos` in the file manager. Count visible items, then show hidden files without changing attributes.
2. Compare `ls -la mi-laboratorio/datos` and `wc -c mi-laboratorio/datos/hola.txt` on Linux/macOS. On PowerShell use `Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force` and inspect `Length`; on CMD use `dir /a mi-laboratorio\datos`.
3. Read a file with spaces using a quoted path and explain the number of arguments the utility receives.
4. Compare `lineas-lf.txt` and `lineas-crlf.txt` without editing. Explain their respective eight and ten bytes.
5. Run `python3 kit/oslab.py manifest mi-laboratorio`. This specific reference dataset contains eight files and 62 bytes. Verify using another tool. Allocated disk blocks measure something different.
6. Copy `hola.txt` into `salida/copia.txt` using the GUI, then compare its content from the terminal. The manifest only counts `datos`, so the output copy does not increase its total.

## Boundary cases and submission

Test a nonexistent path and immediately record the exit status. Explain why elevation does not repair a misspelled name. Change only the output copy and demonstrate that its hash changes while the original remains intact. Do not practise recursive deletion.

Submit a file/bytes/hash/observation table, minimal GUI/CLI evidence, an explanation of why `.nota.txt` counts and an original/copy comparison. Distinguish content, names, metadata and allocation.

## Recovery and validation scope

Retain the original dataset; remove only the identified output copy after assessment. Explain rather than hide disagreements between tools. Linux reference-kit tests do not establish that each learner's native Windows/macOS GUI and CLI were executed; record their actual environments and results.

# L11A · R02: a Bash script you can defend

## Preparation and contract

Three hours; M06 and M08; Linux Bash and synthetic data, without administrative privilege. Read `kit/resumen.bash`. Identify its parameter, workspace marker validation, nonrecursive scope, expansion, output and failure code. Predict the result before running it.

## Guided sequence

1. Run `bash -n kit/resumen.bash` and explain what syntax checking cannot verify.
2. Run `bash kit/resumen.bash mi-laboratorio`. Expected reference output is `{"count":8,"total_bytes":62}`.
3. Repeat with a newly generated workspace whose name contains spaces. Quote variable expansions; do not insert literal quotes into the path value itself.
4. Run with a missing argument and an invalid directory. Capture `$?` immediately. An invalid input must produce an error, not a successful zero-file report.
5. Compare with `python3 kit/oslab.py manifest mi-laboratorio`. Explain the additional functionality and limits of each implementation.

## Independent improvement

Copy the script to `mi-laboratorio/salida/resumen-alumno.bash`. Add help and two tests. Retain the baseline result and expected failure behavior. Do not introduce arbitrary command evaluation, broad recursion or administrative access.

Submit the contract, diff, outputs and hidden-file explanation. Explain unmatched-glob behavior. More advanced topics include bounded size, locking and error handling; do not claim the small sample already implements all of them.

## Recovery

Remove only the learner's copy after submission. Retain kit source and original dataset. Review every generated code change before execution.

# L16A · R03: CMD, BAT and PowerShell on one problem

## Native prerequisites

Three hours; M13–M15. Use a real Windows environment and an approved interpreter; a Linux container cannot validate Windows behavior. Record edition/build, `$PSVersionTable`, working directory and account. Prepare the workspace with approved Python or receive it from the instructor. Keep existing execution policies; follow the instructor's legitimate procedure when a policy blocks a file.

## Guided sequence

1. In CMD read `kit\resumen.cmd` using `type`, explain expansion and `errorlevel`, then run `kit\resumen.cmd mi-laboratorio`. Expected count-only output: `{"count":8}`.
2. In PowerShell inspect `Get-ChildItem -LiteralPath .\mi-laboratorio\datos -Force | Get-Member`. Explain the type and `Length` property.
3. Run the reviewed file with its approved engine: `powershell.exe -NoProfile -File kit\Resumen.ps1 -Workspace mi-laboratorio`, or the intended `pwsh` variant. Expect count eight and bytes 62. Record which engine was actually used.
4. Select `Name`, `Length` and `Attributes`; export only those properties to a new output file. Do not insert `Format-Table` before data export.
5. In a trial copy test an absent workspace and invalid marker. Distinguish running a script, emitted JSON and process exit status.

## Analysis and evidence

BAT's name-list parsing has encoding, filename and enumeration-error limits. Document them rather than hiding them. Explain which task should migrate to PowerShell. This file-count example does not validate Registry, events, services or domain administration.

Submit both outputs, a text/object comparison and a negative case. Remove only disposable exports. The script/design exist; native results require a Windows-specific test record and are not implied by web-campus tests.

# L21A · R04: macOS, zsh and portability limits

## Guided sequence

Three hours; M11 and M20; a permitted Mac. Use fictional files, not personal preferences or profiles.

1. Record `sw_vers`, `uname -m`, `zsh --version` and the available Python version; identify OS, architecture, shell and language separately.
2. Open the workspace in Finder and Terminal, show hidden files and locate `.nota.txt`.
3. Read `kit/resumen.zsh`. Explain `emulate -L zsh`, local options and glob qualifiers for hidden files and no matches.
4. Run `zsh -n kit/resumen.zsh` and then `zsh kit/resumen.zsh mi-laboratorio`. Expect eight files and 62 bytes; syntax checking and execution are different evidence.
5. Compare `python3 kit/oslab.py manifest mi-laboratorio`. Inspect a synthetic file with `ls -le@` and distinguish content, permissions and attributes.
6. Review the Bash script without executing it under zsh. Explain why changing the interpreter is not a port. Read local `stat` help and compare GNU/Linux syntax.

## Variants and reflection

Create a new workspace with spaces. Test missing arguments and an incorrect marker in a copy. Describe what environment and absolute paths a launchd task would need; this portability exercise does not install a background agent.

Submit a compatibility matrix and expected/observed results. Reading APFS/TCC documentation does not replace their native exercises. Do not grant Full Disk Access to count the learner's own files.

## Recovery and limits

Keep platform protection, Keychain and boot volumes unchanged. Remove only trial copies after assessment. The instructor records actual macOS/zsh versions and results; Linux or browser checks do not establish native execution.

# L27B · R05: a timeline and exact matching on synthetic evidence

## Preparation

Three hours; reinforces M28–M29 without adding course hours. The reference kit contains eight synthetic events, not original EVTX, journal or Unified Log acquisitions. Hash `eventos.json` with the platform's native tool and record source and time zone. Do not use business logs.

## Guided sequence

1. Run `python3 kit/oslab.py timeline mi-laboratorio`. Expect E01–E08 in time order. E01 retains `2026-09-14T10:00:00+02:00` and normalizes to `2026-09-14T08:00:00+00:00`.
2. Locate `source_index` and `original`. Explain their value for repeatability.
3. Run `python3 kit/oslab.py match mi-laboratorio`. Expect four matches: E02/domain, E02/ip, E04/sha256 and E08/domain.
4. Verify that lookalikes in E03 and the subdomain in E07 do not match. This kit's contract is exact identity, not substring matching or automatic inclusion of subdomains.
5. Confirm the input hash remains unchanged. This verifies observed content integrity, not complete custody of a real investigation.

## Negative cases

Copy the workspace to a new directory. Remove a timestamp's zone or repeat an event ID in the copy. The tool should reject the input rather than invent UTC or silently remove duplicates. Record the failure and restore only the copy.

## Interpretation and recovery

Four matches are not four incidents: they occur in three events. E04's hash belongs to harmless `hola.txt`. Do not connect to the example indicators. Present a hypothesis, a benign alternative and an additional check without attributing an actor or confirmed compromise.

Submit manifest, timeline, matching output, negative controls and coverage. Preserve originals and remove the copy after evaluation. This lab does not establish physical acquisition, memory analysis, native EVTX analysis or a complete expert investigation.

# L25A · R06: operate and observe a local web service

## Scope

Three hours; M24 and preparation for M25. This is a teaching-only HTTP service without authentication/TLS, personal data or external publication. It is not a production server.

## Without Docker

1. From the course directory run `python3 kit/web.py`. Default listener: `127.0.0.1:8080`.
2. Open the page and request the health endpoint: `curl --fail --silent --show-error http://127.0.0.1:8080/healthz`. On Windows use `curl.exe` to avoid alias ambiguity.
3. Verify `{"status":"ok","synthetic":true}` and inspect headers with `curl -I http://127.0.0.1:8080/healthz`.
4. Request `http://127.0.0.1:8080/no-existe`; expect 404 and explain why connectivity still exists.
5. Correlate terminal JSON logs with status/response. Check that they exclude query strings and client data.
6. Run `python3 -m unittest discover -s kit -p test_web.py -v`. Tests manage their own separate local server.

## Optional container comparison

On a dedicated Docker lab host, inspect the kit's Compose instructions, host port 18080 versus container port 8080, user, read-only filesystem, internal network and health check. Validate with `docker compose config` before approved execution. Do not add host administration sockets or privileged mode.

Review `swarm.yaml`: a previously distributed image and no published ports. Explain an authorized overlay-network client and removal of only the practice stack. Do not invent an image digest or initialize a production cluster for this exercise. Native container execution requires its own evidence.

## Submission and shutdown

Submit status/headers/body/logs for 200 and 404, port diagram, health-check meaning and residual risk. Stop the manual server with Ctrl+C and confirm it no longer responds. For an approved Compose run, stop only that project without removing unrelated resources. Local HTTP tests do not establish Docker/Swarm or TLS validation.

# L30C · R07: a minimal, verified and reversible change

## Scope and Linux variant

Three hours; M30. Use a fictional file in `salida`, not live service configuration. Copy `mi-laboratorio/datos/hola.txt` to `mi-laboratorio/salida/config.txt`, check the path and ownership and record the initial mode.

```bash
modo_inicial=$(stat -c '%a' mi-laboratorio/salida/config.txt)
printf 'Observed mode: %s\n' "$modo_inicial"
chmod 600 mi-laboratorio/salida/config.txt
stat -c '%a %U %G' mi-laboratorio/salida/config.txt
chmod "$modo_inicial" mi-laboratorio/salida/config.txt
stat -c '%a' mi-laboratorio/salida/config.txt
```

No elevation is needed for the learner's own file. Do not copy GNU `stat` options to macOS without local help. Confirm unchanged content and restoration of the actual initial mode, not an assumed 644.

## Windows/macOS and negative checks

On Windows record the test file ACL using `Get-Acl`, inspect inheritance in the GUI and propose the minimum change. Apply/restore only under instructor approval with practice identities. On macOS distinguish Unix permissions, ACLs and privacy controls; use native `stat` syntax. No variant changes global policy.

Use a second fictional account supplied by the instructor for allowed/denied tests. With only one account, declare the negative test unexecuted; reading an ACL alone does not demonstrate effective denial.

## Expected evidence and recovery

Submit a ticket with initial state, objective, impact, approval, prior copy, change, functional/negative test or explicit pending status, rollback and residual risk. One file permission does not justify claiming that the entire machine is hardened or certified.

Restore and compare content/permissions, then remove only the practice copy. Native identity/policy tests require separate instructor validation.

# L31B · R08: valid structure is not a true conclusion

## Preparation

Four hours; M31 and R05. No provider, subscription or model is required: `respuesta-ia.json` is simulated model output. Review the eight synthetic events and treat E06 as untrusted data. Use a copy when editing. The kit neither runs model calls nor executes returned instructions.

## Guided sequence

1. Read the sample and run `python3 kit/oslab.py review mi-laboratorio`. Expect `structurally_valid: true`, `semantically_verified: false` and `requires_human_review: true`.
2. In a copy add an unsupported top-level `actions` field; validation should fail and its contents must not run.
3. Restore the sample and change a reference to `E999`; validation should fail on an unknown reference.
4. Restore valid structure and write a conclusion citing E02 but claiming that it alone proves a compromise. Structural validation may pass; the learner must reject the unsupported conclusion.
5. Produce a corrected observation, hypothesis, alternative and next check. Verify every reference manually.

## Optional approved CLI

An instructor may obtain another response using an approved local/remote tool with synthetic data only. Record model, version/settings, destination, inputs and verification. Review resources/license before downloading a model and provide no execution capability. The kit does not verify provider permissions.

## Assessment and closure

Submit three cases: unsupported field, unknown reference and unsupported inference. Explain which the program detects and which requires judgment. Valid JSON alone does not earn a pass. Preserve only permitted synthetic responses and revoke temporary tool access. This bounded exercise demonstrates controls and limits; it is not a general prompt-injection resistance certification.
