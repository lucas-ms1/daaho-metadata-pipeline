# DAAHO Successor Guide — August 28, 2026

This is the authoritative entry point for the repository handoff. The data
release remains dated August 24, 2026; the repository handoff/tag is dated
August 28, 2026.

## A. Project purpose and workflow

DAAHO is a small pipeline for turning source images (locally in `_gdrive/` or
`SAMPLES/`, or optionally downloaded from Google Drive) into a LOC15-oriented
metadata envelope. Local Tesseract OCR is attempted first; a configured model
may provide OCR fallback and metadata extraction. Deterministic derivations,
tier policy, validation, optional human review, and CSV export follow.

Each canonical `*.loc15.json` is an envelope with:

- `metadata`: the authoritative descriptive values for use and export;
- `metadata_tiers`: Tier 1 extracted evidence/description, Tier 2 proposals,
  and Tier 3 human-only/default structure, including inherited historical values;
- `field_provenance`: how fields were assigned or reviewed;
- `context`: models, schema, derivations, validation, and correction history.

The companion `*.json` files are original machine-output evidence. They are not
the corrected descriptive layer. Reviews and experiments must use a new dated
or temporary output directory. Historical few-shot and OCR-v2 outputs are
comparison evidence, not current metadata.

## B. Authoritative file map

- Corrected canonical JSON and raw companions:
  `out_manual_corrections_2026-08-24/`
- Canonical CSV:
  `release_2026-08-24_manual_corrections/final_metadata_manual_corrections_2026-08-24.csv`
- Validation report:
  `release_2026-08-24_manual_corrections/validation_report_manual_corrections_2026-08-24.csv`
- Correction log:
  `release_2026-08-24_manual_corrections/CORRECTION_LOG_2026-08-24.md`
- Release note:
  `release_2026-08-24_manual_corrections/RELEASE_NOTE_2026-08-24.md`
- SHA-256 manifest:
  `release_2026-08-24_manual_corrections/sha256_manual_corrections_2026-08-24.csv`
- QA ledger: `QA_FLAG_DISPOSITION_2026-08-28.md`
- Final verification: `FINAL_VERIFICATION_REPORT_2026-08-28.md`
- Tier comparison: `TIER_DIFFERENCE_REPORT_2026-08-28.csv`
- Rollback/historical only: root `out/` and
  `freeze_2026-07-07_out_baseline/`
- Experimental, Dropbox-only and noncanonical: root
  `out_ocr_v2_gpt54mini/`
- Historical/noncanonical: `historical_exports/`, old untracked exports under
  `out/`, and legacy viewer artifacts under `public/`.

Paths above are relative to `handoff/` except the explicitly named root paths.

## C. Authority and tier semantics

Top-level `metadata` is authoritative for descriptive use. The canonical August
CSV is the authoritative tabular export. `metadata_tiers` preserve proposal and
history structure and are not automatically authoritative when they differ
from top-level metadata. Raw companions preserve original machine evidence.

The reproducible comparison command is:

```powershell
python .\scripts\report_tier_differences.py `
  --metadata-dir .\out_manual_corrections_2026-08-24 `
  --output .\handoff\TIER_DIFFERENCE_REPORT_2026-08-28.csv
```

It compares each schema-defined tier field with the same field in top-level
`metadata`, using exact JSON value equality. The current result is **25 field
differences across 18 records**. Use the generated CSV for the exact list;
differences are inherited state to reconcile later, not authority to rewrite
the August release.

## D. Five completed corrections

The [correction log](release_2026-08-24_manual_corrections/CORRECTION_LOG_2026-08-24.md)
records the authorized details:

- `BC-0698`: recovered the target article transcript.
- `BC-0703`: corrected Swasdi Nitibhon spelling in description/transcript and
  recorded the reviewed decision not to add him as contributor.
- `BC-0710`: corrected controlled place metadata to
  `Massachusetts--Gloucester` while retaining source-visible `Glouchester` in
  the transcript.
