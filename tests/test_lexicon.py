"""Lexicon, spelling conversion and compounds."""
import unittest

from tests.support import branches
from shared import compound
from shared.interpreter import comparable
from shared.orthography import to_phonetic
from shared.sequencer import Sequencer


class Orthography(unittest.TestCase):
    def test_examples(self):
        for form, family, expected in [
                ('Quendi', 'quenya', 'kwendi'), ('nehta-', 'quenya', 'nexta-'), ('hyanda', 'quenya', 'j̊anda'),
                ('lómë', 'quenya', 'lōme'), ('naxa', 'quenya', 'naksa'), ('yunque', 'quenya', 'juŋkwe'),
                ('Ñoldor', 'quenya', 'noldor'), ('riel(lë)', 'quenya', 'riel'),
                ('Thû', 'sindarin', 'θū'), ('rhaed', 'sindarin', 'r̥aed'), ('ylf', 'sindarin', 'ylv'),
                ('delw', 'sindarin', 'delu'), ('maw', 'sindarin', 'mau'), ('tîw', 'sindarin', 'tīw'),
                ('iolf', 'sindarin', 'jolv'), ('aphad-', 'sindarin', 'affad-'), ('Gwath', 'sindarin', 'gwaθ')]:
            self.assertEqual(to_phonetic(form, family), expected, form)

    def test_agrees_with_attested_final_forms(self):
        # dictionary forms vs the last form of their derivations; the rest are
        # mostly Eldamo variants (other inflected form, verb stem, plural)
        for b, code in (('quenya', 'q'), ('sindarin', 's')):
            data = branches()[b]
            pairs = {(d['form'] or d['word_form'], d['steps'][-1]['after']) for d in data['derivations']
                     if d['steps'] and d['steps'][-1]['lang'] == code and d['word_lang'] == code and not d['deleted']}
            ok = sum(comparable(to_phonetic(a, b)) == comparable(t) for a, t in pairs)
            self.assertGreater(ok / len(pairs), 0.8, b)


class Lexicon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lex = {b: d['lexicon'] for b, d in branches().items()}

    def find(self, b, lang, form):
        return [e for e in self.lex[b] if e['lang'] == lang and e['form'] == form]

    def test_homonyms_are_separate_pages(self):
        world, = self.find('quenya', 'q', 'Ambar')
        fate, = self.find('quenya', 'q', 'ambar')
        self.assertNotEqual(world['id'], fate['id'])
        self.assertEqual(fate['stems'], ['ambart-'])
        self.assertIn('MBAR', [r['form'] for r in world['roots']])

    def test_stems_and_roots(self):
        linde, = self.find('quenya', 'q', 'lindë')
        self.assertIn('lindi-', linde['stems'])
        self.assertIn('LIN²', [r['form'] for r in linde['roots']])

    def test_elements_resolved(self):
        casallie, = self.find('quenya', 'q', 'Casallië')
        first, second = casallie['elements']
        self.assertEqual((first['form'], first.get('tag')), ('Casar', 'assimilated'))
        self.assertIn('id', first)
        self.assertIn('id', second)

    def test_stage_forms_from_derivations(self):
        alt, = self.find('quenya', 'q', 'Altáriel')
        self.assertIn('altarielle', alt['stages']['q'])

    def test_no_deleted_words(self):
        for entries in self.lex.values():
            self.assertFalse([e for e in entries if e['mark'].startswith('-')])


class Compounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.seq = {b: Sequencer(d) for b, d in cls.data.items()}

    def test_primitive_compound(self):
        # kiryahto: kirjā + aktō formed in Primitive Elvish -> kirjaxto
        b = 'quenya'
        lex = {e['id']: e for e in self.data[b]['lexicon']}
        word = next(e for e in lex.values() if e['form'] == 'kiryahto')
        ids = [x['id'] for x in word['elements']]
        forms = [comparable(v['form']) for v in compound.predict(lex, self.seq[b], ids, 'late', 0)]
        self.assertIn('kirjaxto', forms)

    def test_latest_stage_uses_stem_of_first_element(self):
        b = 'quenya'
        lex = {e['id']: e for e in self.data[b]['lexicon']}
        fate = next(e for e in lex.values() if e['form'] == 'ambar' and e['lang'] == 'q')
        lie = next(e for e in lex.values() if e['form'] == 'lië' and e['lang'] == 'q')
        vs = compound.predict(lex, self.seq[b], [fate['id'], lie['id']], 'late', 2)
        self.assertEqual(vs[0]['joined'], 'ambart+lie')

    def test_benchmark_floor(self):
        for b, data in self.data.items():
            r = compound.backtest(data, data['lexicon'], self.seq[b])
            self.assertGreater(r['cases'], 40, b)
            self.assertGreaterEqual(r['any'] / r['cases'], 0.25, b)


if __name__ == '__main__':
    unittest.main()
