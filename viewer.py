#!/usr/bin/env python3
"""Retired local viewer entry point.

This compatibility stub serves the same retirement notice as the static site.
It deliberately exposes no metadata or review API and never reads ``out/``.
"""

from pathlib import Path

from flask import Flask, send_from_directory


app = Flask(__name__)
PUBLIC_DIR = Path(__file__).resolve().parent / "public"


@app.get("/")
def retirement_notice():
    return send_from_directory(PUBLIC_DIR, "index.html")


if __name__ == "__main__":
    print("DAAHO viewer is retired; serving the retirement notice only.")
    app.run(host="127.0.0.1", port=5000, debug=False)
