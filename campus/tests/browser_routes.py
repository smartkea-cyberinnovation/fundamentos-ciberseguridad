#!/usr/bin/env python3
"""Real-browser checks for role paths, independent of the external DPD catalogue."""
from functools import partial
from http.server import ThreadingHTTPServer
import json,os,sys,unittest
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright,expect,TimeoutError as BrowserTimeout
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE))
from serve import Handler
KEY='smartkea.learning-paths.v1';CAMPUS_KEY='fundamentos-ciberseguridad:progress:v1'
class RoutesAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(HERE/'dist')))
        Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}/'
        cls.pw=sync_playwright().start();cls.engine=os.environ.get('CAMPUS_BROWSER','chromium')
        if cls.engine not in ('chromium','webkit','firefox'):raise ValueError('Unsupported browser')
        options={'headless':True}
        if os.environ.get('CAMPUS_BROWSER_EXECUTABLE'):options['executable_path']=os.environ['CAMPUS_BROWSER_EXECUTABLE']
        cls.browser=getattr(cls.pw,cls.engine).launch(**options)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.server.server_close()
    def setUp(self):
        self.context=self.browser.new_context(viewport={'width':1440,'height':1000})
        self.page=self.context.new_page();self.errors=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
    def tearDown(self):
        try:self.assertEqual(self.errors,[])
        finally:self.context.close()
    def go(self,path='rutas.html'):self.page.goto(self.base+path,wait_until='networkidle')
    def stored(self,key=KEY):return self.page.evaluate('(k)=>localStorage.getItem(k)',key)
    def wait_completed(self,ids,page=None):
        page=page or self.page
        try:
            page.wait_for_function('''([key, ids]) => {
                const raw = localStorage.getItem(key);
                if (raw === null) return false;
                const completed = JSON.parse(raw).completed;
                return completed.length === ids.length && ids.every(id => completed.includes(id));
            }''',arg=[KEY,ids],timeout=5000)
        except BrowserTimeout:
            self.fail(f'Expected {ids}; stored {page.evaluate("k=>localStorage.getItem(k)",KEY)}')
    def wait_absent(self):self.page.wait_for_function('key=>localStorage.getItem(key)===null',arg=KEY)
    def peer(self,ignore_storage=False):
        page=self.context.new_page();page.on('pageerror',lambda e:self.errors.append(str(e)))
        if ignore_storage:page.add_init_script("window.addEventListener('storage',event=>event.stopImmediatePropagation(),true)")
        page.goto(self.base+'rutas.html',wait_until='networkidle');return page
    def hold_storage_lock(self):
        self.page.evaluate('''key=>new Promise(ready=>{
            navigator.locks.request(key+':write',{mode:'exclusive'},()=>new Promise(release=>{
                window.releaseRoutesLock=release;ready(true);
            }));
        })''',KEY)
    def wait_pending(self,count):
        self.page.wait_for_function('''async ([key,count])=>{
            const {pending}=await navigator.locks.query();
            return pending.filter(lock=>lock.name===key+':write').length===count;
        }''',arg=[KEY,count])
    def release_storage_lock(self):
        self.page.evaluate('window.releaseRoutesLock()')
        self.page.wait_for_function('''async key=>{
            const {held,pending}=await navigator.locks.query();
            return ![...held,...pending].some(lock=>lock.name===key+':write');
        }''',arg=KEY)
    def test_01_routes_and_dpd_filter(self):
        self.go();expect(self.page.locator('[data-route]:visible')).to_have_count(6)
        expect(self.page.locator('[data-phase]')).to_have_count(26)
        self.page.locator('#route-filter').select_option('dpd')
        expect(self.page.locator('[data-route]:visible')).to_have_count(1)
        expect(self.page.locator('[data-phase]:visible')).to_have_count(6)
        expect(self.page.locator('#ruta-dpd')).to_contain_text('128 h')
    def test_02_storage_requires_opt_in(self):
        self.go();self.page.locator('[data-phase]').first.check();self.assertIsNone(self.stored())
        self.page.reload();expect(self.page.locator('[data-phase]').first).not_to_be_checked()
        self.page.locator('[data-phase]').first.check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1'])
        self.assertEqual(len(json.loads(self.stored())['completed']),1)
        self.page.reload();expect(self.page.locator('[data-phase]').first).to_be_checked()
        self.page.locator('#remember-paths').uncheck();self.wait_absent();self.assertIsNone(self.stored())
    def test_03_clear_preserves_campus(self):
        self.go();self.page.evaluate('(k)=>localStorage.setItem(k,"synthetic-campus-fixture")',CAMPUS_KEY)
        self.page.locator('[data-phase]').first.check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1'])
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click()
        self.wait_absent();self.assertIsNone(self.stored());self.assertEqual(self.stored(CAMPUS_KEY),'synthetic-campus-fixture')
    def test_04_malformed_storage_is_ignored(self):
        self.go();self.page.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({schema:1,completed:["<script>"]}))',KEY)
        self.page.reload();expect(self.page.locator('#remember-paths')).not_to_be_checked()
        expect(self.page.locator('[data-phase]:checked')).to_have_count(0)
    def test_05_presentation_keyboard(self):
        self.go();self.page.locator('#start-presentation').click()
        expect(self.page.locator('#slide-count')).to_have_text('Ruta 1 de 6')
        self.page.keyboard.press('ArrowRight');expect(self.page.locator('#slide-count')).to_have_text('Ruta 2 de 6')
        self.page.keyboard.press('Escape');expect(self.page.locator('#start-presentation')).to_be_focused()
        expect(self.page.locator('[data-route]:visible')).to_have_count(6)
    def test_06_external_catalogue_and_current_exam_links(self):
        self.go();expect(self.page.locator('a[href="https://github.com/WiktorNykiel/fundamentos-ciberseguridad/tree/main/awesome-dpd"]')).to_be_visible()
        self.assertEqual(0,self.page.locator('a[href^="dpd/"]').count())
        response=self.page.request.get(self.base+'examen/questions.json')
        self.assertTrue(response.ok);self.assertEqual(100,len(response.json()['questions']))
        self.page.locator('a[href="examen/"]').click();self.assertIn('/examen/',self.page.url)
    def test_07_responsive_and_local_requests(self):
        remote=[];self.page.on('request',lambda req:remote.append(req.url) if not req.url.startswith(self.base) else None)
        out=HERE/'qa/current'/self.engine/'screenshots';out.mkdir(parents=True,exist_ok=True)
        for path in ('rutas.html',):
            for width in (320,360,768,1440):
                self.page.set_viewport_size({'width':width,'height':960});self.go(path)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(path,width))
                if width in (360,1440):self.page.screenshot(path=str(out/f'{path.replace("/","-")}-{width}.png'),full_page=False)
        self.assertEqual(remote,[])
    def test_08_without_javascript(self):
        context=self.browser.new_context(java_script_enabled=False);self.addCleanup(context.close)
        p=context.new_page();p.goto(self.base+'rutas.html');expect(p.locator('[data-route]')).to_have_count(6)
        expect(p.locator('[data-phase]')).to_have_count(26);expect(p.locator('h1')).to_be_visible()
    def test_09_latest_intent_preserves_other_tab_changes_without_reviving_a_deleted_record(self):
        self.go();self.page.locator('[data-phase]').nth(0).check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1'])
        other=self.context.new_page();other.add_init_script("window.addEventListener('storage',event=>event.stopImmediatePropagation(),true)")
        other.goto(self.base+'rutas.html');self.page.locator('[data-phase]').nth(1).check();other.locator('[data-phase]').nth(2).check()
        self.wait_completed(['no-tecnico-1','no-tecnico-2','no-tecnico-3'])
        self.assertEqual(['no-tecnico-1','no-tecnico-2','no-tecnico-3'],json.loads(self.stored())['completed'])
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click();self.wait_absent();other.locator('[data-phase]').nth(3).check()
        self.assertIsNone(self.stored());expect(other.locator('#remember-paths')).not_to_be_checked()
        other.locator('#remember-paths').check();self.wait_completed(['no-tecnico-4']);self.assertEqual(['no-tecnico-4'],json.loads(self.stored())['completed'])
        other.close()
    def test_10_interleaved_tabs_preserve_both_deliberate_marks(self):
        self.go();self.page.locator('#remember-paths').check();self.wait_completed([])
        with self.page.expect_popup() as opened:
            self.page.evaluate("window.routesPeer = window.open('rutas.html', '_blank')")
        other=opened.value;other.on('pageerror',lambda e:self.errors.append(str(e)))
        other.wait_for_load_state('networkidle')
        self.page.evaluate('''key => {
            const get = Storage.prototype.getItem;
            let interleave = true;
            Storage.prototype.getItem = function(name) {
                const raw = get.call(this, name);
                if (name === key && interleave) {
                    interleave = false;
                    // Deliver the peer's real UI action after this read, before its write.
                    // Values and synchronous storage semantics stay unchanged.
                    window.routesPeer.document.querySelector('[data-phase="no-tecnico-2"]').click();
                }
                return raw;
            };
        }''',KEY)
        self.page.locator('[data-phase="no-tecnico-1"]').check()
        self.wait_completed(['no-tecnico-1','no-tecnico-2'])
        self.wait_completed(['no-tecnico-1','no-tecnico-2'],other)
        other.close()
    def test_11_simultaneous_pending_writes_merge_after_the_exclusive_lock(self):
        self.go();self.page.locator('#remember-paths').check();self.wait_completed([])
        other=self.peer(ignore_storage=True);self.hold_storage_lock()
        self.page.locator('[data-phase="no-tecnico-1"]').check()
        other.locator('[data-phase="no-tecnico-2"]').check()
        self.page.locator('[data-phase="no-tecnico-3"]').check()
        other.locator('[data-phase="no-tecnico-4"]').check()
        self.wait_pending(4);self.wait_completed([]);self.release_storage_lock()
        self.wait_completed(['no-tecnico-1','no-tecnico-2','no-tecnico-3','no-tecnico-4'])
        expect(self.page.locator('[data-phase="no-tecnico-1"]')).to_be_checked()
        expect(other.locator('[data-phase="no-tecnico-4"]')).to_be_checked()
    def test_12_rapid_toggle_keeps_latest_intent_without_erasing_a_peer_mark(self):
        self.go();self.page.locator('#remember-paths').check();self.wait_completed([])
        other=self.peer(ignore_storage=True);self.hold_storage_lock()
        phase=self.page.locator('[data-phase="no-tecnico-1"]')
        phase.check();other.locator('[data-phase="no-tecnico-2"]').check();phase.uncheck()
        self.wait_pending(3);expect(phase).not_to_be_checked();self.release_storage_lock()
        self.wait_completed(['no-tecnico-2']);expect(phase).not_to_be_checked()
    def test_13_cancel_pending_opt_in_does_not_create_a_saved_record(self):
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.hold_storage_lock()
        self.page.locator('#remember-paths').check();self.page.locator('#remember-paths').uncheck()
        self.wait_pending(2);self.release_storage_lock();self.assertIsNone(self.stored())
        expect(self.page.locator('[data-phase="no-tecnico-1"]')).to_be_checked()
        expect(self.page.locator('#remember-paths')).not_to_be_checked()
    def test_14_new_opt_in_supersedes_an_older_cancelled_callback(self):
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.hold_storage_lock()
        remember=self.page.locator('#remember-paths');remember.check();remember.uncheck();remember.check()
        self.wait_pending(3);self.release_storage_lock();self.wait_completed(['no-tecnico-1'])
        expect(remember).to_be_checked();expect(self.page.locator('#path-status')).to_contain_text('Marcas guardadas')
    def test_15_clear_wins_over_this_tabs_pending_write(self):
        self.go();self.page.locator('#remember-paths').check();self.wait_completed([])
        self.hold_storage_lock();self.page.locator('[data-phase="no-tecnico-1"]').check()
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click()
        self.wait_pending(2);self.release_storage_lock();self.assertIsNone(self.stored())
        expect(self.page.locator('[data-phase]:checked')).to_have_count(0)
        expect(self.page.locator('#remember-paths')).not_to_be_checked()
    def test_16_peer_write_after_queued_delete_stays_in_memory(self):
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1']);other=self.peer(ignore_storage=True);self.hold_storage_lock()
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click()
        other.locator('[data-phase="no-tecnico-2"]').check();self.wait_pending(2);self.release_storage_lock()
        self.assertIsNone(self.stored());expect(other.locator('#remember-paths')).not_to_be_checked()
        expect(other.locator('[data-phase="no-tecnico-1"]')).not_to_be_checked()
        expect(other.locator('[data-phase="no-tecnico-2"]')).to_be_checked()
    def test_17_missed_delete_and_recreate_does_not_merge_an_old_lifetime(self):
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1']);old_id=json.loads(self.stored())['recordId'];other=self.peer(ignore_storage=True)
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click();self.wait_absent()
        self.page.locator('[data-phase="no-tecnico-2"]').check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-2']);new_id=json.loads(self.stored())['recordId'];self.assertNotEqual(old_id,new_id)
        other.locator('[data-phase="no-tecnico-3"]').check()
        expect(other.locator('#remember-paths')).not_to_be_checked();self.wait_completed(['no-tecnico-2'])
        self.assertEqual(new_id,json.loads(self.stored())['recordId'])
        expect(other.locator('[data-phase="no-tecnico-1"]')).not_to_be_checked()
        expect(other.locator('[data-phase="no-tecnico-3"]')).to_be_checked()
        other.locator('#remember-paths').check();self.wait_completed(['no-tecnico-2','no-tecnico-3'])
    def test_18_old_queued_delete_does_not_remove_a_new_lifetime(self):
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.page.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1']);old_id=json.loads(self.stored())['recordId'];other=self.peer(ignore_storage=True)
        self.hold_storage_lock();self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click()
        self.page.locator('[data-phase="no-tecnico-2"]').check();self.page.locator('#remember-paths').check()
        other.locator('#remember-paths').uncheck();self.wait_pending(3);self.release_storage_lock()
        self.wait_completed(['no-tecnico-2']);self.assertNotEqual(old_id,json.loads(self.stored())['recordId'])
        expect(other.locator('#path-status')).to_contain_text('registro nuevo')
    def test_19_other_tab_opt_in_does_not_enable_this_tabs_saving(self):
        self.go();other=self.peer();self.page.locator('[data-phase="no-tecnico-1"]').check()
        self.page.locator('#remember-paths').check();self.wait_completed(['no-tecnico-1'])
        expect(other.locator('#remember-paths')).not_to_be_checked();other.locator('[data-phase="no-tecnico-2"]').check()
        self.wait_completed(['no-tecnico-1']);other.locator('#remember-paths').check()
        self.wait_completed(['no-tecnico-1','no-tecnico-2'])
    def test_20_missing_web_locks_preserves_the_saved_copy_and_uses_memory(self):
        self.go();raw=json.dumps({'schema':1,'completed':['no-tecnico-1']})
        self.page.evaluate('([key,raw])=>localStorage.setItem(key,raw)',[KEY,raw])
        self.page.add_init_script("Object.defineProperty(navigator,'locks',{get(){return undefined;}})")
        self.page.reload();expect(self.page.locator('#remember-paths')).not_to_be_checked()
        expect(self.page.locator('[data-phase="no-tecnico-1"]')).to_be_checked()
        self.page.locator('[data-phase="no-tecnico-2"]').check();self.page.locator('#remember-paths').click()
        expect(self.page.locator('#remember-paths')).not_to_be_checked()
        expect(self.page.locator('#path-status')).to_contain_text('visita');self.assertEqual(raw,self.stored())
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click()
        expect(self.page.locator('[data-phase]:checked')).to_have_count(0)
        expect(self.page.locator('#path-status')).to_contain_text('No fue posible eliminar');self.assertEqual(raw,self.stored())
    def test_21_denied_storage_keeps_the_current_draft_usable(self):
        self.page.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied','SecurityError');}})")
        self.go();self.page.locator('[data-phase="no-tecnico-1"]').check();self.page.locator('#remember-paths').click()
        expect(self.page.locator('#remember-paths')).not_to_be_checked()
        expect(self.page.locator('[data-phase="no-tecnico-1"]')).to_be_checked()
        expect(self.page.locator('#path-status')).to_contain_text('visita')
    def test_22_legacy_v1_record_remains_compatible_until_recreated(self):
        self.go();self.page.evaluate('(key)=>localStorage.setItem(key,JSON.stringify({schema:1,completed:["no-tecnico-1"]}))',KEY)
        self.page.reload();other=self.peer(ignore_storage=True);self.hold_storage_lock()
        self.page.locator('[data-phase="no-tecnico-2"]').check();other.locator('[data-phase="no-tecnico-3"]').check()
        self.wait_pending(2);self.release_storage_lock();self.wait_completed(['no-tecnico-1','no-tecnico-2','no-tecnico-3'])
        self.assertEqual('legacy',json.loads(self.stored())['recordId'])
    def test_23_cancel_clear_keeps_the_pending_write_and_record(self):
        self.go();self.page.locator('#remember-paths').check();self.wait_completed([]);self.hold_storage_lock()
        self.page.locator('[data-phase="no-tecnico-1"]').check();self.page.once('dialog',lambda d:d.dismiss())
        self.page.locator('#clear-paths').click();self.wait_pending(1);self.release_storage_lock()
        self.wait_completed(['no-tecnico-1']);expect(self.page.locator('#remember-paths')).to_be_checked()
    def test_24_clear_can_remove_the_corrupt_record_that_was_observed(self):
        self.go();self.page.evaluate('key=>localStorage.setItem(key,"{broken json")',KEY);self.page.reload()
        self.page.once('dialog',lambda d:d.accept());self.page.locator('#clear-paths').click();self.wait_absent()
        expect(self.page.locator('#path-status')).to_contain_text('Marcas de rutas borradas')
if __name__=='__main__':unittest.main(verbosity=2)
