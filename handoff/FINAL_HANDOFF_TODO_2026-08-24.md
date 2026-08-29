# Final Handoff To-Do

The five record-level decisions are resolved and implemented in `out_manual_corrections_2026-08-24/`. No additional metadata decision is currently blocking documentation.

## 1. Finish the successor documentation

- Update `README.md` and the final successor guide to name the corrected release as the authoritative descriptive dataset.
- Keep `out/` and `handoff/freeze_2026-07-07_out_baseline/` documented as the stable rollback baseline.
- Link the release note and correction log in `handoff/release_2026-08-24_manual_corrections/`.
- Reword the historical transcript-bug claim: envelope/tier preservation is regression-tested, but the exact cause of the old blank transcript has not been reproduced conclusively.
- Document the accepted `BC-0710` validation warning, inherited metadata/tier proposal differences, and the need to install `requirements-dev.txt` in a clean environment.

## 2. Close or defer older review notes explicitly

- Review `out/ocr_swap_jinming_check_2026-05-09.md` and label its older experimental OCR flags as accepted limitations or successor work.
- Review `out/summary_review_notes.md` and record that broad summary revision is outside this handoff unless the advisor requests it.
- State that broader place-policy work is outside this handoff.

## 3. Decide the static-viewer disposition

- If the static viewer is part of the handoff, regenerate `public/data.json` from the corrected release and verify all 19 records.
- Otherwise, label `public/` as legacy/noncanonical in the successor guide.

## 4. Clean and deliver the repository

- Review `git status --short` carefully; the summer work and handoff files are currently local and largely uncommitted.
- Confirm that no secrets or machine-specific files are included.
- Commit the intended code, tests, corrected dataset, and handoff documentation.
- Push the handoff branch and create a release tag or archival snapshot.
- From a clean checkout, install runtime and development requirements, run `python -m pytest -q -p no:cacheprovider`, and verify the canonical CSV and manifest.

## 5. Send the final handoff

- Give the advisor/successor the corrected dataset path, canonical CSV path, release note, correction log, and rollback-baseline path.
- State that the five flagged records are closed and identify any deliberately deferred viewer, OCR, summary, or policy work.
