"""Single source of truth for the campus publication location.

The portable release stays at dist/. Workers serves the same public content
inside PUBLIC_BASE_PATH, leaving the rest of smartkea.com to its existing site.
"""
PUBLIC_ORIGIN = 'https://smartkea.com'
PUBLIC_BASE_PATH = '/introduccion-ciberseguridad/'
PUBLIC_URL = PUBLIC_ORIGIN + PUBLIC_BASE_PATH
PRODUCTION_ROUTES = [{'pattern': PUBLIC_URL.removeprefix('https://') + '*',
                      'zone_name': 'smartkea.com'}]


def not_found_page(base_path: str = '/') -> str:
    """Explicit template; never rewrite arbitrary educational HTML or code."""
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>No encontrado · Campus</title>'
            f'<link rel="stylesheet" href="{base_path}assets/styles.css"></head>'
            '<body class="print-reader"><main><h1>No se encontró ese archivo.</h1>'
            '<p>Las secciones del campus se navegan desde el índice.</p>'
            f'<a href="{base_path}?lang=es#/temario">Abrir el temario completo</a>'
            '<section lang="en"><h2>File not found.</h2>'
            '<p>Use the course index to find a lesson.</p>'
            f'<a href="{base_path}?lang=en#/temario">Open the course index</a>'
            '</section></main></body></html>')
