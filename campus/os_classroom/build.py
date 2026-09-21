"""Compile one-concept learning views and no-JavaScript OS readers."""
from __future__ import annotations
import html
import json
import re
import shutil
from pathlib import Path
from .common import LESSONS as COMMON
from .linux import LESSONS as LINUX
from .windows import LESSONS as WINDOWS
from .macos import LESSONS as MACOS
from .sources import REFERENCES

HERE = Path(__file__).resolve().parent
LESSONS = COMMON + LINUX + WINDOWS + MACOS


def language(value, lang):
    if isinstance(value, dict):
        if set(value) == {'es', 'en'}:
            if not all(isinstance(v, str) and v.strip() for v in value.values()):
                raise ValueError('Missing translation')
            return value[lang]
        return {k: language(v, lang) for k, v in value.items()}
    if isinstance(value, list):
        return [language(v, lang) for v in value]
    return value


def views(lesson, lang):
    es = lang == 'es'
    result = []
    def add(kind, title, body='', **extra):
        result.append(dict(id=f'{lesson["id"]}:{len(result)}', kind=kind,
                           title=title, body=body, **extra))
    add('goal', lesson['question'], lesson['outcome'])
    for concept in lesson['concepts']:
        add('concept', concept['title'], concept['body'], takeaway=concept['takeaway'])
        add('micro', ('Comprueba: ' if es else 'Check: ') + concept['title'],
            ('Sin mirar la explicación, describe una situación de esta lección en la que importa esta idea. Identifica un dato que observarías y uno que NO podrías concluir solo con ese dato.' if es else 'Without looking back, describe a situation in this lesson where this idea matters. Identify one fact you would observe and one conclusion you could NOT draw from it alone.'),
            expected=concept['takeaway'])
    add('diagram', 'Relaciona las piezas' if es else 'Connect the parts', diagram=lesson['diagram'])
    ex = lesson['example']
    add('example', ex['title'], ex['explanation'], code=ex['command'], shell=ex['shell'], expected=ex['expected'])
    lab = lesson['lab']
    add('environment', 'Prepara tu práctica' if es else 'Prepare your lab', lab['environment'], expected=lab['success'])
    for n, step in enumerate(lab['steps'], 1):
        add('lab', f'{n}. {step["title"]}', code=step['command'], expected=step['expected'], shell=ex['shell'])
    add('quiz', lesson['quiz']['question'], quiz=lesson['quiz'])
    add('evidence', 'Comprueba y conserva evidencia' if es else 'Verify and retain evidence', lab['evidence'], expected=lab['success'])
    add('recovery', 'Recupera y cierra' if es else 'Recover and close', lab['recovery'])
    add('handover', 'Explica tu decisión' if es else 'Explain your decision', lesson['summary'], expected=(
        'En cinco líneas: objetivo, resultado observado, evidencia, límite y siguiente acción. Compara corregir frente a sustituir: esfuerzo, impacto y reversibilidad. No inventes eficacia, ahorro o atribución.' if es else
        'In five lines: goal, observed result, evidence, limitation and next action. Compare fixing with replacing: effort, impact and reversibility. Do not invent effectiveness, savings or attribution.'))
    return result


def catalog(lang):
    if lang not in ('es', 'en'):
        raise ValueError('Unsupported language')
    items = []
    seen = set()
    for raw in LESSONS:
        lesson = language(raw, lang)
        if lesson['id'] in seen or not re.fullmatch(r'OS-[CLWA]\d{2}', lesson['id']):
            raise ValueError('Invalid lesson ID')
        seen.add(lesson['id'])
        if len(lesson['concepts']) != 3 or len(lesson['diagram']) != 4 or not lesson['lab']['steps']:
            raise ValueError('Incomplete lesson')
        if any(ref not in REFERENCES for ref in lesson['refs']):
            raise ValueError('Unknown primary reference')
        lesson['group'] = {'C':'common', 'L':'linux', 'W':'windows', 'A':'macos'}[lesson['id'][3]]
        lesson['views'] = views(lesson, lang)
        lesson['sources'] = [{'title':REFERENCES[r][0], 'url':REFERENCES[r][1]} for r in lesson['refs']]
        items.append(lesson)
    return dict(id='smartkea-os-study', version=1, language=lang, lessons=items)


def render_reading(data):
    esc = html.escape
    lang = data['language']
    title = 'Sistemas operativos · Lectura' if lang == 'es' else 'Operating systems · Reading'
    text = f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="study.css"></head><body class="reader"><header><a href="./?lang={lang}">Aula / Classroom</a><h1>{title}</h1></header><main><nav aria-label="Index">'
    text += ''.join(f'<p><a href="#{x["id"]}">{x["id"]} · {esc(x["title"])}</a></p>' for x in data['lessons']) + '</nav>'
    for item in data['lessons']:
        text += f'<article id="{item["id"]}"><h2>{item["id"]} · {esc(item["title"])}</h2>'
        for view in item['views']:
            text += '<section><h3>'+esc(view['title'])+'</h3><p>'+esc(view.get('body',''))+'</p>'
            if view.get('diagram'):
                text += '<ol>'+''.join('<li>'+esc(d)+'</li>' for d in view['diagram'])+'</ol>'
            if view.get('code'):
                text += '<pre><code>'+esc(view['code'])+'</code></pre>'
            text += '<p>'+esc(view.get('expected',''))+'</p>'
            if view.get('quiz'):
                q = view['quiz']
                text += '<ol>'+''.join('<li>'+esc(o)+'</li>' for o in q['options'])+'</ol><details><summary>Solución / Answer</summary><p>'+esc(q['explanation'])+'</p></details>'
            text += '</section>'
        text += '<ul>'+''.join(f'<li><a href="{esc(r["url"], quote=True)}" rel="noreferrer">{esc(r["title"])}</a></li>' for r in item['sources'])+'</ul></article>'
    return text+'</main></body></html>'


def build_into(stage: Path):
    target = stage/'sistemas'
    target.mkdir()
    for name in ('index.html','study.css','study.js','model.js','environment.js'):
        path = HERE/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Missing OS classroom asset: '+name)
        shutil.copyfile(path, target/name)
    for lang in ('es','en'):
        data = catalog(lang)
        (target/f'course.{lang}.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
        (target/f'reading.{lang}.html').write_text(render_reading(data),encoding='utf-8')
    return {'lessons':len(LESSONS), 'concepts':sum(len(x['concepts']) for x in LESSONS), 'languages':['es','en']}
