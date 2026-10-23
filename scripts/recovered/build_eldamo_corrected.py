import zipfile,re,collections,html,posixpath
from bs4 import BeautifulSoup,Tag
ZIP='/mnt/data/eldamo-0.8.13.zip'; PREFIX='eldamo-0.8.13/'; BASE='https://eldamo.org/'
z=zipfile.ZipFile(ZIP)
def soup(path): return BeautifulSoup(z.read(PREFIX+path),'html.parser')
def clean(t): return t.get_text(' ',strip=True) if hasattr(t,'get_text') else str(t).strip()
def url_for(path): return BASE+path
def ix_sounds(lang):
 path=f'content/phonetic-indexes/phonetics-{lang}.html';s=soup(path);h=next(x for x in s.find_all('h2') if x.get_text(' ',strip=True)=='Phonemes')
 out=[]; typ=''
 for table in h.find_next_siblings():
  if table.name=='h2':break
  if table.name!='table':continue
  for tr in table.find_all('tr'):
   cells=tr.find_all('td',recursive=False)
   if not cells:continue
   typ=clean(cells[0])
   for td in cells[1:]:
    for a in td.find_all('a',href=True):
     name=clean(a)
     if re.fullmatch(r'\[[^]]+\]',name):
      p=posixpath.normpath(posixpath.join(posixpath.dirname(path),a['href']))
      if (name,p) not in [(a,b) for a,b,c in out]:out.append((name,p,typ))
 return out
# Use table's first-cell marker when shown; otherwise inherit within that table; base on nearby enclosing entry head.
markers=['ᴱAQ.','ᴱQ.','ᴹAQ.','ᴹQ.','AQ.','Q.','ᴱ✶','ᴹ✶','✶']
mark_re=re.compile(r'^(ᴱAQ\.|ᴱQ\.|ᴹAQ\.|ᴹQ\.|AQ\.|Q\.|ᴱ✶|ᴹ✶|✶)(?:\s|$)')
def parse_page(lang,ph,p):
 s=soup(p);result=[]
 for u in s.find_all('u'):
  if clean(u)!='Phonetic Development':continue
  parent=u.parent;tb=parent.find_next_sibling('table')
  if tb is None:continue
  # find closest main entry preceding the block e.g. dt or p id lang-word
  prev=parent.find_previous(['dt','p'])
  context=clean(prev) if prev else ''
  m=mark_re.match(context); period=m.group(1) if m else ('Q.' if lang=='q' else 'AQ.')
  for tr in tb.find_all('tr',recursive=False):
   tds=tr.find_all('td',recursive=False)
   if len(tds)<4:continue
   vals=[clean(t) for t in tds]
   relation=vals[2]
   if relation not in ('<','>','←','→'):continue
   m=mark_re.match(vals[0]);
   if m: period=m.group(1)
   if period.startswith('ᴱ'):continue
   rulelinks=[a for a in tds[0].find_all('a',href=True) if '/words/' in a['href']]
   rule=clean(rulelinks[0]) if rulelinks else (re.sub(r'^(?:ᴹAQ\.|ᴹQ\.|AQ\.|Q\.|ᴹ✶|✶)\s*','',vals[0]).strip() or '[без названия]')
   if rule=='[без названия]' and not vals[0].strip():rule='[без названия]'
   link=url_for(posixpath.normpath(posixpath.join(posixpath.dirname(p),rulelinks[0]['href']))) if rulelinks else ''
   refs=[]
   for a in tds[4].find_all('a',href=True) if len(tds)>4 else []:
    ref=(clean(a),url_for(posixpath.normpath(posixpath.join(posixpath.dirname(p),a['href'].split('#')[0])))+('#'+a['href'].split('#',1)[1] if '#' in a['href'] else ''))
    if ref not in refs:refs.append(ref)
   result.append(dict(lang=lang,ph=ph,page=url_for(p),mark=period,rule=rule,rulelink=link,result=vals[1],origin=vals[3],op=relation,refs=refs))
 return result
