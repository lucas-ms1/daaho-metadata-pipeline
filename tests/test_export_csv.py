import csv
import json
import sys

import pytest

import export_csv


def _write_minimal_output(out_dir):
    out_dir.mkdir()
    payload = {
        "metadata": {
            "identifier": "BC-TEST",
            "title": "Test title",
            "description": "Test summary",
            "subjects": ["Test subject"],
            "transcript": "Test transcript",
        },
        "context": {},
    }
    (out_dir / "BC-TEST.loc15.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def _run_export(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["export_csv.py", *map(str, args)])
    export_csv.main()


def test_normalize_headers_deduplicates_in_original_order():
    headers = ["Identifier", "Title", "Summary", "Summary", "Identifier", "Transcript"]

    assert export_csv.normalize_headers(headers) == [
        "Identifier",
        "Title",
        "Summary",
        "Transcript",
    ]


def test_template_free_export_uses_unique_standard_headers(tmp_path, monkeypatch):
    out_dir = tmp_path / "out"
    output = tmp_path / "metadata.csv"
    _write_minimal_output(out_dir)

    _run_export(monkeypatch, "--out-dir", out_dir, "--output", output)

    with output.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert len(reader.fieldnames) == 31
    assert len(reader.fieldnames) == len(set(reader.fieldnames))
    assert rows == [
        {
            **{header: "" for header in reader.fieldnames},
            "Identifier": "BC-TEST",
            "Title": "Test title",
            "Summary": "Test summary",
            "Subject (FAST)": "Test subject",
            "Transcript": "Test transcript",
            "Preservation Filename": "BC-TEST",
        }
    ]


def test_custom_template_deduplicates_all_headers(tmp_path, monkeypatch):
    out_dir = tmp_path / "out"
    output = tmp_path / "metadata.csv"
    template = tmp_path / "template.csv"
    _write_minimal_output(out_dir)
    template.write_text(
        "Identifier,Title,Summary,Summary,Identifier,Transcript\n",
        encoding="utf-8",
    )

    _run_export(
        monkeypatch,
        "--out-dir",
        out_dir,
        "--template",
        template,
        "--output",
        output,
    )

    with output.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    assert rows[0] == ["Identifier", "Title", "Summary", "Transcript"]
    assert rows[1] == ["BC-TEST", "Test title", "Test summary", "Test transcript"]


def test_explicit_missing_template_fails(tmp_path, monkeypatch, capsys):
    out_dir = tmp_path / "out"
    output = tmp_path / "metadata.csv"
    missing_template = tmp_path / "missing.csv"
    _write_minimal_output(out_dir)

    with pytest.raises(SystemExit) as exc_info:
        _run_export(
            monkeypatch,
            "--out-dir",
            out_dir,
            "--template",
            missing_template,
            "--output",
            output,
        )

    assert exc_info.value.code == 2
    assert f"CSV template not found: {missing_template}" in capsys.readouterr().err
    assert not output.exists()
