from pathlib import Path
import json
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page()
 failures=[]
 page.on('pageerror',lambda e: failures.append(str(e)))
 page.set_content((r/'app/index.html').read_text(),wait_until='load')
 for b,display,research in [('quenya',139,216),('sindarin',118,114)]:
  page.locator(f'[data-load="{b}"]').click()
  assert page.locator('#atlas-corpus option').count()==2
  assert f'({research})' in page.locator('#atlas-corpus option[value="research"]').inner_text()
  assert page.locator('#atlas-corpus').input_value()=='research'
  page.locator('#atlas-period').uncheck()
  page.locator('#atlas-corpus').select_option('research')
  page.locator('#all-chains').click()
  assert page.locator('#atlas-count').inner_text().startswith(f'{research} цепочек'),(b,page.locator('#atlas-count').inner_text())
  assert page.locator('.atlas-card').count()>0
  page.locator('#atlas-grade').select_option('U')
  assert 'цепочек' in page.locator('#atlas-count').inner_text()
  page.locator('#atlas-grade').select_option('all')
  page.locator('#atlas-corpus').select_option('display')
  assert page.locator('#atlas-count').inner_text().startswith(f'{display} цепочек')
  data=json.loads((r/'branches'/b/'data/chains_common_schema.json').read_text())
  assert len(data)>=display+research # legacy schema remains an archival superset
  assert {x['corpus'] for x in data}=={'display','research'}
  ledger=json.loads((r/'branches'/b/'data/chain_identity_ledger.json').read_text())
  assert len(ledger)==display
  page.locator('#branch-home').click()
 assert not failures,failures
 browser.close()
print('RESEARCH CORPORA PASS')
