"""One evidence-aware graph derivation algorithm for both Eldamo branches.

The atomic adjacency graph deliberately excludes non-atomic contextual rules; these
are not deleted. They remain in rules_full.json and guarded_rules.json, and can be
executed on whole word forms by the shared v3 interpreter. It is incorrect to
represent a context rule as an unconditional sound->sound transition.
"""
from __future__ import annotations
import csv,json,re,collections,sys
from pathlib import Path
from .audit import engine,BASE
BAD=re.compile(r'[\[\]{}|()/₀₁₂₃₄₅₆VCXS_+*?=<>⁺⁻\d\s]')
# Exclude placeholder V/C etc, but retain real IPA e.g. phonemic oe and ø.

def literal_side(text):
 text=text.strip().replace('`','')
 if text.startswith('-') and text.endswith('-'):pos='medial';text=text[1:-1]
 elif text.endswith('-'):pos='initial';text=text[:-1]
 elif text.startswith('-'):pos='final';text=text[1:]
 else:pos='any'
 if not text or text in ('ø','∅') or 'ø' in text or BAD.search(text):return None,pos
 return text,pos

def create(branch):
 root=BASE/'branches'/branch;d=root/'data';app=root/'app'
 # Canonical evidence basis: direct extraction ONLY, identical for both branches.
 # Legacy-expanded variants remain in complete_rules.json but cannot silently seed canonical edges.
 records=json.loads((d/'unified_rules.json').read_text())
 with (d/'unified_semantic_audit.csv').open(newline='') as f:
  audits={(r['era'],r['marker'],r['formula'],r['url'],r['rule']):r for r in csv.DictReader(f)}
 edges=[];guarded=[];seen={}
 for i,r in enumerate(records):
  a,pos_a=literal_side(r['a']);b,pos_b=literal_side(r['b'])
  ev=audits.get((r['era'],r['marker'],r['formula'],r['url'],r['rule']),{})
  attrs={'id':f'{branch}-r{i+1}', 'marker':r['marker'], 'era':r['era'], 'stage':int(r['stage']),
      'rule':r['rule'], 'url':r['url'], 'formula':r['formula'], 'a_formula':r['a'], 'b_formula':r['b'],
      'cards':', '.join(r['catalogs']), 'phonemes':r['sounds'], 'sources':r['refs'],
      'audit':ev.get('validation_status','unverified'), 'tested':int(ev.get('rule_examples_reproduced') or 0)>0,
      'exact':int(ev.get('rule_examples_reproduced') or 0)>0,
      'comment':'', 'cautions':'Результат атомарной проекции. Проверяйте языковую ступень, диалект, историческую редакцию и фонетическое окружение.'}
  reason=[]
  if a is None or b is None:reason.append('complex_or_contextual_formula')
  if pos_a!=pos_b:reason.append('asymmetric_boundary')
  if a==b:reason.append('no_sound_change')
  if reason:
   guarded.append({**attrs,'reason':reason,'a':r['a'],'b':r['b']});continue
  key=(r['era'],r['stage'],r['marker'],a,b,r['url'])
  if key in seen:
   # Several distinct Eldamo records can project to the same atom.
   # Keep every source rule identity, never silently drop their provenance.
   edges[seen[key]]['source_rule_ids'].append(attrs['id'])
   edges[seen[key]]['source_rule_variants'].append({k:attrs[k] for k in ('id','rule','formula','a_formula','b_formula','url','phonemes','sources','audit','tested')})
   continue
  seen[key]=len(edges)
  edges.append({**attrs,'a':a,'b':b,'position':pos_a,
   'source_rule_ids':[attrs['id']],
   'source_rule_variants':[{k:attrs[k] for k in ('id','rule','formula','a_formula','b_formula','url','phonemes','sources','audit','tested')}]})
 # Guarded catalog is completely retained, including all contextual rules.
 (d/'guarded_rules.json').write_text(json.dumps(guarded,ensure_ascii=False,indent=2))
 (d/'atomic_edges_unified.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2))
 # Enumerate all structural candidates depth 2-3, stage-monotone and without cycles.
 adj=collections.defaultdict(list)
 for e in edges:adj[(e['era'],e['a'])].append(e)
 paths=[];sig=set();cutoffs=[]
 for era in ['late','middle']:
  for source in sorted({e['a'] for e in edges if e['era']==era}):
   stack=[(source,[source],[],-1,'any')]
   budget=60000;visited=0
   while stack:
    node,states,steps,last,position=stack.pop();visited+=1
    if visited>budget:
     cutoffs.append([era,source,budget]);break
    if len(steps)>=2:
     key=(era,tuple(states),tuple(e['url'] for e in steps))
     if key not in sig:
      sig.add(key)
      paths.append({'id':f'{branch.upper()}{len(paths)+1}', 'era':era, 'states':states,
             'grade':'unassessed','kind':'new-unassessed','rules':[e['rule'] for e in steps],
             'urls':[e['url'] for e in steps], 'markers':' → '.join(e['marker'] for e in steps),
             'stages':[e['stage'] for e in steps], 'required_position':position, 'evidence':'Не оценена как единая история словоформ.',
             'reason':'Структурно составимая последовательность атомарных правил; совместимость окружений и хронология не установлены.',
             'action':'Проверить применение к одной словоформе, диалект и редакцию концепции.'})
    if len(steps)>=3:continue
    for e in adj[(era,node)]:
     if e['stage']<last or e['b'] in states:continue
     edge_position=e.get('position','any')
     if position!='any' and edge_position!='any' and edge_position!=position:continue
     next_position=edge_position if position=='any' else position
     stack.append((e['b'],states+[e['b']],steps+[e],e['stage'],next_position))
 (d/'unified_structural_chains.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2))
 return {'branch':branch,'all_rules':len(records),'atomic_edges':len(edges),'guarded_rules':len(guarded),'structural_chains':len(paths),'search_truncations':cutoffs}
if __name__=='__main__':
 for b in ['quenya','sindarin']:print(create(b))
