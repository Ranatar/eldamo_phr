from pathlib import Path
import re,json,html,zipfile
P=Path('/mnt/data')
s=(P/'eldamo_sound_path_explorer.html').read_text()
md=(P/'eldamo_six_languages_ipa_catalog.md').read_text()
ph=re.findall(r'^## \[([^\]]+)\]$',md,re.M)
assert len(ph)==61,len(ph)
js_ph=json.dumps(ph,ensure_ascii=False)
nav=md.split('## Навигация по IPA',1)[1].split('\n## [p]',1)[0]
nav=nav.split('> Классификация')[0]
sections=re.split(r'\n### (Согласные|Гласные|Дифтонги)\n',nav)
from markdown_it import MarkdownIt
parser=MarkdownIt('default',{'html':False}).enable('table')
blocks=[]
for i in range(1,len(sections),2):
 name=sections[i]; part=sections[i+1]
 # HTML from markdown with link text [[p]] and href #p
 tbl=parser.render(part)
 tbl=re.sub(r'<a href="#[^"]+">\[([^<]+)\]</a>',lambda m:'<button type="button" class="ipa-sound" data-phoneme="'+html.escape(m.group(1),quote=True)+'">'+html.escape(m.group(1))+'</button>',tbl)
 blocks.append('<h3>'+name+'</h3>'+tbl)
# CSS additions
css='''
.selection-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.side{min-width:0;border:1px solid var(--stroke);border-radius:10px;padding:12px}.side h3{margin:0 0 10px;font-size:16px}.choice-mode{display:flex;gap:7px;margin-bottom:10px}.mode{background:#283e60;color:var(--fg);border:1px solid #536988;padding:8px 10px;font-size:13px;flex:1}.mode.active{background:#9ac7ff;color:#09192d}.current{background:#0b1423;padding:8px 11px;border-radius:7px;margin-bottom:10px;font-size:14px}.current strong{font-size:20px;color:#c7e1ff}.ipa-scroll{max-height:470px;overflow:auto}.ipa-scroll h3{font-size:14px;margin:14px 0 6px}.ipa-scroll table{border-collapse:collapse;width:100%;font-size:12px}.ipa-scroll th,.ipa-scroll td{border:1px solid #405470;padding:6px;vertical-align:middle}.ipa-scroll th{color:#ccdafa;background:#263854}.ipa-sound{background:#293b55;color:#d8eaff;padding:3px 6px;font-size:13px;margin:2px;border:1px solid #4a658b;border-radius:5px;min-width:31px}.ipa-sound:hover{background:#5077ad}.ipa-sound.selected{background:#b9dbff;color:#10243e;outline:2px solid #f2e0a0}.cluster-control{display:none}.cluster-control.active{display:block}.ipa-choice.hidden{display:none}.filter-tip{font-size:12px;color:var(--muted);margin-top:8px}.empty-info{padding:12px;background:#1c2b42;border:1px solid #4b607b;border-radius:8px}.nearby{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0}.nearby button{background:#263f60;color:#dcecff;border:1px solid #526c8e;font-size:13px;padding:5px 10px}@media(max-width:760px){.selection-grid{grid-template-columns:1fr}.ipa-scroll{max-height:340px}}
'''
s=s.replace('</style>',css+'</style>')
a=s.index('<div class="controls">')
b=s.index('<div class="row"><label><input type="checkbox" id="stage"',a)
selection='''<div class="selection-grid">'''
for slot,label,default in [('from','Исходное состояние','b'),('to','Целевое состояние','f')]:
 selection+=f'''<div class="side" data-slot="{slot}"><h3>{label}</h3><div class="choice-mode"><button type="button" class="mode active" data-slot="{slot}" data-mode="phoneme">Отдельная фонема</button><button type="button" class="mode" data-slot="{slot}" data-mode="cluster">Сочетание</button></div><div class="current">Выбрано: <strong id="{slot}-chosen">{default}</strong></div><div class="ipa-choice" id="{slot}-ipa"><div class="ipa-scroll">{''.join(blocks)}</div></div><div class="cluster-control" id="{slot}-cluster"><label>Первая фонема сочетания<select id="{slot}-first"></select></label><label>Сочетание<select id="{slot}-combo"></select></label><div class="filter-tip">В списке только сочетания, присутствующие в индексированных преобразованиях. Для незнакомых сочетаний нужен полноценный анализ словоформ.</div></div></div>'''
