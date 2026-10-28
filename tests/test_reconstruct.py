"""Reconstruction between periods (shared/reconstruct.py)."""
import unittest

from tests.support import branches
from shared import reconstruct as R
from shared.interpreter import comparable


class Reconstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = R.Context(branches())
        q = cls.ctx.lexicon['quenya']
        cls.linde = next(e for e in q.values() if e['form'] == 'lindë' and e['lang'] == 'q')

    def forms(self, src, dst, **kw):
        return [comparable(v['form']) for v in R.reconstruct(self.ctx, src, dst, **kw)]

    def test_normalized_stages(self):
        for b, norm in self.ctx.normal.items():
            self.assertGreater(len(norm), 1500, b)
            with_primitive = sum(1 for n in norm if 0 in n['forms'])
            self.assertGreater(with_primitive / len(norm), 0.4, b)
            for n in norm:
                self.assertGreaterEqual(len(n['forms']), 1)

    def test_backward_to_primitive(self):
        # lindë has no derivation; ᴹ✶lindē and ✶GLIN (Ety) are Tolkien's
        # Q. -e continues ✶-e as well as ✶-ē: both are verified, the root ranks them up
        got = self.forms(('quenya', 'late', 2), ('quenya', 'late', 0), word=self.linde['id'])
        self.assertIn('lindē', got[:3])
        self.assertIn('glindē', got)

    def test_every_backward_form_is_verified(self):
        vs = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('quenya', 'late', 1), word=self.linde['id'])
        for v in vs:
            run = self.ctx.forward('quenya', 'late', v['form'], 1, 2)
            self.assertIn('linde', [comparable(f) for f, _ in run], v['form'])

    def test_forward(self):
        # Ancient Quenya / Old Sindarin forms of a primitive form by the laws
        self.assertEqual(self.forms(('sindarin', 'late', 0), ('sindarin', 'late', 3), form='ambar')[0], 'amar')

    def test_cognate(self):
        got = self.forms(('quenya', 'late', 2), ('sindarin', 'late', 3), word=self.linde['id'])
        self.assertIn('glinn', got)       # N. glinn, Ety/GLIN

    def test_conception_link_first(self):
        vs = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('quenya', 'middle', 2), word=self.linde['id'])
        self.assertIn('link', vs[0]['marks'])
        vs = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('quenya', 'middle', 2), word=self.linde['id'],
                           use_links=False)
        self.assertFalse(any('link' in v['marks'] for v in vs))
        self.assertTrue(any('neologism' in v['marks'] for v in vs))

    def test_phonotactics(self):
        pt = self.ctx.phonotactics('sindarin', 's')
        self.assertEqual(pt.problems('aglar'), [])
        self.assertTrue(pt.problems('lnn'))

    def test_stem_marks_the_final_vowel(self):
        # lindë (lindi-): the stem keeps the ancient i that became ë in the simplex (intro-quenya §2.4.2);
        # a candidate that gives the stem is marked, the weight does not change (STEM_BONUS)
        hints = R._hints(self.ctx, 'quenya', self.linde, 'late', 2)
        self.assertEqual(hints['stems'], ['lindi'])
        vs = {v['form']: v['marks'] for v in R.reconstruct(self.ctx, ('quenya', 'late', 2), ('quenya', 'late', 0),
                                                           word=self.linde['id'])}
        self.assertIn('stem', vs['lindi'])
        self.assertNotIn('stem', vs['lindē'])
        # the same form without the word: nothing to compare with
        vs = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('quenya', 'late', 0), form='linde')
        self.assertFalse(any('stem' in v['marks'] for v in vs))

    def test_compound_by_cognate_elements(self):
        # S. Adanel = Adan + -iel¹ has no Quenya cognate in Eldamo; its elements do: Q. Atan, -iel.
        # Quenya -iel after n: aranel, Ailinel, but Uinéniel -- both are built
        vs = R.reconstruct(self.ctx, ('sindarin', 'late', 3), ('quenya', 'late', 2), word='4023112133')
        built = [v['form'] for v in vs if 'elements' in v['marks']]
        self.assertEqual(built[:2], ['atanel', 'ataniel'])
        self.assertIn('elements', vs[0]['marks'])
        # the earlier stages are taken back from the word so built, not from the Sindarin form
        for stage in (0, 1):
            vs = R.reconstruct(self.ctx, ('sindarin', 'late', 3), ('quenya', 'late', stage), word='4023112133')
            self.assertIn('elements', vs[0]['marks'], stage)
            run = [comparable(f) for f, _ in self.ctx.forward('quenya', 'late', vs[0]['form'], stage, 2)]
            self.assertTrue({'atanel', 'ataniel'} & set(run), (stage, vs[0]['form'], run))

    def test_root_match(self):
        self.assertTrue(R.root_match('glindē', ['GLIN']))
        self.assertTrue(R.root_match('mbara', ['MBAR']))
        self.assertFalse(R.root_match('dindē', ['LIN²']))

    def test_cognates_inside_references(self):
        # Q. erinqua: <cognate v="ereb" source="VT42/10.1912"/> inside a <ref>; S. ereb has a ref at that place
        e = self.ctx.lexicon['quenya']['700840261']
        self.assertIn('3983103205', [x['id'] for x in e['links']['cognate']])
        q = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('sindarin', 'late', 3), word='700840261')
        self.assertEqual((comparable(q[0]['form']), q[0]['marks']), ('ereb', ['link']))
        s = R.reconstruct(self.ctx, ('sindarin', 'late', 3), ('quenya', 'late', 2), word='3983103205')
        self.assertEqual(comparable(s[0]['form']), comparable('eriŋkwa'))     # the link read backwards

    def test_near_cognates(self):
        # without the link: S. ereb < ✶erikwā is one sound from ✶eriŋkwā and means 'single, alone' too
        q = R.reconstruct(self.ctx, ('quenya', 'late', 2), ('sindarin', 'late', 3), word='700840261', use_links=False)
        self.assertEqual(comparable(q[0]['form']), 'ereb')
        self.assertIn('near-cognate', q[0]['marks'])

    def test_cognate_link_first(self):
        # ᴹQ. fara- 'to hunt' ~ N. fara-: Eldamo's <cognate>
        vs = R.reconstruct(self.ctx, ('quenya', 'middle', 2), ('sindarin', 'middle', 2), word='2865546933')
        self.assertIn('link', vs[0]['marks'])
        self.assertEqual(comparable(vs[0]['form']), 'fara')

    def test_other_forms_are_not_the_word(self):
        # Q. fara- 'to hunt': Eldamo's derivation is of the inflected farále 'you hunt' < ✶pʰáralē
        # (a <ref> with <inflect form="aorist 2nd-sg"/>)
        e = self.ctx.lexicon['quenya']['550230859']
        self.assertNotIn('pʰaralē', e.get('starts', []))
        self.assertIn('farále', [o['form'] for o in e.get('other_forms', [])])
        got = self.forms(('quenya', 'late', 2), ('sindarin', 'late', 3), word='550230859')
        self.assertEqual(got[0], 'fara')          # a verb stem keeps its vowel

    def test_rare_correspondences_when_nothing_else(self):
        # S. ereb as a bare form: -b < -kwā is rare in the derivations
        self.assertTrue(self.forms(('sindarin', 'late', 3), ('quenya', 'late', 2), form='ereb', spelled=True))

    def entry(self, branch, form):
        code = {'quenya': 'q', 'sindarin': 's'}[branch]
        return next(e for e in self.ctx.lexicon[branch].values() if e['form'] == form and e['lang'] == code)

    def test_one_law_left_out_when_nothing_else(self):
        # S. randir keeps nd, which "[mb], [nd] became [mm], [nn]" makes nn ("usually", says Tolkien)
        e = self.entry('sindarin', 'randir')
        vs = R.reconstruct(self.ctx, ('sindarin', 'late', 3), ('sindarin', 'late', 0), word=e['id'])
        irr = [v for v in vs if 'irregular' in v['marks']]
        self.assertTrue(irr)
        self.assertIn('868023175', [t[0] for t in irr[0]['steps'] if t[2] is None])

    def test_compound_by_its_elements(self):
        # S. Mithrandir = mith + randir: no form gives it by the laws; its make-up at the
        # primitive stage is shown, marked as not leading to the word
        e = self.entry('sindarin', 'Mithrandir')
        vs = R.reconstruct(self.ctx, ('sindarin', 'late', 3), ('sindarin', 'late', 0), word=e['id'])
        self.assertTrue(vs)
        self.assertEqual(set(vs[0]['marks']), {'elements', 'unconfirmed'})
        self.assertTrue(vs[0]['form'].startswith('mitʰi'))
        # and through it, the other branch
        self.assertTrue(self.forms(('sindarin', 'late', 3), ('quenya', 'late', 2), word=e['id']))

    def test_no_compound_by_a_partial_cognate(self):
        # S. Arthedain = arthor + Adan; Q. turmen is a partial cognate of arthor: no ✶turmenatan
        e = self.entry('sindarin', 'Arthedain')
        self.assertNotIn('turmenatan', self.forms(('sindarin', 'late', 3), ('quenya', 'late', 2), word=e['id']))


if __name__ == '__main__':
    unittest.main()
