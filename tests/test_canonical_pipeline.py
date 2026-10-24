"""Fail if canonical interface data differs from the shared research pipeline."""
import json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
for branch in ('quenya','sindarin'):
 d=ROOT/'branches'/branch/'data'
 derived=json.loads((d/'unified_assessed_chains.json').read_text())
 app=json.loads((d/'research_chains_for_app.json').read_text())
 assert len(derived)==len(app)
 assert len({c['id'] for c in derived})==len(derived)
 for i,(drow,row) in enumerate(zip(derived,app)):
  assert row['provenance_corpus']=='canonical_shared_pipeline'
  for key,value in drow.items():assert row[key]==value,(branch,i,key)
 edges=json.loads((d/'atomic_edges_unified.json').read_text())
 idx={(e['era'],e['a'],e['b'],e['url'],e['stage'],e['marker']) for e in edges}
 for c in derived:
  assert len(c['urls'])==len(c['states'])-1==len(c['stages']),c['id']
  for i,url in enumerate(c['urls']):
   marker=c['markers'].split(' → ')[i]
   signature=(c['era'],c['states'][i],c['states'][i+1],url,c['stages'][i],marker)
   assert signature in idx,(branch,c['id'],signature)
 print(branch,'canonical rows:',len(app),'grades',dict(Counter(x['grade'] for x in app)),'atomic edges',len(edges))
print('canonical pipeline invariants OK')
