import os, json, base64
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from .schema import (
    LOC15_SCHEMA,
    MAX_OCR_CHARS,
    MAX_OUTPUT_TOKENS,
    DEFAULT_MODEL,
    TIER1_FIELDS,
    TIER2_FIELDS,
    TIER3_FIELDS,
    TIER3_DEFAULTABLE_FIELDS,
    FIELD_PROVENANCE_LABELS,
)

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

PROMPT_VERSION = "loc15_v1"
_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_SYSTEM_PROMPT_PATH = _PROMPTS_DIR / f"{PROMPT_VERSION}_system.txt"
_USER_PROMPT_PATH = _PROMPTS_DIR / f"{PROMPT_VERSION}_user.txt"
_CACHED_SYSTEM_PROMPT: Optional[str] = None
_CACHED_USER_PROMPT: Optional[str] = None


def _load_prompt(path: Path) -> str:
    if not path.exists():
        raise RuntimeError(f"Prompt file missing: {path}. Ensure prompts/ exists in the repo root.")
    return path.read_text(encoding="utf-8")


def _get_prompts() -> Tuple[str, str]:
    global _CACHED_SYSTEM_PROMPT, _CACHED_USER_PROMPT
    if _CACHED_SYSTEM_PROMPT is None:
        _CACHED_SYSTEM_PROMPT = _load_prompt(_SYSTEM_PROMPT_PATH)
    if _CACHED_USER_PROMPT is None:
        _CACHED_USER_PROMPT = _load_prompt(_USER_PROMPT_PATH)
    return _CACHED_SYSTEM_PROMPT, _CACHED_USER_PROMPT


def _get_client() -> OpenAI:
    if OpenAI is None:
        raise RuntimeError("openai not installed. pip install openai")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI()

def _clean_metadata(md: Dict[str, Any]) -> Dict[str, Any]:
    """Post-process metadata to fix common issues."""
    import re
    
    # Fix date field - handle "\\" or invalid dates
    if "date" in md and md["date"]:
        date_val = str(md["date"]).strip()
        # If it's just backslashes or invalid, try to extract from title or set to null
        if date_val in ["\\", "\\\\", ""] or not re.match(r"^(\d{4}(-\d{2}(-\d{2})?)?|undated)$", date_val):
            # Try to extract date from title if it contains one
            title = md.get("title", "")
            date_match = re.search(r"(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4})", title)
            if date_match:
                md["date"] = date_match.group(1)
            else:
                md["date"] = "undated"
    
    # Fix subjects - split semicolon-separated strings into arrays
    if "subjects" in md and md["subjects"]:
        if isinstance(md["subjects"], list):
            new_subjects = []
            for subj in md["subjects"]:
                if isinstance(subj, str) and ";" in subj:
                    # Split semicolon-separated string
                    split_subjects = [s.strip() for s in subj.split(";") if s.strip()]
                    new_subjects.extend(split_subjects)
                elif isinstance(subj, str) and subj.strip():
                    new_subjects.append(subj.strip())
            md["subjects"] = [s for s in new_subjects if s] if new_subjects else None
        elif isinstance(md["subjects"], str):
            # Convert string to array
            md["subjects"] = [s.strip() for s in md["subjects"].split(";") if s.strip()] or None
    
    # Remove broken/empty subject entries
    if "subjects" in md and isinstance(md["subjects"], list):
        md["subjects"] = [s for s in md["subjects"] if s and len(s.strip()) > 1 and not s.strip().startswith(";")]
    
    # Fix genre - same as subjects
    if "genre" in md and md["genre"]:
        if isinstance(md["genre"], list):
            new_genre = []
            for gen in md["genre"]:
                if isinstance(gen, str) and ";" in gen:
                    split_genre = [g.strip() for g in gen.split(";") if g.strip()]
                    new_genre.extend(split_genre)
                elif isinstance(gen, str) and gen.strip():
                    new_genre.append(gen.strip())
            md["genre"] = [g for g in new_genre if g] if new_genre else None
        elif isinstance(md["genre"], str):
            md["genre"] = [g.strip() for g in md["genre"].split(";") if g.strip()] or None

    # Fix keywords - same as subjects
    if "keywords" in md and md["keywords"]:
        if isinstance(md["keywords"], list):
            new_keywords = []
            for kw in md["keywords"]:
                if isinstance(kw, str) and ";" in kw:
                    split_keywords = [k.strip() for k in kw.split(";") if k.strip()]
                    new_keywords.extend(split_keywords)
                elif isinstance(kw, str) and kw.strip():
                    new_keywords.append(kw.strip())
            md["keywords"] = [k for k in new_keywords if k] if new_keywords else None
        elif isinstance(md["keywords"], str):
            md["keywords"] = [k.strip() for k in md["keywords"].split(";") if k.strip()] or None
    
    return md

