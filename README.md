# mini_loc15

Tiny, modular pipeline for extracting OCR + Dublin Core–aligned LOC15 metadata from images/PDFs, with Google Drive download support.

> **Authoritative release (August 24, 2026):** use
> `out_manual_corrections_2026-08-24/` and
> `handoff/release_2026-08-24_manual_corrections/final_metadata_manual_corrections_2026-08-24.csv`.
> Start with `handoff/SUCCESSOR_GUIDE_2026-08-28.md`. The root `out/`, the July
> freeze, root `final_metadata.csv`, older exports, and viewer data are
> rollback/historical or noncanonical only. The viewer is retired; no maintained
> website is included. Always use an explicit new or temporary output directory
> for commands that write files.

## Setup

### 1. Environment Setup (Windows PowerShell)
Runtime dependencies are listed in `requirements.txt`. `requirements-dev.txt`
includes those dependencies plus the test runner.

```powershell
py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements-dev.txt
```

### 2. Configuration
Create the local environment file:

```powershell
Copy-Item -LiteralPath .\.env.example -Destination .\.env
```

Edit `.env` and set:
- **`OPENAI_API_KEY`**: Your OpenAI API key (required)
- **`GDRIVE_FOLDER_ID`**: Google Drive folder ID (optional, for Google Drive downloads)

Edit `.config/client_secret.json` with your Google OAuth credentials (only needed for Google Drive support):
- Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
- Enable Google Drive API
- Create OAuth 2.0 credentials (Desktop app)

Google Drive is optional. If it is needed, create the configuration directory
and copy the safe example before replacing its placeholders with authorized
credentials:

```powershell
New-Item -ItemType Directory -Path .\.config -Force | Out-Null
Copy-Item -LiteralPath .\.config\client_secret.json.example -Destination .\.config\client_secret.json
```

Do not commit `.env`, `client_secret.json`, or `token.json`.

### 3. External OCR Dependency
Tesseract is not installed by pip. Install it separately and ensure it is on
`PATH` before processing images:

```powershell
where.exe tesseract
tesseract --version
```

At this handoff, Tesseract was not available on the current machine. If OCR is
missing or weak, the pipeline may call the `o4-mini` OCR fallback, which can
create an additional paid API call.

## Usage

### Option A: Process local files
Use a new dated output directory for experiments or new processing runs:

```powershell
python -m app.main --in .\SAMPLES --out .\out_experiment_2026-07-16
```

### Option B: Pull from Google Drive
```powershell
python -m app.main --gdrive --out .\out_experiment_2026-07-16
```

### Tier 3 defaults (human-provided)
These fields are **never AI-generated** and are only set if you pass explicit defaults:
```powershell
python -m app.main --in .\SAMPLES --out .\out_experiment_2026-07-16 `
  --collection "My Collection" `
  --repository "My Repository" `
  --series "Series A" `
  --folder "Folder 3" `
  --box "Box 1" `
  --identifier "ABC-123" `
  --call-number "MSS-001" `
  --digital-identifier "DIG-456" `
  --reproduction-number "REP-789" `
  --permalink "https://example.com/item/123" `
  --digital-collection "Digital Collection Name" `
  --digital-publisher "Digital Publisher" `
  --digitized true
```

### Additional Options
```powershell
python -m app.main --in .\SAMPLES --out .\out_experiment_2026-07-16 `
  --model gpt-4o `
  --ocr-model o4-mini `
  --overwrite `
  --apply-reviews `
  --validate-vocab
```

`gpt-4o` is the metadata extraction default. `o4-mini` is the OCR/transcription
fallback default. `--force-llm-ocr` uses the OCR model for every input and can
substantially increase API usage. `--validate-vocab` and the online vocabulary
advisory can make external FAST/AAT requests.

### Rebuild outputs from existing JSON (no OCR/AI call)
```powershell
python -m app.main --out .\out_experiment_2026-07-16 --rebuild-from-existing
```

Do not rebuild `out/` or the frozen package in place. Use a temporary copy or a
new dated output directory even though transcript preservation is now covered
by regression tests.

## Viewer status

The static and Flask viewers are retired legacy artifacts. `public/index.html`
is a retirement notice; `viewer.py` serves that notice only; `build_static.py`
does not regenerate data; and `public/data.json` is stale/noncanonical. See
`LEGACY_VIEWER_NOTICE.md`. No maintained website is included in this handoff.

## Tiered output format
Each output file includes:
```json
{
  "metadata": { ... },
  "metadata_tiers": { "tier1": {...}, "tier2": {...}, "tier3": {...} },
  "field_provenance": { "subjects": "AI-Proposed Subject", ... },
  "context": { "model": "...", "schema_version": "...", "vocabulary_validation": {...}, ... }
}
```

## Review workflow
1. Run the pipeline to generate AI proposals in a new output folder.
2. Review proposals outside the retired viewer and save any authorized review
   file only beside a versioned working copy.
3. Re-run with `--apply-reviews` against that versioned copy.
4. Use `--validate-vocab` only when network vocabulary checks are authorized.

## Exporting CSV
```powershell
python .\export_csv.py --out-dir .\out_experiment_2026-07-16 --output .\final_metadata.csv
```

Without `--template`, the exporter uses 31 built-in unique headers. To use a
specific template, pass it explicitly:

```powershell
python .\export_csv.py `
  --out-dir .\out_experiment_2026-07-16 `
  --template .\out\final_metadata_2026-04-27_handoff.csv `
  --output .\final_metadata.csv
```

Exact duplicate template headers are removed while preserving the first
occurrence. An explicitly supplied missing template fails clearly. Do not use
the duplicate-header human review CSV as a direct automated correction source.

With review/provenance columns:
```powershell
python .\export_csv.py `
  --out-dir .\out_experiment_2026-07-16 `
  --output .\final_metadata.csv `
  --apply-reviews --include-review-columns
```

## Testing and Safe Verification

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pip check
python -m pytest -q -p no:cacheprovider
```

The validation report command writes its output file, so use a temporary copy
or the frozen validation report for strictly read-only checks. The viewer,
review workflow, export commands, and validation commands can all write files.

The repository accepts image input and has nominal PDF support, but PDF
processing does not currently have focused test coverage and should be verified
before production use.

`out/` and `handoff/freeze_2026-07-07_out_baseline/` are rollback/historical
evidence only. Do not overwrite, rebuild, apply reviews to, or run experiments
inside them. The authoritative descriptive release is the August corrected
package named at the top of this README.

## Notes
- Keeps code small and split into focused modules.
- OCR uses Tesseract; if OCR is empty/weak and an image is available, it falls back to a model transcription call.
- AI extraction is constrained to a compact LOC15 schema and returns an envelope with `metadata_tiers` and `field_provenance`.
- The `.config/` folder and `.env` file contain sensitive credentials; only the safe client-secret example is intended for version control.

## File path (Google Drive)

NHPTC Planning/Pilot Projects/Digital Collections/Asian American Experience

## Validation counts (SAMPLES)

**Dataset:** `SAMPLES/`  
**Date:** 2026-03-11  

Baseline (before evidence place normalization):
- 0 errors, 6 warnings (all `place` evidence warnings)
- Top warning codes: `place_looks_like_recipient_not_sender`=3, `place_mismatch_with_header_sender`=2, `likely_missing_secondary_place`=1

After evidence place normalization:
- 0 errors, 0 warnings
- Top warning codes: (none)
