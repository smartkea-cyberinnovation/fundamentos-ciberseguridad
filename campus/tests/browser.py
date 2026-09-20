"""Aceptación funcional con Chromium sobre el curso real compilado."""
import json
import os
import re
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parents[1]
KEY='fundamentos-ciberseguridad:progress:v1'
class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((HERE/'dist/course.json').read_text(encoding='utf-8'))
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));cls.port=sock.getsockname()[1]
        cls.server=subprocess.Popen([sys.executable,str(HERE/'serve.py'),'--port',str(cls.port)],stdout=subprocess.DEVNULL)
        cls.base=f'http://127.0.0.1:{cls.port}'
        for _ in range(60):
            try:
                with socket.create_connection(('127.0.0.1',cls.port),timeout=.2):break
            except OSError:time.sleep(.1)
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
        (HERE/'qa/screenshots').mkdir(parents=True,exist_ok=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.p.stop();cls.server.terminate();cls.server.wait(timeout=10)
    def setUp(self):
        self.context=self.browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
        self.page=self.context.new_page();self.errors=[];self.external=[]
        self.page.on('pageerror',lambda error:self.errors.append(str(error)))
        def route(r):
            if urlsplit(r.request.url).hostname not in ('127.0.0.1','localhost'):self.external.append(r.request.url);r.abort()
            else:r.continue_()
        self.page.route('**/*',route)
        self.page.goto(self.base);self.page.get_by_role('heading',name=re.compile('Entiende el sistema')).wait_for()
    def tearDown(self):
        self.assertEqual(self.errors,[]);self.assertEqual(self.external,[]);self.context.close()
    def goto(self,fragment):
        self.page.goto(self.base+'/'+fragment);self.page.wait_for_timeout(180)
    def state(self):return self.page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
    def test_01_dashboard(self):
        self.assertEqual(self.page.locator('.block-card').count(),7)
        self.page.screenshot(path=str(HERE/'qa/screenshots/01-inicio.png'),full_page=True)
    def test_02_navigation_and_read(self):
        self.goto('#/modulo/M05');self.page.locator('#read-check').check();self.page.reload();self.page.locator('#read-check').wait_for()
        self.assertTrue(self.page.locator('#read-check').is_checked());self.assertTrue(self.state()['modules']['M05']['read'])
        self.page.screenshot(path=str(HERE/'qa/screenshots/05-lectura.png'),full_page=True)
    def test_03_notes_are_text(self):
        self.goto('#/modulo/M05');self.page.locator('#notes').fill('<img src=x onerror=alert(1)> nota de prueba');self.page.reload();self.page.locator('#notes').wait_for()
        self.assertIn('<img',self.page.locator('#notes').input_value());self.assertEqual(self.page.locator('img[src=x]').count(),0)
    def test_04_quiz(self):
        self.goto('#/modulo/M05/revision');q=self.data['modules'][4]['quiz']
        self.page.locator(f'input[name=answer][value="{q["correct"]}"]').check();self.page.get_by_role('button',name='Comprobar respuesta',exact=True).click()
        self.assertTrue(self.state()['modules']['M05']['quiz'])
    def test_05_wizard(self):
        self.goto('#/modulo/M05/practica/L05A')
        for _ in range(5):self.page.locator('[data-action=step-done]').click()
        self.page.get_by_role('button',name='Completar práctica',exact=True).click()
        self.assertTrue(self.state()['labs']['L05A']['done'])
        self.page.screenshot(path=str(HERE/'qa/screenshots/03-practica.png'),full_page=True)
    def test_06_search(self):
        self.page.locator('#global-search').fill('PowerShell');self.page.get_by_role('heading',name='Resultados de búsqueda.').wait_for()
        self.assertGreater(self.page.locator('.search-result').count(),0)
        self.page.locator('#global-search').fill('<img src=x>');self.page.wait_for_timeout(300)
        self.assertEqual(self.page.locator('img[src=x]').count(),0)
    def test_07_presentation_keyboard(self):
        self.goto('#/modulo/M05');self.page.get_by_role('button',name=re.compile('Modo presentación')).click()
        self.page.locator('#presentation').wait_for(state='visible');first=self.page.locator('#slide-counter').inner_text()
        self.page.keyboard.press('ArrowRight');self.assertNotEqual(self.page.locator('#slide-counter').inner_text(),first)
        self.assertFalse(self.page.locator('#slide-content > h3').first.is_visible())
        self.page.screenshot(path=str(HERE/'qa/screenshots/02-presentacion.png'))
        self.page.keyboard.press('Escape');self.assertFalse(self.page.locator('#presentation').is_visible())
    def test_08_export_and_reset(self):
        self.goto('#/modulo/M01');self.page.locator('#read-check').check();self.goto('#/progreso')
        with self.page.expect_download() as info:self.page.get_by_role('button',name='Exportar progreso').click()
        data=json.loads(Path(info.value.path()).read_text());self.assertTrue(data['modules']['M01']['read'])
        self.page.get_by_role('button',name='Reiniciar',exact=True).click();self.page.get_by_role('button',name='Borrar mi progreso',exact=True).click()
        self.assertFalse(self.state()['modules']['M01']['read'])
    def test_09_import_rejects_unknown_course(self):
        self.goto('#/modulo/M01');before=self.state();bad={**before,'courseId':'otro'};self.goto('#/progreso')
        self.page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
        self.page.wait_for_timeout(120);self.assertIn('No se importó',self.page.locator('#status').inner_text())
        self.assertEqual(self.state()['courseId'],before['courseId'])
    def test_10_mobile(self):
        self.page.set_viewport_size({'width':390,'height':844});self.goto('#/modulo/M05')
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),391)
        self.page.locator('#menu-toggle').click();self.assertTrue(self.page.locator('#sidebar').is_visible())
        self.page.locator('#menu-toggle').click();self.page.screenshot(path=str(HERE/'qa/screenshots/04-movil.png'),full_page=True)
    def test_11_resources(self):
        self.goto('#/recursos');self.assertGreater(self.page.locator('.resource-grid a').count(),5)
        self.page.locator('.resource-grid a').first.click()
        article=self.page.locator('#main article.prose');article.wait_for()
        self.assertGreater(len(article.inner_text()),100)
    def test_12_bad_route(self):
        self.goto('#/modulo/M99');self.assertTrue(self.page.get_by_role('heading',name='No se encontró esa sección').is_visible())
    def test_13_skip_link_preserves_route(self):
        self.goto('#/modulo/M05');self.page.locator('.skip-link').focus();self.page.keyboard.press('Enter')
        self.assertIn('#/modulo/M05',self.page.url);self.assertEqual(self.page.evaluate('document.activeElement.id'),'main')
    def test_14_csp(self):
        response=self.page.request.get(self.base)
        self.assertIn("script-src 'self'",response.headers['content-security-policy'])
        self.assertNotIn('unsafe-inline',response.headers['content-security-policy'])
    def test_15_all_links_have_text(self):
        self.assertEqual(self.page.locator('a').evaluate_all('(els)=>els.filter(e=>!e.textContent.trim()&&!e.getAttribute("aria-label")).length'),0)
    def test_16_import_roundtrip(self):
        self.goto('#/modulo/M01');s=self.state();s['modules']['M02']['read']=True;self.goto('#/progreso')
        self.page.once('dialog',lambda d:d.accept())
        self.page.locator('#import-file').set_input_files({'name':'progress.json','mimeType':'application/json','buffer':json.dumps(s).encode()})
        self.page.wait_for_timeout(150);self.assertTrue(self.state()['modules']['M02']['read'])
    def test_17_internal_reference(self):
        self.goto('#/modulo/M05');self.page.locator('#theory a[href^="#/recurso/"]').first.click()
        self.page.locator('#main article.prose').wait_for();self.assertIn('#/recurso/',self.page.url)
    def test_18_resume(self):
        self.goto('#/modulo/M05');self.page.locator('#read-check').check();self.goto('#/curso')
        self.page.get_by_role('link',name=re.compile('Continuar mi recorrido')).click()
        self.page.locator('#read-check').wait_for();self.assertIn('#/modulo/M05',self.page.url)
    def test_19_continuous_reading(self):
        self.page.goto(self.base+'/lectura.html')
        self.assertEqual(self.page.locator('article[id^=M]').count(),32)
        self.assertEqual(self.page.locator('article[id^=D]').count(),len(self.data['resources']))
        self.assertEqual(self.page.locator('script').count(),0)
    def test_20_manual_result_check(self):
        self.goto('#/modulo/M05/practica/L05A')
        self.page.locator('[data-action=step][data-step="2"]').click()
        self.page.locator('[name=files]').fill('8');self.page.locator('[name=bytes]').fill('62')
        self.page.get_by_role('button',name='Contrastar cantidades').click()
        self.assertIn('Coincide con R01',self.page.locator('#result-feedback').inner_text())
        self.assertFalse(self.state()['labs']['L05A']['done'])
    def test_21_tabs_do_not_echo_storage_updates(self):
        self.goto('#/modulo/M05')
        other=self.context.new_page()
        other.goto(self.base+'/#/modulo/M06')
        other.locator('#read-check').wait_for()
        self.page.evaluate("window.storageEvents=0; window.addEventListener('storage',()=>window.storageEvents++)")
        other.evaluate("window.storageEvents=0; window.addEventListener('storage',()=>window.storageEvents++)")
        self.page.locator('#read-check').check()
        self.page.wait_for_timeout(500)
        events=self.page.evaluate('window.storageEvents')+other.evaluate('window.storageEvents')
        self.assertLessEqual(events,4,'A storage event must not be written back to other tabs')
        self.assertTrue(other.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).modules.M05.read',KEY))
        self.assertEqual(self.state()['lastRoute'],'#/modulo/M05')
        other.close()
    def test_22_completed_wizard_reopens_at_closure(self):
        self.goto('#/modulo/M05/practica/L05A')
        for _ in range(5):
            self.page.locator('[data-action=step-done]').click()
        self.page.reload()
        self.page.locator('[data-action=step-done]').wait_for()
        self.assertEqual(self.page.locator('[data-action=step][aria-current=step]').get_attribute('data-step'),'4')
    def test_23_unicode_export_can_be_imported(self):
        self.goto('#/modulo/M01')
        state=self.state()
        for module in state['modules'].values():module['notes']='界'*3000
        payload=json.dumps(state,ensure_ascii=False).encode('utf-8')
        self.assertGreater(len(payload),200000)
        self.goto('#/progreso')
        self.page.once('dialog',lambda d:d.accept())
        self.page.locator('#import-file').set_input_files({'name':'unicode-progress.json','mimeType':'application/json','buffer':payload})
        self.page.wait_for_timeout(150)
        self.assertEqual(self.state()['modules']['M32']['notes'],'界'*3000)
    def test_24_outline(self):
        self.goto('#/temario')
        self.assertEqual(self.page.locator('.outline-table tbody tr').count(),32)
        self.page.locator('tr[data-module=M16] a').first.click()
        self.assertIn('#/modulo/M16',self.page.url)
    def test_25_onboarding(self):
        self.goto('#/empezar')
        self.assertTrue(self.page.get_by_role('heading',name='Empieza por aquí.').is_visible())
        self.page.get_by_role('link',name='Guía de estudio completa').click()
        self.page.locator('#main article.prose').wait_for()
    def test_26_multiterm_search(self):
        self.page.locator('#global-search').fill('Linux permisos')
        self.page.get_by_role('heading',name='Resultados de búsqueda.').wait_for()
        self.assertGreater(self.page.locator('.search-result').count(),0)
    def test_27_resume_review_tab(self):
        self.goto('#/modulo/M05/revision')
        self.assertEqual(self.state()['lastRoute'],'#/modulo/M05/revision')
        self.page.reload();self.page.locator('#main h1').wait_for()
        self.assertEqual(self.state()['lastRoute'],'#/modulo/M05/revision')
    def test_28_cross_tab_continuation_is_local(self):
        self.goto('#/modulo/M05')
        other=self.context.new_page();other.goto(self.base+'/#/modulo/M06')
        other.locator('#read-check').wait_for()
        other.locator('#read-check').check();self.page.wait_for_timeout(200)
        self.goto('#/curso')
        self.assertIn('/M05',self.page.get_by_role('link',name=re.compile('Continuar mi recorrido')).get_attribute('href'))
        other.close()
    def test_29_mobile_outline(self):
        self.page.set_viewport_size({'width':390,'height':844});self.goto('#/temario')
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),391)
        self.page.screenshot(path=str(HERE/'qa/screenshots/06-indice-movil.png'),full_page=True)
    def test_30_intro_does_not_change_resume(self):
        self.goto('#/modulo/M05/practicas');self.goto('#/empezar')
        self.assertEqual(self.state()['lastRoute'],'#/modulo/M05/practicas')
    def test_31_cross_tab_resume_survives_dashboard_reload(self):
        self.goto('#/modulo/M05')
        self.page.locator('#read-check').check()
        self.goto('#/curso')
        other=self.context.new_page();other.goto(self.base+'/#/modulo/M06')
        other.locator('#read-check').check()
        self.page.wait_for_timeout(200)
        self.page.reload()
        self.page.get_by_role('heading',name=re.compile('Entiende el sistema')).wait_for()
        self.assertIn('/M05',self.page.get_by_role('link',name=re.compile('Continuar mi recorrido')).get_attribute('href'))
        other.close()
if __name__=='__main__':unittest.main(verbosity=2)
