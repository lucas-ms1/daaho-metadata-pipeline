#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path
from typing import Iterable, List, Set, Tuple

FAST_PLACE_PATTERN = re.compile(r"^[^;]+--[^;]+$")
DC_CANONICAL = "District of Columbia--Washington"
DC_VARIANTS = {
    "washington (d.c.)": DC_CANONICAL,
    "washington d.c.": DC_CANONICAL,
    "washington dc": DC_CANONICAL,
    "united states--washington d.c.": DC_CANONICAL,
}


def _split_semicolon(value: str) -> List[str]:
    return [token.strip() for token in value.split(";") if token.strip()]


def _canonicalize_place(token: str) -> str:
    collapsed = " ".join(token.strip().split())
    mapped = DC_VARIANTS.get(collapsed.lower())
    if mapped:
        return mapped
    return collapsed


def _read_rows(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield row


def _write_list(path: Path, values: Set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(sorted(values)) + "\n"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build deterministic local FAST place/subject lists from reviewed CSV.")
    parser.add_argument("--input-csv", required=True, help="Path to reviewed metadata CSV")
    parser.add_argument("--out-places", default="vocab/fast_places.txt", help="Output path for approved place list")
    parser.add_argument("--out-subjects", default="vocab/fast_subjects.txt", help="Output path for approved subject list")
    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    places: Set[str] = set()
    subjects: Set[str] = set()
    dropped_places: Set[str] = set()
    canonicalized: Set[Tuple[str, str]] = set()

    for row in _read_rows(input_csv):
        raw_place = (row.get("Location") or "").strip()
        for token in _split_semicolon(raw_place):
            canonical = _canonicalize_place(token)
            if canonical != token:
                canonicalized.add((token, canonical))
            if FAST_PLACE_PATTERN.match(canonical):
                places.add(canonical)
            else:
                dropped_places.add(token)

        raw_subjects = (row.get("Subject (FAST)") or "").strip()
        for token in _split_semicolon(raw_subjects):
            subjects.add(" ".join(token.split()))

    out_places = Path(args.out_places)
    out_subjects = Path(args.out_subjects)
    _write_list(out_places, places)
    _write_list(out_subjects, subjects)

    print(f"Wrote {len(places)} approved places to {out_places}")
    print(f"Wrote {len(subjects)} approved subjects to {out_subjects}")
    if canonicalized:
        print("Canonicalized place variants:")
        for src, dst in sorted(canonicalized):
            print(f"  {src} -> {dst}")
    if dropped_places:
        print("Dropped non FAST-style place tokens:")
        for token in sorted(dropped_places):
            print(f"  {token}")


if __name__ == "__main__":
    main()
