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

    def test_roots_through_a_source_word(self):
        # S. Adanel = Adan + -iel¹; Adan < Q. Atan (a derivation, not a root), whose element atta < √ATATA;
        # -iel has no root: its primitive ✶-iel stands in its place
        e = self.entry('sindarin', 's', 'Adanel')
        self.assertEqual([(r['form'], r['part']) for r in e['roots']], [('ATATA', 0)])
        self.assertEqual([(g['form'], g['part']) for g in e['root_gaps']], [('-iel', 1)])
        self.assertEqual([(r['form'], r['via']) for r in self.entry('sindarin', 's', 'Adan')['roots']], [('ATATA', 'source')])

    def test_roots_through_elements_of_elements(self):
        # S. Mithrandir = mith + randir, randir = √RAN + dîr < √N(D)ER: three roots, though the page
        # of randir names RAN alone; S. Arthedain = arthor + Adan, arthor < ✶artaurē = √RĀ/ARA + √TUR
        parts = lambda e: [sorted(r['form'] for r in e['roots'] if r['part'] == k)
                           for k in sorted({r['part'] for r in e['roots']})]
        self.assertEqual(parts(self.entry('sindarin', 's', 'Mithrandir')), [['MITH'], ['RAN'], ['N(D)ER']])
        self.assertEqual(parts(self.entry('sindarin', 's', 'Arthedain')), [['RĀ/ARA'], ['TUR'], ['ATATA']])

    def test_partial_cognate(self):
        # S. arthor √RĀ/ARA + √TUR ~ Q. turmen √TUR + √MEN: shown after the laws, marked partial
        from shared import reconstruct as R
        lex = {e['id']: e for b in self.data for e in self.data[b]['lexicon']}
        arthor = self.entry('sindarin', 's', 'arthor')
        turmen = self.entry('quenya', 'q', 'turmen')
        self.assertTrue(R.partial_cognate(arthor, turmen))
        self.assertFalse(R.partial_cognate(self.entry('quenya', 'q', 'calar'), self.entry('sindarin', 's', 'calar')))
        ctx = R.Context(self.data)
        vs = R.reconstruct(ctx, ('sindarin', 'late', 3), ('quenya', 'late', 2), word=arthor['id'])
        marks = {v['form']: v['marks'] for v in vs}
        self.assertIn('partial', marks.get('turmen', []))
        self.assertNotIn('partial', vs[0]['marks'])

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
        # Q. hyarma: the backward search gives ✶j̊arma; ᴹ√KHYAR says hy- was kʰj- (its make-up,
        # hyar- + má < ✶maɣ-, comes first: ✶kʰjar+maɣa)
        from shared import reconstruct as R
        ctx = R.Context(self.data)
        e = self.entry('quenya', 'q', 'hyarma')
        vs = R.reconstruct(ctx, ('quenya', 'late', 2), ('quenya', 'late', 0), word=e['id'])
        self.assertEqual(vs[0]['form'], 'kʰjarmaɣa')
        self.assertIn('elements', vs[0]['marks'])
        laws = [v for v in vs if 'elements' not in v['marks']]
        self.assertEqual(laws[0]['form'], 'kʰjarma')
        self.assertIn('root', laws[0]['marks'])
        # a root that ends in its vowel gives it too: S. rhûn < ✶srōn- ((S)RŌ; Q. rómen), not ✶srūn-
        e = self.entry('sindarin', 's', 'rhûn')
        vs = R.reconstruct(ctx, ('sindarin', 'late', 3), ('sindarin', 'late', 0), word=e['id'])
        self.assertTrue(vs[0]['form'].startswith('srō'), vs[0]['form'])
        # each conception has its own roots: ᴱ√MBARA for the early one
        self.assertEqual([c[2] for c in roots.candidates(self.table, 'ambara', 'early', 3)], ['ep'] * 3)
        self.assertEqual(roots.candidates(self.table, 'aeiou', 'late', 3), [])          # no consonants, no root


if __name__ == '__main__':
    unittest.main()
