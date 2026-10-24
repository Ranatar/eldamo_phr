# Eldamo — readable source edition

`app/index.html` — human-readable HTML with separate `styles.css`, `app.js`, `data.js` (offline under `file://`), plus `edges.json`, `rules.json`.

`app/standalone.html` — unchanged autonomous original reference, generated from the same embedded corpus.

The JSON datasets are split from the original and `data.js` embeds those exact values.
`build_standalone.py` reconstructs a standalone HTML from the readable source without network calls.
`test_parity.py` compares reference and source build in Chromium (screenshots, actions and data).
Run `python test_parity.py` and `python build_standalone.py`.

The two versions should produce the same rendered interface. Failure is an error, not a known limitation.
