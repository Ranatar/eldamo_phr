"""Stress, boundaries and the chronological sequencer."""
import unittest

from tests.support import branches
from shared.interpreter import apply, apply_rule, compile_rule, comparable, phonemes
from shared.sequencer import Sequencer, backtest
from shared.stress import nuclei, stressed


def run(src, dst, form, **kw):
    return apply_rule(compile_rule(src, dst), form, **kw)['ordered']


def stressed_vowel(form, mode):
    word = phonemes(form)
    return ''.join(word[i] for i in sorted(stressed(word, mode)))


class Stress(unittest.TestCase):
    def test_initial(self):
        self.assertEqual(stressed_vowel('kalāra', 'initial'), 'a')
        self.assertEqual(phonemes('kalāra').index('a'), 1)

    def test_latin(self):
        # penult heavy (long vowel or two consonants) takes the stress, else the antepenult
        self.assertEqual(stressed_vowel('kalāra', 'latin'), 'ā')
        word = phonemes('falassa')
        self.assertEqual(sorted(stressed(word, 'latin')), [3])
        word = phonemes('kalima')
        self.assertEqual(sorted(stressed(word, 'latin')), [1])
        # disyllables: first syllable
        self.assertEqual(sorted(stressed(phonemes('lindē'), 'latin')), [1])

    def test_strack_examples(self):
        # Eldamo "stress" entries: LAS.se, ni.QUES.se, TYA.li.e, las.se.LAN.ta;
        # BE.ren, fin.AR.fin, CE.le.born, ca.le.NAR.dhon, o.RO.phin
        cases = [('lasse', 'latin', 1), ('nikwesse', 'latin', 4), ('tjalie', 'latin', 2),
                 ('lasselanta', 'latin', 6), ('beren', 'latin-sindarin', 1),
                 ('finarfin', 'latin-sindarin', 3), ('keleborn', 'latin-sindarin', 1),
                 ('kalenarðon', 'latin-sindarin', 5), ('orofin', 'latin-sindarin', 2)]
        for form, mode, index in cases:
            self.assertEqual(sorted(stressed(phonemes(form), mode)), [index], form)

    def test_diphthong_is_one_nucleus(self):
        self.assertEqual(len(nuclei(phonemes('gail'))), 1)
        self.assertEqual(len(nuclei(phonemes('maia'))), 2)

    def test_marked_stress_wins(self):
        self.assertEqual(stressed_vowel('álākō', 'latin'), 'á')


class StressMarks(unittest.TestCase):
    def test_unstressed_long_vowel(self):
        # ˌV̄S: only an unstressed long vowel before another syllable shortens
        self.assertEqual(run('ˌV̄S', 'V̆S', 'dōmi', stress_mode='initial'), [])
        self.assertEqual([comparable(x) for x in run('ˌV̄S', 'V̆S', 'kalāra', stress_mode='initial')], ['kalara'])

    def test_unknown_stress_ignores_marks(self):
        self.assertTrue(run('ˌV̄S', 'V̆S', 'dōmi'))

    def test_stressed_vowel(self):
        self.assertEqual(run('wŏ́', 'wa', 'wolo', stress_mode='initial'), ['walo'])
        self.assertEqual(run('wŏ́', 'wa', 'kawo', stress_mode='initial'), [])


class Boundaries(unittest.TestCase):
    def test_boundary_kept_and_required(self):
        self.assertEqual(apply('n+m', 'm+m', 'kan+mal')['ordered'], ['kam+mal'])
        self.assertEqual(apply('n+m', 'm+m', 'ka+nmal')['ordered'], [])

    def test_boundary_survives_other_rules(self):
        self.assertEqual(apply('a', 'e', 'ka+ra')['ordered'], ['ke+re'])
        self.assertEqual(apply('Cĭ+C', 'Cø+C', 'tali+nde')['ordered'], ['tal+nde'])


class Phonotactics(unittest.TestCase):
    def test_diphthong_offglide(self):
        self.assertEqual(apply('u', 'o', 'anour')['ordered'], [])
        self.assertEqual(apply('ou', 'au', 'anour')['ordered'], ['anaur'])
        self.assertEqual(apply('ij', 'i', 'maija')['ordered'], ['maia'])

    def test_labialized_velar_is_one_consonant(self):
        self.assertIn('alkwā', apply('aCaCV', 'aCCV', 'alakwā')['ordered'])

    def test_monosyllable_scope(self):
        self.assertEqual(run('C*ăC', 'C*āC', 'bar', scope='mono'), ['bār'])
        self.assertEqual(run('C*ăC', 'C*āC', 'θand', scope='mono'), [])
        self.assertEqual(run('C*ĭC', 'C*īC', 'gail', scope='mono'), [])
        self.assertEqual(run('C*ăC', 'C*āC', 'barad', scope='mono'), [])


class SequencerRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.seq = {b: Sequencer(d) for b, d in cls.data.items()}

    def form(self, branch, era, first, last, word):
        seq = self.seq[branch]
        return comparable(seq.run(word, seq.sequence(era, first, last))[0]['form'])

    def test_rule_order_is_complete(self):
        for seq in self.seq.values():
            self.assertEqual(len(seq.rules), len({c.id for c in seq.rules}))
            for c in seq.rules:
                self.assertIsNotNone(c.order)

    def test_elsewhere_condition(self):
        # [sr] became [ss] precedes initial [s] unvoicing, but does not take its sites
        self.assertEqual(self.form('quenya', 'late', 1, 1, 'srōn'), comparable('r̥ōn'))

    def test_known_derivations(self):
        self.assertEqual(self.form('sindarin', 'late', 0, 3, 'ambar'), 'amar')
        self.assertEqual(self.form('sindarin', 'late', 0, 3, 'kairē'), 'kaer')

    def test_backtest_floor(self):
        # regression guard: share of derivations whose main reading is the attested form
        floor = {'quenya': 0.75, 'sindarin': 0.65}
        for b, data in self.data.items():
            r = backtest(data, self.seq[b])
            self.assertGreaterEqual(r['main'] / r['derivations'], floor[b], b)
            self.assertGreaterEqual(r['any'], r['main'])


if __name__ == '__main__':
    unittest.main()
