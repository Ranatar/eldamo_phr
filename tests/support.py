"""Shared fixtures: one fresh build per test process.

QUETTAMIN_TEST_DATA=committed reads the committed branch data instead (scripts/build.py sets
it for the browser tests, which run beside the others; those check the data against a fresh
build).
"""
import os
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.pipeline import build_all, load_all  # noqa: E402


@lru_cache(maxsize=1)
def branches():
    return load_all() if os.environ.get('QUETTAMIN_TEST_DATA') == 'committed' else build_all()
