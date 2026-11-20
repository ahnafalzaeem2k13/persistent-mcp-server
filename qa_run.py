
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path('/content/persistent-mcp-server'); out=root/'results'; out.mkdir(exist_ok=True)
report={'project':'NIGHTLINE — The City After Dark','browser':'Playwright Chromium','version':None,'url':'http://127.0.0.1:8765/','viewports':{},'interactions':{},'console_errors':[],'page_errors':[],'failed_requests':[]}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 report['version']=b.version
 for name,w,h in [('desktop',1440,900),('tablet',768,1024)]:
  page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  page.on('console',lambda m: report['console_errors'].append(m.text) if m.type=='error' else None)
  page.on('pageerror',lambda e: report['page_errors'].append(str(e)))
  page.on('requestfailed',lambda r: report['failed_requests'].append({'url':r.url,'error':r.failure}))
  resp=page.goto(report['url'],wait_until='networkidle',timeout=30000)
  page.screenshot(path=str(out/f'after-{name}-viewport.png'),full_page=False)
  page.screenshot(path=str(out/f'after-{name}.png'),full_page=True)
  nav=page.locator('#nav'); menu=page.locator('#menuBtn')
  data={'status':resp.status if resp else None,'title':page.title(),'viewport':[w,h],
        'scroll_width':page.evaluate('document.documentElement.scrollWidth'),
        'horizontal_overflow':page.evaluate('document.documentElement.scrollWidth > window.innerWidth'),
        'nav_display':nav.evaluate('(e)=>getComputedStyle(e).display') if nav.count() else None,
        'menu_visible':menu.is_visible() if menu.count() else False}
  if name=='tablet':
   data['menu_expanded_before']=menu.get_attribute('aria-expanded')
   menu.click(); page.wait_for_timeout(180)
   data['menu_expanded_after_open']=menu.get_attribute('aria-expanded')
   data['nav_visible_after_open']=nav.is_visible()
   page.screenshot(path=str(out/'after-tablet-menu.png'),full_page=False)
   nav.locator('a[href="#network"]').click(); page.wait_for_timeout(100)
   data['menu_expanded_after_link']=menu.get_attribute('aria-expanded')
   data['hash_after_link']=page.evaluate('location.hash')
   report['interactions']['tablet_navigation']='passed' if data['menu_expanded_after_open']=='true' and data['menu_expanded_after_link']=='false' and data['hash_after_link']=='#network' else 'failed'
  if name=='desktop':
   data['desktop_nav_links']=nav.locator('a').count()
   report['interactions']['desktop_inline_navigation']='passed' if data['desktop_nav_links']==3 and nav.is_visible() else 'failed'
  report['viewports'][name]=data
  page.close()
 # Functional route selection and motion toggle on tablet-size page
 page=b.new_page(viewport={'width':768,'height':1024})
 page.goto(report['url'],wait_until='networkidle')
 route=page.locator('button[data-route="river"]')
 route.click()
 report['interactions']['route_selection']='passed' if route.get_attribute('aria-pressed')=='true' else 'failed'
 motion=page.locator('#motionBtn')
 motion.click()
 report['interactions']['motion_toggle']='passed' if motion.get_attribute('aria-pressed')=='true' else 'failed'
 page.close(); b.close()
report['overall_pass']=all(v['status']==200 and not v['horizontal_overflow'] for v in report['viewports'].values()) and not report['console_errors'] and not report['page_errors'] and not report['failed_requests'] and all(v=='passed' for v in report['interactions'].values())
(out/'QA-REPORT.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
