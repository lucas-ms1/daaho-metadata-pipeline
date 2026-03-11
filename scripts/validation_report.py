#!/usr/bin/env python3
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _iter_items(out_dir: Path) -> Iterable[Path]:
    for path in sorted(out_dir.glob("*.loc15.json")):
        if path.is_file():
            yield path


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_json(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _collect_issues(
    source: str,
    severity: str,
    issues: List[Dict[str, Any]],
    filename: str,
    identifier: str,
) -> Iterable[Dict[str, str]]:
    for issue in issues:
        yield {
            "filename": filename,
            "identifier": identifier,
            "source": source,
            "severity": severity,
            "field": str(issue.get("field") or ""),
            "code": str(issue.get("code") or ""),
            "message": str(issue.get("message") or ""),
            "value": _as_json(issue.get("value")),
            "suggestions": _as_json(issue.get("suggestions")),
            "evidence": _as_json(issue.get("evidence")),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate deterministic validation findings from out/*.loc15.json")
    parser.add_argument("--out-dir", default="out", help="Directory containing .loc15.json files")
    parser.add_argument("--output", default="out/validation_report.csv", help="Output CSV file")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    output_csv = Path(args.output)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, str]] = []
    counts = Counter()

    for json_path in _iter_items(out_dir):
        try:
            payload = _load_json(json_path)
        except Exception as exc:
            print(f"Skipping {json_path.name}: {exc}")
            continue

        metadata = payload.get("metadata", {})
        context = payload.get("context", {})
        identifier = str(metadata.get("identifier") or json_path.stem.replace(".loc15", ""))
        filename = json_path.name

        core = context.get("validation_core") or {}
        evidence = context.get("validation_evidence_qc") or {}
        online = context.get("validation_online") or {}

        for row in _collect_issues("validation_core", "error", core.get("errors", []), filename, identifier):
            rows.append(row)
            counts[(row["source"], row["severity"], row["field"], row["code"])] += 1
        for row in _collect_issues("validation_core", "warning", core.get("warnings", []), filename, identifier):
            rows.append(row)
            counts[(row["source"], row["severity"], row["field"], row["code"])] += 1
        for row in _collect_issues("validation_evidence_qc", "error", evidence.get("errors", []), filename, identifier):
            rows.append(row)
            counts[(row["source"], row["severity"], row["field"], row["code"])] += 1
        for row in _collect_issues("validation_evidence_qc", "warning", evidence.get("warnings", []), filename, identifier):
            rows.append(row)
            counts[(row["source"], row["severity"], row["field"], row["code"])] += 1
        for row in _collect_issues("validation_online", "warning", online.get("warnings", []), filename, identifier):
            rows.append(row)
            counts[(row["source"], row["severity"], row["field"], row["code"])] += 1

    headers = [
        "filename",
        "identifier",
        "source",
        "severity",
        "field",
        "code",
        "message",
        "value",
        "suggestions",
        "evidence",
    ]
    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} findings to {output_csv}")
    if counts:
        print("Summary by source/severity/field/code:")
        for (source, severity, field, code), count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            print(f"  {count:3d}  {source} | {severity} | {field} | {code}")


if __name__ == "__main__":
    main()
