#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


WORD_RE = re.compile(r"[A-Za-z0-9]+")
VAGUE_PATTERNS = [
    "the document discusses",
    "this document discusses",
    "the document is about",
    "this document is about",
]


def _normalize_item_id(value: str) -> str:
    stem = Path(str(value).strip()).stem
    if stem.endswith(".loc15"):
        stem = stem[: -len(".loc15")]
    if stem.endswith("_Recto"):
        stem = stem[: -len("_Recto")]
    return stem


def _first_header_index(headers: List[str], name: str) -> Optional[int]:
    try:
        return headers.index(name)
    except ValueError:
        return None


def _csv_cell(row: List[str], index: Optional[int]) -> str:
    if index is None or index >= len(row):
        return ""
    return row[index].strip()


def _load_human_rows(path: Path) -> Dict[str, Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        headers = next(reader)
        indexes = {
            "identifier": _first_header_index(headers, "Identifier"),
            "title": _first_header_index(headers, "Title"),
            "summary": _first_header_index(headers, "Summary"),
            "creator": _first_header_index(headers, "Creator"),
            "date": _first_header_index(headers, "Date"),
            "location": _first_header_index(headers, "Location"),
            "genre": _first_header_index(headers, "Genre"),
        }
        if indexes["identifier"] is None or indexes["summary"] is None:
            raise ValueError("Human CSV must contain Identifier and Summary columns.")

        rows: Dict[str, Dict[str, str]] = {}
        for row in reader:
            identifier = _normalize_item_id(_csv_cell(row, indexes["identifier"]))
            summary = _csv_cell(row, indexes["summary"])
            if not identifier:
                continue
            rows[identifier] = {
                "Identifier": identifier,
                "Human Title": _csv_cell(row, indexes["title"]),
                "Human Creator": _csv_cell(row, indexes["creator"]),
                "Human Date": _csv_cell(row, indexes["date"]),
                "Human Location": _csv_cell(row, indexes["location"]),
                "Human Genre": _csv_cell(row, indexes["genre"]),
                "Human Summary": summary,
            }
    return rows


def _load_json_outputs(out_dir: Path) -> Dict[str, Dict[str, Any]]:
    outputs: Dict[str, Dict[str, Any]] = {}
    if not out_dir.exists():
        return outputs
    for path in sorted(out_dir.glob("*.loc15.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        outputs[_normalize_item_id(path.name)] = payload
    return outputs


def _description(payload: Optional[Dict[str, Any]]) -> str:
    if not payload:
        return ""
    metadata = payload.get("metadata") or {}
    return str(metadata.get("description") or "")


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text or ""))


def _tokens(text: str) -> set:
    return {match.group(0).lower() for match in WORD_RE.finditer(text or "") if len(match.group(0)) > 2}


def _jaccard(a: str, b: str) -> float:
    a_tokens = _tokens(a)
    b_tokens = _tokens(b)
    if not a_tokens and not b_tokens:
        return 1.0
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def _validation_counts(payload: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    if not payload:
        return 0, 0
    context = payload.get("context") or {}
    errors = 1 if context.get("validation_error") else 0
    warnings = 0
    for source in ("validation_core", "validation_evidence_qc", "validation_online"):
        block = context.get(source) or {}
        errors += len(block.get("errors") or [])
        warnings += len(block.get("warnings") or [])
    return errors, warnings


def _flags(summary: str, errors: int, warnings: int) -> str:
    flags: List[str] = []
    word_count = _word_count(summary)
    lowered = summary.lower()
    if not summary:
        flags.append("missing_summary")
    if summary and word_count < 40:
        flags.append("shorter_than_40_words")
    if len(summary) > 1000:
        flags.append("schema_limit_risk_over_1000_chars")
    if any(pattern in lowered for pattern in VAGUE_PATTERNS):
        flags.append("vague_opening")
    if errors:
        flags.append("validation_errors")
    if warnings:
        flags.append("validation_warnings")
    return "; ".join(flags)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare baseline and few-shot AI summaries against human summaries.")
    parser.add_argument(
        "--human-csv",
        default=r"emailtemps\AAEM Metadata (Lived Experiences) - Phase1.csv",
        help="CSV containing approved human Summary values",
    )
    parser.add_argument("--baseline-dir", default="out", help="Directory containing baseline .loc15.json files")
    parser.add_argument(
        "--fewshot-dir",
        default="out_fewshot_summary_test",
        help="Directory containing few-shot .loc15.json files",
    )
    parser.add_argument("--output", default="out/summary_fewshot_comparison.csv", help="Output comparison CSV")
    args = parser.parse_args()

    human_rows = _load_human_rows(Path(args.human_csv))
    baseline = _load_json_outputs(Path(args.baseline_dir))
    fewshot = _load_json_outputs(Path(args.fewshot_dir))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "Identifier",
        "Human Title",
        "Human Creator",
        "Human Date",
        "Human Location",
        "Human Genre",
        "Human Summary",
        "Baseline AI Summary",
        "Few-Shot AI Summary",
        "Human word count",
        "Baseline word count",
        "Few-shot word count",
        "Baseline length delta vs human",
        "Few-shot length delta vs human",
        "Baseline lexical similarity to human",
        "Few-shot lexical similarity to human",
        "Few-shot validation errors",
        "Few-shot validation warnings",
        "Automatic flags",
        "Tone/style match score baseline (1-5)",
        "Tone/style match score few-shot (1-5)",
        "Specificity score baseline (1-5)",
        "Specificity score few-shot (1-5)",
        "Factual grounding score baseline (1-5)",
        "Factual grounding score few-shot (1-5)",
        "Readability score baseline (1-5)",
        "Readability score few-shot (1-5)",
        "Cataloging usefulness score baseline (1-5)",
        "Cataloging usefulness score few-shot (1-5)",
        "Winner",
        "Notes",
    ]

    rows: List[Dict[str, Any]] = []
    for identifier in sorted(human_rows):
        human_summary = human_rows[identifier]["Human Summary"]
        baseline_summary = _description(baseline.get(identifier))
        fewshot_payload = fewshot.get(identifier)
        fewshot_summary = _description(fewshot_payload)
        fewshot_errors, fewshot_warnings = _validation_counts(fewshot_payload)

        human_wc = _word_count(human_summary)
        baseline_wc = _word_count(baseline_summary)
        fewshot_wc = _word_count(fewshot_summary)
        row = {
            **human_rows[identifier],
            "Baseline AI Summary": baseline_summary,
            "Few-Shot AI Summary": fewshot_summary,
            "Human word count": human_wc,
            "Baseline word count": baseline_wc,
            "Few-shot word count": fewshot_wc,
            "Baseline length delta vs human": baseline_wc - human_wc,
            "Few-shot length delta vs human": fewshot_wc - human_wc,
            "Baseline lexical similarity to human": f"{_jaccard(baseline_summary, human_summary):.3f}",
            "Few-shot lexical similarity to human": f"{_jaccard(fewshot_summary, human_summary):.3f}",
            "Few-shot validation errors": fewshot_errors,
            "Few-shot validation warnings": fewshot_warnings,
            "Automatic flags": _flags(fewshot_summary, fewshot_errors, fewshot_warnings),
            "Tone/style match score baseline (1-5)": "",
            "Tone/style match score few-shot (1-5)": "",
            "Specificity score baseline (1-5)": "",
            "Specificity score few-shot (1-5)": "",
            "Factual grounding score baseline (1-5)": "",
            "Factual grounding score few-shot (1-5)": "",
            "Readability score baseline (1-5)": "",
            "Readability score few-shot (1-5)": "",
            "Cataloging usefulness score baseline (1-5)": "",
            "Cataloging usefulness score few-shot (1-5)": "",
            "Winner": "",
            "Notes": "",
        }
        rows.append(row)

    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} comparison rows to {output_path}")
    print(f"Human summaries: {len(human_rows)}")
    print(f"Baseline outputs matched: {sum(1 for identifier in human_rows if identifier in baseline)}")
    print(f"Few-shot outputs matched: {sum(1 for identifier in human_rows if identifier in fewshot)}")


if __name__ == "__main__":
    main()
