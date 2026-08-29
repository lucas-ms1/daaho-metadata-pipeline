# DAAHO Transfer Checklist — August 28, 2026

## Release/package

- [ ] Clone `https://github.com/lucas-ms1/daaho-metadata-pipeline.git`.
- [ ] Check out annotated tag `handoff-2026-08-28`.
- [ ] Resolve the final commit with
  `git rev-parse handoff-2026-08-28^{commit}` and record it in the transfer log.
- [ ] Confirm authoritative JSON exists at
  `out_manual_corrections_2026-08-24/` (19 canonical + 19 raw files).
- [ ] Confirm canonical CSV at
  `handoff/release_2026-08-24_manual_corrections/final_metadata_manual_corrections_2026-08-24.csv`.
- [ ] Review the release note, correction log, validation report, SHA-256
  manifest, successor guide, QA ledger, tier report, and final verification report.
- [ ] Recognize `out/` and `handoff/freeze_2026-07-07_out_baseline/` as
  rollback/historical only.
- [ ] Recognize that the viewer is retired and no maintained website is included.

## Acknowledgments

- [ ] Advisor acknowledges 8 accepted limitations, including `BC-0697`
  newspaper bleed and the intentional `BC-0710` warning.
- [ ] Advisor decides whether 14 deferred field-level issues belong in a future
  release, including OCR/name corrections and unsigned-letter creator policy.
- [ ] Successor understands that tier differences are proposals/history and
  top-level metadata/canonical CSV are authoritative.

## Access

- [ ] Repository owner adds the successor to the appropriate GitHub
  collaborator/team and verifies read access (plus write access if required).
- [ ] Dropbox/Drive owner grants access to the DAAHO source location and the
  `NHPTC Planning/Pilot Projects/Digital Collections/Asian American Experience`
  materials.
- [ ] Successor creates their own `.env` from `.env.example` and supplies their
  own authorized OpenAI key if paid processing is needed.
- [ ] Successor creates `.config/client_secret.json` only from
  `.config/client_secret.json.example` using their authorized Google OAuth
  client, then generates their own local token through the approved flow.
- [ ] Confirm no `.env`, real OAuth client secret, token, or API key was sent
  through Git or email.

## Recipient verification

- [ ] Successor can clone and check out the tag.
- [ ] Successor can open the guide and authoritative release files.
- [ ] Successor creates a clean Python 3.13 environment and installs using the
  documented requirements/snapshot method.
- [ ] `python -m pip check` succeeds.
- [ ] Full tests, CLI help checks, and manifest verification succeed.
- [ ] Successor confirms receipt and identifies any access gap in writing.

All unchecked access/acknowledgment/receipt items are human actions. This file
does not claim they have occurred.
