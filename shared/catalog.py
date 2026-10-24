"""Rebuild complete Markdown catalog for both branches from reconciled rules.
No HTML anchors. No silent omission of contextual rules.
"""
import json,unicodedata,re,collections
from pathlib import Path
from .audit import BASE
ORDER=['p','b','pʰ','t','d','tʰ','tʲ','dʲ','k','g','kʰ','kʷ','gʷ','ɸ','β','f','v','θ','ð','s','z','x','ɣ','h','m','m̥','n','n̥','nʲ','ŋ','ŋʷ','l','l̥','r','r̥','w','w̥','j','j̊','y','ȳ','œ','ae','oe','iw','i','ī','e','ē','ę̄','ǣ','ø','a','ā','o','ō','ǭ','u','ū','ai','ei','oi','ui','au','eu','iu','ou']
VOWELS={'a','e','i','o','u','ā','ē','ī','ō','ū','ǣ','ǭ','ę̄','ø','y','ȳ','œ'}
DIPHTHONGS={'ai','ei','oi','ui','au','eu','iu','ou','ae','oe','iw'}
RANK={'quenya':{'Q.':0,'AQ.':1,'✶':2,'ᴹQ.':3,'ᴹAQ.':4,'ᴹ✶':5},'sindarin':{'S.':0,'OS.':1,'AT.':2,'✶':3,'N.':4,'ON.':5,'ᴹ✶':6}}
def slug(s):
 s=unicodedata.normalize('NFKC',s).lower()
 return ''.join(c for c in s if c.isalnum() or unicodedata.category(c).startswith('M') or c in ('-','_'))
def esc(s):return str(s or '').replace('|','\\|').replace('\n',' ')
def create(branch):
 target=BASE/'branches'/branch/'catalog';target.mkdir(exist_ok=True)
 rows=json.loads((BASE/'branches'/branch/'data/complete_rules.json').read_text())
 symbols=sorted(set(json.loads((BASE/'branches'/branch/'data/unified_phonemes.json').read_text())) | {s for r in rows for s in r.get('sounds',[]) if s},key=lambda s:(ORDER.index(s) if s in ORDER else 999,s))
 assert len(symbols)==61, (branch,len(symbols))
 by=collections.defaultdict(list)
 for i,r in enumerate(rows):
  for sym in r['sounds']:by[sym].append((i,r))
 md=[f'# Атлас фонетических правил — {branch.title()}','', 'Eldamo 0.8.13. Включены все записи единого корпуса, включая контекстные правила и сохранённые развернутые варианты.','',
 '## Навигация по IPA','','### Согласные','','| Тип | Губные | Переднеязычные | Велярные и др. | Сонорные |','|---|---|---|---|---|']
 def labels(group):return ' · '.join(f'[[{p}]](#{slug(p)})' for p in group if p in symbols) or '—'
 md += ['| Смычные | '+labels(['p','b','pʰ'])+' | '+labels(['t','d','tʰ','tʲ','dʲ'])+' | '+labels(['k','g','kʰ','kʷ','gʷ'])+' | — |',
 '| Фрикативные | '+labels(['ɸ','β','f','v'])+' | '+labels(['θ','ð','s','z'])+' | '+labels(['x','ɣ','h'])+' | — |',
 '| Носовые | '+labels(['m','m̥'])+' | '+labels(['n','n̥','nʲ'])+' | '+labels(['ŋ','ŋʷ'])+' | — |',
 '| Аппроксиманты / плавные | '+labels(['w','w̥'])+' | '+labels(['l','l̥','r','r̥'])+' | — | '+labels(['j','j̊'])+' |','',
 '### Гласные','','| Передние | Центральные | Задние |','|---|---|---|',
 '| '+labels(['i','ī','e','ē','ę̄','ǣ','y','ȳ','œ'])+' | '+labels(['a','ā','ø'])+' | '+labels(['o','ō','ǭ','u','ū'])+' |', '',
 '### Дифтонги','','| Фонемы |','|---|','| '+labels(['ai','ei','oi','ui','au','eu','iu','ou','ae','oe','iw'])+' |','']
 other=[p for p in symbols if p not in set(ORDER)]
 if other:md+=['### Прочие обозначения','',' · '.join(f'[[{p}]](#{slug(p)})' for p in other),'']
 md += ['## Покрытие','','| Показатель | Значение |','|---|---:|',f'| Отдельных обозначений | {len(symbols)} |',f'| Записей правил | {len(rows)} |',f'| Звуковых привязок правил | {sum(len(r["sounds"]) for r in rows)} |','']
 for sym in symbols:
  md += [f'## [{sym}]','','| Маркер | Правило Eldamo | Точная формула | Каталоги | Все звуки записи | Источники | Происхождение |','|---|---|---|---|---|---|---|']
  group=sorted(by[sym],key=lambda v:(RANK[branch].get(v[1]['marker'],99),v[1]['rule'],v[1]['formula']))
  if not group:md.append('| — | Нет записей для данного обозначения | — | — | — | — | — |')
  for i,r in group:
   title=esc(r['rule']);url=r.get('url','');link=f'[{title}]({url})' if url else title
   references=', '.join(map(esc,r.get('refs',[]))) or '—'
   soundlinks=', '.join(f'[[{p}]](#{slug(p)})' for p in r['sounds'])
   md.append('| '+' | '.join([esc(r['marker']),link,f'`{esc(r["formula"])}`',', '.join(map(esc,r['catalogs'])),soundlinks,references,esc(r['provenance'])])+' |')
  md.append('')
 out=target/'complete_phonetic_catalog.md';out.write_text('\n'.join(md)+'\n')
 assert sum(line.startswith('| ') and '`' in line for line in md)==sum(len(by[s]) for s in symbols)
 return {'branch':branch,'file':str(out),'records':len(rows),'sound_links':sum(len(by[s]) for s in symbols)}
if __name__=='__main__':
 for branch in ['quenya','sindarin']:print(create(branch))
