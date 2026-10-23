import re,collections,unicodedata,pathlib
source=pathlib.Path('/mnt/data/build_eldamo_corrected.py').read_text().split("sounds={x:ix_sounds(x)")[0]
exec(source)
langs=['q','mq','aq','maq','p','mp']
langnames={'q':'Quenya','mq':'Middle Quenya','aq':'Ancient Quenya','maq':'Middle Ancient Quenya','p':'Primitive Elvish','mp':'Middle Primitive Elvish'}
sounds={l:ix_sounds(l) for l in langs}
rows=[];fails=[]
for lang,ss in sounds.items():
 for ph,p,typ in ss:
  try:
   for r in parse_page(lang,ph,p):
    if r['mark'].startswith('ᴱ'):continue
    rows.append(r)
  except Exception as e:fails.append((lang,ph,str(e)))
# order following IPA articulation via classifications
phonemes=list(dict.fromkeys(ph for lang in langs for ph,p,t in sounds[lang]))
consonants=['p','b','pʰ','t','d','tʰ','tʲ','dʲ','k','g','kʰ','kʷ','gʷ','ɸ','β','f','v','θ','ð','s','z','x','ɣ','h','m','m̥','n','n̥','nʲ','ŋ','ŋʷ','l','l̥','r','r̥','w','w̥','j','j̊']
vowels=['i','ī','e','ē','ę̄','ǣ','ø','a','ā','o','ō','ǭ','u','ū']
diph=['ai','ei','oi','ui','au','eu','iu','ou']
remaining=[p.strip('[]') for p in phonemes if p.strip('[]') not in consonants+vowels+diph]
assert not remaining,remaining
order={f'[{p}]':i for i,p in enumerate(consonants+vowels+diph)}
phonemes.sort(key=lambda p:order[p])
bykey={};allruleph=collections.defaultdict(set)
for r in rows:
 key=(r['rulelink'],r['rule'],r['result'],r['origin'],r['op'],r['mark'])
 if key not in bykey:bykey[key]={**r,'phs':set(),'langs':set(),'pages':set(),'refs':[]}
 x=bykey[key];x['phs'].add(r['ph']);x['langs'].add(r['lang']);x['pages'].add(r['page']);
 for ref in r['refs']:
  if ref not in x['refs']:x['refs'].append(ref)
 if r['rulelink']:allruleph[r['rulelink']].add(r['ph'])
rank={'Q.':0,'ᴹQ.':1,'AQ.':2,'ᴹAQ.':3,'✶':4,'ᴹ✶':5}
main=collections.defaultdict(list);cross=collections.defaultdict(list)
for r in bykey.values():
 ps=sorted(r['phs'],key=lambda p:order[p]);home=ps[0];main[home].append(r)
 for p in ps[1:]:cross[p].append((home,r))
