# Eldamo research package — readable edition

## Open
- `app/built.html` — current one-file offline HTML app (with the assessed 38 additional chains).
- `app/index.html` — readable, multi-file offline app. Keep `styles.css`, `data.js`, and `app.js` in the same directory.

## Modify and rebuild
- Edit `app/styles.css` and `app/app.js`.
- Data is available in `app/edges.json`, `app/rules.json`; `app/data.js` is their prebuilt browser representation.
- `python development/build_standalone.py` creates `app/built.html` from the readable source.
- `python development/test_parity.py` checks browser behavior and reports differences versus `app/standalone.html` reference.
- The identical original reference HTML can be found as `legacy/eldamo_sound_path_explorer_complete_original.html`.

The browser tests were successfully run in Chromium using Playwright's `page.set_content()` because file URL navigation is blocked in the test environment. Initial 1280 px screenshots were identical pixel-for-pixel.

The corpus of Eldamo 0.8.13 is research data; graph paths remain structural candidates, not historical proof.

## Chain assessments
- `reports/eldamo_38_chain_assessment.md`: individual assessments for all 38 additional chains.
- `data/eldamo_38_chain_assessment.csv`: machine-readable assessments.
- `development/assess_38.py`: reproducible process, requires `eldamo_extended_rule_inventory.csv` alongside the project as a research input (included under data).