sounds={x:ix_sounds(x) for x in ['q','aq']}
allrows=[]; coverage={}; failures=[]
for lang,ls in sounds.items():
 for ph,p,typ in ls:
  try: rows=parse_page(lang,ph,p)
  except Exception as e:failures.append((lang,ph,str(e)));continue
  allrows.extend(rows);coverage[(lang,ph)]=(p,typ,len(rows))
print('SOUNDS',[(k,len(v)) for k,v in sounds.items()],'rows',len(allrows),'fail',failures)
print('vowels',[(x,y,z) for (x,y),(p,t,z) in coverage.items() if 'vowel' in t or 'diphthong' in t])
# collapse by identical rule+expression+marker, preserve all sources and both language indications. One principal entry per matched instance across phonemes
unique=collections.OrderedDict()
for r in allrows:
 key=(r['rule'],r['result'],r['op'],r['origin'],r['mark'],r['rulelink'])
 if key not in unique: unique[key]=dict(r,langs=set(),phs=set(),pages=set(),refs=[])
 a=unique[key];a['langs'].add(r['lang']);a['phs'].add(r['ph']);a['pages'].add(r['page']);
 for ref in r['refs']:
  if ref not in a['refs']:a['refs'].append(ref)
print('unique',len(unique),'markers',collections.Counter(r['mark'] for r in allrows))
# Collect associations at rule level with every phoneme shown as card for a rule, across differing transformations.
rule_sounds=collections.defaultdict(set)
for r in allrows:
 if r['rulelink']:rule_sounds[r['rulelink']].add(r['ph'])
# phoneme normalization, show consonants followed by vowels followed diphthongs
cat_order=['voiceless-stops','voiced-stops','voiceless-spirants','voiced-spirants','nasals','continuants','voiced-continuants','voiceless-continuants','vowels','long-vowels','diphthongs','others']
order={};types={}
for lang in ['q','aq']:
 for ph,p,t in sounds[lang]:
  if ph not in order:order[ph]=len(order)
  types[ph]=t if ph not in types else types[ph]
# actual sort by categories; since Q first has proper series; group under category
sortphon=sorted(order, key=lambda ph:(min([cat_order.index(t) if t in cat_order else 99 for l,ss in sounds.items() for p,_,t in ss if p==ph] or [99]),order[ph]))
ph_num={p:i+1 for i,p in enumerate(sortphon)}
rank={'Q.':0,'ᴹQ.':1,'AQ.':2,'ᴹAQ.':3,'✶':4,'ᴹ✶':5}
# canonical sound first occurrence; cross references for all others. Must preserve separate markers.
by_ph=collections.defaultdict(list); backlinks=collections.defaultdict(list)
for key,r in unique.items():
 phs=sorted(r['phs'],key=lambda p:ph_num[p]);main=phs[0];by_ph[main].append(r)
 for ph in phs[1:]:backlinks[ph].append((main,r))
