# Repository Inventory — August 28, 2026

## Phase 0 baseline

- Repository: `https://github.com/lucas-ms1/daaho-metadata-pipeline.git`
- Initial branch: `main` (tracking `origin/main`)
- Safety branch created without discarding changes: `handoff-closeout-2026-08-28`
- Initial HEAD: `9df31d0d3728ebe67a066df7a787d122206fea52`
- Tags initially present: none.
- Initial short status: 8 modified tracked files and 25 untracked
  top-level status entries. Expanded file accounting was 147 untracked files
  (155 changed/untracked file entries total). The untracked count is dominated
  by the 38-file August release and the July freeze/handoff package.
- Initial tracked-file count: 139.
- Initial modified tracked files: `.gitignore`, `KNOWN_ISSUES.md`, `README.md`,
  `app/ai_metadata.py`, `app/main.py`, `app/ocr.py`, `app/schema.py`, and
  `export_csv.py`.

These were pre-existing local changes and were preserved. No reset, clean,
checkout-discard, or overwrite of the authoritative/frozen data was performed.

## High-level tracked/untracked categories at baseline

| Category | Baseline state | Closeout decision |
|---|---|---|
| Application, prompts, sample/source images, `out/`, root `final_metadata.csv`, viewer | Tracked | Keep application/history; label `out/` historical; relocate ambiguous root CSV as historical; retire viewer. |
| August corrected 38 JSON files | Untracked | Include as authoritative release. |
| August release-support directory | Untracked | Include all five support files unchanged. |
| July freeze and July handoff notes | Untracked | Include as labeled historical/rollback evidence with superseded banners. |
| `out/summary_review_notes.md` | Tracked | Keep as a historical QA source. |
| `out/ocr_swap_jinming_check_2026-05-09.md` | Untracked | Include as the second historical QA source. |
| OCR-v2 JSON directory | Untracked | Exclude from Git; retain as Dropbox-only experimental output and inventory it in the successor guide. |
| Extra generated reports/exports in `out/` | Mostly untracked | Exclude except the required OCR QA source note; do not add generated reports wholesale. |
| Code/tests/dependency work | Mixed modified/untracked | Include reviewed production fixes, tests, safe scripts, requirements, and tested snapshot. |
| Vocabulary file `vocab/aat_genre.txt` | Untracked; referenced by CLI | Include. |
| Root PDF, PowerPoint, Excel | Untracked | Exclude as unreviewed private/historical binaries; retain in Dropbox only. |
| One-off validators/migrations | Untracked | Include only `scripts/ocr_swap_reports.py` as reproducible historical QA tooling; exclude root scratch/network validators and prompt fixer. |
| Legacy `public/data.json` and images | Tracked | Preserve as explicitly stale historical evidence; serve only retirement notice. |

## Credential and path review

- `.env`, `.venv/`, `.config/client_secret.json`, and `.config/token.json` are
  ignored. A real `.env` exists locally and contains credential-shaped entries;
  values were not printed or copied.
- Only `.env.example` and `.config/client_secret.json.example` are eligible for
  version control. Example placeholders were not treated as secrets.
- Application references to environment-variable names and OAuth schema keys
  are expected and contain no credential values.
- `validate_subjects.py` contains hosted-session absolute scratch paths and is
  excluded.
- `handoff/REPRODUCIBILITY_CHECK_2026-07-16.md` contained a personal `%TEMP%`
  expansion; it was replaced with a generic `%TEMP%` description.
- README setup examples mention credential variable/file names only and transmit
  no values.

## Historical artifacts and binaries

- `DAAHO_process_doc.pdf`, `DAAHO_AI_ML_slides.pptx`, and
  `DAAHO_metadata_2026-04-03.xlsx` are untracked and excluded. They were not
  staged or inspected for publication because they are not necessary to
  reproduce the authoritative release.
- Root `final_metadata.csv` was tracked but stale/ambiguous; the closeout moves
  it under `historical_exports/` with an explicit legacy name.
- Old untracked CSVs and validation outputs under `out/` remain Dropbox-only.
- `out_ocr_v2_gpt54mini/` remains Dropbox-only experimental evidence.

## Deployment discovery

`vercel.json` is present and tracked. No `.vercel/project.json`, GitHub workflow,
or other local deployment binding was found. The Vercel configuration alone is
not evidence of a promised or currently live maintained site, and absence of
local metadata does not prove that no external deployment exists. No external
project was deleted or modified. If the repository is connected to a deployment,
the curated configuration/build now serves the retirement notice rather than
regenerating stale data from `out/`.
