"""Build everything from source/eldamo-data-*.xml.xz and run the tests.

    python scripts/build.py                 # data, catalog, exports, atlas, report, all tests
    python scripts/build.py --no-browser    # skip the browser test (no Playwright needed)
    python scripts/build.py --no-tests      # build only

Only the Python standard library is required to build. Writes:
  branches/<branch>/data/*.json, branches/<branch>/catalog.md,
  exports/canonical.json, exports/atlas.graphml,
  app/index.html, app/corpus.html, reports/audit.md, reports/audit.json,
  reports/sequencer.md, reports/sequencer.json
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.app import write_app  # noqa: E402
from shared.catalog import write_catalog  # noqa: E402
from shared.exports import write_exports  # noqa: E402
from shared.pipeline import build_all, write_branch  # noqa: E402
from shared.report import write_report, write_sequencer_report  # noqa: E402


def step(name, fn, *args):
    t = time.perf_counter()
    result = fn(*args)
    print(f'{name:<34} {time.perf_counter() - t:6.1f} s', flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--no-tests', action='store_true', help='build without running tests')
    parser.add_argument('--no-browser', action='store_true', help='skip the Playwright browser test')
    args = parser.parse_args(argv)

    branches = step('model, graph and chains', build_all)
    for name, data in branches.items():
        s = data['summary']
        print(f"  {name}: {s['rules']} rules, {s['pairs']} pairs, {s['derivations']} derivations, "
              f"{s['edges']} edges, {s['chains']['chains']} chains {s['chains']['grades']}, "
              f"reproduction {s['reproduction_rate'] * 100:.1f}%", flush=True)
        step(f'write {name} data and catalog', lambda n=name, d=data: (write_branch(n, d), write_catalog(n, d)))
    step('exports and corpus browser', write_exports, branches)
    step('atlas app/index.html', write_app, branches)
    step('report', write_report, branches)
    step('sequencer backtest', write_sequencer_report, branches)

    if args.no_tests:
        return 0
    env = dict(os.environ, PYTHONUTF8='1')
    if args.no_browser:
        env['ELDAMO_SKIP_BROWSER'] = '1'
    cmd = [sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.', '-v']
    print('RUN', ' '.join(cmd[1:]), flush=True)
    return subprocess.run(cmd, cwd=ROOT, env=env).returncode


if __name__ == '__main__':
    sys.exit(main())
