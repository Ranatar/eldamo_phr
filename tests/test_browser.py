"""The built atlas and corpus browser in a real browser (Playwright, optional).

Skipped when Playwright or its Chromium is unavailable, or when
ELDAMO_SKIP_BROWSER=1. Set ELDAMO_REQUIRE_BROWSER=1 to turn a missing
browser into a failure, and ELDAMO_CHROMIUM=/path/to/chrome to use a
specific browser executable.
"""
import os
import unittest

from tests.support import ROOT, branches

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

REQUIRE = os.environ.get('ELDAMO_REQUIRE_BROWSER') == '1'
SKIP = os.environ.get('ELDAMO_SKIP_BROWSER') == '1'


@unittest.skipIf(SKIP, 'ELDAMO_SKIP_BROWSER=1')
class Browser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            if REQUIRE:
                raise RuntimeError('playwright is not installed')
            raise unittest.SkipTest('playwright is not installed')
        cls.pw = sync_playwright().start()
        try:
            exe = os.environ.get('ELDAMO_CHROMIUM')
            cls.browser = cls.pw.chromium.launch(executable_path=exe) if exe else cls.pw.chromium.launch()
        except Exception as exc:  # browser binary missing
            cls.pw.stop()
            if REQUIRE:
                raise
            raise unittest.SkipTest(f'no Chromium for Playwright: {exc}')
        cls.atlas = (ROOT / 'app' / 'index.html').as_uri()
        cls.corpus = (ROOT / 'app' / 'corpus.html').as_uri()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def page(self, url, width=1280):
        page = self.browser.new_page(viewport={'width': width, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(url)
        self.addCleanup(page.close)
        self.addCleanup(lambda: self.assertEqual(errors, []))
        return page

    def test_intro_search_and_word(self):
        page = self.page(self.atlas)
        self.assertIn('Quettamin', page.inner_text('#intro'))
        self.assertTrue(page.is_hidden('#word-card'))
        # the reference is collapsed and not drawn until opened
        self.assertFalse(page.evaluate("document.getElementById('ref-paths').open"))
        self.assertEqual(page.inner_text('#output'), '')
        page.fill('#q', 'galadh')
        page.click('#q-results button[data-word="3005081253"]')     # S. galadh, not N. galadh
        page.wait_for_function("location.hash.includes('w=3005081253') && !document.getElementById('word-card').hidden")
        self.assertIn('galadh', page.inner_text('#word-card'))
        self.assertTrue(page.is_hidden('#intro'))
        # the panorama fills every period; the word's own cell is attested
        page.wait_for_function("[...document.querySelectorAll('.pcell .pform')].every(x => x.textContent !== '…')", timeout=60000)
        self.assertIn('attested', page.get_attribute('.pcell[data-cell="sindarin/late/3"]', 'class'))
        self.assertGreaterEqual(page.locator('.pcell').count(), 15)

    def test_neologisms_by_switch(self):
        page = self.page(self.atlas)
        page.fill('#q', 'ticket')
        self.assertNotIn('lelyaláve', page.inner_text('#q-results'))
        page.check('#neo-toggle')
        self.assertIn('lelyaláve', page.inner_text('#q-results'))

    def test_reference_sections(self):
        page = self.page(self.atlas + '#ref=paths&b=quenya&era=late&from=b&to=v')
        self.assertTrue(page.evaluate("document.getElementById('ref-paths').open"))
        self.assertFalse(page.evaluate("document.getElementById('ref-chains').open"))
        out = page.inner_text('#output')
        self.assertIn('b → v', out)
        page.click('#rules-to')
        self.assertIn('Правила со звуком [v]', page.inner_text('#output'))
        # cluster rules used to be empty because formulas were split on the wrong arrows
        page.click('.picker[data-slot=from] .mode-switch button[data-mode=cluster]')
        page.fill('#from-cluster', 'mb')
        page.dispatch_event('#from-cluster', 'change')
        page.click('#rules-from')
        self.assertNotIn('Подформул с этим звуком нет', page.inner_text('#output'))
        page.click('#ref-toggle-all')
        self.assertTrue(page.evaluate("document.getElementById('ref-derivations').open"))
        self.assertEqual(page.inner_text('#ref-toggle-all'), 'Свернуть всё')
        self.assertIn('цепоч', page.inner_text('#chains'))
        page.fill('#deriv-query', 'alda')
        self.assertIn('alda', page.inner_text('#derivations'))
        page.click('#ref-toggle-all')
        self.assertFalse(page.evaluate("document.getElementById('ref-chains').open"))

    def test_era_switch_updates_reference(self):
        page = self.page(self.atlas + '#ref=chains&b=sindarin')
        late = page.inner_text('#chains').split('\n')[0]
        page.select_option('#era-select', 'middle')
        self.assertNotEqual(late, page.inner_text('#chains').split('\n')[0])
        self.assertIn('era=middle', page.evaluate('location.hash'))

    def test_old_addresses_and_back(self):
        # addresses of the phonetic atlas open the reference with the same sounds
        page = self.page(self.atlas + '#quenya')
        self.assertIn('ref=paths', page.evaluate('location.hash'))
        self.assertTrue(page.evaluate("document.getElementById('ref-paths').open"))
        page.select_option('#branch-select', 'sindarin')
        page.wait_for_function("location.hash.includes('b=sindarin')")
        page.go_back()
        page.wait_for_function("document.getElementById('branch-select').value === 'quenya'")

    def test_malformed_hash_and_cluster_in_hash(self):
        page = self.page(self.atlas + '#%')
        self.assertTrue(page.is_visible('#intro'))
        page.evaluate("location.hash = 'sindarin?from=nt'")
        page.wait_for_function("document.getElementById('branch-select').value === 'sindarin'")
        box = '.picker[data-slot=from]'
        self.assertEqual(page.get_attribute(box + ' .mode-switch button[data-mode=cluster]', 'aria-pressed'), 'true')
        self.assertEqual(page.input_value('#from-cluster'), 'nt')

    def test_narrow_screen(self):
        page = self.page(self.atlas + '#w=403686503', width=375)
        page.wait_for_function("[...document.querySelectorAll('.pcell .pform')].every(x => x.textContent !== '…')", timeout=60000)
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 375)
        page.goto(self.atlas + '#ref=paths&b=quenya')
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 375)

    def test_wordform_engine_matches_python(self):
        # app/wordform.js repeats shared/ (interpreter, sequencer, junctions, compounds, backform)
        from shared.parity import vectors
        V = vectors(branches())
        recon = V.pop('__recon__')[::3]        # a third of the reconstruction calls: each takes a while
        page = self.page(self.atlas)
        bad = page.evaluate("cases => WF.parityRecon({quenya: WFUI.engine('quenya'), sindarin: WFUI.engine('sindarin')}, cases)", recon)
        self.assertEqual(bad, [], 'reconstruction')
        for b, v in V.items():
            bad = page.evaluate('([b, v]) => WF.parity(WFUI.engine(b), v)', [b, v])
            self.assertEqual(bad, [], b)

    def test_wordform_panel(self):
        page = self.page(self.atlas + '#tab=compose')
        page.fill('#wf-q1', 'Ambar')
        page.click('#wf-r1 button[data-id="4273482913"]')        # Ambar "world", not ambar "fate"
        page.fill('#wf-q2', 'lindë')
        page.click('#wf-r2 button[data-id="403686503"]')
        self.assertIn('lindi-', page.inner_text('#wf-chosen2'))
        page.click('#wf-go')
        first = page.inner_text('#wf-output .wf-variant.main')
        self.assertIn('amballindë', first)
        self.assertIn('Casallië', page.inner_text('#wf-output'))
        # formed in Primitive Elvish: the laws of Ancient Quenya and Quenya act on the join
        page.select_option('#wf-stage', '0')
        page.click('#wf-go')
        self.assertIn('восстановлена', page.inner_text('#wf-output'))
        self.assertGreater(page.locator('#wf-output .wf-variant').count(), 1)
        # a variant becomes the current word: a form without an Eldamo page
        page.click('#wf-output .wf-variant.main [data-use]')
        page.wait_for_function("location.hash.includes('f=') && document.getElementById('word-card').textContent.includes('Форма без статьи')")
        self.assertIn('Форма без статьи Eldamo', page.inner_text('#word-card'))

    def test_word_is_first_element(self):
        page = self.page(self.atlas + '#w=4273482913&tab=compose')
        self.assertIn('Ambar', page.inner_text('#wf-chosen1'))
        self.assertEqual(page.input_value('#wf-branch'), 'quenya')

    def test_wordform_suffix(self):
        page = self.page(self.atlas + '#tab=compose')
        page.fill('#wf-q1', '-ima')
        page.click('#wf-r1 button:has-text("-ima")')
        self.assertIn('суффикс', page.inner_text('#wf-chosen1'))
        page.fill('#wf-q2', 'cen-')
        page.click('#wf-r2 button:has(.form:text-is("cen-"))')
        page.click('#wf-go')
        self.assertIn('cénima', page.inner_text('#wf-output .wf-variant.main'))
        self.assertIn('Засвидетельствованные слова с этим аффиксом', page.inner_text('#wf-output'))

    def test_reconstruction_panel(self):
        page = self.page(self.atlas + '#w=403686503')
        self.assertEqual(page.input_value('#rc-src'), 'quenya|late|2')
        page.select_option('#rc-dst', 'quenya|late|0')
        page.click('#rc-go')
        self.assertIn('lindē', page.inner_text('#rc-output'))
        # a cognate through the common primitive form
        page.select_option('#rc-dst', 'sindarin|late|3')
        page.click('#rc-go')
        self.assertIn('через праформу', page.inner_text('#rc-output'))
        # the middle conception: Eldamo's own link comes first
        page.select_option('#rc-dst', 'quenya|middle|2')
        page.click('#rc-go')
        self.assertIn('связь Eldamo', page.inner_text('#rc-output .wf-variant.main'))

    def test_panorama_cell_and_rule_in_reference(self):
        page = self.page(self.atlas + '#w=3880471189')                # Q. lelya "delicate"
        page.wait_for_selector('.pcell[data-cell="sindarin/late/3"] .sym')
        page.click('.pcell[data-cell="sindarin/late/3"]')
        main = page.inner_text('#rc-output .wf-variant.main')
        self.assertIn('dail', main)
        self.assertIn('dst=sindarin', page.evaluate('location.hash'))
        # rules are grouped by stage and open in the reference
        page.click('#rc-output .wf-variant.main details.stages summary')
        page.click('#rc-output .wf-variant.main [data-rule]')
        page.wait_for_function("location.hash.includes('ref=rule') && document.getElementById('ref-paths').open")
        self.assertIn('Правило', page.inner_text('#output'))
        # the word stays chosen
        self.assertIn('lelya', page.inner_text('#word-card'))

    def test_open_word_from_derivation(self):
        page = self.page(self.atlas + '#ref=derivations&b=quenya&q=alda')
        page.click('#derivations details.card summary >> nth=0')
        page.click('#derivations [data-word] >> nth=0')
        page.wait_for_function("location.hash.includes('w=') && !document.getElementById('word-card').hidden")

    def test_early_conception(self):
        page = self.page(self.atlas + '#ref=paths&b=quenya&era=early')
        self.assertEqual(page.input_value('#era-select'), 'early')
        self.assertIn('Early Quenya', page.inner_text('#branch-path'))

    def test_corpus_browser(self):
        page = self.page(self.corpus)
        self.assertIn('записей', page.inner_text('#count'))
        page.select_option('#branch', 'sindarin')
        page.click('[data-section=derivations]')
        page.fill('#q', 'aglareb')
        self.assertFalse(page.inner_text('#count').startswith('0 '))
        self.assertIn('aglareb', page.inner_text('#body'))


if __name__ == '__main__':
    unittest.main()
