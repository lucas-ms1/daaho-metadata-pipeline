# Known Issues

> **Superseded July-era status note.** The August 24 corrected release is
> authoritative; `out/` is rollback evidence, not the current descriptive
> release. The five record decisions are complete. Current-status claims are
> superseded by `handoff/SUCCESSOR_GUIDE_2026-08-28.md` and
> `handoff/QA_FLAG_DISPOSITION_2026-08-28.md`. The exact historical cause of
> the blank-transcript incident was not conclusively reproduced. Regression
> coverage verifies envelope/tier preservation and explicit process-path
> transcript assignment, not a definitive reconstruction of that cause.

## Few-shot rebuild stripped transcript field

- Observed: all 19 `out_fewshot_summary_test/*.loc15.json` files have empty `metadata.transcript`; `metadata.language` and other non-Summary fields are also often blank or changed. Baseline `out/*.loc15.json` has transcripts populated for 18 of 19 files.
- Status: guarded by `tests/test_rebuild_existing.py`; direct assignment/fallback is guarded by `tests/test_process_path.py`. The exact historical cause was not conclusively reproduced.
- Historical caveat: the existing `out_fewshot_summary_test/` files remain transcript-stripped and should not be treated as evidence-complete metadata outputs.
- Why it matters: this blocks future use of `out_fewshot_summary_test/` as a metadata source and could silently strip transcripts on any future rebuild against any output set.
- Successor warning: avoid running `python -m app.main --out .\out --rebuild-from-existing` or any other in-place rebuild against stable evidence folders unless working from a backup or temporary copy.

## OCR-v2 warning rows remain experimental

- Status: `out_ocr_v2_gpt54mini/` should not replace `out/` wholesale. The OCR-v2 validation audit still has two warning rows, documented in `handoff/OCR_V2_QA_2026-07-07.md`.
- Successor warning: treat OCR-v2 as comparison evidence only unless the flagged rows, especially `BC-0710_Recto.loc15.json`, are manually reviewed and corrected in a new versioned output copy.
