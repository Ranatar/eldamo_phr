"""Quettamin from the command line: look up a word, reconstruct its form for
another period, show the panorama of all periods, join words and affixes.

Reads the data written by scripts/build.py (branches/<branch>/data/), so a
command takes seconds. Periods are written branch/conception/stage:
quenya/late/2 (Q.), sindarin/late/3 (S.), quenya/middle/2 (ᴹQ.), sindarin/early/1 (G.)...

    python scripts/quettamin.py word lindë
    python scripts/quettamin.py reconstruct erinqua --to sindarin/late/3
    python scripts/quettamin.py reconstruct ereb --from sindarin/late/3 --to quenya/late/2 --form
    python scripts/quettamin.py panorama galadh
    python scripts/quettamin.py compose Ambar lindë
    python scripts/quettamin.py compose cen- -ima --stage 0
    python scripts/quettamin.py affix -ima
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared import affixes, compound, junctions  # noqa: E402
from shared.interpreter import comparable  # noqa: E402
from shared.languages import BRANCHES, ERA_NAMES, ERAS  # noqa: E402
from shared.pipeline import load_all  # noqa: E402
from shared.reconstruct import Context, reconstruct  # noqa: E402

MARKS = {
    'attested': 'засвидетельствовано', 'link': 'связь Eldamo', 'near-cognate': 'слово Eldamo с близкой праформой',
    'unchanged': 'без изменений', 'reconstructed': 'восстановлено', 'root': 'согласуется с корнем',
    'cognate': 'через праформу', 'primitive-attested': 'праформа Eldamo', 'neologism': 'неологизм',
    'phonotactics': 'нетипично для языка', 'main': 'основное чтение',
}


AFFIX = '\u2063'          # invisible mark for words that begin with a hyphen (see main)


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass


class Data:
    def __init__(self):
        self.branches = load_all()
        self.ctx = Context(self.branches)

    def langs(self, branch: str) -> dict:
        return self.ctx.langs(branch)

    def period(self, text: str) -> tuple:
        try:
            b, era, stage = text.split('/')
            stage = int(stage)
        except ValueError:
            raise SystemExit(f'период пишется ветвь/концепция/стадия, например quenya/late/2: {text}')
        if b not in BRANCHES or era not in ERAS or self.ctx.code(b, era, stage) is None:
            raise SystemExit(f'нет такого периода: {text}')
        return b, era, stage

    def period_name(self, p: tuple) -> str:
        b, era, stage = p
        lang = next(l for l in self.langs(b).values() if l['era'] == era and l['stage'] == stage)
        return f"{lang['marker']} {lang['name']} ({ERA_NAMES[era]})"

    def own_period(self, branch: str, entry: dict):
        lang = self.langs(branch).get(entry['lang'])
        return (branch, lang['era'], lang['stage']) if lang else None

    def find(self, query: str, branch: str | None = None, sub: bool = False) -> list:
        """[(branch, entry)] by Eldamo id or by form (exact, ignoring accents and homonym numbers)."""
        out, seen = [], set()
        key = comparable(query.strip()).strip('-')
        for b in ([branch] if branch else BRANCHES):
            for e in self.branches[b]['lexicon']:
                if e['id'] in seen:
                    continue
                form = comparable(e['form'].rstrip('¹²³⁴⁵⁶⁷⁸⁹')).strip('-')
                if e['id'] == query or form == key or (sub and key in form):
                    out.append((b, e))
                    seen.add(e['id'])
        # the latest languages first, then neologisms
        order = {'q': 0, 's': 0, 'mq': 1, 'n': 1, 'eq': 2, 'g': 2}
        exact = query.strip()
        out.sort(key=lambda be: (be[1]['form'].rstrip('¹²³⁴⁵⁶⁷⁸⁹') != exact, be[1].get('neo', False),
                                 order.get(be[1]['lang'], 3)))
        return out

    def marker(self, branch: str, code: str) -> str:
        lang = self.langs(branch).get(code)
        return lang['marker'] if lang else code


def describe(data: Data, b: str, e: dict) -> str:
    bits = [f"{data.marker(b, e['lang'])} {e['form']} «{e.get('gloss', '')}»", f"id {e['id']}"]
    if e.get('neo'):
        bits.append('неологизм')
    if e.get('starts'):
        bits.append('праформа ' + ', '.join(e['starts']))
    if e.get('roots'):
        bits.append('корень ' + ', '.join(r['form'] for r in e['roots']))
    if e.get('elements'):
        bits.append('состав ' + ' + '.join(x['form'] for x in e['elements']))
    return ' · '.join(bits)


def pick(data: Data, query: str, branch: str | None = None):
    found = data.find(query, branch)
    if not found:
        raise SystemExit(f'в лексиконе нет «{query}»; попробуйте word {query} --sub')
    if len(found) > 1:
        print('найдено несколько статей, взята первая (другую можно указать по id):')
        for b, e in found[:8]:
            print('   ', describe(data, b, e))
    return found[0]


def show_variants(variants: list, limit: int) -> None:
    if not variants:
        print('  форм не найдено')
    for v in variants[:limit]:
        marks = ', '.join(MARKS[m] for m in v['marks'] if m in MARKS)
        print(f"  {v['form']:<18} {v['score']:<6} {v['route']}" + (f'  [{marks}]' if marks else '')
              + (f"  ({', '.join(v['problems'])})" if v.get('problems') else ''))


def cmd_word(data: Data, args) -> None:
    found = data.find(args.form, args.branch, args.sub)
    for b, e in found[:args.n]:
        print(describe(data, b, e))
    print(f'статей: {len(found)}')


def cmd_reconstruct(data: Data, args) -> None:
    dst = data.period(args.to)
    if args.form:
        src = data.period(args.src or f'{dst[0]}/late/{data.ctx.last_stage(dst[0], "late")}')
        print(f'форма {args.query}: {data.period_name(src)} → {data.period_name(dst)}')
        show_variants(reconstruct(data.ctx, src, dst, form=args.query, spelled=not args.phonetic), args.n)
        return
    b, e = pick(data, args.query)
    src = data.period(args.src) if args.src else data.own_period(b, e)
    if src is None:
        raise SystemExit('у слова нет периода (неологизм): укажите --from и --form')
    print(describe(data, b, e))
    print(f'{data.period_name(src)} → {data.period_name(dst)}')
    show_variants(reconstruct(data.ctx, src, dst, word=e['id']), args.n)


def cmd_panorama(data: Data, args) -> None:
    b, e = pick(data, args.query)
    src = data.own_period(b, e)
    if src is None:
        raise SystemExit('у слова нет периода (неологизм)')
    print(describe(data, b, e))
    for era in ERAS:
        for branch in BRANCHES:
            langs = sorted((l for l in data.langs(branch).values() if l['era'] == era), key=lambda l: l['stage'])
            cells = []
            for l in langs:
                vs = reconstruct(data.ctx, src, (branch, era, l['stage']), word=e['id'], limit=1)
                if not vs:
                    cells.append(f"{l['marker']} —")
                    continue
                sign = '●' if 'attested' in vs[0]['marks'] else '↔' if 'link' in vs[0]['marks'] else \
                    '≈' if 'near-cognate' in vs[0]['marks'] else '◇' if 'neologism' in vs[0]['marks'] else '○'
                cells.append(f"{l['marker']} {vs[0]['form']} {sign}")
            print(f'{ERA_NAMES[era]:>8} {branch:<9} ' + ' · '.join(cells))
    print('● засвидетельствовано · ↔ связь Eldamo · ≈ слово Eldamo с близкой праформой · ○ восстановлено · ◇ неологизм')


def cmd_compose(data: Data, args) -> None:
    branch = args.branch
    d = data.branches[branch]
    seq = data.ctx.seq[branch]
    lexicon = data.ctx.lexicon[branch]
    a = pick(data, args.first, branch)[1]
    b = pick(data, args.second, branch)[1]
    era = args.era
    last = data.ctx.last_stage(branch, era)
    stage = last if args.stage is None else args.stage
    table = junctions.learn(d['junctions']['cases'])
    model = affixes.learn(d['affixes']['cases'])
    print(f"{describe(data, branch, a)}\n{describe(data, branch, b)}\nстадия: {data.period_name((branch, era, stage))}")
    variants = compound.predict(lexicon, seq, [a['id'], b['id']], era, stage, table=table, affix_model=model)
    if not variants:
        print('  форм не найдено')
    for v in variants[:args.n]:
        extra = []
        if v.get('junction') and list(v['junction']) != [0, 0, '']:
            extra.append(f"стык {v['junction']}")
        if v.get('adjustments'):
            extra.append('поправки ' + ', '.join(str(x.get('rule', x)) if isinstance(x, dict) else str(x) for x in v['adjustments']))
        score = v.get('score', '')
        print(f"  {v['form']:<20} {score!s:<6} из {' + '.join(v.get('elements') or [])}" + (f"  ({'; '.join(extra)})" if extra else ''))


def cmd_affix(data: Data, args) -> None:
    key = comparable(args.affix.rstrip('¹²³⁴⁵⁶⁷⁸⁹'))
    rows = [c for c in data.branches[args.branch]['affixes']['cases']
            if comparable(c.get('affix_form', '').rstrip('¹²³⁴⁵⁶⁷⁸⁹')) == key]
    for c in rows:
        print(f"  {c['form']:<18} = {c['base_form']} + {c['affix_form']}   [{c['a']} + {c['b']} → {c['c']}]")
    print(f'производных: {len(rows)}')


def main(argv=None) -> None:
    utf8_console()
    ap = argparse.ArgumentParser(prog='quettamin', description='Quettamin: слова квенья и синдарина по данным Eldamo.')
    sub = ap.add_subparsers(dest='command', required=True)
    w = sub.add_parser('word', help='найти слово в лексиконе')
    w.add_argument('form', help='форма или id статьи Eldamo')
    w.add_argument('--branch', choices=list(BRANCHES))
    w.add_argument('--sub', action='store_true', help='искать подстроку')
    w.add_argument('--n', type=int, default=30)
    r = sub.add_parser('reconstruct', help='форма слова для другого периода')
    r.add_argument('query', help='слово (форма или id) либо форма с --form')
    r.add_argument('--to', required=True, help='целевой период, например sindarin/late/3')
    r.add_argument('--from', dest='src', help='исходный период (по умолчанию — язык слова)')
    r.add_argument('--form', action='store_true', help='не искать статью: реконструировать саму форму')
    r.add_argument('--phonetic', action='store_true', help='форма в фонетической записи Eldamo, а не в написании Толкина')
    r.add_argument('--n', type=int, default=8)
    p = sub.add_parser('panorama', help='формы слова во всех периодах')
    p.add_argument('query')
    c = sub.add_parser('compose', help='сложение или производное слово')
    c.add_argument('first')
    c.add_argument('second')
    c.add_argument('--branch', choices=list(BRANCHES), default='quenya')
    c.add_argument('--era', choices=list(ERAS), default='late')
    c.add_argument('--stage', type=int, help='стадия образования (по умолчанию — сам язык)')
    c.add_argument('--n', type=int, default=8)
    a = sub.add_parser('affix', help='засвидетельствованные производные с аффиксом')
    a.add_argument('affix')
    a.add_argument('--branch', choices=list(BRANCHES), default='quenya')
    # an affix (-ima) or a stem (cen-) is a word here, not an option
    argv = [AFFIX + a if a.startswith('-') and not a.startswith('--') and a != '-h' else a
            for a in (sys.argv[1:] if argv is None else argv)]
    args = ap.parse_args(argv)
    for k, v in vars(args).items():
        if isinstance(v, str) and v.startswith(AFFIX):
            setattr(args, k, v[len(AFFIX):])
    data = Data()
    {'word': cmd_word, 'reconstruct': cmd_reconstruct, 'panorama': cmd_panorama,
     'compose': cmd_compose, 'affix': cmd_affix}[args.command](data, args)


if __name__ == '__main__':
    main()
