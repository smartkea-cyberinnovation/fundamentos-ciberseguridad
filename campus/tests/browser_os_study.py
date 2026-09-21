"""Real OS classroom browser acceptance. No fallback mocks or skipped blocked browser."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ENGINE=os.environ.get('CAMPUS_BROWSER','chromium')
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

class BrowserOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'dist')))
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.http.server_port}/sistemas/'
        cls.pw=sync_playwright().start();cls.browser=getattr(cls.pw,ENGINE).launch()
        cls.catalog=json.loads((ROOT/'dist/sistemas/course.es.json').read_text())
        (ROOT/'qa/os-study').mkdir(parents=True,exist_ok=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.http.shutdown();cls.http.server_close()
    def setUp(self):
        self.context=self.browser.new_context(viewport={'width':1440,'height':1000});self.page=self.context.new_page()
    def tearDown(self):self.context.close()
    def open(self,path='?lang=es#OS-C01/0'):
        self.page.goto(self.url+path);self.page.locator('#content h1').wait_for()
        self.page.wait_for_function("document.querySelector('#position').textContent.includes('OS-')")
    def test_01_all_lessons_both_languages(self):
        for lang in ['es','en']:
            for lesson in self.catalog['lessons']:
                self.open(f'?lang={lang}#{lesson["id"]}/1')
                self.assertEqual(self.page.locator('#content h1').count(),1)
                self.assertIn(lesson['id'],self.page.locator('#position').inner_text())
                self.assertEqual(lang,self.page.locator('html').get_attribute('lang'))
    def test_02_micropractice_follows_concept(self):
        self.open('?lang=es#OS-C01/1');self.page.locator('#next').click()
        self.assertEqual('Micropráctica',self.page.locator('.eyebrow').inner_text())
    def test_03_present_keyboard_and_escape(self):
        self.open('?lang=es#OS-L01/1');self.page.locator('#present').click()
        self.page.keyboard.press('ArrowRight');self.assertTrue(self.page.url.endswith('/2'))
        self.page.keyboard.press('Escape');self.assertNotIn('presentation',self.page.locator('body').get_attribute('class') or '')
    def test_04_fullscreen_rejection_fallback(self):
        self.page.add_init_script("Element.prototype.requestFullscreen=function(){return Promise.reject(new Error('test denial'))}")
        self.open();self.page.locator('#fullscreen').click()
        self.assertIn('presentation',self.page.locator('body').get_attribute('class'))
        self.assertTrue(self.page.locator('#next').is_visible())
    def test_05_mobile_and_tablet_no_global_overflow(self):
        for lang in ['es','en']:
            for width in [320,390,768,820,1024,1440]:
                self.page.set_viewport_size({'width':width,'height':900})
                self.open(f'?lang={lang}#OS-W03/8')
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                self.page.screenshot(path=str(ROOT/f'qa/os-study/{ENGINE}-{lang}-{width}.png'))
    def test_06_environment_selector_arm(self):
        self.open('?lang=en#OS-W01/0');self.page.locator('#help').click()
        self.page.locator('#host-choice').select_option('mac-arm')
        self.assertIn('ARM64',self.page.locator('#environment-result').inner_text())
        self.assertIn('AD DS',self.page.locator('#environment-result').inner_text())
    def test_07_explicit_persistence_and_reload(self):
        self.open();self.assertIsNone(self.page.evaluate("localStorage.getItem('smartkea.os.study.v1')"))
        self.page.locator('#dashboard').click();self.page.locator('#remember').check();self.page.locator('#close-panel').click()
        self.page.locator('#done').click();self.page.reload();self.page.locator('#position').wait_for()
        self.assertIn('done',self.page.locator('#marks').inner_text())
    def test_08_timer_pauses_when_hidden(self):
        self.open();self.page.locator('#start').click();self.page.wait_for_timeout(1100)
        self.page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
        self.assertTrue(self.page.locator('#pause').is_disabled())
        before=self.page.locator('#clock').inner_text();self.page.wait_for_timeout(1200);self.assertEqual(before,self.page.locator('#clock').inner_text())
    def test_09_quiz_requires_correct_answer(self):
        l=self.catalog['lessons'][0];n=next(i for i,v in enumerate(l['views']) if v['kind']=='quiz')
        self.open(f'?lang=es#OS-C01/{n}');self.assertTrue(self.page.locator('#done').is_disabled())
        self.page.locator(f'[data-answer="{l["quiz"]["correct"]}"]').click();self.assertTrue(self.page.locator('#done').is_enabled())
    def test_10_native_lab_confirmation(self):
        self.open('?lang=es#OS-L01/10');self.page.locator('#done').click()
        self.assertIn('Confirma',self.page.locator('#status').inner_text())
        self.page.locator('#blocked').click();self.assertIn('blocked',self.page.locator('#marks').inner_text())
    def test_11_no_js_full_reading(self):
        with self.browser.new_context(java_script_enabled=False) as context:
            p=context.new_page();p.goto(self.url+'reading.en.html')
            self.assertEqual(28,p.locator('article').count());self.assertIn('Operating systems',p.title())
    def test_12_import_rejects_bad_schema(self):
        self.open();self.page.locator('#dashboard').click()
        self.page.locator('#import').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"schema":0}'})
        self.assertIn('rechazada',self.page.locator('#import-preview').inner_text())
    def test_13_download_evidence(self):
        l=self.catalog['lessons'][0];n=next(i for i,v in enumerate(l['views']) if v['kind']=='handover')
        self.open(f'?lang=es#OS-C01/{n}')
        with self.page.expect_download() as event:self.page.locator('#template').click()
        self.assertTrue(event.value.suggested_filename.endswith('.md'))
    def test_14_import_confirmation_then_merge(self):
        x={'schema':1,'course':'smartkea-os-study','marks':{'OS-C01:0':{'status':'done','at':1}},'sessions':{},'last':'OS-C01/0','goal':2}
        self.open();self.page.locator('#dashboard').click()
        self.page.locator('#import').set_input_files({'name':'copy.json','mimeType':'application/json','buffer':json.dumps(x).encode()})
        self.page.locator('#confirm-import').wait_for();self.page.locator('#confirm-import').click()
        self.assertIn('done',self.page.locator('#marks').inner_text())

if __name__=='__main__':unittest.main(verbosity=2)
