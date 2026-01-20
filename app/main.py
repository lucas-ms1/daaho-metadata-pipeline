import os, json, argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

from .schema import LOC15_SCHEMA, SCHEMA_VERSION
from .ocr import tesseract_ocr, pil_bytes
from .ai_metadata import extract_metadata, transcribe_with_model, apply_tier_policy, apply_review_overrides, PROMPT_VERSION
try:
    from .gdrive import pull_files_from_folder
except ImportError:
    pull_files_from_folder = None

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except Exception:
    pass  # Fall back to system env vars if python-dotenv not available

try:
    from jsonschema import Draft7Validator
except Exception:
    Draft7Validator = None

def _validate(obj: Dict[str, Any]) -> str:
    if Draft7Validator is None:
        return ""
    v = Draft7Validator(LOC15_SCHEMA)
    errs = sorted(v.iter_errors(obj), key=lambda e: e.path)
    return "; ".join([f"{'.'.join(map(str, e.path))}: {e.message}" for e in errs])


def rebuild_existing_outputs(out_dir: str, defaults: Dict[str, Any], apply_reviews: bool, validate_vocab: bool) -> None:
    out_path = Path(out_dir)
    if not out_path.exists():
        print(f"No output directory found: {out_dir}")
        return
    for json_file in sorted(out_path.glob("*.loc15.json")):
        try:
            raw = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"✗ {json_file.name}: {exc}")
            continue
        md = raw.get("metadata", raw)
        context = raw.get("context", {})
        md, metadata_tiers, field_provenance, policy_notes = apply_tier_policy(md, defaults=defaults)
        if validate_vocab:
            from .vocab_validation import validate_metadata
            context["vocabulary_validation"] = validate_metadata(md)
        review_notes: List[str] = []
        if apply_reviews:
            review_path = out_path / f"{json_file.stem.replace('.loc15', '')}.review.json"
            if review_path.exists():
                try:
                    review_data = json.loads(review_path.read_text(encoding="utf-8"))
                    md, review_notes = apply_review_overrides(md, review_data)
                    md, metadata_tiers, field_provenance, policy_notes = apply_tier_policy(md, defaults=defaults)
                except Exception:
                    review_notes.append("Failed to apply review overrides.")
        if policy_notes or review_notes:
            context["policy_notes"] = policy_notes + review_notes
        context["schema_version"] = SCHEMA_VERSION
        context["rebuilt_from_existing"] = True
        envelope = {
            "metadata": md,
            "metadata_tiers": metadata_tiers,
            "field_provenance": field_provenance,
            "context": context,
        }
        err = _validate(md)
        if err:
            envelope["context"]["validation_error"] = err
        json_file.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Rebuilt {json_file.name}")

def _parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    val = str(value).strip().lower()
    if val in {"true", "1", "yes", "y"}:
        return True
    if val in {"false", "0", "no", "n"}:
        return False
    return None

def process_path(
    path: str,
    out_dir: str,
    collection: str,
    repository: str,
    permalink: str,
    model: str,
    output_ext: str = ".loc15.json",
    defaults: Optional[Dict[str, Any]] = None,
    overwrite: bool = False,
    apply_reviews: bool = False,
    validate_vocab: bool = False,
) -> None:
    p = Path(path)
    if not p.exists():
        print(f"Skip missing: {p}")
        return
    
    # Check if output already exists
    out = Path(out_dir) / f"{p.stem}{output_ext}"
    if out.exists() and not overwrite:
        print(f"⊘ Skipping {p.name} (already processed)")
        return
    
    print(f"Processing {p.name}...", end="", flush=True)
    
    # OCR first
    text, conf = tesseract_ocr(str(p))
    img_bytes = pil_bytes(str(p))
    if len(text.strip()) < 25:
        try:
            t = transcribe_with_model(img_bytes, model=model)
            if len(t) > len(text):
                text = t
                conf = max(conf, 85.0)
        except Exception:
            pass
    # AI metadata
    md = extract_metadata(
        img_bytes,
        text,
        filename=p.name,
        model=model,
        known_collection=collection,
        known_repository=repository,
        known_permalink=permalink,
    )
    policy_defaults = defaults or {}
    if collection:
        policy_defaults["collection"] = collection
    if repository:
        policy_defaults["repository"] = repository
    if permalink:
        policy_defaults["permalink"] = permalink
    md, metadata_tiers, field_provenance, policy_notes = apply_tier_policy(md, defaults=policy_defaults)
    review_notes: List[str] = []
    if apply_reviews:
        review_path = Path(out_dir) / f"{p.stem}.review.json"
        if review_path.exists():
            try:
                review_data = json.loads(review_path.read_text(encoding="utf-8"))
                md, review_notes = apply_review_overrides(md, review_data)
                md, metadata_tiers, field_provenance, policy_notes = apply_tier_policy(md, defaults=policy_defaults)
            except Exception:
                review_notes.append("Failed to apply review overrides.")
    # Envelope & validate
    context = {
        "filename": p.name,
        "processing_confidence": float(conf),
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "schema_version": SCHEMA_VERSION,
    }
    if validate_vocab:
        from .vocab_validation import validate_metadata
        context["vocabulary_validation"] = validate_metadata(md)
    if policy_notes or review_notes:
        context["policy_notes"] = policy_notes + review_notes
    if apply_reviews:
        context["review_applied"] = bool(review_notes)
    envelope = {
        "metadata": md,
        "metadata_tiers": metadata_tiers,
        "field_provenance": field_provenance,
        "context": context,
    }
    err = _validate(md)
    if err:
        envelope["context"]["validation_error"] = err
    # write
    os.makedirs(out_dir, exist_ok=True)
    out.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    print(" Done.")

