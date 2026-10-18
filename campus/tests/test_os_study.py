"""OS learning content and build invariants, without pretending to run native labs."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from os_classroom.build import catalog, build_into, render_reading, LESSONS
from os_classroom.schema import B, quiz

class OSStudy(unittest.TestCase):
    def test_complete_paths(self):
        data=catalog('es'); self.assertEqual(28,len(data['lessons']))
        self.assertEqual({'common':4,'linux':8,'windows':8,'macos':8}, {g:sum(x['group']==g for x in data['lessons']) for g in ['common','linux','windows','macos']})
    def test_language_parity(self):
        for a,b in zip(catalog('es')['lessons'],catalog('en')['lessons']):
            self.assertEqual(a['id'],b['id']); self.assertEqual([v['id'] for v in a['views']],[v['id'] for v in b['views']])
            self.assertEqual(a['example']['command'],b['example']['command'])
    def test_one_concept_per_view(self):
        for l in catalog('es')['lessons']:
            self.assertEqual(3,sum(v['kind']=='concept' for v in l['views']))
            self.assertEqual(3,sum(v['kind']=='micro' for v in l['views']))
            for i,v in enumerate(l['views']):
                if v['kind']=='concept':self.assertEqual('micro',l['views'][i+1]['kind'])
    def test_readings_substantial(self):
        for l in catalog('en')['lessons']:
            for c in l['concepts']:self.assertGreater(len(c['body'].split()),30)
    def test_complete_lab_contract(self):
        for l in catalog('es')['lessons']:
            for key in ['environment','evidence','success','recovery','symptom','hint']:self.assertTrue(l['lab'][key])
            self.assertGreaterEqual(len(l['lab']['steps']),3)
            for s in l['lab']['steps']:self.assertTrue(s['title'] and s['expected'])
    def test_sources_https(self):
        for l in catalog('en')['lessons']:
            self.assertTrue(l['sources'])
            for r in l['sources']:self.assertTrue(r['url'].startswith('https://'))
    def test_stable_unique_view_ids(self):
        data=catalog('es');ids=[v['id'] for l in data['lessons'] for v in l['views']]
        self.assertEqual(len(ids),len(set(ids)))
    def test_missing_language_rejected(self):
        with self.assertRaises(ValueError):B('real','')
    def test_bad_quiz_rejected(self):
        with self.assertRaises(ValueError):quiz(B('q','q'),[B('a','a')],2,B('e','e'))
    def test_build_has_readers_and_no_external_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);build_into(root);out=root/'sistemas'
            self.assertTrue((out/'reading.es.html').is_file());self.assertTrue((out/'reading.en.html').is_file())
            self.assertEqual(28,len(json.loads((out/'course.en.json').read_text())['lessons']))
            self.assertNotIn('src="https://',(out/'index.html').read_text())
    def test_reading_html_escapes_content(self):
        data=copy.deepcopy(catalog('es'));data['lessons'][0]['views'][0]['body']='<script>alert(1)</script>'
        text=render_reading(data);self.assertIn('&lt;script&gt;',text);self.assertNotIn('<script>alert',text)
    def test_unknown_language_rejected(self):
        with self.assertRaises(ValueError):catalog('xx')
    def test_both_editions_have_recovery_and_handover(self):
        for lang in ['es','en']:
            for l in catalog(lang)['lessons']:
                self.assertEqual(['recovery','handover'],[v['kind'] for v in l['views'][-2:]])
    def test_no_modification_of_core_catalog(self):
        self.assertTrue(all(x['id'].startswith('OS-') for x in LESSONS))
        self.assertTrue(all('hours' not in x for x in LESSONS))

if __name__=='__main__':unittest.main()
