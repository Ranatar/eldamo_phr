"""Build everything from source/eldamo-data-*.xml.xz and run the tests.

    python scripts/build.py                 # data, catalog, exports, atlas, report, all tests
    python scripts/build.py --no-browser    # skip the browser test (no Playwright needed)
    python scripts/build.py --no-tests      # build only
    python scripts/build.py --full          # recompute even what reports/inputs.json says is current

The data, catalogs and reports depend only on source/ and the Python code in shared/ (except
app.py and exports.py, which make the pages): reports/inputs.json keeps a fingerprint of those
files, and when it has not changed the build reads the committed data back instead of
recomputing them (seconds instead of minutes); the pages and exports are always rebuilt. The
tests rebuild the model from source on their own, so stale data would still fail them. The
reconstruction check runs in parallel processes (QUETTAMIN_JOBS, default: the CPUs), and the
browser tests run beside the others.

Only the Python standard library is required to build. Writes:
  branches/<branch>/data/*.json, branches/<branch>/catalog.md,
  exports/canonical.json, exports/atlas.graphml,
  app/index.html, app/corpus.html, app/graph.html, reports/audit.md, reports/audit.json,
  reports/sequencer.md, reports/sequencer.json, reports/reconstruction.md, reports/reconstruction.json
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.app import write_app  # noqa: E402
from shared.graph_page import write_graph  # noqa: E402
from shared.catalog import write_catalog  # noqa: E402
from shared.exports import write_exports  # noqa: E402
from shared.io import write_text  # noqa: E402
from shared.languages import BRANCHES  # noqa: E402
from shared.pipeline import DATA_FILES, build_all, load_all, write_branch  # noqa: E402
from shared.report import write_reconstruction_report, write_report, write_sequencer_report  # noqa: E402


def step(name, fn, *args):
    t = time.perf_counter()
    result = fn(*args)
    print(f'{name:<34} {time.perf_counter() - t:6.1f} s', flush=True)
    return result


INPUTS = ROOT / 'reports' / 'inputs.json'
# the pages and exports (always rebuilt) and the test vectors do not change the data or reports
PAGE_CODE = {'app.py', 'exports.py', 'parity.py', 'graph_page.py'}


def fingerprint() -> str:
    h = hashlib.sha256()
    files = sorted(p for p in (ROOT / 'shared').glob('*.py') if p.name not in PAGE_CODE)
    files += sorted((ROOT / 'source').glob('*'))
    for p in files:
        h.update(p.relative_to(ROOT).as_posix().encode() + b'\0')
        h.update(p.read_bytes().replace(b'\r\n', b'\n') + b'\0')
    return h.hexdigest()


def cached_outputs() -> list:
    out = [ROOT / 'reports' / f'{n}.{ext}' for n in ('audit', 'sequencer', 'reconstruction') for ext in ('md', 'json')]
    for b in BRANCHES:
        out += [ROOT / 'branches' / b / 'data' / f'{n}.json' for n in DATA_FILES]
        out.append(ROOT / 'branches' / b / 'catalog.md')
    return out


def is_current(fp: str) -> bool:
    try:
        recorded = json.loads(INPUTS.read_text(encoding='utf-8')).get('fingerprint')
    except (OSError, ValueError):
        return False
    return recorded == fp and all(p.exists() for p in cached_outputs())


def run_tests(no_browser: bool) -> int:
    """The browser tests in one process, the rest in another, side by side."""
    env = dict(os.environ, PYTHONUTF8='1')
    if no_browser:
        env['ELDAMO_SKIP_BROWSER'] = '1'
    modules = sorted(f'tests.{p.stem}' for p in (ROOT / 'tests').glob('test_*.py'))
    shards = [[m for m in modules if m != 'tests.test_browser']]
    if not no_browser and 'tests.test_browser' in modules:
        # the browser tests split over the remaining CPUs (each part starts its own Chromium)
        import unittest
        ids = []
        def walk(suite):
            for t in suite:
                if isinstance(t, unittest.TestSuite):
                    walk(t)
                else:
                    ids.append(t.id())
        walk(unittest.defaultTestLoader.loadTestsFromName('tests.test_browser'))
        parts = max(1, min(3, (os.cpu_count() or 1) - 1, len(ids)))
        shards += [ids[k::parts] for k in range(parts)]
    procs = []
    for k, shard in enumerate(shards):
        log = tempfile.TemporaryFile()
        cmd = [sys.executable, '-X', 'utf8', '-m', 'unittest', '-v', *shard]
        print('RUN', shard[0].split('.')[1] + (f' … ({len(shard)})' if len(shard) > 1 else ''), flush=True)
        # the browser tests read the committed data; the first part checks it against a fresh build
        shard_env = env if k == 0 else dict(env, QUETTAMIN_TEST_DATA='committed')
        procs.append((subprocess.Popen(cmd, cwd=ROOT, env=shard_env, stdout=log, stderr=subprocess.STDOUT), log))
    code = 0
    for proc, log in procs:
        code = proc.wait() or code
        log.seek(0)
        text = log.read().decode('utf-8', 'replace')
        sys.stdout.write(text)
        sys.stdout.flush()
        if os.environ.get('GITHUB_ACTIONS'):
            annotate(text)
    return code


def annotate(text: str) -> None:
    """On GitHub Actions: each failed test as an annotation (its name and the last line of its
    traceback), readable through the API where the full log is not."""
    for block in text.split('=' * 70)[1:]:
        lines = [l for l in block.strip().splitlines() if l.strip()]
        head = next((l for l in lines if l.startswith(('FAIL:', 'ERROR:'))), None)
        if head:
            tail = next((l for l in reversed(lines) if not l.startswith(('-' * 10, 'Ran ', 'FAILED', 'OK'))), '')
            print(f'::error::{head} -- {tail[:400]}', flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--no-tests', action='store_true', help='build without running tests')
    parser.add_argument('--no-browser', action='store_true', help='skip the Playwright browser test')
    parser.add_argument('--full', action='store_true', help='recompute the data and reports even if current')
    args = parser.parse_args(argv)

    fp = fingerprint()
    if not args.full and is_current(fp):
        print('data and reports are current (reports/inputs.json): read back, not recomputed', flush=True)
        branches = step('read branch data', load_all)
        step('exports and corpus browser', write_exports, branches)
        step('atlas app/index.html', write_app, branches)
        step('graph app/graph.html', write_graph, branches)
        return 0 if args.no_tests else run_tests(args.no_browser)

    branches = step('model, graph and chains', build_all)
    for name, data in branches.items():
        s = data['summary']
        print(f"  {name}: {s['rules']} rules, {s['pairs']} pairs, {s['derivations']} derivations, "
              f"{s['edges']} edges, {s['chains']['chains']} chains {s['chains']['grades']}, "
              f"reproduction {s['reproduction_rate'] * 100:.1f}%", flush=True)
        step(f'write {name} data and catalog', lambda n=name, d=data: (write_branch(n, d), write_catalog(n, d)))
    step('exports and corpus browser', write_exports, branches)
    step('atlas app/index.html', write_app, branches)
    step('graph app/graph.html', write_graph, branches)
    step('report', write_report, branches)
    step('sequencer backtest', write_sequencer_report, branches)
    step('reconstruction check', write_reconstruction_report, branches)
    write_text(INPUTS, json.dumps({'fingerprint': fp}, indent=1) + '\n')

    return 0 if args.no_tests else run_tests(args.no_browser)


if __name__ == '__main__':
    sys.exit(main())
