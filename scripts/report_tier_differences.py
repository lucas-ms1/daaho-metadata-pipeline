#!/usr/bin/env python3
"""Report differences between authoritative top-level metadata and tier values."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELDS_BY_TIER = {
    "tier1": [
        "transcript", "text_reading", "description", "title", "generated_title", "date",
        "contributors", "correspondents", "place", "keywords", "decade",
    ],
    "tier2": ["subjects", "genre", "creator", "publisher", "theme"],
    "tier3": [
        "rights", "repository", "collection", "series", "folder", "box", "identifier",
        "call_number", "digital_identifier", "reproduction_number", "permalink",
        "digital_collection", "digital_publisher", "digitized",
    ],
}
HEADERS = ["record", "tier", "field", "top_level_value", "tier_value"]


def render(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def collect_differences(metadata_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(metadata_dir.glob("*.loc15.json")):
        envelope = json.loads(path.read_text(encoding="utf-8"))
        metadata = envelope.get("metadata") or {}
        tiers = envelope.get("metadata_tiers") or {}
        for tier_name, fields in FIELDS_BY_TIER.items():
            tier = tiers.get(tier_name) or {}
            for field in fields:
                top_value = metadata.get(field)
                tier_value = tier.get(field)
                if top_value != tier_value:
                    rows.append(
                        {
                            "record": path.name.replace("_Recto.loc15.json", ""),
                            "tier": tier_name,
                            "field": field,
                            "top_level_value": render(top_value),
                            "tier_value": render(tier_value),
                        }
                    )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-dir", type=Path, default=Path("out_manual_corrections_2026-08-24"))
    parser.add_argument("--output", type=Path, default=Path("handoff/TIER_DIFFERENCE_REPORT_2026-08-28.csv"))
    args = parser.parse_args()

    rows = collect_differences(args.metadata_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} field differences across {len({row['record'] for row in rows})} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
