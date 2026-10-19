#!/usr/bin/env python3
"""Export public Figma Make context from canonical sources; never edits the repository.

From the repository root, after its normal build:
    python3 docs/figma-make/exportar.py --output /tmp/smartkea-figma-make

Outside the repository, also pass --repo /path/to/fundamentos-ciberseguridad.
Only Python's standard library is required. JSON Schema validation remains a
separate check; this exporter verifies the bank with its actual Python validator.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urljoin

# Import canonical validators without leaving bytecode files in the repository.
sys.dont_write_bytecode = True

REPO_URL = 'https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad'
CAMPUS = 'https://smartkea.com/introduccion-ciberseguridad/'
TERM = 'https://www.smartkea.com/fundamentos-ciberseguridad/term/'
STATIC_FILES = ('README.md', 'FIGMA-MAKE.md', 'producto.json', 'producto.schema.json',
                'banco-preguntas.schema.json', 'FUENTES.md', 'exportar.py')
READINGS = (
    ('D41', '01-representacion-codificacion.md'),
    ('D42', '02-logica-digital.md'),
    ('D43', '03-arquitectura-memoria-es.md'),
    ('D44', '04-sistemas-software.md'),
    ('D45', '05-redes-cloud.md'),
    ('D46', '06-guia-cobertura.md'),
)


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def find_repo(explicit):
    candidates = [Path(explicit)] if explicit else [Path.cwd(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / 'campus/build.py').is_file() and (candidate / 'formacion/introduccion-informatica/banco-preguntas.json').is_file():
            return candidate.resolve()
    raise ValueError('No se encuentra el repositorio. Indica --repo /ruta/al/repositorio.')


def validate_output_directory(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    if output == repo or repo in output.parents:
        raise ValueError('La salida debe estar fuera del repositorio y de todos sus descendientes.')
    if output.exists() and any(path.is_symlink() for path in output.iterdir()):
        raise ValueError('La carpeta de entrega no debe contener enlaces simbólicos de salida.')
    return output


def update_product_provenance(output, repo, commit, head, public_ref):
    """Only the exported contract acquires the identity of this particular build."""
    path = output/'producto.json'
    if not path.is_file():
        return
    product = load_json(path)
    provenance = product['provenance']
    provenance.update(snapshotCommit=commit, sourceHead=head,
                      publicSourceRef=public_ref,
                      generatedAt=datetime.now(timezone.utc).isoformat(),
                      snapshotScope='Generated export; exact build and source head are recorded independently.',
                      consolidationReviewStatus='Publication is not verified by this exporter.')
    provenance.pop('headObservedWhilePreparing', None)
    for source in product['sources']:
        if source.get('kind') != 'repository':
            continue
        local = repo/source['path']
        source.pop('localObservedCommit', None)
        source['observedSourceHead'] = head
        source['sha256'] = hash_file(local)
        ref = public_ref
        status = 'public_reference_supplied_by_release_operator'
        if public_ref == provenance.get('publicBaselineCommit'):
            result = subprocess.run(['git', 'show', public_ref+':'+source['path']],
                                    cwd=repo, capture_output=True)
            if result.returncode == 0 and hashlib.sha256(result.stdout).hexdigest() == source['sha256']:
                status = 'content_matches_published_baseline'
            else:
                ref, status = 'main', 'pending_consolidation'
        source.update(publicRef=ref, publicationStatus=status,
                      url=f"{REPO_URL}/blob/{ref}/{source['path']}")
    write_json(path, product)


def split_spanish_with_sources(text):
    match = re.fullmatch(r'\s*<!-- ES -->(.*?)<!-- EN -->(.*?)<!-- COMMON -->(.*?)\s*', text, re.S)
    if not match:
        raise ValueError('El recurso no conserva los bloques ES, EN y COMMON esperados.')
    return match[1].strip() + '\n\n' + match[3].strip() + '\n'


def portable_reading(text, source_path, commit):
    """Keep teaching text and code; only shift heading depth and resolve links."""
    output = []
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = re.match(r'(`{3,}|~{3,})', stripped)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append(line)
            continue
        if fence is not None:
            output.append(line)
            continue
        line = re.sub(r'^(#{1,5})(\s+)', r'#\1\2', line)

        def resolve(match):
            target = match[2]
            if target.startswith(('https://', 'http://', 'mailto:')):
                return match[0]
            if target.startswith('#/'):
                target = CAMPUS + '?lang=es' + target
            elif target.startswith('../#/'):
                target = CAMPUS + '?lang=es' + target[3:]
            else:
                target = urljoin(f'{REPO_URL}/blob/{commit}/{source_path}', target)
            return '[' + match[1] + '](' + target + ')'

        output.append(re.sub(r'(?<!!)\[([^\]]+)\]\(([^\s)]+)\)', resolve, line))
    return '\n'.join(output)


def export_bank_markdown(bank, source_path, source_sha, commit):
    topics = {topic['id']: topic['title'] for topic in bank['topics']}
    rows = [
        '# Introducción a la informática · Banco completo de 100 preguntas', '',
        f"**Edición {bank['version']} · Español · Cuatro opciones y una respuesta correcta.**", '',
        'Exportación generada de la fuente canónica. Este archivo sirve para estudiar y revisar; no es una segunda fuente editable.', '',
        f'Fuente: [{source_path}]({REPO_URL}/blob/{commit}/{source_path}).',
        f'SHA-256 de los bytes de la fuente: `{source_sha}`.', '',
        f'[Practicar 20 al azar]({CAMPUS}examen/) · [Guía de estudio D46]({CAMPUS}?lang=es#/recurso/D46).', '',
        'En el simulador, elegir corrige al momento y la primera respuesta queda registrada. Aquí las soluciones están visibles para el repaso. No existe calificación oficial ni verificación de identidad.', '',
        '## Índice por tema', '',
    ]
    for topic in bank['topics']:
        count = sum(q['topic'] == topic['id'] for q in bank['questions'])
        rows.append(f"- [{topic['id']} · {topic['title']}](#{topic['id'].lower()}) — {count} preguntas.")
    difficulty = {'basico': 'básico', 'intermedio': 'intermedio', 'aplicacion': 'aplicación'}
    for topic in bank['topics']:
        rows += ['', f'<a id="{topic["id"].lower()}"></a>', f'## {topic["id"]} · {topic["title"]}', '']
        for question in bank['questions']:
            if question['topic'] != topic['id']:
                continue
            rows += [f"### {question['id']} · {difficulty[question['difficulty']]}", '', question['prompt'], '']
            for option in question['options']:
                rows.append(f"- **{option['id']})** {option['text']}")
            answer = next(option for option in question['options'] if option['id'] == question['correctOptionId'])
            rows += ['', f"**Respuesta correcta: {answer['id']}) {answer['text']}**", '',
                     '**Explicación.** ' + question['explanation'], '',
                     f"**Repaso:** [{question['study']['label']}]({urljoin(CAMPUS+'examen/',question['study']['url'])}).", '']
    return '\n'.join(rows).strip() + '\n'


def make_inventory(course, english, os_course, os_english, term, term_config, bank, commit):
    en_modules = {item['id']: item for item in english['modules']}
    en_resources = {item['id']: item for item in english['resources']}
    en_os = {item['id']: item for item in os_english['lessons']}
    counts = Counter(question['topic'] for question in bank['questions'])
    return {
        'schemaVersion': 1, 'version': '1.0.0', 'snapshotCommit': commit, 'repository': REPO_URL,
        'scope': 'Inventario completo de IDs, títulos y rutas; los cuerpos docentes completos permanecen en los catálogos del build.',
        'campus': {
            'id': course['id'], 'version': course['version'], 'languages': ['es','en'],
            'counts': {'modules': len(course['modules']), 'slides': sum(len(m['slides']) for m in course['modules']), 'labs': sum(len(m['labs']) for m in course['modules']), 'resources': len(course['resources']), 'blocks': len(course['blocks']), 'plannedHours': course['hours']},
            'blocks': course['blocks'],
            'modules': [{'id':m['id'],'title':{'es':m['title'],'en':en_modules[m['id']]['title']},'block':m['block'],'hours':m['hours'],'theoryHours':m['theoryHours'],'practiceHours':m['practiceHours'],'prerequisites':m['prerequisites'],'sourcePath':m['source'],'url':CAMPUS+'?lang=es#/modulo/'+m['id'],
                         'labs':[{'id':l['id'],'title':l['title'],'hours':l['hours'],'environment':l['environment'],'success':l['success'],'url':CAMPUS+'?lang=es#/modulo/'+m['id']+'/practica/'+l['id']} for l in m['labs']]} for m in course['modules']],
            'resources': [{'id':r['id'],'title':{'es':r['title'],'en':en_resources[r['id']]['title']},'kind':r['kind'],'url':CAMPUS+'?lang=es#/recurso/'+r['id'],'englishCoverage':'summary_with_full_edition_pending' if r['id'] in ['D37','D38','D39','D40'] else 'developed_reading'} for r in course['resources']],
        },
        'os': {'id':os_course['id'],'version':os_course['version'],'languages':['es','en'],
               'counts':{'lessons':len(os_course['lessons']),'views':sum(len(l['views']) for l in os_course['lessons']),'common':sum(l['group']=='common' for l in os_course['lessons']),'linux':sum(l['group']=='linux' for l in os_course['lessons']),'windows':sum(l['group']=='windows' for l in os_course['lessons']),'macos':sum(l['group']=='macos' for l in os_course['lessons'])},
               'lessons':[{'id':l['id'],'title':{'es':l['title'],'en':en_os[l['id']]['title']},'group':l['group'],'question':l['question'],'outcome':l['outcome'],'viewCount':len(l['views']),'viewKinds':[v['kind'] for v in l['views']],'url':CAMPUS+'sistemas/?lang=es#'+l['id']+'/0'} for l in os_course['lessons']]},
        'term': {'id':term['id'],'version':term['version'],'languages':['es'],
                 'counts':{'modules':len(term['modules']),'lessons':sum(len(m['lessons']) for m in term['modules']),'challenges':sum(len(m['lessons']) for m in term['modules']),'questions':sum(len(l['quiz']) for m in term['modules'] for l in m['lessons']),'estimatedMinutes':term['minutes']},
                 'labConfiguredInSnapshot':bool(term_config['lab']['url']),
                 'modules':[{'id':m['id'],'title':m['title'],'summary':m['summary'],'level':m['level'],'lessons':[{'id':l['id'],'title':l['title'],'summary':l['summary'],'minutes':l['minutes'],'objectives':l['objectives'],'prerequisites':l['prerequisites'],'stepCount':len(l['steps']),'questionCount':len(l['quiz']),'url':TERM+'#/leccion/'+l['id']+'/concepto/0'} for l in m['lessons']]} for m in term['modules']]},
        'exam': {'version':bank['version'],'language':'es','questionCount':len(bank['questions']),'sessionLength':20,
                 'topics':[{'id':t['id'],'title':t['title'],'questionCount':counts[t['id']],'studyResources':sorted({q['study']['url'].split('/')[-1] for q in bank['questions'] if q['topic']==t['id']})} for t in bank['topics']],
                 'questionIds':[q['id'] for q in bank['questions']]},
        'countingRules': ['Las horas y marcas pertenecen a su itinerario; no sumarlas ni convertirlas en asistencia.','Las vistas OS no son lecciones independientes.','Las preguntas TERM no forman parte del banco de100 de informática.','D37–D40 tienen resumen EN y edición docente completa EN pendiente.'],
    }


def collect_case_inventory(repo, public_ref):
    """Inventory the supplementary classroom case without adding curriculum hours."""
    base = 'formacion/casos/c99-forense/'
    questions = load_json(repo/base/'preguntas.json')
    scenario = load_json(repo/base/'evidencias/escenario.json')
    spanish = (repo/base/'PRACTICA.md').read_text(encoding='utf-8')
    english = (repo/base/'PRACTICA.en.md').read_text(encoding='utf-8')
    activities = re.findall(r'^## (A\d{2})\b', spanish, re.M)
    question_ids = [question['id'] for question in questions['questions']]
    if (scenario.get('synthetic') is not True or questions.get('public_answers') is not True
            or questions.get('case_id') != scenario.get('case_id')
            or len(activities) != 10 or len(set(activities)) != 10
            or re.findall(r'^## (A\d{2})\b', english, re.M) != activities
            or len(question_ids) != 12 or len(set(question_ids)) != 12):
        raise ValueError('Revisa el contrato C99-DFIR: diez actividades ES/EN y doce preguntas públicas del escenario sintético.')
    # Read module linkage from the same canonical helper used by the campus build.
    sys.path.insert(0, str(repo/'campus'))
    try:
        spec = importlib.util.spec_from_file_location('smartkea_case_operations', repo/'campus/operations.py')
        operations = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(operations)
    finally:
        sys.path.pop(0)
    linked_modules = sorted(operations.CASE_MODULES)
    if linked_modules != ['M27', 'M28', 'M29']:
        raise ValueError('La ampliación C99-DFIR cambió de módulos; revisa el contrato antes de exportar.')
    inputs = [base+name for name in ('README.md','PRACTICA.md','PRACTICA.en.md','DOCENTE.md',
              'INFORME.md','FUENTES.md','preguntas.json','evidencias/escenario.json',
              'herramientas/forense.py','Dockerfile.laboratorio','compose.laboratorio.yaml')]
    inputs += [path.relative_to(repo).as_posix() for path in sorted((repo/base/'evidencias/webroot').glob('*.txt'))]
    inputs += ['campus/operations.py', 'campus/tests/test_c99_case.py']
    inventory = {
        'id': scenario['case_id'], 'status': 'existing',
        'title': (repo/base/'README.md').read_text(encoding='utf-8').splitlines()[0].removeprefix('# '),
        'scope': 'Supplementary repository material; no independent campus server route or new progress record.',
        'sourcePath': base+'README.md', 'url': f'{REPO_URL}/blob/{public_ref}/{base}README.md',
        'studentGuides': {language: f'{REPO_URL}/blob/{public_ref}/{base}{name}' for language,name in [('es','PRACTICA.md'),('en','PRACTICA.en.md')]},
        'linkedModules': linked_modules, 'activityIds': activities, 'activityCount': len(activities),
        'questionCount': len(question_ids), 'questionIds': question_ids,
        'questionLanguage': questions['language'], 'questionSourcePath': base+'preguntas.json',
        'publicAnswers': True, 'syntheticEvidence': True,
        'addedModules': 0, 'addedHours': 0, 'newProgressMarks': False,
        'includedInInformaticsExamBank': False,
        'execution': 'Offline synthetic-evidence analysis; optional legitimate local classroom shell, not malware execution.',
    }
    return inventory, inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', help='Raíz del repositorio canónico; se detecta si se ejecuta dentro de él.')
    parser.add_argument('--output', required=True, help='Carpeta de entrega obligatoriamente fuera del checkout.')
    parser.add_argument('--public-ref', default='main', help='Rama o SHA remoto publicado para los enlaces; nunca se deduce del HEAD local.')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', args.public_ref) or '..' in args.public_ref:
        raise ValueError('Indica una referencia pública de Git válida.')
    repo = find_repo(args.repo)
    output = validate_output_directory(repo, args.output)
    output.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    for name in STATIC_FILES:
        source = here/name
        if source.is_file() and source.resolve() != (output/name).resolve():
            shutil.copyfile(source, output/name)

    input_names = ['campus/dist/course.json','campus/dist/course.en.json','campus/dist/sistemas/course.es.json','campus/dist/sistemas/course.en.json','term/dist/course.json','term/dist/config.json','campus/dist/build-info.json']
    missing = [name for name in input_names if not (repo/name).is_file()]
    if missing:
        raise ValueError('Ejecuta primero python3 campus/cloudflare.py build. Faltan: '+', '.join(missing))
    course, english, os_course, os_english, term, term_config, info = [load_json(repo/name) for name in input_names]
    commit = info['sourceCommit']
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('El catálogo no identifica un commit reproducible.')
    head = subprocess.run(['git','rev-parse','HEAD'],cwd=repo,check=True,capture_output=True,text=True).stdout.strip()
    source_path = 'formacion/introduccion-informatica/banco-preguntas.json'
    bank_path = repo/source_path
    bank = load_json(bank_path)
    spec = importlib.util.spec_from_file_location('smartkea_bank_validator', repo/'campus/exam_build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_bank(bank,{r['id'] for r in course['resources']})
    paths_spec = importlib.util.spec_from_file_location('smartkea_paths_validator', repo/'campus/learning_paths.py')
    paths_module = importlib.util.module_from_spec(paths_spec)
    paths_spec.loader.exec_module(paths_module)
    role_routes, credentials, path_sources = paths_module.collect_paths(repo)
    paths_report = paths_module.validate_paths(role_routes, credentials, path_sources, course['modules'])
    if paths_report['routes'] != 6 or paths_report['phases'] != 26:
        raise ValueError('El contrato requiere las seis rutas revisadas y sus 26 etapas.')
    input_names += ['formacion/rutas/routes.json', 'formacion/rutas/credentials.json',
                    'formacion/rutas/sources.json', 'campus/learning_paths.py',
                    'campus/assets/routes.js', 'campus/tests/test_learning_paths.py',
                    'campus/tests/browser_routes.py']
    compact_sha = hashlib.sha256(json.dumps(bank,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
    if compact_sha != info['exam']['bankSha256']:
        raise ValueError('Banco y build no coinciden. Regenera el sitio antes de exportar.')
    shutil.copyfile(bank_path,output/'banco-preguntas.json')
    (output/'BANCO-100-PREGUNTAS.md').write_text(export_bank_markdown(bank,source_path,hash_file(bank_path),args.public_ref),encoding='utf-8')
    inventory = make_inventory(course,english,os_course,os_english,term,term_config,bank,commit)
    inventory['learningPaths'] = {
        'status': 'existing', 'scope': 'Reviewed local integration; production is verified separately.',
        'language': role_routes['language'], 'sourceSchema': role_routes['schema'],
        'sourceReviewDate': role_routes['reviewed_at'], 'counts': paths_report,
        'sourcePath': 'formacion/rutas/routes.json', 'url': CAMPUS+'rutas.html',
        'storageKey': 'smartkea.learning-paths.v1', 'hoursNotice': role_routes['hours_notice'],
        'routes': [{**route, 'url': CAMPUS+'rutas.html#ruta-'+route['id']} for route in role_routes['routes']],
        'certifications': credentials['certifications'], 'sources': path_sources['sources'],
    }
    case_inventory, case_inputs = collect_case_inventory(repo, args.public_ref)
    inventory['caseStudies'] = [case_inventory]
    inventory['countingRules'].append('Las diez actividades y doce preguntas de C99-DFIR amplían M27–M29; no añaden módulos, horas ni preguntas al examen de informática.')
    input_names += case_inputs + ['term/assets/state.js', 'term/assets/app.js',
                    'term/verify_public.py', 'term/tests/persistence.test.mjs',
                    'term/tests/persistence-browser.mjs', 'term/docs/VALIDACION.md']
    write_json(output/'catalogo-publico.json',inventory)
    samples = {'schemaVersion':1,'version':'1.0.0','snapshotCommit':commit,'scope':'Muestras completas reales para composición; el inventario no sustituye el resto de cuerpos del build.',
               'module':next(m for m in course['modules'] if m['id']=='M02'),'reading':next(r for r in course['resources'] if r['id']=='D41'),'osLesson':next(l for l in os_course['lessons'] if l['id']=='OS-L01'),'termLesson':term['modules'][0]['lessons'][0],'question':bank['questions'][0],
               'learningPath':role_routes['routes'][0]}
    write_json(output/'muestras-contenido.json',samples)
    update_product_provenance(output, repo, commit, head, args.public_ref)

    notes = ['# Introducción a la informática · Apuntes D41–D46','',
             '**Edición española completa y fuentes compartidas. Exportación generada; no editar como una segunda fuente.**','',
             'Este cuaderno reúne los seis recursos públicos del repositorio. Conserva el contenido español, ejemplos, ejercicios y fuentes de cada lectura; no incorpora la correspondencia privada utilizada durante la revisión curricular.','',
             'Transformaciones editoriales de exportación: seleccionar los bloques ES y COMMON, aumentar un nivel los encabezados y resolver enlaces relativos para que el archivo pueda consultarse fuera del repositorio. Los bloques de código conservan sus bytes de texto.','',
             f'Snapshot local del catálogo: `{commit}`. Commit local leído de las fuentes: `{head}`. Referencia pública para los enlaces: `{args.public_ref}`. Las huellas individuales figuran en el manifiesto; los commits locales no se presentan como publicados.','',
             '## Índice','']
    reading_inputs = []
    for rid,name in READINGS:
        path = repo/'formacion/introduccion-informatica'/name
        spanish = split_spanish_with_sources(path.read_text(encoding='utf-8'))
        title = next(line[2:] for line in spanish.splitlines() if line.startswith('# '))
        notes.append(f'- [{rid} · {title}](#{rid.lower()})')
        reading_inputs.append({'id':rid,'path':path.relative_to(repo).as_posix(),'sha256':hash_file(path),'title':title,'text':spanish})
    for item in reading_inputs:
        notes += ['', '---', '', f'<a id="{item["id"].lower()}"></a>',
                  f'**{item["id"]} · [Abrir en el campus]({CAMPUS}?lang=es#/recurso/{item["id"]}) · [Fuente original]({REPO_URL}/blob/{args.public_ref}/{item["path"]})**','',
                  portable_reading(item['text'],item['path'],args.public_ref)]
    (output/'APUNTES-D41-D46.md').write_text('\n'.join(notes).strip()+'\n',encoding='utf-8')

    checks = [
        {'id':'canonical-python-bank-validator','passed':True,'detail':'Validación real de campus/exam_build.py:100 preguntas,12 temas,opciones,IDs y enlaces.'},
        {'id':'canonical-python-paths-validator','passed':True,**paths_report},
        {'id':'supplementary-forensic-case-inventory','passed':True,'activityCount':case_inventory['activityCount'],'questionCount':case_inventory['questionCount'],'addedModules':0,'addedHours':0},
        {'id':'bank-copy-byte-equality','passed':(output/'banco-preguntas.json').read_bytes()==bank_path.read_bytes()},
        {'id':'compiled-bank-hash','passed':compact_sha==info['exam']['bankSha256'],'sha256':compact_sha},
        {'id':'markdown-all-100','passed':len(re.findall(r'^### INF-\d{3}\b',(output/'BANCO-100-PREGUNTAS.md').read_text(),re.M))==100},
        {'id':'markdown-all-6-readings','passed':len(reading_inputs)==6},
        {'id':'json-parse','passed':True},
    ]
    for path in output.glob('*.json'):
        if path.name not in ['manifest.json','validacion.json']:
            load_json(path)
    checks.append({'id':'text-attachments-below-1MB','passed':all(p.stat().st_size<1_000_000 for p in output.iterdir() if p.is_file() and p.suffix in ['.json','.md','.py'])})
    report = {'schemaVersion':1,'generatedAt':datetime.now(timezone.utc).isoformat(),'snapshotCommit':commit,'sourceHead':head,'publicSourceRef':args.public_ref,
              'checks':checks,'passed':all(c['passed'] for c in checks),'schemaValidation':'Not performed by the standard-library exporter; validate both JSON Schemas separately.','browserTestsRun':False,'productionAcceptancePerformed':False,
              'warnings':[] if head==commit else ['El head y el commit del catálogo difieren. El manifiesto declara ambos; recompila si necesitas un snapshot único de la revisión actual.']}
    if not report['passed']:
        raise ValueError('Una comprobación del exportador no ha pasado: '+json.dumps(checks,ensure_ascii=False))
    write_json(output/'validacion.json',report)
    inputs = [{'path':name,'sha256':hash_file(repo/name)} for name in input_names]
    inputs += [{k:item[k] for k in ['id','path','sha256']} for item in reading_inputs]
    manifest = {'schemaVersion':1,'packageId':'smartkea-figma-make-handoff','version':'1.0.0','generatedAt':report['generatedAt'],'repository':REPO_URL,'snapshotCommit':commit,'sourceHead':head,'publicSourceRef':args.public_ref,
                'productionAcceptancePerformed':False,'canonicalBank':{'sourcePath':source_path,'sourceSha256':hash_file(bank_path),'compactPublishedSha256':compact_sha,'version':bank['version'],'questions':100},
                'generatedExportPolicy':'Edit canonical sources and rerun exportar.py; never maintain generated Markdown/JSON as a second editorial bank.',
                'inputFiles':inputs,'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':hash_file(p)} for p in sorted(output.iterdir()) if p.is_file() and p.name!='manifest.json' and p.suffix!='.zip'],
                'manifestHashPolicy':'Excludes itself and optional transport ZIP to avoid a circular hash.'}
    write_json(output/'manifest.json',manifest)
    print(json.dumps({'output':str(output),'snapshotCommit':commit,'sourceHead':head,'questions':100,'readings':6,'files':len(manifest['files'])+1,'passed':True},ensure_ascii=False))


if __name__ == '__main__':
    main()
