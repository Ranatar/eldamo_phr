from pathlib import Path
from playwright.sync_api import sync_playwright
import hashlib, json
root=Path(__file__).resolve().parent
p=(root/'app') if (root/'app').exists() else (root.parent/'app')
if not (p/'standalone.html').exists() and (root.parent/'legacy/eldamo_sound_path_explorer_complete_original.html').exists():
 import shutil
 shutil.copyfile(root.parent/'legacy/eldamo_sound_path_explorer_complete_original.html',p/'standalone.html')
if not (p/'built.html').exists():
 import subprocess,sys
 subprocess.run([sys.executable,str(root/'build_standalone.py')],check=True)
files=['standalone.html','index.html','built.html']
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 results={}
 for filename in files:
  page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda err: errors.append(str(err)))
  html=(p/filename).read_text()
  if filename=='index.html':
   from bs4 import BeautifulSoup
   soup=BeautifulSoup(html,'html.parser')
   for link in soup.find_all('link',href='styles.css'):
    style=soup.new_tag('style');style.string=(p/'styles.css').read_text();link.replace_with(style)
   for tag in soup.find_all('script',src=True):
    js=(p/tag['src']).read_text(); tag.attrs={};tag.string=js
   html=str(soup)
  page.set_content(html,wait_until='load');page.wait_for_timeout(500)
  initial={'title':page.title(),'numbers':page.locator('#numbers').inner_text(),'buttons':page.locator('button').count(),'rules':page.locator('.rule-table').count(),'errors':errors[:],'data':page.evaluate('({edges:EDGES.length,phonemes:PHONEMES.length,rulekeys:Object.keys(RULE_CATALOG).length})')}
  page.screenshot(path=str(p/(filename+'.png')),full_page=True,animations='disabled')
  # rules buttons
  page.locator('#rules-from').click();page.wait_for_timeout(200)
  initial['from_rules']={'count':page.locator('#rule-count').inner_text(),'rows':page.locator('#rule-table tbody tr').count(),'name':page.locator('#rule-title').inner_text()}
  page.locator('#rules-to').click();page.wait_for_timeout(150)
  initial['to_rules']={'count':page.locator('#rule-count').inner_text(),'rows':page.locator('#rule-table tbody tr').count()}
  page.locator('#go').click();page.wait_for_timeout(100)
  initial['bf']=page.locator('#output').inner_text()[:450]
  page.locator('.side[data-slot="to"] .ipa-sound[data-phoneme="v"]').first.click()
  page.locator('#go').click();page.wait_for_timeout(100)
  initial['bv']=page.locator('#output').inner_text()[:450]
  initial['errors_final']=errors
  results[filename]=initial
  page.close()
 browser.close()
 baseline=results['standalone.html']; failures=[]
 for k,v in results.items():
  if k!='standalone.html':
   for field in baseline:
    if v[field]!=baseline[field]:failures.append(f'{k}: {field} mismatch! {repr(v[field])[:150]} / {repr(baseline[field])[:150]}')
 print(json.dumps(results,ensure_ascii=False,indent=2)[:4500]);print('DIFFERENCES',failures)
 assert not failures
 print('PASS parity in headless Chromium')
