"""Evidence-first routes, independent from the canonical 480-hour course totals."""
from __future__ import annotations
from pathlib import Path
import json,html,re,shutil
from urllib.parse import urlsplit
E=lambda x:html.escape(str(x),quote=True)
ROOT=Path(__file__).resolve().parent.parent

def prerequisites(module_ids:list[str],modules:list[dict])->list[str]:
    catalog={m['id']:m for m in modules}; visited=set(); visiting=set()
    def visit(mid):
        if mid in visiting:raise ValueError('Cyclic module prerequisites')
        if mid not in catalog:raise ValueError('Unknown module '+mid)
        if mid in visited:return
        visiting.add(mid)
        for child in catalog[mid]['prerequisites']:visit(child)
        visiting.remove(mid);visited.add(mid)
    for mid in module_ids:visit(mid)
    return sorted(visited-set(module_ids))

def collect_paths(root:Path=ROOT)->tuple[dict,dict,dict]:
    routes=json.loads((root/'formacion/rutas/routes.json').read_text('utf-8'))
    certs=json.loads((root/'formacion/rutas/credentials.json').read_text('utf-8'))
    sources=json.loads((root/'formacion/rutas/sources.json').read_text('utf-8'))
    return routes,certs,sources

def validate_paths(routes,certs,sources,modules)->dict:
    if routes.get('schema')!=1 or len(routes['routes'])!=6:raise ValueError('Expected six versioned learning paths')
    source_ids={s['id'] for s in sources['sources']};cert_ids={c['id'] for c in certs['certifications']}
    route_ids=set();stage_ids=set()
    for s in [*sources['sources'],*certs['certifications']]:
        u=urlsplit(s['url'])
        if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Unsafe source URL')
    for r in routes['routes']:
        if not re.fullmatch('[a-z-]+',r['id']) or r['id'] in route_ids:raise ValueError('Invalid route ID')
        route_ids.add(r['id'])
        if not set(r['certifications'])<=cert_ids:raise ValueError('Unknown credential')
        if r['weeks']!=sum(p['weeks'] for p in r['phases']) or r['estimated_hours']!=sum(p['estimated_hours'] for p in r['phases']):raise ValueError('Wrong route totals')
        for p in r['phases']:
            if p['id'] in stage_ids or not p['id'].startswith(r['id']+'-'):raise ValueError('Duplicate/wrong phase')
            stage_ids.add(p['id'])
            if min(p['weeks'],p['hours_per_week'])<=0 or p['estimated_hours']!=p['weeks']*p['hours_per_week']:raise ValueError('Wrong phase hours')
            if not set(p['source_refs'])<=source_ids or not p['evidence'].strip():raise ValueError('Missing source/evidence')
            prerequisites(p['module_refs'],modules)
    return {'routes':len(route_ids),'phases':len(stage_ids),'credentials':len(cert_ids),'sources':len(source_ids)}

