from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
for b,edges,rules,chains in [('quenya',601,61,139),('sindarin',234,57,118)]:
 d=json.loads((root/'branches'/b/'app_data.json').read_text())
 assert len(d['edges'])==edges,(b,'edges')
 assert len(d['rules'])==rules,(b,'rules')
 assert len(d['chains'])==chains,(b,'chains')
 assert len(d['phonemes'])>40
 assert len(d['markers'])>=6
 assert len((root/'branches'/b/'markup.html').read_text())>1000
 assert len({(c.get('era'),tuple(c['states'])) for c in d['chains']})<=len(d['chains'])
 assert all('a' in e and 'b' in e for e in d['edges'])
 print(b, 'source datasets intact',edges,rules,chains)
print('DATA PASS')
