# Acceptance scope / Alcance de aceptación · 2.3

## Distinct layers

1. **Python unit tests:** compiler, translation parity, local delivery, release manifest, provenance and design-token calculations.
2. **JavaScript unit/model tests:** validation, state/navigation, explicit interface translations, AES-GCM snapshots and merge behavior. `app-model.test.mjs` uses a minimal in-memory DOM adapter: it is not browser rendering.
3. **Browser acceptance:** `browser_bilingual.py` runs actual Playwright Chromium and WebKit. Twenty test methods include repeated checks across languages, 32 modules/three views, all references and multiple viewport sizes. Counts of test methods and internal scenarios must not be conflated.
4. **Existing regression suites:** the kit and curriculum planning remain separate.
5. **Cloudflare local acceptance:** the dedicated workflow builds the static release, checks Wrangler configuration/dry-run and serves through a local runtime. It does not publish to an account.

## Current implementation

Acceptance belongs to an exact commit and environment. Consult the completed GitHub Actions run for the current release; previous repository runs remain historical evidence only. The migration preserves the existing Python, JavaScript, browser, kit and planning suites. The existence of this file is not a test result.

Screenshots and logs are retained separately under `campus/qa/`, including failures. The Pages package and source snapshot are uploaded only after the complete campus job succeeds. Generated QA files are ignored and do not invalidate provenance of clean source inputs. A modified/unidentified checkout is reported as `sourceCommit: null`, not assigned an unrelated CI SHA.

## Responsive and privacy cases

Widths 320, 360, 390, 768, 820, 1024 and 1440 px cover home, index, theory, guided practice, progress and sharing in both languages. Tests check global overflow, mobile menu, language/state continuity, presentation keyboard, no-JavaScript reading, JSON confirmation and a cross-profile progress link. Transfer must require confirmation and exclude notes. Keep raw saved state for recovery when invalid; never silently reset and overwrite it.

## Limits

This does not certify WCAG conformance, human translation perfection, every physical iPad/Safari configuration, account deployment, OTP login, cloud synchronization or execution of the 96 native labs. Check a physical phone/tablet and the real provider URL before a cohort. Progress is self-reported. No secrets, real learner data or production systems are used by the tests.

## Reproduce

See [EDICION.md](EDICION.md) for commands, [DESIGN.md](DESIGN.md) for design constraints and [DEPLOY-CLOUDFLARE.md](DEPLOY-CLOUDFLARE.md) for provider acceptance. For each release record commit, workflow run, Python/Node/browser versions, outcomes, artifact SHA-256 and unresolved limitations in the PR or release record.
