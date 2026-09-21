"""Local tests use synthetic responses; live observations are a separate workflow."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import audit_publication as audit

class Response:
    def __init__(self,status,kind,body):
        self.status=status;self.headers={'Content-Type':kind};self.body=body
    def read(self,n):return self.body[:n]
    def __enter__(self):return self
    def __exit__(self,*args):pass

class PublicationTests(unittest.TestCase):
    def test_fixed_scope(self):
        self.assertEqual(len(audit.TARGETS),7)
        self.assertTrue(audit.BASE.startswith('https://smartkea.com/introduccion-ciberseguridad/'))
        for path,_,_ in audit.TARGETS:self.assertNotIn('..',path)
    def test_course_counts(self):
        data={'language':'en','version':'example','modules':[{'labs':[{},{}]}],'resources':[{}],'hours':14}
        result=audit.inspect_body('course.en.json',json.dumps(data).encode())
        self.assertEqual((result['modules'],result['labs'],result['resources']),(1,2,1))
    def test_build_fields_are_allowlisted(self):
        result=audit.inspect_body('build-info.json',b'{"version":"x","secret":"never-retained"}')
        self.assertEqual(result['build'],{'version':'x'})
    def test_redirect_is_not_followed(self):
        self.assertIsNone(audit.NoRedirect().redirect_request(None,None,302,'',{},'https://other.test'))
    def test_all_expected_statuses(self):
        class Opener:
            def open(self,req,timeout):
                path=req.full_url[len(audit.BASE):]
                _,status,mime=next(x for x in audit.TARGETS if x[0]==path)
                return Response(status,'text/javascript' if mime=='javascript' else mime,b'{}' if mime=='application/json' else b'example')
        with patch.object(audit.urllib.request,'build_opener',return_value=Opener()):
            result=audit.review()
        self.assertTrue(result['passed'])
    def test_network_error_remains_a_failed_observation(self):
        class Opener:
            def open(self,*a,**k):raise OSError('synthetic')
        with patch.object(audit.urllib.request,'build_opener',return_value=Opener()):result=audit.review()
        self.assertFalse(result['passed']);self.assertEqual(len(result['observations']),7)
    def test_invalid_json_not_silently_accepted(self):
        with self.assertRaises(ValueError):audit.inspect_body('course.json',b'<html>not json</html>')

if __name__=='__main__':unittest.main()
