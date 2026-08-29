#!/usr/bin/env python3
"""Verify the immutable August 24 release manifest without rewriting it."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path, PurePosixPath
import sys


DEFAULT_MANIFEST = Path(
    "handoff/release_2026-08-24_manual_corrections/sha256_manual_corrections_2026-08-24.csv"
)
MANIFEST_COLUMNS = ["RelativePath", "SHA256", "Bytes", "LastWriteTimeUTC"]
STRICT_DIRECTORIES = (
    Path("out_manual_corrections_2026-08-24"),
    Path("handoff/release_2026-08-24_manual_corrections"),
)


def normalize_relative_path(value: str) -> Path:
    """Convert either manifest separator style to a safe repository-relative path."""
    normalized = value.strip().replace("\\", "/")
    pure = PurePosixPath(normalized)
    if not normalized or pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe manifest path: {value!r}")
    return Path(*pure.parts)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def verify_manifest(root: Path, manifest_relative: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / manifest_relative
    if not manifest_path.is_file():
        return [f"manifest missing: {manifest_relative.as_posix()}"]

    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != MANIFEST_COLUMNS:
            errors.append(f"unexpected manifest columns: {reader.fieldnames!r}")
        rows = list(reader)

    listed: set[Path] = set()
    for row_number, row in enumerate(rows, start=2):
        try:
            relative = normalize_relative_path(row.get("RelativePath", ""))
        except ValueError as exc:
            errors.append(f"row {row_number}: {exc}")
            continue
        if relative in listed:
            errors.append(f"row {row_number}: duplicate path: {relative.as_posix()}")
            continue
        listed.add(relative)
        target = root / relative
        if not target.is_file():
            errors.append(f"missing: {relative.as_posix()}")
            continue
        try:
            expected_bytes = int(row.get("Bytes", ""))
        except ValueError:
            errors.append(f"row {row_number}: invalid byte count for {relative.as_posix()}")
            continue
        actual_bytes = target.stat().st_size
        if actual_bytes != expected_bytes:
            errors.append(
                f"size mismatch: {relative.as_posix()} expected {expected_bytes}, got {actual_bytes}"
            )
        expected_hash = (row.get("SHA256") or "").strip().upper()
        actual_hash = sha256_file(target)
        if actual_hash != expected_hash:
            errors.append(
                f"hash mismatch: {relative.as_posix()} expected {expected_hash}, got {actual_hash}"
            )

    allowed_unlisted = {manifest_relative}
    for directory in STRICT_DIRECTORIES:
        absolute_directory = root / directory
        if not absolute_directory.is_dir():
            errors.append(f"required directory missing: {directory.as_posix()}")
            continue
        for target in sorted(path for path in absolute_directory.iterdir() if path.is_file()):
            relative = target.relative_to(root)
            if relative not in listed and relative not in allowed_unlisted:
                errors.append(f"unlisted extra file: {relative.as_posix()}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = normalize_relative_path(str(args.manifest))
    errors = verify_manifest(root, manifest)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Manifest verification failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    with (root / manifest).open("r", encoding="utf-8-sig", newline="") as handle:
        count = sum(1 for _ in csv.DictReader(handle))
    print(f"PASS: verified {count} manifest entries; sizes and SHA-256 hashes match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
