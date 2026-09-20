# Curriculum expansion master plan — English overview

[Main index in Spanish](README.md) · [Curriculum map](01-mapa-curricular.md) · [Next implementation steps](08-continuacion.md) · [Primary sources](09-fuentes.md)

**Owner: Wiktor Nykiel. Reference edition: 1.0, 18 September 2026.**

## Scope and status

This is a durable planning reference for extending the existing course from genuine computing fundamentals to system administration, architecture, cybersecurity operations and risk governance. It defines **18 areas and 108 proposed units**, together with learning outcomes, laboratory designs, a risk example, partial control mappings and bilingual terminology.

The reviewed baseline is **Campus 2.2**, commit `2f8b8d2614638d9a034e1cac92fb16c6e75bb6c5`. Its existing 32 modules, 96 laboratory designs and 480 planned hours remain unchanged. The proposed units overlap with and extend that baseline; their hours are not added automatically. Existing module IDs and learner progress must be preserved.

**This overview is not a full English translation of the course.** Complete Spanish/English lessons, assessments, interface strings and guided activities remain an implementation requirement. The new plan is not yet a new runtime catalogue in the static campus.

## Learning progression

| Area | Subject | Expected result |
|---|---|---|
| A01 | Computing fundamentals | Explain data representation, hardware, software and basic troubleshooting |
| A02 | Cross-platform terminal and automation | Use Bash/zsh, CMD/BAT and PowerShell with explicit input/output and error contracts |
| A03 | Operating systems and administration | Manage identities, permissions, processes, services, configuration and recovery |
| A04 | Networking | Diagnose communication by layer and justify permitted traffic flows |
| A05 | Virtualization, storage and backup | Operate an isolated, recoverable lab using the available licensed hypervisor |
| A06 | Web, application and data architecture | Explain a request path and evolve a design without unnecessary complexity |
| A07 | Cloud and infrastructure as code | Compare responsibility, identity, cost and operational requirements across providers |
| A08 | Containers and orchestration | Distinguish Docker, Compose, Swarm and Kubernetes responsibilities |
| A09 | Cybersecurity and threats | Distinguish assets, threats, vulnerabilities, events, incidents and risk |
| A10 | Protection capabilities | Select and verify controls for a specific scenario rather than by product popularity |
| A11 | Governance, NIST functions and teams | Connect desired outcomes with owners, evidence, decisions and metrics |
| A12 | GRC, risk and control mapping | Assess and treat risks with explicit assumptions and partial mappings |
| A13 | AppSec and authorized assessment | Review application controls and verify remediation in a private lab |
| A14 | Blue Team, incident response and DFIR | Triage, preserve evidence, choose proportionate containment and recover |
| A15 | CTI and hunting | Answer intelligence questions with provenance, confidence and tested searches |
| A16 | Resilience and wider risks | Address physical, human, supplier and correlated service failures |
| A17 | Supervised AI and privacy | Use AI to explain or review without delegating authority or exposing sensitive data |
| A18 | Capstone and professional practice | Deliver an operable solution, defend its decisions and disclose its limits |

Each area contains six proposed units. The Spanish curriculum map supplies their stable identifiers, prerequisites, objectives, theory topics and practice outcomes. Every future lesson must include a worked example, a guided task, positive and negative checks, evidence, recovery, common mistakes, assessment and versioned sources.

## Architecture cases

The plan uses eight patterns: static website; single-server WordPress; separate application and database tiers; multiple application instances; modular enterprise application; containerized service; managed/serverless service; and hybrid or multi-region design. More components are not automatically better. Students document requirements, traffic, identities, data, failure points, costs and rollback in architecture decision records.

VirtualBox, VMware product families and Proxmox are treated distinctly. Hardware, guest operating-system rights and product licensing must be checked before preparing a cohort. Containers do not replace native operating-system labs or recovery of persistent data.

## Governance and evidence

The NIST section covers the six CSF functions and 22 categories through educational examples. It links operations to roles such as system administration, IAM, architecture, AppSec, SOC, CSIRT, DFIR, CTI, GRC, business continuity and privacy. The role assignments are teaching models, not an official organizational structure or role certification.

The control section contains **12 partial mapping families** between CSF outcomes, GDPR starting points, ISO 27001 topics and ENS areas. The mappings are explicitly not automatic equivalences. Exact ISO references require an authorized text or a clearly identified informative reference; they have not been fabricated to fill gaps. Technical controls do not establish lawful purpose, transparency, data-subject rights or every other privacy obligation.

## Worked risk example

All figures are synthetic. A baseline frequency of 0.40 events/year and average loss of EUR 120,000/event gives an illustrative annualized expected loss of EUR 48,000. Current controls yield EUR 32,400 under the stated assumptions; the proposed target yields EUR 13,440.

The incremental benefit of the new treatment is therefore EUR 18,960/year compared with the current state, not the entire baseline-to-target difference. With an additional annual-equivalent cost of EUR 12,000, the illustrative net expected benefit is EUR 6,960. These figures are not a guaranteed return or evidence of a vendor's effectiveness. The document distinguishes frequency from probability, sensitivity bounds from confidence intervals, and corporate losses from harm to people.

## Laboratories and safe assessment

The reference defines **24 laboratory scenarios**, not 24 additional completed executions. The integrated DVWA/Juice Shop case covers environment identification, normal application behavior, source review, prepared synthetic evidence, control improvement, detection, incident handling and recovery. Vulnerable applications are never deployed with the public campus. No exploitation payloads, credential extraction, evasion or operational lateral-intrusion chains are supplied.

The ambiguous term in the original request, “juicybox”, is provisionally interpreted as OWASP Juice Shop and recorded as an assumption rather than silently renamed.

## Learner experience and cross-device continuity

The roadmap requires a light, independent editorial identity with readable structure, accessible navigation and responsive layouts for phones, tablets and laptops. No institution's name, logo or affiliation is included. Device checks must distinguish viewport simulations from native Safari/iPadOS validation.

Three capabilities remain separate: sharing a lesson link, transferring a progress snapshot, and authenticating/synchronizing an account. A lesson URL must not carry persistent authentication tokens. The existing validated file export/import remains a fallback. Any future transfer link requires minimum data, a short-lived reference, explicit confirmation and protection against message-preview consumption.

Optional email OTP requires a proper identity component, rate and retry limits, one-time expiry, session security, per-user authorization and a privacy/retention design. It is not implemented by this planning document and must not be represented as current functionality.

## Next delivery

Read the current repository first. Develop A01/A02 in full Spanish and English, reusing existing material and preserving IDs/progress. Then expand networking, virtualization, web/cloud and orchestration before deepening governance, risk, operations and specialist routes. Update the machine-readable plan, sources and actual test status at every delivery. The continuation instructions are saved in `08-continuacion.md` so requirements need not be reconstructed from chat history.
