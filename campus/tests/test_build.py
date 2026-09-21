"""Pruebas unitarias del compilador; los fixtures no son contenido docente."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build
from content import LESSONS, notes_and_quizzes
from operations import READINGS
from integral import READINGS as INTEGRAL_READINGS

class MarkdownTests(unittest.TestCase):
    def test_html_is_escaped(self):
        result=build.markdown('<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>')['html']
        self.assertNotIn('<script',result); self.assertNotIn('<img',result)
    def test_unsafe_links(self):
        for value in ['javascript:alert(1)','data:text/html,xxx','//example.test/x','https://ok.test/\x00x']:
            self.assertEqual(build.safe_link(value,'formacion/test.md'),'')
    def test_https_link(self):
        self.assertIn('href="https://example.test/x"',build.inline('[Enlace](https://example.test/x)'))
    def test_relative_link_stays_in_repo(self):
        self.assertIn('/blob/main/formacion/FUENTES.md',build.safe_link('../FUENTES.md','formacion/modulos/01.md'))
        self.assertEqual(build.safe_link('../../../x','a.md'),'')
    def test_code_is_literal(self):
        self.assertIn('&lt;img',build.markdown('```sh\n<img src=x>\n```')['html'])
        self.assertNotIn('<img',build.inline('`<img>`'))
    def test_table(self):
        out=build.markdown('| A | B |\n|---|---|\n| uno | dos |')['html']
        self.assertIn('<table>',out);self.assertIn('scope="col"',out);self.assertIn('<td>dos</td>',out)
    def test_lists(self):
        out=build.markdown('1. Uno\n2. Dos\n\n- Tres')['html']
        self.assertIn('<ol>',out);self.assertIn('<ul>',out)
    def test_headings_unique(self):
        out=build.markdown('## Igual\ntexto\n## Igual\ntexto',prefix='M05')
        self.assertEqual([x['id'] for x in out['toc']],['M05-1','M05-2'])
        self.assertEqual(len(out['slides']),2)
    def test_link_with_inline_code(self):
        out=build.inline('[`archivo`](https://example.test/x)')
        self.assertIn('<code>archivo</code>',out);self.assertNotIn('\x00',out)
    def test_slide_ids_do_not_duplicate_reader(self):
        out=build.markdown('## Tema\nTexto',prefix='M01')
        self.assertIn('id="M01-1-slide"',out['slides'][0]['html'])
    def test_empty(self): self.assertEqual(build.markdown('')['html'],'')
    def test_nul_cannot_inject_token(self): self.assertIn('�',build.inline('\x00100\x00'))

class CurriculumTests(unittest.TestCase):
    def test_notes_cover_course(self):
        notes,quiz=notes_and_quizzes();self.assertEqual(len(notes),32);self.assertEqual(set(notes),set(quiz))
        for mid,q in quiz.items():
            self.assertEqual(len(q['options']),3);self.assertEqual(q['options'][q['correct']],LESSONS[mid][5])
    def test_module_split(self):
        text='# M01–M04 · bloque\n## M01 · Uno\ntexto\n## M02 · Dos\ntexto'
        self.assertEqual(set(build.split_modules(text)),{'M01','M02'})
    def test_labs_fields(self):
        text='## M05 · Test\nTeoría\n\n**L05A · Archivos.** Entorno: VM. Tareas: leer. Evidencia: informe. Éxito: verificado. Recuperación: copia.\n\n**L05B · Copia.** Entorno: VM.\n\n**L05C · Volver.** Entorno: VM.'
        theory,labs=build.labs_from(text,'M05')
        self.assertNotIn('**L05A',theory);self.assertEqual(len(labs),3)
        self.assertEqual(labs[0]['tasks'],'leer.');self.assertEqual(labs[0]['title'],'Archivos')
    def test_capstone(self):
        text='# M32 · Proyecto\nIntro\n## L32A · Construir\n**Tareas:** operar.\n\n## L32B · Observar\n**Éxito:** verificar.\n\n## L32C · Recuperar\n**Recuperación:** conservar.'
        _,labs=build.labs_from(text,'M32');self.assertEqual([x['id'] for x in labs],['L32A','L32B','L32C'])
        self.assertEqual(labs[0]['tasks'],'operar.')
    def fixture(self,path):
        (path/'modulos').mkdir();(path/'planificacion').mkdir();(path/'practicas').mkdir();(path/'lecciones').mkdir()
        for name in build.PUBLIC_DOCS + ['PLAN-DOCENTE.md','COMO-ESTUDIAR.md','DESPLIEGUE-ESTATICO.md']:
            (path/name).write_text('# '+name+'\nSynthetic test reference.\n',encoding='utf-8')
        for n in range(1,9):
            (path/'lecciones'/f'{n:02}-fixture.md').write_text(f'# Fixture {n}\nSynthetic lesson.\n',encoding='utf-8')
        (path/'operacion').mkdir()
        for rid,name,_,_ in READINGS:
            (path/'operacion'/name).write_text(f'# {rid} fixture\nSynthetic operational lesson.\n',encoding='utf-8')
        extension=path.parent/'itinerario-integral';extension.mkdir()
        for rid,name in INTEGRAL_READINGS:
            (extension/name).write_text('<!-- ES -->\n# Prueba '+rid+'\n\nDatos sintéticos.\n<!-- EN -->\n# Test '+rid+'\n\nSynthetic data.\n',encoding='utf-8')
        mods=[];parts=[]
        for n in range(1,33):
            mid=f'M{n:02}';mods.append({'id':mid,'titulo':f'Módulo {n}','prerrequisitos':[]})
            body=f'## {mid} · Teoría\n\nTexto de prueba del compilador.\n\n'
            body+='\n\n'.join(f'**L{n:02}{s} · Práctica {s}.** Entorno: VM. Tareas: observar. Evidencia: informe. Éxito: contrastar. Recuperación: conservar.' for s in 'ABC')
            if n<32:parts.append(body)
        (path/'modulos/01.md').write_text('\n\n'.join(parts),encoding='utf-8')
        (path/'CAPSTONE.md').write_text('# M32 · Proyecto\n\n'+''.join(f'## L32{s} · Fase {s}\n\n**Tareas:** comprobar.\n\n' for s in 'ABC'),encoding='utf-8')
        (path/'planificacion/curriculo.json').write_text(json.dumps(mods),encoding='utf-8')
    def test_collect_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'formacion/sistemas-operativos';path.mkdir(parents=True);self.fixture(path);data=build.collect(path)
            self.assertEqual(len(data['modules']),32);self.assertEqual(data['hours'],480)
            self.assertEqual(sum(len(m['labs']) for m in data['modules']),96)
            self.assertEqual(sum(m['theoryHours'] for m in data['modules']),168)
            self.assertEqual([r['id'] for r in data['resources']],[f'D{i:02}' for i in range(1,37)])
    def test_duplicate_catalog_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'formacion/sistemas-operativos';path.mkdir(parents=True);self.fixture(path);p=path/'planificacion/curriculo.json'
            data=json.loads(p.read_text());data.append(data[0]);p.write_text(json.dumps(data))
            with self.assertRaises(ValueError):build.collect(path)
    def test_internal_reference_link(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'formacion/sistemas-operativos';path.mkdir(parents=True);self.fixture(path)
            (path/'FUENTES.md').write_text('# Fuentes\nDocumentación.',encoding='utf-8')
            (path/'LABORATORIO.md').write_text('# Lab\n[Fuentes](FUENTES.md)',encoding='utf-8')
            data=build.collect(path);lab=next(r for r in data['resources'] if r['title']=='Lab')
            self.assertIn('href="#/recurso/',lab['html'])
    def test_collect_missing_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'formacion/sistemas-operativos';path.mkdir(parents=True);self.fixture(path);(path/'CAPSTONE.md').write_text('# Sin módulo',encoding='utf-8')
            with self.assertRaises(ValueError):build.collect(path)
    def test_security_policy(self):
        self.assertNotIn('unsafe-inline',build.CSP);self.assertNotIn('unsafe-eval',build.CSP)
        self.assertIn("frame-ancestors 'none'",build.CSP)
    def test_student_allowlist(self):
        self.assertNotIn('BANCO-PREGUNTAS.md',build.PUBLIC_DOCS)
        self.assertNotIn('GUIA-DOCENTE.md',build.PUBLIC_DOCS)

if __name__=='__main__': unittest.main(verbosity=2)
