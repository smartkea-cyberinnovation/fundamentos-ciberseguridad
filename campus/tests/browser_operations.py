#!/usr/bin/env python3
"""Real browser checks for appended operational readings; not native OS lab tests."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
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

class OperationsBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ENGINE not in ('chromium','webkit'):raise ValueError('Unsupported browser')
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(HERE/'dist')))
        Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}/'
        cls.playwright=sync_playwright().start()
        cls.browser=getattr(cls.playwright,ENGINE).launch(headless=True)
        cls.shots=HERE/'qa/operations'/ENGINE
        cls.shots.mkdir(parents=True,exist_ok=True)
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
    def go(self,route,lang='es'):
        self.page.goto(self.base+'?lang='+lang+route,wait_until='networkidle')
        expect(self.page.locator('html')).to_have_attribute('lang',lang)
        expect(self.page.locator('#main h1')).to_be_visible()
    def test_all_new_readings_and_toc(self):
        for lang in ('es','en'):
            for rid in ('D22','D23','D24','D25'):
                with self.subTest(lang=lang,resource=rid):
                    self.go('#/recurso/'+rid,lang)
                    self.assertGreater(len(self.page.locator('#main article').inner_text()),4500)
                    self.page.locator('#main .toc summary').click()
                    self.page.locator('#main .toc a').last.click()
                    self.assertIn('/recurso/'+rid,self.page.url)
    def test_crosslinks_and_context_navigation(self):
        for lang in ('es','en'):
            self.go('#/modulo/M18',lang)
            self.page.locator('#main article a[href="#/recurso/D24"]').last.click()
            expect(self.page.locator('#main h1')).to_contain_text('TLS')
            self.page.locator('#main article a[href="#/recurso/D25"]').first.click()
            expect(self.page.locator('#main article')).to_contain_text('OPS-L12')
    def test_responsive_reading_widths(self):
        for width in (320,390,768,820,1024,1440):
            self.page.set_viewport_size({'width':width,'height':1000})
            for lang in ('es','en'):
                with self.subTest(width=width,lang=lang):
                    self.go('#/recurso/D24',lang)
                    self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'))
                    self.page.screenshot(path=str(self.shots/f'd24-{lang}-{width}.png'),full_page=True)
    def test_language_switch_preserves_core_progress(self):
        self.go('#/modulo/M07')
        self.page.locator('#read-check').check()
        self.page.locator('#main article a[href="#/recurso/D22"]').last.click()
        self.page.locator('#language').select_option('en')
        expect(self.page.locator('html')).to_have_attribute('lang','en')
        self.go('#/modulo/M07','en')
        expect(self.page.locator('#read-check')).to_be_checked()
    def test_continuous_readings_include_extension_without_javascript(self):
        context=self.browser.new_context(java_script_enabled=False)
        try:
            page=context.new_page()
            for path,lang in (('lectura.html','es'),('reading.en.html','en')):
                page.goto(self.base+path)
                expect(page.locator('html')).to_have_attribute('lang',lang)
                for rid in ('D22','D23','D24','D25'):
                    expect(page.locator('article#'+rid)).to_have_count(1)
                expect(page.locator('article#D25')).to_contain_text('OPS-L12')
        finally:context.close()

if __name__=='__main__':unittest.main(verbosity=2)
