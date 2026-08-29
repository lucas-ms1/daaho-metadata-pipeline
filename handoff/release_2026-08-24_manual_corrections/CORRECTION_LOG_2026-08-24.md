# Human-Approved Correction Log

Date: August 24, 2026

This log records the five corrections applied in `out_manual_corrections_2026-08-24/`. The stable `out/` dataset and `handoff/freeze_2026-07-07_out_baseline/` were not edited.

## Approved changes

| Record | Fields changed | Baseline | Corrected release | Decision and evidence |
|---|---|---|---|---|
| `BC-0698` | Transcript | Blank | Manual transcription of the Miami University/President Hoover rescue article and its directly associated photograph caption | The user approved recovery of only the Miami rescue article. Unrelated newspaper columns were excluded. Unusual printed forms, including `Yokohoma`, `Hoishoto`, and `the boiling seas was caused`, were preserved rather than silently modernized. |
| `BC-0703` | Description; transcript; contributor review provenance | `Swadi Nitibon` | `Swasdi Nitibhon` | The user approved `Swasdi Nitibhon` as the canonical spelling and directed that `Nitibhom` not be preserved. Contributors remain null because the foreword discusses Nitibhon and his group but was not written by or addressed to him. |
| `BC-0710` | Place | `Massachusetts--Glouchester` | `Massachusetts--Gloucester` | The user approved the controlled-vocabulary spelling for search and discovery. The literal transcript and raw evidence retain `Glouchester`. Broader place-policy work is outside this handoff. |
| `BC-0713` | Title; date; transcript; title-derivation context | `28 February 1942`; `1942-02-28` | `26 February 1942`; `1942-02-26` | The source image shows `February 26th, 1942`. Top-level metadata, Tier 1, transcript, and title-derivation context were synchronized. |
| `BC-0934` | Contributors; correspondents; transcript | `Ernest H. Hahm`; `Rose Choi`; `10-254 Yon Am-Dong` | `Ernest H. Hahne`; `Rosa Choi`; `18-254 Ton Am-Dong` | The user approved all three readings and confirmed that Rosa Choi belongs in correspondents. Carol L. Anderson and Paul F. Erwin remain contributors. |

## Representation and provenance handling

- Every corrected top-level metadata field was mirrored to its corresponding `metadata_tiers.tier1` field.
- Corrected fields carry dated human-review provenance.
- Each affected record contains a dated `context.human_corrections` entry.
- Validation context was recomputed after correction.
- The 19 raw companion `.json` files remain byte-for-byte copies of the stable baseline and serve as original machine-output evidence.
- Unrelated, pre-existing differences between top-level metadata and tier proposal fields were inherited unchanged. Resolving those differences would be a separate metadata-policy decision, not part of these five approved corrections.

## Scope boundaries

- No wholesale OCR-v2 adoption or model rerun.
- No broad summary rewrite. The only summary change is the approved name spelling in `BC-0703`.
- No broad place-policy revision.
- No change to `BC-0698` title or other page-level metadata.
- No addition of Swasdi Nitibhon to contributors.
- No edit to `out/` or the July 7 frozen baseline.

## Expected validation exception

Core validation reports no errors. Evidence QA reports one expected warning for `BC-0710`: the searchable controlled place is `Massachusetts--Gloucester`, while the source-faithful transcript says `Glouchester, Massachusetts`. This warning is retained as evidence of the deliberate normalization and is not suppressed.
