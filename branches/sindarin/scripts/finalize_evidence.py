from pathlib import Path
import json,re,csv,collections
P=Path(__file__).resolve().parent.parent
app=P/'app'
edges=json.loads((app/'edges.json').read_text())
# assessor supplies get_rule_examples; script must not mutate chains on import
import importlib.util
sp=importlib.util.spec_from_file_location('audit',P/'scripts'/'assess_chains.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def normalize(x):return re.sub(r'\s+','',str(x).casefold()).strip('[]')
rows=[]
for e in edges:
 samples=m.get_rule_examples(e['url']) if e['url'] else []
 # Confirm exact same abstract phonetic formula, not merely any example on rule page
 exact=[r for r in samples if normalize(r['formula'])==normalize(e['a']+' > '+e['b'])]
 e['tested']=int(bool(exact));e['exact']=int(any(not r['deleted'] for r in exact))
 rows.append({'period':e['era'],'marker':e['marker'],'rule_url':e['url'],'phonetic_rule':e['a']+' → '+e['b'],'examples_on_page':len(samples),'matching_formula_examples':len(exact),'non_obsolete_matching_examples':sum(not r['deleted'] for r in exact)})
(app/'edges.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2))
(app/'data.js').write_text('window.ELDAMO_EDGES = '+json.dumps(edges,ensure_ascii=False)+';\nwindow.ELDAMO_RULES = '+json.dumps(json.loads((app/'rules.json').read_text()),ensure_ascii=False)+';\n')
with (P/'data'/'atomic_edge_evidence.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Matched step formula examples',sum(e['tested'] for e in edges),'non obsolete',sum(e['exact'] for e in edges))
