"""Shared fixtures: one fresh build per test process."""
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.pipeline import build_all  # noqa: E402


@lru_cache(maxsize=1)
def branches():
    return build_all()
