import json

from app.main import rebuild_existing_outputs


def _metadata(**overrides):
    metadata = {
        "title": "Letter to Jane Smith, 1937",
        "creator": None,
        "contributors": ["Jane Smith"],
        "correspondents": ["John Doe"],
        "publisher": None,
        "date": "1937",
        "place": "Ohio--Oxford",
        "language": "English",
        "subjects": ["Education"],
        "theme": ["Student life"],
        "genre": ["Correspondence"],
        "keywords": ["student records"],
        "decade": "1930-1939",
        "description": "A short test description.",
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
        "transcript": "Original transcript text that must survive rebuild.",
        "text_reading": "Original text reading that must survive rebuild.",
        "generated_title": "Generated test title",
        "field_confidence": {},
    }
    metadata.update(overrides)
    return metadata


def test_rebuild_preserves_existing_envelope_fields(tmp_path):
    json_file = tmp_path / "BC-0001_Recto.loc15.json"
    envelope = {
        "metadata": _metadata(),
        "metadata_tiers": {
            "tier1": {
                "transcript": "Original transcript text that must survive rebuild.",
                "legacy_tier_note": "preserve tier sentinel",
            },
            "custom_tier": {"legacy_field": "preserve custom tier"},
        },
        "field_provenance": {
            "transcript": "Legacy transcript provenance",
            "legacy_field": "preserve provenance sentinel",
        },
        "context": {
            "legacy_context_note": "preserve context sentinel",
            "schema_version": "older_schema_version",
        },
        "top_level_sentinel": {"legacy": True},
    }
    json_file.write_text(json.dumps(envelope, indent=2), encoding="utf-8")

    rebuild_existing_outputs(
        out_dir=str(tmp_path),
        defaults={},
        apply_reviews=False,
        approved_places=set(),
        approved_subjects=set(),
        approved_genre=set(),
        online_vocab_advisory=False,
    )

    rebuilt = json.loads(json_file.read_text(encoding="utf-8"))
    metadata = rebuilt["metadata"]
    context = rebuilt["context"]

    assert metadata["transcript"] == "Original transcript text that must survive rebuild."
    assert metadata["text_reading"] == "Original text reading that must survive rebuild."
    assert context["legacy_context_note"] == "preserve context sentinel"
    assert context["rebuilt_from_existing"] is True
    assert rebuilt["metadata_tiers"]["tier1"]["legacy_tier_note"] == "preserve tier sentinel"
    assert rebuilt["metadata_tiers"]["custom_tier"]["legacy_field"] == "preserve custom tier"
    assert rebuilt["field_provenance"]["transcript"] == "Legacy transcript provenance"
    assert rebuilt["field_provenance"]["legacy_field"] == "preserve provenance sentinel"
    assert rebuilt["top_level_sentinel"] == {"legacy": True}
