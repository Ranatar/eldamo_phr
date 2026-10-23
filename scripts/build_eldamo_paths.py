import pathlib,collections,re,csv,json,unicodedata
ns={};exec(pathlib.Path('/mnt/data/build_eldamo_corrected.py').read_text().split('sounds={x:ix_sounds(x)')[0],ns)
langs=['q','mq','aq','maq','p','mp']; sounds={l:ns['ix_sounds'](l) for l in langs}
rows=[]
for l,ss in sounds.items():
 for ph,path,typ in ss:
  for r in ns['parse_page'](l,ph,path):
   if not r['mark'].startswith('ᴱ'): rows.append(r)
marks={'✶':('late',0),'AQ.':('late',1),'Q.':('late',2),'ᴹ✶':('middle',0),'ᴹAQ.':('middle',1),'ᴹQ.':('middle',2)}
def clean(s):return unicodedata.normalize('NFC',s.strip())
# Deliberately narrow atomic eligibility. Boundary-sensitive forms retained but cannot match boundary-free forms.
atomic=re.compile(r'^[a-zɸβθðɣŋʰʷʲɱɲɥʃʒʦʧçʁʎʔɚəɛɔæøœǣǭę̄āēīōūȳṃṇṛḷẓṣ́̂̆̄̃]+(?:-)?$',re.I)
def eligible(s):return bool(atomic.fullmatch(s)) and not any(t in s for t in ('{','}','[',']','(',')','/',',',' ','*','?'))
unique={}; rejected=collections.Counter()
for r in rows:
 if r['mark'] not in marks: rejected['unmapped period']+=1;continue
 a,b=clean(r['result']),clean(r['origin'])
 if r['op'] in ('<','←'): source,target=b,a
 elif r['op'] in ('>','→'): source,target=a,b
 else:rejected['unknown direction']+=1;continue
 if source==target:rejected['no change']+=1;continue
 if not (eligible(source) and eligible(target)):rejected['non-atomic / context-sensitive notation']+=1;continue
 era,stage=marks[r['mark']]
 key=(era,stage,source,target,r['rulelink'],r['rule'])
 if key not in unique:unique[key]={**r,'source':source,'target':target,'era':era,'stage':stage,'langs':set(),'phs':set(),'refs':set()}
 item=unique[key];item['langs'].add(r['lang']);item['phs'].add(r['ph']);item['refs'].update(tuple(z) for z in r['refs'])
edges=list(unique.values())
by_origin=collections.defaultdict(list)
for e in edges:by_origin[(e['era'],e['source'])].append(e)
# Paths must advance historical stages strictly, so are conservative candidates, not proof.
paths=[]
for a in edges:
 for b in by_origin[(a['era'],a['target'])]:
  if b['stage']<=a['stage']:continue
  paths.append([a,b])
  for c in by_origin[(a['era'],b['target'])]:
   if c['stage']<=b['stage']:continue
   paths.append([a,b,c])
# Deduplicate by cited rule identifiers (same sound sequences can have multiple interpretations)
up={}
for p in paths:
 k=(p[0]['era'],tuple((e['source'],e['target'],e['mark'],e['rulelink']) for e in p));up[k]=p
