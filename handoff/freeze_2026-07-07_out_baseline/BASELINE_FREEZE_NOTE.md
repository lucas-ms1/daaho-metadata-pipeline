# DAAHO Baseline Freeze

Freeze date: July 7, 2026

I froze `out/` as the DAAHO baseline package. It contains the current 19 LOC15 metadata outputs and the copied supporting baseline files from `out/`.

This freeze includes:
- `out_baseline/`: copied baseline files from `out/`
- `final_metadata_out_baseline_2026-07-07.csv`: regenerated final CSV for the baseline
- `validation_report_out_baseline_2026-07-07.csv`: validation report for the baseline
- `sha256_out_baseline_2026-07-07.csv`: SHA256 manifest for the source `out/` files

Verification summary:
- Source file count: 51
- Source LOC15 JSON count: 19
- Frozen file count: 51
- Frozen LOC15 JSON count: 19
- Final CSV data rows: 19
- Final CSV columns: 31
- Final CSV duplicate headers: 0
- Validation findings: 0
- Manifest hash rows: 51
- Source/frozen hash differences: 0

`out_ocr_v2_gpt54mini/` remains experimental because its current validation report still flags two `place_mismatch_with_header_sender` warnings. It should not replace this baseline without targeted QA and correction.

Known baseline check: `BC-0698_Recto.loc15.json` has an empty `metadata.transcript` value in the current baseline. This is documented as a check, not as a reason to adopt OCR-v2.

Future OCR, summary, or rebuild experiments should be run in new output folders and should not overwrite `out/`.
