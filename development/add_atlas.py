from pathlib import Path
import csv,json
root=Path(__file__).resolve().parents[1]; app=root/'app'
source=root/'data'
def read(name):
 with (source/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
critical=read('eldamo_critical_101_atlas.csv')
structural=read('eldamo_v3_rebuilt_structural_graph.csv')
items=[]
for r in critical:
 items.append({'id':'C'+r['id'],'states':r['states'].split(' → '),'era':r['era'],'grade':r['grade'],'kind':'assessed','markers':'','evidence':r['example'],'reason':r['reason'],'action':r['action'],'sources':r['source'],'rules':r['rules'].split(' || '),'urls':r['rule_urls'].split(' || '),'language':r['languages'],'previous':r['previous_status']})
# Don't downgrade evaluated items; structural matches may be listed in both and are kept only in reviewed version
existing={(tuple(x['states']),x['era']) for x in items}
for i,r in enumerate(structural,1):
 nodes=r['states'].split(' → ')
 if (tuple(nodes),r['era']) in existing: continue
 items.append({'id':'S'+str(i),'states':nodes,'era':r['era'],'grade':'—','kind':'structural','markers':r['markers'],'evidence':'','reason':'Структурный кандидат: общая последовательность словоформ и все ограничения пока не проверены.','action':'Проверить окружение, хронологию и словарные примеры каждого шага.','sources':'','rules':[],'urls':r['rule_urls'].split(' || '),'language':'','previous':r['status'],'supported':r['example_supported_steps'],'exact':r['exact_formula_supported_steps']})
(app/'chains.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
(app/'chains.js').write_text('window.ELDAMO_CHAINS = '+json.dumps(items,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
html=(app/'index.html').read_text(encoding='utf-8')
anchor='   <section class="panel">\n    <h2>\n     О достоверности'
if 'id="chain-atlas"' in html:
 print('Atlas markup already present; keeping it unchanged')
 return_dummy = True
else:
 return_dummy = False
assert anchor in html or return_dummy
insert='''   <section class="panel" id="chain-atlas">
    <h2>Атлас цепочек</h2>
    <p class="muted">101 предварительно оценённая цепочка и дополнительные структурные кандидаты. Оценка относится к целой цепочке, а не к отдельной стрелке. «Не оценена» — не категория U.</p>
    <div class="row">
     <button type="button" id="all-chains">Все цепочки</button>
     <button type="button" class="secondary-action" id="develop-from">Развитие исходного звука</button>
     <button type="button" class="secondary-action" id="origins-to">Происхождение конечного звука</button>
    </div>
    <div class="controls atlas-filters">
     <label>Степень обоснованности<select id="atlas-grade"><option value="all">Все категории</option><option value="A">A — непосредственно подтверждена</option><option value="B">B — хорошо обоснована</option><option value="C">C — частично обоснована</option><option value="D">D — формально возможна</option><option value="U">U — недостаточно данных</option><option value="X">X — противоречива</option><option value="—">Не оценена</option></select></label>
     <label>Поиск по цепочке<input id="atlas-query" placeholder="Например pʰ, ɸ или pt" /></label>
    </div>
    <div class="row"><label><input id="atlas-period" type="checkbox" checked /> Учитывать выбранный период</label><label><input id="atlas-stage" type="checkbox" checked /> Соблюдать порядок языковых ступеней для деревьев</label></div>
    <div class="stats" id="atlas-count"></div>
    <div id="atlas-results" aria-live="polite"></div>
   </section>
'''
if not return_dummy: html=html.replace(anchor,insert+anchor)
if 'src="chains.js"' not in html: html=html.replace('<script defer="" src="app.js">', '<script defer="" src="chains.js"></script>\n  <script defer="" src="app.js">')
(app/'index.html').write_text(html,encoding='utf-8')
css=(app/'styles.css').read_text(encoding='utf-8')
if '/* Expandable chain atlas' not in css: css+='''\n/* Expandable chain atlas and contextual development trees */
.atlas-filters{margin-top:14px}.atlas-card{border:1px solid var(--stroke);border-radius:10px;margin:9px 0;padding:12px;background:#111d30}.atlas-card summary{cursor:pointer;font-weight:600}.atlas-card summary:hover{color:var(--accent)}.atlas-route{overflow-wrap:anywhere}.atlas-grade{display:inline-block;border:1px solid #697b94;border-radius:5px;padding:1px 7px;margin-left:8px;font-size:12px;color:#cbd9ed}.atlas-meta{font-size:12px;color:var(--muted);margin:8px 0}.atlas-card ol{padding-left:23px}.atlas-card li{margin:6px 0}.atlas-link{display:inline-block;margin:4px 8px 4px 0}.atlas-pager{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:15px}.atlas-pager button{background:#2c4366;color:#e5efff}.atlas-tree-group{margin:12px 0 20px;border-left:2px solid #587298;padding-left:13px}.atlas-tree-group h3{margin:7px 0}.atlas-tree-route{padding:7px 9px;margin:5px 0;background:#1e3049;border-radius:7px;overflow-wrap:anywhere}.atlas-status{font-size:12px;color:#aec4dd}.atlas-note{padding:9px;background:#26374c;border-radius:7px;margin:10px 0}
'''
(app/'styles.css').write_text(css,encoding='utf-8')
print('Atlas entries',len(items),'reviewed',len(critical),'structural extras',len(items)-len(critical))
