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

    def test_landing_then_branch(self):
        page = self.page(self.atlas)
        self.assertTrue(page.is_visible('#landing'))
        self.assertTrue(page.is_hidden('#app'))
        page.click('[data-branch=quenya]')
        page.wait_for_function("location.hash.startsWith('#quenya')")
        self.assertTrue(page.is_hidden('#landing'))
        self.assertIn('засвидетельствован целиком', page.inner_text('#output'))

    def test_paths_rules_chains_derivations(self):
        page = self.page(self.atlas + '#quenya?era=late&from=b&to=v')
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
        self.assertIn('цепоч', page.inner_text('#chains'))
        page.fill('#deriv-query', 'alda')
        self.assertIn('alda', page.inner_text('#derivations'))

    def test_era_switch_updates_everything(self):
        page = self.page(self.atlas + '#sindarin')
        late = page.inner_text('#chains').split('\n')[0]
        page.select_option('#era-select', 'middle')
        self.assertNotEqual(late, page.inner_text('#chains').split('\n')[0])
        self.assertIn('era=middle', page.evaluate('location.hash'))

    def test_hash_navigation_and_back(self):
        page = self.page(self.atlas + '#quenya')
        page.evaluate("location.hash = 'sindarin'")
        page.wait_for_function("document.getElementById('branch-select').value === 'sindarin'")
        page.go_back()
        page.wait_for_function("document.getElementById('branch-select').value === 'quenya'")

    def test_malformed_hash_and_cluster_in_hash(self):
        page = self.page(self.atlas + '#%')
        self.assertTrue(page.is_visible('#landing'))
        page.evaluate("location.hash = 'sindarin?from=nt'")
        page.wait_for_function("document.getElementById('branch-select').value === 'sindarin'")
        box = '.picker[data-slot=from]'
        self.assertEqual(page.get_attribute(box + ' .mode-switch button[data-mode=cluster]', 'aria-pressed'), 'true')
        self.assertEqual(page.input_value('#from-cluster'), 'nt')

    def test_narrow_screen(self):
        page = self.page(self.atlas + '#quenya', width=375)
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 375)

    def test_wordform_engine_matches_python(self):
        # app/wordform.js repeats shared/ (interpreter, sequencer, junctions, compounds, backform)
        from shared.parity import vectors
        V = vectors(branches())
        recon = V.pop('__recon__')[::3]        # a third of the reconstruction calls: each takes a while
        page = self.page(self.atlas + '#quenya')
        bad = page.evaluate("cases => WF.parityRecon({quenya: WFUI.engine('quenya'), sindarin: WFUI.engine('sindarin')}, cases)", recon)
        self.assertEqual(bad, [], 'reconstruction')
        for b, v in V.items():
            bad = page.evaluate('([b, v]) => WF.parity(WFUI.engine(b), v)', [b, v])
            self.assertEqual(bad, [], b)

    def test_wordform_panel(self):
        page = self.page(self.atlas + '#quenya')
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

    def test_wordform_suffix(self):
        page = self.page(self.atlas + '#quenya')
        page.fill('#wf-q1', '-ima')
        page.click('#wf-r1 button:has-text("-ima")')
        self.assertIn('суффикс', page.inner_text('#wf-chosen1'))
        page.fill('#wf-q2', 'cen-')
        page.click('#wf-r2 button:has(.form:text-is("cen-"))')
        page.click('#wf-go')
        self.assertIn('cénima', page.inner_text('#wf-output .wf-variant.main'))
        self.assertIn('Засвидетельствованные слова с этим аффиксом', page.inner_text('#wf-output'))

    def test_reconstruction_panel(self):
        page = self.page(self.atlas + '#quenya')
        page.fill('#rc-q', 'lindë')
        page.click('#rc-r button[data-id="403686503"]')
        self.assertEqual(page.input_value('#rc-src'), 'late|2')
        page.select_option('#rc-dst', 'late|0')
        page.click('#rc-go')
        self.assertIn('lindē', page.inner_text('#rc-output .wf-variant.main'))
        # a cognate through the common primitive form
        page.select_option('#rc-dst-branch', 'sindarin')
        page.select_option('#rc-dst', 'late|3')
        page.click('#rc-go')
        self.assertIn('через праформу', page.inner_text('#rc-output'))
        # the middle conception: Eldamo's own link comes first
        page.select_option('#rc-dst-branch', 'quenya')
        page.select_option('#rc-dst', 'middle|2')
        page.click('#rc-go')
        self.assertIn('связь Eldamo', page.inner_text('#rc-output .wf-variant.main'))

    def test_early_conception(self):
        page = self.page(self.atlas + '#quenya?era=early')
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
