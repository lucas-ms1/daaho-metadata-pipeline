from datetime import date as dt_date
from typing import Any, Dict, List, Optional, Tuple

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def parse_iso_date(date_str: Optional[str]) -> Tuple[Optional[str], Optional[int], Optional[int], Optional[int]]:
    """Parse YYYY / YYYY-MM / YYYY-MM-DD with strict calendar validity."""
    if date_str is None:
        return None, None, None, None

    value = str(date_str).strip()
    if value == "":
        return None, None, None, None

    parts = value.split("-")
    if len(parts) not in {1, 2, 3}:
        raise ValueError("Date must be YYYY, YYYY-MM, or YYYY-MM-DD.")

    if not all(part.isdigit() for part in parts):
        raise ValueError("Date contains non-numeric segments.")

    year = int(parts[0])
    if year < 1000 or year > 9999:
        raise ValueError("Year must be between 1000 and 9999.")

    if len(parts) == 1:
        return "year", year, None, None

    month = int(parts[1])
    if month < 1 or month > 12:
        raise ValueError("Month must be between 01 and 12.")

    if len(parts) == 2:
        return "month", year, month, None

    day = int(parts[2])
    try:
        dt_date(year, month, day)
    except ValueError as exc:
        raise ValueError(str(exc))
    return "day", year, month, day


def format_title_date_suffix(date_str: Optional[str]) -> Optional[str]:
    precision, year, month, day = parse_iso_date(date_str)
    if precision is None:
        return None
    if precision == "year":
        return f"{year}"
    if precision == "month":
        return f"{MONTH_NAMES[month]} {year}"
    return f"{day} {MONTH_NAMES[month]} {year}"


def derive_decade(date_str: Optional[str]) -> Optional[str]:
    try:
        precision, year, _, _ = parse_iso_date(date_str)
    except ValueError:
        return None
    if precision is None:
        return None
    decade_start = (year // 10) * 10
    return f"{decade_start}-{decade_start + 9}"


def apply_derivations(md: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    notes: List[str] = []
    llm_decade = md.get("decade")
    date_value = md.get("date")
    try:
        parse_iso_date(date_value)
    except ValueError:
        notes.append(f"Date '{date_value}' is invalid for derivation; derived decade set to null.")
    derived_decade = derive_decade(md.get("date"))
    md["decade"] = derived_decade
    if llm_decade not in [None, ""] and llm_decade != derived_decade:
        notes.append(
            f"LLM decade ignored; pipeline-derived decade '{derived_decade}' from date '{md.get('date')}'."
        )
    return md, notes


def derive_normalized_title(raw_title: Optional[str], date_value: Optional[str]) -> Tuple[Optional[str], List[str], bool]:
    """
    Deterministically normalize only the terminal title suffix from date.
    Does not infer date from title and does not rewrite title body content.
    """
    notes: List[str] = []
    if raw_title is None:
        notes.append("Raw title missing; normalized title not derived.")
        return None, notes, False

    title = str(raw_title).strip()
    if title == "":
        notes.append("Raw title empty; normalized title not derived.")
        return title, notes, False

    try:
        precision, _, _, _ = parse_iso_date(date_value)
    except ValueError:
        notes.append(f"Date '{date_value}' invalid; normalized title not derived.")
        return title, notes, False

    expected_suffix = "undated" if precision is None else (format_title_date_suffix(date_value) or "")
    if expected_suffix == "":
        notes.append("Expected suffix unavailable; normalized title not derived.")
        return title, notes, False

    if "," in title:
        body = title.rsplit(",", 1)[0].strip()
    else:
        body = title
    if body == "":
        notes.append("Title body empty after suffix split; normalized title not derived.")
        return title, notes, False

    normalized = f"{body}, {expected_suffix}"
    changed = normalized != title
    if changed:
        notes.append("Normalized title suffix deterministically from metadata.date.")
    return normalized, notes, changed
