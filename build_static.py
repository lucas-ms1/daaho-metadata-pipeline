#!/usr/bin/env python3
"""Retired static-viewer build entry point.

The former builder read the historical ``out/`` directory and regenerated
``public/data.json``. That behavior is intentionally disabled so deployments
serve only ``public/index.html``, the retirement notice. The stale data file is
retained as labeled historical evidence and is not rebuilt.
"""

from pathlib import Path


def main() -> int:
    notice = Path(__file__).resolve().parent / "public" / "index.html"
    if not notice.is_file():
        raise SystemExit(f"Retirement notice missing: {notice}")
    print("Viewer retired: serving the existing public/index.html notice; no data regenerated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
