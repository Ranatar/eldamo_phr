from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
base=Path(__file__).resolve().parents[1]
pagefile=base/'app/index.html'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--allow-file-access-from-files'])
 page=browser.new_page(viewport={'width':1280,'height':1000})
 errors=[]
 page.on('pageerror',lambda exc:errors.append(str(exc)))
 page.set_content(pagefile.read_text(encoding="utf8"), wait_until="load")
 assert page.locator('[data-load]').count()==2
 for branch,count in [('quenya','391'),('sindarin','234')]:
  page.locator(f'[data-load="{branch}"]').click()
  print('loaded',branch, 'numbers=',page.locator('#numbers').inner_text()[:120], 'errors',errors)
  assert count in page.locator('#numbers').inner_text()
  assert page.locator('.ipa-sound').count()>20
  # actual display rules
  for label in ['#rules-from','#rules-to']:
   if page.locator(label).count():page.locator(label).click()
  page.locator('#go').click()
  assert page.locator('#results').count() or page.locator('#output').count()
  page.locator('#all-chains').click()
  print('atlas',page.locator('#atlas-count').inner_text()[:120])
  assert 'цепоч' in page.locator('#atlas-count').inner_text()
  page.locator('#develop-from').click()
  assert 'Развитие' in page.locator('#atlas-count').inner_text()
  page.locator('#origins-to').click()
  assert 'Происхождение' in page.locator('#atlas-count').inner_text()
  page.locator('#branch-home').click()
 assert not errors,errors
 browser.close()
print('PASS')
