"""Content and parser acceptance, not proof of native labs or legal compliance."""
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from bilingual import collect_en
from integral import READINGS, IDS, editions, add_resources, folder

class EditionParserTests(unittest.TestCase):
    SAMPLE='<!-- ES -->\n# Español\n\nTexto.\n<!-- EN -->\n# English\n\nText.'
    def test_both_editions(self):
        result=editions(self.SAMPLE)
        self.assertEqual(set(result),{'es','en'});self.assertIn('Texto.',result['es']);self.assertNotIn('Texto.',result['en'])
    def test_shared_references(self):
        data=editions(self.SAMPLE+'\n<!-- COMMON -->\nShared reference')
        for value in data.values():self.assertIn('Shared reference',value)
    def test_missing_english(self):
        with self.assertRaises(ValueError):editions('<!-- ES -->\n# Solo\n\nTexto')
    def test_duplicate_language(self):
        with self.assertRaises(ValueError):editions(self.SAMPLE+'<!-- EN -->')
    def test_invalid_order(self):
        with self.assertRaises(ValueError):editions('<!-- EN -->\n# English\n\ntext\n<!-- ES -->\n# Español\n\ntexto')
    def test_shared_before_english(self):
        with self.assertRaises(ValueError):editions(self.SAMPLE.replace('<!-- EN -->','<!-- COMMON -->\n<!-- EN -->'))
    def test_duplicate_shared(self):
        with self.assertRaises(ValueError):editions(self.SAMPLE+'<!-- COMMON --><!-- COMMON -->')
    def test_missing_title(self):
        with self.assertRaises(ValueError):editions(self.SAMPLE.replace('# English','English'))
    def test_changed_prior_ids_rejected(self):
        with self.assertRaises(ValueError):add_resources([],build.COURSE,build.ROOT,build.REPO,build.markdown,build.read_text)

class IntegralContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es=build.collect();cls.en=collect_en(cls.es,build.HERE/'locales/en',build.markdown,build.read_text)
        cls.raw={rid:editions(build.read_text(folder(build.COURSE)/name)) for rid,name in READINGS}
    def selected(self,data):return [r for r in data['resources'] if r['id'] in IDS]
    def test_stable_resource_order(self):
        for data in (self.es,self.en):self.assertEqual([r['id'] for r in data['resources']],[f'D{i:02}' for i in range(1,41)])
    def test_substantive_both_languages(self):
        for data in (self.es,self.en):
            for r in self.selected(data):
                if r['id'] not in {f'D{i:02}' for i in range(26,37)}:
                    continue
                self.assertGreater(len(r['html']),3500,r['id']);self.assertGreaterEqual(len(r['toc']),4,r['id'])
                self.assertTrue(r['slides']);self.assertNotIn('<!--',r['html']);self.assertNotIn('<h1',r['html'])
    def test_new_outlines_are_explicit_about_translation_scope(self):
        for rid,name in (('D37','12-curriculum.md'),('D38','13-ecosystem.md'),
                         ('D39','14-library.md'),('D40','15-master-glossary.md')):
            self.assertIn((rid,name),READINGS)
            es=next(r for r in self.es['resources'] if r['id']==rid)
            en=next(r for r in self.en['resources'] if r['id']==rid)
            self.assertGreaterEqual(len(es['toc']),4,rid)
            self.assertEqual(es['kind'],'Esquema de estudio')
            self.assertEqual(en['kind'],'English summary')
            self.assertIn('English summary',en['html'])
            self.assertIn('full English teaching edition is pending',en['html'])
            for resource in (es,en):
                self.assertGreater(len(resource['html']),300,rid)
                self.assertTrue(resource['slides'])
                self.assertNotIn('<!--',resource['html'])
                self.assertNotIn('<h1',resource['html'])
    def test_core_identity_and_hours(self):
        for data in (self.es,self.en):
            self.assertEqual(data['hours'],480)
            self.assertEqual([m['id'] for m in data['modules']],[f'M{i:02}' for i in range(1,33)])
            self.assertEqual([l['id'] for m in data['modules'] for l in m['labs']],[f'L{i:02}{s}' for i in range(1,33) for s in 'ABC'])
    def test_eighteen_unique_activity_designs(self):
        for language in ('es','en'):
            text='\n'.join(v[language] for v in self.raw.values())
            found=re.findall(r'\*\*(INT-L\d{2}):',text)
            self.assertEqual(sorted(found),[f'INT-L{i:02}' for i in range(1,19)])
    def test_thirty_six_glossary_entries(self):
        for language in ('es','en'):
            found=re.findall(r'^\| (INT-G\d{2}) \|',self.raw['D35'][language],re.M)
            self.assertEqual(found,[f'INT-G{i:02}' for i in range(1,37)])
    def test_reading_links_resolve(self):
        for data in (self.es,self.en):
            ids={r['id'] for r in data['resources']}
            for r in self.selected(data):
                for rid in re.findall(r'href="#/recurso/(D\d{2})"',r['html']):self.assertIn(rid,ids,(r['id'],rid))
    def test_source_registry_covers_references(self):
        for language in ('es','en'):
            sources=set(re.findall(r'^\| ([HTNWSIPCVR]\d{2}) \|',self.raw['D36'][language],re.M))
            self.assertGreaterEqual(len(sources),60)
            for rid,values in self.raw.items():
                if rid=='D36':continue
                refs=set(re.findall(r'\b([HTNWSIPCVR]\d{2})\b',values[language]))
                self.assertTrue(refs<=sources,(rid,refs-sources))
    def test_no_institutional_brand(self):
        for values in self.raw.values():
            for raw in values.values():self.assertNotIn('nebrija',raw.lower())
    def test_source_links_point_to_maintained_repository(self):
        for data in (self.es,self.en):
            for r in self.selected(data):self.assertTrue(r['source'].startswith(data['repository']+'/blob/main/formacion/itinerario-integral/'))
    def test_current_market_period_is_explicit(self):
        for language in ('es','en'):
            text=self.raw['D34'][language]
            self.assertIn('2025–2035',text);self.assertIn('21 %',text);self.assertIn('2025',text)
    def test_glossary_distinguishes_capability_and_product(self):
        for language in ('es','en'):
            for term in ('Intune','Purview','Presidio','TLP','BitLocker'):
                self.assertIn(term,self.raw['D32'][language])
    def test_missing_integral_language_fails_closed(self):
        def read(path):
            raw=build.read_text(path)
            return raw.replace('<!-- EN -->','') if path.name=='01-computing.md' else raw
        with self.assertRaises(ValueError):collect_en(self.es,build.HERE/'locales/en',build.markdown,read)

if __name__=='__main__':unittest.main(verbosity=2)