def _extract_decade(date_value: Optional[str]) -> Optional[str]:
    if not date_value or date_value == "undated":
        return None
    try:
        year = int(str(date_value).split("-")[0])
    except (ValueError, IndexError):
        return None
    decade_start = (year // 10) * 10
    return f"{decade_start}-{decade_start + 9}"

def apply_tier_policy(
    md: Dict[str, Any],
    defaults: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]], Dict[str, str], List[str]]:
    defaults = defaults or {}
    policy_notes: List[str] = []

    allowed_defaults = {
        field: defaults[field]
        for field in TIER3_DEFAULTABLE_FIELDS
        if field in defaults and defaults[field] not in [None, ""]
    }

    for field in TIER3_FIELDS:
        val = md.get(field)
        default_val = allowed_defaults.get(field)
        if default_val is not None:
            if val != default_val:
                md[field] = default_val
                policy_notes.append(f"Applied tier3 default for '{field}'.")
            continue
        if val is None or val == "" or val == [] or val == {}:
            continue
        md[field] = None
        policy_notes.append(f"Cleared tier3 field '{field}' generated by model.")

    decade = _extract_decade(md.get("date")) or md.get("decade")
    if decade and not md.get("decade"):
        md["decade"] = decade

    tier1: Dict[str, Any] = {}
    for field in TIER1_FIELDS:
        if field == "decade":
            tier1[field] = decade
        else:
            tier1[field] = md.get(field)

    tier2 = {field: md.get(field) for field in TIER2_FIELDS}
    tier3 = {field: md.get(field) for field in TIER3_FIELDS}

    field_provenance: Dict[str, str] = {}
    for field in TIER1_FIELDS + TIER2_FIELDS + TIER3_FIELDS:
        field_provenance[field] = FIELD_PROVENANCE_LABELS.get(field, "AI-Generated")

    metadata_tiers = {"tier1": tier1, "tier2": tier2, "tier3": tier3}
    return md, metadata_tiers, field_provenance, policy_notes


def apply_review_overrides(md: Dict[str, Any], review: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    overrides = review.get("overrides") or {}
    notes: List[str] = []
    for field in TIER2_FIELDS:
        if field not in overrides:
            continue
        override_val = overrides.get(field)
        if isinstance(override_val, str):
            override_val = override_val.strip()
            if override_val == "":
                override_val = None
        if field in {"subjects", "theme", "genre"}:
            if isinstance(override_val, str):
                parts = [v.strip() for v in override_val.replace("\n", ";").split(";") if v.strip()]
                override_val = parts or None
            elif isinstance(override_val, list):
                cleaned = [str(v).strip() for v in override_val if str(v).strip()]
                override_val = cleaned or None
            else:
                override_val = None
        md[field] = override_val
        notes.append(f"Applied review override for '{field}'.")
    return md, notes

def _image_to_data_url(img_bytes: bytes) -> str:
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def transcribe_with_model(img_bytes: bytes, max_chars: int = MAX_OCR_CHARS, model: str = DEFAULT_MODEL) -> str:
    client = _get_client()
    data_url = _image_to_data_url(img_bytes)
    resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Transcribe ALL visible text. Preserve line breaks; prefix clearly handwritten lines with '[handwritten] '. Use '[illegible]'/'[unclear]' for unreadable parts. Return PLAIN TEXT only."},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }],
        temperature=0,
        max_tokens=900,
    )
    text = (resp.choices[0].message.content or "").strip()
    return text[:max_chars]

def extract_metadata(img_bytes: bytes, ocr_text: str, filename: str, model: str = DEFAULT_MODEL, known_collection: str = "", known_repository: str = "", known_permalink: str = "") -> Dict[str, Any]:
    client = _get_client()
    data_url = _image_to_data_url(img_bytes)
    ocr_text = (ocr_text or "").strip()[:MAX_OCR_CHARS]

    system_prompt, user_prompt_template = _get_prompts()
    user_prompt = user_prompt_template.format(
        filename=filename,
        ocr_text=ocr_text if ocr_text else "(none)",
        known_collection=known_collection or "",
        known_repository=known_repository or "",
        known_permalink=known_permalink or "",
    )
    content: List[Dict[str, Any]] = [
        {"type": "text", "text": user_prompt},
        {"type": "image_url", "image_url": {"url": data_url}},
    ]

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": content}],
            temperature=0,
            top_p=1,
            presence_penalty=0,
            frequency_penalty=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "loc15_metadata",
                    "schema": LOC15_SCHEMA,
                    "strict": True,
                },
            },
            max_tokens=MAX_OUTPUT_TOKENS,
        )
        raw = resp.choices[0].message.content or "{}"
        try:
            parsed = json.loads(raw)
            if not parsed or len(parsed) == 0:
                print(f"WARNING: API returned empty metadata for {filename}. Raw response: {raw[:200]}")
                return {}
            
            # Clean the metadata
            parsed = _clean_metadata(parsed)
            return parsed
        except json.JSONDecodeError as parse_err:
            print(f"WARNING: JSON parse error for {filename}: {parse_err}")
            # Try to extract JSON from the response
            i, j = raw.find("{"), raw.rfind("}")
            if i >= 0 and j > i:
                try:
                    parsed = json.loads(raw[i:j+1])
                    parsed = _clean_metadata(parsed)
                    return parsed
                except:
                    pass
            print(f"ERROR: Could not recover JSON for {filename}")
            return {}
    except Exception as e:
        print(f"ERROR extracting metadata for {filename}: {e}")
        return {}
