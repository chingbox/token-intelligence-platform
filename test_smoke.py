"""Browser smoke tests. Run: python test_smoke.py (requires playwright + chromium)."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).parent)))
Thread(target=server.serve_forever,daemon=True).start()
path=f'http://127.0.0.1:{server.server_port}/index.html'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(path)
    page.wait_for_selector('#totalTokens')
    initial=page.locator('#totalTokens').inner_text()
    assert initial not in ('—','0'),initial
    assert page.locator('#totalUSD').inner_text().startswith('US$')
    page.locator('#buffer').fill('0')
    page.locator('#buffer').dispatch_event('change')
    lower=page.locator('#totalTokens').inner_text()
    assert int(lower.replace(',',''))<int(initial.replace(',',''))
    page.locator('[data-page="roi"]').click()
    assert page.locator('#roiSaving').inner_text().endswith('Tokens')
    page.locator('#roiTasks').fill('1');page.locator('#roiTasks').dispatch_event('input')
    assert '-' in page.locator('#roiSaving').inner_text()
    page.locator('[data-page="pricing"]').click()
    page.locator('#addModel').click()
    assert page.locator('#modelRows tr').count()==2
    page.locator('[data-page="estimate"]').click()
    with page.expect_download() as d: page.locator('#exportEstimate').click()
    assert d.value.suggested_filename=='token-budget.csv'
    page.locator('[data-page="analytics"]').click()
    csv='phase,input_tokens,output_tokens\n需求與研究,1000,2000\n需求與研究,500,200\n'
    page.locator('#csvFile').set_input_files({'name':'actual.csv','mimeType':'text/csv','buffer':csv.encode('utf-8')})
    assert '匯入完成' in page.locator('#importStatus').inner_text()
    assert '3,700' in page.locator('#actualTotal').inner_text()
    page.locator('[data-page="resources"]').click()
    with page.expect_download() as d: page.locator('#downloadSkill').click()
    assert d.value.suggested_filename=='SKILL.md'
    assert not errors,errors
    mobile=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mobile.goto(path)
    assert mobile.locator('main').evaluate('(e)=>e.scrollWidth <= window.innerWidth + 1'), 'main overflow on mobile'
    print('PASS: load, formulas, ROI, pricing, CSV export/import, SKILL.md download, mobile layout, JS errors')
    browser.close()