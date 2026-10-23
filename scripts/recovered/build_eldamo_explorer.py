import csv,json,re,html,pathlib,collections,zipfile,datetime
P=pathlib.Path('/mnt/data');read=lambda n:list(csv.DictReader(open(P/n,encoding='utf-8-sig',newline='')))
rules=read('eldamo_v2_all_rules.csv');valid=read('eldamo_v3_rule_example_validation.csv');notes={r['rule_url']:r for r in read('eldamo_rule_commentary_audit.csv')};vmap={(r['marker'],r['from'],r['to'],r['rule_url']):r for r in valid}
rank={'✶':0,'AQ.':1,'Q.':2,'ᴹ✶':0,'ᴹAQ.':1,'ᴹQ.':2}
period={'✶':'late','AQ.':'late','Q.':'late','ᴹ✶':'middle','ᴹAQ.':'middle','ᴹQ.':'middle'}
edges=[];seen=set();discard=collections.Counter()
for r in rules:
 mark=r['marker']; era=period.get(mark)
 if not era:continue
 items=(r.get('parsed_variants') or '').split(';')
 if not items or not items[0].strip(): items=[r['from']+' → '+r['to']]
 for x in items:
  pair=re.split(r'\s*→\s*',x.strip())
  if len(pair)!=2:discard['unparsed']+=1;continue
  a,b=map(str.strip,pair)
  if not a or not b or a==b or len(a)>14 or len(b)>14: discard['empty_or_large']+=1;continue
  # Atomic state paths only, explicitly avoid semantic variables and context shorthand
  if re.search(r'[{}|VCS_+*?⁺⁻₁₂₃\[\]()]',a+b):discard['contextual']+=1;continue
  key=(mark,a,b,r.get('rule_url',''))
  if key in seen:continue
  seen.add(key)
  v=vmap.get((mark,r['from'],r['to'],r['rule_url']),{})
  note=notes.get(r['rule_url'],{})
  snippet=note.get('notes','')
  cautions=note.get('caution_terms','')
  edges.append(dict(a=a,b=b,era=era,stage=rank[mark],marker=mark,rule=r['rule'],url=r['rule_url'] or '',cards=r['language_cards'],tested=int(v.get('matching_example_rows') or 0),exact=int(v.get('exact_formula_matches') or 0),cautions=cautions,comment=(snippet[:250] if snippet else '')))
# Comparison to historical candidates from CSV, no assertion of proof
cases=read('eldamo_critical_101_atlas.csv')
annot={e['url']:notes[e['url']] for e in edges if e['url'] in notes}
chron=[]
for url,n in annot.items():
 txt=n['notes']
 for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])',txt):
  if re.search(r'\b(before|after|preced|follow|earlier|later|dialect|Noldor|Vanyar|only|except)\b',sent,re.I):
   if len(sent)<30:continue
   chron.append(dict(rule_url=url,rule=n['title'],type='explicit-order-or-context-clue',excerpt=sent[:560],automatic_constraint='NOT INFERRED',review='manual relation extraction required'))
