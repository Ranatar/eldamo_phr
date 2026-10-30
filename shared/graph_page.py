"""app/graph.html: the graph of origins -- words, primitive forms and roots of both branches,
linked from the origin to what comes from it.

The page is neo-roots' graph (graph_template.html, graph_messages.json: an interactive d3
page by the author of neo-roots), filled with Quettamin's data in the same form (make_graph.py):
nodes are Eldamo pages, keyed by page id; edges go from the origin to what comes from it
(root -> primitive form -> word) with the relation: deriv, element, combine, see, deprecated,
cognate (the paths from each word to its roots, shared/lexicon.py) and merged, filed,
rootderiv (the index of roots, shared/root_index.py). d3 is embedded (app/vendor/d3.min.js,
ISC licence), so the page works without a network, as the rest of Quettamin does.
"""
from __future__ import annotations

import json

from . import root_index
from .io import embed_json, write_text
from .source import ROOT, meta

APP = ROOT / 'app'
# 'instead': a deprecated word -> what Eldamo suggests instead (not a link of origin)
RELS = ['deriv', 'element', 'combine', 'see', 'deprecated', 'cognate', 'merged', 'filed', 'rootderiv', 'instead']
KINDS = ['word', 'form', 'protoform', 'root']
WARN = ['deprecated', 'deleted', 'rejected', 'doubtful', 'unglossed', 'early']
STEPS = {'e': 'element', 'd': 'deriv', 'c': 'combine', 's': 'see', 'x': 'deprecated', 'k': 'cognate'}
PRIMITIVE = ('p', 'mp', 'ep', 'np')
GROUP = {'quenya': 'nq', 'sindarin': 'ns'}
VIA_RULE = {'': 'deriv', 'element': 'element', 'source': 'intermediate', 'combine': 'combine', 'see': 'see',
            'deprecated': 'deprecated', 'cognate': 'cognate'}


def _rule(e: dict) -> str | None:
    """How the word's roots were found, in the terms of neo-roots (rule.* of the catalog)."""
    rs = e.get('roots') or []
    if not rs:
        return None
    if any(r.get('part') for r in rs):
        return 'elements'
    r = rs[0]
    if not r.get('via') and len(r.get('path') or []) > 1:
        return 'intermediate'
    return VIA_RULE.get(r.get('via', ''), 'deriv')