def is_supported(name: str) -> bool:
    name = name.lower()
    return name.endswith((".png",".jpg",".jpeg",".tif",".tiff",".bmp",".gif",".webp",".pdf"))

def main():
    ap = argparse.ArgumentParser(description="mini_loc15: tiny OCR + AI LOC15 metadata pipeline")
    ap.add_argument("--in", dest="inp", default="", help="Local file or directory")
    ap.add_argument("--out", dest="out_dir", default="./out", help="Output directory")
    ap.add_argument("--gdrive", action="store_true", help="Fetch from Google Drive folder (env GDRIVE_FOLDER_ID) to a temp dir first")
    ap.add_argument("--samples", action="store_true", help="Process all .jpg files in SAMPLES/ folder")
    ap.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    ap.add_argument("--collection", default="", help="Known collection (Tier 3 default; optional)")
    ap.add_argument("--repository", default="", help="Known repository (Tier 3 default; optional)")
    ap.add_argument("--permalink", default="", help="Known permalink (Tier 3 default; optional)")
    ap.add_argument("--series", default="", help="Known series (Tier 3 default; optional)")
    ap.add_argument("--folder", default="", help="Known folder (Tier 3 default; optional)")
    ap.add_argument("--box", default="", help="Known box (Tier 3 default; optional)")
    ap.add_argument("--identifier", default="", help="Known identifier (Tier 3 default; optional)")
    ap.add_argument("--call-number", default="", help="Known call number (Tier 3 default; optional)")
    ap.add_argument("--digital-identifier", default="", help="Known digital identifier (Tier 3 default; optional)")
    ap.add_argument("--reproduction-number", default="", help="Known reproduction number (Tier 3 default; optional)")
    ap.add_argument("--digital-collection", default="", help="Known digital collection (Tier 3 default; optional)")
    ap.add_argument("--digital-publisher", default="", help="Known digital publisher (Tier 3 default; optional)")
    ap.add_argument("--digitized", default="", help="Known digitized flag (true/false; Tier 3 default; optional)")
    ap.add_argument("--dltemp", default="./_gdrive", help="Temp dir for Google Drive downloads")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs")
    ap.add_argument("--apply-reviews", action="store_true", help="Apply review overrides when generating outputs")
    ap.add_argument("--validate-vocab", action="store_true", help="Validate subjects/genre against FAST/AAT")
    ap.add_argument("--rebuild-from-existing", action="store_true", help="Rebuild envelopes from existing JSON outputs without re-running OCR/AI")
    args = ap.parse_args()

    paths: List[str] = []

    if args.gdrive:
        if pull_files_from_folder is None:
            raise RuntimeError("Google Drive support not available. Install google-api-python-client and google-auth-oauthlib.")
        folder_id = os.getenv("GDRIVE_FOLDER_ID", "")
        if not folder_id:
            raise RuntimeError("Set GDRIVE_FOLDER_ID when using --gdrive")
        dl = pull_files_from_folder(folder_id, args.dltemp)
        paths.extend([p for p in dl if is_supported(p)])

    if args.inp:
        p = Path(args.inp)
        if p.is_file() and is_supported(str(p)):
            paths.append(str(p))
        elif p.is_dir():
            for x in p.rglob("*"):
                if x.is_file() and is_supported(str(x)):
                    paths.append(str(x))

    # If no inputs specified, default to processing SAMPLES folder
    if not paths and not args.gdrive:
        args.samples = True

    if args.samples:
        # Try both uppercase and lowercase folder names
        samples_dir = Path("SAMPLES")
        if not samples_dir.exists():
            samples_dir = Path("samples")
        if samples_dir.exists():
            for img_file in sorted(samples_dir.glob("*.jpg")):
                if img_file.is_file():
                    paths.append(str(img_file))
        else:
            print(f"Warning: SAMPLES/samples directory not found")

    if not paths:
        print("No inputs. Use --in <path>, --samples, and/or --gdrive.")
        return

    defaults: Dict[str, Any] = {
        "series": args.series or None,
        "folder": args.folder or None,
        "box": args.box or None,
        "identifier": args.identifier or None,
        "call_number": args.call_number or None,
        "digital_identifier": args.digital_identifier or None,
        "reproduction_number": args.reproduction_number or None,
        "digital_collection": args.digital_collection or None,
        "digital_publisher": args.digital_publisher or None,
        "digitized": _parse_bool(args.digitized),
    }
    if args.collection:
        defaults["collection"] = args.collection
    if args.repository:
        defaults["repository"] = args.repository
    if args.permalink:
        defaults["permalink"] = args.permalink

    if args.rebuild_from_existing:
        rebuild_existing_outputs(args.out_dir, defaults, args.apply_reviews, args.validate_vocab)
        return

    for path in paths:
        try:
            process_path(
                path,
                args.out_dir,
                args.collection,
                args.repository,
                args.permalink,
                args.model,
                output_ext=".loc15.json",
                defaults=defaults,
                overwrite=args.overwrite,
                apply_reviews=args.apply_reviews,
                validate_vocab=args.validate_vocab,
            )
        except Exception as e:
            print(f"✗ {path}: {e}")

if __name__ == "__main__":
    main()