def slug(s):return ''.join(c for c in s.lower() if c.isalnum() or c=='-' or unicodedata.category(c).startswith('M'))
assert len(set(slug(p) for p in phonemes))==len(phonemes)
def pl(p):return f'[{p}](#{slug(p)})'
def esc(s):return str(s).replace('|','\\|').replace('\n',' ')
def link(label,url):return f'[{esc(label).replace("[","\\[").replace("]","\\]")}]({url})' if url else esc(label)
def cs(*args):return ' · '.join(pl('['+v+']') for v in args if '['+v+']' in order) or '—'
nav=['## Навигация по IPA','','### Согласные','','| Способ образования | Губные | Зубные / альвеолярные | Палатальные / палатализованные | Велярные | Лабиовелярные | Гортанные |','|---|---|---|---|---|---|---|']
nav+=['| Смычные | '+ ' | '.join([cs('p','b','pʰ'),cs('t','d','tʰ'),cs('tʲ','dʲ'),cs('k','g','kʰ'),cs('kʷ','gʷ'),'—'])+' |',
'| Фрикативные | '+' | '.join([cs('ɸ','β','f','v'),cs('s','z','θ','ð'),'—',cs('x','ɣ'),'—',cs('h')])+' |',
'| Носовые | '+' | '.join([cs('m','m̥'),cs('n','n̥'),cs('nʲ'),cs('ŋ'),cs('ŋʷ'),'—'])+' |',
'| Боковые | '+' | '.join(['—',cs('l','l̥'),'—','—','—','—'])+' |',
'| Дрожащие | '+' | '.join(['—',cs('r','r̥'),'—','—','—','—'])+' |',
'| Аппроксиманты | '+' | '.join([cs('w','w̥'),'—',cs('j','j̊'),'—','—','—'])+' |',
'', '### Гласные','','| Подъём | Передние | Центральные | Задние |','|---|---|---|---|',
'| Верхние | '+cs('i','ī')+' | — | '+cs('u','ū')+' |',
'| Средние | '+cs('e','ē','ę̄','ǣ','ø')+' | — | '+cs('o','ō','ǭ')+' |',
'| Нижние | — | '+cs('a','ā')+' | — |','', '### Дифтонги','','| С окончанием на i | С окончанием на u |','|---|---|',f'| {cs("ai","ei","oi","ui")} | {cs("au","eu","iu","ou")} |','', '> Классификация служит навигацией по историческим звукам Eldamo, не утверждая, что все они одновременно существовали в одной синхронной системе.','','']
used=set(re.findall(r'\[\[([^\]]+)\]\]\(#[^)]*\)', '\n'.join(nav)))
assert used==set(p.strip('[]') for p in phonemes), (used,set(p.strip('[]') for p in phonemes)-used)
md=['# Исторические фонетические изменения эльфийских языков по Eldamo 0.8.13','','Quenya · Middle Quenya · Ancient Quenya · Middle Ancient Quenya · Primitive Elvish · Middle Primitive Elvish','','## Методика','','- Основа — **все отдельные звуковые карточки** из разделов Phonemes шести языковых каталогов в локальном архиве Eldamo 0.8.13.','- **Исключены записи с ранними маркерами `ᴱQ.`, `ᴱAQ.`, `ᴱ✶`**. У остальных исторические метки сохранены без переименования.','- Первичная группировка — фонема, затем единая таблица с сортировкой маркеров **Q. → ᴹQ. → AQ. → ᴹAQ. → ✶ → ᴹ✶**.','- Идентичные сочетания **ссылка на правило + название + точная формула + маркер** сведены к одной основной записи. Все языковые карточки и источники объединены.','- При повторении одной и той же записи у нескольких звуков дано основное вхождение и перекрёстная ссылка; связанные фонемы указаны по всем карточкам **данного правила**, а «карточки записи» — по совпадающей формуле и маркеру.','- Наличие одного преобразования в разных периодах не приравнивается к тождеству исторических процессов.','- Направление стрелки сохраняет направление символов в Eldamo: `результат ← исходная форма` или `результат → исходная форма`.','','## Контроль полноты','','| Языковой каталог | Звуковых карточек | Отобранных вхождений |','|---|---:|---:|']
for l in langs:md.append(f'| [{langnames[l]}](https://eldamo.org/content/phonetic-indexes/phonetics-{l}.html) | {len(sounds[l])} | {sum(r["lang"]==l for r in rows)} |')
md+=['',f'- Различных фонемных обозначений: **{len(phonemes)}**.',f'- Вхождений после исключения ранних меток: **{len(rows)}**.',f'- Основных уникальных записей: **{len(bykey)}**.',f'- Повторных вхождений: **{len(rows)-len(bykey)}**.',f'- Ошибок чтения: **{len(fails)}**.','']+nav
for ph in phonemes:
 md+=['## '+ph,'']
 applicable=[(l,p) for l in langs for label,p,kind in sounds[l] if label==ph]
 md+=['**Языковые карточки:** '+ ' · '.join(f'[{langnames[l]}]({url_for(p)})' for l,p in applicable),'']
 es=sorted(main[ph],key=lambda r:(rank.get(r['mark'],99),r['rule'].lower(),r['result'],r['origin']))
 if es:
  md+=['| Маркер | Правило Eldamo | Изменение | Языковые каталоги | Связанные фонемы правила | Карточки записи | Источники |','|---|---|---|---|---|---|---|']
  for r in es:
   exp=f"{r['result']} {'←' if r['op'] in ('<','←') else '→'} {r['origin']}"
   phon=sorted(allruleph.get(r['rulelink'],set()) or r['phs'],key=lambda p:order[p]);cards=sorted(r['phs'],key=lambda p:order[p])
   refs=', '.join(link(n,u) for n,u in r['refs']) or '—'
   md.append('| '+' | '.join([esc(r['mark']),link(r['rule'],r['rulelink']),f'`{esc(exp)}`',', '.join(langnames[l] for l in langs if l in r['langs']),', '.join(pl(p) for p in phon),', '.join(pl(p) for p in cards),refs])+' |')
 else:md.append('Нет самостоятельных записей с выбранными маркерами.')
 md+=['']
 if cross[ph]:
  md+=['**Совпадающие записи, основные строки которых находятся у других фонем:**','','| Маркер | Правило | Изменение | Основная фонема |','|---|---|---|---|']
  for home,r in sorted(cross[ph],key=lambda x:(rank.get(x[1]['mark'],99),x[1]['rule'])):
   exp=f"{r['result']} {'←' if r['op'] in ('<','←') else '→'} {r['origin']}"
   md.append(f"| {r['mark']} | {link(r['rule'],r['rulelink'])} | `{esc(exp)}` | {pl(home)} |")
  md+=['']
if fails:md+=['## Ошибки чтения','','```',repr(fails),'```']
path=pathlib.Path('/mnt/data/eldamo_six_languages_ipa_catalog.md');path.write_text('\n'.join(md)+'\n','utf-8')
assert all(re.search(r'^## '+re.escape(p)+r'$',path.read_text(),re.M) for p in phonemes)
print('saved',path,'size',path.stat().st_size,'phonemes',len(phonemes),'rows',len(rows),'unique',len(bykey),'failures',fails,'markers',collections.Counter(r['mark'] for r in rows))
