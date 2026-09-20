#!/usr/bin/env python3
"""Comprueba hashes del kit y enlaces relativos; no ejecuta los laboratorios."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Inventario JSON de rutas ya verificadas en Git para revision de un delta')
    args = parser.parse_args()
    baseline = set(json.loads(args.baseline.read_text(encoding='utf-8'))) if args.baseline else set()
    manifest = json.loads((ROOT / 'qa' / 'integridad.json').read_text(encoding='utf-8'))
    errors, checked = [], 0
    for row in manifest:
        path = (ROOT / row['path']).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append('Archivo ausente o fuera de alcance: ' + row['path'])
        else:
            data = path.read_bytes()
            if path.suffix == '.cmd':
                data = data.replace(b'\r\n', b'\n')
            if hashlib.sha256(data).hexdigest() != row['sha256']:
                errors.append('Hash diferente: ' + row['path'])
    for doc in sorted(ROOT.rglob('*.md')):
        text = re.sub(r'```.*?```', '', doc.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            part = urlsplit(target)
            if part.scheme or target.startswith('#'):
                continue
            candidate = (doc.parent / unquote(part.path)).resolve()
            if not candidate.is_relative_to(ROOT):
                errors.append('Enlace fuera del curso: ' + target)
                continue
            relative = candidate.relative_to(ROOT).as_posix()
            checked += 1
            if not candidate.exists() and relative not in baseline:
                errors.append(doc.relative_to(ROOT).as_posix() + ': falta ' + target)
    print(json.dumps({'hashes': len(manifest), 'enlaces_relativos': checked,
                      'baseline_externo': bool(baseline), 'errores': errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
