"""Build the reviewed 100-question practice bank and its static application."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil

HERE = Path(__file__).resolve().parent
BANK = HERE.parent / 'formacion/introduccion-informatica/banco-preguntas.json'
ASSETS = ('index.html', 'exam.css', 'exam.js', 'model.mjs')


def validate_bank(data: dict, resource_ids: set[str]) -> None:
    if not isinstance(data, dict) or data.get('schemaVersion') != 1:
        raise ValueError('Unsupported practice bank schema.')
    topics = data.get('topics', [])
    if not isinstance(topics, list) or [t.get('id') for t in topics] != [f'T{i:02}' for i in range(1,13)]:
        raise ValueError('The bank must identify all twelve syllabus topics.')
    topic_ids = {t['id'] for t in topics}
    questions = data.get('questions', [])
    if not isinstance(questions, list) or len(questions) != 100:
        raise ValueError('The reviewed bank must contain exactly 100 questions.')
    seen, prompts, used_topics = set(), set(), set()
    for question in questions:
        qid = question.get('id')
        if not isinstance(qid, str) or not re.fullmatch(r'INF-\d{3}', qid) or qid in seen:
            raise ValueError('Invalid or duplicate question ID.')
        seen.add(qid)
        if question.get('topic') not in topic_ids:
            raise ValueError('Unknown question topic: '+qid)
        used_topics.add(question['topic'])
        if question.get('difficulty') not in ('basico', 'intermedio', 'aplicacion'):
            raise ValueError('Unknown difficulty: '+qid)
        for key in ('prompt', 'explanation'):
            if not isinstance(question.get(key), str) or not question[key].strip():
                raise ValueError('Missing question content: '+qid)
        prompt = question['prompt'].strip().casefold()
        if prompt in prompts:
            raise ValueError('Duplicate question wording: '+qid)
        prompts.add(prompt)
        options = question.get('options', [])
        if (not isinstance(options, list) or len(options) != 4
                or {x.get('id') for x in options} != set('abcd')
                or any(not isinstance(x.get('text'), str) or not x['text'].strip() for x in options)
                or len({x['text'].strip().casefold() for x in options}) != 4
                or question.get('correctOptionId') not in set('abcd')):
            raise ValueError('Four distinct options and one correct answer are required: '+qid)
        study = question.get('study', {})
        target = re.fullmatch(r'\.\./#/recurso/(D\d{2})', study.get('url', ''))
        if not target or target[1] not in resource_ids or not study.get('label'):
            raise ValueError('Study reference does not resolve: '+qid)
    if used_topics != topic_ids:
        raise ValueError('At least one syllabus topic has no practice question.')


def build_into(stage: Path, resource_ids: set[str]) -> dict:
    if BANK.is_symlink() or not BANK.is_file() or BANK.stat().st_size > 1_000_000:
        raise ValueError('Missing or unsafe practice bank source.')
    data = json.loads(BANK.read_text(encoding='utf-8'))
    validate_bank(data, resource_ids)
    target = stage / 'examen'
    target.mkdir()
    for name in ASSETS:
        source = HERE / 'exam' / name
        if source.is_symlink() or not source.is_file() or source.stat().st_size > 1_000_000:
            raise ValueError('Missing practice application asset: '+name)
        shutil.copyfile(source, target / name)
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    (target/'questions.json').write_bytes(payload)
    return {'questions': len(data['questions']), 'sessionQuestions': 20,
            'topics': len(data['topics']), 'language': 'es', 'version': data['version'],
            'bankSha256': hashlib.sha256(payload).hexdigest()}