# Escaping Markdown
fmt=lambda s:str(s).replace('|','\\|').replace('\n',' ')
def link_ph(p):return f'[{p}](#фонема-{ph_num[p]})'
def text_link(label,url):return '['+fmt(label).replace('[','\\[').replace(']','\\]')+']('+url+')' if url else fmt(label)
out=['# Фонетические изменения Quenya и Ancient Quenya — полный каталог по фонемам','',
 '**Источник:** локальный архив Eldamo 0.8.13, [`Quenya Phonetics`](https://eldamo.org/content/phonetic-indexes/phonetics-q.html), [`Ancient Quenya Phonetics`](https://eldamo.org/content/phonetic-indexes/phonetics-aq.html).','',
 '## Методика и замечания','',
 '- Включены **все звуки** из таблиц *Phonemes* обоих языков, в том числе краткие гласные, долгие гласные и дифтонги (там, где они представлены).',
 '- В пределах фонемы записи находятся в одной таблице без разделения по языкам. Порядок маркеров: **Q. → ᴹQ. → AQ. → ᴹAQ.**, затем остальные обозначения (✶, ᴹ✶).',
 '- Маркеры **ᴱQ.** и **ᴱAQ.** исключены; остальные сохранены. Пустой маркер внутри таблицы наследует предыдущий.',
 '- Полностью совпавшие **название правила + ссылка на правило + формула + маркер** объединены. Если одинаковая запись попалась на нескольких карточках звуков, таблица содержит её один раз в разделе первой фонемы; под другими фонемами указана перекрёстная ссылка.',
 '- **«Связанные фонемы»** означает все фонемы, в карточках которых фигурирует **данное правило Eldamo** (по ссылке на правило); перечисление может быть шире конкретного преобразования. Звуки, только упомянутые в формуле, но не имеющие отдельной карточки с этим правилом, сюда автоматически не добавляются.',
 '- Столбец **«Карточки записи»** сообщает, в каких звуковых карточках встретилось именно данное преобразование с тем же маркером; это более узкий набор, чем «Связанные фонемы».',
 '- Знаки `<` и `>` отображаются в формулах в виде `←` и `→` соответственно, без изменения порядка двух частей.', '',
 '## Контроль полноты','',
 '| Показатель | Значение |','|---|---:|',
 f'| Звуков Quenya | {len(sounds["q"])} |',f'| Звуков Ancient Quenya | {len(sounds["aq"])} |',
 f'| Различных фонем | {len(sortphon)} |', f'| Исходных отобранных строк | {len(allrows)} |',f'| Уникальных основных записей | {len(unique)} |',
 f'| Удалённых повторных вхождений | {len(allrows)-len(unique)} |',f'| Ошибок чтения карточек | {len(failures)} |','',
 '## Навигация','', ' · '.join(link_ph(p) for p in sortphon),'']
for ph in sortphon:
 out.extend([f'## Фонема {ph_num[ph]}','',f'**{ph}**', ''])
 for lang,nm in [('aq','Ancient Quenya'),('q','Quenya')]:
  match=[p for name,p,t in sounds[lang] if name==ph]
  if match:out.append(f'Карточка {nm}: [{ph}]({url_for(match[0])}).  ')
 out.append('')
 es=sorted(by_ph[ph],key=lambda r:(rank.get(r['mark'],8),r['rule'].lower(),r['result'],r['origin']))
 if es:
  out+=['| Маркер | Правило Eldamo | Изменение | Связанные фонемы правила | Карточки записи | Источники |','|---|---|---|---|---|---|']
  for r in es:
   formula=f"{r['result']} {'←' if r['op'] in ('<','←') else '→'} {r['origin']}"
   allph=sorted(rule_sounds.get(r['rulelink'],set()) or r['phs'],key=lambda p:ph_num[p]);en=sorted(r['phs'],key=lambda p:ph_num[p]);refs=', '.join(text_link(n,u) for n,u in r['refs']) or '—'
   out.append('| '+' | '.join([fmt(r['mark']),text_link(r['rule'],r['rulelink']),f'`{fmt(formula)}`',', '.join(link_ph(p) for p in allph),', '.join(link_ph(p) for p in en),refs])+' |')
 else:out.append('Нет собственных основных записей.')
 out.append('')
 if backlinks[ph]:
  out+=['**Правила, основные записи которых размещены у других фонем:**','', '| Маркер | Правило | Изменение | Основная фонема |','|---|---|---|---|']
  for primary,r in sorted(backlinks[ph],key=lambda x:(rank.get(x[1]['mark'],8),x[1]['rule'])):
   formula=f"{r['result']} {'←' if r['op'] in ('<','←') else '→'} {r['origin']}"
   out.append(f"| {fmt(r['mark'])} | {text_link(r['rule'],r['rulelink'])} | `{fmt(formula)}` | {link_ph(primary)} |")
  out.append('')
if failures:out+=['## Ошибки чтения','','```',repr(failures),'```']
name='/mnt/data/eldamo_quenya_ancient_quenya_complete_tables_v2.md'
open(name,'w',encoding='utf8').write('\n'.join(out)+'\n')
print('saved',name,'bytes',len(open(name,'rb').read()),'phonemes',len(sortphon))
