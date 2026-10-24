"""Every canonical source rule must be accounted for exactly once, even if projections coincide."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
for branch in ('quenya','sindarin'):
 d=ROOT/'branches'/branch/'data'
 rules=json.loads((d/'unified_rules.json').read_text('utf-8'))
 edges=json.loads((d/'atomic_edges_unified.json').read_text('utf-8'))
 guarded=json.loads((d/'guarded_rules.json').read_text('utf-8'))
 audit=list(csv.DictReader((d/'unified_semantic_audit.csv').open(encoding='utf-8',newline='')))
 assert len(audit)==len(rules)
 identity=[]
 for e in edges:
  ids=e['source_rule_ids'];variants=e['source_rule_variants']
  assert len(ids)==len(variants) and ids[0]==e['id']
  for rid,variant in zip(ids,variants):
   assert rid==variant['id']
   i=int(rid.rsplit('-r',1)[-1])-1
   assert (variant['formula'],variant['url'],variant['rule'])==(rules[i]['formula'],rules[i]['url'],rules[i]['rule'])
   identity.append(rid)
 identity.extend(g['id'] for g in guarded)
 expected={f'{branch}-r{i}' for i in range(1,len(rules)+1)}
 assert len(identity)==len(rules) and set(identity)==expected
 assert len(set(identity))==len(identity)
 print(branch,'PASS',len(rules),'source identities; merged',sum(len(e['source_rule_ids'])-1 for e in edges))
