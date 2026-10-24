import os,re,json,zipfile,collections,copy,shutil,hashlib,csv,posixpath,html
from pathlib import Path
from bs4 import BeautifulSoup,Tag
ROOT=Path(__file__).resolve().parent.parent;APP=ROOT/'app';APP.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT.parent/'eldamo-0.8.13.zip'
if not SOURCE.exists():raise FileNotFoundError(f'Place Eldamo source archive at {SOURCE}')
Z=zipfile.ZipFile(SOURCE); prefix='eldamo-0.8.13/content/'
CFG=[('Primitive Elvish','p','late',0,['✶']),('Ancient Telerin','at','late',1,['AT.']),('Old Sindarin','os','late',2,['OS.']),('Sindarin','s','late',3,['S.']),('Middle Primitive Elvish','mp','middle',0,['ᴹ✶']),('Old Noldorin','on','middle',1,['ON.']),('Noldorin','n','middle',2,['N.'])]
BASE='https://eldamo.org/content/'
def clean(el):return el.get_text(' ',strip=True)
def loc(p,href):return posixpath.normpath(posixpath.join(posixpath.dirname(p),href.split('#')[0]))
def soup(p):return BeautifulSoup(Z.read(prefix+p),'html.parser')
all_sounds=collections.defaultdict(set); raw=[];errors=[]; seen=set()
for lang,code,era,stage,markers in CFG:
 path='phonetic-indexes/phonetics-'+code+'.html'; sp=soup(path)
 h=next((x for x in sp.find_all(re.compile('^h[1-6]$')) if clean(x).lower()=='phonemes'),None)
 assert h,lang
 pages=[]
 for el in h.next_elements:
  if isinstance(el,Tag) and el.name in ['h1','h2','h3'] and 'Phonetic Groups' in clean(el):break
  if isinstance(el,Tag) and el.name=='a' and re.fullmatch(r'\[[^]]+\]',clean(el)) and el.get('href'):
   symbol=clean(el)[1:-1];p=loc(path,el['href']);
   if (symbol,p) not in pages:pages.append((symbol,p))
 for sym,p in pages:
  all_sounds[sym].add(code)
  try:s=soup(p)
  except Exception as e:errors.append([code,sym,str(e)]);continue
  labels=s.find_all(string=lambda t:bool(t) and t.strip()=='Phonetic Development')
  for label in labels:
   tab=label.parent.find_next('table')
   if not tab:continue
   mark=''; rule=''
   for tr in tab.find_all('tr'):
    cells=tr.find_all(['td','th'],recursive=False)
    if len(cells)<4:continue
    lcell=clean(cells[0]); mm=re.match(r'^((?:ᴱ|ᴹ)?(?:AT|OS|ON|S|N|Q|AQ|T)\.|ᴹ✶|ᴱ✶|✶)\s*(.*)',lcell)
    if mm:mark,rule=mm.groups()
    if mark not in markers:continue
    direction=clean(cells[2]);
    if direction not in ['<','>','←','→']:continue
    left=clean(cells[1]);right=clean(cells[3]);
    if direction in ['<','←']: a,b=right,left
    else:a,b=left,right
    links=[BASE+loc(p,t['href']) for t in cells[0].find_all('a',href=True)]
    refs=[clean(t) for t in cells[4].find_all('a',href=True)] if len(cells)>4 else []
    snippet=clean(cells[4]) if len(cells)>4 else ''
    url=links[0] if links else ''
    rec={'symbol':sym,'catalog':code,'language':lang,'era':era,'stage':stage,'marker':mark,'rule':rule or '[без названия]','a':a,'b':b,'formula':left+' '+direction+' '+right,'url':url,'sound_url':BASE+p,'refs':refs,'example_note':snippet[:500]}
    k=(code,sym,mark,rec['formula'],url,tuple(refs))
    if k not in seen:raw.append(rec);seen.add(k)
print('raw',len(raw),'sounds',len(all_sounds),'errors',errors[:5])
# Deduplicate by rule formula marker but preserve per-sound references
merged={}
for rec in raw:
 k=(rec['era'],rec['marker'],rec['formula'],rec['url'],rec['rule'])
 if k not in merged:
  v=rec.copy();v['sounds']=[rec['symbol']];v['catalogs']=[rec['catalog']];v['refs_all']=list(rec['refs']);merged[k]=v
 else:
  v=merged[k];
  for field,val in [('sounds',rec['symbol']),('catalogs',rec['catalog'])]:
   if val not in v[field]:v[field].append(val)
  for ref in rec['refs']:
   if ref not in v['refs_all']:v['refs_all'].append(ref)
