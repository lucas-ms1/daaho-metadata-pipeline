# mini_loc15

Tiny, modular pipeline for extracting OCR + Dublin Core–aligned LOC15 metadata from images/PDFs, with Google Drive download support.

## Setup

### 1. Environment Setup
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Copy the example files and configure them:
```bash
cp .env.example .env
cp .config/client_secret.json.example .config/client_secret.json
```

Edit `.env` and set:
- **`OPENAI_API_KEY`**: Your OpenAI API key (required)
- **`GDRIVE_FOLDER_ID`**: Google Drive folder ID (optional, for Google Drive downloads)

Edit `.config/client_secret.json` with your Google OAuth credentials (only needed for Google Drive support):
- Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
- Enable Google Drive API
- Create OAuth 2.0 credentials (Desktop app)

## Usage

### Option A: Process local files
```bash
python -m app.main --in ./samples --out ./out
```

### Option B: Pull from Google Drive
```bash
python -m app.main --gdrive --out ./out
```

### Tier 3 defaults (human-provided)
These fields are **never AI-generated** and are only set if you pass explicit defaults:
```bash
python -m app.main --in ./samples --out ./out \
  --collection "My Collection" \
  --repository "My Repository" \
  --series "Series A" \
  --folder "Folder 3" \
  --box "Box 1" \
  --identifier "ABC-123" \
  --call-number "MSS-001" \
  --digital-identifier "DIG-456" \
  --reproduction-number "REP-789" \
  --permalink "https://example.com/item/123" \
  --digital-collection "Digital Collection Name" \
  --digital-publisher "Digital Publisher" \
  --digitized true
```

### Additional Options
```bash
python -m app.main --in ./samples --out ./out \
  --model gpt-4o \
  --overwrite \
  --apply-reviews \
  --validate-vocab
```

### Rebuild outputs from existing JSON (no OCR/AI call)
```bash
python -m app.main --out ./out --rebuild-from-existing
```

## Viewing Metadata

Once you have extracted metadata to the `out/` folder, you can view it with the included web viewer:

```bash
python3 viewer.py
```

Then open **http://localhost:5000** in your browser.

### Features:
- 🖼️ **Image thumbnails** with tiered metadata display
- 🔍 **Live search** across all metadata fields
- 📋 **Collapsible accordions** for long text fields (transcript, text_reading)
- 🧾 **Archivist review form** for Tier 2 fields with saved overrides
- ✅ **Controlled vocabulary hints** with FAST/AAT validation warnings and autocomplete
- 📊 **Confidence scores** and model information

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
1. Run the pipeline to generate AI proposals in `out/*.loc15.json`.
2. Start the viewer and fill out the Tier 2 review form.
3. Review overrides are saved as `out/<item>.review.json`.
4. Re-run with `--apply-reviews` to apply overrides to outputs.
5. Use `--validate-vocab` to add FAST/AAT validation warnings to outputs.

## Exporting CSV
```bash
python export_csv.py --out-dir ./out --output final_metadata.csv
```

With review/provenance columns:
```bash
python export_csv.py --out-dir ./out --output final_metadata.csv \
  --apply-reviews --include-review-columns
```

## Notes
- Keeps code small and split into focused modules.
- OCR uses Tesseract; if OCR is empty/weak and an image is available, it falls back to a model transcription call.
- AI extraction is constrained to a compact LOC15 schema and returns an envelope with `metadata_tiers` and `field_provenance`.
- The `.config/` folder and `.env` file contain sensitive credentials and are gitignored.

## File path (Google Drive)

NHPTC Planning/Pilot Projects/Digital Collections/Asian American Experience