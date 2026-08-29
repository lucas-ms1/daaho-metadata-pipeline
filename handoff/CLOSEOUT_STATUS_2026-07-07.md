# DAAHO Closeout Status, 2026-07-07

> **SUPERSEDED HISTORICAL JULY NOTE.** The August 24 corrected release is
> authoritative; `out/` is rollback evidence only, and the five record
> decisions below are no longer pending. Use `SUCCESSOR_GUIDE_2026-08-28.md`
> and `QA_FLAG_DISPOSITION_2026-08-28.md` for current status. The exact
> historical cause of the blank-transcript incident was not conclusively
> reproduced; current tests verify envelope/tier preservation and explicit
> transcript assignment, not a definitive reconstruction of that cause.

This note summarizes the current handoff state for the next research assistant.

## Current Stable Baseline

- `out/` is the working stable baseline for the current 19 LOC15 metadata outputs.
- `handoff/freeze_2026-07-07_out_baseline/` is the frozen read-only baseline package.
- The frozen package already includes `BASELINE_FREEZE_NOTE.md`, `sha256_out_baseline_2026-07-07.csv`, `validation_report_out_baseline_2026-07-07.csv`, and a copied `out_baseline/` directory.
- Known baseline caveat: `BC-0698_Recto.loc15.json` has an empty `metadata.transcript` value.

## Completed Fixes / Decisions

- The `--rebuild-from-existing` transcript/envelope stripping issue has been fixed in code and is guarded by `tests/test_rebuild_existing.py`.
- Existing `out_fewshot_summary_test/` files remain historically transcript-stripped and should not be used as evidence-complete metadata.
- OCR-v2 was QA-reviewed and remains experimental. See `handoff/OCR_V2_QA_2026-07-07.md`.

## Commands To Verify Current State

```powershell
python -m pytest -q
python scripts\validation_report.py --out-dir out --output out\validation_report_current_audit.csv
Get-Content -Raw KNOWN_ISSUES.md
Get-Content -Raw handoff\OCR_V2_QA_2026-07-07.md
```

The validation command writes `out\validation_report_current_audit.csv`. For strictly read-only verification, copy `out/` to a temporary folder first or use the frozen validation report in `handoff/freeze_2026-07-07_out_baseline/`.

## Do Not Do

- Do not run `python -m app.main --out .\out --rebuild-from-existing` on `out/` in place.
- Do not adopt `out_ocr_v2_gpt54mini/` wholesale.
- Do not use `out_fewshot_summary_test/` as evidence-complete.
- Do not modify the frozen baseline.

## Recommended Next Work

- Finalize successor handoff documentation.
- Decide whether to leave `out/` unchanged as the final deliverable or create a new versioned correction copy only if a human approves targeted fixes such as `BC-0710`.
- If making future corrections, do them in a new folder such as `out_manual_corrections_YYYY-MM-DD/`.