records=list(merged.values())
# tokenize literal IPA, while excluding Eldamo pattern placeholders and alternations
invalid=re.compile(r'[{}|\[\]()/₁₂₃₄VCŠS_+*?=<>⁺⁻⁰\d ]')
def literal(x):
 x=x.strip().replace('`','')
 x=re.sub(r'^-|-$','',x)
 if not x or invalid.search(x) or x in ['ø','∅'] or 'ø' in x:return None
 return x
edges=[];edict={}
for rec in records:
 a=literal(rec['a']);b=literal(rec['b']);
 if a is None or b is None or a==b:continue
 key=(rec['era'],rec['stage'],a,b,rec['marker'],rec['url'])
 if key in edict:continue
 e={'a':a,'b':b,'era':rec['era'],'stage':rec['stage'],'marker':rec['marker'],'rule':rec['rule'],'url':rec['url'],'cards':', '.join(rec['catalogs']),'tested':0,'exact':0,'cautions':'Проверить окружение, хронологию и диалект; атомарная проекция, не полная семантика.','comment':rec['example_note'][:180],'formula':rec['formula']}
 edict[key]=e;edges.append(e)
# actual rule page examples used for edge evidence based on formula and link (avoid claiming proof)
cache={}
for e in edges:
 url=e['url']
 if not url or '/content/' not in url:continue
 p=url.split('/content/',1)[1].split('#')[0]
 if p not in cache:
  try:cache[p]=soup(p)
  except:cache[p]=None
 sp=cache[p]
 if sp:
  title=sp.get_text(' ',strip=True)
  e['tested']=int('Phonetic Rule Examples' in title)
  # no full word derivation proved; keep exact=0
# per-phoneme full rules, including ones without graph edge
byphon=collections.defaultdict(list)
for rec in records:
 r={'marker':rec['marker'],'rule':rec['rule'],'formula':rec['formula'],'url':rec['url'],'catalogs':', '.join(rec['catalogs']),'source':', '.join(rec['refs_all']),'sounds':', '.join(rec['sounds'])}
 for sym in rec['sounds']:byphon[sym].append(r)
for sym in byphon:
 byphon[sym].sort(key=lambda x:(['S.','OS.','AT.','✶','N.','ON.','ᴹ✶'].index(x['marker']) if x['marker'] in ['S.','OS.','AT.','✶','N.','ON.','ᴹ✶'] else 99,x['rule']))
# graphs: depth 2-4, monotone stage and era
adj=collections.defaultdict(list)
for e in edges:adj[(e['era'],e['a'])].append(e)
chains=[]; duplicate=set()
for era in ['late','middle']:
 for start in sorted({e['a'] for e in edges if e['era']==era}):
  stack=[(start,[start],[],-1)]
  examined=0
  while stack and examined<30000:
   at,states,path,prev=stack.pop();examined+=1
   if len(path)>=2:
    key=(era,tuple(states),tuple((x['url'],x['marker']) for x in path))
    if key not in duplicate:
     duplicate.add(key)
     chains.append({'id':'S'+str(len(chains)+1),'states':states,'era':era,'grade':'unassessed','kind':'new-unassessed','markers':' → '.join(x['marker'] for x in path),'evidence':'Нет проверенного непрерывного этимологического ряда','reason':'Структурно составимая последовательность. Контекст, порядок и соответствие одной словоформе не проверены.','action':'Проверить каждый шаг по примерам и развёрнутым заметкам Eldamo.','rule_urls':[x['url'] for x in path], 'urls':[x['url'] for x in path], 'rules':[x['rule'] for x in path]})
   if len(path)==3:continue
   for e in adj[(era,at)][:60]:
    if e['stage']<prev or e['b'] in states:continue
    stack.append((e['b'],states+[e['b']],path+[e],e['stage']))
   if len(chains)>12000:break
  if len(chains)>12000:break
# smaller catalog bounded size if huge
print('merged',len(records),'edges',len(edges),'chains',len(chains))
# update application from template
T=ROOT/'scripts'/'template'
for file in ['index.html','styles.css','app.js']:
 shutil.copy(T/file,APP/file)
