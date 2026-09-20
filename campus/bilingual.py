"""Build the reviewed English teaching edition. Never fall back silently to Spanish."""
from __future__ import annotations
import csv
import html
import re
from pathlib import Path

BLOCKS_EN = [
 ('Foundations and method','Understand before automating.'),
 ('Linux and Bash','Files, permissions, services and reliable scripts.'),
 ('Windows, CMD, BAT and PowerShell','Native administration through objects and access controls.'),
 ('macOS, Darwin and zsh','Understand the Apple platform and its Unix foundations.'),
 ('Operations and cybersecurity','Connect, protect, observe and investigate.'),
 ('Terminal AI','Assistance with context, boundaries and independent verification.'),
 ('Capstone project','Build, operate, explain and recover a system.')]


def chunks(text: str, pattern: str) -> dict[str, str]:
    matches=list(re.finditer(pattern,text,re.M))
    result={}
    for n,m in enumerate(matches):
        if m[1] in result: raise ValueError('Duplicate translated ID: '+m[1])
        result[m[1]]=text[m.start():matches[n+1].start() if n+1<len(matches) else len(text)].strip()
    return result


def collect_en(spanish: dict, directory: Path, markdown, read_text) -> dict:
    modules={}; resources={}
    for name in ('foundations-linux.md','windows-macos.md','operations-capstone.md'):
        part=chunks(read_text(directory/name),r'^# (M\d{2}) · ')
        if modules.keys() & part.keys(): raise ValueError('Repeated translated module')
        modules.update(part)
    for name in ('references-core.md','references-learning.md'):
        part=chunks(read_text(directory/name),r'^# (D\d{2}) · ')
        if resources.keys() & part.keys(): raise ValueError('Repeated translated resource')
        resources.update(part)
    guides=chunks(read_text(directory/'guides.md'),r'^# (L\d{2}[ABC]) · ')
    quiz={}
    for row in csv.reader(read_text(directory/'quizzes.tsv').splitlines(),delimiter='\t'):
        if len(row)!=5 or row[0] in quiz: raise ValueError('Invalid translated quiz row')
        quiz[row[0]]={'question':row[1],'options':row[2:],'correct':0,'explanation':row[2]}
    if set(modules)!=set(m['id'] for m in spanish['modules']) or set(quiz)!=set(modules):
        raise ValueError('Missing translated module or quiz')
    if set(resources)!=set(r['id'] for r in spanish['resources']): raise ValueError('Missing translated reference')
    expected_guides={l['id'] for m in spanish['modules'] for l in m['labs'] if 'guide' in l}
    if set(guides)!=expected_guides: raise ValueError('Missing translated practical guide')
    out={**spanish,'language':'en','modules':[],'resources':[],
         'blocks':[{**b,'title':v[0],'description':v[1]} for b,v in zip(spanish['blocks'],BLOCKS_EN)]}
    def render(raw,prefix):
        data=markdown(raw,prefix=prefix)
        for key in ['html']:
            data[key]=data[key].replace('aria-label="Tabla desplazable"','aria-label="Scrollable table"')
        for sl in data['slides']:
            sl['html']=sl['html'].replace('aria-label="Tabla desplazable"','aria-label="Scrollable table"')
        return data
    for original in spanish['modules']:
        mid=original['id'];raw=modules[mid]
        matches=list(re.finditer(r'^\*\*(L\d{2}[ABC]) · (.*?)\*\*',raw,re.M))
        if [m[1] for m in matches]!=[l['id'] for l in original['labs']]: raise ValueError('Translated lab mismatch: '+mid)
        labs=[];theory=raw
        # Labs are self-contained paragraphs. Preserve the concluding theory/rubric.
        for match,base in zip(matches,original['labs']):
            end=raw.find('\n\n',match.end());end=len(raw) if end<0 else end
            body=raw[match.end():end].strip();fields={}
            names={'environment':'Environment','tasks':'Tasks','evidence':'Evidence','success':'Success','recovery':'Recovery'}
            for field,name in names.items():
                hit=re.search(r'\b'+name+r':\s*(.*?)(?=\b(?:Environment|Tasks|Evidence|Success|Recovery):|$)',body,re.S)
                if not hit: raise ValueError('Missing '+field+' in '+match[1])
                fields[field]=hit[1].strip()
            lab={k:v for k,v in base.items() if k not in ('html','guide','title')}
            lab.update(fields);lab.update(id=match[1],title=match[2].rstrip('.'),html=render(body,match[1])['html'])
            if match[1] in guides:lab['guide']={'title':guides[match[1]].splitlines()[0].split(' · ',1)[1],**render(guides[match[1]],match[1]+'-guide')}
            labs.append(lab)
            theory=theory.replace(raw[match.start():end],'')
        theory=re.sub(r'^## Laboratories\s*$','',theory,flags=re.M).strip()
        theory='\n'.join(theory.splitlines()[1:]).strip()
        rendered=render(theory,mid)
        question=dict(quiz[mid]); position=original['quiz']['correct']
        options=list(question['options']); answer=options.pop(0);options.insert(position,answer)
        question.update(options=options,correct=position)
        out['modules'].append({**original,'title':raw.splitlines()[0].split(' · ',1)[1],
            'labs':labs,'quiz':question,**rendered,'search':html.unescape(re.sub('<[^>]+>',' ',rendered['html']))})
    for original in spanish['resources']:
        raw=resources[original['id']]
        out['resources'].append({**original,'title':raw.splitlines()[0].split(' · ',1)[1],
            'kind':'Extended lesson' if original['kind']=='Lección ampliada' else 'Reference',**render(raw,original['id'])})
    return out
