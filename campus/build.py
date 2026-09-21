#!/usr/bin/env python3
"""Compila el campus estático desde los Markdown del curso. Sin dependencias ni red."""
from __future__ import annotations
import hashlib
import html
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import quote, urlsplit
from content import notes_and_quizzes
from bilingual import collect_en
from provenance import source_commit
from release_inputs import public_kit_files
from publication import not_found_page
from operations import add_resources, related_reading
from os_classroom.build import build_into as build_os_classroom

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COURSE = ROOT / 'formacion' / 'sistemas-operativos'
REPO = 'https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad'
BLOCKS = [
    ('fundamentos', 'Fundamentos y método', 1, 4, 'Comprender antes de automatizar.'),
    ('linux', 'Linux y Bash', 5, 12, 'Archivos, permisos, servicios y automatización.'),
    ('windows', 'Windows, CMD, BAT y PowerShell', 13, 19, 'Administrar Windows a través de objetos y controles nativos.'),
    ('macos', 'macOS, Darwin y zsh', 20, 23, 'Entender las particularidades de la plataforma Apple.'),
    ('operacion', 'Operación y ciberseguridad', 24, 30, 'Conectar, proteger, observar e investigar.'),
    ('ia', 'IA desde terminal', 31, 31, 'Asistencia con contexto, límites y verificación.'),
    ('proyecto', 'Proyecto integrador', 32, 32, 'Construir, explicar y recuperar una solución.'),
]
PUBLIC_DOCS = ['LABORATORIO.md', 'REFERENCIA-CRUZADA.md', 'CHEATSHEETS.md',
               'BASTIONADO.md', 'COMPETENCIAS.md', 'EVALUACION.md', 'PLANTILLAS.md',
               'FUENTES.md', 'INICIO-RAPIDO.md', 'USO-RESPONSABLE.md']
CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def safe_link(target: str, source: str = '') -> str:
    """Solo enlaces HTTPS, fragmentos locales o rutas resueltas en el repositorio."""
    if any(ord(c) < 32 for c in target) or target.startswith('//'):
        return ''
    parsed = urlsplit(target)
    if parsed.scheme:
        return target if parsed.scheme == 'https' and parsed.netloc else ''
    if target.startswith('#'):
        return target
    if not source:
        return ''
    from posixpath import normpath, dirname, join
    path = normpath(join(dirname(source), parsed.path))
    if path.startswith('../') or path.startswith('/'):
        return ''
    return REPO + '/blob/main/' + quote(path, safe='/') + (('#' + quote(parsed.fragment)) if parsed.fragment else '')


def inline(text: str, source: str = '') -> str:
    """Subconjunto Markdown deliberadamente pequeño; HTML crudo siempre escapado."""
    text = text.replace("\x00", "�")
    tokens: list[str] = []
    def token(value: str) -> str:
        tokens.append(value)
        return f'\x00{len(tokens)-1}\x00'
    text = re.sub(r'`([^`\n]+)`', lambda m: token('<code>' + esc(m[1]) + '</code>'), text)
    def link(m: re.Match[str]) -> str:
        url = safe_link(m[2], source)
        label = esc(m[1])
        return token(f'<a href="{esc(url)}" rel="noreferrer noopener">{label}</a>') if url else label
    text = re.sub(r'\[([^\]\n]+)\]\(([^\s)]+)\)', link, text)
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    for index in range(len(tokens)-1, -1, -1):
        text = text.replace(f'\x00{index}\x00', tokens[index])
    return text


