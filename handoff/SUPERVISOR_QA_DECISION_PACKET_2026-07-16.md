# Supervisor QA Decision Packet

> **SUPERSEDED HISTORICAL JULY DECISION PACKET.** The August 24 corrected
> release is authoritative; `out/` is rollback evidence only, and all five
> record decisions are complete. Use `SUCCESSOR_GUIDE_2026-08-28.md` and
> `QA_FLAG_DISPOSITION_2026-08-28.md` for current status. The exact historical
> blank-transcript cause was not conclusively reproduced; regression coverage
> verifies envelope/tier preservation and explicit transcript assignment, not
> a definitive reconstruction of that cause.

Date: July 16, 2026

## 1. Baseline Status

- `out/` remains the stable baseline.
- The immutable package is `handoff/freeze_2026-07-07_out_baseline/`.
- `out_ocr_v2_gpt54mini/` remains experimental.
- The historical few-shot outputs are not evidence-complete metadata.
- This package validates cleanly and is the safest version to preserve.
- Any approved changes will be made in a new folder such as `out_manual_corrections_YYYY-MM-DD/`, never in `out/`.

## 2. High-Confidence Candidates Pending Approval

These are proposed corrections only. None has been applied to the baseline.

| Record | Field | Current baseline | Proposed change | Evidence and scope |
|---|---|---|---|---|
| `BC-0710` | `metadata.place` | `Massachusetts--Glouchester` | `Massachusetts--Gloucester` | Use the approved controlled-vocabulary spelling. Update the corresponding tiered value only; preserve the source spelling in the transcript. |
| `BC-0713` | Date | `1942-02-28` | `1942-02-26` | The source image visibly says `February 26th, 1942`. A future correction must consistently update the title, date, transcript, and tiered copies. |
| `BC-0934` | Contributor | `Ernest H. Hahm` | `Ernest H. Hahne` | The source signature visibly says `Ernest H. Hahne`. A future correction should update the contributor, transcript, and tiered copies. The image and human reference support `Rosa Choi` rather than `Rose Choi`, but whether the student belongs in `correspondents` requires supervisor approval. |

## 3. Decisions Requiring Human Authority

- `BC-0698`: leave its transcript blank or authorize manual transcript recovery.
- `BC-0703`: choose between the source-visible form `Swasdi Nitibhom`, the human-reference form `Swasdi Nitibhon`, or another authoritative form. This is not a mechanical correction.
- Define whether `place` means document origin, recipient location, or all relevant locations.
- Decide whether summary improvement remains in scope.
- Decide whether the approved high-confidence corrections should be implemented in a new versioned output copy.

## 4. Explicitly Excluded Work

This proposal does not authorize:

- Wholesale OCR-v2 adoption.
- Broad prompt or model reruns.
- Mutation of `out/`.
- Mutation of the frozen package.
- Automatic normalization of ambiguous names.
- Use of the duplicate-header human CSV as a direct automated correction source.

## 5. Supervisor Reply Template

- Approve versioned corrections for `BC-0710`, `BC-0713`, and Ernest H. Hahne: Yes/No
- Approve Rosa Choi spelling: Yes/No
- Keep Rosa Choi in `correspondents`: Yes/No/Needs review
- Recover `BC-0698` transcript: Yes/No
- Canonical `BC-0703` name:
- Place policy:
- Further summary work in scope: Yes/No
- Additional model/API calls authorized: Yes/No

## 6. Work After Approval

Approved corrections will:

- Be made only in a new versioned copy.
- Preserve the original frozen baseline.
- Update duplicate metadata and tier representations consistently.
- Record human-approved provenance.
- Receive validation, comparison, and hash checks before delivery.
