import copy,json,sys,unittest,shutil,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campus'))
from learning_paths import collect_paths,validate_paths,prerequisites,render
class LearningPathsTests(unittest.TestCase):
    def setUp(self):
        self.routes,self.certs,self.sources=collect_paths()
        from build import collect
        self.modules=collect()['modules']
    def check(self):return validate_paths(self.routes,self.certs,self.sources,self.modules)
    def test_six_routes_26_phases(self):
        self.assertEqual(self.check(),{'routes':6,'phases':26,'credentials':13,'sources':32})
    def test_wrong_hours_rejected(self):
        self.routes['routes'][0]['estimated_hours']+=1
        with self.assertRaises(ValueError):self.check()
    def test_unknown_credential_rejected(self):
        self.routes['routes'][0]['certifications'].append('invented')
        with self.assertRaises(ValueError):self.check()
    def test_unknown_source_rejected(self):
        self.routes['routes'][0]['phases'][0]['source_refs'].append('invented')
        with self.assertRaises(ValueError):self.check()
    def test_unknown_module_rejected(self):
        with self.assertRaises(ValueError):prerequisites(['M99'],self.modules)
    def test_cycle_rejected(self):
        with self.assertRaises(ValueError):prerequisites(['a'],[{'id':'a','prerequisites':['b']},{'id':'b','prerequisites':['a']}])
    def test_prerequisites_do_not_repeat_selected(self):
        self.assertEqual(prerequisites(['b'],[{'id':'a','prerequisites':[]},{'id':'b','prerequisites':['a']}]),['a'])
    def test_evidence_is_required(self):
        self.routes['routes'][0]['phases'][0]['evidence']=' '
        with self.assertRaises(ValueError):self.check()
    def test_duplicate_route_rejected(self):
        self.routes['routes'][1]['id']=self.routes['routes'][0]['id']
        with self.assertRaises(ValueError):self.check()
    def test_unsafe_url_rejected(self):
        self.sources['sources'][0]['url']='javascript:alert(1)'
        with self.assertRaises(ValueError):self.check()
    def test_render_is_independent_from_the_dpd_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);stage=root/'output';(stage/'assets').mkdir(parents=True)
            shutil.copytree(ROOT/'formacion/rutas',root/'formacion/rutas')
            (root/'campus/assets').mkdir(parents=True)
            for name in ('routes.js','routes.css'):shutil.copyfile(ROOT/'campus/assets'/name,root/'campus/assets'/name)
            report=render(stage,{'modules':self.modules},root)
            self.assertEqual(report['routes'],6);self.assertFalse((stage/'dpd').exists())
            page=(stage/'rutas.html').read_text();self.assertNotIn('href="dpd/',page)
            self.assertIn('https://github.com/WiktorNykiel/fundamentos-ciberseguridad/tree/main/awesome-dpd',page)
            self.assertIn('href="examen/"',page)
if __name__=='__main__':unittest.main()
