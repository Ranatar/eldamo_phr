from playwright.sync_api import sync_playwright
from pathlib import Path
from hashlib import sha256
P=Path(__file__).resolve().parent.parent/'app'
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 reports=[]
 for mode in ['modular','standalone']:
  page=browser.new_page(viewport={'width':1280,'height':1000}); errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  if mode=='standalone':page.set_content((P/'standalone.html').read_text(),wait_until='load')
  else:
   from bs4 import BeautifulSoup
   html=BeautifulSoup((P/'index.html').read_text(),'html.parser')
   for x in html.find_all('script'):x.decompose()
   for x in html.find_all('link',href='styles.css'):x.decompose()
   st=html.new_tag('style');st.string=(P/'styles.css').read_text();html.head.append(st)
   page.set_content(str(html),wait_until='load')
   for f in ['data.js','chains.js','app.js']:page.add_script_tag(content=(P/f).read_text())
  page.wait_for_timeout(350)
  outputs={'initial':page.locator('body').inner_text()[:500]}
  page.screenshot(path=str(P.parent/'scripts'/f'parity_{mode}.png'))
  # locate rules buttons
  buttons=page.locator('button').all_text_contents();print('actions',mode,[x.strip() for x in buttons if 'Правила' in x or 'Найти' in x][:8])
  rulesbtn=page.locator('button').filter(has_text='Правила исходного')
  if rulesbtn.count():rulesbtn.first.click();outputs['rules']=page.locator('#rule-panel').inner_text()[:900]
  searchbtn=page.locator('button').filter(has_text='Найти пути')
  if searchbtn.count():searchbtn.first.click();outputs['search']=page.locator('#output').inner_text()[:900]
  page.locator('#all-chains').click();outputs['atlas']=page.locator('#atlas-results').inner_text()[:900]
  page.locator('#develop-from').click();outputs['forward']=page.locator('#atlas-results').inner_text()[:900]
  page.locator('#origins-to').click();outputs['backward']=page.locator('#atlas-results').inner_text()[:900]
  outputs['errors']=errors
  reports.append(outputs);page.close()
 print('equal',reports[0]==reports[1]);print('errors',reports[0]['errors']);print('fields',[(k,len(v)) for k,v in reports[0].items()]);print('screens same',sha256((P.parent/'scripts'/'parity_modular.png').read_bytes()).hexdigest()==sha256((P.parent/'scripts'/'parity_standalone.png').read_bytes()).hexdigest())
 assert reports[0]==reports[1] and not reports[0]['errors']
 browser.close()
