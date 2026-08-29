# DAAHO Reproducibility Check

> **SUPERSEDED HISTORICAL JULY NOTE.** The August 24 corrected release is
> authoritative; `out/` is rollback evidence only, and the five record
> decisions are complete. Use `SUCCESSOR_GUIDE_2026-08-28.md` and
> `QA_FLAG_DISPOSITION_2026-08-28.md` for current status. The exact historical
> blank-transcript cause was not conclusively reproduced; current tests verify
> envelope/tier preservation and explicit transcript assignment, not a
> definitive reconstruction of that cause.

Date: July 16, 2026

## Current Verification

- System Python: 3.13.2
- Existing `.venv` Python: 3.13.2
- System test result: `17 passed, 4 subtests passed`
- Existing `.venv` cannot run tests because `pytest` is not installed.
- `requirements-dev.txt` now declares the test dependency.
- Tesseract is unavailable on the current machine.
- System Python lacks the optional Google Drive and Flask packages.
- Existing `.venv` imports the application, Google Drive support, and viewer.
- `python .\export_csv.py --help` succeeds.
- A template-based temporary export matched the frozen CSV exactly: 19 rows and 31 columns.
- No paid calls, Google authorization, real OCR, or full pipeline processing were used for verification.

The existing `.venv` is not a clean successor environment because it still
lacks `pytest`. The declared dependencies were instead verified in a fresh
temporary environment as recorded below.

## Clean Temporary Environment Verification

Verified on July 16, 2026, using a uniquely named temporary virtual environment
under `%TEMP%`, outside the repository. The machine-specific temporary path is
intentionally omitted.

- Python: 3.13.2
- pip: 26.1.2
- pytest: 9.1.1
- openai: 2.45.0
- Pillow: 12.3.0
- pytesseract: 0.3.13
- Flask: 3.1.3
- google-api-python-client: 2.198.0
- requests: 2.34.2
- `python -m pip check`: `No broken requirements found.`
- Full test suite: `17 passed, 4 subtests passed`
- Imports: Flask, Google API client, OpenAI, Pillow, pytesseract, pytest,
  requests, `app.main`, `app.gdrive`, and `viewer` all imported successfully.
- CLI checks: `python -m app.main --help` and
  `python .\export_csv.py --help` both exited 0.
- Export comparison: a temporary template-based export had 19 data rows, 31
  unique columns, and complete row-matrix equality with the frozen final CSV.
- Tesseract remained externally unavailable (`where.exe tesseract` exited 1),
  and no real OCR was attempted.
- No credentials, paid model calls, Google authorization, or external
  vocabulary operations were used.
- The temporary virtual environment and temporary export CSV were removed
  after verification.
- A dependency lock remains deferred until repository and release scope is
  finalized. The versions above are the tested snapshot for this handoff.

## Successor Verification Commands

```powershell
Set-Location -LiteralPath 'C:\path\to\DAAHO'

py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r .\requirements-dev.txt

where.exe tesseract
tesseract --version

$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pip check
python -m pytest -q -p no:cacheprovider
python -m app.main --help
python .\export_csv.py --help
```

Use a new output directory for any processing run. Do not use these commands
against `out/` or the frozen baseline.

## Known Limitations

- Tesseract requires a separate installation and was unavailable during this check.
- Processing images requires an authorized OpenAI API key and may incur paid calls.
- Google Drive requires OAuth credentials, browser authorization, and token-file creation.
- Online FAST/AAT advisory checks require network access.
- PDF processing lacks focused test coverage.
- Viewer review actions and export/validation commands write files.
- Repository cleanup, committing, and release versioning remain pending.
- No dependency lock has been created; the tested snapshot above records the
  successful clean-environment versions pending final repository/release scope.