def build(branches: dict) -> dict:
    lexicons = {b: d['lexicon'] for b, d in branches.items()}
    roots = root_index.build(lexicons)
    nodes, edges = {}, {}
    entries = {}
    for b, lex in lexicons.items():
        for e in lex:
            if e.get('speech') == 'root' or e['id'] in entries:
                continue
            entries[e['id']] = e
            prim = e['lang'] in PRIMITIVE
            n = {'f': e['form'], 'l': e['lang'], 'k': 'protoform' if prim else 'word',
                 'grp': 'np' if prim else GROUP.get(b, 'nq')}
            if e.get('gloss'):
                n['g'] = e['gloss']
            if e.get('speech'):
                n['s'] = e['speech']
            r = _rule(e)
            if r:
                n['r'] = r
            if any(x.get('via') in ('deprecated', 'cognate') for x in e.get('roots') or []):
                n['u'] = 1
            if e.get('alt_lang'):
                n['al'] = e['alt_lang']
            # x: 'd' a deprecated word (Eldamo suggests another instead), 'm' a form of another
            # conception merged into a word (shown under it on Eldamo's page)
            links = e.get('links') or {}
            if links.get('deprecated'):
                n['x'] = 'd'
            elif links.get('combine'):
                n['x'] = 'm'
            nodes[e['id']] = n
    for rid, r in roots.items():
        n = {'f': r['f'], 'l': r['l'], 'k': 'root'}
        if r.get('g'):
            n['g'] = r['g']
        n['rec'] = 1 if r.get('listed') and not r.get('w') else 0
        if r.get('w'):
            n['wn'] = [WARN.index(x) for x in r['w']]
        if r.get('al'):
            n['al'] = r['al']
        if not r.get('listed'):
            n['nl'] = 1
        if r.get('instead'):
            n['ins'] = r['instead']
        dc = sum(len(v) for v in (r.get('words') or {}).values())
        if dc:
            n['dc'] = dc
        nodes[rid] = n

    shortcut = {}

    def edge(a, b, rel, written=None, sc=False):
        if a not in nodes or b not in nodes or a == b:
            return
        key = (a, b, rel)
        shortcut[key] = shortcut.get(key, True) and sc
        rec = edges.setdefault(key, {})
        for w in written or ():
            rec.setdefault('w', [])
            if w not in rec['w']:
                rec['w'].append(w)

    def written(parent: str, child: str) -> list:
        """How the parent's references write its derivation from the child."""
        p = entries.get(parent)
        return [[src, [v, *inter, p['form']]] for src, v, inter in (p.get('written') or {}).get(child, [])] if p else []

    for wid, e in entries.items():
        recs = [[r.get('path') or []] + (r.get('more') or []) for r in e.get('roots') or []]
        recs += [[g.get('path') or []] for g in e.get('root_gaps') or []]
        for paths in recs:
            for path in paths:
                # the root named directly beside a longer way to it from the same place
                sc = any(len(q) > len(path) and q[:len(path) - 1] == path[:-1] for q in paths)
                parent = wid
                for k, (step, nid) in enumerate(path):
                    rel = STEPS.get(step, 'deriv')
                    edge(nid, parent, rel, written(parent, nid) if rel == 'deriv' else None,
                         sc=sc and k == len(path) - 1)
                    parent = nid
    # the word's elements also when its roots come another way or it has none (neo-roots'
    # element_parts): ᴹQ. mir < ᴹ√MĪ/IMI with -r², Q. calima < √KAL with cal- and -ima, NQ. aialca =
    # ai(a)- + -lka; a root named both as an element and a derivation is drawn once
    for wid, e in entries.items():
        for x in e.get('elements') or ():
            i = x.get('id')
            if i and (i, wid, 'deriv') not in edges:
                edge(i, wid, 'element')
    for wid, e in entries.items():
        links = e.get('links') or {}
        for t in links.get('combine', ())[:1]:
            if t.get('id') in entries:
                edge(wid, t['id'], 'combine')
        ins = [t['id'] for t in links.get('deprecated', ()) if t.get('id') in nodes]
        for t in ins:
            edge(wid, t, 'instead')
        if ins and wid in nodes:
            nodes[wid]['ins'] = ins
    for rid, r in roots.items():
        for x in r.get('merged', ()):
            edge(x, rid, 'merged')
        for x in r.get('here', ()):
            edge(x, rid, 'filed')
        for x in r.get('from', ()):
            edge(x, rid, 'rootderiv')
    for key, rec in edges.items():
        if shortcut.get(key):
            rec['sc'] = 1
    # nodes that do not go back to a root along the links of origin; `ds`, how many words come
    # from such a node (make_graph.py)
    origin = {'deriv', 'element', 'combine', 'see', 'deprecated', 'cognate'}
    down = {}
    for (a, b, rel) in edges:
        if rel in origin:
            down.setdefault(a, []).append(b)
    reached = {i for i, n in nodes.items() if n['k'] == 'root'}
    todo = list(reached)
    while todo:
        for y in down.get(todo.pop(), ()):
            if y not in reached:
                reached.add(y)
                todo.append(y)
    for i, n in nodes.items():
        # a word with an entry goes back to a root exactly when its entry has roots (a cognate counts
        # for the word itself only); make_graph.py
        if n['k'] == 'root' or (bool(entries[i].get('roots')) if i in entries else i in reached):
            continue
        n['nr'] = 1
        seen, todo = {i}, [i]
        while todo:
            for y in down.get(todo.pop(), ()):
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
        ds = sum(1 for y in seen if y != i and nodes[y].get('grp') and not nodes[y].get('x'))
        if ds:
            n['ds'] = ds
    ids = list(nodes)
    index = {x: k for k, x in enumerate(ids)}
    return {
        'version': meta()['eldamo_version'],
        'rels': RELS, 'kinds': KINDS, 'warn': WARN,
        'ids': ids,
        'nodes': [nodes[x] for x in ids],
        'edges': [[index[a], index[b], RELS.index(rel)] + ([e] if e else []) for (a, b, rel), e in edges.items()],
    }


