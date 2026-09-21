"""Structural and semantic coverage checks; not evidence of native lab execution."""
import re
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build
from bilingual import collect_en
from operations import READINGS, RELATED, add_resources, related_reading

class OperationalContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es=build.collect()
        cls.en=collect_en(cls.es,build.HERE/'locales/en',build.markdown,build.read_text)
    def operational(self,data):
        return [r for r in data['resources'] if r['id'] in {x[0] for x in READINGS}]
    def resource(self,data,rid):
        return next(r for r in data['resources'] if r['id']==rid)
    def test_append_only_ids(self):
        for data in (self.es,self.en):
            self.assertEqual([r['id'] for r in data['resources']],[f'D{i:02}' for i in range(1,37)])
    def test_old_library_tail_is_unchanged(self):
        tail=[r['source'].split('/')[-1] for r in self.es['resources'][18:21]]
        self.assertEqual(tail,['PLAN-DOCENTE.md','COMO-ESTUDIAR.md','DESPLIEGUE-ESTATICO.md'])
    def test_no_new_hours_or_core_lab_ids(self):
        for data in (self.es,self.en):
            self.assertEqual(data['hours'],480)
            self.assertEqual([m['id'] for m in data['modules']],[f'M{i:02}' for i in range(1,33)])
            self.assertEqual([l['id'] for m in data['modules'] for l in m['labs']],
                             [f'L{i:02}{s}' for i in range(1,33) for s in 'ABC'])
    def test_operational_resources_are_substantive(self):
        for data in (self.es,self.en):
            for r in self.operational(data):
                self.assertGreater(len(r['html']),6000,r['id'])
                self.assertGreaterEqual(len(r['toc']),6,r['id'])
                self.assertTrue(r['slides']);self.assertNotIn('<h1',r['html'])
    def test_links_resolve_to_resources(self):
        for data in (self.es,self.en):
            ids={r['id'] for r in data['resources']}
            for r in self.operational(data):
                for rid in re.findall(r'href="#/recurso/(D\d{2})"',r['html']):self.assertIn(rid,ids)
    def test_sixteen_control_ids_in_both_languages(self):
        for data in (self.es,self.en):
            r=self.resource(data,'D25')
            self.assertEqual(set(re.findall(r'\bOS-\d{2}\b',r['html'])),{f'OS-{i:02}' for i in range(1,17)})
    def test_twelve_laboratory_designs_in_both_languages(self):
        for data in (self.es,self.en):
            r=self.resource(data,'D25')
            self.assertEqual(set(re.findall(r'\bOPS-L\d{2}\b',r['html'])),{f'OPS-L{i:02}' for i in range(1,13)})
    def test_eight_browsing_policy_ids(self):
        for data in (self.es,self.en):
            self.assertEqual(set(re.findall(r'\bNAV-\d{2}\b',self.resource(data,'D24')['html'])),{f'NAV-{i:02}' for i in range(1,9)})
    def test_context_links_in_relevant_modules(self):
        for data in (self.es,self.en):
            for m in data['modules']:
                for rid in RELATED.get(m['id'],[]):self.assertIn(f'href="#/recurso/{rid}"',m['html'])
    def test_missing_translation_fails_closed(self):
        def read(path):return '' if path.name=='operations-control.md' else build.read_text(path)
        with self.assertRaises(ValueError):collect_en(self.es,build.HERE/'locales/en',build.markdown,read)
    def test_reordered_base_refused(self):
        with self.assertRaises(ValueError):add_resources([],build.COURSE,build.ROOT,build.REPO,build.markdown,build.read_text)
    def test_unknown_language_refused(self):
        with self.assertRaises(ValueError):related_reading('M18','xx')
    def test_content_covers_non_equivalence_and_privacy(self):
        for data in (self.es,self.en):
            text=' '.join(r['html'] for r in self.operational(data))
            for term in ('LDAP','AD DS','Entra','SSSD','LAPS','TCC','SMB','NFS','WinHTTP','BYOD','E2EE','TLS','QUIC','LOPDGDD'):
                self.assertIn(term,text)

if __name__=='__main__':unittest.main()
