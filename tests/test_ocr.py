from PIL import Image

from app import ocr


def test_missing_pytesseract_returns_empty_ocr_and_warns_once(monkeypatch, capsys):
    monkeypatch.setattr(ocr, "pytesseract", None)
    monkeypatch.setattr(ocr, "_tesseract_warning_emitted", False)

    assert ocr.tesseract_ocr("unused.jpg") == ("", 0.0)
    assert ocr.tesseract_ocr("unused.jpg") == ("", 0.0)

    stderr = capsys.readouterr().err
    assert stderr.count("Tesseract OCR unavailable") == 1
    assert "Returning empty OCR" in stderr
    assert "paid model fallback" in stderr


def test_unusable_tesseract_returns_empty_ocr_and_warns_once(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "image.png"
    Image.new("RGB", (2, 2), "white").save(image_path)

    class UnusableTesseract:
        @staticmethod
        def image_to_string(_image):
            raise RuntimeError("tesseract executable not found")

    monkeypatch.setattr(ocr, "pytesseract", UnusableTesseract())
    monkeypatch.setattr(ocr, "_tesseract_warning_emitted", False)

    assert ocr.tesseract_ocr(str(image_path)) == ("", 0.0)
    assert ocr.tesseract_ocr(str(image_path)) == ("", 0.0)

    stderr = capsys.readouterr().err
    assert stderr.count("Tesseract OCR unavailable") == 1
    assert "RuntimeError: tesseract executable not found" in stderr
    assert "paid model fallback" in stderr


def test_unreadable_image_does_not_claim_tesseract_is_unavailable(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "not-an-image.bin"
    image_path.write_bytes(b"not an image")

    class UncalledTesseract:
        @staticmethod
        def image_to_string(_image):
            raise AssertionError("Tesseract should not run when the image cannot be opened")

    monkeypatch.setattr(ocr, "pytesseract", UncalledTesseract())
    monkeypatch.setattr(ocr, "_tesseract_warning_emitted", False)

    assert ocr.tesseract_ocr(str(image_path)) == ("", 0.0)

    stderr = capsys.readouterr().err
    assert "Tesseract OCR unavailable" not in stderr
