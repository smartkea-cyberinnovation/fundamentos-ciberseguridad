"""Full inherited browser acceptance plus the new index/deployment cases."""
import unittest
import browser as base

class ExtendedBrowserTests(base.BrowserTests):
    def test_32_outline_filter_by_block(self):
        self.goto('#/temario')
        self.page.locator('#outline-block').select_option('linux')
        self.assertEqual(self.page.locator('[data-outline-row]:visible').count(),8)
        self.assertIn('8 de 32',self.page.locator('#outline-count').inner_text())
    def test_33_outline_query_and_empty(self):
        self.goto('#/temario')
        self.page.locator('#outline-query').fill('M05')
        self.assertGreater(self.page.locator('[data-outline-row]:visible').count(),0)
        self.page.locator('#outline-query').fill('terminoimposible123')
        self.assertTrue(self.page.locator('#outline-empty').is_visible())
        self.page.locator('#outline-reset').click()
        self.assertEqual(self.page.locator('[data-outline-row]:visible').count(),32)
    def test_34_outline_progress(self):
        self.goto('#/modulo/M05');self.page.locator('#read-check').check()
        self.goto('#/temario');self.page.locator('#outline-status').select_option('started')
        self.assertEqual(self.page.locator('[data-outline-row]:visible').count(),1)
        self.assertIn('M05',self.page.locator('[data-outline-row]:visible').inner_text())
    def test_35_deployment_lesson(self):
        self.goto('#/recurso/D21')
        self.assertIn('Pages y Workers',self.page.locator('#main').inner_text())
        self.assertIn('cloudflare.py',self.page.locator('#main').inner_text())
    def test_36_mobile_filters(self):
        self.page.set_viewport_size({'width':390,'height':844});self.goto('#/temario')
        self.page.locator('#outline-block').select_option('macos')
        self.assertEqual(self.page.locator('[data-outline-row]:visible').count(),4)
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),391)
        self.page.screenshot(path=str(base.HERE/'qa/screenshots/06-indice-filtros-movil.png'),full_page=True)
    def test_37_block_jump_clears_conflicting_filters(self):
        self.goto('#/temario')
        self.page.locator('#outline-block').select_option('macos')
        self.page.locator('#outline-query').fill('sincoincidencias123')
        self.page.locator('[data-scroll="outline-linux"]').click()
        self.assertEqual(self.page.locator('#outline-block').input_value(),'linux')
        self.assertEqual(self.page.locator('[data-outline-row]:visible').count(),8)
        self.assertEqual(self.page.locator('#outline-query').input_value(),'')


if __name__=="__main__":unittest.main(verbosity=2)
