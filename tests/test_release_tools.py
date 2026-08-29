import csv
import hashlib
import json
from pathlib import Path

from scripts.report_tier_differences import collect_differences
from scripts.verify_release_manifest import verify_manifest


def _manifest_row(relative: str, payload: bytes) -> dict[str, str]:
    return {
        "RelativePath": relative,
        "SHA256": hashlib.sha256(payload).hexdigest().upper(),
        "Bytes": str(len(payload)),
        "LastWriteTimeUTC": "2026-08-24T00:00:00Z",
    }


def test_manifest_verifier_accepts_windows_separators_and_checks_content(tmp_path):
    data_dir = tmp_path / "out_manual_corrections_2026-08-24"
    support_dir = tmp_path / "handoff" / "release_2026-08-24_manual_corrections"
    data_dir.mkdir()
    support_dir.mkdir(parents=True)
    payload = b"release payload"
    target = data_dir / "item.json"
    target.write_bytes(payload)
    manifest = support_dir / "sha256_manual_corrections_2026-08-24.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["RelativePath", "SHA256", "Bytes", "LastWriteTimeUTC"]
        )
        writer.writeheader()
        writer.writerow(_manifest_row("out_manual_corrections_2026-08-24\\item.json", payload))

    relative_manifest = manifest.relative_to(tmp_path)
    assert verify_manifest(tmp_path, relative_manifest) == []

    target.write_bytes(b"changed and longer payload")
    errors = verify_manifest(tmp_path, relative_manifest)
    assert any("size mismatch" in error for error in errors)
    assert any("hash mismatch" in error for error in errors)


def test_manifest_verifier_rejects_unlisted_extra_file(tmp_path):
    data_dir = tmp_path / "out_manual_corrections_2026-08-24"
    support_dir = tmp_path / "handoff" / "release_2026-08-24_manual_corrections"
    data_dir.mkdir()
    support_dir.mkdir(parents=True)
    payload = b"release payload"
    (data_dir / "item.json").write_bytes(payload)
    (data_dir / "extra.json").write_bytes(b"extra")
    manifest = support_dir / "sha256_manual_corrections_2026-08-24.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["RelativePath", "SHA256", "Bytes", "LastWriteTimeUTC"]
        )
        writer.writeheader()
        writer.writerow(_manifest_row("out_manual_corrections_2026-08-24/item.json", payload))

    errors = verify_manifest(tmp_path, manifest.relative_to(tmp_path))
    assert "unlisted extra file: out_manual_corrections_2026-08-24/extra.json" in errors


def test_tier_difference_report_compares_corresponding_fields(tmp_path):
    payload = {
        "metadata": {"title": "Authoritative", "creator": None},
        "metadata_tiers": {
            "tier1": {"title": "Historical proposal"},
            "tier2": {"creator": None},
        },
    }
    (tmp_path / "BC-TEST_Recto.loc15.json").write_text(json.dumps(payload), encoding="utf-8")

    rows = collect_differences(tmp_path)

    assert rows == [
        {
            "record": "BC-TEST",
            "tier": "tier1",
            "field": "title",
            "top_level_value": '"Authoritative"',
            "tier_value": '"Historical proposal"',
        }
    ]
