"""Build standalone Eldamo explorer with per-state rule view from the catalog.
Run: python build_eldamo_rules_ui.py
"""
import re,json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=(ROOT/'eldamo_sound_path_explorer_ipa.html').read_text(encoding='utf8')
md=(ROOT/'eldamo_six_languages_ipa_catalog.md').read_text(encoding='utf8')
sections=re.split(r'(?m)^## \[([^\]\n]+)\]\s*$',md)
rule_map={}
for i in range(1,len(sections),2):
    phon,body=sections[i:i+2]
    lines=body.splitlines(); entries=[];seen=set()
    for line in lines:
        if not line.startswith('| ') or line.startswith('| ---') or line.startswith('| Маркер'):continue
        cols=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(cols)!=7:continue
        marker,title,formula,langs,linked,cards,sources=cols
        formula=formula.strip('`')
        def markdown_text(t):
            return re.sub(r'\\([\[\]])',r'\1',re.sub(r'\[([^\]]*(?:\\\][^\]]*)*)\]\((https?://[^\s)]+)\)',r'\1',t))
        match=re.search(r'\]\((https?://[^\s)]+)\)',title)
        url=match.group(1) if match else ''
        label=markdown_text(title)
        refs=re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',sources)
        key=(marker,formula,url,langs)
        if key in seen:continue
        seen.add(key)
        entries.append({'marker':marker,'title':label,'url':url,'formula':formula,'langs':langs,'sources':refs,'linked':re.findall(r'\[\[([^\]]+)\]\]',linked)})
    rule_map[phon]=entries
assert len(rule_map)>=55,(len(rule_map),list(rule_map))
# add distinct action buttons for from/to
needle='<button id="go">Найти пути</button>'
assert needle in src
src=src.replace(needle,needle+'<button id="rules-from" class="secondary-action" type="button">Правила исходного звука</button><button id="rules-to" class="secondary-action" type="button">Правила конечного звука</button>')
needle='<section class="panel"><h2>Найденные цепочки</h2>'
assert needle in src
src=src.replace(needle,'<section class="panel" id="rule-panel" hidden><h2 id="rule-title">Правила выбранного состояния</h2><div class="stats" id="rule-count"></div><div id="rule-table"></div></section>'+needle)
needle='</style>'
css='''
.secondary-action{background:#2c4366;color:#e5efff;border:1px solid #647993}
.rule-scroll{overflow-x:auto;margin-top:12px}.rule-table{width:100%;border-collapse:collapse;font-size:13px;min-width:650px}.rule-table th,.rule-table td{padding:9px 10px;text-align:left;vertical-align:top;border-bottom:1px solid #405470}.rule-table th{background:#243750;position:sticky;top:0}.rule-table td:first-child{white-space:nowrap}.rule-table .refs{font-size:12px}.rule-note{margin-top:12px;color:#b5c6dc}
'''
src=src.replace(needle,css+needle)
# embedded index, shown exactly as grouped on phoneme pages, no assumptions about cluster membership
insert='''
const RULE_CATALOG=__DATA__;
function showRules(slot){
 const selection=vals[slot]; const panel=$('rule-panel');panel.hidden=false;
 $('rule-title').textContent='Фонетические правила: ['+selection+']';
 const matching=RULE_CATALOG[selection]||[];
 const isCluster=!PHSET.has(selection);
 // For clusters use exact matching at either side of an attested formula; do not infer from unrelated constituent rules.
 const norm=s=>s.replace(/^-|-$/g,'').trim();
 const records=isCluster?Object.values(RULE_CATALOG).flat().filter(r=>{
   const parts=r.formula.split(/→|←/);return parts.length===2&&parts.some(p=>norm(p.replace(/`/g,''))===selection);
 }):matching;
 const uniq=[];const seen=new Set();
 for(const r of records){const k=[r.marker,r.title,r.formula,r.url,r.langs].join('\\u001f');if(!seen.has(k)){seen.add(k);uniq.push(r)}}
 const ranking={'Q.':0,'ᴹQ.':1,'AQ.':2,'ᴹAQ.':3,'✶':4,'ᴹ✶':5};
 uniq.sort((a,b)=>(ranking[a.marker]??99)-(ranking[b.marker]??99)||a.formula.localeCompare(b.formula));
 $('rule-count').textContent=uniq.length+' записей по каталогу Eldamo 0.8.13'+(isCluster?' (строгое совпадение всей комбинации в формуле)':'');
 if(!uniq.length){$('rule-table').innerHTML='<div class="empty-info">Для этого выбора нет отдельной записи в каталоге. Это не доказывает отсутствие контекстных преобразований в целом.</div>';return}
 const cells=uniq.map(r=>'<tr><td>'+safe(r.marker)+'</td><td>'+(r.url?'<a href="'+safe(r.url)+'" target="_blank" rel="noopener">'+safe(r.title)+'</a>':safe(r.title))+'</td><td><code>'+safe(r.formula)+'</code></td><td>'+safe(r.langs)+'</td><td class="refs">'+r.sources.map(x=>'<a href="'+safe(x[1])+'" target="_blank" rel="noopener">'+safe(x[0])+'</a>').join(' · ')+'</td></tr>').join('');
 $('rule-table').innerHTML='<div class="rule-scroll"><table class="rule-table"><thead><tr><th>Период</th><th>Правило</th><th>Формула</th><th>Языковые карточки</th><th>Источники</th></tr></thead><tbody>'+cells+'</tbody></table></div><p class="rule-note">Это записи из полного каталога фонем. Для сочетаний показываются формулы с точно совпадающей комбинацией, без подмены правилами отдельных составляющих.</p>';
 panel.scrollIntoView({behavior:'smooth',block:'start'});
}
$('rules-from').addEventListener('click',()=>showRules('from'));
$('rules-to').addEventListener('click',()=>showRules('to'));
'''.replace('__DATA__',json.dumps(rule_map,ensure_ascii=False,separators=(',',':')))
needle="$('go').addEventListener('click',find);"
assert needle in src
src=src.replace(needle,insert+'\n'+needle)
out=ROOT/'eldamo_sound_path_explorer_complete.html';out.write_text(src,encoding='utf8')
print('written',out,'phonemes',len(rule_map),'rows',sum(map(len,rule_map.values())))
