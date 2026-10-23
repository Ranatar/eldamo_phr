import sys
sys.path.insert(0,'/mnt/data')
from eldamo_context_interpreter import supports,changes
import pandas as pd,collections
P='/mnt/data/'
atlas=pd.read_csv(P+'eldamo_critical_101_atlas.csv').fillna('')
edges=pd.read_csv(P+'eldamo_sound_edges.csv').fillna('')
evidence=pd.read_csv(P+'eldamo_strict_chain_evidence.csv').fillna('')
edgeindex=collections.defaultdict(list)
for _,r in edges.iterrows():edgeindex[(r['rule_url'],r['from'],r['to'])].append(r)
byid=collections.defaultdict(list)
for _,r in evidence.iterrows():byid[int(r['id'])].append(r)
records=[]; detail=[]
for _,p in atlas.iterrows():
    pid=int(p['id']); states=[x.strip() for x in p['states'].split('→')];urls=[x.strip() for x in p['rule_urls'].split('||')];steps=[]
    for i,(a,b) in enumerate(zip(states,states[1:])):
        options=edgeindex.get((urls[i],a,b),[]) if i<len(urls) else []
        if not options: options=[r for _,r in edges.iterrows() if r['from']==a and r['to']==b and r['rule_url']==(urls[i] if i<len(urls) else '')]
        feasible,why=supports(a,b);steps.append((feasible,why))
    ev=byid[pid]
    form_tests=0; form_success=0; full_word_success=0; held=[]
    for r in ev:
        forms=[x.strip() for x in r['word_forms'].split('→')]
        if len(forms)!=len(states):continue
        matches=[]
        for i,(a,b) in enumerate(zip(states,states[1:])):
            preds,why=changes(a,b,forms[i]);match=forms[i+1] in preds
            if steps[i][0]:form_tests+=1;form_success+=int(match)
            matches.append(match if steps[i][0] else None)
            detail.append(dict(id=pid,formula=f'{a} → {b}',form=f'{forms[i]} → {forms[i+1]}',supported=steps[i][0],matched=match if steps[i][0] else '',source=r['source'],article=r['article']))
        if matches and all(x is True for x in matches):full_word_success+=1;held.append(r['word_forms'])
    status='limited: unsupported constructs' if not all(v for v,_ in steps) else ('compatible with supplied examples' if full_word_success else ('literal mismatch in examples' if form_tests and form_success<form_tests else 'no complete worked example'))
    records.append(dict(id=pid,chain=p['states'],old_grade=p['grade'],step_count=len(steps),supported_steps=sum(x for x,_ in steps),step_coverage=round(sum(x for x,_ in steps)/len(steps),3) if steps else 0,examples=len(ev),tested_step_instances=form_tests,matching_step_instances=form_success,fully_reproduced_example_rows=full_word_success,parser_status=status,unsupported_notes='; '.join(sorted(set(reason for good,reason in steps if not good))),example=' || '.join(held[:3]),rule_urls=p['rule_urls']))
R=pd.DataFrame(records);R.to_csv(P+'eldamo_context_chain_audit.csv',index=False);pd.DataFrame(detail).to_csv(P+'eldamo_context_example_tests.csv',index=False)
print('status:',R.parser_status.value_counts().to_dict());print('supported full chains',sum(R.step_coverage==1),'full reproduced',sum(R.fully_reproduced_example_rows>0));print('examples',len(detail),'matches',sum(x['matched'] is True for x in detail));print('total steps',sum(R.step_count),'covered',sum(R.supported_steps));print('sample',R[R.fully_reproduced_example_rows>0][['id','chain','example']].head(8).to_string(index=False))
