#!/usr/bin/env python3
"""Complete and verify only this Lab 02 project; never modify another lab.
Run: python build_submission.py
Requires Python 3.13, Playwright 1.57.0/Chromium, Beautiful Soup 4.14.3,
tinycss2 1.5.1, Node.js, pdfLaTeX and pdfinfo.
"""
from __future__ import annotations
import functools
import hashlib
import http.server
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import textwrap
import threading
import zipfile
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import tinycss2

ROOT = Path(__file__).resolve().parent
RESULTS = []


def write(name, content):
    target = ROOT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


def build_site():
    """Keep the existing content, layout and stylesheet; apply scoped additions."""
    html = (ROOT / 'index.html').read_text()
    css = (ROOT / 'style.css').read_text()
    if 'id="registration-form"' not in html:
        digest = hashlib.sha1(b'blob ' + str(len(html.encode())).encode() + b'\0' + html.encode()).hexdigest()
        if digest != '25ddf991b0aeb8bd590c2d5ae6fa66a723d85a42':
            raise RuntimeError('The original HTML changed; inspect before applying the Lab 02 update.')
        changes = [
            ('  <link rel="stylesheet" href="style.css">', '  <link rel="stylesheet" href="style.css">\n  <link rel="icon" href="images/event-banner.svg" type="image/svg+xml">\n  <script src="form-demo.js" defer></script>'),
            ('<body>', '<body>\n  <a class="skip-link" href="#main-content">Skip to main content</a>'),
            ('<span>15-16 October 2026</span>', '<span>Sample event: 15-16 October 2026</span>'),
            ('<main class="page-shell">', '<main id="main-content" class="page-shell" tabindex="-1">'),
            ('images/event-banner.jpg', 'images/event-banner.svg'),
            ('with laptop and technology symbols"', 'with a laptop and connected technology nodes" width="800" height="500"'),
            ('Complete the registration form with valid information.', 'Try the demonstration form using sample information.'),
            ('Keep the selected date in mind for the planned session.', 'Check the validation message; no real booking is made.'),
            ('<div class="two-column lists-layout">', '<div class="two-column">'),
            ('<div class="table-wrap">', '<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable event schedule">'),
            ('<form action="#register" method="get" onsubmit="return false;">', '<form id="registration-form" action="#register" method="get"\n            aria-describedby="static-notice" autocomplete="off">'),
            ('minlength="10" maxlength="15" inputmode="numeric" required', 'minlength="10" maxlength="15" inputmode="numeric"\n                   pattern="[0-9]{10,15}" title="Enter 10 to 15 digits." required'),
            ('<legend>Topics of Interest</legend>', '<legend>Topics of Interest (optional)</legend>'),
            ('<div class="choice-row checkbox-row">', '<div class="choice-row">'),
            ('<div class="form-note" role="note">', '<div id="static-notice" class="form-note" role="note">'),
            ('The form is intentionally prevented from submitting because this HTML lab has no backend service.', 'Submit checks your entries locally. No registration is created, and this page does not send or save your information.'),
            ('<button type="submit" class="primary-button">Submit Registration</button>', '<button type="submit" id="submit-demo" class="primary-button" disabled>Submit Registration</button>'),
            ('      </form>', '        <p id="form-status" class="form-status" role="status" aria-live="polite">Use sample information to test this demonstration.</p>\n        <noscript><p>JavaScript is disabled. Submit is unavailable to prevent data transmission. Reset still works.</p></noscript>\n      </form>'),
            ('Email: <a href="mailto:cse.lab@seu.edu.bd">cse.lab@seu.edu.bd</a>', 'Sample contact from the lab manual: <span>cse.lab@seu.edu.bd</span>\n          <br>This address is shown as an example; event enquiries are not monitored here.'),
            ('        <a href="#top">Back to top</a>', '        <p><a href="https://html.spec.whatwg.org/multipage/" target="_blank"\n              rel="noopener noreferrer">Read the HTML Living Standard</a></p>\n        <a href="#top">Back to top</a>'),
        ]
        for old, new in changes:
            if old not in html:
                raise RuntimeError('Expected HTML fragment missing: ' + old)
            html = html.replace(old, new)
        lines = []
        for line in html.splitlines():
            indent = re.match(r'^\s*', line).group()
            lines.extend(textwrap.wrap(line, width=110, subsequent_indent=indent+'  ',
                                       break_long_words=False, break_on_hyphens=False,
                                       replace_whitespace=False) if len(line)>110 else [line])
        write('index.html', '\n'.join(lines)+'\n')
    if '.skip-link {' not in css:
        css = css.replace('--teal: #0f8b8d;', '--teal: #0b7476;')
        css = css.replace('input:focus-visible {', 'input:focus-visible,\n.table-wrap:focus-visible {')
        css += '''
/* Small accessibility and safe-demo additions to the existing Lab 02 theme. */
.skip-link {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 100;
  padding: 10px 16px;
  background: var(--white);
  transform: translateY(-180%);
}

.skip-link:focus {
  transform: translateY(0);
}

#main-content,
#contact {
  scroll-margin-top: 84px;
}

.form-status {
  min-height: 1.65em;
  margin: 18px 0 0;
  color: #205c4d;
  font-weight: 600;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.about-grid > div,
.footer-inner > div,
.field-group {
  min-width: 0;
}

.site-footer p {
  overflow-wrap: anywhere;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
'''
        write('style.css', css)
    write('form-demo.js', '''"use strict";

// Safety helper only: field validation remains native HTML validation.
// Install the handlers before enabling Submit. No storage or network calls.
const form = document.getElementById("registration-form");
const submitButton = document.getElementById("submit-demo");
const statusMessage = document.getElementById("form-status");

if (form && submitButton && statusMessage) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    statusMessage.textContent =
      "Validation successful. Demo only: no information was sent or saved.";
  });

  form.addEventListener("reset", function () {
    statusMessage.textContent =
      "Form reset. Use sample information to try the demonstration again.";
  });

  // Without this helper, the disabled button prevents click/Enter submission.
  submitButton.disabled = false;
}
''')
    write('images/event-banner.svg', '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500" role="img" aria-labelledby="title desc">
  <title id="title">SEU TechConnect 2026 classroom event banner</title>
  <desc id="desc">A laptop displaying code brackets, connected technology nodes, and the sample event date.</desc>
  <rect width="800" height="500" fill="#102d46"/>
  <circle cx="755" cy="30" r="190" fill="#16415b"/>
  <circle cx="28" cy="510" r="170" fill="#16415b"/>
  <g stroke="#3a8392" stroke-width="2" fill="none">
    <path d="M64 283H132L174 241H236M560 251H646L694 204H746M564 329H656L691 364H750"/>
    <circle cx="64" cy="283" r="8"/><circle cx="746" cy="204" r="8"/>
    <circle cx="750" cy="364" r="8"/>
  </g>
  <g font-family="Arial, sans-serif">
    <text x="48" y="55" fill="#85d8d0" font-size="16" letter-spacing="3">SOUTHEAST UNIVERSITY / CSE 472</text>
    <text x="48" y="112" fill="#ffffff" font-size="48" font-weight="700">TechConnect 2026</text>
    <text x="50" y="149" fill="#cae1e9" font-size="20">Build. Share. Learn together.</text>
  </g>
  <rect x="227" y="201" width="346" height="204" rx="14" fill="#d5e9ef"/>
  <rect x="241" y="215" width="318" height="172" rx="5" fill="#173d59"/>
  <g stroke="#87e2d3" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M321 267L289 301L321 335M479 267L511 301L479 335M422 252L377 349"/>
  </g>
  <path d="M206 405H594L624 425H176Z" fill="#eff7fa"/>
  <path d="M176 425H624L609 434H191Z" fill="#98bacb"/>
  <g font-family="Arial, sans-serif" font-size="15" font-weight="700" text-anchor="middle">
    <rect x="50" y="190" width="124" height="38" rx="19" fill="#22677b"/>
    <text x="112" y="215" fill="#fff">WEB</text>
    <rect x="630" y="263" width="124" height="38" rx="19" fill="#22677b"/>
    <text x="692" y="288" fill="#fff">AI + DATA</text>
    <rect x="50" y="331" width="137" height="38" rx="19" fill="#22677b"/>
    <text x="118" y="356" fill="#fff">ROBOTICS</text>
  </g>
  <text x="400" y="475" text-anchor="middle" fill="#cae1e9" font-family="Arial, sans-serif" font-size="16">15-16 OCTOBER 2026 | CLASSROOM DEMONSTRATION</text>
</svg>
''')
    (ROOT/'screenshots').mkdir(exist_ok=True)
    (ROOT/'tests').mkdir(exist_ok=True)


def check(test, expected, actual, ok=True, status=None):
    row = dict(id=f'T{len(RESULTS)+1:02d}', test=test, expected=expected,
               actual=str(actual), status=status or ('PASS' if ok else 'FAIL'))
    RESULTS.append(row)
    print(row['id'], row['test'], row['status'], row['actual'], flush=True)


class NestingCheck(HTMLParser):
    void = set('area base br col embed hr img input link meta param source track wbr'.split())
    def __init__(self):
        super().__init__(); self.stack=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        if tag not in self.void: self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag: self.errors.append(tag)
        else: self.stack.pop()


def run_tests():
    html=(ROOT/'index.html').read_text(); soup=BeautifulSoup(html,'html.parser')
    nesting=NestingCheck(); nesting.feed(html)
    check('HTML5 structure and nesting','HTML5, metadata and balanced tags',
          f'Unclosed tags: {len(nesting.stack)}; nesting errors: {len(nesting.errors)}',
          html.startswith('<!DOCTYPE html>') and soup.html.get('lang')=='en' and
          bool(soup.select_one('meta[charset]')) and bool(soup.select_one('meta[name="viewport"]')) and
          bool(soup.title) and not nesting.stack and not nesting.errors)
    sections=len(soup.select('main section'))
    check('Semantic structure','One h1; at least three sections; all landmarks',
          f'{len(soup.select("h1"))} main heading; {sections} sections',
          len(soup.select('h1'))==1 and sections>=3 and all(soup.find(x) for x in ['header','nav','main','footer']))
    ids=[e['id'] for e in soup.select('[id]')]; inputs=soup.select('input')
    check('IDs and labels','Unique IDs and connected labels for every input',
          f'{len(ids)} IDs; {len(inputs)} explicitly labelled inputs',
          len(ids)==len(set(ids)) and all(e.get('name') and soup.find('label',attrs={'for':e.get('id')}) for e in inputs))
    nested=soup.select('li > ul, li > ol')
    check('Lists','Ordered, unordered and correctly nested lists',
          f'{len(nested)} nested lists inside parent list items',bool(soup.ul and soup.ol and nested))
    rows=soup.select('tbody tr')
    check('Schedule table','Caption, five headings and four consistent data rows',
          f'{len(soup.select("thead th"))} headings; {len(rows)} data rows',
          bool(soup.caption) and len(rows)==4 and len(soup.select('thead th'))==5 and all(len(r.select('td'))==5 for r in rows))
    paths=[e.get('src') or e.get('href') for e in soup.select('img[src],script[src],link[href]')]
    missing=[p for p in paths if not (ROOT/p).is_file()]
    check('Local file references','All linked local resources exist',f'{len(paths)} references; missing: {missing}',not missing)
    css_errors=[]; declarations=[]
    def walk(rules):
        for r in rules:
            if r.type=='error': css_errors.append(r.message)
            elif r.type=='qualified-rule':
                for d in tinycss2.parse_declaration_list(r.content,skip_whitespace=True,skip_comments=True):
                    if d.type=='error': css_errors.append(d.message)
                    elif d.type=='declaration': declarations.append([d.name,tinycss2.serialize(d.value).strip()])
            elif r.type=='at-rule' and r.content:
                walk(tinycss2.parse_rule_list(r.content,skip_whitespace=True,skip_comments=True))
    walk(tinycss2.parse_stylesheet((ROOT/'style.css').read_text(),skip_whitespace=True,skip_comments=True))
    check('CSS syntax','No CSS parser errors',f'{len(declarations)} declarations; {len(css_errors)} errors',not css_errors)
    js=subprocess.run(['node','--check',str(ROOT/'form-demo.js')],capture_output=True,text=True)
    check('Helper syntax','Node syntax check succeeds',f'Exit code {js.returncode}',js.returncode==0)
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/index.html'
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        browser_version=browser.version
        context=browser.new_context(viewport={'width':1200,'height':1100},device_scale_factor=1,reduced_motion='reduce')
        page=context.new_page(); page.set_default_timeout(15000)
        errors=[]; requests=[]; responses={}
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('request',lambda r:requests.append(r.url))
        page.on('response',lambda r:responses.update({r.url:r.status}))
        page.goto(url,wait_until='networkidle')
        image=page.locator('img').evaluate('(e)=>e.complete && e.naturalWidth===800')
        gradient=page.locator('.site-header').evaluate('(e)=>getComputedStyle(e).backgroundImage')
        unsupported=page.evaluate('(ds)=>ds.filter(([p,v])=>!CSS.supports(p,v))',declarations)
        check('Rendered image and styling','Image loaded and CSS declarations supported',
              f'Image loaded: {image}; unsupported declarations: {len(unsupported)}',image and 'linear-gradient' in gradient and not unsupported)
        anchors=[e.get_attribute('href') for e in page.locator('a[href^="#"]').all()]; failed=[]
        for href in anchors:
            if href=='#main-content': page.keyboard.press('Tab')
            page.locator(f'a[href="{href}"]').first.click()
            if page.locator(href).count()!=1 or not page.url.endswith(href): failed.append(href)
        check('Internal navigation','Every link reaches its target',f'{len(anchors)} links checked; {len(failed)} failures',not failed)
        external=soup.select('a[href^="https://"]')
        safe=all(a.get('target')=='_blank' and {'noopener','noreferrer'}<=set(a.get('rel',[])) for a in external)
        check('External link attributes','HTTPS, new tab and safe relationship attributes',f'{len(external)} external links checked',safe)
        ep=context.new_page()
        try:
            er=ep.goto('https://html.spec.whatwg.org/multipage/',timeout=25000,wait_until='domcontentloaded')
            check('Live external destination','HTML standard loads successfully',f'HTTP {er.status if er else "unknown"}',bool(er and er.ok))
        except Exception:
            check('Live external destination','HTML standard loads successfully','Live navigation unavailable in the test environment',status='BLOCKED')
        ep.close()
        page.locator('button[type="reset"]').click(); page.locator('#submit-demo').click()
        valid=page.locator('form').evaluate('(e)=>e.checkValidity()')
        focus=page.evaluate('document.activeElement.id')
        check('Required fields','Empty form rejected and first required field focused',f'Valid: {valid}; focus: {focus}',not valid and focus=='fullname')
        page.locator('#fullname').fill('Demo Student')
        page.locator('#studentid').fill('2023000000001')
        page.locator('#email').fill('demo@example.com')
        page.locator('#preferred-date').fill('2026-10-15')
        page.locator('#attendee').check()
        page.locator('#fullname').fill('Al')
        short=page.locator('#fullname').evaluate('(e)=>e.validity.tooShort')
        check('Name minimum length','Two-character name rejected',f'tooShort: {short}',short)
        page.locator('#fullname').fill('Demo Student')
        page.locator('#studentid').fill('ABCDEFGHIJKLM')
        mismatch=page.locator('#studentid').evaluate('(e)=>e.validity.patternMismatch')
        page.locator('#studentid').fill('1234567890123456')
        length=len(page.locator('#studentid').input_value())
        check('Student ID limits','Letters rejected; maximum fifteen digits',f'Letter mismatch: {mismatch}; capped length: {length}',mismatch and length==15)
        page.locator('#studentid').fill('2023000000001')
        page.locator('#email').fill('not-an-email')
        mismatch=page.locator('#email').evaluate('(e)=>e.validity.typeMismatch')
        check('Email validation','Malformed email rejected',f'typeMismatch: {mismatch}',mismatch)
        page.locator('#email').fill('demo@example.com')
        dates=[]
        for date in ['2026-10-14','2026-10-15','2026-10-16','2026-10-17']:
            page.locator('#preferred-date').fill(date)
            dates.append(page.locator('#preferred-date').evaluate('(e)=>e.checkValidity()'))
        check('Date boundaries','Only 15 and 16 October accepted',f'14, 15, 16, 17 October valid: {dates}',dates==[False,True,True,False])
        page.locator('#preferred-date').fill('2026-10-15')
        page.locator('#presenter').check(); exclusive=not page.locator('#attendee').is_checked()
        page.locator('#attendee').check(); exclusive=exclusive and not page.locator('#presenter').is_checked()
        check('Radio group','Exactly one participation type selected',f'Exclusive: {exclusive}',exclusive)
        page.locator('#topic-web').check(); page.locator('#topic-ai').check()
        count=page.locator('input[type="checkbox"]:checked').count()
        check('Checkbox choices','Two topics can be selected independently',f'Selected topics: {count}',count==2)
        before=page.url; requests.clear(); page.locator('#submit-demo').click(); page.wait_for_timeout(200)
        message=page.locator('#form-status').inner_text()
        safe_submit='Validation successful.' in message and page.url==before and not requests
        check('Valid demo submission','Local confirmation; no request or navigation',f'Confirmation: {"Validation successful." in message}; new requests: {len(requests)}',safe_submit)
        page.locator('#email').press('Enter'); page.wait_for_timeout(200)
        check('Enter-key submission','Enter uses the same safe handler',f'Unchanged URL: {page.url==before}; new requests: {len(requests)}',page.url==before and not requests)
        def capture(name,start,end):
            page.evaluate('window.scrollTo(0,0)')
            top=0 if start is None else page.locator(start).bounding_box()['y']-18
            box=page.locator(end).bounding_box(); bottom=box['y']+box['height']+(0 if end=='#contact' else 18)
            page.screenshot(path=str(ROOT/'screenshots'/name),full_page=True,
                            clip={'x':0,'y':max(0,top),'width':1200,'height':bottom-max(0,top)})
        capture('homepage-top.png',None,'#about')
        capture('event-goals.png','#goals','#goals')
        capture('event-details.png','#activities','#schedule')
        capture('registration-form.png','#register','#contact')
        page.locator('button[type="reset"]').click()
        reset=page.locator('form').evaluate('(e)=>[...e.querySelectorAll("input")].every(i=>["radio","checkbox"].includes(i.type)?!i.checked:i.value==="")')
        check('Reset button','All fields and selections return to defaults',f'All controls reset: {reset}',reset)
        page.locator('label[for="fullname"]').click(); focused=page.evaluate('document.activeElement.id')=='fullname'
        page.locator('label[for="topic-iot"]').click(); selected=page.locator('#topic-iot').is_checked()
        check('Label interaction','Labels focus or toggle the corresponding input',f'Text focus: {focused}; checkbox selected: {selected}',focused and selected)
        page.locator('#fullname').focus(); page.keyboard.press('Tab')
        outline=page.evaluate('({width:getComputedStyle(document.activeElement).outlineWidth,style:getComputedStyle(document.activeElement).outlineStyle})')
        check('Keyboard focus','Tab gives a visible three-pixel focus outline',f'{outline["width"]} {outline["style"]}',outline['width']=='3px' and outline['style']=='solid')
        for width in [1200,820,390,320]:
            page.set_viewport_size({'width':width,'height':900})
            docwidth=page.evaluate('document.documentElement.scrollWidth')
            check(f'Responsive layout at {width}px','No horizontal document overflow',f'Document width: {docwidth}px; viewport: {width}px',docwidth<=width)
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('window.scrollTo(0,document.getElementById("register").offsetTop-76)')
        page.screenshot(path=str(ROOT/'screenshots/mobile-registration.png'))
        page.locator('.table-wrap').evaluate('(e)=>e.scrollLeft=100')
        offset=page.locator('.table-wrap').evaluate('(e)=>e.scrollLeft')
        check('Mobile table scrolling','Wide table scrolls inside its own region',f'Horizontal offset: {offset}px',offset>0)
        reduced=page.locator('html').evaluate('(e)=>getComputedStyle(e).scrollBehavior')
        check('Reduced motion','Reduced-motion preference disables smooth scrolling',f'scroll-behavior: {reduced}',reduced=='auto')
        nj=browser.new_context(java_script_enabled=False,reduced_motion='reduce',viewport={'width':1200,'height':900})
        np=nj.new_page(); nr=[]; np.on('request',lambda r:nr.append(r.url)); np.goto(url,wait_until='networkidle')
        for sel,value in [('#fullname','Demo Student'),('#studentid','2023000000001'),('#email','demo@example.com'),('#preferred-date','2026-10-15')]: np.locator(sel).fill(value)
        np.locator('#attendee').focus(); np.keyboard.press('Space'); nr.clear(); initial=np.url
        np.locator('#email').press('Enter'); np.wait_for_timeout(200)
        disabled=np.locator('#submit-demo').is_disabled()
        check('No-JavaScript safety','Submit disabled; Enter sends no information',f'Disabled: {disabled}; new requests: {len(nr)}; unchanged URL: {np.url==initial}',disabled and not nr and np.url==initial)
        nj.close()
        check('Console and page errors','No avoidable errors on the implemented page',f'Errors recorded: {len(errors)}',not errors)
        required=['/index.html','/style.css','/form-demo.js','/images/event-banner.svg']
        loaded=all(any(u.endswith(name) and status==200 for u,status in responses.items()) for name in required)
        check('Real resource loading','HTML, CSS, helper and SVG load through HTTP',f'All four resources returned HTTP 200: {loaded}',loaded)
        browser.close()
    server.shutdown()
    summary=dict(Counter(r['status'] for r in RESULTS))
    data={'checked_at_utc':datetime.now(timezone.utc).isoformat(),
          'environment':{'browser':'Chromium '+browser_version,'mode':'local HTTP server in GitHub Actions','viewports':[1200,820,390,320],'screenshots':5},
          'summary':summary,'tests':RESULTS}
    write('tests/results.json',json.dumps(data,indent=2)+'\n')
    rows=['# Actual browser and source test results','',f'Browser: Chromium {browser_version}. Delivery: real local HTTP server.',
          '',f'Summary: {summary}','', '| ID | Check | Expected | Actual | Status |','|---|---|---|---|---|']
    for r in RESULTS: rows.append('| '+' | '.join(str(r[k]).replace('|','/') for k in ['id','test','expected','actual','status'])+' |')
    write('tests/TEST_RESULTS.md','\n'.join(rows)+'\n')
    if summary.get('FAIL'): raise RuntimeError('At least one test failed; see tests/results.json.')
    return data


def tex(value):
    replacements={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(replacements.get(c,c) for c in str(value))


def build_report(data):
    metadata={'BrowserVersion':data['environment']['browser'],'PythonVersion':platform.python_version(),
              'PlaywrightVersion':importlib.metadata.version('playwright'),'SoupVersion':importlib.metadata.version('beautifulsoup4'),
              'CSSVersion':importlib.metadata.version('tinycss2'),'PassedCount':data['summary'].get('PASS',0),
              'BlockedCount':data['summary'].get('BLOCKED',0),'FailedCount':data['summary'].get('FAIL',0),
              'TotalCount':len(RESULTS),'HTMLLines':len((ROOT/'index.html').read_text().splitlines()),
              'CSSLines':len((ROOT/'style.css').read_text().splitlines())}
    write('report/build-metadata.tex',''.join(f'\\newcommand{{\\{k}}}{{{tex(v)}}}\n' for k,v in metadata.items()))
    rows=[]
    for r in RESULTS:
        rows.append(' & '.join(tex(r[k]) for k in ['id','test','expected'])+' & '+r'\textbf{'+tex(r['status'])+'}. '+tex(r['actual'])+r' \\[2pt]'+'\n')
    write('report/test-cases.tex',''.join(rows))
    report=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype}
\usepackage[left=21mm,right=21mm,top=22mm,bottom=22mm,headheight=15pt]{geometry}
\usepackage{graphicx,xcolor,booktabs,array,longtable,tabularx}
\usepackage{listings,caption,fancyhdr,titlesec,enumitem,float}
\usepackage[hidelinks]{hyperref}
\definecolor{navy}{HTML}{12324B}
\definecolor{teal}{HTML}{0B7476}
\definecolor{muted}{HTML}{5B6874}
\definecolor{line}{HTML}{D6E0E8}
\titleformat{\section}{\Large\bfseries\color{navy}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\large\bfseries\color{navy}}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{16pt}{8pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}
\setlength{\emergencystretch}{3em}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{muted}CSE 472 / Web and Internet Programming Lab}
\fancyhead[R]{\small\color{muted}Lab Report 02}
\fancyfoot[L]{\small\color{muted}Jannatul Tuna Trisha / 2023200000664}
\fancyfoot[R]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\captionsetup{font=small,labelfont=bf,skip=8pt}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\lstdefinelanguage{CSS}{morekeywords={color,background,margin,padding,display,grid,flex,width,height,border,font,position,media,root},sensitive=true,morecomment=[s]{/*}{*/},morestring=[b]"}
\lstdefinelanguage{JavaScript}{morekeywords={const,if,function,false,true},sensitive=true,morecomment=[l]{//},morestring=[b]",morestring=[b]'}
\lstset{basicstyle=\ttfamily\fontsize{8.5}{10.2}\selectfont,keywordstyle=\color{navy}\bfseries,
commentstyle=\color{muted},stringstyle=\color{teal},numbers=left,numberstyle=\tiny\color{muted},numbersep=8pt,
showstringspaces=false,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,
tabsize=2,frame=single,rulecolor=\color{line},framesep=5pt,xleftmargin=12pt,xrightmargin=3pt,
aboveskip=10pt,belowskip=10pt,captionpos=t}
\input{build-metadata.tex}
\hypersetup{pdftitle={CSE 472 Lab Report 02: HTML Fundamentals and Structured Webpage Development},pdfauthor={Jannatul Tuna Trisha}}
\begin{document}
\begin{titlepage}
\centering
{\Large\bfseries\color{navy}SOUTHEAST UNIVERSITY\par}
\vspace{8pt}
{\large Department of Computer Science and Engineering\par}
\vspace{26pt}
{\large CSE 472\par Web and Internet Programming Lab\par}
\vspace{34pt}
{\fontsize{30}{36}\selectfont\bfseries\color{navy}Lab Report 02\par}
\vspace{14pt}
{\LARGE\bfseries HTML Fundamentals and\par Structured Webpage Development\par}
\vspace{20pt}
{\small\color{muted}ASSIGNMENT TITLE\par}
\vspace{5pt}
{\large SEU Tech Event Information\par and Registration Page\par}
\vspace{32pt}
\begin{tabular}{@{}ll@{}}
\textbf{Submitted by} & Jannatul Tuna Trisha \\[8pt]
\textbf{Student ID} & 2023200000664 \\[8pt]
\textbf{Section} & 01 \\[8pt]
\textbf{Semester} & 9th \\[8pt]
\textbf{Submitted to} & Abid Ahmad \\[8pt]
\textbf{Submission date} & 8 September 2026 \\
\end{tabular}
\vfill
{\small\color{muted}Individual laboratory submission\par}
{\small\color{muted}HTML5 structure, lists, tables, forms and semantic layout\par}
\end{titlepage}
\setcounter{page}{2}

\section{Student Information}
\begin{tabularx}{\linewidth}{@{}L{36mm}Y@{}}
\toprule
Student & Jannatul Tuna Trisha \\
Student ID / Section & 2023200000664 / 01 \\
Semester & 9th \\
Department / University & Computer Science and Engineering / Southeast University \\
Course & CSE 472 -- Web and Internet Programming Lab \\
Instructor & Abid Ahmad \\
Submission date & 8 September 2026 \\
Repository folder & \url{https://github.com/Trisha105/CSE472/tree/main/labs/lab-02-html} \\
\bottomrule
\end{tabularx}
\section{Introduction}
This experiment applies the final submission task in the CSE 472 HTML lab manual: a complete single-page event information and registration website \cite{manual}. The page is titled \emph{SEU Tech Event Information and Registration Page}. Its content includes an event overview, goals, activity tracks, a four-session schedule, a registration form and contact details.

The event name, dates, sessions and rooms are classroom examples, not an official university announcement. The sample contact address comes from the manual and is labelled as an example. HTML provides the structure, an external CSS file provides the presentation, and a small JavaScript helper prevents the demonstration form from sending information.
\section{Objectives}
The aim was to build a structured HTML5 page using meaningful semantic elements and a clear heading hierarchy. The work also practised ordered, unordered and nested lists; a captioned schedule table; labelled form controls; appropriate input constraints; and correct local file paths. A further objective was to test the completed page and document its actual output with source code and browser screenshots.

\clearpage
\section{Software and Tools Used}
\begin{tabularx}{\linewidth}{@{}L{46mm}Y@{}}
\toprule
\textbf{Tool} & \textbf{Use in this experiment} \\
\midrule
UTF-8 files and command-line editing & Preserving and completing the existing HTML/CSS project. \\
\BrowserVersion & Rendering the website and exercising its controls. \\
Python \PythonVersion; Playwright \PlaywrightVersion & Automated checks and genuine browser screenshots. \\
Beautiful Soup \SoupVersion; tinycss2 \CSSVersion & Inspecting markup and parsing the stylesheet. \\
Node.js & Syntax-checking the form helper. \\
pdfLaTeX, listings and pdfinfo & Compiling the report, displaying full source code and checking PDF metadata. \\
Git and GitHub Actions & Running the actual served website, reviewing related changes and publishing the submission. \\
\bottomrule
\end{tabularx}
\section{Short Theory of HTML}
HTML stands for HyperText Markup Language. It describes the structure of webpage content and is not a general-purpose programming language. A browser reads elements such as headings, paragraphs, images, lists, tables and forms and renders them as a page. Attributes provide additional information, such as an image path, a link destination or an input type \cite{manual}.

Semantic elements describe the role of content. For example, \texttt{nav} identifies navigation, \texttt{main} contains the main page content, and \texttt{footer} holds closing information. A \texttt{div} groups a block without assigning a special semantic role, while a \texttt{span} groups a short inline part of text.
\section{HTML5 Document Structure}
The file begins with \texttt{<!DOCTYPE html>} and uses \texttt{<html lang="en">}. Its head contains UTF-8 encoding, a responsive viewport, a descriptive browser-tab title, a page description and an external CSS link. The local SVG is also used as the favicon. The deferred helper runs after the document is parsed.

The body contains a keyboard skip link, a header with exactly one \texttt{h1}, a navigation bar, a main area with five sections and a footer. About, Goals, Activities, Schedule and Registration have IDs used by the internal links. The document therefore meets the manual's requirement for at least three meaningful sections \cite{manual}.

\clearpage
\section{Important Tags and Attributes}
{\small
\begin{tabularx}{\linewidth}{@{}L{48mm}Y@{}}
\toprule
\textbf{Tag or attribute} & \textbf{Use in this implementation} \\
\midrule
\texttt{header, nav, main, section, footer} & Separate the introduction, links, main content and contact area. \\
\texttt{h1, h2, h3, p} & Give the page a main heading, section/subsection headings and paragraphs. \\
\texttt{div, span} & Group cards and fields; highlight the purpose and event details. \\
\texttt{a, href, target, rel} & Connect page anchors and external sources; safe new-tab attributes are used. \\
\texttt{img, src, alt} & Display the local event illustration with a meaningful description. \\
\texttt{ul, ol, li} & Present goals, participation steps and nested activity tracks. \\
\texttt{table, caption, thead, tbody} & Organise the table title, column headings and four session rows. \\
\texttt{tr, th, td, scope} & Define consistent rows, header associations and data cells. \\
\texttt{form, label, input, button} & Collect demonstration values and provide Submit and Reset. \\
\texttt{fieldset, legend} & Name the participation and optional-interest groups. \\
\texttt{id, for, name, value} & Associate labels, identify fields and distinguish selected choices. \\
\texttt{required, type, minlength, maxlength, pattern, min, max} & Apply native required, length, numeric-pattern, email and date constraints. \\
\bottomrule
\end{tabularx}}
\section{Requirements Analysis}
Table~\ref{tab:req} maps the manual's final task to this project. Responsive styling, a reset button, keyboard support and safe form feedback are supporting additions, not extra requirements attributed to the manual.
\begin{table}[H]\small
\caption{Final-task requirement mapping.}\label{tab:req}
\begin{tabularx}{\linewidth}{@{}L{56mm}Y@{}}
\toprule
\textbf{Requirement} & \textbf{Implemented evidence} \\
\midrule
HTML5 and semantic layout & Complete skeleton, header, nav, main, five sections and footer. \\
Meaningful headings and text & One h1, clear subheadings and explanatory event/participation content. \\
Div, span, hyperlink and image & Grouped content, highlighted text, anchors and a local SVG with alt text. \\
Three list types & Goals list, ordered steps and correctly nested activity tracks. \\
Schedule table & Caption, five column headings and four data rows. \\
Required registration controls & Name, ID, email, date, one radio group and three checkboxes. \\
Code and submission evidence & Full source, five browser screenshots, compiled report and verified ZIP. \\
\bottomrule
\end{tabularx}
\end{table}

\clearpage
\section{Project Folder Structure}
\begin{lstlisting}[numbers=none,caption={Final Lab 02 folder layout.}]
labs/lab-02-html/
|-- index.html
|-- style.css
|-- form-demo.js
|-- images/event-banner.svg
|-- screenshots/
|   |-- homepage-top.png
|   |-- event-goals.png
|   |-- event-details.png
|   |-- registration-form.png
|   `-- mobile-registration.png
|-- report/
|   |-- lab_report_02.tex
|   |-- build-metadata.tex
|   |-- test-cases.tex
|   `-- lab_report_02.pdf
|-- tests/
|   |-- results.json
|   `-- TEST_RESULTS.md
|-- build_submission.py
|-- README.md
|-- SHA256SUMS.txt
`-- CSE472_Lab_02_Complete.zip
\end{lstlisting}
The archive excludes itself, Git metadata, caches, temporary LaTeX files and unrelated repository content. SVG is used instead of the suggested JPG because it is a small scalable local image; the manual does not require a particular image format.
\section{Design and Implementation Procedure}
The repository was inspected before editing. The existing Lab 02 HTML, CSS and README on \texttt{main} were read. No other lab folder or repository-specific instruction file was present in the inspected baseline. The update retained the existing event content, section order, cards and navy/teal colour scheme.

The missing image was supplied as an original SVG, and its reference was corrected. A skip link, labelled scrollable table region, reduced-motion rule and local form feedback were added. The ID field now accepts 10--15 digits; this is an example validation rule, not a claim about university-wide ID policy.

The helper installs submission/reset handlers before enabling Submit. Native HTML validation runs first; a valid submission is then cancelled and replaced by a local demonstration message. The completed page was tested, captured in Chromium, included in this report and packaged. Only related Lab 02 files and its build workflow were intentionally changed.

\clearpage
\section{Complete HTML Source Code}
Listing~\ref{lst:html} contains all \HTMLLines{} lines of the final HTML file. Visual line wrapping in this report does not change the source.
\lstinputlisting[language=HTML,caption={Complete final index.html.},label={lst:html}]{../index.html}
\clearpage
\section{Complete CSS Source Code}
Listing~\ref{lst:css} contains all \CSSLines{} lines of the external stylesheet. The original theme is retained with small accessibility and form-state additions.
\lstinputlisting[language=CSS,caption={Complete final style.css.},label={lst:css}]{../style.css}

\clearpage
\section{Explanation of Major Website Sections}
\textbf{Header and navigation.} The header introduces the page and sample event. Six main links reach the sections and footer; a skip link and Back to top link provide additional navigation. The single main heading names the assignment.

\textbf{About and Goals.} About explains eligibility, venue and participation. The local illustration depicts a laptop and technology topics, not an actual campus photograph. Goals are shown as an unordered list, and the academic-project notice makes the fictional event status clear.

\textbf{Activities and Schedule.} An ordered list explains the demonstration process. Nested lists group Web, AI/Data and IoT/Robotics topics. The schedule has a caption, five column headings and four sample sessions. Its labelled region scrolls on narrow screens without widening the whole page.

\textbf{Registration and Contact.} Nine inputs are explicitly labelled. The four main fields use text, email and date types; radio buttons share one group name, while checkboxes allow multiple interests. The footer identifies the student and labels the manual's contact address as an example.
\subsection{Complete Safety Helper}
The helper adds no database, account system, server request or storage. Submit starts disabled, is enabled only after the handlers are installed, and remains unavailable without JavaScript. Native HTML controls supply the actual field validation \cite{standard}.
\lstinputlisting[language=JavaScript,caption={Complete form-demo.js helper.}]{../form-demo.js}

\section{Testing Procedure}
Static checks inspected explicit tag nesting, metadata, landmarks, IDs, labels, list structure, schedule rows and local file references. tinycss2 parsed the stylesheet, Chromium checked its declaration support, and Node checked the helper syntax. These are local parser/browser checks, not an official W3C conformance certificate.

The final recorded run used \BrowserVersion{} with the delivered files served by a real local HTTP server in GitHub Actions. HTML, CSS, JavaScript and the SVG were loaded through their actual URLs. The earlier local development browser had blocked direct file and loopback access; the final served-page run is a separate check and is reported independently.

Browser tests exercised required and malformed fields, date boundaries, radio exclusivity, independent checkboxes, Submit, Enter, Reset, labels, focus outlines, reduced motion and widths of 1200, 820, 390 and 320 pixels. Fictitious values were used: Demo Student, 2023000000001 and demo@example.com. The test observed the URL and network activity around submission. A separate JavaScript-disabled context checked the fallback.

External-link safety and a live visit to the HTML standard were checked separately. Any unavailable live destination is marked BLOCKED, not PASS. The university server's availability, other browser engines, physical phones and full screen-reader behaviour are not asserted. To repeat the build, install the tools in the README and run \texttt{python build\_submission.py} from the Lab 02 folder.

\section{Test Cases and Actual Results}
The final recorded run contains \TotalCount{} checks: \textbf{\PassedCount{} passed}, \textbf{\BlockedCount{} blocked}, and \textbf{\FailedCount{} failed}. The following results are generated from the executed checks. Full records are included in \texttt{tests/results.json} and \texttt{tests/TEST\_RESULTS.md}.
{\fontsize{9.5}{11.2}\selectfont
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.04}
\begin{longtable}{@{}L{9mm}L{34mm}L{47mm}L{69mm}@{}}
\caption{Executed tests with expected and actual results.}\label{tab:tests}\\
\toprule\textbf{ID}&\textbf{Check}&\textbf{Expected}&\textbf{Actual result}\\\midrule
\endfirsthead
\multicolumn{4}{@{}l}{Table \thetable{} continued}\\[5pt]
\toprule\textbf{ID}&\textbf{Check}&\textbf{Expected}&\textbf{Actual result}\\\midrule
\endhead
\bottomrule\endfoot
\bottomrule\endlastfoot
\input{test-cases.tex}
\end{longtable}}

\clearpage
\section{Output Screenshots}
Figures~\ref{fig:home}--\ref{fig:mobile} are genuine Chromium captures of the implemented page. Four images show desktop page regions at a 1200-pixel width; the final image shows a 390-by-844-pixel mobile viewport. No screenshot is copied from the manual or recreated as a mockup.
\begin{figure}[H]\centering
\includegraphics[width=\linewidth,height=190mm,keepaspectratio]{../screenshots/homepage-top.png}
\caption{Header, navigation, introduction, local event illustration and participation details.}\label{fig:home}
\end{figure}
\clearpage
\begin{figure}[H]\centering
\includegraphics[width=\linewidth,height=200mm,keepaspectratio]{../screenshots/event-details.png}
\caption{Ordered participation steps, nested topic lists and the complete four-row schedule.}\label{fig:details}
\end{figure}
The activity lists are nested inside their parent items. All five headings and all four sample sessions are visible in the desktop table.
\clearpage
\begin{figure}[H]\centering
\includegraphics[width=\linewidth,height=200mm,keepaspectratio]{../screenshots/registration-form.png}
\caption{Complete form and footer after a valid demonstration submission. The fictitious test values are shown with explicit confirmation that nothing was sent or saved.}\label{fig:form}
\end{figure}
\clearpage
\begin{figure}[H]\centering
\includegraphics[width=\linewidth]{../screenshots/event-goals.png}
\caption{Unordered goals and the academic-project notice.}\label{fig:goals}
\end{figure}
\begin{figure}[H]\centering
\includegraphics[height=118mm,keepaspectratio]{../screenshots/mobile-registration.png}
\caption{Mobile registration layout with one-column fields and a visible focus outline. The navigation scrolls within its own strip.}\label{fig:mobile}
\end{figure}

\clearpage
\section{Problems Faced and Solutions}
\textbf{Missing image asset.} The initial HTML referenced an event-banner JPG that was not in the repository. An original SVG was added, and the page and documentation were updated to use its real relative path. The final browser check verifies both HTTP loading and image rendering.

\textbf{A form could imply a real registration service.} The previous form silently cancelled submission. The updated version states its demonstration purpose, shows local feedback and prevents data transmission. Submit is initially disabled and stays disabled when JavaScript is unavailable. The Enter-key fallback was tested separately.

\textbf{Local browser access was restricted.} The initial development environment blocked direct file and loopback navigation. A browser-preview run was used during development. The final suite runs in GitHub Actions against a real HTTP server, so resource loading is not inferred only from files existing on disk.

\textbf{Long source listings needed readable page layout.} The report includes the actual final files through \texttt{listings}, with wrapping and line numbers. Screenshots preserve aspect ratio. Repeated table headings keep the test cases readable across pages.
\section{Learning Outcomes}
The work shows how individual HTML elements combine into a complete page. Label-click and keyboard tests demonstrate the relationship between an input and its label. Goals and steps are suited to lists, while a schedule needs consistent table headings and rows. Separating HTML and CSS keeps the document structure clear while allowing responsive layouts.

The form also demonstrates an important limitation: visible input controls and browser validation do not create a registration service. A production version would require a backend, server-side validation and an appropriate data-handling process. Recording blocked checks separately from successful tests is part of reporting results accurately.
\clearpage
\section{Conclusion}
The Lab 02 page combines the required HTML5 structure, semantic sections, meaningful text, links, image, lists, schedule and registration controls. The existing design was completed without changing another lab. The actual browser results document the tested behaviour and distinguish any unavailable external check. Complete source code, five screenshots, the compiled report, reproducible build script and a verified ZIP are included in the submission.
\section{References}
\begingroup\renewcommand{\section}[2]{}
\begin{thebibliography}{9}
\bibitem{manual} A. Ahmad, \emph{CSE 472 -- Web and Internet Programming Lab: Complete HTML Lab Manual}, Southeast University. Supplied course manual, especially Sections 19--26. The uploaded copy was a DOCX document.
\bibitem{standard} WHATWG, \emph{HTML Living Standard}. Accessed 8 September 2026. \url{https://html.spec.whatwg.org/multipage/}
\end{thebibliography}\endgroup
\textbf{Image attribution:} \texttt{images/event-banner.svg} is an original illustration created for this submission using simple vector shapes and text. It is not a campus photograph and contains no third-party logo or font file. The five output images are browser captures of this project.
\end{document}
'''
    write('report/lab_report_02.tex',report)
    with tempfile.TemporaryDirectory(prefix='lab02-tex-') as temp:
        cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+temp,'lab_report_02.tex']
        for _ in range(3):
            completed=subprocess.run(cmd,cwd=ROOT/'report',capture_output=True,text=True)
            if completed.returncode:
                print(completed.stdout[-12000:]); raise RuntimeError('LaTeX compilation failed.')
        log=(Path(temp)/'lab_report_02.log').read_text(errors='replace')
        problems=[line for line in log.splitlines() if any(x in line for x in ['Overfull','undefined references','LaTeX Error'])]
        if problems: print('Layout warnings to inspect:',problems)
        shutil.copy2(Path(temp)/'lab_report_02.pdf',ROOT/'report/lab_report_02.pdf')
    info=subprocess.check_output(['pdfinfo',str(ROOT/'report/lab_report_02.pdf')],text=True)
    pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
    print(info)
    return pages,problems


