# Cloudflare deployment / Despliegue Cloudflare · Campus ES/EN 2.3

## Select the correct application / Seleccionar la aplicación correcta

The campus is a static site in `campus/dist`, generated with Python. The independent legacy Next.js application remains in the original repository and is excluded from this repository. **Do not select the Next.js preset or OpenNext for this campus.**

The production entry point is **https://smartkea.com/introduccion-ciberseguridad/**, served by the `fundamentos-ciberseguridad` Worker. Its only production route is `smartkea.com/introduccion-ciberseguridad/*`; an exact zone redirect adds a missing trailing slash. See [Workers publication and recovery](WORKERS-RECOVERY.md) and [repository migration](../docs/MIGRATION.md).

Los logs históricos aportados del 16 de septiembre de 2026 mostraban Workers Builds autodetectando Next.js, un binding hacia `frontend` inexistente y otro intento sin entry-point/assets. No demuestran el estado actual de la cuenta. La configuración explícita siguiente evita mezclar aplicaciones, sin crear un Worker `frontend` innecesario ni desactivar controles.

## Pages with Git integration / Pages conectado a Git

| Setting / Ajuste | Value / Valor |
|---|---|
| Repository | `smartkea-cyberinnovation/fundamentos-ciberseguridad` |
| Production branch | `main`, after this release has been integrated |
| Root directory | `campus` |
| Framework | None / Ninguno |
| Build command | `python3 build.py && python3 check_release.py` |
| Build output directory | `dist` |
| Environment variable | `SKIP_DEPENDENCY_INSTALL=1` |
| Python version | `PYTHON_VERSION=3.13` |

Use a preview branch for initial testing. Connecting an older branch does not deploy the new release. Set variables for both production and previews where appropriate. No application secrets are needed to build or serve the static site. The two commands must both succeed; do not replace errors with `|| true`.

## Direct Upload for a trial / ZIP para prueba

Build from the repository root:

```sh
python3 campus/build.py
python3 campus/check_release.py
```

Upload **`campus/pages-ready.zip`**, whose root contains `index.html`, not the sources ZIP or the outer GitHub Actions artifact ZIP. When downloading an Actions artifact, extract its enclosed `pages-ready.zip` first. The manifest validator checks files, catalogue parity, headers, local asset references and byte equality between folder and ZIP.

The Pages dashboard accepts a ZIP; Wrangler Pages upload uses a directory. A Direct Upload project cannot be converted into a Git-integrated Pages project. Choose Git integration from the start for continuous updates, or create a separate trial project for manual upload.

## Existing Workers Builds / Worker existente

Preserve the explicit root `wrangler.jsonc` and `campus/cloudflare.py` wrapper. Confirm the Git connection and these settings in the Cloudflare dashboard; editing this document does not configure the account.

| Setting | Value |
|---|---|
| Repository | `smartkea-cyberinnovation/fundamentos-ciberseguridad` |
| Production branch | `main` |
| Root directory | repository root |
| Build command | empty, because the wrapper builds and validates |
| Production deploy command | `python3 campus/cloudflare.py deploy` |
| Preview/version upload command | `python3 campus/cloudflare.py preview` |
| Environment | `SKIP_DEPENDENCY_INSTALL=1`, `PYTHON_VERSION=3.13.3`, `NODE_VERSION=22.23.2` |
| Pinned Wrangler | `4.132.0` |

Inspect without publishing:

```sh
python3 campus/cloudflare.py plan
python3 campus/cloudflare.py build
python3 campus/cloudflare.py dry-run
```

`deploy` publishes production; `preview` uploads a test version; `dry-run` does neither. Use the provider's authorized credentials locally or in its build environment, never paste them into chat, source files, screenshots or logs. Run `python3 campus/cloudflare.py --help` to verify supported operations. Do not run bare `npx wrangler deploy` from the legacy app and allow framework migration to change configuration implicitly.

## Acceptance after publication / Prueba del alojamiento

Open the actual provider URL with `?lang=es#/curso` and `?lang=en#/curso`. For the SmartKEA Worker use `https://smartkea.com/introduccion-ciberseguridad/` and verify the release version and source commit in `/introduccion-ciberseguridad/build-info.json`; a root-hosted Pages site uses `/build-info.json`. Then check the syllabus filters; theory/labs/self-check in M05; L05A five phases and recovery; language switching without lost notes; presentation and keyboard; export/import; and a progress link between two separate browser profiles. Import must require confirmation and must not transfer notes. Try 320/390px phone and 768/820px tablet widths, portrait and landscape, then a real iPad/Safari when available.

Confirm `_headers` protections are delivered, absent files return 404 rather than misleading HTML success, no unintended external font/analytics request exists and the kit downloads. Static HTML rendering, browser tests and provider hosting are separate checks. Do not claim an account deployment from a local Wrangler test.

## Rollback and troubleshooting / Recuperación

Keep the previous accepted deployment and its matching ZIP/commit. Restore via the provider's deployment history or republish that exact verified release. Do not delete the learner's local storage when rolling back. Domain/origin changes require exporting progress first; browser storage is origin-scoped.

For a blank page, inspect browser errors and verify JavaScript MIME, CSP, paths and the catalogue files. For a wrong application, check root, build command and output. For missing English data, stop the build and restore complete `campus/locales/en/` sources rather than silently substituting Spanish. For an import failure, check expiry, correct catalogue, secure context and recipient confirmation; use a private JSON copy as fallback.

## Official references / Referencias

- [Pages build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)
- [Build image and environment](https://developers.cloudflare.com/pages/configuration/build-image/)
- [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/)
- [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)

Prepared does not mean deployed. This document does not assert an active public URL, account setup or OTP service. For optional identity see [IDENTITY-OPTIONAL.md](IDENTITY-OPTIONAL.md).
