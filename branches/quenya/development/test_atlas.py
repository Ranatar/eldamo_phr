from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 for name in ['app/index.html','app/built.html']:
  page=browser.new_page(viewport={'width':1280,'height':1000})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  import re
  html=(root/name).read_text(encoding='utf-8')
  html=re.sub(r'<script[^>]*src="[^"]+"[^>]*>\s*</script>', '', html)
  page.set_content(html,wait_until='load')
  if name.endswith('index.html'):
   for script in ['data.js','chains.js','app.js']:
    page.add_script_tag(content=(root/'app'/script).read_text(encoding='utf-8'))
  page.wait_for_timeout(400)
  assert page.locator('#atlas-count').inner_text().startswith('87 '),(name,page.locator('#atlas-count').inner_text())
  assert page.locator('#atlas-results .atlas-card').count()==20
  page.locator('#atlas-grade').select_option('B')
  assert page.locator('#atlas-results .atlas-card').count()>0
  page.locator('#atlas-grade').select_option('all')
  page.locator('#develop-from').click()
  assert 'Развитие от' in page.locator('#atlas-count').inner_text()
  page.locator('#origins-to').click()
  assert 'Происхождение' in page.locator('#atlas-count').inner_text()
  page.locator('#all-chains').click()
  page.locator('#rules-from').click()
  assert not page.locator('#rule-panel').is_hidden()
  page.locator('#go').click()
  assert 'нет пути' in page.locator('#output').inner_text()
  assert not errors,(name,errors)
  print(name,'PASS',page.locator('#atlas-count').inner_text())
  page.close()
 browser.close()
