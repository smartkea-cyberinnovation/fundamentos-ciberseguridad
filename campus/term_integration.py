"""Integrate the independent TERM release without changing campus content bytes."""
import importlib.util
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
TERM = HERE.parent / 'term'
TERM_BASE = '/fundamentos-ciberseguridad/term/'
TERM_PREFIX = TERM_BASE.strip('/')
spec = importlib.util.spec_from_file_location('smartkea_term_builder', TERM/'build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def build_term():
    return builder.build()


def term_404():
    return builder.shell_document('No se encontró esta página', '<p>Abre el itinerario y selecciona una lección.</p>', base=TERM_BASE)


def merged_headers(campus_headers: str, campus_base: str) -> str:
    # Scope the original policy instead of stacking two CSP values on TERM.
    if not campus_headers.startswith('/*\n'):
        raise ValueError('Unexpected campus headers; cannot scope the policy safely.')
    original = campus_base+'*\n'+campus_headers.split('\n',1)[1]
    term_headers = (TERM/'dist/_headers').read_text()
    if not term_headers.startswith('/*\n'):
        raise ValueError('Unexpected TERM headers.')
    return original+'\n'+TERM_BASE+'*\n'+term_headers.split('\n',1)[1]


def redirects():
    return f'{TERM_BASE.rstrip("/")} {TERM_BASE} 308\n'


def copy_term(output: Path):
    builder.validate(TERM/'dist')
    target=output/TERM_PREFIX
    target.mkdir(parents=True)
    for name,path in builder.public_files(TERM/'dist').items():
        if name=='_headers':continue
        (target/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target/name)
    (target/'404.html').write_text(term_404())
    (output/'_redirects').write_text(redirects())
    return target


def expected_files():
    builder.validate(TERM/'dist')
    return {TERM_PREFIX+'/'+n for n in builder.public_files(TERM/'dist') if n!='_headers'}|{'_redirects'}


def validate_term(output: Path):
    report=builder.validate(TERM/'dist')
    target=output/TERM_PREFIX
    for name,path in builder.public_files(TERM/'dist').items():
        if name in ('_headers','SHA256SUMS.txt'):continue
        expected=term_404().encode() if name=='404.html' else path.read_bytes()
        if (target/name).read_bytes()!=expected:
            raise ValueError('TERM public bytes changed in staging: '+name)
    if (output/'_redirects').read_text()!=redirects():
        raise ValueError('TERM entry redirect drifted.')
    return report
