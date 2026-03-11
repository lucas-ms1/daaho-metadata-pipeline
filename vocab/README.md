# Local Controlled Vocabulary Lists

These files are deterministic, in-repo controlled lists used by offline validation:

- `fast_places.txt`: approved FAST-style place tokens (`State--City`)
- `fast_subjects.txt`: approved reviewed subject terms from `Subject (FAST)`

Regenerate from a reviewed metadata CSV:

```bash
python scripts/build_vocab_from_review_csv.py --input-csv "<path-to-reviewed-csv>" --out-places vocab/fast_places.txt --out-subjects vocab/fast_subjects.txt
```

Notes:
- Place canonicalization currently normalizes common Washington, D.C. variants to `District of Columbia--Washington`.
- Non FAST-style place tokens are dropped by the builder and printed in script output.
