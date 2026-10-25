"""Word formation at the latest stage: course §6.1, junction table, mutation."""
import unittest

from tests.support import branches
from shared import affixes, backform, compound, junctions, morphophonology as M
from shared.interpreter import comparable, join, phonemes as P
from shared.sequencer import Sequencer


def j(x):
    return join(x) if x is not None else None


class Course(unittest.TestCase):
    """Examples of Strack's Quenya course, chapter 6.1."""

    def test_prosodic_lengthening(self):
        cases = [('kuluma', 'va', 'kulumāva'), ('atanatar', 'i', 'atanatāri'), ('telume', 'va', 'telumēva'),
                 ('falasse', 'va', None), ('falasse', 'lion', 'falassēlion'), ('telume', 'lion', 'telumēlion'),
                 ('morikwend', 'ion', None), ('lūme', 'nna', None)]
        for base, suffix, expected in cases:
            self.assertEqual(j(M.prosodic_lengthening(P(base), P(suffix))), expected, base + '+' + suffix)
        self.assertIsNone(M.prosodic_lengthening(P('telume'), P('i'), e_noun=True))

    def test_compound_reduction(self):
        for word, form, stem in [('valinōre', 'valinor', 'valinōr'), ('morikwende', 'morikwen', 'morikwend'),
                                 ('kaimasambe', 'kaimasan', 'kaimasamb')]:
            red = M.reduce_compound(P(word))
            self.assertEqual((j(red[0]), j(red[1])), (form, stem), word)
        self.assertEqual(j(M.shorten_final_long(P('eldamār'), 4)), 'eldamar')

    def test_directional_shortening(self):
        self.assertEqual(j(M.directional_shortening(P('endōre'), P('nna'))), 'endorenna')
        self.assertIsNone(M.directional_shortening(P('lūme'), P('nna')))

    def test_cuivienen(self):
        forms = [j(w) for w, _, _ in M.compound_variants(P('kuivie'), P('nēn'))]
        self.assertIn('kuiviēnen', forms)

    def test_soft_mutation(self):
        for word, expected in [('tir', 'dir'), ('gwen', 'wen'), ('galad', 'alad'), ('mīr', 'vīr'), ('haered', 'xaered')]:
            self.assertEqual(j(M.lenite(P(word))), expected)
        for word in ('r̥ūn', 'l̥eweg', 'nīn', 'θīr', 'faroθ'):
            self.assertIsNone(M.lenite(P(word)), word)       # lh, rh, n, th, f do not mutate
        # ancient nasalized stops: ✶mbar > bâr, mutated *mâr
        self.assertEqual(j(M.lenite(P('bār'), 'mbar')), 'mār')
        self.assertEqual(j(M.lenite(P('dōr'), 'ndorē')), 'nōr')

    def test_no_epenthesis_inside_geminate(self):
        # Q. "nasals and liquids often became syllabic after a consonant" (ClV₁ > CV₁lV₁) does not split ll
        from shared.interpreter import apply
        rule = ('ClV₁|ml|Cr|{ptk}{nm}', 'CV₁lV₁|mul|Car|{ptk}{an|um}')
        self.assertEqual(apply(*rule, 'amballinde')['ordered'], [])
        self.assertEqual(apply(*rule, 'aklinde')['ordered'], ['akilinde'])


class Junctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.seq = {b: Sequencer(d) for b, d in cls.data.items()}

    def lexicon(self, b):
        return {e['id']: e for e in self.data[b]['lexicon']}

    def test_casallie_assimilation_is_attested(self):
        rows = self.data['quenya']['junctions']['cases']
        row = next(r for r in rows if r['form'] == 'Casallië')
        self.assertEqual(list(row['junction']), [1, 0, 'l'])

    def test_ambar_linde(self):
        # the example of the plan: Ambar "world" + lindë -> amballindë
        lex = self.lexicon('quenya')
        ambar = next(e for e in lex.values() if e['form'] == 'Ambar' and e['lang'] == 'q')
        linde = next(e for e in lex.values() if e['form'] == 'lindë' and e['lang'] == 'q')
        table = junctions.learn(junctions.cases('quenya', self.data['quenya']['lexicon']))
        vs = compound.predict(lex, self.seq['quenya'], [ambar['id'], linde['id']], 'late', 2, table=table)
        self.assertEqual(vs[0]['form'], 'amballinde')
        self.assertIn('ambarlinde', [v['form'] for v in vs])

    def test_leave_one_out_floor(self):
        floors = {'quenya': (0.37, 0.60), 'sindarin': (0.32, 0.55)}
        for b, (main, anyv) in floors.items():
            r = compound.latest_backtest(self.data[b], self.data[b]['lexicon'], self.seq[b])
            self.assertGreaterEqual(r['main'] / r['cases'], main, b)
            self.assertGreaterEqual(r['any'] / r['cases'], anyv, b)


class Affixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.seq = {b: Sequencer(d) for b, d in cls.data.items()}

    def entry(self, b, lang, form):
        return next(e for e in self.data[b]['lexicon'] if e['lang'] == lang and e['form'] == form)

    def test_allomorphs(self):
        for b, lang, form, expected in [('quenya', 'q', '-(n)dil', ['ndil', 'dil']), ('quenya', 'q', 'al(a)-¹', ['ala', 'al']),
                                        ('sindarin', 's', '-(r)on', ['ron', 'on']), ('quenya', 'q', '-itë', ['ite'])]:
            self.assertEqual(affixes.allomorphs(self.entry(b, lang, form), b), expected, form)

    def test_derivation(self):
        b = 'quenya'
        lex = {e['id']: e for e in self.data[b]['lexicon']}
        model = affixes.learn(self.data[b]['affixes']['cases'])
        cen, ima = self.entry(b, 'q', 'cen-'), self.entry(b, 'q', '-ima')
        # either order of picking: the suffix goes last
        for ids in ([cen['id'], ima['id']], [ima['id'], cen['id']]):
            vs = compound.predict(lex, self.seq[b], ids, 'late', 2, affix_model=model)
            self.assertEqual(vs[0]['form'], 'kēnima')      # cénima «visible», PE22/156
            self.assertEqual(vs[0]['kind'], 'suffix')
        u, linde = self.entry(b, 'q', 'ú-'), self.entry(b, 'q', 'lindë')
        vs = compound.predict(lex, self.seq[b], [u['id'], linde['id']], 'late', 2, affix_model=model)
        self.assertEqual(vs[0]['form'], 'ūlinde')

    def test_no_deep_junction_changes(self):
        for b, data in self.data.items():
            for r in data['affixes']['cases']:
                self.assertLessEqual(max(r['junction'][0], r['junction'][1]), affixes.MAX_OP, r['form'])

    def test_leave_one_out_floor(self):
        floors = {'quenya': (0.55, 0.65), 'sindarin': (0.42, 0.52)}
        for b, (main, anyv) in floors.items():
            r = affixes.leave_one_out(b, self.data[b]['lexicon'])
            self.assertGreaterEqual(r['main'] / r['cases'], main, b)
            self.assertGreaterEqual(r['any'] / r['cases'], anyv, b)


class Backform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()['quenya']
        cls.seq = Sequencer(cls.data)

    def test_linde(self):
        # lindë has no derivation of its own; ᴹ✶lindē and Ety GLIN show the expected answers
        found = [f['primitive'] for f in backform.backform(self.seq, self.seq.backform_table('q'), 'linde', 'late', 2)]
        self.assertIn('lindē', found)
        self.assertIn('glindē', found)

    def test_every_candidate_is_verified(self):
        for f in backform.backform(self.seq, self.seq.backform_table('q'), 'ambar', 'late', 2):
            last = f['trace'][-1][2] if f['trace'] else f['primitive']
            self.assertEqual(comparable(last), 'ambar')


if __name__ == '__main__':
    unittest.main()
