# Legacy viewer notice

The DAAHO web viewer is retired as of August 28, 2026. Repository history and
the retained `templates/viewer.html`, `public/data.json`, and `public/images/`
preserve evidence of the former implementation. They are noncanonical and are
not a maintained website or release surface.

- `public/index.html` is now a retirement notice.
- `build_static.py` is a no-op verifier that cannot rebuild stale data from `out/`.
- `viewer.py` serves only the retirement notice and exposes no review or data API.
- `vercel.json` may deploy the notice, but local configuration does not prove an
  external deployment exists.

The authoritative corrected JSON is in
`out_manual_corrections_2026-08-24/`; use the successor guide for the complete
release map.
