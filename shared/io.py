"""File output: always UTF-8 with '\\n' line endings, written atomically."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name + '.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def dumps(obj, compact: bool = False) -> str:
    if compact:
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'), sort_keys=False)
    return json.dumps(obj, ensure_ascii=False, indent=1) + '\n'


def write_json(path: Path, obj, compact: bool = False) -> None:
    write_text(path, dumps(obj, compact))


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def embed_json(obj) -> str:
    """JSON safe to place inside <script type="application/json">."""
    return dumps(obj, compact=True).replace('</', '<\\/').replace('<!--', '<\\!--')
