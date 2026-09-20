#!/usr/bin/env python3
"""Deriva y valida 240 sesiones y 96 laboratorios; no asigna fechas reales."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

CATALOG = Path(__file__).with_name('curriculo.json')
# Minutos de teoria, minutos de practica y reparto entre laboratorios.
NORMAL = [(90, 30, {'A': 30}), (60, 60, {'A': 60}), (30, 90, {'A': 90}),
          (60, 60, {'B': 60}), (30, 90, {'B': 90}),
          (30, 90, {'B': 30, 'C': 60}), (0, 120, {'C': 120})]


def build(modules: list) -> dict:
    if not isinstance(modules, list) or len(modules) != 32:
        raise ValueError('Se requieren 32 modulos')
    sessions, labs, seen = [], [], set()
    for number, item in enumerate(modules, 1):
        code = f'M{number:02d}'
        if set(item) != {'id', 'titulo', 'prerrequisitos'} or item['id'] != code:
            raise ValueError('Identificador o esquema de modulo incorrecto')
        if not isinstance(item['titulo'], str) or not item['titulo'].strip():
            raise ValueError('Titulo ausente')
        prerequisites = item['prerrequisitos']
        if not isinstance(prerequisites, list) or any(not isinstance(p, str) or p not in seen for p in prerequisites):
            raise ValueError('Prerrequisito no disponible: ' + code)
        if len(prerequisites) != len(set(prerequisites)):
            raise ValueError('Prerrequisito duplicado')
        seen.add(code)
        if number <= 30:
            pattern, lab_minutes = NORMAL, 180
        else:
            theory_sessions, per_lab = (4, 2) if number == 31 else (5, 5)
            pattern = [(120, 0, {})] * theory_sessions
            pattern += [(0, 120, {letter: 120}) for letter in 'ABC' for _ in range(per_lab)]
            lab_minutes = per_lab * 120
        allocated = {letter: 0 for letter in 'ABC'}
        for theory, practical, portions in pattern:
            if theory + practical != 120 or sum(portions.values()) != practical:
                raise ValueError('Sesion incoherente')
            allocations = []
            for letter, minutes in portions.items():
                allocated[letter] += minutes
                allocations.append({'id': f'L{number:02d}{letter}', 'minutos': minutes})
            sessions.append({'id': f'S{len(sessions) + 1:03d}', 'modulo': code,
                             'teoria_min': theory, 'practica_min': practical,
                             'laboratorios': allocations})
        for letter in 'ABC':
            if allocated[letter] != lab_minutes:
                raise ValueError('Reparto de laboratorio incoherente')
            labs.append({'id': f'L{number:02d}{letter}', 'modulo': code, 'minutos': lab_minutes,
                         'estado_ejecucion': 'sin_acreditacion_por_este_generador'})
    theory = sum(s['teoria_min'] for s in sessions)
    practical = sum(s['practica_min'] for s in sessions)
    if (len(sessions), len(labs), theory, practical) != (240, 96, 10080, 18720):
        raise ValueError('Totales curriculares incorrectos')
    return {'edicion': '1.1', 'sesiones': sessions, 'laboratorios': labs,
            'resumen': {'sesiones': len(sessions), 'laboratorios': len(labs),
                        'teoria_h': theory // 60, 'practica_h': practical // 60,
                        'total_h': (theory + practical) // 60}}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Mostrar solo resumen validado')
    args = parser.parse_args(argv)
    try:
        modules = json.loads(CATALOG.read_text(encoding='utf-8'))
        result = build(modules)
        print(json.dumps(result['resumen'] if args.check else result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
