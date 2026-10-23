import csv,collections
from pathlib import Path
from eldamo_interpreter_v3 import apply
P=Path(__file__).resolve().parent
def read(n):return list(csv.DictReader((P/n).open(encoding='utf8')))
paths=read('eldamo_sound_candidate_paths.csv');evidence=read('eldamo_strict_chain_evidence.csv');inv=read('eldamo_v2_all_rules.csv');by=collections.defaultdict(list)
for r in inv:by[(r['rule_url'],r['marker'])].append(r)
formrows=collections.defaultdict(list)
for r in evidence:formrows[int(r['id'])].append(r)
rows=[];totaltest=0;success=0
for i,p in enumerate(paths,1):
 urls=[s.strip() for s in p['rule_urls'].split(' || ')];markers=[s.strip() for s in p['periods'].split('→')];statuses=[];examples=0;verified=0;partial=0;unknown=0;witness=''
 for ev in formrows[i]:
  forms=[s.strip() for s in ev['word_forms'].split('→')]
  if len(forms)!=len(urls)+1:continue
  examples+=1;stepstatus=[]
  for step,(a,b,url,mark) in enumerate(zip(forms,forms[1:],urls,markers)):
   candidates=by.get((url,mark),[])
   statuses=collections.Counter();hit=False
   for c in candidates:
    out,stat=apply(c['from'],c['to'],a)
    statuses[stat]+=1
    if b in out:hit=True;break
   stepstatus.append(('match' if hit else 'no_match') if candidates else 'not_in_inventory')
  if all(x=='match' for x in stepstatus):verified+=1;witness=ev['word_forms'];
  elif 'match' in stepstatus:partial+=1
  if 'not_in_inventory' in stepstatus:unknown+=1
  totaltest+=1
 rows.append({'id':i,'states':p['states'],'periods':p['periods'],'rule_urls':p['rule_urls'],'evidence_sequences_tested':examples,'full_sequences_reproduced_from_linked_rules':verified,'partially_reproduced':partial,'sequences_with_missing_rule_variants':unknown,'witness':witness,'note':'individual rule formulas tested, without independent chronology verification'})
with (P/'eldamo_v3_101_rule_level_audit.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('paths',len(rows),'with linked-rule complete sequence',sum(int(r['full_sequences_reproduced_from_linked_rules'])>0 for r in rows),'tested',totaltest,'with any evidence',sum(int(r['evidence_sequences_tested'])>0 for r in rows))
