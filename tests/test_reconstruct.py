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
        got = self.forms(('quenya', 'late', 2), ('quenya', 'late', 0), word=self.linde['id'])
        self.assertEqual(got[0], 'lindē')
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


if __name__ == '__main__':
    unittest.main()
