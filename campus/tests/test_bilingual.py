"""Translation structure tests; these do not certify human translation quality."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from bilingual import chunks,collect_en

class BilingualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es=build.collect()
        cls.en=collect_en(cls.es,build.HERE/'locales/en',build.markdown,build.read_text)
    def test_module_identity_parity(self):
        self.assertEqual([m['id'] for m in self.es['modules']],[m['id'] for m in self.en['modules']])
    def test_96_labs_are_translated_and_keep_hours(self):
        es=[l for m in self.es['modules'] for l in m['labs']];en=[l for m in self.en['modules'] for l in m['labs']]
        self.assertEqual(len(en),96)
        self.assertEqual([(l['id'],l['hours']) for l in es],[(l['id'],l['hours']) for l in en])
    def test_every_translated_lab_has_five_substantive_fields(self):
        for m in self.en['modules']:
            for l in m['labs']:
                for field in ('environment','tasks','evidence','success','recovery'):
                    self.assertGreater(len(l[field]),10,(l['id'],field))
    def test_hours_and_prerequisites_unchanged(self):
        self.assertEqual(sum(m['hours'] for m in self.en['modules']),480)
        for es,en in zip(self.es['modules'],self.en['modules']):
            for key in ('prerequisites','hours','theoryHours','practiceHours','block'):self.assertEqual(es[key],en[key])
    def test_every_module_has_theory_toc_slides(self):
        for m in self.en['modules']:
            self.assertGreater(len(m['html']),600,m['id']);self.assertTrue(m['toc']);self.assertTrue(m['slides'])
    def test_resources_ids_and_text_present(self):
        self.assertEqual(len(self.en['resources']),40)
        self.assertEqual(len(self.es['resources']),40)
        for es,en in zip(self.es['resources'],self.en['resources']):
            self.assertEqual(es['id'],en['id']);self.assertGreater(len(en['html']),300)
    def test_all_eight_extended_guides_translated(self):
        guides=[l for m in self.en['modules'] for l in m['labs'] if 'guide' in l]
        self.assertEqual(len(guides),8)
        for l in guides:self.assertGreater(len(l['guide']['html']),300)
    def test_quiz_answer_positions_match_spanish(self):
        for es,en in zip(self.es['modules'],self.en['modules']):
            q=en['quiz'];self.assertEqual(q['correct'],es['quiz']['correct']);self.assertEqual(len(q['options']),3)
            self.assertEqual(len(set(q['options'])),3);self.assertEqual(q['options'][q['correct']],q['explanation'])
    def test_missing_translation_stops_build(self):
        def read(p):return '' if p.name=='windows-macos.md' else build.read_text(p)
        with self.assertRaises(ValueError):collect_en(self.es,build.HERE/'locales/en',build.markdown,read)
    def test_missing_reference_stops_build(self):
        es=copy.deepcopy(self.es);es['resources'].append({'id':'D99'})
        with self.assertRaises(ValueError):collect_en(es,build.HERE/'locales/en',build.markdown,build.read_text)
    def test_duplicate_translated_identifier_rejected(self):
        with self.assertRaises(ValueError):chunks('# M01 · A\ntext\n# M01 · B',r'^# (M\d{2}) · ')
    def test_unknown_quiz_rejected(self):
        def read(p):return build.read_text(p)+('\nM99\tx\ta\tb\tc' if p.name=='quizzes.tsv' else '')
        with self.assertRaises(ValueError):collect_en(self.es,build.HERE/'locales/en',build.markdown,read)
    def test_active_editions_keep_independent_repository_identity(self):
        for course in (self.es,self.en):
            self.assertEqual(course['repository'],'https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad')
    def test_header_targets_exist_in_each_module(self):
        for course in (self.es,self.en):
            for m in course['modules']:
                ids=set(re.findall(r'\bid="([^"]+)"',m['html']))
                for entry in m['toc']:self.assertIn(entry['id'],ids)

if __name__=='__main__':unittest.main()
