import csv,collections,re
from pathlib import Path
from eldamo_interpreter_v3 import parse,split_top
P=Path(__file__).resolve().parent
def load(n):return list(csv.DictReader((P/n).open(encoding='utf8')))
rows=load('eldamo_v2_all_rules.csv');checks=load('eldamo_v3_rule_example_validation.csv')
check={(r['marker'],r['from'],r['to'],r['rule_url']):r for r in checks}

def alts(a,b):
 aa=split_top(a);bb=split_top(b)
 if len(aa)!=len(bb):return []
 final=[]
 for x,y in zip(aa,bb):
  try:xpat,xini,xfin,xmed=parse(x);ypat,yini,yfin,ymed=parse(y)
  except Exception:continue
  if (xini,xfin,xmed)!=(yini,yfin,ymed) or len(xpat)!=len(ypat):continue
  n=max([len(opts) for opts,_ in xpat+ypat]+[1]);
  for i in range(n):
   aout=[];bout=[];ok=True
   for (p,idx),(q,jdx) in zip(xpat,ypat):
    pp=p[i] if len(p)==n else p[0] if len(p)==1 else None
    qq=q[i] if len(q)==n else q[0] if len(q)==1 else None
    if not pp or not qq or pp in ('V','V̄','V̆','C','S','X','ø') or qq in ('V','V̄','V̆','C','S','X','ø') or idx or jdx:ok=False;break
    aout.append(pp);bout.append(qq)
   if ok:final.append((''.join(aout),''.join(bout)))
 return list(dict.fromkeys(final))

atomic=[]
for r in rows:
 k=(r['marker'],r['from'],r['to'],r['rule_url']);ev=check.get(k,{})
 for a,b in alts(r['from'],r['to']):
  if a==b or not a or not b:continue
  atomic.append({'marker':r['marker'],'from':a,'to':b,'rule_url':r['rule_url'],'evidence':ev.get('status','unknown'),'matched':ev.get('matching_example_rows','0'),'formula_matched':ev.get('exact_formula_matches','0')})
cands=load('eldamo_new_atomic_candidates.csv')
lookup=collections.defaultdict(list)
for a in atomic:lookup[(a['marker'],a['from'],a['to'])].append(a)
audit=[]
for i,c in enumerate(cands,1):
 states=[x.strip() for x in c['states'].split('→')];marks=[x.strip() for x in c['markers'].split('→')]
 steps=[lookup.get((m,a,b),[]) for m,a,b in zip(marks,states,states[1:])]
 audit.append({'id':i,'states':c['states'],'markers':c['markers'],'identified_steps':sum(bool(x) for x in steps),'total_steps':len(steps),'fully_identified':all(steps),'steps_with_matching_page_examples':sum(any(int(e['matched'])>0 for e in group) for group in steps),'every_step_has_page_example':all(any(int(e['matched'])>0 for e in group) for group in steps),'evidence_rule_urls':' || '.join(';'.join(sorted({x['rule_url'] for x in group if x['rule_url']})) for group in steps),'status':'structural only; no full form chain attested here'})
with (P/'eldamo_v3_27_normalized_reassessment.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=audit[0].keys());w.writeheader();w.writerows(audit)
print('atomic expanded',len(atomic),'fully identified new27',sum(x['fully_identified'] for x in audit),'all edges example supported',sum(x['every_step_has_page_example'] for x in audit))
# Rebuild a separate atomic graph: preserve concept-era and in-world stage constraints.
period={'✶':('late',0),'AQ.':('late',1),'Q.':('late',2),'ᴹ✶':('middle',0),'ᴹAQ.':('middle',1),'ᴹQ.':('middle',2)}
lookup2=collections.defaultdict(list)
for edge in atomic:
 if edge['marker'] not in period:continue
 era,stage=period[edge['marker']];edge['era']=era;edge['stage']=stage
 lookup2[(era,edge['from'])].append(edge)
paths={}
for origin in atomic:
 if origin['marker'] not in period:continue
 for nextedge in lookup2[(origin['era'],origin['to'])]:
  if nextedge['stage']<=origin['stage']:continue
  p=[origin,nextedge];key=tuple((e['marker'],e['from'],e['to'],e['rule_url']) for e in p)
  paths[key]=p
  for third in lookup2[(origin['era'],nextedge['to'])]:
   if third['stage']<=nextedge['stage']:continue
   path=[origin,nextedge,third];key=tuple((e['marker'],e['from'],e['to'],e['rule_url']) for e in path);paths[key]=path
res=[]
for p in paths.values():
 res.append({'states':' → '.join([p[0]['from']]+[e['to'] for e in p]),'markers':' → '.join(e['marker'] for e in p),'era':p[0]['era'],'rule_urls':' || '.join(e['rule_url'] for e in p),'example_supported_steps':sum(int(e['matched'])>0 for e in p),'exact_formula_supported_steps':sum(int(e['formula_matched'])>0 for e in p),'steps':len(p),'status':'structural candidate — no full-word sequential proof'})
with (P/'eldamo_v3_rebuilt_structural_graph.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=res[0].keys());w.writeheader();w.writerows(res)
print('rebuilt structural',len(res),'all steps have example',sum(x['example_supported_steps']==x['steps'] for x in res),'all steps exact',sum(x['exact_formula_supported_steps']==x['steps'] for x in res))
