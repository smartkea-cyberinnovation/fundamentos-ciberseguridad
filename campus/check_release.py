#!/usr/bin/env python3
"""Validate a local Pages bundle; no credentials, network or execution of content."""
from __future__ import annotations
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent

def validate(directory: Path, archive: Path) -> dict:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('La salida debe ser un directorio regular.')
    required={'index.html','course.json','course.en.json','reading.en.html','assets/i18n.js','assets/portable.js','lectura.html','_headers','build-info.json','assets/app.js','assets/state.js','assets/navigation.js','assets/styles.css','SHA256SUMS.txt','404.html','assets/catalog.js','assets/catalog.css'}
    files={p.relative_to(directory).as_posix():p for p in directory.rglob('*') if p.is_file() and not p.name.startswith('.')}
    if any(p.is_symlink() for p in directory.rglob('*')): raise ValueError('No se admiten enlaces simbólicos.')
    if not required <= files.keys(): raise ValueError('Faltan activos: '+', '.join(sorted(required-files.keys())))
    if any(p.stat().st_size>=25*1024*1024 for p in files.values()) or len(files)>1000:
        raise ValueError('La salida excede los límites de Direct Upload del panel.')
    expected={}
    for line in files['SHA256SUMS.txt'].read_text().splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not match or match[2] in expected: raise ValueError('Manifiesto incorrecto o duplicado.')
        name=match[2]
        if PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts or name not in files:
            raise ValueError('Ruta de manifiesto inválida.')
        expected[name]=match[1]
        if hashlib.sha256(files[name].read_bytes()).hexdigest()!=match[1]: raise ValueError('Hash incorrecto: '+name)
    if set(expected)!=files.keys()-{'SHA256SUMS.txt'}: raise ValueError('Cobertura de manifiesto incompleta.')
    course=json.loads(files['course.json'].read_text())
    if course['id']!='fundamentos-ciberseguridad' or len(course['modules'])!=32 or course['hours']!=480:
        raise ValueError('Identidad o carga curricular incorrecta.')
    labs=[l for m in course['modules'] for l in m['labs']]
    if len(labs)!=96 or len({l['id'] for l in labs})!=96: raise ValueError('Catálogo de prácticas incorrecto.')
    english=json.loads(files['course.en.json'].read_text())
    if english.get('language')!='en' or course.get('language')!='es': raise ValueError('Idiomas del catálogo incorrectos.')
    if english['id']!=course['id'] or english['hours']!=course['hours'] or english['version']!=course['version']: raise ValueError('Ediciones incompatibles.')
    for key in ('modules','resources'):
        if [x['id'] for x in english[key]]!=[x['id'] for x in course[key]]: raise ValueError('Identificadores bilingües incompatibles.')
    for es,en in zip(course['modules'],english['modules']):
        if [x['id'] for x in es['labs']]!=[x['id'] for x in en['labs']] or es['hours']!=en['hours']: raise ValueError('Laboratorios bilingües incompatibles.')
        if not en['html'].strip() or not en['quiz']['question']: raise ValueError('Contenido traducido vacío.')
    headers=files['_headers'].read_text()
    for value in ["script-src 'self'","object-src 'none'","frame-ancestors 'none'",'nosniff']:
        if value not in headers: raise ValueError('Falta una protección: '+value)
    if 'unsafe-inline' in headers or 'unsafe-eval' in headers: raise ValueError('CSP permisiva.')
    for rel in ('index.html','lectura.html','reading.en.html'):
        text=files[rel].read_text()
        for target in re.findall(r'(?:src|href)="([^"]+)"',text):
            if target.startswith(('https://','#','./')): continue
            clean=target.partition('#')[0].partition('?')[0]
            if clean and clean not in files: raise ValueError('Activo HTML inexistente: '+clean)
    with zipfile.ZipFile(archive) as z:
        if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(files):
            raise ValueError('El ZIP no coincide con los activos publicados.')
        for name in z.namelist():
            if name.startswith('/') or '..' in PurePosixPath(name).parts: raise ValueError('Ruta ZIP no válida.')
            if z.read(name)!=files[name].read_bytes(): raise ValueError('Contenido ZIP diferente: '+name)
    return {'status':'passed','version':course['version'],'modules':32,'labs':96,'hours':480,
            'languages':['es','en'],'englishModules':len(english['modules']),'englishLabs':sum(len(m['labs']) for m in english['modules']),
            'assets':len(files),'zipBytes':archive.stat().st_size,'zipSha256':hashlib.sha256(archive.read_bytes()).hexdigest()}

if __name__=='__main__':
    print(json.dumps(validate(HERE/'dist',HERE/'pages-ready.zip'),ensure_ascii=False,indent=2))
