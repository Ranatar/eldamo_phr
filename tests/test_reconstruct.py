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
        # Q. fara- 'to hunt': Eldamo's derivation is of the gerund farálë < ✶pʰáralē
        e = self.ctx.lexicon['quenya']['550230859']
        self.assertNotIn('pʰaralē', e.get('starts', []))
        self.assertIn('farále', [o['form'] for o in e.get('other_forms', [])])
        got = self.forms(('quenya', 'late', 2), ('sindarin', 'late', 3), word='550230859')
        self.assertEqual(got[0], 'fara')          # a verb stem keeps its vowel

    def test_rare_correspondences_when_nothing_else(self):
        # S. ereb as a bare form: -b < -kwā is rare in the derivations
        self.assertTrue(self.forms(('sindarin', 'late', 3), ('quenya', 'late', 2), form='ereb', spelled=True))


if __name__ == '__main__':
    unittest.main()
