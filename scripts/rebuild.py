from pathlib import Path
import json,hashlib,csv,zipfile
root=Path(__file__).resolve().parents[1]
branches={}
for name in ('quenya','sindarin'):
    b=root/'branches'/name/'app'
    previous=json.loads((root/'branches'/name/'app_data.json').read_text(encoding='utf8'))
    # Source-of-truth is branch JSON plus the extracted legacy HTML markup.
    for field,file in [('edges','edges.json'),('rules','rules.json'),('chains','chains.json')]:
        previous[field]=json.loads((b/file).read_text(encoding='utf8'))
    # Preserve stage configuration, phoneme inventory and original markup verbatim.
    previous['markup']=(root/'branches'/name/'markup.html').read_text(encoding='utf8')
    # The path explorer and canonical atlas must use the SAME shared atomic graph.
    previous['edges']=json.loads((root/'branches'/name/'data/atomic_edges_unified.json').read_text(encoding='utf8'))
    previous['research_chains']=json.loads((root/'branches'/name/'data/research_chains_for_app.json').read_text(encoding='utf8'))
    previous['provenance']=json.loads((root/'branches'/name/'data/chain_step_provenance.json').read_text(encoding='utf8'))
    branches[name]=previous
html=(root/'app/template.html').read_text(encoding='utf8').replace('__BRANCHES__',json.dumps(branches,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__RUNTIME__',(root/'app/runtime.js').read_text(encoding='utf8'))
(root/'app/index.html').write_text(html,encoding='utf8')
print('Rebuilt',root/'app/index.html')
