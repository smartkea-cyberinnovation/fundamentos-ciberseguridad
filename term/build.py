#!/usr/bin/env python3
"""Build the complete static TERM course. Standard library; no content execution.

Public inputs are explicitly listed. Build output never includes local .env,
terminal transcripts, credentials, Docker volumes or learner workspaces.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COURSE_ID = 'smartkea-term-linux'
PUBLIC_PATH = '/fundamentos-ciberseguridad/term/'
PUBLIC_URL = 'https://www.smartkea.com' + PUBLIC_PATH
VERSION = '1.0.0'
MARKER = '.term-generated'
ASSETS = ('app.js', 'state.js', 'styles.css')
DOCS = ('README.md', 'GUIA-DOCENTE.md', 'DEPLOY.md', 'SECURITY.md', 'CONEXION-TTYD.md', 'LABS.md', 'ARQUITECTURA.md', 'VALIDACION.md', 'EDICION.md', 'LICENSE.md', 'SWARM.md', 'INSTRUCTOR.md', 'SOURCES.md', 'VALIDATION.md')
BASE_CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#075cc6"/><path d="m15 19 13 13-13 13m21 0h14" fill="none" stroke="white" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_public(path: Path) -> str:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents) or not path.is_file() or path.stat().st_size > 3_000_000:
        raise ValueError(f'Public source missing or invalid: {path.name}')
    return path.read_text(encoding='utf-8')


def source_commit() -> str | None:
    try:
        value = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL, timeout=10).strip()
        return value if re.fullmatch(r'[a-f0-9]{40}', value) else None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def source_dirty() -> bool | None:
    try:
        return bool(subprocess.check_output(['git', 'status', '--porcelain', '--', 'term'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL, timeout=10).strip())
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def collect(directory: Path = HERE / 'content') -> dict:
    modules = []
    for name in ('core.json', 'security.json'):
        data = json.loads(read_public(directory / name))
        modules.extend(data['modules'])
    if [m['id'] for m in modules] != [f'm{i:02}' for i in range(1, 17)]:
        raise ValueError('Expected the complete 16-module Linux course in order.')
    ids, questions = set(), set()
    def require_text(value):
        if not isinstance(value, str) or not value.strip() or '\x00' in value:
            raise ValueError('Empty or invalid course text.')
    for module in modules:
        for key in ('title', 'summary', 'level'):
            require_text(module[key])
        if len(module['lessons']) != 3:
            raise ValueError('Each module requires three complete lessons.')
        for i, lesson in enumerate(module['lessons'], 1):
            ident = lesson['id']
            if ident != f"{module['id']}-l{i:02}" or ident in ids:
                raise ValueError('Invalid or duplicate lesson ID.')
            ids.add(ident)
            if not isinstance(lesson['minutes'], int) or not 15 <= lesson['minutes'] <= 240:
                raise ValueError('Invalid teaching time.')
            for key in ('title', 'summary'):
                require_text(lesson[key])
            for key in ('objectives', 'prerequisites', 'takeaways'):
                if not isinstance(lesson[key], list) or not lesson[key]:
                    raise ValueError(f'Missing {key}: {ident}')
                for value in lesson[key]: require_text(value)
            if len(lesson['sections']) < 3 or len(lesson['steps']) < 3 or len(lesson['quiz']) < 2:
                raise ValueError(f'Incomplete lesson: {ident}')
            for section in lesson['sections']:
                require_text(section['title'])
                if not section['body']: raise ValueError('Missing concept explanation.')
                for value in section['body']: require_text(value)
            for step in lesson['steps']:
                for key in ('title','command','explanation','expected','verify','undo','environment','caution'):
                    require_text(step[key])
                if step['shell'] not in ('bash','sh'): raise ValueError('Scope limited to Linux shells.')
            for q in lesson['quiz']:
                require_text(q['question']); require_text(q['explanation'])
                if q['question'] in questions: raise ValueError('Duplicate question.')
                questions.add(q['question'])
                if len(q['options']) != 4 or len(set(q['options'])) != 4 or type(q['answer']) is not int or not 0 <= q['answer'] < 4:
                    raise ValueError('Invalid quiz answer or options.')
            c = lesson['challenge']
            for key in ('title','brief','solution'): require_text(c[key])
            for key in ('deliverables','hints','rubric'):
                if not c[key]: raise ValueError('Incomplete challenge.')
                for value in c[key]: require_text(value)
            if len(lesson['sources']) < 2: raise ValueError('Missing primary references.')
            for source in lesson['sources']:
                require_text(source['title'])
                parsed = urlsplit(source['url'])
                if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError('Reference must use an HTTPS URL without credentials.')
    lessons = [l for m in modules for l in m['lessons']]
    return {'id':COURSE_ID, 'version':VERSION, 'language':'es', 'title':'Terminal Linux y seguridad',
            'author':'Wiktor Nykiel · SmartKEA', 'editionDate':'2026-10-07',
            'minutes':sum(l['minutes'] for l in lessons), 'modules':modules}


def lab_config(environ=None) -> dict:
    env = os.environ if environ is None else environ
    url = env.get('TERM_LAB_URL', '').strip()
    allowed = [x.strip() for x in env.get('TERM_LAB_ALLOWED_ORIGINS','').split(',') if x.strip()]
    if not url:
        if allowed or env.get('TERM_LAB_EMBED','0') not in ('0',''):
            raise ValueError('Set TERM_LAB_URL before enabling an origin or embedding.')
        return {'url':'','allowedOrigins':[],'embed':False}
    if len(allowed) > 8: raise ValueError('Too many lab origins.')
    canonical=[]
    for origin in allowed:
        u = urlsplit(origin)
        if u.scheme != 'https' or not re.fullmatch(r'[A-Za-z0-9.-]+(?::[0-9]{1,5})?',u.netloc) or u.path or u.query or u.fragment:
            raise ValueError('Lab origins must be exact HTTPS origins; wildcards are prohibited.')
        if u.hostname.lower() in ('smartkea.com','www.smartkea.com','localhost'):
            raise ValueError('Use a separate HTTPS hostname for ttyd.')
        try: port=u.port
        except ValueError: raise ValueError('Lab origin has an invalid port.') from None
        if port is not None and not 1 <= port <= 65535: raise ValueError('Lab origin has an invalid port.')
        canonical.append('https://'+u.hostname.lower()+(f':{port}' if port not in (None,443) else ''))
    u = urlsplit(url)
    try: port=u.port
    except ValueError: raise ValueError('Lab URL has an invalid port.') from None
    origin = 'https://'+(u.hostname or '').lower()+(f':{port}' if port not in (None,443) else '')
    if u.scheme!='https' or u.username or u.password or origin not in canonical or u.query or u.fragment or '%' in u.netloc or any(c in url for c in ('\r','\n','\t',' ','\\')):
        raise ValueError('Lab URL must match an approved origin and contain no credentials, query or fragment.')
    if env.get('TERM_LAB_EMBED','0') not in ('0','1',''):
        raise ValueError('TERM_LAB_EMBED must be 0 or 1.')
    return {'url':origin+(u.path or '/'), 'allowedOrigins':list(dict.fromkeys(canonical)), 'embed':env.get('TERM_LAB_EMBED') == '1'}


def headers(lab: dict, pattern: str = '/*') -> str:
    frames = ' '.join(lab['allowedOrigins']) if lab['embed'] else "'none'"
    return (pattern + '\n  Content-Security-Policy: ' + BASE_CSP + '; frame-src ' + frames + '\n'
            '  X-Content-Type-Options: nosniff\n  X-Frame-Options: DENY\n'
            '  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n'
            '  Cache-Control: no-cache\n')


def inline(text: str) -> str:
    text = html.escape(str(text), quote=True)
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    return re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)


def plist(values):
    return '<ul>' + ''.join('<li>'+inline(v)+'</li>' for v in values) + '</ul>'


def shell_document(title: str, body: str, *, base='./', doc=False) -> str:
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="light"><meta name="referrer" content="no-referrer">'
            f'<title>{html.escape(title)} · TERM · SmartKEA</title>'
            f'<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">'
            f'<link rel="stylesheet" href="{base}assets/styles.css"></head>'
            f'<body class="manual-body {"doc-body" if doc else ""}"><main class="manual-wrap">'
            '<header class="manual-header"><span class="eyebrow">SMARTKEA / TERM · WIKTOR NYKIEL</span>'
            f'<h1>{html.escape(title)}</h1><a class="button" href="{base}">Abrir curso interactivo</a>'
            f' <a class="button" href="{base}manual.html">Manual completo</a></header>' + body +
            '<footer class="manual-footer"><p>SmartKEA · Edición 7 de octubre de 2026. '
            'Prácticas con datos sintéticos en entornos propios de laboratorio.</p></footer></main></body></html>')


def manual(data: dict) -> str:
    body = ('<p>Curso práctico de GNU/Linux, sh, Bash, shellscript, Kali, Docker, redes y seguridad. '
            'Lee, anticipa el efecto, practica, verifica y explica. Cada bloque incluye reto y solución.</p>'
            f'<p>16 módulos · 48 lecciones · {data["minutes"]/60:g} horas orientativas. '
            'Los tiempos son una planificación docente, no un requisito para superar la formación.</p>'
            '<p>Los resultados esperados son orientativos: se contrastan con tu propia VM. '
            'La web no ejecuta estos comandos. Mantén la misma terminal entre pasos que comparten variables.</p>'
            '<nav class="manual-nav" aria-label="Índice del manual"><h2>Índice</h2>')
    for m in data['modules']:
        body += f'<a href="#{m["id"]}">{m["id"][1:]} · {html.escape(m["title"])}</a>'
    body += '</nav>'
    for m in data['modules']:
        body += f'<section class="manual-module" id="{m["id"]}"><p class="eyebrow">MÓDULO {m["id"][1:]}</p><h1>{html.escape(m["title"])}</h1><p>{inline(m["summary"])}</p>'
        for l in m['lessons']:
            body += f'<article class="manual-lesson" id="{l["id"]}"><h2>{html.escape(l["title"])}</h2><p>{inline(l["summary"])}</p><p class="muted">{l["minutes"]} minutos orientativos</p><h3>Al terminar podrás</h3>'+plist(l['objectives'])+'<h3>Antes de empezar</h3>'+plist(l['prerequisites'])
            for s in l['sections']:
                body += '<section><h3>'+html.escape(s['title'])+'</h3>'+''.join('<p>'+inline(p)+'</p>' for p in s['body'])+'</section>'
            body += '<h3>Práctica paso a paso</h3>'
            for i,s in enumerate(l['steps'],1):
                body += f'<section class="manual-step"><h4>{i}. {html.escape(s["title"])}</h4><p><strong>Entorno:</strong> {inline(s["environment"])} · {s["shell"]}</p><pre><code>{html.escape(s["command"])}</code></pre>'
                for key,label in (('explanation','Qué hace y por qué'),('expected','Resultado orientativo'),('verify','Cómo verificar'),('caution','Antes de ejecutar'),('undo','Reversión')):
                    body += f'<p><strong>{label}:</strong> {inline(s[key])}</p>'
                body += '</section>'
            c=l['challenge']
            body += '<section><h3>Reto: '+html.escape(c['title'])+'</h3><p>'+inline(c['brief'])+'</p><h4>Entregables</h4>'+plist(c['deliverables'])+'<h4>Pistas</h4>'+plist(c['hints'])+'<h4>Solución razonada</h4><pre>'+html.escape(c['solution'])+'</pre><h4>Criterios de aceptación</h4>'+plist(c['rubric'])+'</section><h3>Comprueba tu comprensión</h3>'
            for q in l['quiz']:
                body += '<section class="manual-quiz"><h4>'+html.escape(q['question'])+'</h4><ol>'+''.join('<li>'+inline(o)+'</li>' for o in q['options'])+'</ol><p><strong>'+chr(65+q['answer'])+'. '+inline(q['options'][q['answer']])+'</strong></p><p>'+inline(q['explanation'])+'</p></section>'
            body += '<h3>Ideas que debes recordar</h3>'+plist(l['takeaways'])+'<h3>Fuentes primarias</h3><ul>'+''.join(f'<li><a href="{html.escape(s["url"],quote=True)}" rel="noopener noreferrer">{html.escape(s["title"])}</a></li>' for s in l['sources'])+'</ul></article>'
        body += '</section>'
    return shell_document('Terminal Linux y seguridad · Manual completo',body)


def markdown_doc(text: str, source: str) -> str:
    """Small escaped Markdown renderer for our documentation, not arbitrary HTML."""
    def mdinline(value):
        def link(match):
            label,target=match[1],html.unescape(match[2])
            if target.startswith(('https://','#')):
                href=target
            elif Path(target.split('#')[0]).name in DOCS:
                href=Path(target.split('#')[0]).stem+'.html'+('#'+target.split('#',1)[1] if '#' in target else '')
            else:
                path=PurePosixPath('term/docs')/target
                href='https://github.com/smartkea-cyberinnovation/fundamentos-ciberseguridad/blob/main/'+str(path)
            return f'<a href="{html.escape(href,quote=True)}">{label}</a>'
        return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,inline(value))
    out=[]; code=None; para=[]; listing=None; rows=[]
    def flush():
        nonlocal listing,rows
        if para: out.append('<p>'+mdinline(' '.join(para))+'</p>');para.clear()
        if listing: out.append('</'+listing+'>');listing=None
        if rows:
            head=rows[0];body=rows[2:] if len(rows)>1 and re.match(r'^\s*\|?\s*:?-',rows[1]) else rows[1:]
            cells=lambda r:[c.strip() for c in r.strip().strip('|').split('|')]
            out.append('<table><thead><tr>'+''.join('<th>'+mdinline(c)+'</th>' for c in cells(head))+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+mdinline(c)+'</td>' for c in cells(r))+'</tr>' for r in body)+'</tbody></table>');rows=[]
    for line in text.splitlines():
        if line.startswith('```'):
            if code is None: flush();code=[]
            else: out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');code=None
            continue
        if code is not None:code.append(line);continue
        if line.lstrip().startswith('|'):flush() if not rows else None;rows.append(line);continue
        if rows:flush()
        if not line.strip():flush();continue
        if (h:=re.match(r'^(#{1,6})\s+(.+)',line)):
            flush();level=len(h[1]);ident=re.sub(r'[^\w-]+','-',h[2].lower()).strip('-');out.append(f'<h{level} id="{ident}">'+mdinline(h[2])+f'</h{level}>');continue
        if (li:=re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)',line)):
            if para:flush()
            if not listing:listing='ul';out.append('<ul>')
            out.append('<li>'+mdinline(li[1])+'</li>');continue
        if listing:flush()
        if line.startswith('> '):flush();out.append('<blockquote>'+mdinline(line[2:])+'</blockquote>');continue
        para.append(line)
    if code is not None:raise ValueError('Unclosed documentation code block: '+source)
    flush();return '<div class="doc-content">'+''.join(out)+'</div>'


def public_lab_files() -> list[tuple[str,Path]]:
    names = json.loads(read_public(HERE/'labs/public-files.json'))
    if not isinstance(names,list) or not names:raise ValueError('Missing explicit lab download inventory.')
    files=[]
    for name in names:
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or name in ('.env',) or any(x in ('secrets','workspace','evidence') for x in p.parts):
            raise ValueError('Unsafe lab inventory path.')
        path=HERE/'labs'/p
        read_public(path)
        files.append(('labs/'+name,path))
    for name in DOCS:
        path=HERE/'README.md' if name=='README.md' else HERE/'docs'/name
        read_public(path)
        files.append(('README.md' if name=='README.md' else 'docs/'+name,path))
    return files


def zip_files(output: Path, files: list[tuple[str,Path]]):
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name,path in sorted(files):
            info=zipfile.ZipInfo(name,(2026,10,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100755 if name.endswith('.sh') else 0o100644)<<16
            z.writestr(info,path.read_bytes())


def public_files(path: Path) -> dict[str,Path]:
    if path.is_symlink() or not path.is_dir(): raise ValueError('Invalid output directory.')
    out={}
    for p in path.rglob('*'):
        if p.is_symlink():raise ValueError('Symlinks not allowed in public output.')
        if p.is_file() and not any(x.startswith('.') for x in p.relative_to(path).parts):out[p.relative_to(path).as_posix()]=p
    return out


def validate(directory: Path = HERE/'dist') -> dict:
    files=public_files(directory)
    required={'index.html','manual.html','course.json','config.json','build-info.json','favicon.svg','_headers','404.html','SHA256SUMS.txt','downloads/labs.zip'}|{'assets/'+a for a in ASSETS}|{'docs/'+Path(d).stem+'.html' for d in DOCS}
    if not required <= files.keys():raise ValueError('Incomplete TERM release: '+','.join(sorted(required-files.keys())))
    expected={}
    for line in files['SHA256SUMS.txt'].read_text().splitlines():
        match=re.fullmatch(r'([a-f0-9]{64})  (.+)',line)
        if not match or match[2] in expected or match[2] not in files:raise ValueError('Invalid release manifest.')
        expected[match[2]]=match[1]
        if digest(files[match[2]])!=match[1]:raise ValueError('Release digest mismatch: '+match[2])
    if set(expected)!=files.keys()-{'SHA256SUMS.txt'}:raise ValueError('Incomplete manifest coverage.')
    info=json.loads(files['build-info.json'].read_text())
    if info['modules']!=16 or info['lessons']!=48 or info['questions']!=96:raise ValueError('Incomplete teaching edition.')
    for rel,path in files.items():
        if path.suffix!='.html':continue
        for value in re.findall(r'(?:href|src)="([^"]+)"',path.read_text()):
            u=urlsplit(html.unescape(value))
            if u.scheme or value.startswith('#'):continue
            if not u.path:continue
            target=(path.parent/u.path).resolve()
            if not target.is_relative_to(directory.resolve()):raise ValueError('HTML reference escapes release.')
            if target.is_dir():target=target/'index.html'
            if not target.is_file():raise ValueError('Broken HTML asset: '+rel+' -> '+value)
    return dict(info,status='passed',assets=len(files),manifestSha256=digest(files['SHA256SUMS.txt']))


def build(output: Path = HERE/'dist') -> dict:
    data=collect();lab=lab_config()
    if output.is_symlink() or (output.exists() and not (output/MARKER).is_file()):raise ValueError('Refusing to overwrite an unrelated output directory.')
    # Capture provenance before creating our own untracked staging directory.
    revision=source_commit();dirty=source_dirty()
    temporary=Path(tempfile.mkdtemp(prefix='.term-build-',dir=output.parent))
    try:
        (temporary/'assets').mkdir();(temporary/'docs').mkdir();(temporary/'downloads').mkdir()
        for name in ASSETS:(temporary/'assets'/name).write_text(read_public(HERE/'assets'/name))
        (temporary/'index.html').write_text(read_public(HERE/'index.html'))
        (temporary/'course.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
        (temporary/'config.json').write_text(json.dumps({'lab':lab,'version':VERSION},ensure_ascii=False))
        (temporary/'_headers').write_text(headers(lab))
        (temporary/'favicon.svg').write_text(FAVICON)
        (temporary/'manual.html').write_text(manual(data))
        (temporary/'404.html').write_text(shell_document('No se encontró esta página','<p>Abre el itinerario y selecciona una lección.</p>'))
        for name in DOCS:
            source=HERE/name if name=='README.md' else HERE/'docs'/name
            text=read_public(source);title=text.splitlines()[0].lstrip('# ').strip()
            (temporary/'docs'/(Path(name).stem+'.html')).write_text(shell_document(title,markdown_doc(text,name),base='../',doc=True))
        zip_files(temporary/'downloads/labs.zip',public_lab_files())
        lessons=[l for m in data['modules'] for l in m['lessons']]
        info={'id':COURSE_ID,'version':VERSION,'sourceCommit':revision,'sourceDirty':dirty,
              'publicUrl':PUBLIC_URL,'publicBasePath':PUBLIC_PATH,'modules':len(data['modules']),'lessons':len(lessons),
              'questions':sum(len(l['quiz']) for l in lessons),'steps':sum(len(l['steps']) for l in lessons),
              'minutes':data['minutes'],'courseSha256':digest(temporary/'course.json'),
              'contentSha256':hashlib.sha256((read_public(HERE/'content/core.json')+read_public(HERE/'content/security.json')).encode()).hexdigest(),
              'labConfigured':bool(lab['url'])}
        (temporary/'build-info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
        (temporary/MARKER).write_text('term-v1\n');(temporary/'.assetsignore').write_text(MARKER+'\n')
        (temporary/'SHA256SUMS.txt').write_text(''.join(digest(p)+'  '+name+'\n' for name,p in sorted(public_files(temporary).items())))
        report=validate(temporary)
        if output.exists():shutil.rmtree(output)
        temporary.rename(output)
        return report
    except BaseException:
        shutil.rmtree(temporary);raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    print(json.dumps(validate() if args.check else build(),ensure_ascii=False,indent=2))
