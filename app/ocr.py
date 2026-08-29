import io
import sys
from typing import Tuple
from PIL import Image, ImageOps
try:
    import pytesseract
except ImportError:
    pytesseract = None

_tesseract_warning_emitted = False


def _warn_tesseract_unavailable(reason: str) -> None:
    global _tesseract_warning_emitted
    if _tesseract_warning_emitted:
        return
    print(
        f"WARNING: Tesseract OCR unavailable ({reason}). Returning empty OCR; "
        "the caller may invoke a paid model fallback.",
        file=sys.stderr,
    )
    _tesseract_warning_emitted = True


def pil_bytes(img_path: str) -> bytes:
    with Image.open(img_path) as im:
        if im.mode not in ("RGB","RGBA"):
            im = im.convert("RGB")
        bio = io.BytesIO()
        im.save(bio, format="PNG")
        return bio.getvalue()

def tesseract_ocr(img_path: str) -> Tuple[str, float]:
    if pytesseract is None:
        _warn_tesseract_unavailable("pytesseract is not installed")
        return "", 0.0

    try:
        with Image.open(img_path) as im:
            gray = ImageOps.grayscale(im)
    except Exception:
        return "", 0.0

    try:
        text = pytesseract.image_to_string(gray)
    except Exception as exc:
        _warn_tesseract_unavailable(f"{type(exc).__name__}: {exc}")
        return "", 0.0

    try:
        alnum = sum(c.isalnum() for c in text)
        conf = min(95.0, max(5.0, (alnum / max(1, len(text))) * 100.0)) if text else 0.0
        return text, conf
    except Exception:
        return "", 0.0
