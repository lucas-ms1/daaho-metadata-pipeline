# Known Issues

## Few-shot rebuild strips transcript field

- Observed: all 19 `out_fewshot_summary_test/*.loc15.json` files have empty `metadata.transcript`; `metadata.language` and other non-Summary fields are also often blank or changed. Baseline `out/*.loc15.json` has transcripts populated for 18 of 19 files.
- Suspected cause: `--rebuild-from-existing` dispatches from `main()` lines 775-785 into `rebuild_existing_outputs()` lines 405-493 in `app/main.py`. That function sets `md = raw.get("metadata", raw)`, reapplies policy, then writes a fresh `envelope = {"metadata": md, "metadata_tiers": ..., "field_provenance": ..., "context": ...}`; it does not merge back any top-level or tier fields not explicitly reconstructed.
- Why it matters: this blocks future use of `out_fewshot_summary_test/` as a metadata source and could silently strip transcripts on any future rebuild against any output set.
- Recommended fix: make the rebuild path start from the existing envelope and update only the fields it intentionally rewrites. Preserve all existing `metadata` keys, top-level keys, tiers, provenance, and context entries unless the rebuild step explicitly replaces them.
