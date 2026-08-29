import json

import pytest
from PIL import Image

from app import main


def _metadata(transcript):
    return {
        "title": "Test letter, 1937",
        "creator": None,
        "contributors": None,
        "correspondents": None,
        "publisher": None,
        "date": "1937",
        "place": None,
        "language": "English",
        "subjects": ["Education"],
        "theme": None,
        "genre": ["Correspondence"],
        "keywords": None,
        "decade": "1930-1939",
        "description": "A test description.",
        "collection": None,
        "series": None,
        "folder": None,
        "box": None,
        "format": None,
        "medium": None,
        "type": None,
        "rights": None,
        "repository": None,
        "identifier": None,
        "call_number": None,
        "digital_identifier": None,
        "reproduction_number": None,
        "permalink": None,
        "digital_collection": None,
        "digital_publisher": None,
        "digitized": None,
        "transcript": transcript,
        "text_reading": None,
        "generated_title": None,
        "field_confidence": {},
    }


def _run_process(tmp_path, monkeypatch, extracted_transcript):
    image_path = tmp_path / "BC-TEST_Recto.jpg"
    Image.new("RGB", (2, 2), "white").save(image_path)
    output_dir = tmp_path / "output"

    monkeypatch.setattr(
        main,
        "tesseract_ocr",
        lambda _path: ("Usable local OCR transcript text.", 91.0),
    )
    monkeypatch.setattr(main, "pil_bytes", lambda _path: b"image-bytes")
    monkeypatch.setattr(
        main,
        "transcribe_with_model",
        lambda *_args, **_kwargs: pytest.fail("paid OCR fallback must not run"),
    )
    monkeypatch.setattr(
        main,
        "extract_metadata",
        lambda *_args, **_kwargs: _metadata(extracted_transcript),
    )

    main.process_path(
        path=str(image_path),
        out_dir=str(output_dir),
        collection="",
        repository="",
        permalink="",
        model="test-metadata-model",
        ocr_model="test-ocr-model",
        approved_places=set(),
        approved_subjects=set(),
        approved_genre=set(),
        online_vocab_advisory=False,
    )
    return json.loads((output_dir / "BC-TEST_Recto.loc15.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("blank_transcript", ["", None])
def test_process_path_assigns_usable_ocr_when_extraction_transcript_is_blank(
    tmp_path, monkeypatch, blank_transcript
):
    envelope = _run_process(tmp_path, monkeypatch, blank_transcript)

    assert envelope["metadata"]["transcript"] == "Usable local OCR transcript text."
    assert envelope["metadata_tiers"]["tier1"]["transcript"] == "Usable local OCR transcript text."
    assert envelope["context"]["transcript_assignment"] == {
        "source": "ocr_fallback",
        "fallback_used": True,
        "ocr_source": "tesseract",
    }
    assert "process_path fallback" in envelope["field_provenance"]["transcript"]


def test_process_path_preserves_nonblank_extracted_transcript(tmp_path, monkeypatch):
    envelope = _run_process(tmp_path, monkeypatch, "Deliberate extracted transcript.")

    assert envelope["metadata"]["transcript"] == "Deliberate extracted transcript."
    assert envelope["metadata_tiers"]["tier1"]["transcript"] == "Deliberate extracted transcript."
    assert envelope["context"]["transcript_assignment"] == {
        "source": "metadata_extraction",
        "fallback_used": False,
        "ocr_source": "tesseract",
    }
    assert "metadata extraction" in envelope["field_provenance"]["transcript"]
