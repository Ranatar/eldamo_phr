"""Render IPA-like articulatory navigation in both selection slots."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent.parent
sounds=set(json.loads((P/'data'/'phonemes.json').read_text()))
# Place and manner: schematic IPA placement; some Eldamo historical symbols are broad phonetic representations.
columns=['Губные','Зубные / альвеолярные','Палатальные','Велярные','Гортанные']
consonants=[('Смычные', [['p','b','pʰ'],['t','d','tʰ'],[],['k','g','kʰ'],[]]),('Носовые', [['m','m̥'],['n','n̥'],[],['ŋ'],[]]),('Фрикативные', [['ɸ','β','f','v'],['θ','ð','s','z'],[],['x','ɣ'],['h']]),('Аппроксиманты', [['w','w̥'],['r','r̥','l','l̥'],['j','j̊'],[],[]])]
vowels=[('Верхний подъём',[['i','ī','y','ȳ'],[],['u','ū']]),('Средний подъём',[['e','ē','ø','œ','ę̄'],[],['o','ō','ǭ']]),('Нижний подъём',[['a','ā','ǣ'],[],[]])]
diph=['ai','ei','oi','ui','au','eu','iu','ou','ae','oe','iw']
html=P/'app'/'index.html';s=BeautifulSoup(html.read_text(),'html.parser')
def cell_with_buttons(c,items):
 for p in items:
  if p not in sounds:continue
  btn=s.new_tag('button',attrs={'type':'button','class':'ipa-sound','data-phoneme':p});btn.string=p;c.append(btn)
for slot in ['from','to']:
 node=s.find(id=slot+'-ipa');node.clear()
 sc=s.new_tag('div',attrs={'class':'ipa-scroll'});node.append(sc)
 for title,heads,rows in [('Согласные',['Способ образования']+columns,consonants),('Гласные',['Подъём','Передний ряд','Средний ряд','Задний ряд'],vowels)]:
  h=s.new_tag('h3');h.string=title;sc.append(h)
  table=s.new_tag('table');sc.append(table)
  thead=s.new_tag('thead');table.append(thead);tr=s.new_tag('tr');thead.append(tr)
  for head in heads:th=s.new_tag('th');th.string=head;tr.append(th)
  body=s.new_tag('tbody');table.append(body)
  for title2,cells in rows:
   tr=s.new_tag('tr');body.append(tr);th=s.new_tag('th');th.string=title2;tr.append(th)
   for vals in cells:
    td=s.new_tag('td');tr.append(td);cell_with_buttons(td,vals)
 h=s.new_tag('h3');h.string='Дифтонги и сочетания, выделенные Eldamo в разделе фонем';sc.append(h)
 table=s.new_tag('table');body=s.new_tag('tbody');table.append(body);sc.append(table)
 for i in range(0,len(diph),6):
  tr=s.new_tag('tr');body.append(tr)
  for p in diph[i:i+6]:
   td=s.new_tag('td');tr.append(td);cell_with_buttons(td,[p])
 known={p for group in consonants for cell in group[1] for p in cell} | {p for group in vowels for cell in group[1] for p in cell} | set(diph)
 missing=sorted(sounds-known)
 if missing:
  h=s.new_tag('h3');h.string='Дополнительные обозначения';sc.append(h)
  table=s.new_tag('table');body=s.new_tag('tbody');table.append(body);sc.append(table)
  for i in range(0,len(missing),8):
   tr=s.new_tag('tr');body.append(tr)
   for p in missing[i:i+8]:
    td=s.new_tag('td');tr.append(td);cell_with_buttons(td,[p])
html.write_text(str(s))
print('IPA table',len(sounds),'sounds; additional',len(missing))
