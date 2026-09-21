# Acceptance scope / Alcance de aceptación · 2.4

## Distinct layers

1. **Python unit tests:** compiler, translation parity, local delivery, release manifest, provenance and design-token calculations. Operational-reading tests additionally check stable IDs, links, hours, translated coverage, control/rule/lab identifiers and failure when translation is absent.
2. **JavaScript unit/model tests:** validation, state/navigation, explicit interface translations, AES-GCM snapshots and merge behavior. `app-model.test.mjs` uses a minimal in-memory DOM adapter: it is not browser rendering.
3. **Browser acceptance:** `browser_bilingual.py` runs actual Playwright Chromium and WebKit. Twenty test methods include repeated checks across languages, 32 modules/three views, all references and multiple viewport sizes. `browser_operations.py` adds five methods per engine for D22–D25, contextual links, six viewport widths, retained core progress and no-JavaScript reading. Counts of test methods and internal scenarios must not be conflated.
4. **Existing regression suites:** the kit and curriculum planning remain separate.
5. **Cloudflare local acceptance:** the dedicated workflow builds the static release, checks Wrangler configuration/dry-run and serves through a local runtime. It checks stable resource IDs and the package version rather than a stale hardcoded release. It does not publish to an account.
6. **Public HTTP observation:** `audit_publication.py` performs seven fixed public GETs, without credentials or following redirects. Its dated report includes status, MIME, selected security headers, content hashes and allowlisted public build identifiers. Passing this observation does not prove all browser functions, native labs or cloud account settings.

## Current implementation

Acceptance belongs to an exact commit and environment. Consult the completed GitHub Actions run for the current release; previous repository runs remain historical evidence only. The migration preserves the existing Python, JavaScript, browser, kit and planning suites. The existence of this file is not a test result.

Screenshots and logs are retained separately under `campus/qa/`, including failures. The Pages package and source snapshot are uploaded only after the complete campus job succeeds. Generated QA files are ignored and do not invalidate provenance of clean source inputs. A modified/unidentified checkout is reported as `sourceCommit: null`, not assigned an unrelated CI SHA.

The first live observation on 21 September 2026 identified release 2.3.0 at commit `beae889a580b3bd36864eb19bb05760d232ff805`. This is a baseline observation before D22–D25, not evidence that the new readings are already in production. Compare subsequent public build-info and catalogues with the integrated commit before claiming publication.

## Responsive and privacy cases

Widths 320, 360, 390, 768, 820, 1024 and 1440 px cover home, index, theory, guided practice, progress and sharing in both languages. Tests check global overflow, mobile menu, language/state continuity, presentation keyboard, no-JavaScript reading, JSON confirmation and a cross-profile progress link. Transfer must require confirmation and exclude notes. Keep raw saved state for recovery when invalid; never silently reset and overwrite it.

The operational suite captures D24 at 320, 390, 768, 820, 1024 and 1440 px in both languages and browser engines. Reading a table with internal horizontal scrolling is distinct from overflow of the whole document. Screenshots are reviewed as release evidence, not asserted because a capture command exists.

## Limits

This does not certify WCAG conformance, human translation perfection, every physical iPad/Safari configuration, account deployment, OTP login, cloud synchronization or execution of the 96 native labs. Check a physical phone/tablet and the real provider URL before a cohort. Progress is self-reported. No secrets, real learner data or production systems are used by the laboratory tests. The separate publication check observes the public campus without altering it.

The twelve OPS-L designs, sixteen OS controls and eight NAV rules are teaching material, not controls configured on students' devices. No LDAP/AD changes, browsing blocks, TLS interception, private-message access or native Windows/macOS configuration is performed by adding these readings.

## Reproduce

See [EDICION.md](EDICION.md) for commands, [DESIGN.md](DESIGN.md) for design constraints and [DEPLOY-CLOUDFLARE.md](DEPLOY-CLOUDFLARE.md) for provider acceptance. For each release record commit, workflow run, Python/Node/browser versions, outcomes, artifact SHA-256 and unresolved limitations in the PR or release record.
