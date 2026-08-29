# DAAHO Manual-Corrections Release

Release date: August 24, 2026

## Status

This is the new corrected 19-record handoff dataset. It supersedes the stable baseline for approved descriptive use while preserving the stable baseline unchanged for audit and rollback.

## Authoritative release files

- Corrected records: `out_manual_corrections_2026-08-24/`
- Canonical metadata export: `final_metadata_manual_corrections_2026-08-24.csv`
- Validation findings: `validation_report_manual_corrections_2026-08-24.csv`
- Human decision history: `CORRECTION_LOG_2026-08-24.md`
- Integrity manifest: `sha256_manual_corrections_2026-08-24.csv`

The corrected record folder contains exactly 19 canonical `.loc15.json` files and 19 unchanged raw companion `.json` files. Historical CSVs and audit reports copied from `out/` were intentionally excluded from the corrected folder so that stale artifacts cannot be mistaken for current outputs; their originals remain in `out/`.

## Verification summary

- 19 canonical LOC15 records and 19 raw companions.
- Canonical CSV: 19 data rows, 31 unique columns, and the same header order as the July 7 frozen export.
- CSV comparison against the frozen baseline changes exactly five records and only these exported fields:
  - `BC-0698`: Transcript
  - `BC-0703`: Summary, Transcript
  - `BC-0710`: Location
  - `BC-0713`: Title, Date, Transcript
  - `BC-0934`: Contributors, Correspondents, Transcript
- Deterministic core validation: zero errors and zero warnings.
- Evidence QA: zero errors and one accepted warning for the deliberate `Glouchester` source spelling versus `Gloucester` controlled metadata.
- Full automated suite: `17 passed, 4 subtests passed` under Python 3.13.2.
- The existing project `.venv` does not contain pytest; a successor should install `requirements-dev.txt` in a clean environment rather than rely on that old environment folder.

## Version boundaries

- Stable baseline retained: `out/`
- Immutable rollback package retained: `handoff/freeze_2026-07-07_out_baseline/`
- Corrected release: `out_manual_corrections_2026-08-24/`
- Experimental OCR-v2 remains: `out_ocr_v2_gpt54mini/`
- Root `final_metadata.csv`, older exports, and `public/data.json` are not canonical release data.

## Remaining handoff work

The record-level correction decisions are complete. Remaining work is documentation and repository delivery: finish the successor guide, state the disposition of older OCR/summary flags and legacy viewer data, review the dirty worktree, commit the intended files, push, and tag or archive the release.
