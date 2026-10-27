"""Roots through Eldamo's links (shared/lexicon.py) and roots for a primitive form (shared/roots.py)."""
import unittest

from tests.support import branches
from shared import roots


class Roots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.table = roots.table(cls.data['quenya']['lexicon'])

    def entry(self, b, lang, form):
        e, = [e for e in self.data[b]['lexicon'] if e['lang'] == lang and e['form'] == form]
        return e

    def test_roots_of_elements(self):
        # Q. hyarma: no root of its own; hyar- < ᴹ√KHYAR, má < √MAƷ
        rs = self.entry('quenya', 'q', 'hyarma')['roots']
        self.assertIn('KHYAR', [r['form'] for r in rs])
        self.assertTrue(all(r['via'] == 'element' for r in rs))

    def test_compound_roots_by_element(self):
        # Q. palantír: palan < √PAL + tir- < √TIR (the page names only TIR); not the roots of
        # S. Gwahaedir, which Eldamo links to it as a cognate
        rs = self.entry('quenya', 'q', 'palantír')['roots']
        self.assertEqual([(r['form'], r['part']) for r in rs], [('PAL', 0), ('TIR', 1)])
        rs = self.entry('quenya', 'q', 'hyarma')['roots']
        self.assertEqual([(r['form'], r['part']) for r in rs], [('KHYAR', 0), ('MAH', 1), ('MAG', 1)])

    def test_roots_of_cognates(self):
        # Q. Perian: no root, no elements; cognate S. Perian = per- + ?, per- < √PER
        rs = self.entry('quenya', 'q', 'Perian')['roots']
        self.assertEqual([(r['form'], r['via']) for r in rs], [('PER', 'cognate')])

    def test_own_roots_come_first(self):
        rs = self.entry('quenya', 'q', 'lár')['roots']
        self.assertEqual([(r['form'], r.get('via')) for r in rs], [('DAR', None)])

    def test_candidates(self):
        best = lambda f, era: roots.candidates(self.table, f, era, 1)[0][3]
        self.assertEqual(best('kʰjarja', 'middle'), 'KHYAR')
        self.assertEqual(best('ambara', 'late'), 'MBAR')          # after the augment a-
        self.assertEqual(best('periandō', 'late'), 'PER')
        # nasal infixion: KAB > kambā is found, though √KAM, whose whole form begins the word, ranks first
        self.assertIn('KAB', [c[3] for c in roots.candidates(self.table, 'kambā', 'late', 4)])

    def test_root_seeds_the_primitive(self):
        # Q. hyarma: the backward search gives ✶j̊arma; ᴹ√KHYAR says hy- was kʰj-
        from shared import reconstruct as R
        ctx = R.Context(self.data)
        e = self.entry('quenya', 'q', 'hyarma')
        vs = R.reconstruct(ctx, ('quenya', 'late', 2), ('quenya', 'late', 0), word=e['id'])
        self.assertEqual(vs[0]['form'], 'kʰjarma')
        self.assertIn('root', vs[0]['marks'])
        # each conception has its own roots: ᴱ√MBARA for the early one
        self.assertEqual([c[2] for c in roots.candidates(self.table, 'ambara', 'early', 3)], ['ep'] * 3)
        self.assertEqual(roots.candidates(self.table, 'aeiou', 'late', 3), [])          # no consonants, no root


if __name__ == '__main__':
    unittest.main()
