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


class InterfaceCatalog(unittest.TestCase):
    """app/messages.json: every key the interface uses exists, in both languages, with the same placeholders."""
    DYNAMIC = {'tag.': ['suffix', 'prefix'], 'problem.': ['initial', 'cluster', 'final'], 'branch.': ['quenya', 'sindarin'],
               'route.': ['attested', 'same', 'forward', 'backDirect', 'backPrimitive', 'backRoot', 'cognateLink', 'viaPrimitive',
                          'nearSame', 'nearClose', 'link', 'unchanged', 'reetymology', 'then', 'byElements', 'partialLink', 'irregularLaw', 'composed', 'composedUnconfirmed'],
               'card.root.': ['element', 'cognate', 'source', 'combine', 'see', 'deprecated'],
               'root.via.': ['element', 'cognate', 'source', 'combine', 'see', 'deprecated'],
               'ipa.': ['labial', 'dental', 'palatal', 'velar', 'labiovelar', 'glottal', 'stop', 'fricative', 'nasal',
                        'lateral', 'trill', 'approximant', 'high', 'mid', 'low', 'front', 'central', 'back']}
    FILES = ('runtime.js', 'word_ui.js', 'wordform_ui.js', 'reconstruct_ui.js', 'corpus_template.html')

    @classmethod
    def setUpClass(cls):
        cls.messages = json.loads((ROOT / 'app' / 'messages.json').read_text(encoding='utf-8'))

    def used(self):
        keys = {p + k for p, ks in self.DYNAMIC.items() for k in ks}
        call = re.compile(r"\b(?:T|TN|I18N\.tn?)\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
        for name in self.FILES:
            text = (ROOT / 'app' / name).read_text(encoding='utf-8')
            for args in call.findall(text):
                keys.update(k for k in re.findall(r"'([a-zA-Z]+\.[A-Za-z_.-]*)'", args) if not k.endswith('.'))
        for name in ('template.html', 'corpus_template.html'):
            text = (ROOT / 'app' / name).read_text(encoding='utf-8')
            keys.update(re.findall(r'data-i18n(?:-html)?="([^"]+)"', text))
            for attrs in re.findall(r'data-i18n-attr="([^"]+)"', text):
                keys.update(pair.split(':')[1].strip() for pair in attrs.split(';'))
        return keys

    def test_no_untranslated_text_in_sources(self):
        """Russian interface text lives only in the catalog: none in the code outside comments,
        and in the templates only as the default text of an element marked for translation."""
        from html.parser import HTMLParser
        cyr = re.compile('[А-Яа-яЁё]')
        for name in ('router.js', 'wordform.js', 'word_ui.js', 'wordform_ui.js', 'reconstruct_ui.js',
                     'runtime.js', 'i18n.js'):
            text = (ROOT / 'app' / name).read_text(encoding='utf-8')
            code = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
            for k, line in enumerate(code.split('\n'), 1):
                line = re.sub(r'(^|\s)//.*$', '', line)
                self.assertNotRegex(line, cyr, f'{name}: {line.strip()[:80]}')

        class Check(HTMLParser):
            VOID = {'meta', 'link', 'input', 'br', 'img', 'hr', 'source', 'col', 'wbr'}

            def __init__(self):
                super().__init__()
                self.stack, self.bad, self.script = [], [], False

            def handle_starttag(self, tag, attrs):
                a = dict(attrs)
                covered = {pair.split(':')[0].strip() for pair in (a.get('data-i18n-attr') or '').split(';') if pair}
                for k, v in attrs:
                    if v and cyr.search(v) and k not in covered and not k.startswith('data-'):
                        self.bad.append(f'<{tag} {k}="{v[:40]}">')
                self.script = tag in ('script', 'style')
                if tag not in self.VOID:
                    self.stack.append('data-i18n' in a or 'data-i18n-html' in a)

            def handle_endtag(self, tag):
                self.script = False
                if tag not in self.VOID and self.stack:
                    self.stack.pop()

            def handle_data(self, data):
                if not self.script and cyr.search(data) and not any(self.stack):
                    self.bad.append(data.strip()[:60])

        for name in ('template.html', 'corpus_template.html'):
            html = (ROOT / 'app' / name).read_text(encoding='utf-8')
            html = re.sub(r'<script\b[^>]*>.*?</script>', '', html, flags=re.S)   # the code is checked above
            c = Check()
            c.feed(html)
            self.assertEqual(c.bad, [], name)

    def test_keys(self):
        used = self.used()
        self.assertEqual(sorted(used - set(self.messages)), [], 'keys missing from app/messages.json')
        self.assertEqual(sorted(set(self.messages) - used), [], 'unused keys in app/messages.json')

    def test_languages_and_placeholders(self):
        def texts(v):
            return list(v.values()) if isinstance(v, dict) else [v]
        for key, entry in self.messages.items():
            self.assertEqual(set(entry), {'ru', 'en'}, key)
            ru, en = entry['ru'], entry['en']
            if isinstance(ru, dict):
                self.assertEqual(set(ru), {'one', 'few', 'many'}, key)
                self.assertEqual(set(en), {'one', 'other'}, key)
            self.assertFalse(any(re.search('[А-Яа-яЁё]', t) for t in texts(en)) and key not in ('lang.switch', 'lang.title'), key)
            names = {frozenset(re.findall(r'\{(\w+)\}', t)) for t in texts(ru) + texts(en)}
            self.assertEqual(len(names), 1, key)


if __name__ == '__main__':
    unittest.main()
