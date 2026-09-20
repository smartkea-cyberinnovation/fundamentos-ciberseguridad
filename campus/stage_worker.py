#!/usr/bin/env python3
"""Stage a validated portable release at its public prefix; no network or labs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit
from check_release import validate
from publication import PUBLIC_BASE_PATH, PUBLIC_URL, not_found_page

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / 'worker-dist'
MARKER = '.campus-worker-generated'
TRANSFORMED = {'_headers', '404.html', 'build-info.json', 'SHA256SUMS.txt'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_files(directory: Path) -> dict[str, Path]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('El staging debe ser un directorio regular.')
    paths = list(directory.rglob('*'))
    if any(path.is_symlink() for path in paths):
        raise ValueError('El staging no admite enlaces simbólicos.')
    return {path.relative_to(directory).as_posix(): path for path in paths
            if path.is_file() and not any(part.startswith('.') for part in path.relative_to(directory).parts)}


def write_manifest(directory: Path) -> None:
    files = public_files(directory)
    (directory/'SHA256SUMS.txt').write_text(''.join(
        sha256(path) + '  ' + name + '\n' for name, path in sorted(files.items())
        if name != 'SHA256SUMS.txt'), encoding='utf-8')


def check_manifest(directory: Path) -> None:
    files = public_files(directory)
    expected = {}
    for line in (directory/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match or match[2] in expected or match[2] not in files:
            raise ValueError('Manifiesto de staging incorrecto.')
        expected[match[2]] = match[1]
        if sha256(files[match[2]]) != match[1]:
            raise ValueError('Hash del staging incorrecto: ' + match[2])
    if set(expected) != files.keys() - {'SHA256SUMS.txt'}:
        raise ValueError('Cobertura del manifiesto de staging incompleta.')


def validate_staging(output: Path = OUTPUT, source: Path = HERE/'dist',
                     archive: Path = HERE/'pages-ready.zip') -> dict:
    release = validate(source, archive)
    files = public_files(output)
    prefix = PUBLIC_BASE_PATH.strip('/')
    target = output / prefix
    originals = public_files(source)
    expected = {prefix+'/'+name for name in originals if name != '_headers'}
    expected |= {'_headers', 'SHA256SUMS.txt'}
    if files.keys() != expected:
        raise ValueError('El staging no conserva exactamente los activos públicos del campus.')
    for name, original in originals.items():
        if name not in TRANSFORMED and original.read_bytes() != (target/name).read_bytes():
            raise ValueError('El staging ha cambiado contenido del campus: ' + name)
    if (output/'_headers').read_bytes() != (source/'_headers').read_bytes():
        raise ValueError('Las cabeceras deben estar en la raíz del staging y conservar sus protecciones.')
    if (target/'404.html').read_text(encoding='utf-8') != not_found_page(PUBLIC_BASE_PATH):
        raise ValueError('La página 404 no está adaptada al prefijo público.')
    for url in re.findall(r'(?:href|src)="([^"]+)"', (target/'404.html').read_text(encoding='utf-8')):
        parsed = urlsplit(url)
        if not parsed.path.startswith(PUBLIC_BASE_PATH):
            raise ValueError('Un enlace 404 sale del campus.')
        if parsed.path != PUBLIC_BASE_PATH and not (output/parsed.path.lstrip('/')).is_file():
            raise ValueError('Un activo 404 no existe en el staging.')
    if (output/MARKER).read_text() != 'campus-worker-v1\n':
        raise ValueError('El staging no pertenece al generador.')
    if (output/'.assetsignore').read_text() != MARKER+'\n':
        raise ValueError('El marcador interno no está excluido de los activos.')
    info = json.loads((target/'build-info.json').read_text())
    source_info = json.loads((source/'build-info.json').read_text())
    expected_info = dict(source_info, publicBasePath=PUBLIC_BASE_PATH, publicUrl=PUBLIC_URL,
                         sourceManifestSha256=sha256(source/'SHA256SUMS.txt'))
    if info != expected_info:
        raise ValueError('La procedencia del staging no coincide con la release validada.')
    check_manifest(target)
    check_manifest(output)
    return dict(release, publicUrl=PUBLIC_URL, publicBasePath=PUBLIC_BASE_PATH,
                workerAssets=len(files), workerManifestSha256=sha256(output/'SHA256SUMS.txt'),
                sourceCommit=info['sourceCommit'])


def stage(output: Path = OUTPUT, source: Path = HERE/'dist',
          archive: Path = HERE/'pages-ready.zip') -> dict:
    validate(source, archive)
    if output.is_symlink() or (output.exists() and not (output/MARKER).is_file()):
        raise ValueError('No se puede reemplazar un staging ajeno al generador.')
    temporary = Path(tempfile.mkdtemp(prefix='.campus-worker-build-', dir=output.parent))
    try:
        target = temporary / PUBLIC_BASE_PATH.strip('/')
        target.mkdir()
        for name, path in public_files(source).items():
            if name == '_headers':
                shutil.copyfile(path, temporary/name)
            else:
                (target/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target/name)
        (target/'404.html').write_text(not_found_page(PUBLIC_BASE_PATH), encoding='utf-8')
        info = json.loads((target/'build-info.json').read_text())
        info.update(publicBasePath=PUBLIC_BASE_PATH, publicUrl=PUBLIC_URL,
                    sourceManifestSha256=sha256(source/'SHA256SUMS.txt'))
        (target/'build-info.json').write_text(json.dumps(info, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        (temporary/MARKER).write_text('campus-worker-v1\n', encoding='utf-8')
        (temporary/'.assetsignore').write_text(MARKER+'\n', encoding='utf-8')
        write_manifest(target)
        write_manifest(temporary)
        report = validate_staging(temporary, source, archive)
        if output.exists():
            shutil.rmtree(output)
        temporary.rename(output)
        return report
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


if __name__ == '__main__':
    print(json.dumps(stage(), ensure_ascii=False, indent=2))