chron=chron[:5000]
with open(P/'eldamo_order_and_context_clues.csv','w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=['rule_url','rule','type','excerpt','automatic_constraint','review']);w.writeheader();w.writerows(chron)
# Tests against historical candidates paths, textual stage monotonicity, and normalized graph inclusion
by=collections.defaultdict(list)
for e in edges:by[(e['era'],e['a'])].append(e)
def feasible(path,era,maxout=10000):
 states=[s.strip() for s in path.split('→')]
 chains=[([], -1)]
 for a,b in zip(states,states[1:]):
  opts=[e for e in by[(era,a)] if e['b']==b]
  nextc=[]
  for chosen,stage in chains:
   for e in opts:
    if e['stage']>=stage:nextc.append((chosen+[e],e['stage']))
  chains=nextc[:maxout]
  if not chains:break
 return len(chains),states
rows=[]
for c in cases:
 n,ss=feasible(c['states'],c['era'])
 rows.append({'id':c['id'],'path':c['states'],'era':c['era'],'previous_grade':c['grade'],'stage_consistent_rule_combinations':n,'verdict':'structurally possible using atomic rule variants' if n else 'not resolved by atomic graph (NOT refuted)','limitations':'Rule-local examples do not prove sequential word history; prose chronology and context not automatically enforced'})
with open(P/'eldamo_101_stage_reassessment.csv','w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Build searchable index covering all literal variants; separate period filters and ascending in-world stage
asset=json.dumps(edges,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
ht='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eldamo — атлас звуковых путей</title><style>
:root{color-scheme:dark;--bg:#0d1523;--fg:#e7edf6;--muted:#9aabc2;--accent:#88baff;--panel:#172237;--stroke:#34445c}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}header{padding:30px max(20px,calc((100vw - 1100px)/2));background:linear-gradient(110deg,#1d3556,#101a2b)}h1{margin:0 0 5px;font-size:clamp(23px,4vw,35px)}h2{font-size:19px;margin:8px 0 14px}small,.muted{color:var(--muted)}main{max-width:1100px;padding:20px;margin:auto}.panel{background:var(--panel);border:1px solid var(--stroke);border-radius:13px;padding:19px;margin-bottom:16px}.controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}label{display:block;font-size:13px;color:var(--muted)}input,select{display:block;width:100%;background:#0b1423;color:var(--fg);border:1px solid #60718a;border-radius:7px;padding:10px;font:inherit;margin-top:5px}button{background:#8abaff;color:#051224;border:0;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer}button:hover{background:#b4d3ff}.row{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:14px}.row label{display:flex;gap:6px;align-items:center}.row input{width:auto;margin:0}.stats{font-size:13px;color:var(--muted)}.path{border-top:1px solid var(--stroke);padding:15px 0}.route{font-size:20px;font-weight:650;overflow-wrap:anywhere;line-height:1.8}.route span{display:inline-block;border-radius:6px;background:#283e60;padding:0px 9px;margin:2px}.pill{display:inline-block;border:1px solid #556b87;padding:2px 7px;border-radius:100px;font-size:12px;color:#baccdf;margin:5px 4px 5px 0}ol{padding-left:22px}li{margin:6px 0}a{color:#a5cdff;overflow-wrap:anywhere}.warn{border-left:3px solid #d2ad6d;padding:8px 12px;background:#352b22;color:#f0d8ad;border-radius:4px;margin:10px 0}details{margin-top:8px}summary{cursor:pointer;color:#bcd4fa}code{color:#b1e1f1}#output{min-height:70px}@media(max-width:650px){.controls{grid-template-columns:1fr}main{padding:12px}.panel{padding:14px}}</style></head><body><header><h1>Атлас звуковых путей Eldamo</h1><div>Праэльфийский → древняя квенья → квенья · Eldamo 0.8.13</div><small>Автономный исследовательский интерфейс. Цепочки — структурные кандидаты, не автоматически доказанные исторические процессы.</small></header><main><section class="panel"><h2>Поиск путей между звуками и сочетаниями</h2><div class="controls"><label>Исходный звук / сочетание<input id="from" list="sounds" value="pʰ" spellcheck="false"></label><label>Конечный звук / сочетание<input id="to" list="sounds" value="f" spellcheck="false"></label><label>Период разработки Толкина<select id="era"><option value="late">Поздняя концепция (✶, AQ., Q.)</option><option value="middle">Средняя концепция (ᴹ✶, ᴹAQ., ᴹQ.)</option></select></label><label>Максимальная длина<select id="depth"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option></select></label></div><datalist id="sounds"></datalist><div class="row"><label><input type="checkbox" id="stage" checked> Соблюдать ступени Primitive → Ancient → Quenya</label><label><input type="checkbox" id="evidence"> Только переходы с воспроизведёнными примерами</label><label><input type="checkbox" id="simple" checked> Без повторения состояний</label></div><div class="row"><button id="go">Найти пути</button><button id="swap" style="background:#2c4366;color:#e5efff">Поменять местами</button><span class="stats" id="numbers"></span></div></section><section class="panel"><h2>Найденные цепочки</h2><div id="output" aria-live="polite">Укажите два звука и нажмите «Найти пути».</div></section><section class="panel"><h2>О достоверности</h2><p>Каждая стрелка связана с записью правила Eldamo. Наличие формулы и даже отдельного примера <strong>не доказывает</strong> непрерывное развитие одной словоформы. Сохраняются ограничения из свободных заметок, диалектные исключения, редакционные различия, порядок внутри одной ступени и специфика групп звуков.</p><p>Индекс включает лишь те варианты правил, которые безопасно удалось представить как переходы между явными строковыми состояниями. Контекстные формулы остаются в полном каталоге и интерпретаторе Python, но не превращаются в безусловные рёбра интерфейса.</p><p>Выполненный поиск не показывает гарантированно все исторические линии: это контролируемый поиск по атомарной проекции правил. Статусы «есть пример» — свидетельства одного шага, не всей цепочки.</p></section></main><script>
const EDGES=__DATA__;
const $=x=>document.getElementById(x);
const states=Array.from(new Set(EDGES.flatMap(e=>[e.a,e.b]))).sort((a,b)=>a.localeCompare(b));
$('sounds').innerHTML=states.map(s=>'<option value="'+s.replace(/&/g,'&amp;').replace(/"/g,'&quot;')+'"></option>').join('');
$('numbers').textContent=`${EDGES.length} атомарных переходов · ${states.length} звуковых состояний`;
const safe=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
function find(){const src=$('from').value.trim(),dst=$('to').value.trim(),era=$('era').value,maxD=Number($('depth').value),stage=$('stage').checked,ev=$('evidence').checked,simple=$('simple').checked;
 const adj=new Map();for(const e of EDGES){if(e.era!==era||(ev&&!e.tested))continue;if(!adj.has(e.a))adj.set(e.a,[]);adj.get(e.a).push(e)}
 let found=[],queue=[{at:src,nodes:[src],edges:[],st:-1}],scanned=0,truncated=false;const LIMIT=70000;
 for(let head=0;head<queue.length;head++){const p=queue[head];if(++scanned>LIMIT){truncated=true;break}if(p.at===dst&&p.edges.length){found.push(p);if(found.length>=80){truncated=true;break}continue}if(p.edges.length>=maxD)continue;
 for(const e of (adj.get(p.at)||[])){if(stage&&e.stage<p.st)continue;if(simple&&p.nodes.includes(e.b))continue;queue.push({at:e.b,nodes:p.nodes.concat(e.b),edges:p.edges.concat(e),st:e.stage})}}
 const out=$('output');if(!found.length){out.innerHTML='<p>Путей в выбранной проекции не найдено. Это <strong>не опровержение</strong> исторической возможности: попробуйте увеличить глубину, снять фильтр примеров или проверить контекстные правила в полном каталоге.</p>'+(truncated?'<p class="warn">Поиск ограничен по числу перебираемых состояний.</p>':'');return}
 found.sort((a,b)=>a.edges.length-b.edges.length||b.edges.reduce((n,x)=>n+(x.exact?1:0),0)-a.edges.reduce((n,x)=>n+(x.exact?1:0),0));out.innerHTML=`<p class="stats">Найдено ${found.length} структурных кандидатов; отображается до 80. ${truncated?'Поиск был ограничен ресурсами.':''}</p>`+found.map((p,i)=>'<article class="path"><div class="route">'+p.nodes.map(n=>'<span>'+safe(n)+'</span>').join(' → ')+'</div><span class="pill">'+p.edges.length+' перехода</span><span class="pill">'+p.edges.filter(x=>x.exact).length+' с точным примером шага</span><details '+(i===0?'open':'')+'><summary>Правила, источники и ограничения</summary><ol>'+p.edges.map(e=>'<li><strong>'+safe(e.a)+' → '+safe(e.b)+'</strong> · '+safe(e.marker)+' · '+(e.url?'<a href="'+safe(e.url)+'" target="_blank" rel="noopener">'+safe(e.rule)+'</a>':safe(e.rule))+' <small>('+safe(e.cards)+')</small>'+(e.exact?'<div class="muted">Есть пример с совпадающей формулой на странице правила.</div>':'<div class="muted">Точного проверенного примера шага нет.</div>')+(e.cautions?'<div class="warn">Условия из заметки требуют проверки: '+safe(e.cautions)+'</div>':'')+(e.comment?'<details><summary>Фрагмент пояснения</summary>'+safe(e.comment)+'…</details>':'')+'</li>').join('')+'</ol></details></article>').join('')}
$('go').addEventListener('click',find);$('swap').addEventListener('click',()=>{let v=$('from').value;$('from').value=$('to').value;$('to').value=v;find()});$('from').addEventListener('keydown',e=>{if(e.key==='Enter')find()});$('to').addEventListener('keydown',e=>{if(e.key==='Enter')find()});find();</script></body></html>'''.replace('__DATA__',asset)
(P/'eldamo_sound_path_explorer.html').write_text(ht,encoding='utf-8')
stat=collections.Counter(r['verdict'] for r in rows)
report=f'''# Eldamo 0.8.13 — автономный поиск звукопреобразований и аудит ограничений

## Что реализовано

- [Интерактивный атлас](eldamo_sound_path_explorer.html): автономная HTML-страница, полнотекстовые значения исходного и конечного звука или сочетания, отдельная средняя/поздняя концепция, ограничение длины, поиск в ширину, ссылки и комментарии к правилам.
- Преобразования извлечены из **990 записей** существующего каталога; используются **{len(edges)} атомарных рёбер** после разложения простых альтернатив, при этом контекстно-зависимые формулы **не приравниваются к безусловным законам**.
- Разобрано **101** ранее найденная цепочка с проверкой наличия направленных атомарных переходов и неубывания исторической ступени; результаты в `eldamo_101_stage_reassessment.csv`. Критерий лишь структурный.
- Извлечено **{len(chron)} фрагментов заметок**, потенциально описывающих относительную хронологию, диалектные условия либо исключения; они сохранены как **требующие интерпретации**, а не автоматически выведенные ограничения.
- Подготовлен полный каталог шести разделов и включён скрипт его генерации.

## Из чего состоят данные

| Вид данных | Объём |
|---|---:|
| Записи формул | {len(rules)} |
| Атомарные рёбра для интерактивного поиска | {len(edges)} |
| Отложенные варианты при разборе | {sum(discard.values())} |
| Фрагменты примечаний для ручной формализации | {len(chron)} |
| Исходные цепочки с найденной структурной проекцией по ступеням | {sum(x['stage_consistent_rule_combinations']>0 for x in rows)} из 101 |

## Граница доказанности

Это **поисковый прототип**, а не универсальная реконструкция всех исторически допустимых словоформ. Расширенный интерпретатор Python v3 поставляется отдельно и остаётся нормативной точкой для проверки контекста на словоформах. HTML использует атомарную проекцию и может предлагать формально совместимые, но исторически несовместимые цепочки. Редакционные эпохи не смешиваются; внутри одной ступени относительная хронология из комментариев **не применяется автоматически**, чтобы избежать неподтверждённых предположений. Ни один путь не назван доказанным исключительно по факту нахождения.

### Почему свободные заметки пока не стали автоматическими ограничениями

Фраза `before X` может обозначать порядок изменения, границу фонетического окружения или историю разработки концепции; её нельзя конвертировать в графическое ограничение без понимания референта X. Реестр `eldamo_order_and_context_clues.csv` хранит соответствующие фрагменты для проверки человеком, не превращая их в искусственную хронологию.

## Файлы

- `eldamo_sound_path_explorer.html` — интерактивный браузерный поиск.
- `eldamo_six_languages_ipa_catalog.md` — ранее составленный полный каталог.
- `make_eldamo_six.py` и `build_eldamo_corrected.py` — исходные скрипты составления каталога.
- `eldamo_101_stage_reassessment.csv` — повторная структурная проверка первоначальных цепочек.
- `eldamo_order_and_context_clues.csv` — фрагменты заметок о порядке и контекстах.
- `eldamo_interpreter_v3.py` — проверка формул на словоформах.
- `eldamo_v3_comprehensive_audit.md` — предшествующий подробный аудит.

## Воспроизведение

Для повторного извлечения из исходника понадобится `eldamo-0.8.13.zip` (не включён из-за объёма и отдельного распространения исходных данных). HTML работает без него и без сети; доступ к внешнему сайту нужен лишь для перехода по ссылкам Eldamo.
'''
(P/'eldamo_explorer_and_chronology_report.md').write_text(report,encoding='utf-8')
files=['eldamo_sound_path_explorer.html','eldamo_explorer_and_chronology_report.md','eldamo_101_stage_reassessment.csv','eldamo_order_and_context_clues.csv','eldamo_six_languages_ipa_catalog.md','make_eldamo_six.py','build_eldamo_corrected.py','eldamo_interpreter_v3.py','eldamo_v3_comprehensive_audit.md','eldamo_v3_101_rule_level_audit.csv','eldamo_v3_rule_example_validation.csv','eldamo_v3_rebuilt_structural_graph.csv','eldamo_v2_all_rules.csv','eldamo_v3_27_normalized_reassessment.csv','build_eldamo_explorer.py']
with zipfile.ZipFile(P/'eldamo_integrated_research_package.zip','w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for fn in files:z.write(P/fn,arcname=fn)
print(json.dumps({'atomic_edges':len(edges),'notes':len(chron),'stage_possible':sum(x['stage_consistent_rule_combinations']>0 for x in rows),'discard':discard,'bundle_bytes':(P/'eldamo_integrated_research_package.zip').stat().st_size},ensure_ascii=False,default=str))
