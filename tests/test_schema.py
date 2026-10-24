from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]
for b in ('quenya','sindarin'):
 app=json.loads((p/'branches'/b/'app_data.json').read_text())
 edges=json.loads((p/'branches'/b/'data/edges_common_schema.json').read_text())
 rules=json.loads((p/'branches'/b/'data/rules_common_schema.json').read_text())
 assert len(edges)==len(app['edges'])
 assert [e['original'] for e in edges]==app['edges']
 assert len(rules)==sum(map(len,app['rules'].values()))
 for rr in rules:assert rr['original'] in app['rules'][rr['phoneme']]
 print(b,'lossless edge and rule schema PASS')
