"""Smoke tests for static Eldamo explorer, using Playwright and Chromium.
Run from workspace after installing playwright and Chromium.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parent/'eldamo_sound_path_explorer_complete.html').read_text(encoding='utf-8')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':900})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='load')
    assert 'Eldamo' in page.title()
    page.locator('#rules-from').click()
    assert 'запис' in page.locator('#rule-count').inner_text()
    assert page.locator('#rule-table tbody tr').count()>0
    page.locator('#rules-to').click()
    assert page.locator('#rule-table tbody tr').count()>0
    page.locator('#go').click()
    assert 'нет пути b → f' in page.locator('#output').inner_text()
    page.locator('.side[data-slot="from"] .mode[data-mode="cluster"]').click()
    page.locator('#rules-from').click()
    assert 'сочетания' in page.locator('#rule-count').inner_text() or 'комбинации' in page.locator('#rule-count').inner_text()
    assert not errors,errors
    print('PASS: phoneme and cluster rule views, path diagnostic, zero JS errors')
    browser.close()
