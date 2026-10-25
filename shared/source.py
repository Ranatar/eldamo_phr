"""Access to the bundled Eldamo data model (source/eldamo-data-*.xml.xz)."""
from __future__ import annotations

import hashlib
import json
import lzma
import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / 'source'
SITE = 'https://eldamo.org/content/'


def meta() -> dict:
    return json.loads((SOURCE_DIR / 'SOURCE.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def xml_bytes() -> bytes:
    m = meta()
    packed = (SOURCE_DIR / m['file']).read_bytes()
    if hashlib.sha256(packed).hexdigest() != m['xz_sha256']:
        raise SystemExit(f"checksum mismatch for source/{m['file']}")
    data = lzma.decompress(packed)
    if hashlib.sha256(data).hexdigest() != m['xml_sha256'] or len(data) != m['xml_bytes']:
        raise SystemExit('decompressed eldamo-data.xml does not match SOURCE.json')
    data.decode('utf-8')  # strict UTF-8
    return data


@lru_cache(maxsize=1)
def root() -> ET.Element:
    return ET.fromstring(xml_bytes())


def word_url(page_id: str | None) -> str:
    return f'{SITE}words/word-{page_id}.html' if page_id else ''


def source_url(source: str | None) -> str:
    """Eldamo reference link with the anchor of the exact passage, e.g. PE17/113.1501."""
    if not source:
        return ''
    book = source.split('/', 1)[0]
    return f'{SITE}references/ref-{book}.html#{source}'


def source_label(source: str | None) -> str:
    """Short citation without Eldamo's internal line number: PE17/113.1501 -> PE17/113."""
    if not source:
        return ''
    head, _, _ = source.partition('.')
    return head