def build_readme(data,pages):
    summary=data['summary']
    text=f'''# CSE 472 - Lab Report 02
## HTML Fundamentals and Structured Webpage Development

**Assignment: SEU Tech Event Information and Registration Page**

| Student field | Value |
|---|---|
| Name | Jannatul Tuna Trisha |
| Student ID | 2023200000664 |
| Section | 01 |
| Semester | 9th |
| Department | Computer Science and Engineering |
| University | Southeast University |
| Course | CSE 472 - Web and Internet Programming Lab |
| Instructor | Abid Ahmad |
| Submission date | 8 September 2026 |

## Description and features
The single-page project applies the manual's final task: HTML5 metadata, one h1, semantic header/navigation/main/five sections/footer, meaningful div/span, safe links, a local image, ordered/unordered/nested lists, a five-column schedule with four data rows, and nine explicitly labelled registration inputs. External CSS provides cards, responsive fields, a scrollable table, keyboard focus and reduced-motion support. No CSS framework is used.

The event dates, rooms and programme are classroom examples, not an official university announcement. The contact address is taken from the manual and labelled as an example. The ID constraint of 10-15 digits is an example rule, not university policy.

## Run the website
Open `index.html` in a modern browser. All page resources are local; internet access is needed only to follow external hyperlinks. No build step or package installation is needed just to view the website.

Alternatively, from this folder run `python -m http.server 8000`, then open `http://127.0.0.1:8000/`. A GitHub source folder is not automatically a deployed website.

## Static form limitation
The form is a demonstration, not a registration service. HTML constraints check entries. `form-demo.js` cancels valid submission, displays feedback and does not send or save information. Submit starts disabled and is enabled only after the handlers are installed. It stays disabled without JavaScript. Reset restores default field values. Use fictitious values when testing.

## Actual testing summary
The final run used **{data['environment']['browser']}** against a **real local HTTP server in GitHub Actions**. Results: **{summary.get('PASS',0)} passed, {summary.get('BLOCKED',0)} blocked, {summary.get('FAIL',0)} failed** across 33 checks. See [the full table](tests/TEST_RESULTS.md) and [raw results](tests/results.json).

The suite covers markup, CSS syntax/support, local references and real HTTP asset loading, image rendering, internal links, safe external links, native validation, radio/checkbox behaviour, Submit, Enter, Reset, labels, keyboard focus, no-JavaScript fallback, table scrolling and widths of 1200/820/390/320 pixels. No console or page error is claimed absent unless the recorded check passes. An unavailable external destination is marked BLOCKED rather than PASS.

During initial local development, the execution environment blocked direct file and loopback access. The final served-page run is separate from that preview test. No official W3C validation certificate, cross-browser, physical-phone or full screen-reader test is claimed.

## Project structure
```text
lab-02-html/
|-- index.html
|-- style.css
|-- form-demo.js
|-- images/event-banner.svg
|-- screenshots/ (five PNG browser captures)
|-- report/
|   |-- lab_report_02.tex
|   |-- build-metadata.tex
|   |-- test-cases.tex
|   `-- lab_report_02.pdf
|-- tests/
|   |-- results.json
|   |-- TEST_RESULTS.md
|   `-- build-status.json
|-- build_submission.py
|-- README.md
|-- SHA256SUMS.txt
`-- CSE472_Lab_02_Complete.zip
```

## LaTeX compilation
The compiled report has **{pages} pages** and includes the complete final HTML, CSS and safety helper. Keep the whole folder structure so relative listing/image paths resolve. In `report/`, run:
```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error lab_report_02.tex
```
No shell escape is required. TeX Live needs the standard LaTeX packages, listings and lmodern.

## Reproduce the complete submission
The build script runs only within this Lab 02 folder. It preserves the original HTML/CSS design and refuses to patch an unexpected initial HTML version. It tests, captures screenshots, generates the report, compiles it three times, creates checksums and verifies the archive.
```bash
python -m pip install playwright==1.57.0 beautifulsoup4==4.14.3 tinycss2==1.5.1
python -m playwright install --with-deps chromium
python build_submission.py
```
Python 3.13, Node.js, pdfLaTeX and pdfinfo are also required. Normal local HTTP navigation must be permitted. `.github/workflows/lab-02-build.yml` provides the same build on GitHub.

## Screenshot previews
All five images are genuine browser captures. The successful form screenshot uses fictitious registration values.

![Header and introduction](screenshots/homepage-top.png)
![Goals and academic-project notice](screenshots/event-goals.png)
![Lists and schedule](screenshots/event-details.png)
![Complete registration form and footer](screenshots/registration-form.png)
![Mobile form viewport](screenshots/mobile-registration.png)

## Image attribution
`images/event-banner.svg` is an original vector illustration made for this Lab 02 submission, using simple shapes and text. It is also used as the local favicon. It contains no third-party photograph, university logo or distributed font file, and is not a real campus photo.

## Submission contents and archive checks
The ZIP contains the HTML, CSS, helper, local SVG, five screenshots, complete LaTeX source with generated tables, compiled PDF, README, reproducible build script, actual test results and SHA-256 manifest. The ZIP excludes itself, `.git`, caches, temporary compilation files and unrelated repository files. The build prints every member, checks ZIP CRCs, extracts into a temporary folder and compares all extracted bytes with their source files.
'''
    write('README.md',text)


