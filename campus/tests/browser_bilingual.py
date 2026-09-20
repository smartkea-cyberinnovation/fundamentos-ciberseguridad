#!/usr/bin/env python3
"""Real-browser acceptance. A missing/blocked browser is an ERROR, never a skip.

Set CAMPUS_BROWSER=webkit to additionally validate WebKit with its installed engine.
A viewport simulation is not a physical iPad/iPhone or a native OS laboratory.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
from threading import Thread
import unittest
from playwright.sync_api import sync_playwright, expect

HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE))
from serve import Handler
KEY='fundamentos-ciberseguridad:progress:v1'
ENGINE=os.environ.get('CAMPUS_BROWSER','chromium')
SHOTS=HERE/'qa/current'/ENGINE/'screenshots'
class BrowserAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(HERE/'dist')))
        Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}/'
        cls.playwright=sync_playwright().start()
        engine=os.environ.get('CAMPUS_BROWSER','chromium')
        if engine not in ('chromium','webkit','firefox'):raise ValueError('Unsupported engine')
        options={'headless':True}
        if os.environ.get('CAMPUS_BROWSER_EXECUTABLE'):options['executable_path']=os.environ['CAMPUS_BROWSER_EXECUTABLE']
        cls.browser=getattr(cls.playwright,engine).launch(**options)
        cls.catalogs={lang:json.loads((HERE/('dist/course.en.json' if lang=='en' else 'dist/course.json')).read_text()) for lang in ('es','en')}
        SHOTS.mkdir(parents=True,exist_ok=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.playwright.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.context=self.browser.new_context(viewport={'width':1440,'height':1000})
        self.page=self.context.new_page();self.errors=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
    def tearDown(self):
        try:self.assertEqual(self.errors,[])
        finally:self.context.close()
    def go(self,route='#/curso',lang='es',page=None):
        p=page or self.page;p.goto(self.base+'?lang='+lang+route,wait_until='networkidle')
        expect(p.locator('html')).to_have_attribute('lang',lang)
        expect(p.locator('#main h1')).to_be_visible();return p
    def state(self,page=None):return (page or self.page).evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
    def test_01_start_pages(self):
        for lang,title in [('es','Aprende. Practica. Comprueba.'),('en','Learn. Practise. Verify.')]:
            with self.subTest(lang=lang):
                self.go(lang=lang);expect(self.page.locator('#main h1')).to_have_text(title)
                self.page.screenshot(path=str(SHOTS/f'home-{lang}.png'),full_page=True)
    def test_02_all_modules_and_tabs_both_languages(self):
        for lang,catalog in self.catalogs.items():
            for m in catalog['modules']:
                for suffix in ('','/practicas','/revision'):
                    with self.subTest(lang=lang,module=m['id'],tab=suffix):
                        self.go('#/modulo/'+m['id']+suffix,lang)
                        expect(self.page.locator('#main h1')).to_have_text(m['title'])
                        self.assertNotIn('undefined',self.page.locator('#main').inner_text())
    def test_03_switch_language_keeps_notes_and_reading(self):
        self.go('#/modulo/M05');self.page.locator('#read-check').check()
        self.page.locator('.notes-panel summary').click();self.page.locator('#notes').fill('Synthetic private study note')
        self.page.locator('#language').select_option('en')
        expect(self.page.locator('html')).to_have_attribute('lang','en');expect(self.page.locator('#read-check')).to_be_checked()
        expect(self.page.locator('#notes')).to_have_value('Synthetic private study note')
        self.page.reload();expect(self.page.locator('#notes')).to_have_value('Synthetic private study note')
    def test_04_syllabus_filters(self):
        for lang in ('es','en'):
            with self.subTest(lang=lang):
                self.go('#/temario',lang);expect(self.page.locator('[data-outline-row]:visible')).to_have_count(32)
                for query in ('M05',' m05 '):
                    self.page.locator('#outline-query').fill(query)
                    expect(self.page.locator('[data-outline-row]:visible')).to_have_count(1)
                    expect(self.page.locator('[data-outline-row]:visible')).to_have_attribute('data-module','M05')
                self.page.locator('#outline-query').fill('nothing-12345');expect(self.page.locator('#outline-empty')).to_be_visible()
                self.page.locator('#outline-reset').click();expect(self.page.locator('[data-outline-row]:visible')).to_have_count(32)
                self.page.locator('#outline-block').select_option('linux');expect(self.page.locator('[data-outline-row]:visible')).to_have_count(8)
    def test_05_formative_quiz(self):
        self.go('#/modulo/M01/revision','en');correct=self.catalogs['en']['modules'][0]['quiz']['correct']
        self.page.locator(f'input[name=answer][value="{correct}"]').check();self.page.locator('#quiz button').click()
        self.assertTrue(self.state()['modules']['M01']['quiz'])
    def test_06_guided_lab_checks_and_recovery(self):
        self.go('#/modulo/M05/practica/L05A','en')
        for phase in range(5):
            expect(self.page.locator(f'[data-phase="{phase}"]')).to_have_attribute('aria-current','step')
            self.page.locator('#step-check').check()
            if phase<4:self.page.locator('#wizard-next').click()
        expect(self.page.locator('#finish-lab')).to_be_enabled();self.page.locator('#finish-lab').click()
        self.assertTrue(self.state()['labs']['L05A']['done']);self.page.reload()
        expect(self.page.locator('[data-phase="4"]')).to_have_attribute('aria-current','step')
    def test_07_portable_progress_requires_confirmation(self):
        self.go('#/modulo/M05','en');self.page.locator('#read-check').check()
        self.page.locator('.notes-panel summary').click();self.page.locator('#notes').fill('PRIVATE-NOTE-NOT-SHARED')
        self.go('#/compartir','en');self.page.locator('#make-transfer').click();expect(self.page.locator('#shared-url')).to_be_visible()
        url=self.page.locator('#shared-url').input_value();self.assertNotIn('PRIVATE',url)
        receiver=self.browser.new_context();p=receiver.new_page()
        try:
            p.goto(url,wait_until='networkidle');expect(p.locator('#accept-transfer')).to_be_visible()
            self.assertIsNone(p.evaluate('(k)=>localStorage.getItem(k)',KEY))
            self.assertNotIn('/transfer/',p.url)
            p.locator('#accept-transfer').click();expect(p.locator('#read-check')).to_be_checked()
            self.assertEqual(self.state(p)['modules']['M05']['notes'],'')
        finally:receiver.close()
    def test_08_bad_transfer_does_not_change_notes(self):
        self.go('#/modulo/M05');self.page.locator('#read-check').check();original=self.state()
        self.go('#/transfer/bad','en');expect(self.page.locator('#main')).to_contain_text('expired or incompatible')
        self.assertEqual(self.state()['modules'],original['modules'])
    def test_09_presentation_keyboard(self):
        self.go('#/modulo/M05','en');self.page.locator('#present').click();expect(self.page.locator('#presentation')).to_be_visible()
        before=self.page.locator('#slide-count').inner_text();self.page.keyboard.press('ArrowRight')
        self.assertNotEqual(self.page.locator('#slide-count').inner_text(),before)
        self.page.screenshot(path=str(SHOTS/'presentation-en.png'))
        self.page.keyboard.press('Escape');expect(self.page.locator('#presentation')).not_to_be_visible()
    def test_10_library_all_resources(self):
        for lang,catalog in self.catalogs.items():
            for r in catalog['resources']:
                with self.subTest(lang=lang,resource=r['id']):
                    self.go('#/recurso/'+r['id'],lang);expect(self.page.locator('#main h1').first).to_have_text(r['title'])
    def test_11_no_global_overflow_at_phone_tablet_laptop_sizes(self):
        for width,height in [(320,740),(360,800),(390,844),(768,1024),(820,1180),(1024,768),(1440,1000)]:
            self.page.set_viewport_size({'width':width,'height':height})
            for lang in ('es','en'):
                for route in ['#/curso','#/temario','#/modulo/M05','#/modulo/M05/practica/L05A','#/progreso','#/compartir']:
                    with self.subTest(width=width,height=height,lang=lang,route=route):
                        self.go(route,lang)
                        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width+1)
            if width in (390,768,820):
                self.go('#/temario','en');self.page.screenshot(path=str(SHOTS/f'index-en-{width}.png'),full_page=True)
    def test_12_mobile_menu_can_open_and_close(self):
        self.page.set_viewport_size({'width':390,'height':844});self.go(lang='en')
        self.page.locator('#menu-button').click();expect(self.page.locator('#sidebar')).to_be_visible()
        self.page.locator('#sidebar .primary-nav a[href="#/temario"]').click()
        expect(self.page.locator('#sidebar')).not_to_be_visible();expect(self.page.locator('#outline-query')).to_be_visible()
    def test_13_two_tab_resume_survives_dashboard_reload(self):
        self.go('#/modulo/M05/revision');self.go('#/curso')
        other=self.context.new_page();self.go('#/modulo/M06','es',other);other.locator('#read-check').check()
        self.page.reload();expect(self.page.locator('#resume')).to_have_attribute('href','#/modulo/M05/revision')
    def test_14_read_without_javascript(self):
        context=self.browser.new_context(java_script_enabled=False);p=context.new_page()
        try:
            for lang,path in [('es','lectura.html'),('en','reading.en.html')]:
                p.goto(self.base+path);expect(p.locator('html')).to_have_attribute('lang',lang)
                expect(p.locator('article#M32')).to_be_attached()
        finally:context.close()
    def test_15_skip_link_keeps_route(self):
        self.go('#/modulo/M05');url=self.page.url;self.page.locator('.skip-link').focus();self.page.keyboard.press('Enter')
        self.assertEqual(self.page.url,url);expect(self.page.locator('#main')).to_be_focused()
    def test_16_reset_requires_confirmation(self):
        self.go('#/modulo/M05');self.page.locator('#read-check').check();self.go('#/progreso')
        self.page.once('dialog',lambda d:d.dismiss());self.page.locator('#reset').click()
        self.assertTrue(self.state()['modules']['M05']['read'])
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#reset').click()
        self.assertFalse(self.state()['modules']['M05']['read'])
    def test_17_backup_round_trip(self):
        self.go('#/modulo/M05');self.page.locator('#read-check').check();self.go('#/progreso')
        with self.page.expect_download() as download:self.page.locator('#export').click()
        saved=Path(download.value.path()).read_bytes()
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#reset').click()
        self.page.once('dialog',lambda d:d.accept())
        self.page.locator('#import-file').set_input_files({'name':'progress.json','mimeType':'application/json','buffer':saved})
        expect(self.page.locator('#status')).to_contain_text('Copia importada');self.assertTrue(self.state()['modules']['M05']['read'])
    def test_18_kit_result_checks(self):
        self.go('#/modulo/M05/practica/L05A','en');self.page.locator('[data-phase="2"]').click()
        self.page.locator('input[name=files]').fill('8');self.page.locator('input[name=bytes]').fill('62');self.page.locator('#result-check button').click()
        expect(self.page.locator('#result-feedback')).to_contain_text('Correct:')
    def test_19_deep_link_unknown_module(self):
        self.go('#/modulo/M99','en');expect(self.page.locator('#main h1')).to_contain_text('not found')
    def test_20_larger_text_preserves_reading(self):
        self.go('#/modulo/M05','en');self.page.locator('#text-size').check();self.page.reload()
        expect(self.page.locator('body')).to_have_class('large-text')

if __name__=='__main__':unittest.main(verbosity=2)
