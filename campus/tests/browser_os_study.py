"""Real OS classroom browser acceptance. No fallback mocks or skipped blocked browser."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright, expect

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
    def wait_view(self,lesson,index,page=None):
        (page or self.page).wait_for_function("""({lesson,index}) => {
            const position=document.querySelector('#position').textContent;
            return location.hash==='#'+lesson+'/'+index && position.startsWith(lesson+' · ')
                && position.split(' · ').at(-1).startsWith((index+1)+' / ');
        }""",arg={'lesson':lesson,'index':index})
    def seed_record(self):
        record={'schema':1,'course':'smartkea-os-study','marks':{'OS-C01:0':{'status':'done','at':1}},
                'sessions':{'session-old':{'lesson':'OS-C01','kind':'study','ms':2000,'problemMs':0,'at':1}},'last':'OS-C01/0','goal':2}
        self.open();self.page.evaluate("record=>localStorage.setItem('smartkea.os.study.v1',JSON.stringify(record))",record)
        self.page.reload();self.wait_view('OS-C01',0)
    def saved_record(self):return self.page.evaluate("JSON.parse(localStorage.getItem('smartkea.os.study.v1'))")
    def test_01_all_lessons_both_languages(self):
        for lang in ['es','en']:
            for lesson in self.catalog['lessons']:
                self.open(f'?lang={lang}#{lesson["id"]}/1')
                self.assertEqual(self.page.locator('#content h1').count(),1)
                self.assertIn(lesson['id'],self.page.locator('#position').inner_text())
                self.assertEqual(lang,self.page.locator('html').get_attribute('lang'))
    def test_02_micropractice_follows_concept(self):
        self.open('?lang=es#OS-C01/1');self.page.locator('#next').click()
        self.wait_view('OS-C01',2)
        self.assertEqual('Micropráctica',self.page.locator('.eyebrow').text_content())
    def test_03_present_keyboard_and_escape(self):
        self.open('?lang=es#OS-L01/1');self.page.locator('#present').click()
        self.assertEqual('lesson',self.page.evaluate('document.activeElement.id'))
        self.page.keyboard.press('ArrowRight');self.wait_view('OS-L01',2)
        self.page.locator('#next').click();self.wait_view('OS-L01',3)
        self.page.keyboard.press('ArrowRight');self.wait_view('OS-L01',4)
        self.page.locator('#prev').click();self.wait_view('OS-L01',3)
        self.page.keyboard.press('Space');self.wait_view('OS-L01',2)
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
    def test_15_outline_search_hides_nonmatching_lessons(self):
        self.open();self.page.locator('#find').fill('launchd')
        self.assertEqual(1,self.page.locator('#outline a[data-lesson]:visible').count())
        self.assertIn('launchd',self.page.locator('#outline a[data-lesson]:visible').inner_text())
        self.page.locator('#find').fill('')
        self.assertEqual(28,self.page.locator('#outline a[data-lesson]:visible').count())
    def test_16_skip_link_preserves_lesson_and_moves_focus(self):
        self.open('?lang=es#OS-L03/5');before=self.page.url
        self.page.locator('.skip').focus();self.page.keyboard.press('Enter')
        self.assertEqual('lesson',self.page.evaluate('document.activeElement.id'))
        self.assertEqual(before,self.page.url)
        self.wait_view('OS-L03',5)
    def test_17_reset_reaches_other_lesson_stops_timer_and_storage_echo(self):
        self.context.add_init_script("""window.osRecordWrites=0;
            const setItem=Storage.prototype.setItem;
            Storage.prototype.setItem=function(key,value){if(this===localStorage&&key==='smartkea.os.study.v1')window.osRecordWrites++;return setItem.call(this,key,value);};""")
        self.seed_record();other=self.context.new_page();other.goto(self.url+'?lang=es#OS-L01/1');self.wait_view('OS-L01',1,other)
        other.locator('#start').click();expect(other.locator('#pause')).to_be_enabled()
        self.page.locator('#dashboard').click();self.page.once('dialog',lambda d:d.accept());self.page.locator('#reset').click()
        expect(other.locator('#status')).to_contain_text('reiniciado');expect(other.locator('#pause')).to_be_disabled()
        self.assertEqual({},self.saved_record()['marks']);self.assertEqual({},self.saved_record()['sessions'])
        self.assertEqual(1,self.saved_record()['generation']);self.assertTrue(other.url.endswith('#OS-L01/1'))
        other.locator('#blocked').click();expect(self.page.locator('#outline a[data-lesson="OS-L01"]')).to_be_visible()
        self.page.wait_for_timeout(200)
        writes=[page.evaluate('window.osRecordWrites') for page in (self.page,other)]
        self.page.wait_for_timeout(300)
        self.assertEqual(writes,[page.evaluate('window.osRecordWrites') for page in (self.page,other)])
        saved=self.saved_record();self.assertEqual(['OS-L01:1'],list(saved['marks']));self.assertEqual({},saved['sessions'])
    def test_18_stale_tab_cannot_restore_reset_data_when_storage_event_is_missed(self):
        self.seed_record();other=self.context.new_page()
        other.add_init_script("window.addEventListener('storage',event=>event.stopImmediatePropagation(),true)")
        other.goto(self.url+'?lang=es#OS-L01/1');self.wait_view('OS-L01',1,other)
        self.page.locator('#dashboard').click();self.page.once('dialog',lambda d:d.accept());self.page.locator('#reset').click()
        other.locator('#next').click();self.wait_view('OS-L01',2,other)
        expect(other.locator('#status')).to_contain_text('reiniciado')
        other.locator('#blocked').click()
        saved=self.saved_record();self.assertEqual(1,saved['generation']);self.assertEqual(['OS-L01:2'],list(saved['marks']));self.assertEqual({},saved['sessions'])
    def test_19_removing_saved_record_disables_saving_in_other_tab(self):
        for method in ('removeItem','clear'):
            with self.subTest(method=method):
                self.seed_record();other=self.context.new_page();other.goto(self.url+'?lang=es#OS-L01/1');self.wait_view('OS-L01',1,other)
                self.page.evaluate("method=>method==='clear'?localStorage.clear():localStorage.removeItem('smartkea.os.study.v1')",method)
                expect(other.locator('#status')).to_contain_text('reiniciado')
                other.locator('#next').click();self.wait_view('OS-L01',2,other);other.locator('#blocked').click()
                self.assertIsNone(self.saved_record());other.locator('#dashboard').click();expect(other.locator('#remember')).not_to_be_checked();other.close()
    def test_20_initial_load_error_is_persistent_and_can_retry(self):
        self.page.clock.install();self.page.route('**/course.es.json',lambda route:route.abort())
        self.page.goto(self.url+'?lang=es#OS-C01/0');expect(self.page.locator('#load-error')).to_be_visible()
        self.page.clock.fast_forward(7000);expect(self.page.locator('#load-error')).to_be_visible()
        self.assertNotIn('Cargando',self.page.locator('#content h1').inner_text())
        for control in ('help','dashboard','share','present','fullscreen','start','break','next'):
            expect(self.page.locator('#'+control)).to_be_disabled()
        expect(self.page.locator('#load-error a')).to_have_attribute('href','reading.es.html')
        self.page.unroute('**/course.es.json');self.page.locator('#retry-load').click();self.wait_view('OS-C01',0)
        expect(self.page.locator('#load-error')).to_have_count(0);expect(self.page.locator('#dashboard')).to_be_enabled()
    def test_21_failed_language_switch_restores_selector_and_preserves_record(self):
        self.seed_record();before=self.saved_record();self.page.route('**/course.en.json',lambda route:route.abort())
        self.page.locator('#language').select_option('en');expect(self.page.locator('#load-error')).to_be_visible()
        expect(self.page.locator('html')).to_have_attribute('lang','es');expect(self.page.locator('#language')).to_have_value('es')
        self.assertIn('?lang=es',self.page.url);self.assertEqual(before,self.saved_record());self.assertIn('done',self.page.locator('#marks').inner_text())
        expect(self.page.locator('#load-error a')).to_have_attribute('href','reading.en.html')
        self.page.unroute('**/course.en.json');self.page.locator('#retry-load').click()
        expect(self.page.locator('html')).to_have_attribute('lang','en');expect(self.page.locator('#language')).to_have_value('en')
        expect(self.page.locator('#load-error')).to_have_count(0);self.assertIn('done',self.page.locator('#marks').inner_text())
    def test_22_obsolete_language_failure_does_not_replace_newer_success(self):
        self.open();held=[];self.page.route('**/course.en.json',lambda route:held.append(route))
        self.page.locator('#language').select_option('en');self.page.wait_for_timeout(50);self.assertEqual(1,len(held))
        self.page.locator('#language').select_option('es');expect(self.page.locator('#language')).not_to_have_attribute('aria-busy','true')
        held[0].abort();self.page.wait_for_timeout(50)
        expect(self.page.locator('#load-error')).to_have_count(0);expect(self.page.locator('#language')).to_have_value('es')
        expect(self.page.locator('html')).to_have_attribute('lang','es');self.wait_view('OS-C01',0)
    def test_23_future_import_remains_editable_after_saves_and_reload(self):
        self.open();self.page.locator('#dashboard').click();self.page.locator('#remember').check()
        record={'schema':1,'course':'smartkea-os-study','generation':9007199254740991,
                'marks':{'OS-C01:0':{'status':'done','at':9007199254740991}},'sessions':{},'last':'OS-C01/0','goal':2}
        self.page.locator('#import').set_input_files({'name':'future.json','mimeType':'application/json','buffer':json.dumps(record).encode()})
        self.page.locator('#confirm-import').click();self.assertEqual(0,self.saved_record()['generation'])
        self.assertEqual(0,self.saved_record()['marks']['OS-C01:0']['at'])
        self.page.locator('#review').click();self.page.locator('#next').click();self.wait_view('OS-C01',1)
        self.page.locator('#prev').click();self.wait_view('OS-C01',0);self.page.reload();self.wait_view('OS-C01',0)
        self.assertEqual('review',self.saved_record()['marks']['OS-C01:0']['status'])
        self.assertIn('review',self.page.locator('#marks').inner_text())
        self.page.locator('#dashboard').click();self.page.once('dialog',lambda d:d.accept());self.page.locator('#reset').click()
        self.assertEqual(1,self.saved_record()['generation']);self.assertEqual({},self.saved_record()['marks'])

if __name__=='__main__':unittest.main(verbosity=2)