selection+='''</div><div class="controls" style="margin-top:14px"><label>Период разработки Толкина<select id="era"><option value="late">Поздняя концепция (✶, AQ., Q.)</option><option value="middle">Средняя концепция (ᴹ✶, ᴹAQ., ᴹQ.)</option></select></label><label>Максимальное число переходов<select id="depth"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option></select></label></div>'''
s=s[:a]+selection+s[b:]
# Remove datalist prior initialization but retain embedded DATA
s=s.replace('const states=Array.from(new Set(EDGES.flatMap(e=>[e.a,e.b]))).sort((a,b)=>a.localeCompare(b));\n\'$(' ,'const states=Array.from(new Set(EDGES.flatMap(e=>[e.a,e.b]))).sort((a,b)=>a.localeCompare(b));\n\'$(') if False else s
s=re.sub(r"\$\('sounds'\)\.innerHTML=.*?\.join\(''\);",'',s)
anchor="$('numbers').textContent=`${EDGES.length} атомарных переходов · ${states.length} звуковых состояний`;"
ui='''
const PHONEMES=__PHONEMES__;
const PHSET=new Set(PHONEMES);
const compound=states.filter(s=>!PHSET.has(s) && s.length>1 && !/[{}|VCS_+*?⁺⁻₁₂₃\\[\\]()]/.test(s));
const vals={from:'b',to:'f'}, modes={from:'phoneme',to:'phoneme'};
function selectState(slot,val){vals[slot]=val;$(slot+'-chosen').textContent=val;document.querySelectorAll('.side[data-slot="'+slot+'"] .ipa-sound').forEach(b=>b.classList.toggle('selected',modes[slot]==='phoneme'&&b.dataset.phoneme===val));}
function fillCombos(slot){let first=$(slot+'-first').value;let opts=compound.filter(s=>s.startsWith(first));let sel=$(slot+'-combo');sel.replaceChildren(...opts.map(s=>new Option(s,s)));if(opts.length){selectState(slot,opts[0]);sel.disabled=false}else{sel.disabled=true;selectState(slot,'');}}
function setMode(slot,mode){modes[slot]=mode;document.querySelectorAll('.mode[data-slot="'+slot+'"]').forEach(x=>x.classList.toggle('active',x.dataset.mode===mode));$(slot+'-ipa').classList.toggle('hidden',mode!=='phoneme');$(slot+'-cluster').classList.toggle('active',mode==='cluster');if(mode==='cluster'){fillCombos(slot)}else{selectState(slot,PHSET.has(vals[slot])?vals[slot]:'b')}}
for(const slot of ['from','to']){
 const firsts=[...new Set(compound.map(s=>PHONEMES.filter(p=>s.startsWith(p)).sort((a,b)=>b.length-a.length)[0]).filter(Boolean))];
 $(slot+'-first').replaceChildren(...firsts.map(s=>new Option(s,s)));
 $(slot+'-first').addEventListener('change',()=>fillCombos(slot));
 $(slot+'-combo').addEventListener('change',()=>selectState(slot,$(slot+'-combo').value));
 document.querySelectorAll('.side[data-slot="'+slot+'"]').forEach(c=>c.addEventListener('click',e=>{const b=e.target.closest('.ipa-sound');if(b){selectState(slot,b.dataset.phoneme)}}));
 setMode(slot,'phoneme');
}
document.querySelectorAll('.mode').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.slot,b.dataset.mode)));
'''.replace('__PHONEMES__',js_ph)
s=s.replace(anchor,anchor+ui)
s=s.replace("const src=$('from').value.trim(),dst=$('to').value.trim()","const src=vals.from.trim(),dst=vals.to.trim()")
old="if(!found.length){out.innerHTML='<p>Путей в выбранной проекции не найдено. Это <strong>не опровержение</strong> исторической возможности: попробуйте увеличить глубину, снять фильтр примеров или проверить контекстные правила в полном каталоге.</p>'+(truncated?'<p class=\"warn\">Поиск ограничен по числу перебираемых состояний.</p>':'');return}"
new="""if(!found.length){
 const reached=new Map([[src,0]]),pending=[src];for(let k=0;k<pending.length&&k<500;k++){let u=pending[k];if(reached.get(u)>=maxD)continue;for(const e of adj.get(u)||[]){if(!reached.has(e.b)){reached.set(e.b,reached.get(u)+1);pending.push(e.b)}}}
 const near=[...reached].filter(([v])=>v!==src).sort((a,b)=>a[1]-b[1]).slice(0,14);
 const incoming=EDGES.filter(e=>e.b===dst&&e.era===era).map(e=>e.a).filter((v,i,a)=>a.indexOf(v)===i).slice(0,14);
 out.innerHTML='<div class=\"empty-info\"><strong>В выбранных правилах нет пути '+safe(src)+' → '+safe(dst)+'.</strong><p>Это не ошибка поиска и не доказательство невозможности развития. Поиск соединяет только документированные в индексе атомарные переходы и не подменяет один звук другим.</p><div>Из '+safe(src)+' достижимы (без учёта ограничения порядка ступеней):</div><div class=\"nearby\">'+near.map(([v,n])=>'<button type=\"button\" data-near=\"'+safe(v)+'\">'+safe(v)+' · '+n+' шаг(а)</button>').join('')+'</div><div>Непосредственно к '+safe(dst)+' ведут: '+(incoming.map(safe).join(', ')||'в этом периоде нет входящих переходов')+'</div><p class=\"muted\">'+(src==='b'&&dst==='f'?'Для b каталог содержит b → β → v, а не b → f; f образуется, например, из ɸ. Для b → f нет соединяющего правила в индексированной выборке.':'Проверяйте также период, последовательность ступеней и полные контекстные формулы в каталоге.')+'</p></div>'+(truncated?'<p class=\"warn\">Поиск ограничен по числу перебираемых состояний.</p>':'');out.querySelectorAll('[data-near]').forEach(b=>b.addEventListener('click',()=>{setMode('to','phoneme');selectState('to',b.dataset.near);find()}));return} """
assert old in s
s=s.replace(old,new)
# replace swap handler and keydown handlers
s=re.sub(r"\$\('swap'\)\.addEventListener\('click',.*?;find\(\);</script>","$('swap').addEventListener('click',()=>{const a=vals.from,b=vals.to;setMode('from',PHSET.has(b)?'phoneme':'cluster');setMode('to',PHSET.has(a)?'phoneme':'cluster');selectState('from',b);selectState('to',a);find()});find();</script>",s,flags=re.S)
assert 'const PHONEMES=' in s and 'id="from-first"' in s
(P/'eldamo_sound_path_explorer_ipa.html').write_text(s)
# update archive
source=P/'eldamo_integrated_research_package.zip'
target=P/'eldamo_integrated_research_package_ipa.zip'
with zipfile.ZipFile(source) as zin,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as zout:
 for item in zin.infolist():
  if item.filename=='eldamo_sound_path_explorer.html':zout.writestr(item.filename,s.encode('utf8'))
  else:zout.writestr(item,zin.read(item.filename))
 zout.write(P/'update_eldamo_explorer_ipa.py',arcname='update_eldamo_explorer_ipa.py')
print('written',target.stat().st_size,'phonemes',len(ph),'combos',len(re.findall('data-phoneme',s)))
