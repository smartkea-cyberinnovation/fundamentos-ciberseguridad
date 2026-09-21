"""Explicit, append-only operational readings; no changes to hours or progress IDs."""
from urllib.parse import quote

READINGS = (
    ('D22', '01-identidad-bastionado.md', 'Identidades y bastionado', 'Identity and hardening'),
    ('D23', '02-redes-recursos.md', 'Redes y recursos compartidos', 'Networks and shared resources'),
    ('D24', '03-navegacion-tls.md', 'Navegación, cuentas y TLS', 'Browsing, accounts and TLS'),
    ('D25', '04-deteccion-laboratorios.md', 'Detección y aceptación', 'Detection and acceptance'),
)
RELATED = {
    'M07': ('D22','D23'), 'M08': ('D22','D25'), 'M09': ('D23',),
    'M10': ('D23','D24'), 'M17': ('D22','D23'), 'M18': ('D22','D23','D24'),
    'M19': ('D22','D25'), 'M21': ('D22',), 'M22': ('D22','D23','D24'),
    'M23': ('D22','D25'), 'M24': ('D23','D24'), 'M25': ('D24',),
    'M27': ('D25',), 'M28': ('D25',), 'M29': ('D25',),
}

def related_reading(mid: str, language: str) -> str:
    if language not in ('es','en'):
        raise ValueError('Unsupported reading language')
    if mid not in RELATED:
        return ''
    labels = {r[0]:r[2 if language == 'es' else 3] for r in READINGS}
    title = 'Ampliación: control operativo' if language == 'es' else 'Further study: operational control'
    note = ('Lecturas complementarias; no añaden horas ni nuevas marcas de progreso.' if language == 'es'
            else 'Supplementary readings; no added hours or progress milestones.')
    links = ' · '.join(f'[{rid}: {labels[rid]}](#/recurso/{rid})' for rid in RELATED[mid])
    return f'\n\n## {title}\n\n{note}\n\n{links}\n'

def add_resources(resources, course, root, repo, markdown, read_text) -> None:
    # Refuse accidental renumbering if the original catalogue changes underneath this extension.
    if [r['id'] for r in resources] != [f'D{i:02}' for i in range(1,22)]:
        raise ValueError('Review stable D01-D21 ordering before appending operational readings')
    for rid, filename, _, _ in READINGS:
        path=course/'operacion'/filename
        raw=read_text(path)
        if not raw.startswith('# '):
            raise ValueError('Operational reading requires a title: '+rid)
        source=path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
        body='\n'.join(raw.splitlines()[1:]).strip()
        resources.append({'id':rid,'title':raw.splitlines()[0][2:].strip(),'kind':'Lección ampliada',
            'source':repo+'/blob/main/'+quote(source,safe='/'), **markdown(body,source,rid)})