paths=list(up.values())
paths.sort(key=lambda p:(-len(p),p[0]['era'],p[0]['source'],p[-1]['target']))
base=pathlib.Path('/mnt/data')
with (base/'eldamo_sound_edges.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['era','stage','marker','from','to','rule','rule_url','source_cards','sound_cards','references'])
 for e in sorted(edges,key=lambda e:(e['era'],e['stage'],e['source'],e['target'])):
  w.writerow([e['era'],e['stage'],e['mark'],e['source'],e['target'],e['rule'],e['rulelink'],'; '.join(sorted(e['langs'])),'; '.join(sorted(e['phs'])),'; '.join(f'{x} {u}' for x,u in sorted(e['refs']))])
with (base/'eldamo_sound_candidate_paths.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['era','states','periods','rules','rule_urls','confidence'])
 for p in paths:w.writerow([p[0]['era'],' → '.join([p[0]['source']]+[e['target'] for e in p]),' → '.join(e['mark'] for e in p),' || '.join(e['rule'] for e in p),' || '.join(e['rulelink'] for e in p),'formally composable; needs contextual verification'])
# prose report with selected instructive examples
picks=[]
for pattern in [('pʰ','ɸ','f'),('tʰ','θ','s'),('kʰ','x','h')]:
 matches=[p for p in paths if tuple([p[0]['source']]+[e['target'] for e in p])==pattern]
 if matches:picks+=matches[:2]
if len(picks)<6:picks+=paths[:max(0,12-len(picks))]
picks=list({tuple((e['source'],e['target'],e['mark']) for e in p):p for p in picks}.values())
md=['# Сквозные линии звукопреобразований Eldamo 0.8.13 — первый проверяемый прототип','',
'## Назначение','',
'Это **машинно построенный список кандидатов на исторические линии**, а не реконструкция автоматически подтверждённых этимологий. Из шести звуковых каталогов извлечены ориентированные переходы, для которых обе стороны формулы являются явно записанными линейными звуковыми последовательностями. Этимологическая проверка по конкретным словам ещё не выполнена.','',
'## Ключевые ограничения','',
'- Направление восстановлено по обозначению Eldamo: `A < B` даёт `B → A`, `A > B` даёт `A → B`.','- Разделены **поздняя концепция** (`✶`, `AQ.`, `Q.`) и **средняя концепция** (`ᴹ✶`, `ᴹAQ.`, `ᴹQ.`); смешивать их запрещено.','- Задаётся упрощённый порядок стадий `Primitive → Ancient Quenya → Quenya`. Это порядок *ярлыков языковой ступени*, а не гарантированная датировка каждого изменения.','- В CSV кандидатов следующая стрелка допускается, только если её источник буквально совпадает с результатом предыдущей и стадия **строго выше**. Поэтому это намеренно неполный поиск: внутристадийные цепочки пропускаются.','- Формулы со скобками, подстановками, перечислениями и прочими неатомарными обозначениями вынесены из автоматического соединения. Границы слова (`-`) при сопоставлении не отбрасываются.','- Фонетические окружения и исключения из текстов правил полностью **не формализованы**. Каждая найденная составная линия — гипотеза до проверки по этимологическим статьям и контекстам.','- Одинаковые переходы с различными ссылками на правила оставлены как независимые варианты.','',
'## Охват и результаты','',
f'- Исходные карточки: **{sum(len(v) for v in sounds.values())}**, отобранные строки: **{len(rows)}**.',
f'- Нормализованные ориентированные записи (с уникальным правилом и эпохой): **{len(edges)}**.',
f'- Не вошли в строгую нормализацию: **{sum(rejected.values())}** строк; причины: '+', '.join(f'{k} — {v}' for k,v in rejected.items())+'.',
f'- Формально составные линии из двух или трёх переходов: **{len(paths)}** (включая варианты по ссылкам на правила).','',
'## Иллюстративные найденные цепочки','',
'Ниже приведены **кандидаты**, которые проходят только структурную проверку; звуковая, позиционная и текстологическая валидность не доказана.','']
for i,p in enumerate(picks[:12],1):
 md+=[f'### {i}. `'+ ' → '.join([p[0]['source']]+[e['target'] for e in p])+'`','', '| Переход | Маркер | Правило | Карточки языков |','|---|---|---|---|']
 for e in p:
  rule=f'[{e["rule"]}]({e["rulelink"]})' if e['rulelink'] else e['rule']
  md.append(f'| `{e["source"]} → {e["target"]}` | `{e["mark"]}` | {rule.replace("|","\\|")} | {", ".join(sorted(e["langs"]))} |')
 md.append('')
md+=['## Файлы результатов','','- [`eldamo_sound_edges.csv`](eldamo_sound_edges.csv) — полный список строго нормализованных рёбер с маркерами, страницами и источниками.','- [`eldamo_sound_candidate_paths.csv`](eldamo_sound_candidate_paths.csv) — все найденные дву- и трёхшаговые пути (кандидаты).','- Скрипт `build_eldamo_paths.py` воспроизводит обработку из архива в той же папке.','',
'## Следующий методологический этап','',
'Для каждой линии нужно проверить исходные формулировки правил (позиционные и морфонологические условия), а затем найти реальные этимологические цепи конкретных слов в Eldamo. Только после этого можно повышать статус «формально составима» до «текстологически подтверждена».']
(base/'eldamo_sound_paths_report.md').write_text('\n'.join(md)+'\n',encoding='utf8')
print('rows',len(rows),'edges',len(edges),'rejected',dict(rejected),'paths',len(paths),'sample',[(p[0]['era'],[p[0]['source']]+[e['target'] for e in p]) for p in picks[:12]])
