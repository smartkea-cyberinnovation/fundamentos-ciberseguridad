"""Mathematical contrast and markup checks; not WCAG conformance testing."""
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def luminance(code):
    rgb=[int(code[i:i+2],16)/255 for i in (1,3,5)]
    values=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
    return sum(a*b for a,b in zip(values,(.2126,.7152,.0722)))
def contrast(a,b):
    hi,lo=sorted((luminance(a),luminance(b)),reverse=True);return (hi+.05)/(lo+.05)
class DesignTests(unittest.TestCase):
    def test_body_text_contrast(self):self.assertGreaterEqual(contrast('#23252b','#ffffff'),7)
    def test_muted_text_contrast(self):self.assertGreaterEqual(contrast('#555b66','#f7f6f4'),4.5)
    def test_white_button_text_contrast(self):self.assertGreaterEqual(contrast('#ffffff','#b0142f'),4.5)
    def test_link_contrast(self):self.assertGreaterEqual(contrast('#870b23','#ffffff'),4.5)
    def test_layout_has_reduced_motion_and_small_screen_rules(self):
        css=(ROOT/'assets/styles.css').read_text();self.assertIn('prefers-reduced-motion',css);self.assertIn('max-width:360px',css);self.assertIn('min-height:44px',css)
    def test_no_external_font_or_institutional_brand(self):
        html=(ROOT/'index.html').read_text();css=(ROOT/'assets/styles.css').read_text()
        self.assertIn('brand-mark',html);self.assertNotIn('@import',css);self.assertNotIn('fonts.googleapis',html+css)
    def test_skip_link_and_dialog_labels_present(self):
        html=(ROOT/'index.html').read_text();self.assertIn('class="skip-link"',html);self.assertIn('aria-labelledby="slide-heading"',html)
if __name__=='__main__':unittest.main()
