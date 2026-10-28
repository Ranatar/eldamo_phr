"""The index of roots: every root page of Eldamo's primitive languages with what Eldamo says
about it and the words of both branches that come from it.

Following neo-roots (neo_roots.py, build_root_index), as Eldamo's root index
(root-indexes/roots-np.html, root-index.xq) shows its roots:

* merged      -- roots of other conceptions merged into this one by <combine> (√LAS¹ holds
                 ᴹ√LAS¹ and ᴱ√LASA), and `into`, the roots this one is merged into;
* filed       -- the root it is filed under (a nested page: p LUB³ under N√LUP, ᴹ√KHOTH
                 under √KHOT¹) and the roots filed under it;
* canon       -- the end of both: the one root all these pages stand for (ᴹ√LUB² ≡ √LUB³ ≡
                 N√LUP); roots of other conceptions are compared by it (reconstruct.py);
* derives     -- roots it derives from (its <deriv>: ᴹ√GALAD < √GAL²) and those derived from it;
* warnings    -- as Eldamo marks a root ⚠️: deprecated (itself or the page its <see> names;
                 `instead`, the replacement), deleted (|), rejected (-), doubtful (‽),
                 unglossed, early (ᴱ√); a root without warnings is recommended;
* words       -- per branch, the words whose roots (shared/lexicon.py) are this root or a
                 root merged into or filed under it.

Recommended roots of the Neo-Primitive list (np, p, mp, ep without <combine>) that no word
comes from are the material for new words.
"""
from __future__ import annotations

PRIMITIVE = ('p', 'mp', 'ep', 'np')


def _ids(e: dict, tag: str) -> list:
    return [x['id'] for x in (e.get('links') or {}).get(tag, ()) if x.get('id')]


def roots_of(lexicons: dict) -> dict:
    """id -> root entry, from the lexicons of the branches (the same pages in both)."""
    out = {}
    for lex in lexicons.values():
        for e in lex:
            if e.get('speech') == 'root' and e['lang'] in PRIMITIVE:
                out.setdefault(e['id'], e)
    return out


def canonical(roots: dict) -> dict:
    """id -> the root a root stands for: its <combine> links followed to the end, then the
    root page it is filed under (nested pages), followed to the top."""
    out = {}
    for rid in roots:
        cur, seen = rid, {rid}
        while True:
            nxt = next((i for i in _ids(roots[cur], 'combine') if i in roots), None)
            if nxt is None or nxt in seen:
                break
            seen.add(nxt)
            cur = nxt
        while roots[cur].get('under') in roots and roots[cur]['under'] not in seen:
            cur = roots[cur]['under']
            seen.add(cur)
        out[rid] = cur
    return out


def warnings(e: dict, roots: dict) -> list:
    out = []
    dep = _ids(e, 'deprecated') + [i for s in _ids(e, 'see') if s in roots for i in _ids(roots[s], 'deprecated')]
    if dep:
        out.append('deprecated')
    m = e.get('mark') or ''
    if '|' in m:
        out.append('deleted')
    if '-' in m:
        out.append('rejected')
    if '‽' in m:
        out.append('doubtful')
    if not e.get('gloss') or e.get('gloss') == '[unglossed]':
        out.append('unglossed')
    if e['lang'] == 'ep':
        out.append('early')
    return out


def build(lexicons: dict) -> dict:
    """{id: record} for the page (app/word_ui.js); keys are short, the page holds every root."""
    roots = roots_of(lexicons)
    canon = canonical(roots)
    into = {}
    for rid, e in roots.items():
        chain, cur, seen = [], rid, {rid}
        while True:
            nxt = next((i for i in _ids(roots[cur], 'combine') if i in roots), None)
            if nxt is None or nxt in seen:
                break
            chain.append(nxt)
            seen.add(nxt)
            cur = nxt
        into[rid] = chain
    merged, filed_here, derived = {}, {}, {}
    for rid, chain in into.items():
        for t in chain:
            merged.setdefault(t, []).append(rid)
    for rid, e in roots.items():
        if e.get('under') in roots:
            filed_here.setdefault(e['under'], []).append(rid)
    # the roots a root derives from: those its own derivations name (lexicon.py: ᴹ√GALAD < √GAL²)
    parents = {rid: list(dict.fromkeys(r['id'] for r in e.get('roots', ()) if not r.get('via') and r['id'] in roots and r['id'] != rid))
               for rid, e in roots.items()}
    for rid, ps in parents.items():
        for p in ps:
            derived.setdefault(p, []).append(rid)
    # the words of each root, credited also to the roots it is merged into or filed under
    words = {}
    for b, lex in lexicons.items():
        for e in lex:
            if e.get('speech') == 'root':
                continue
            seen = set()
            for r in e.get('roots', ()):
                rid = r['id']
                if rid not in roots:
                    continue
                targets = [rid] + into.get(rid, [])
                if canon.get(rid) not in targets:
                    targets.append(canon[rid])
                for t in targets:
                    if t not in seen:
                        seen.add(t)
                        words.setdefault(t, {}).setdefault(b, []).append(e['id'])
    out = {}
    for rid, e in sorted(roots.items(), key=lambda kv: (kv[1]['form'], kv[1]['lang'], kv[0])):
        rec = {'f': e['form'], 'l': e['lang'], 'g': e.get('gloss') or ''}
        if e.get('alt_lang'):
            rec['al'] = e['alt_lang']          # Eldamo's index prints it in brackets: N√ [√] LUP
        if e.get('mark'):
            rec['m'] = e['mark']
        w = warnings(e, roots)
        if w:
            rec['w'] = w
        inst = [i for i in _ids(e, 'deprecated') if i in roots]
        if inst:
            rec['instead'] = inst
        see = [i for i in _ids(e, 'see') if i in roots]
        if see:
            rec['see'] = see
        if into[rid]:
            rec['into'] = into[rid]
        if merged.get(rid):
            rec['merged'] = merged[rid]
        if e.get('under') in roots:
            rec['under'] = e['under']
        if filed_here.get(rid):
            rec['here'] = filed_here[rid]
        if canon[rid] != rid:
            rec['canon'] = canon[rid]
        if parents[rid]:
            rec['from'] = parents[rid]
        if derived.get(rid):
            rec['to'] = derived[rid]
        if words.get(rid):
            rec['words'] = words[rid]
        # Eldamo's own list: roots without <combine>
        if not _ids(e, 'combine'):
            rec['listed'] = 1
        out[rid] = rec
    return out
