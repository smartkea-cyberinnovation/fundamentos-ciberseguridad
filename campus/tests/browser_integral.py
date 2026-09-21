#!/usr/bin/env python3
"""Real browser acceptance of D26-D36, distinct from native OS lab execution."""
from functools import partial
from http.server import ThreadingHTTPServer
import os
from pathlib import Path
import sys
from threading import Thread
import unittest
from playwright.sync_api import sync_playwright, expect
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from serve import Handler
ENGINE=os.environ.get('CAMPUS_BROWSER','chromium')

class IntegralBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ENGINE not in ('chromium','webkit'):raise ValueError('Unsupported browser')
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(HERE/'dist')))
        Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}/'
        cls.playwright=sync_playwright().start();cls.browser=getattr(cls.playwright,ENGINE).launch(headless=True)
        cls.shots=HERE/'qa/integral'/ENGINE;cls.shots.mkdir(parents=True,exist_ok=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.playwright.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.context=self.browser.new_context(viewport={'width':1440,'height':1000})
        self.page=self.context.new_page();self.errors=[]
        self.page.on('pageerror',lambda error:self.errors.append(str(error)))
    def tearDown(self):
        try:self.assertEqual(self.errors,[])
        finally:self.context.close()
    def go(self,rid,lang='es'):
        self.page.goto(self.base+'?lang='+lang+'#/recurso/'+rid,wait_until='networkidle')
        expect(self.page.locator('html')).to_have_attribute('lang',lang)
        expect(self.page.locator('#main h1')).to_be_visible()
    def test_all_eleven_readings_both_languages(self):
        for lang in ('es','en'):
            for n in range(26,37):
                with self.subTest(language=lang,resource=n):
                    self.go(f'D{n:02}',lang)
                    self.assertGreater(len(self.page.locator('#main article').inner_text()),2500)
                    self.page.locator('#main .toc summary').click()
                    self.page.locator('#main .toc a').last.click()
                    self.assertIn('/recurso/D',self.page.url)
    def test_context_links(self):
        for lang in ('es','en'):
            self.go('D26',lang)
            self.page.locator('#main article a[href="#/recurso/D32"]').first.click()
            expect(self.page.locator('#main article')).to_contain_text('TLP')
    def test_mobile_tablet_desktop(self):
        for width in (320,390,768,820,1024,1440):
            self.page.set_viewport_size({'width':width,'height':1000})
            for lang in ('es','en'):
                self.go('D28',lang)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'))
                self.page.screenshot(path=str(self.shots/f'hardware-{lang}-{width}.png'),full_page=True)
    def test_glossary_references_and_language(self):
        self.go('D35')
        expect(self.page.locator('#main article')).to_contain_text('INT-G36')
        self.page.locator('#language').select_option('en')
        expect(self.page.locator('html')).to_have_attribute('lang','en')
        expect(self.page.locator('#main article')).to_contain_text('separation of duties')
        self.page.locator('#main article a[href="#/recurso/D36"]').first.click()
        expect(self.page.locator('#main article')).to_contain_text('RFC 9846')
    def test_no_js_continuous_reading(self):
        context=self.browser.new_context(java_script_enabled=False)
        try:
            page=context.new_page()
            for path in ('lectura.html','reading.en.html'):
                page.goto(self.base+path)
                for n in range(26,37):expect(page.locator(f'article#D{n:02}')).to_have_count(1)
        finally:context.close()

if __name__=='__main__':unittest.main(verbosity=2)
