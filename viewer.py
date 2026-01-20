#!/usr/bin/env python3
"""
Flask-based metadata viewer for LOC15 JSON files and their corresponding images.
Usage: python3 viewer.py
Then open http://localhost:5000 in your browser
"""

import os
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory, request, abort

try:
    from app.vocab_validation import validate_fast_subject, validate_aat_genre
except Exception:
    validate_fast_subject = None
    validate_aat_genre = None

app = Flask(__name__)

# Configure paths
IMAGE_DIR = Path(__file__).parent / "_gdrive"
METADATA_DIR = Path(__file__).parent / "out"
REVIEW_SUFFIX = ".review.json"

ARRAY_FIELDS = {"subjects", "theme", "genre", "keywords", "contributors", "correspondents"}
REVIEW_FIELDS = {"subjects", "genre", "creator", "publisher", "theme"}


def _review_path(base_name: str) -> Path:
    return METADATA_DIR / f"{base_name}{REVIEW_SUFFIX}"


def _load_review(base_name: str) -> dict:
    review_path = _review_path(base_name)
    if not review_path.exists():
        return {}
    try:
        with open(review_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _normalize_review_payload(payload: dict) -> dict:
    reviewer = (payload.get("reviewer") or "").strip()
    status = (payload.get("status") or "").strip()
    notes = (payload.get("notes") or "").strip()
    overrides = payload.get("overrides") or {}

    normalized_overrides = {}
    for key, val in overrides.items():
        if key not in REVIEW_FIELDS:
            continue
        if key in ARRAY_FIELDS:
            if isinstance(val, str):
                parts = [v.strip() for v in val.replace("\n", ";").split(";") if v.strip()]
                normalized_overrides[key] = parts
            elif isinstance(val, list):
                normalized_overrides[key] = [str(v).strip() for v in val if str(v).strip()]
            else:
                normalized_overrides[key] = []
        else:
            normalized_overrides[key] = str(val).strip() if val is not None else ""

    return {
        "reviewer": reviewer,
        "status": status,
        "notes": notes,
        "overrides": normalized_overrides,
        "reviewed_at": datetime.utcnow().isoformat() + "Z",
    }

@app.route('/')
def index():
    """Main viewer page"""
    return render_template('viewer.html')

@app.route('/api/items')
def get_items():
    """Get all items with metadata"""
    items = []
    
    # Iterate through all JSON files in the output directory
    if METADATA_DIR.exists():
        for json_file in sorted(METADATA_DIR.glob("*.loc15.json")):
            # Extract the base filename (e.g., BC-0692_Recto)
            base_name = json_file.stem.replace(".loc15", "")
            
            # Check if corresponding image exists
            image_path = None
            for ext in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
                img_file = IMAGE_DIR / f"{base_name}{ext}"
                if img_file.exists():
                    image_path = f"/images/{base_name}{ext}"
                    break
            
            # Read metadata
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                review = _load_review(base_name)
                items.append({
                    'id': base_name,
                    'image': image_path,
                    'metadata': data.get('metadata', {}),
                    'metadata_tiers': data.get('metadata_tiers', {}),
                    'field_provenance': data.get('field_provenance', {}),
                    'context': data.get('context', {}),
                    'review': review,
                    'filename': base_name
                })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
    
    return jsonify(items)

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve images from the _gdrive directory"""
    return send_from_directory(IMAGE_DIR, filename)


@app.route('/api/review/<item_id>', methods=['GET'])
def get_review(item_id):
    review = _load_review(item_id)
    if not review:
        return jsonify({})
    return jsonify(review)


@app.route('/api/review/<item_id>', methods=['POST'])
def save_review(item_id):
    if not request.is_json:
        abort(400)
    payload = request.get_json() or {}
    normalized = _normalize_review_payload(payload)
    review_path = _review_path(item_id)
    try:
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=2, ensure_ascii=False)
    except Exception:
        abort(500)
    return jsonify({"ok": True, "review": normalized})


@app.route('/api/vocab/fast/search', methods=['GET'])
def search_fast():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"suggestions": []})
    if validate_fast_subject is None:
        return jsonify({"suggestions": [], "error": "Vocabulary lookup not available."}), 503
    result = validate_fast_subject(query)
    suggestions = [{"term": term} for term in result.get("suggestions", [])]
    return jsonify({"suggestions": suggestions})


@app.route('/api/vocab/aat/search', methods=['GET'])
def search_aat():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"suggestions": []})
    if validate_aat_genre is None:
        return jsonify({"suggestions": [], "error": "Vocabulary lookup not available."}), 503
    result = validate_aat_genre(query)
    suggestions = [{"term": term} for term in result.get("suggestions", [])]
    return jsonify({"suggestions": suggestions})


@app.route('/api/vocab/fast/validate', methods=['GET'])
def validate_fast():
    term = (request.args.get("term") or "").strip()
    if not term:
        return jsonify({"valid": False, "suggestions": [], "error": "Empty term."}), 400
    if validate_fast_subject is None:
        return jsonify({"valid": False, "suggestions": [], "error": "Vocabulary lookup not available."}), 503
    result = validate_fast_subject(term)
    return jsonify({
        "valid": result.get("valid", False),
        "suggestions": result.get("suggestions", []),
        "exact_match": result.get("exact_match", False),
        "error": result.get("error"),
    })


@app.route('/api/vocab/aat/validate', methods=['GET'])
def validate_aat():
    term = (request.args.get("term") or "").strip()
    if not term:
        return jsonify({"valid": False, "suggestions": [], "error": "Empty term."}), 400
    if validate_aat_genre is None:
        return jsonify({"valid": False, "suggestions": [], "error": "Vocabulary lookup not available."}), 503
    result = validate_aat_genre(term)
    return jsonify({
        "valid": result.get("valid", False),
        "suggestions": result.get("suggestions", []),
        "exact_match": result.get("exact_match", False),
        "error": result.get("error"),
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🖼️  LOC15 Metadata Viewer")
    print("=" * 60)
    print(f"Images: {IMAGE_DIR}")
    print(f"Metadata: {METADATA_DIR}")
    print("\n📂 Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000)