def markdown(text: str, source: str = '', prefix: str = 's') -> dict:
    """Genera HTML, índice y bloques de presentación. No evalúa Markdown/HTML."""
    lines = text.replace('\r\n', '\n').split('\n')
    output: list[str] = []
    toc: list[dict] = []
    sections: list[dict] = []
    fragment: list[str] = []
    title = 'Introducción'
    i = 0
    def emit(value: str) -> None:
        output.append(value); fragment.append(value)
    def flush() -> None:
        nonlocal fragment
        if fragment:
            sections.append({'title': title, 'html': '\n'.join(fragment)})
            fragment = []
    while i < len(lines):
        line = lines[i]
        if not line.strip(): i += 1; continue
        if line.startswith('```'):
            lang = re.sub('[^a-zA-Z0-9_-]', '', line[3:])[:24]
            code: list[str] = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            emit(f'<pre data-language="{esc(lang)}"><code>' + esc('\n'.join(code)) + '</code></pre>')
            i += 1; continue
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            flush(); title = re.sub(r'[*`]', '', heading[2])
            anchor = f'{prefix}-{len(toc)+1}'
            level = min(4, max(2, len(heading[1])))
            toc.append({'id': anchor, 'title': title})
            emit(f'<h{level} id="{anchor}">{inline(heading[2], source)}</h{level}>')
            i += 1; continue
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|-]+\|\s*$', lines[i+1]):
            cells = lambda value: [inline(x.strip(), source) for x in value.strip().strip('|').split('|')]
            headers = cells(line); rows: list[list[str]] = []; i += 2
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(cells(lines[i])); i += 1
            emit('<div class="table-scroll" tabindex="0" role="region" aria-label="Tabla desplazable"><table><thead><tr>' + ''.join('<th scope="col">'+x+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows) + '</tbody></table></div>')
            continue
        ordered = re.match(r'^\s*\d+[.)]\s+', line)
        if ordered or re.match(r'^\s*[-*]\s+', line):
            tag = 'ol' if ordered else 'ul'; items: list[str] = []
            pattern = r'^\s*\d+[.)]\s+(.+)' if ordered else r'^\s*[-*]\s+(.+)'
            while i < len(lines) and (match := re.match(pattern, lines[i])):
                items.append('<li>' + inline(match[1], source) + '</li>'); i += 1
            emit('<'+tag+'>' + ''.join(items) + '</'+tag+'>'); continue
        if line.startswith('>'):
            emit('<blockquote>' + inline(line.lstrip('> ').strip(), source) + '</blockquote>'); i += 1; continue
        if re.match(r'^[-*_]{3,}\s*$', line):
            emit('<hr>'); i += 1; continue
        paragraph = [line.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||>|\s*[-*]\s|\s*\d+[.)]\s)', lines[i]):
            paragraph.append(lines[i].strip()); i += 1
        emit('<p>' + inline(' '.join(paragraph), source) + '</p>')
    flush()
    slides: list[dict] = []
    for section in sections:
        slides.append({**section, 'html': re.sub(r' id="([^"]+)"', r' id="\1-slide"', section['html'])})
    return {'html': '\n'.join(output), 'toc': toc, 'slides': slides}


