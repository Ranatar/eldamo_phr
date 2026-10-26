"""Files on disk are the current build of the bundled source and read back intact."""
import json
import re
import unittest
import xml.etree.ElementTree as ET

from tests.support import ROOT, branches
from shared.app import payload
from shared.exports import canonical
from shared.io import dumps
from shared.pipeline import DATA_FILES


class Outputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()

    def test_branch_files_are_current(self):
        for b, d in self.data.items():
            for name in DATA_FILES:
                path = ROOT / 'branches' / b / 'data' / f'{name}.json'
                with self.subTest(file=str(path.relative_to(ROOT))):
                    self.assertEqual(path.read_text(encoding='utf-8'), dumps(d[name]),
                                     'stale: run python scripts/build.py')

    def test_canonical_export(self):
        path = ROOT / 'exports' / 'canonical.json'
        self.assertEqual(json.loads(path.read_text(encoding='utf-8')), json.loads(dumps(canonical(self.data))))

    def test_graphml(self):
        tree = ET.parse(ROOT / 'exports' / 'atlas.graphml')
        ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}
        edges = tree.getroot().findall('.//g:edge', ns)
        self.assertEqual(len(edges), sum(len(d['edges']) for d in self.data.values()))

    def _embedded(self, path, element_id):
        html = path.read_text(encoding='utf-8')
        m = re.search(r'<script type="application/json" id="%s">(.*?)</script>' % element_id, html, re.S)
        self.assertIsNotNone(m)
        self.assertNotRegex(html, r'@@[A-Z_]+@@')        # every template marker is filled
        return json.loads(m.group(1))

    def test_atlas_embeds_current_payload(self):
        got = self._embedded(ROOT / 'app' / 'index.html', 'atlas-data')
        self.assertEqual(got, json.loads(dumps(payload(self.data))))

    def test_corpus_browser(self):
        got = self._embedded(ROOT / 'app' / 'corpus.html', 'corpus-data')
        for b, d in self.data.items():
            self.assertEqual(len(got['branches'][b]['derivations']), len(d['derivations']))

    def test_text_outputs_are_utf8_lf(self):
        for path in [*ROOT.glob('branches/*/data/*.json'), *ROOT.glob('branches/*/catalog.md'),
                     ROOT / 'reports' / 'audit.md', ROOT / 'reports' / 'audit.json', ROOT / 'app' / 'index.html',
                     ROOT / 'app' / 'corpus.html', ROOT / 'exports' / 'canonical.json', ROOT / 'exports' / 'atlas.graphml']:
            raw = path.read_bytes()
            raw.decode('utf-8')
            self.assertNotIn(b'\r\n', raw, path)


if __name__ == '__main__':
    unittest.main()
