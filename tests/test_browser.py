"""The built atlas and corpus browser in a real browser (Playwright, optional).

Skipped when Playwright or its Chromium is unavailable, or when
ELDAMO_SKIP_BROWSER=1. Set ELDAMO_REQUIRE_BROWSER=1 to turn a missing
browser into a failure, and ELDAMO_CHROMIUM=/path/to/chrome to use a
specific browser executable.
"""
import os
import re
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

    def page(self, url, width=1280, locale='ru-RU'):
        page = self.browser.new_page(viewport={'width': width, 'height': 900}, locale=locale)
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
        V = vectors(branches(), recon_every=3)  # a third of the reconstruction calls: each takes a while
        recon = V.pop('__recon__')
        root_cases = V.pop('__roots__')
        page = self.page(self.atlas)
        bad = page.evaluate("cases => WF.parityRecon({quenya: WFUI.engine('quenya'), sindarin: WFUI.engine('sindarin')}, cases)", recon)
        self.assertEqual(bad, [], 'reconstruction')
        got = page.evaluate("cases => cases.map(([b, era, f]) => WF.rootCandidates(WFUI.engine(b), f, era, 5).map(c => c[1]))", root_cases)
        self.assertEqual(got, [c[3] for c in root_cases], 'root candidates')
        self.assertGreater(sum(1 for c in root_cases if c[3]), 10)
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
        # a variant becomes the current word: a word without an Eldamo page that keeps its elements
        page.click('#wf-output .wf-variant.main [data-use]')
        page.wait_for_function("location.hash.includes('of=4273482913') && document.getElementById('word-card').textContent.includes('Слово без статьи')")
        card = page.inner_text('#word-card')
        self.assertIn('Ambar + lindë', card)
        # its roots follow the elements' (√MBAR + √LIN²), not guessed from the form
        page.wait_for_function("document.querySelector('#panorama [data-roots=\"quenya/late\"]')")
        late = page.inner_text('#panorama [data-roots="quenya/late"]')
        self.assertNotIn('?', late)
        self.assertIn('+', late)

    def test_formed_word_keeps_etymology(self):
        # Q. quet- + alcar taken from word formation: the primitive form is the elements' (✶aklar),
        # Sindarin goes by their cognates S. ped- (through T. pet-) and S. aglar
        page = self.page(self.atlas + '#f=kʷetalkar&in=quenya/late/2&of=2355375457,2464648865')
        vs = page.evaluate('''() => WF.reconstruct(QU.allEngines(), ['quenya', 'late', 2], ['sindarin', 'late', 3],
            { form: 'kʷetalkar', elements: ['2355375457', '2464648865'], limit: 3 })''')
        self.assertIn('byElements', [s[0] for s in vs[0]['route']])
        self.assertIn('ped-', vs[0]['route'][0][1]['names'])
        self.assertIn('aglar', vs[0]['route'][0][1]['names'])
        p = page.evaluate('''() => WF.reconstruct(QU.allEngines(), ['quenya', 'late', 2], ['quenya', 'late', 0],
            { form: 'kʷetalkar', elements: ['2355375457', '2464648865'], limit: 1 })''')
        self.assertIn('kl', p[0]['form'])

    def test_one_primitive_for_both_branches(self):
        # Primitive Elvish is the ancestor of both branches: Q. quel- and its cognate S. pel- (no
        # Eldamo primitive for either) read back to one ✶kwel-, the same in both rows of the panorama
        page = self.page(self.atlas)
        q, s = page.evaluate('''() => [['quenya', 'late', 0], ['sindarin', 'late', 0]].map(dst =>
            WF.reconstruct(QU.allEngines(), ['quenya', 'late', 2], dst, { word: '3927334449', limit: 3 }))''')
        self.assertEqual(q[0]['form'], s[0]['form'])
        self.assertIn('joint', q[0]['marks'])
        self.assertIn('cognate', s[0]['marks'])
        # a word made in word formation in another conception: from its elements there (ᴹQ. quet-)
        m = page.evaluate('''() => WF.reconstruct(QU.allEngines(), ['quenya', 'late', 2], ['quenya', 'middle', 2],
            { form: 'kʷetalkar', elements: ['2355375457', '2464648865'], limit: 3 })''')
        self.assertTrue(any(seg[0] == 'byElements' for v in m for seg in v['route']))

    def test_root_instead_in_other_era(self):
        # G. cwîl < ᴱ√QḶÐḶ, which Eldamo deprecates for N√KWILID: the late roots are those, not the
        # roots of a word linked to it (ᴹ√MOY of NS. muig²)
        page = self.page(self.atlas + '#w=1512306021')
        page.wait_for_function("document.querySelector('#panorama [data-roots=\"sindarin/late\"]')")
        self.assertIn('KWILID', page.inner_text('#panorama [data-roots="sindarin/late"]'))
        self.assertIn('QḶÐḶ', page.inner_text('#panorama [data-roots="sindarin/early"]'))

    def test_three_elements(self):
        # a third element joins the first two: Q. alda + sil- + -ion
        page = self.page(self.atlas + '#tab=compose')
        self.assertTrue(page.locator('#wf-slot3').is_hidden())
        page.fill('#wf-q1', 'alda')
        page.click('#wf-r1 button:has(.form:text-is("alda"))')
        page.fill('#wf-q2', 'Isil')
        page.click('#wf-r2 button:has(.form:text-is("Isil"))')
        self.assertTrue(page.locator('#wf-slot3').is_visible())
        page.fill('#wf-q3', '-ion')
        page.click('#wf-r3 button:has(.form:text-is("-ion"))')
        page.click('#wf-go')
        first = page.inner_text('#wf-output .wf-variant.main')
        self.assertRegex(first, r'ald\w*isil\w*on')

    def test_root_card_and_index(self):
        # a root of a word opens its card here: what Eldamo says of it, the words from it
        page = self.page(self.atlas + '#w=3005081253')                 # S. galadh
        page.click('#word-card [data-root]')
        page.wait_for_function("location.hash.includes('r=')")
        card = page.inner_text('#word-card')
        self.assertIn('Слова от этого корня', card)
        self.assertIn('galadh', card)
        # √LAS¹: ᴹ√LAS¹ is merged into it
        page.goto(self.atlas + '#r=3661997445')
        page.wait_for_function("document.getElementById('word-card').textContent.includes('LAS')")
        self.assertIn('слиты', page.inner_text('#word-card'))
        self.assertIn('lassë', page.inner_text('#word-card'))
        # the index: a search, the recommended roots without derivatives
        page.goto(self.atlas + '#tab=roots')
        page.fill('#roots-q', 'LUP')
        page.click('#roots-list [data-root]:has(.form:text-is("LUP"))')
        page.wait_for_function("document.getElementById('word-card').textContent.includes('LUP')")
        self.assertIn('LUB', page.inner_text('#word-card'))
        page.fill('#roots-q', '')
        page.select_option('#roots-which', 'free')
        self.assertIn('без производных', page.inner_text('#roots-list'))

    def test_origin_tree(self):
        # S. Mithrandir: mith + randir, randir = √RAN + dîr < √N(D)ER
        page = self.page(self.atlas + '#w=2655041701')
        page.click('#word-card details.origin summary')
        tree = page.inner_text('#word-card details.origin')
        for x in ('randir', 'dîr', 'RAN', 'N(D)ER', 'MITH'):
            self.assertIn(x, tree)

    def test_shortcut_and_alt_lang(self):
        # Q. alda < √GAL² directly, and < ✶galadā < √GAL²: both ways, the direct one marked
        page = self.page(self.atlas + '#w=539805327')
        page.click('#word-card details.origin summary')
        tree = page.inner_text('#word-card details.origin')
        self.assertIn('galadā', tree)
        self.assertIn('(напрямую)', tree)

    def test_graph_page(self):
        # the graph of origins works offline (d3 embedded): S. Mithrandir with its tree down to the roots
        graph = (ROOT / 'app' / 'graph.html').as_uri()
        page = self.page(graph + '#n-2655041701')
        page.wait_for_function("document.querySelectorAll('#graph g.node').length >= 8")
        self.assertIn('Mithrandir', page.inner_text('#card'))
        self.assertIn('index.html#w=2655041701', page.inner_html('#card'))
        page.click('#mode-roots')
        page.wait_for_function("document.querySelectorAll('g.ov-leaf').length > 1000")

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

    def test_reconstruction_form_finds_the_word(self):
        # a typed form offers the lexicon's words; without a choice the one word of the source language is taken
        page = self.page(self.atlas)
        page.select_option('#rc-src', 'quenya|middle|2')
        page.fill('#rc-form', 'mauya')
        self.assertIn('mauya-', page.inner_text('#rc-r'))
        page.select_option('#rc-dst', 'quenya|middle|0')
        page.click('#rc-go')
        out = page.inner_text('#rc-output')
        self.assertIn('Взята статья Eldamo', out)
        self.assertIn('mbauja', out)
        # choosing a word from the list makes it the current word
        page.select_option('#rc-src', 'quenya|late|2')
        page.fill('#rc-form', 'Ambar')
        page.click('#rc-r button[data-word="4273482913"]')
        page.wait_for_function("location.hash.includes('w=4273482913')")

    def test_unruled_step_in_card(self):
        page = self.page(self.atlas + '#w=3934957721')                 # Q. pupso: buspō > puspō with '?'
        self.assertIn('без правила', page.inner_text('#word-card'))

    def test_panorama_cell_and_rule_in_reference(self):
        page = self.page(self.atlas + '#w=3880471189')                # Q. lelya "delicate"
        page.wait_for_selector('.pcell[data-cell="sindarin/late/3"] .sym')
        page.click('.pcell[data-cell="sindarin/late/3"]')
        main = page.inner_text('#rc-output .wf-variant.main')
        self.assertIn('dail', main)                     # S. dail: Eldamo's cognate, inside a reference
        self.assertIn('связь Eldamo', main)
        self.assertIn('dst=sindarin', page.evaluate('location.hash'))
        # rules are grouped by stage and open in the reference
        page.click('#rc-output details.stages summary >> nth=0')
        page.click('#rc-output details.stages[open] [data-rule] >> nth=0')
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

    def visible_cyrillic(self, page):
        lines = page.inner_text('body').split('\n')
        lines = [x for x in lines if re.search('[А-Яа-яЁё]', x) and x.strip() != 'Русский']
        # tooltips and labels too (the panorama cells carry the route in their title)
        lines += page.evaluate("""() => [...document.querySelectorAll('[title], [aria-label], [placeholder]')]
            .filter(el => el.id !== 'lang-toggle')
            .flatMap(el => ['title', 'aria-label', 'placeholder'].map(a => el.getAttribute(a) || ''))
            .filter(v => /[А-Яа-яЁё]/.test(v))""")
        return lines

    def test_english_interface(self):
        page = self.page(self.atlas + '#lang=en&w=3880471189&dst=sindarin/late/3', locale='en-US')
        self.assertEqual(page.evaluate('document.documentElement.lang'), 'en')
        page.wait_for_function("[...document.querySelectorAll('.pcell .pform')].every(x => x.textContent !== '…')", timeout=60000)
        page.click('#rc-go')
        self.assertIn('cognate by an Eldamo link', page.inner_text('#rc-output'))
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.wait_for_function("document.getElementById('derivations').textContent.trim() !== ''", timeout=60000)
        self.assertEqual(self.visible_cyrillic(page), [])
        page.click('#tab-compose')
        page.fill('#wf-q1', 'lindë')
        page.click('#wf-r1 [data-id] >> nth=0')
        page.fill('#wf-q2', 'lindë')
        page.click('#wf-r2 [data-id] >> nth=0')
        page.click('#wf-go')
        self.assertIn('weight', page.inner_text('#wf-output'))
        self.assertEqual(self.visible_cyrillic(page), [])

    def test_language_switch_in_place(self):
        # the language changes without a reload: the word, the panorama, a result and the reference stay
        page = self.page(self.atlas + '#w=403686503', locale='ru-RU')
        page.wait_for_function("[...document.querySelectorAll('.pcell .pform')].every(x => x.textContent !== '…')", timeout=60000)
        page.click('#rc-go')
        page.evaluate("document.querySelectorAll('details.ref').forEach(d => d.open = true)")
        page.wait_for_function("document.getElementById('derivations').textContent.trim() !== ''", timeout=60000)
        page.evaluate('window.__kept = 1')
        page.click('#lang-toggle')
        page.wait_for_function("document.documentElement.lang === 'en'")
        self.assertEqual(page.evaluate('window.__kept'), 1)
        page.wait_for_function("[...document.querySelectorAll('.pcell .pform')].every(x => x.textContent !== '…')", timeout=60000)
        self.assertIn('lindë', page.inner_text('#word-card'))
        self.assertIn('weight', page.inner_text('#rc-output'))
        self.assertEqual(self.visible_cyrillic(page), [])
        # the next visit starts in English and in the chosen theme, before the data are read
        page.click('#theme-toggle')
        theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
        page.goto(self.atlas)
        self.assertEqual(page.evaluate("[document.documentElement.lang, document.documentElement.getAttribute('data-theme')]"), ['en', theme])
        self.assertIn('word forge', page.inner_text('#intro'))

    def test_language_switch(self):
        page = self.page(self.atlas, locale='en-US')
        self.assertIn('word forge', page.inner_text('#intro'))       # an English browser gets English
        page.click('#lang-toggle')
        page.wait_for_function("document.documentElement.lang === 'ru' && document.getElementById('intro').textContent.includes('кузница')")
        self.assertIn('кузница слова', page.inner_text('#intro'))   # the choice is kept
        page.goto(self.corpus)
        self.assertIn('записей', page.inner_text('#count'))
        page.click('#lang-toggle')
        page.wait_for_function("document.documentElement.lang === 'en' && document.getElementById('count').textContent.includes('records')")
        self.assertIn('records', page.inner_text('#count'))
        self.assertEqual(self.visible_cyrillic(page), [])


if __name__ == '__main__':
    unittest.main()
