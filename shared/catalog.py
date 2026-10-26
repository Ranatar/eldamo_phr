"""Human-readable catalog of one branch: rules by language and Eldamo order, chains."""
from __future__ import annotations

from .graph import GRADES
from .io import write_text
from .languages import ERA_NAMES
from .source import ROOT, word_url


def _md(s) -> str:
    return str(s if s is not None else '').replace('|', '\\|').replace('\n', ' ')


def render(branch: str, data: dict) -> str:
    m, s = data['meta'], data['summary']
    pairs = {p['id']: p for p in data['pairs']}
    rules_by_lang = {}
    for r in data['rules']:
        rules_by_lang.setdefault(r['lang'], []).append(r)
    rule_name = {r['id']: r['name'] for r in data['rules']}
    lines = [
        f"# Фонетические правила: {m['title']}",
        '',
        f"Источник: Eldamo {s['eldamo_version']} © Paul Strack, CC BY 4.0. Файл создан `scripts/build.py`; не править вручную.",
        '',
        f"Правил: {s['rules']} (с порядком Eldamo: {s['rules_with_order']}); подформул: {s['pairs']}; "
        f"засвидетельствованных дериваций: {s['derivations'] - s['deleted_derivations']}; "
        f"формулы воспроизводят {s['reproduction_rate'] * 100:.1f}% шагов с известной формулой.",
        '',
        'Столбец «примеры» — число засвидетельствованных шагов дериваций с этой подформулой / сколько из них формула воспроизводит.',
        '',
    ]
    for lang in m['languages']:
        rules = sorted(rules_by_lang.get(lang['code'], []), key=lambda r: (r['order'] is None, r['order'] or 0, r['name']))
        if not rules:
            continue
        lines += [f"## {lang['marker']} {lang['name']} ({ERA_NAMES[lang['era']]} концепция)", '']
        for r in rules:
            head = f"### [{r['name']}]({r['url']})"
            lines += [head, '']
            facts = []
            if r['order'] is not None:
                facts.append(f"порядок {r['order']:05d}")
            if r['formula']:
                facts.append(f"общая формула `{r['formula']['from']} > {r['formula']['to']}`")
            if r['before']:
                facts.append('раньше, чем: ' + '; '.join(_md(b['name']) for b in r['before']))
            if r['after']:
                facts.append('позже, чем: ' + '; '.join(_md(rule_name.get(a, a)) for a in r['after']))
            if r['variant_of']:
                facts.append(f"вариант правила [{_md(rule_name.get(r['variant_of'], r['variant_of']))}]({word_url(r['variant_of'])})")
            if facts:
                lines += ['- ' + f for f in facts] + ['']
            if r['pairs']:
                lines += ['| подформула | вид | примеры |', '|---|---|---|']
                for pid in r['pairs']:
                    p = pairs[pid]
                    ex = f"{p['examples']} / {p['reproduced'] + p['partial']}" if p['examples'] else '—'
                    lines.append(f"| `{_md(p['from'])} > {_md(p['to'])}` | {p['kind']} | {ex} |")
                lines.append('')
    lines += ['## Цепочки с оценками A и B', '']
    for g in ('A', 'B'):
        lines += [f"### {g} — {GRADES[g]}", '']
        for c in data['chains']:
            if c['grade'] == g:
                extra = f" — {c['attested_count']} дерив." if c['attested_count'] else ''
                lines.append(f"- {ERA_NAMES[c['era']][:5]}. `{' → '.join(c['states'])}` ({', '.join(c['markers'])}){extra}")
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def write_catalog(branch: str, data: dict) -> None:
    write_text(ROOT / 'branches' / branch / 'catalog.md', render(branch, data))
