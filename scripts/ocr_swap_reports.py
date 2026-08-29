#!/usr/bin/env python3
import argparse
import csv
import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


METHODOLOGY = """## Methodology disclosure

- The LLM transcription model in the codebase before this run was `gpt-4o`, not `o4-mini`.
- LLM transcription was previously a fallback to Tesseract, not the primary OCR path.
- For this evaluation, LLM OCR was forced on all 19 images so the model swap affects every row.
"""


OCR_CHECKS: Dict[str, List[Dict[str, Any]]] = {
    "BC-0692": [
        {"field": "Title", "expected": "Itinerary"},
        {"field": "Transcript", "expected": "Nakaku", "bad": "Nakku"},
        {"field": "Transcript", "expected": "Straits Sett", "bad": "Straits Settlements"},
        {"field": "Transcript", "expected": "Bombay, India:", "bad": "Bombay, India\n"},
    ],
    "BC-0696": [
        {"field": "Title", "expected": "William N. Jardine", "bad": "William M. Jardine"},
        {"field": "Correspondents", "expected": "William N. Jardine", "bad": "William M. Jardine"},
        {"field": "Transcript", "expected": "William N. Jardine", "bad": "William M. Jardine"},
    ],
    "BC-0697": [
        {"field": "Correspondents", "expected": "Jean Van Ausdall", "bad": "Jeni Van Ausdal"},
        {"field": "Transcript", "expected": "Jean Van Ausdall", "bad": "Jeni Van Ausdal"},
        {"field": "Transcript", "expected": "Hosack's Studio", "bad": "Honack's Studio"},
        {"field": "Transcript", "expected": "good condition.", "bad": "good condition,"},
        {"field": "Transcript", "bad": "Dr. Heckert"},
        {"field": "Transcript", "bad": "Red Cross"},
        {"field": "Transcript", "bad": "Turkey tickets"},
    ],
    "BC-0698": [
        {"field": "Title", "expected": "Tosses His Dime", "bad": "Tosses his dime"},
        {"field": "Transcript", "expected_nonempty": True},
    ],
    "BC-0703": [
        {"field": "Transcript", "expected": "Swasdi Nitibhon", "bad": "Swadi Nitibon"},
    ],
    "BC-0708": [
        {"field": "Title", "expected": "COLLEGE AID LETTER #4", "bad": "College aid letter #4"},
        {"field": "Transcript", "expected": "Sincerly", "bad": "Sincerely yours,"},
    ],
    "BC-0710": [
        {"field": "Location", "expected": "Massachusetts--Gloucester", "bad": "Massachusetts--Glouchester"},
        {"field": "Transcript", "expected": "Wonsonhurst 59", "bad": "Monsonhurst 59"},
        {"field": "Transcript", "expected": "Gloucester, Massachusetts", "bad": "Glouchester, Massachusetts"},
    ],
    "BC-0711": [
        {"field": "Transcript", "expected": "If he can arrange", "bad": "If he will arrange"},
    ],
    "BC-0713": [
        {"field": "Title", "expected": "26 February 1942", "bad": "28 February 1942"},
        {"field": "Date", "expected": "1942-02-26", "bad": "1942-02-28"},
        {"field": "Transcript", "expected": "February 26th, 1942", "bad": "February 28th, 1942"},
    ],
    "BC-0716": [
        {"field": "Transcript", "expected": "STUDENTS' DEPARTMENT", "bad": "STUDENT'S DEPARTMENT"},
        {"field": "Transcript", "expected": "[unclear]", "bad": "Murry"},
    ],
    "BC-0926": [
        {"field": "Transcript", "expected": "WAR\nSAVINGS\nBONDS\nAND\nSTAMPS", "bad": "FOR VICTORY"},
    ],
    "BC-0934": [
        {"field": "Transcript", "expected": "Provisions for vacation", "bad": "Provision for vacation"},
        {"field": "Transcript", "expected": "Rosa Choi", "bad": "Rose Choi"},
        {"field": "Correspondents", "expected": "Ros", "bad": "Rose Choi"},
        {"field": "Transcript", "expected": "18-254 Ton Am-Dong", "bad": "10-254 Yon Am-Dong"},
    ],
}


