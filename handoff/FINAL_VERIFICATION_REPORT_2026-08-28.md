# Final Verification Report — August 28, 2026

The authoritative data release remains dated August 24, 2026. This report
records closeout verification; it does not modify release records.

## Repository baseline

| Check | Result |
|---|---|
| Repository root | Owner-supplied DAAHO workspace (personal absolute path omitted) |
| Starting branch / HEAD | `main` / `9df31d0d3728ebe67a066df7a787d122206fea52` |
| Safety branch | `handoff-closeout-2026-08-28` |
| Remote | `origin` → `https://github.com/lucas-ms1/daaho-metadata-pipeline.git` |
| Initial status | 8 modified tracked files; 25 untracked top-level entries (147 expanded untracked files) |
| Initial tags | none |
| Worktree protection | PASS — no reset, clean, or discard was used |

Full category and secret/path findings are in
`REPOSITORY_INVENTORY_2026-08-28.md`.

## Release package verification

Commands included:

```powershell
python .\scripts\verify_release_manifest.py
python .\scripts\validation_report.py `
  --out-dir .\out_manual_corrections_2026-08-24 `
  --output (Join-Path $env:TEMP 'daaho_validation_check_2026-08-28.csv')
python .\export_csv.py `
  --out-dir .\out_manual_corrections_2026-08-24 `
  --output (Join-Path $env:TEMP 'daaho_export_check_2026-08-28.csv')
```

| Check | Actual result | Verdict |
|---|---|---|
| Canonical `*.loc15.json` count | 19 | PASS |
| Raw companion `*.json` count | 19; names pair exactly | PASS |
| Raw files vs July freeze | 0 byte differences | PASS |
| Canonical files changed vs July freeze | Exactly BC-0698, BC-0703, BC-0710, BC-0713, BC-0934 | PASS |
| Semantic changed paths | Only approved metadata/tier fields plus corresponding provenance, human-correction, validation, and title-derivation context | PASS |
| Canonical CSV data rows | 19 | PASS |
| Canonical CSV columns | 31, all unique, intended order preserved | PASS |
| Fresh export vs canonical CSV | Complete row-matrix equality | PASS |
| Deterministic core validation | 0 errors, 0 warnings | PASS |
| Evidence QA | 0 errors; exactly 1 accepted BC-0710 place warning | PASS |
| Manifest | 42 entries; all files exist and byte sizes/SHA-256 hashes match | PASS |
| Unlisted files in strict release directories | none (manifest itself is the sole permitted unlisted file) | PASS |

The exact changed-path inventory was:

- `BC-0698`: transcript plus Tier 1/provenance/human-correction context.
- `BC-0703`: description/transcript plus Tier 1/provenance and contributor-review context.
- `BC-0710`: place plus Tier 1/provenance/human-correction and recomputed evidence warning.
- `BC-0713`: title/date/transcript plus Tier 1/provenance/human-correction and title-derivation context.
- `BC-0934`: contributors/correspondents/transcript plus Tier 1/provenance/human-correction context.

## Tier and QA disposition checks

```powershell
python .\scripts\report_tier_differences.py
```

- 25 exact field differences across 18 records; PASS (reported reproducibly in
  `TIER_DIFFERENCE_REPORT_2026-08-28.csv`).
- QA ledger: 53 distinct field/span/claim rows; 13 corrected, 18 false
  positives, 8 accepted limitations, and 14 deferred successor items; PASS.

## Environment, dependencies, and tests

A fresh `%TEMP%` virtual environment was created with CPython 3.13.2, then
installed from `requirements-dev.txt`. The exact resolved versions are in
`../constraints-handoff-py313-2026-08-28.txt`; this is a tested Windows
snapshot, not a universal lock.

```powershell
python -m pip install -r .\requirements-dev.txt `
  -c .\constraints-handoff-py313-2026-08-28.txt
python -m pip check
python -m pytest -q -p no:cacheprovider
python -m app.main --help
python .\export_csv.py --help
python .\build_static.py
```

| Check | Actual result | Verdict |
|---|---|---|
| Dependency installation | Completed in fresh Python 3.13.2 environment | PASS |
| Direct imports | Flask, Google API client, jsonschema, OpenAI, Pillow, Pydantic, pytesseract, pytest, requests | PASS |
| `pip check` | `No broken requirements found.` | PASS |
| Full suite | `23 passed, 4 subtests passed in 10.01s` | PASS |
| Application CLI help | exit 0 | PASS |
| Export CLI help | exit 0 | PASS |
| Retired viewer build | exit 0; no data regenerated | PASS |
| Tesseract executable | not found by `where.exe`; command unavailable | NOT TESTED |

No paid model calls, Google authorization, online vocabulary mutations, or
authoritative-output rewrites were performed. Because Tesseract is absent, no
real sample OCR command could be run.

Rebuild tests verify envelope/tier/context preservation. Direct processing-path
tests verify blank/null transcript fallback, deliberate nonblank transcript
preservation, Tier 1 synchronization, and explicit context/provenance. They do
not conclusively reproduce the exact historical blank-transcript cause.

## Viewer/deployment verification

- No promise of a maintained public viewer was found in repository history.
- Only `vercel.json` was discoverable locally; no `.vercel/project.json` or
  GitHub deployment workflow was found.
- `public/index.html` is a retirement notice.
- `build_static.py` cannot rebuild `public/data.json` from historical `out/`.
- `viewer.py` exposes only the retirement notice.
- External deployment existence/state was not established; absence of local
  binding metadata is not proof that no deployment exists.

## Prospective clean archive and post-tag clone

The exact staged index was materialized into a new `%TEMP%` directory with
`git write-tree` and `git checkout-index --all --force --prefix=<temp>/`.
This checks the blobs that will be committed, including release bytes after
Git attribute and line-ending processing.

| Prospective staged-tree check | Actual result | Verdict |
|---|---|---|
| Dependency integrity | `No broken requirements found.` | PASS |
| Full suite | `23 passed, 4 subtests passed` | PASS |
| Application/export CLI help | both exit 0 | PASS |
| Release manifest | 42 entries; byte sizes and SHA-256 hashes match | PASS |
| Release counts | 19 canonical JSON; 19 raw companions | PASS |
| Canonical CSV | 19 rows; 31 unique columns | PASS |
| Credential files/personal paths | none in staged index | PASS |
| Staged binary blobs | none | PASS |

Post-tag read-only clone verification is intentionally recorded in the final
terminal report after tagging; the tagged commit does not embed its own hash.