(APP/'edges.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2));(APP/'rules.json').write_text(json.dumps(byphon,ensure_ascii=False,indent=2));(APP/'chains.json').write_text(json.dumps(chains,ensure_ascii=False,indent=2))
(APP/'data.js').write_text('window.ELDAMO_EDGES = '+json.dumps(edges,ensure_ascii=False)+';\nwindow.ELDAMO_RULES = '+json.dumps(byphon,ensure_ascii=False)+';\n')
(APP/'chains.js').write_text('window.ELDAMO_CHAINS = '+json.dumps(chains,ensure_ascii=False)+';\n')
# replace sound buttons with all recorded IPA, sorted fairly by category
vowels_base={'a','e','i','o','u','ā','ē','ī','ō','ū','ǣ','ǭ','ę̄','ø','y','ȳ','ɛ','ɔ','œ','ə','ǫ','æ','ǣ','ə̄'}
def classification(t):
 if t in vowels_base or (len(t)==1 and t in 'aeiouyæəø'):return 1
 if len(t)>=2 and all(c in 'aeiouyæəøāēīōūǣǭ̄́̆' for c in t):return 2
 return 0
symbols=sorted(all_sounds,key=lambda x:(classification(x),x))
# rebuild IPA selection table for both sides in the same locations
sp=BeautifulSoup((APP/'index.html').read_text(),'html.parser')
sp.title.string='Eldamo — фонетический атлас Sindarin / Noldorin'
h1=sp.find('h1');h1.string='Атлас звуковых путей Sindarin / Noldorin'
hdr=sp.find('header');div=hdr.find('div');div.string='Primitive Elvish → Ancient Telerin → Old Sindarin → Sindarin · Middle Primitive → Old Noldorin → Noldorin'
for slot in ['from','to']:
 area=sp.find(id=slot+'-ipa');area.clear()
 for group,title in [(0,'Согласные'),(1,'Гласные'),(2,'Дифтонги')]:
  h=sp.new_tag('h3');h.string=title;area.append(h)
  table=sp.new_tag('table');body=sp.new_tag('tbody');table.append(body)
  values=[x for x in symbols if classification(x)==group]
  for start in range(0,len(values),10):
   tr=sp.new_tag('tr')
   for phon in values[start:start+10]:
    td=sp.new_tag('td');btn=sp.new_tag('button',attrs={'class':'ipa-sound','type':'button','data-phoneme':phon});btn.string=phon;td.append(btn);tr.append(td)
   body.append(tr)
  area.append(table)
for sel in sp.select('#era option'):
 if sel.get('value')=='late':sel.string='Поздняя: Sindarin'
 if sel.get('value')=='middle':sel.string='Средняя: Noldorin'
sp.select_one('#chain-atlas p').string=f'{len(chains)} структурных кандидатов; историческая доказательность ещё не оценена. Не путать с категорией U.'
opt=sp.new_tag('option',value='unassessed');opt.string='Не оценена';sp.select_one('#atlas-grade').append(opt)
(APP/'index.html').write_text(str(sp))
js=(APP/'app.js').read_text()
js=re.sub(r'const PHONEMES = \[.*?\];', 'const PHONEMES = '+json.dumps(symbols,ensure_ascii=False)+';',js,count=1,flags=re.S)
js=js.replace("const vals = { from: 'b', to: 'f' }", "const vals = { from: 'p', to: 'f' }")
js=js.replace(" : 'b');", " : 'p');")
js=js.replace("src === 'b' && dst === 'f'", "false")
js=js.replace('r.marker, r.title, r.formula, r.url, r.langs','r.marker, r.rule, r.formula, r.url, r.catalogs')
js=js.replace('safe(r.title)','safe(r.rule)').replace('safe(r.langs)','safe(r.catalogs)')
js=js.replace("r.sources.map(x => '<a href=\"' + safe(x[1]) + '\" target=\"_blank\" rel=\"noopener\">' + safe(x[0]) + '</a>').join(' · ')","safe(r.source || '')")
js=js.replace("const ranking = { 'Q.': 0, 'ᴹQ.': 1, 'AQ.': 2, 'ᴹAQ.': 3, '✶': 4, 'ᴹ✶': 5 };", "const ranking = { 'S.': 0, 'OS.': 1, 'AT.': 2, '✶': 3, 'N.': 4, 'ON.': 5, 'ᴹ✶': 6 };")
js=js.replace("'—': 'Не оценена'", "'—': 'Не оценена', unassessed: 'Не оценена'")
js=js.replace("'дополнительная оценённая цепочка'", "'структурный кандидат (оценка отсутствует)'")
js=js.replace('A–X/U — оценки 139 исследованных цепочек; вновь найденные поиском пути не оценены.', 'Категория «Не оценена» означает отсутствие полной проверки цепочки по словоформам, хронологии и контексту.')

# ensure no borrowed quenya-specific wording
js=js.replace('Для b каталог содержит b → β → v, а не b → f; f образуется, например, из ɸ. Для b → f нет соединяющего правила в индексированной выборке.', 'Путь не обнаружен в синдаринском индексе.')
js=js.replace("const gradeInfo =","const gradeInfo =")
(APP/'app.js').write_text(js)
# compile standalone
out=(APP/'index.html').read_text()
out=out.replace('<link href="styles.css" rel="stylesheet"/>','<style>\n'+(APP/'styles.css').read_text()+'\n</style>')
for script in ['data.js','chains.js','app.js']:
 out=re.sub(r'<script[^>]*src="'+script+r'"[^>]*>\s*</script>',lambda m:'<script>\n'+(APP/script).read_text()+'\n</script>',out)
assert 'src="app.js"' not in out
(APP/'standalone.html').write_text(out)
# markdown comprehensive index
catalog=ROOT/'catalog';catalog.mkdir(exist_ok=True)
texts=['# Sindarin / Noldorin — фонетические правила по звукам','', 'Eldamo 0.8.13. Исключены Early-маркеры и боковая ветвь Telerin.','', 'Поздняя: ✶, AT., OS., S. Средняя: ᴹ✶, ON., N.','', '## Навигация по фонемам','', ' · '.join(f'[{s}](#фонема-{i+1})' for i,s in enumerate(symbols)),'']
for i,s in enumerate(symbols):
 texts +=[f'## Фонема {i+1}: [{s}]','', '| Период | Правило | Формула | Каталоги | Источники |','|---|---|---|---|---|']
 for r in byphon.get(s,[]):
  esc=lambda x:str(x).replace('|','\\|').replace('\n',' ')
  texts.append('| '+' | '.join([esc(r['marker']),f"[ {esc(r['rule'])} ]({r['url']})" if r['url'] else esc(r['rule']),f"`{esc(r['formula'])}`",esc(r['catalogs']),esc(r['source'])])+' |')
 texts.append('')
(catalog/'sindarin_phonetic_catalog.md').write_text('\n'.join(texts))
(ROOT/'data').mkdir(exist_ok=True)
with (ROOT/'data'/'rule_inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['era','stage','marker','rule','a','b','formula','url','catalogs','sounds','refs_all']);w.writeheader();w.writerows({k:v.get(k) for k in w.fieldnames} for v in records)
(ROOT/'data'/'phonemes.json').write_text(json.dumps({s:sorted(x) for s,x in all_sounds.items()},ensure_ascii=False,indent=2))
(ROOT/'data'/'parse_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
(ROOT/'README.md').write_text(f'''# Eldamo Sindarin / Noldorin — отдельный фонетический атлас\n\nИсточник: Eldamo 0.8.13, архив eldamo-0.8.13.zip.\n\nПоздняя линия: Primitive Elvish → Ancient Telerin → Old Sindarin → Sindarin.\nСредняя линия: Middle Primitive Elvish → Old Noldorin → Noldorin.\n\nАманский Telerin и Middle Telerin исключены. Разные исторические концепции никогда не смешиваются при поиске.\n\n## Выходные файлы\n\n- `app/standalone.html` — автономная версия\n- `app/index.html`, `styles.css`, `app.js`, `data.js`, `chains.js` — модульная версия\n- `app/rules.json` — каталог правил по звукам\n- `app/edges.json` — осторожная атомарная проекция\n- `app/chains.json` — **структурные, ещё не оценённые** цепочки\n- `catalog/sindarin_phonetic_catalog.md` — полный каталог по звукам\n- `data/rule_inventory.csv` — реестр всех уникальных формул\n- `scripts/build_sindarin.py` — повторная сборка\n\n## Проверки\n\nОбнаружено {len(symbols)} разных обозначений фонем; {len(raw)} вхождений, {len(records)} объединённых записей, {len(edges)} атомарных переходов, {len(chains)} структурных цепочек. Ошибок чтения: {len(errors)}.\n\n**Доказательность:** цепочки категории U, поскольку наличие сочетаемых атомарных правил не является доказательством их последовательной исторической применимости. Применимость окружений и хронология по заметкам ещё не верифицированы для всех путей. Это не перенос 139 оценок Quenya.\n\nСтраница применяет ограничения на период и порядок ступеней. Результаты поиска — гипотезы, а не полностью доказанные этимологии.\n''')
(ROOT/'scripts').mkdir(exist_ok=True)
# Running from scripts/; the current builder is already included
print('done',ROOT)
