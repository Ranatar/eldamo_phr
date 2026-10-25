"""Import the Eldamo data model from an official release into source/.

Usage:
    python scripts/import_eldamo_release.py <eldamo-X.Y.Z.zip | eldamo-data.xml> [--version X.Y.Z]

The project needs only content/data-model/eldamo-data.xml. This script copies
that one file out of a release archive (or takes a bare XML file), compresses
it with xz and records checksums in source/SOURCE.json. Nothing else from the
Eldamo site is redistributed.
"""
import argparse
import hashlib
import json
import lzma
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / 'source'
XML_MEMBER = re.compile(r'^(?:[^/]+/)?content/data-model/eldamo-data\.xml$')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_xml(path: Path):
    archive_info = None
    if zipfile.is_zipfile(path):
        raw = path.read_bytes()
        archive_info = {'file': path.name, 'bytes': len(raw), 'sha256': sha256(raw)}
        with zipfile.ZipFile(path) as z:
            members = [n for n in z.namelist() if XML_MEMBER.match(n)]
            if len(members) != 1:
                raise SystemExit(f'expected exactly one eldamo-data.xml in {path}, found {members}')
            archive_info['member'] = members[0]
            xml = z.read(members[0])
    else:
        xml = path.read_bytes()
    return xml, archive_info


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', type=Path)
    parser.add_argument('--version', help='Eldamo version; read from <word-data version=...> when omitted')
    args = parser.parse_args(argv)

    xml, archive_info = read_xml(args.input)
    xml.decode('utf-8')  # strict: refuse non-UTF-8 input
    head = xml[:4096].decode('utf-8', errors='replace')
    found = re.search(r'<word-data[^>]*\bversion="([^"]+)"', head)
    version = args.version or (found.group(1) if found else None)
    if not version:
        raise SystemExit('cannot determine Eldamo version; pass --version')
    if found and args.version and found.group(1) != args.version:
        raise SystemExit(f'--version {args.version} differs from XML version {found.group(1)}')

    packed = lzma.compress(xml, format=lzma.FORMAT_XZ, preset=9 | lzma.PRESET_EXTREME)
    SOURCE_DIR.mkdir(exist_ok=True)
    name = f'eldamo-data-{version}.xml.xz'
    (SOURCE_DIR / name).write_bytes(packed)
    meta = {
        'eldamo_version': version,
        'file': name,
        'xz_sha256': sha256(packed),
        'xml_bytes': len(xml),
        'xml_sha256': sha256(xml),
        'release_archive': archive_info,
        'upstream': {
            'site': 'https://eldamo.org',
            'repository': 'https://github.com/pfstrack/eldamo',
            'author': 'Paul Strack',
            'license': 'CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)',
        },
    }
    with open(SOURCE_DIR / 'SOURCE.json', 'w', encoding='utf-8', newline='\n') as f:  # Path.write_text(newline=) needs 3.10
        f.write(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    sys.exit(main())
