from pathlib import Path
from playwright.sync_api import sync_playwright
import re, hashlib
r=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 shots=[];outputs=[]
 for name in ['legacy/eldamo_sound_path_explorer_complete_original.html','app/built.html']:
  page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
  page.set_content((r/name).read_text(),wait_until='load')
  page.wait_for_timeout(300)
  shots.append(page.screenshot())
  page.locator('#go').click()
  outputs.append(page.locator('#output').inner_text())
  page.locator('#rules-from').click()
  outputs.append((page.locator('#rule-count').inner_text(),page.locator('#rule-table').inner_text()[:500]))
  page.close()
 print('Original/top UI screenshot pixel identical:',shots[0]==shots[1]); print('Search identical:',outputs[0]==outputs[2]); print('Rule view identical:',outputs[1]==outputs[3])
 assert shots[0]==shots[1] and outputs[0]==outputs[2] and outputs[1]==outputs[3]
 browser.close()
