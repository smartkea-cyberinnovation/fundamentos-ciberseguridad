"""Append-only explicit ES/EN readings. No network, execution or progress migration."""
from pathlib import Path
from urllib.parse import quote

READINGS = tuple((f'D{n:02}', name) for n,name in enumerate((
    '01-computing.md','02-history.md','03-hardware.md','04-networks.md',
    '05-web.md','06-security.md','07-information.md','08-identity.md',
    '09-careers.md','10-glossary.md','11-sources.md','12-curriculum.md','13-ecosystem.md',
    '14-library.md','15-master-glossary.md'),26))
IDS = frozenset(r[0] for r in READINGS)
OUTLINE_IDS = frozenset(('D37', 'D38', 'D39', 'D40'))

def editions(raw: str) -> dict[str,str]:
    if raw.count('<!-- ES -->') != 1 or raw.count('<!-- EN -->') != 1:
        raise ValueError('Exactly one ES and EN section is required')
    if not raw.startswith('<!-- ES -->') or raw.count('<!-- COMMON -->') > 1:
        raise ValueError('Invalid reading delimiters')
    es,en = raw[len('<!-- ES -->'):].split('<!-- EN -->',1)
    common = ''
    if '<!-- COMMON -->' in es:
        raise ValueError('Shared content must follow both editions')
    if '<!-- COMMON -->' in en:
        en,common = en.split('<!-- COMMON -->',1)
    result = {}
    for lang,body in (('es',es),('en',en)):
        body = body.strip()
        if not body.startswith('# ') or len(body.splitlines()) < 3:
            raise ValueError('Each edition needs a title and body')
        result[lang] = body + ('\n\n'+common.strip() if common.strip() else '')
    return result

def folder(course: Path) -> Path:
    return course.parent/'itinerario-integral'

def translated_resources(directory: Path, read_text) -> dict[str,str]:
    base = directory.parents[2]/'formacion/itinerario-integral'
    result = {}
    for rid,name in READINGS:
        raw = editions(read_text(base/name))['en']
        title,body = raw.split('\n',1)
        result[rid] = '# '+rid+' · '+title[2:].strip()+'\n'+body
    return result

def add_resources(resources, course, root, repo, markdown, read_text) -> None:
    if [r['id'] for r in resources] != [f'D{i:02}' for i in range(1,26)]:
        raise ValueError('Preserve D01-D25 before appending the integral readings')
    for rid,name in READINGS:
        path = folder(course)/name
        raw = editions(read_text(path))['es']
        title,body = raw.split('\n',1)
        source = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
        resources.append({'id':rid,'title':title[2:].strip(),
            'kind':'Esquema de estudio' if rid in OUTLINE_IDS else 'Lección ampliada',
            'source':repo+'/blob/main/'+quote(source,safe='/'),
            **markdown(body.strip(),source,rid)})
