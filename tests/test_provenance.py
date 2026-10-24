from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
for branch in ('quenya','sindarin'):
 data=json.loads((root/'branches'/branch/'data/chain_step_provenance.json').read_text())
 for corpus,target in [('critical','app/chains.json'),('structural','data/research_chains_for_app.json')]:
  chains=json.loads((root/'branches'/branch/target).read_text())
  assert len(data[corpus])==len(chains)
  assert [x['id'] for x in data[corpus]]==[x['id'] for x in chains]
  for c,entry in zip(chains,data[corpus]):
   assert len(entry['steps'])==len(c['states'])-1
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--allow-file-access-from-files'])
 page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((root/'app/index.html').read_text(),wait_until='load')
 for branch in ('quenya','sindarin'):
  page.locator(f'[data-load="{branch}"]').click()
  page.locator('#atlas-period').uncheck()
  page.locator('#all-chains').click()
  assert page.locator('.atlas-provenance').count()>0, branch
  assert 'Аудит шагов' in page.locator('.atlas-provenance').first.text_content()
  page.locator('#atlas-corpus').select_option('research')
  assert page.locator('.atlas-provenance').count()>0
  page.locator('#branch-home').click()
 assert not errors,errors
 browser.close()
print('Provenance integrity and browser PASS')
