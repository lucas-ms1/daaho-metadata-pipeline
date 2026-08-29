# Handoff email draft — do not send automatically

**Subject:** DAAHO August 2026 authoritative release and successor handoff

Hello,

The DAAHO successor package is ready. The August 24, 2026 corrected release is
the authoritative descriptive dataset. Its 19 canonical JSON records and 19
raw evidence companions are in `out_manual_corrections_2026-08-24/`, and the
canonical CSV and release support files are under
`handoff/release_2026-08-24_manual_corrections/`.

The five approved corrections—BC-0698, BC-0703, BC-0710, BC-0713, and
BC-0934—are complete. Every older QA flag now has a field/span-level written
disposition in `handoff/QA_FLAG_DISPOSITION_2026-08-28.md`. Deferred OCR,
summary, place, creator-policy, and tier-reconciliation work is listed rather
than silently changed.

The legacy viewer is retired; no maintained website is included. The repository
serves a retirement notice and labels `public/data.json` stale/noncanonical.

Use the annotated tag `handoff-2026-08-28`. Resolve its final commit with:

`git rev-parse handoff-2026-08-28^{commit}`

The tagged package passed clean-environment tests, release-manifest checks, and
clean-clone verification. The full evidence is in
`handoff/FINAL_VERIFICATION_REPORT_2026-08-28.md` and the accompanying delivery
report.

Please confirm:

1. receipt of this handoff;
2. GitHub repository access;
3. Dropbox/source Drive access;
4. ability to clone, open, and run the tagged package; and
5. advisor acknowledgment of the accepted limitations and deferred policy work.

No API key, OAuth client secret, token, or other credential is included in Git
or this email. Please create credentials from the example files using your own
authorized accounts.

Thank you.