def package():
    names=['index.html','style.css','form-demo.js','images/event-banner.svg','README.md','build_submission.py',
           'report/lab_report_02.tex','report/build-metadata.tex','report/test-cases.tex','report/lab_report_02.pdf',
           'tests/results.json','tests/TEST_RESULTS.md','tests/build-status.json']
    names += ['screenshots/'+name for name in ['homepage-top.png','event-goals.png','event-details.png','registration-form.png','mobile-registration.png']]
    for name in names:
        if not (ROOT/name).is_file(): raise RuntimeError('Missing submission file: '+name)
    write('SHA256SUMS.txt',''.join(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in sorted(names)))
    names=sorted(names+['SHA256SUMS.txt'])
    archive=ROOT/'CSE472_Lab_02_Complete.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names: z.write(ROOT/name,'lab-02-html/'+name)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None: raise RuntimeError('ZIP CRC check failed.')
        for member in z.infolist(): print(member.file_size,member.filename)
        with tempfile.TemporaryDirectory(prefix='lab02-extract-') as temp:
            z.extractall(temp)
            for name in names:
                if (Path(temp)/'lab-02-html'/name).read_bytes() != (ROOT/name).read_bytes():
                    raise RuntimeError('Archive extraction mismatch: '+name)
    print(f'ZIP PASS: {len(names)} members; all CRC and extracted-byte checks passed.')
    print('ZIP SHA256:',hashlib.sha256(archive.read_bytes()).hexdigest())


def main():
    build_site()
    data=run_tests()
    pages,warnings=build_report(data)
    build_readme(data,pages)
    write('tests/build-status.json',json.dumps({'pdf_pages':pages,'latex_passes':3,'layout_warnings':warnings,
                                              'tests':data['summary'],'screenshots':5},indent=2)+'\n')
    package()
    if warnings:
        print('Report compiled; inspect listed layout warnings before final delivery.')


if __name__=='__main__':
    main()
