from pathlib import Path
import json,re
base=Path(__file__).resolve().parent.parent
p=base/'app'
e=json.loads((p/'edges.json').read_text());c=json.loads((p/'chains.json').read_text());r=json.loads((p/'rules.json').read_text())
assert e and c and r
assert set(x['era'] for x in e)=={'late','middle'}
assert all(x['grade'] in {'C','D','U'} for x in c)
assert not any(x['marker'] in ['T.','ᴹT.','ᴱQ.'] for x in e)
assert all(x['url'].startswith('https://eldamo.org/content/') for x in e if x['url'])
assert all(len(x['states'])>=3 and len(x['urls'])==len(x['states'])-1 for x in c)
html=(p/'standalone.html').read_text()
for s in ['ELDAMO_EDGES','ELDAMO_RULES','ELDAMO_CHAINS','Развитие исходного звука','Происхождение конечного звука']:
 assert s in html,s
print('PASS',len(e),'edges',len(c),'candidate chains',len(r),'sound entries')
