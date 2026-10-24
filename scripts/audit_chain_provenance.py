"""Audit each chain step against the branch-specific unified atomic graph.
No identity is inferred from endpoints. Does not assign historical grades.
"""
from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parents[1]

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def run():
 summary={}
 for branch in ('quenya','sindarin'):
  base=ROOT/'branches'/branch
  edges=load(base/'data/atomic_edges_unified.json')
  index=collections.defaultdict(list)
  for e in edges:index[(e['era'],e['a'],e['b'])].append(e)
  output={};stats={};detail=[]
  for corpus,path in (('critical',base/'app/chains.json'),('structural',base/'data/research_chains_for_app.json')):
   chains=load(path);counter=collections.Counter();results=[]
   for c in chains:
    states=c.get('states',[]);urls=c.get('urls') or c.get('rule_urls') or []
    steps=[]
    for i,(a,b) in enumerate(zip(states,states[1:])):
     url=urls[i] if i<len(urls) else None
     candidates=index.get((c.get('era'),a,b),[])
     matches=[e for e in candidates if url and e['url']==url]
     if not candidates:status='not_in_atomic_graph'
     elif not url:status='missing_chain_rule_url'
     elif not matches:status='rule_url_mismatch'
     elif len(matches)>1:status='multiple_matching_rules'
     else:status='exact_step_match'
     counter[status]+=1
     steps.append({'index':i,'from':a,'to':b,'rule_url':url,'status':status,
       'candidate_rule_urls':sorted(set(e['url'] for e in candidates)),
       'matching_edge_ids':[e['id'] for e in matches],
       'matching_stages':sorted(set(e['stage'] for e in matches)),
       'matching_positions':sorted(set(e.get('position','any') for e in matches))})
    if len(steps)!=len(states)-1 or not steps:overall='invalid_chain_shape'
    elif any(s['status'] not in ('exact_step_match','multiple_matching_rules') for s in steps):overall='unresolved_steps'
    elif any(s['status']=='multiple_matching_rules' for s in steps):overall='ambiguous_rule_identity'
    else:
     positions=[s['matching_positions'][0] for s in steps]; bounded={p for p in positions if p!='any'}
     stages=[s['matching_stages'][0] for s in steps]
     if len(bounded)>1:overall='incompatible_position'
     elif stages!=sorted(stages):overall='nonmonotone_stages'
     else:overall='graph_steps_verified'
    counter['chain:'+overall]+=1
    result={'id':c['id'],'era':c['era'],'states':states,'overall':overall,'steps':steps,
      'limitation':'Совпадение атомарных правил не доказывает общую этимологию, совместимость контекстов или редакций.'}
    results.append(result)
    if overall!='graph_steps_verified':detail.append({'branch':branch,'corpus':corpus,**result})
   output[corpus]=results;stats[corpus]=dict(sorted(counter.items()))
  (base/'data/chain_step_provenance.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
  summary[branch]=stats
 (ROOT/'reports/chain_step_audit.json').write_text(json.dumps({'summary':summary,'unresolved':detail},ensure_ascii=False,indent=2),encoding='utf8')
 lines=['# Проверка индивидуальных шагов цепочек (v4)','',
  'Аудит строго сопоставляет период, входной и выходной звук и URL конкретного правила с атомарным графом.',
  'Это проверка происхождения данных, **не** доказательство применения всей истории к одной словоформе.','']
 for branch,stats in summary.items():
  lines+=['## '+branch,'']
  for corpus,c in stats.items():
   lines+=['### '+corpus,'']+[f'- `{k}`: {v}' for k,v in c.items()]+['']
 lines+=['Отсутствие шага в атомарном графе означает несоответствие **моделей представления**, не опровержение звукового закона.',
 'Подробности по каждому шагу: `branches/<branch>/data/chain_step_provenance.json`; проблемные случаи: `reports/chain_step_audit.json`.']
 (ROOT/'reports/chain_step_audit.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
