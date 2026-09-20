# Integration record / Registro de integración ES/EN

Historical integration record from the original repository; see [the repository migration](../docs/MIGRATION.md) for the current source location.

The original release completed the implementation prepared for [PR #20](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/pull/20) (`feat/campus-es-en-portable`), reusing its seven English source files rather than discarding the earlier work. It keeps the active course IDs, hours and v1 progress format. The separate master-plan documents in `main` must be retained when merging.

Implementation includes bilingual catalogue compilation, explicit interface localization, light responsive design, presentation, guarded progress import/export and optional sharing of a no-notes snapshot. Native GitHub writes are used to store the reviewed files. Creating trees alone is not publication: a commit must be attached to the branch, validated and merged.

## Acceptance before merge

Read the final diff and review threads, run the campus and Cloudflare-local workflows, inspect artifacts and screenshots, fix actual failures and check that the PR head has not moved. Use the expected head SHA when merging. Do not remove branch controls, ignore failed tests, turn browser errors into skips or close the proposal while losing its content.

After merge, read `main` and the open-PR collection again. Download the post-merge Pages artifact and verify its digest, inner manifest and `build-info.json` source commit. A PR's synthetic merge test SHA is not the definitive main merge SHA; distinguish both in reports.

## Boundaries / Límites

No account settings, collaborators, secrets, licensing or remote hosting are changed by integration. The optional OTP architecture is documentation only. Source/runtime tests do not prove native Windows/macOS lab execution or a physical iPad test. The master expansion plan remains a reference, not 108 new active bilingual lessons.

The actual commit and completed workflow outcomes are recorded in the PR and GitHub Actions rather than inferred from this checklist.