def render(stage:Path,data:dict,root:Path=ROOT)->dict:
    routes,certs,sources=collect_paths(root);report=validate_paths(routes,certs,sources,data['modules'])
    source_by={x['id']:x for x in sources['sources']};cert_by={x['id']:x for x in certs['certifications']}
    def source_link(sid):
        s=source_by[sid];return f'<a href="{E(s["url"])}" rel="noreferrer noopener">{E(s["title"])}</a>'
    def module_links(ids):return ' · '.join(f'<a href="./?lang=es#/modulo/{E(mid)}">{E(mid)}</a>' for mid in ids)
    cards=''.join(f'<button type="button" data-route-select="{E(r["id"])}"><strong>{E(r["name"])}</strong><span class="small">{r["weeks"]} semanas · {r["estimated_hours"]} h orientativas</span></button>' for r in routes['routes'])
    sections=''
    for r in routes['routes']:
        body=''
        for i,p in enumerate(r['phases'],1):
            mods=p['module_refs'];before=prerequisites(mods,data['modules'])
            dep=(f'<details><summary>Prerrequisitos de los módulos enlazados ({len(before)})</summary><p>{module_links(before) or "Sin dependencias previas adicionales."}</p><p class="small">Antes de completar un módulo o laboratorio, cubre sus dependencias. Consultar un extracto no equivale a completar sus horas. El tiempo adicional depende de tu nivel.</p></details>' if mods else '')
            body+=f'<section class="stage"><span class="tag">Etapa {i} · {p["weeks"]} semanas × {p["hours_per_week"]} h</span><h3>{E(p["title"])}</h3><p>{E(p["work"])}</p><p><strong>Evidencia de salida:</strong> {E(p["evidence"])}</p><p class="small">Módulos para consultar: {module_links(mods) or "Actividad jurídica, de negocio o de gobierno; sin terminal obligatoria."}</p>{dep}<details><summary>Fuentes oficiales para esta etapa</summary><p>{"<br>".join(source_link(sid) for sid in p["source_refs"])}</p></details><label><input type="checkbox" data-phase="{E(p["id"])}"> He producido y revisado la evidencia de esta etapa</label></section>'
        credential_html=''
        for cid in r['certifications']:
            c=cert_by[cid]
            credential_html+=f'<p><a href="{E(c["url"])}" rel="noreferrer noopener">{E(c["name"])}</a> · Programa y condiciones oficiales.</p>'
        sections+=f'<section class="route" id="ruta-{E(r["id"])}" data-route="{E(r["id"])}"><div class="route-head"><div><span class="tag">Ruta profesional · {r["weeks"]} semanas / {r["estimated_hours"]} h estimadas</span><h2>{E(r["name"])}</h2></div><p class="progress" data-progress="{E(r["id"])}">0 de {len(r["phases"])} etapas revisadas</p></div><p><strong>Entrada:</strong> {E(r["entry"])}</p><p><strong>Objetivo:</strong> {E(r["outcome"])}</p><div class="stages">{body}</div><h3>Especialización opcional: no hay que obtenerlas todas</h3>{credential_html}</section>'
    page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="Itinerarios de estudio por perfil: DPD, legal, no técnico, soporte, ingeniería y ciberseguridad. SmartKEA."><title>Rutas profesionales · SmartKEA</title><link rel="stylesheet" href="assets/routes.css"><script type="module" src="assets/routes.js"></script></head><body><a class="skip" href="#main">Saltar al contenido</a><header class="top"><a class="brand" href="./">SmartKEA <span class="small">/ Rutas profesionales</span></a><div class="row"><a href="./?lang=es#/temario">Campus ES/EN</a><a href="https://github.com/WiktorNykiel/fundamentos-ciberseguridad/tree/main/awesome-dpd">Awesome DPD · edición original</a><a href="examen/">Ensayar 20 preguntas</a><button id="print-paths" type="button">Imprimir</button></div></header><div class="present-controls"><button id="previous-route" type="button">Anterior</button><span id="slide-count" role="status"></span><button id="next-route" type="button">Siguiente</button><button id="exit-presentation" type="button">Salir de presentación</button></div><main id="main"><section class="hero"><div><span class="tag">Privacidad · Tecnología · Ciberseguridad</span><h1>Elige tu función.<br>Construye tu recorrido.</h1><p>No todas las personas necesitan la misma terminal, el mismo temario o el mismo examen. Empieza desde tus tareas y termina con evidencias que puedas explicar.</p><p class="small">Orientación nueva en español · Campus troncal en español e inglés · Revisión 18 septiembre 2026</p></div><aside class="panel"><div class="stats"><div><div class="stat">6</div><small>perfiles</small></div><div><div class="stat">13</div><small>credenciales opcionales</small></div><div><div class="stat">32</div><small>módulos de referencia</small></div></div><div class="notice">Las rutas no son titulaciones. Sus horas no se suman a las 480 h del currículo ni acreditan formación reconocida para AEPD-DPD.</div><button id="start-presentation" type="button">Presentar las rutas</button><p class="screen-help">Presentación: flechas para navegar, Escape para salir. El contenido largo se desplaza.</p></aside></section><section class="grid route-cards">'''+cards+'''</section><section class="intro"><div class="notice"><strong>Cómo leer el itinerario.</strong> Los módulos enlazados son referencias de estudio, no promesas de completarlos en las horas de la ruta. Sus prerrequisitos y horas originales siguen vigentes. La ruta DPD puede empezar desde derecho o desde tecnología: añade el puente que necesites.</div><p><strong>Método propuesto:</strong> pregunta → fuente primaria → actividad ficticia → evidencia revisable → explicación para dirección y especialistas. Una casilla marcada es autoevaluación, no prueba de competencia ni certificado.</p></section><div class="filters"><label>Mostrar perfil<select id="route-filter"><option value="all">Todos los perfiles</option>'''+''.join(f'<option value="{E(r["id"])}">{E(r["name"])}</option>' for r in routes['routes'])+'''</select></label><label><span>Progreso opcional</span><span><input type="checkbox" id="remember-paths"> Guardar avances en este navegador</span></label><button type="button" id="clear-paths">Borrar estas marcas</button><p class="small" id="path-status" role="status" aria-live="polite">Sin guardar: las marcas duran solo esta visita. No se modifican las notas del campus.</p></div>'''+sections+'''<section class="intro notice"><strong>Decidir con criterio.</strong> AEPD-DPD es voluntaria; autoestudio no es formación reconocida. Los requisitos de certificación, costes y calendarios cambian: contrasta la fuente oficial antes de contratar. El DPD asesora y supervisa; no sustituye al responsable. Las correspondencias de competencias son editoriales, no acreditación ENISA ni datos de demanda laboral.</section></main><footer>SmartKEA · Solo casos ficticios · Progreso opcional en este navegador · <a href="https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/CERTIFICACIONES.md">Guía de certificaciones</a> · <a href="https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/ITINERARIO.md">Itinerario DPD</a> · <a href="https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/main/awesome-dpd/AVISO-LICENCIA.md">Licencias pendientes de decisión</a></footer></body></html>'''
    (stage/'rutas.html').write_text(page,'utf-8')
    shutil.copyfile(root/'campus/assets/routes.css',stage/'assets/routes.css')
    shutil.copyfile(root/'campus/assets/routes.js',stage/'assets/routes.js')
    return report