def read_text(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Fuente ausente o no regular: {path}')
    if path.stat().st_size > 1_000_000:
        raise ValueError(f'Fuente demasiado grande: {path}')
    return path.read_text(encoding='utf-8')


def split_modules(text: str) -> dict[str, str]:
    matches = list(re.finditer(r'(?m)^#{1,2}\s+(M\d{2})\s+[·:—-]', text))
    return {m[1]: text[m.start():matches[n+1].start() if n+1 < len(matches) else len(text)].strip()
            for n, m in enumerate(matches)}


def labs_from(text: str, mid: str) -> tuple[str, list[dict]]:
    pattern = r'(?m)^##\s+(L32[ABC])\s+·\s+([^\n]+)\n' if mid == 'M32' else r'(?m)^\*\*(L\d{2}[ABC])\s+·\s+(.*?)\*\*'
    matches = list(re.finditer(pattern, text)); labs: list[dict] = []
    for n, m in enumerate(matches):
        end = matches[n+1].start() if n+1 < len(matches) else len(text)
        raw = text[m.end():end].strip()
        fields: dict[str, str] = {}
        for name, aliases in [('environment', 'Entorno'), ('tasks', 'Tareas'), ('evidence', 'Evidencia|Evidencias'),
                              ('success', 'Éxito'), ('recovery', 'Recuperación')]:
            hit = re.search(r'(?:\*\*)?(?:'+aliases+r'):(?:\*\*)?\s*(.*?)(?=(?:\*\*)?(?:Entorno|Tareas|Evidencia|Evidencias|Éxito|Recuperación):|\n\n|$)', raw, re.S)
            fields[name] = hit[1].strip().rstrip('*').strip() if hit else ''
        labs.append({'id': m[1], 'title': m[2].strip().rstrip('.').split(' · ')[0], 'raw': raw, **fields})
    theory = text
    for n in range(len(matches)-1, -1, -1):
        end = matches[n+1].start() if n+1 < len(matches) else len(text)
        theory = theory[:matches[n].start()] + theory[end:]
    theory = re.sub(r'(?m)^### Laboratorios\s*$', '', theory).strip()
    return theory, labs


def collect(course: Path = COURSE) -> dict:
    canonical = json.loads(read_text(course / 'planificacion/curriculo.json'))
    chunks: dict[str, tuple[str, str]] = {}
    for path in sorted((course/'modulos').glob('*.md')) + [course/'CAPSTONE.md']:
        text = read_text(path)
        for mid, raw in split_modules(text).items():
            if mid in chunks: raise ValueError('Módulo repetido: ' + mid)
            chunks[mid] = (raw, path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name)
    expected = {f'M{i:02}' for i in range(1,33)}
    if not isinstance(canonical, list) or len(canonical) != 32 or len({m['id'] for m in canonical}) != 32:
        raise ValueError('El catálogo debe contener exactamente 32 IDs únicos.')
    if [m['id'] for m in canonical] != sorted(expected):
        raise ValueError('El catálogo debe estar ordenado de M01 a M32.')
    if set(chunks) != expected or {m['id'] for m in canonical} != expected:
        raise ValueError('El curso debe contener M01–M32, sin módulos ausentes.')
    notes, quizzes = notes_and_quizzes()
    if set(notes) != expected or set(quizzes) != expected: raise ValueError('Apuntes/autoevaluación incompletos.')
    practical_guides: dict[str, dict] = {}
    for path in sorted((course/'practicas').glob('R*.md')):
        raw = read_text(path); ids = re.findall(r'\bL\d{2}[ABC]\b', raw[:600])
        if ids:
            practical_guides[ids[0]] = {'title': raw.splitlines()[0].lstrip('# '), **markdown(raw, path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name, ids[0]+'-guia')}
    modules: list[dict] = []
    for item in canonical:
        mid = item['id']; number = int(mid[1:]); raw, source = chunks[mid]
        theory, labs = labs_from(raw, mid)
        if {x['id'] for x in labs} != {f'L{number:02}{s}' for s in 'ABC'}:
            raise ValueError('Fichas de laboratorio incompletas en ' + mid)
        for lab in labs:
            lab['html'] = markdown(lab.pop('raw'), source, lab['id'])['html']
            if lab['id'] in practical_guides: lab['guide'] = practical_guides[lab['id']]
            lab['hours'] = 10 if number == 32 else 4 if number == 31 else 3
        block = next(b for b in BLOCKS if b[2] <= number <= b[3])
        t, p = (10,30) if number == 32 else (8,12) if number == 31 else (5,9)
        prerequisites = item.get('prerrequisitos', [])
        if any(x not in expected or x >= mid for x in prerequisites): raise ValueError('Prerrequisito inválido: '+mid)
        combined = notes[mid] + '\n\n## Programa y herramientas del módulo\n\n' + re.sub(r'^#[^\n]*\n','',theory)
        combined += related_reading(mid, 'es')
        rendered = markdown(combined, source, mid)
        plain = re.sub('<[^>]+>', ' ', rendered['html'])
        q = quizzes[mid]
        if not isinstance(q.get('correct'), int) or not 0 <= q['correct'] < len(q['options']): raise ValueError('Pregunta inválida: '+mid)
        modules.append({'id':mid, 'title':item['titulo'], 'block':block[0], 'theoryHours':t, 'practiceHours':p,
                        'hours':t+p, 'prerequisites':prerequisites, 'source':REPO+'/blob/main/'+quote(source,safe='/'),
                        'labs':labs, 'quiz':q, 'search':html.unescape(plain), **rendered})
    resources: list[dict] = []
    paths = [course/name for name in PUBLIC_DOCS if (course/name).is_file()]
    paths += sorted((course/'lecciones').glob('[0-9]*.md'))
    paths += [course/name for name in ['PLAN-DOCENTE.md','COMO-ESTUDIAR.md','DESPLIEGUE-ESTATICO.md'] if (course/name).is_file()]
    for index, path in enumerate(paths):
        raw = read_text(path); source = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name
        resources.append({'id': 'D'+str(index+1).zfill(2), 'title':raw.splitlines()[0].lstrip('# '),
                          'kind':'Lección ampliada' if path.parent.name == 'lecciones' else 'Referencia',
                          'source':REPO+'/blob/main/'+quote(source,safe='/'), **markdown(raw, source, 'D'+str(index+1))})
    add_resources(resources, course, ROOT, REPO, markdown, read_text)
    blocks = [{'id':b[0], 'title':b[1], 'description':b[4], 'hours':sum(m['hours'] for m in modules if m['block']==b[0])} for b in BLOCKS]
    result = {'id':'fundamentos-ciberseguridad', 'version':'2.4.0','language':'es', 'repository':REPO, 'modules':modules,
              'blocks':blocks, 'resources':resources, 'hours':sum(m['hours'] for m in modules)}
    if result['hours'] != 480 or sum(m['theoryHours'] for m in modules)!=168: raise ValueError('Carga incoherente.')
    route_content(result)
    return result


def route_content(data: dict) -> None:
    """Enlazar lecturas incluidas dentro del campus, conservando URL fuente."""
    routes = {r['source']: '#/recurso/'+r['id'] for r in data['resources']}
    for m in data['modules']:
        routes.setdefault(m['source'], '#/modulo/'+m['id'])
    def rewrite(text: str) -> str:
        def anchor(hit):
            original = html.unescape(hit[1])
            base, _, fragment = original.partition('#')
            target = routes.get(base)
            if target and fragment and target.startswith('#/modulo/'):
                code = re.search(r'(?i)\bm(\d{2})\b', fragment)
                if code and any(m['id']=='M'+code[1] and m['source']==base for m in data['modules']):
                    target = '#/modulo/M'+code[1]
            return 'href="'+esc(target or original)+'"'
        return re.sub(r'href="([^"]+)"', anchor, text)
    for item in data['modules']+data['resources']:
        item['html'] = rewrite(item['html'])
        for slide in item.get('slides', []): slide['html']=rewrite(slide['html'])
        for lab in item.get('labs', []):
            lab['html']=rewrite(lab['html'])
            if 'guide' in lab: lab['guide']['html']=rewrite(lab['guide']['html'])


def build() -> dict:
    commit = source_commit(ROOT)
    data = collect(); english = collect_en(data, HERE/'locales/en', markdown, read_text); out = HERE/'dist'
    if out.is_symlink(): raise ValueError('dist no puede ser un enlace.')
    if out.exists() and not (out/'.campus-generated').is_file(): raise ValueError('dist no pertenece al generador.')
    stage = Path(tempfile.mkdtemp(prefix='.campus-build-', dir=HERE))
    try:
        (stage/'assets').mkdir()
        for name in ['app.js','state.js','navigation.js','catalog.js','styles.css','catalog.css','i18n.js','portable.js']:
            shutil.copyfile(HERE/'assets'/name, stage/'assets'/name)
        page = read_text(HERE/'index.html')
        (stage/'index.html').write_text(page,encoding='utf-8')
        (stage/'404.html').write_text(not_found_page(),encoding='utf-8')
        (stage/'.assetsignore').write_text('.campus-generated\n',encoding='utf-8')
        (stage/'course.en.json').write_text(json.dumps(english,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
        (stage/'course.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
        (stage/'_headers').write_text('/*\n  Content-Security-Policy: '+CSP+'\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  Cache-Control: no-cache\n',encoding='utf-8')
        (stage/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
        (stage/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#b0142f"/><path d="m16 20 12 12-12 12m20 0h13" fill="none" stroke="white" stroke-width="5"/></svg>',encoding='utf-8')
        body = '<header><p>Wiktor Nykiel · Formación independiente</p><h1>Fundamentos de ciberseguridad</h1><p>Lectura continua · 32 módulos · 480 horas planificadas.</p><a href="./">Volver al campus</a></header><nav aria-label="Índice">'
        body += ''.join(f'<a href="#{m["id"]}">{m["id"]} · {esc(m["title"])}</a><br>' for m in data['modules']) + '</nav>'
        for m in data['modules']:
            body += f'<article id="{m["id"]}"><h1>{m["id"]} · {esc(m["title"])}</h1>{m["html"]}'
            body += ''.join(f'<section><h2>{lab["id"]} · {esc(lab["title"])}</h2>{lab["html"]}</section>' for lab in m['labs'])+'</article>'
        for r in data['resources']:
            body += f'<article id="{r["id"]}"><h1>{esc(r["title"])}</h1>{r["html"]}</article>'
        body = re.sub(r'href="#/(?:modulo|recurso)/(M\d{2}|D\d{2})"', r'href="#\1"', body)
        (stage/'lectura.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lectura · Fundamentos de ciberseguridad</title><link rel="stylesheet" href="assets/styles.css"><body class="print-reader"><main>'+body+'</main></body></html>',encoding='utf-8')
        body_en='<header><p>Wiktor Nykiel · Independent learning</p><h1>Cybersecurity foundations</h1><p>Continuous reading · 32 modules · 480 planned hours.</p><a href="./?lang=en">Open interactive campus</a></header><nav aria-label="Course index">'
        body_en+=''.join(f'<a href="#{m["id"]}">{m["id"]} · {esc(m["title"])}</a><br>' for m in english['modules'])+'</nav>'
        for m in english['modules']:
            body_en+=f'<article id="{m["id"]}"><h1>{m["id"]} · {esc(m["title"])}</h1>{m["html"]}'
            body_en+=''.join(f'<section><h2>{l["id"]} · {esc(l["title"])}</h2>{l["html"]}</section>' for l in m['labs'])+'</article>'
        for r in english['resources']:body_en+=f'<article id="{r["id"]}"><h1>{esc(r["title"])}</h1>{r["html"]}</article>'
        body_en=re.sub(r'href="#/(?:modulo|recurso)/(M\d{2}|D\d{2})"',r'href="#\1"',body_en)
        (stage/'reading.en.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reading · Cybersecurity foundations</title><link rel="stylesheet" href="assets/styles.css"></head><body class="print-reader"><main>'+body_en+'</main></body></html>',encoding='utf-8')
        (stage/'descargas').mkdir()
        with zipfile.ZipFile(stage/'descargas/kit-laboratorio.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for path in public_kit_files(COURSE/'kit'):
                info=zipfile.ZipInfo('kit/'+path.name,(2026,9,14,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        os_report = build_os_classroom(stage)
        (stage/'.campus-generated').write_text('campus-v2\n')
        if out.exists(): shutil.rmtree(out)
        stage.rename(out)
    except BaseException:
        if stage.exists(): shutil.rmtree(stage)
        raise
    report={'modules':len(data['modules']),'labs':sum(len(m['labs']) for m in data['modules']),
            'resources':len(data['resources']),'slides':sum(len(m['slides']) for m in data['modules']),
            'guidedLabs':sum('guide' in lab for m in data['modules'] for lab in m['labs']), 'hours':data['hours']}
    report['languages']=['es','en']
    report['englishModules']=len(english['modules'])
    report['englishLabs']=sum(len(m['labs']) for m in english['modules'])
    report['version']=data['version']
    report['sourceCommit']=commit
    report['osStudy']=os_report
    report['englishCourseSha256']=hashlib.sha256((out/'course.en.json').read_bytes()).hexdigest()
    report['courseSha256']=hashlib.sha256((out/'course.json').read_bytes()).hexdigest()
    (out/'build-info.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(out).as_posix()+'\n' for p in sorted(out.rglob('*')) if p.is_file() and not p.name.startswith('.'))
    (out/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8')
    with zipfile.ZipFile(HERE/'pages-ready.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out.rglob('*')):
            if path.is_file() and not path.name.startswith('.'):
                info=zipfile.ZipInfo(path.relative_to(out).as_posix(),(2026,9,14,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,path.read_bytes())
    print(json.dumps(report,ensure_ascii=False))
    return report

if __name__ == '__main__': build()