# Quettamin's changes to the page of neo-roots, applied at build time, so that a new version of
# graph_template.html and graph_messages.json is taken over by copying the two files
HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-i18n="page.title">Quettamin — граф происхождения</title>
<style>html{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}[hidden]{display:none!important}</style>
"""
ADAPT = [
    # the page offline: no web fonts (the system ones in the stacks of the page), d3 embedded
    ('<title>Neo-Roots Graph</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
     '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
     '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n', HEAD),
    ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400&family=IBM+Plex+Sans:'
     'wght@400;500;600&family=Noto+Serif:ital,wght@0,500;0,600;1,400;1,500&display=swap">\n', ''),
    ('<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>', '<script>\n/*D3*/\n</script>'),
    # the groups are the branches of Quettamin, not the lists of neo-roots
    ('<option value="nq">ᴺQ.</option>', '<option value="nq" data-i18n="group.nq">квенья</option>'),
    ('<option value="ns">ᴺS.</option>', '<option value="ns" data-i18n="group.ns">синдарин</option>'),
    ('<option value="np">ᴺ✶</option>', '<option value="np" data-i18n="group.np">праэльфийский</option>'),
    # from the card of a node back to Quettamin
    ("      ${/^\\d+$/.test(id) ? `<a class=\"ext\" href=\"${SITE}${esc(id)}.html\"",
     "      ${/^\\d+$/.test(id) && (n.k === 'root' || n.grp) ? `<a class=\"ext\" href=\"index.html#${n.k === 'root' ? 'r' : 'w'}=${esc(id)}\">${esc(t('card.quettamin'))}</a>` : ''}\n"
     "      ${/^\\d+$/.test(id) ? `<a class=\"ext\" href=\"${SITE}${esc(id)}.html\""),
    # the language and the theme chosen here and in the atlas are one choice
    ("const LANG_KEY = 'neo-roots-lang';", "const LANG_KEY = 'quettamin-lang';"),
    ("const THEME_KEY = 'neo-roots-theme';", "const THEME_KEY = 'quettamin-theme';"),
]
MESSAGES = {
    'page.title': ('Quettamin — граф происхождения', 'Quettamin — the graph of origins'),
    'page.h1': ('Quettamin: граф происхождения', 'Quettamin: the graph of origins'),
    'page.stat': ('Eldamo {v} · слов: {words} (и заменённых: {dep}) · корней: {roots} · связей: {edges}',
                  'Eldamo {v} · words: {words} (and deprecated: {dep}) · roots: {roots} · links: {edges}'),
    'group.nq': ('квенья', 'Quenya'),
    'group.ns': ('синдарин', 'Sindarin'),
    'group.np': ('праэльфийский', 'Primitive Elvish'),
    'legend.n.nq': ('слово ветви квенья', 'word of the Quenya branch'),
    'legend.n.ns': ('слово ветви синдарина', 'word of the Sindarin branch'),
    'legend.n.proto': ('праформа', 'primitive form'),
    'tag.notListed': ('вне перечня Eldamo', "not in Eldamo's list"),
    'tag.noRootDerivatives': ('производных слов: {n}', 'words derived from it: {n}'),
    'card.quettamin': ('открыть в Quettamin', 'open in Quettamin'),
    'filter.deprecated': ('заменённые слова (Eldamo советует вместо них другие)', 'deprecated words (Eldamo suggests others instead)'),
    'speech.place-name': ('топоним', 'place name'),
    'speech.masc-name': ('мужское имя', 'masculine name'),
    'speech.proper-name': ('имя собственное', 'proper name'),
    'speech.fem-name': ('женское имя', 'feminine name'),
    'speech.collective-name': ('название народа', 'collective name'),
}


def page_html(graph: dict) -> str:
    page = (APP / 'graph_template.html').read_text(encoding='utf-8')
    for a, b in ADAPT:
        if page.count(a) != 1:
            raise SystemExit(f'app/graph_template.html: the place of a Quettamin change is not found once: {a[:60]!r}')
        page = page.replace(a, b)
    if '</head>' not in page:
        # the template is a page body: the head ends before its first element
        k = page.index('<div class="app">')
        page = page[:k] + '</head>\n<body>\n' + page[k:] + '\n</body>\n</html>\n'
    for marker in ('/*GRAPH*/', '/*MESSAGES*/', '/*D3*/'):
        if page.count(marker) != 1:
            raise SystemExit(f'app/graph_template.html must contain {marker} exactly once')
    catalog = json.loads((APP / 'graph_messages.json').read_text(encoding='utf-8'))
    for k, (ru, en) in MESSAGES.items():
        catalog[k] = {'ru': ru, 'en': en}
    d3 = (APP / 'vendor' / 'd3.min.js').read_text(encoding='utf-8').strip().replace('</script', '<\\/script')
    page = page.replace('/*MESSAGES*/', embed_json(catalog), 1)
    page = page.replace('/*D3*/', d3, 1)
    return page.replace('/*GRAPH*/', embed_json(graph), 1)


def write_graph(branches: dict) -> None:
    write_text(APP / 'graph.html', page_html(build(branches)))