- `BC-0713`: synchronized title, date, transcript, and derivation context to
  February 26, 1942.
- `BC-0934`: corrected contributor/correspondent names, address, and transcript.

`BC-0710` intentionally retains the single evidence warning
`place_mismatch_with_header_sender`: controlled discovery spelling and literal
source evidence differ by design.

## E. Deferred and accepted work

The field-level QA ledger is controlling. Deferred work includes the source-
visible `BC-0692` Nakaku spelling, William N. Jardine across `BC-0696`, Jean Van
Ausdall/Hosack's Studio in `BC-0697`, the `BC-0716` plural possessive letterhead,
and creator policy for six unsigned “President” letters. Accepted limitations
include minor OCR/source-faithfulness variants, adjacent-column bleed in
`BC-0697`, and the intentional `BC-0710` warning. Historical summary findings
about discarded few-shot output are not automatically current-release defects.

Deferred and accepted flags did not reopen the approved August release.

## F. Environment and commands

Tested environment: CPython 3.13.2 on Windows. Runtime dependencies are in
`requirements.txt`; development/test dependencies are in `requirements-dev.txt`.
`constraints-handoff-py313-2026-08-28.txt` is the tested Windows snapshot, not a
universal cross-platform lock.

```powershell
py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements-dev.txt `
  -c .\constraints-handoff-py313-2026-08-28.txt
python -m pip check
```

Tesseract is external system software, not installed by pip:

```powershell
where.exe tesseract
tesseract --version
```

It was unavailable on the handoff machine, so real Tesseract execution was not
tested. Image processing may invoke paid/network model calls when local OCR is
missing or weak. Google Drive requires OAuth/browser authorization. Online
FAST/AAT checks require network access. Do not run those operations merely for
release verification.

Safe read-only checks:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest -q -p no:cacheprovider
python -m app.main --help
python .\export_csv.py --help
python .\scripts\verify_release_manifest.py
```

Validation/export commands write files, so use `%TEMP%` or a new dated path:

```powershell
python .\scripts\validation_report.py `
  --out-dir .\out_manual_corrections_2026-08-24 `
  --output (Join-Path $env:TEMP 'daaho_validation_check.csv')

python .\export_csv.py `
  --out-dir .\out_manual_corrections_2026-08-24 `
  --output (Join-Path $env:TEMP 'daaho_export_check.csv')
```

Rebuild tests verify envelope/tier/context preservation. Direct `process_path`
tests verify explicit transcript assignment/fallback and provenance. Neither
test suite conclusively reconstructs the exact historical blank-transcript cause.

## G. Viewer status

The viewer is retired. No repository evidence promised a maintained public
website. `public/index.html` is a retirement page; `build_static.py` cannot
rebuild stale data from `out/`; `viewer.py` serves the notice only; and
`public/data.json` is retained solely as stale historical evidence. Only local
`vercel.json` was found—no local project binding or deployment URL was
discoverable. This does not prove that no external deployment exists.

## H. Git, release, and access

- Repository: `https://github.com/lucas-ms1/daaho-metadata-pipeline.git`
- Annotated tag: `handoff-2026-08-28`
- Resolve the tag to its commit:
  `git rev-parse handoff-2026-08-28^{commit}`

```powershell
git clone https://github.com/lucas-ms1/daaho-metadata-pipeline.git
Set-Location .\daaho-metadata-pipeline
git checkout handoff-2026-08-28
```

Create local credentials only from `.env.example` and
`.config/client_secret.json.example`. Never transmit `.env`, OAuth client
secrets, token files, or API keys through Git or email.

Source material is locally synchronized under repository-relative `_gdrive/`;
the historical Dropbox/Drive description is
`NHPTC Planning/Pilot Projects/Digital Collections/Asian American Experience`.
The human owner must grant the successor repository collaborator/team access
and Dropbox/Drive access, then confirm the successor can clone, open, and run
the tagged package. See `TRANSFER_CHECKLIST_2026-08-28.md`.