OUT_OF_SCOPE_CHECKS: List[Tuple[str, str, str]] = [
    ("BC-0694", "Creator", "Creator"),
    ("BC-0695", "Creator", "Creator"),
    ("BC-0696", "Creator", "Creator"),
    ("BC-0699", "Creator", "Creator"),
    ("BC-0710", "Creator", "Creator"),
    ("BC-0711", "Creator", "Creator"),
    ("BC-0697", "Title", "Title"),
    ("BC-0697", "Date", "Date"),
    ("BC-0697", "Decade", "Decade"),
    ("BC-0697", "Transcript", "transcript newspaper bleed"),
    ("BC-0718", "Location", "Location"),
    ("BC-0718", "Transcript", "transcript handwritten"),
    ("BC-0934", "Contributors", "Contributors"),
]


def _norm_id(value: str) -> str:
    stem = Path(str(value).strip()).stem
    if stem.endswith(".loc15"):
        stem = stem[: -len(".loc15")]
    if stem.endswith("_Recto"):
        stem = stem[: -len("_Recto")]
    return stem


def _load_csv(path: Path) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        rows = {_norm_id(row.get("Identifier", "")): row for row in reader if row.get("Identifier")}
    return headers, rows


def _load_json_rows(out_dir: Path) -> Dict[str, Dict[str, Any]]:
    rows: Dict[str, Dict[str, Any]] = {}
    for path in sorted(out_dir.glob("*.loc15.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows[_norm_id(path.name)] = payload
    return rows


def _clean(value: Optional[str]) -> str:
    return " ".join((value or "").split())


def _quote(value: str, limit: int = 220) -> str:
    compact = _clean(value)
    if len(compact) > limit:
        compact = compact[: limit - 3].rstrip() + "..."
    return compact.replace('"', '\\"')


def _changed_spans(old: str, new: str) -> List[Tuple[str, str]]:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    spans: List[Tuple[str, str]] = []
    matcher = SequenceMatcher(a=old_lines, b=new_lines)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        old_span = "\n".join(old_lines[i1:i2]).strip()
        new_span = "\n".join(new_lines[j1:j2]).strip()
        if old_span or new_span:
            spans.append((_quote(old_span), _quote(new_span)))
        if len(spans) >= 5:
            break
    if not spans and old != new:
        spans.append((_quote(old), _quote(new)))
    return spans


def _write_diff(old_csv: Path, new_csv: Path, output: Path) -> None:
    old_headers, old_rows = _load_csv(old_csv)
    new_headers, new_rows = _load_csv(new_csv)
    headers = [header for header in old_headers if header in new_headers]
    ids = sorted(set(old_rows) | set(new_rows))

    lines: List[str] = [
        "# OCR swap CSV diff",
        "",
        METHODOLOGY.strip(),
        "",
        f"Old CSV: `{old_csv.as_posix()}`",
        f"New CSV: `{new_csv.as_posix()}`",
        "",
    ]

    for identifier in ids:
        old_row = old_rows.get(identifier, {})
        new_row = new_rows.get(identifier, {})
        changes: List[str] = []
        for header in headers:
            old_value = old_row.get(header, "")
            new_value = new_row.get(header, "")
            if old_value == new_value:
                continue
            if header == "Transcript":
                for old_span, new_span in _changed_spans(old_value, new_value):
                    changes.append(f'- transcript: "{old_span}" -> "{new_span}"')
            else:
                changes.append(f'- {header}: "{_quote(old_value)}" -> "{_quote(new_value)}"')
        if changes:
            lines.append(f"### {identifier}")
            lines.extend(changes)
            lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _field_value(row: Dict[str, str], field: str) -> str:
    return row.get(field, "") or ""


def _row_status(row: Dict[str, str], checks: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    passed = 0
    failed = 0
    notes: List[str] = []
    for check in checks:
        field = check["field"]
        value = _field_value(row, field)
        expected = check.get("expected")
        bad = check.get("bad")
        ok = True
        if check.get("expected_nonempty"):
            ok = bool(value.strip())
        if expected is not None and expected not in value:
            ok = False
        if bad is not None and bad in value:
            ok = False
        if ok:
            passed += 1
        else:
            failed += 1
        if expected:
            notes.append(f"{field}: expects `{_clean(expected)}`")
        elif bad:
            notes.append(f"{field}: should not contain `{_clean(bad)}`")
        elif check.get("expected_nonempty"):
            notes.append(f"{field}: should be non-empty")

    if failed == 0:
        status = "yes"
    elif passed > 0:
        status = "partial"
    else:
        status = "no"
    return status, notes


def _context_quote(row: Dict[str, str], checks: List[Dict[str, Any]]) -> str:
    transcript = row.get("Transcript", "")
    for check in checks:
        expected = check.get("expected")
        if expected and expected in transcript:
            index = transcript.find(expected)
            start = max(0, index - 70)
            end = min(len(transcript), index + len(expected) + 70)
            return _quote(transcript[start:end], limit=180)
    return _quote(transcript, limit=180)


def _observed_change(old_row: Dict[str, str], new_row: Dict[str, str], field: str) -> str:
    old_value = old_row.get(field, "") or ""
    new_value = new_row.get(field, "") or ""
    if old_value == new_value:
        return "unchanged"
    if not new_value.strip():
        return "now empty"
    return f'now: "{_quote(new_value)}"'


def _validation_counts(json_rows: Dict[str, Dict[str, Any]]) -> Tuple[int, int]:
    errors = 0
    warnings = 0
    for payload in json_rows.values():
        context = payload.get("context") or {}
        if context.get("validation_error"):
            errors += 1
        for source in ("validation_core", "validation_evidence_qc", "validation_online"):
            block = context.get(source) or {}
            errors += len(block.get("errors") or [])
            warnings += len(block.get("warnings") or [])
    return errors, warnings


def _write_jinming_check(old_csv: Path, new_csv: Path, out_dir: Path, output: Path) -> None:
    _, old_rows = _load_csv(old_csv)
    _, new_rows = _load_csv(new_csv)
    json_rows = _load_json_rows(out_dir)
    errors, warnings = _validation_counts(json_rows)

    lines: List[str] = [
        "# OCR swap Jinming check",
        "",
        METHODOLOGY.strip(),
        "",
        f"Validation findings in new JSON outputs: {errors} errors, {warnings} warnings.",
        "",
        "## OCR-error rows",
        "",
        "| Row | Status | Notes | Relevant span |",
        "|---|---|---|---|",
    ]

    for identifier in sorted(OCR_CHECKS):
        row = new_rows.get(identifier, {})
        status, notes = _row_status(row, OCR_CHECKS[identifier])
        quote = _context_quote(row, OCR_CHECKS[identifier])
        lines.append(f"| {identifier} | {status} | {'; '.join(notes)} | {quote} |")

    lines.extend(
        [
            "",
            "## Not addressed by OCR swap - flag for next round",
            "",
            "- BC-0694, BC-0695, BC-0696, BC-0699, BC-0710, BC-0711 Creator: suspected `Upham, Alfred H.` hallucination.",
            "- BC-0697 Title, Date, Decade, and transcript newspaper bleed: not treated as an OCR-model fix in this round.",
            "- BC-0718 Location and handwritten transcript content: suspected hallucination.",
            "- BC-0934 Contributors: suspected hallucinated contributors.",
            "",
            "## Out-of-scope rows - observed change after OCR swap",
            "",
            "| Row | Field | Observed change |",
            "|---|---|---|",
        ]
    )

    for identifier, field, label in OUT_OF_SCOPE_CHECKS:
        old_row = old_rows.get(identifier, {})
        new_row = new_rows.get(identifier, {})
        lines.append(f"| {identifier} | {label} | {_observed_change(old_row, new_row, field)} |")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _iter_items(out_dir: Path) -> Iterable[Path]:
    return sorted(out_dir.glob("*.loc15.json"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OCR model swap review reports.")
    parser.add_argument("--old-csv", default="out/final_metadata_2026-04-27_handoff.csv")
    parser.add_argument("--new-csv", default="out/final_metadata_2026-05-09_ocr-gpt54mini.csv")
    parser.add_argument("--new-json-dir", default="out_ocr_v2_gpt54mini")
    parser.add_argument("--diff-output", default="out/ocr_swap_diff_2026-05-09.md")
    parser.add_argument("--check-output", default="out/ocr_swap_jinming_check_2026-05-09.md")
    args = parser.parse_args()

    out_dir = Path(args.new_json_dir)
    count = len(list(_iter_items(out_dir)))
    if count != 19:
        raise RuntimeError(f"Expected 19 .loc15.json files in {out_dir}, found {count}.")

    _write_diff(Path(args.old_csv), Path(args.new_csv), Path(args.diff_output))
    _write_jinming_check(Path(args.old_csv), Path(args.new_csv), out_dir, Path(args.check_output))
    print(f"Wrote {args.diff_output}")
    print(f"Wrote {args.check_output}")


if __name__ == "__main__":
    main()
