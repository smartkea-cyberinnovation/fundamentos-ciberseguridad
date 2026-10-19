#!/usr/bin/env python3
"""Offline teaching helper: bounded byte hashing and synthetic event timelines.

Never executes PHP, shell commands or input content. Never opens a network socket.
A generated manifest is a local integrity baseline, not authenticated provenance.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 20 * 1024 * 1024
MAX_FILES = 256
MAX_EVENTS = 10000
MANIFEST_SCHEMA = 'smartkea.teaching-manifest/1'
SCENARIO_SCHEMA = 'smartkea.c99-dfir/1'


def read_regular(path: Path) -> bytes:
    """Read only a bounded regular file; do not interpret its contents.

    This tool runs without elevated privileges on a stable work copy. It is not
    an acquisition agent for a concurrently hostile filesystem.
    """
    if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f'Expected a regular, non-symlink file: {path.name}')
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError('Input exceeds the per-file limit')
    with path.open('rb') as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError('Input grew beyond the per-file limit')
    return data


def load_json(path: Path) -> dict:
    value = json.loads(read_regular(path).decode('utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    return value


def manifest(directory: Path) -> dict:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('Evidence root must be a regular directory')
    rows = []
    total = 0
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinks are outside this teaching tool scope')
        if path.is_dir():
            continue
        if len(rows) >= MAX_FILES:
            raise ValueError('Too many evidence files')
        data = read_regular(path)
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise ValueError('Evidence exceeds the total size limit')
        rows.append({'path': path.relative_to(directory).as_posix(),
                     'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    if not rows:
        raise ValueError('Evidence directory is empty')
    return {'schema': MANIFEST_SCHEMA, 'file_count': len(rows), 'files': rows,
            'scope': 'Local content integrity only; not a signature or a malware verdict.'}


def verify(directory: Path, expected: dict) -> dict:
    if expected.get('schema') != MANIFEST_SCHEMA:
        raise ValueError('Unsupported manifest schema')
    entries = expected.get('files')
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_FILES:
        raise ValueError('Invalid manifest entries')
    wanted = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid manifest entry')
        name, digest, size = entry.get('path'), entry.get('sha256'), entry.get('bytes')
        if not isinstance(name, str) or not name or '\\' in name:
            raise ValueError('Invalid relative evidence path')
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or relative.as_posix() != name:
            raise ValueError('Non-canonical or unsafe evidence path')
        if name in wanted:
            raise ValueError('Duplicate manifest path')
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Invalid SHA-256')
        if type(size) is not int or not 0 <= size <= MAX_FILE_BYTES:
            raise ValueError('Invalid recorded size')
        wanted[name] = {'path': name, 'bytes': size, 'sha256': digest}
    if expected.get('file_count') != len(wanted):
        raise ValueError('Manifest file_count does not match its entries')
    actual = {item['path']: item for item in manifest(directory)['files']}
    missing = sorted(set(wanted) - set(actual))
    extra = sorted(set(actual) - set(wanted))
    changed = sorted(name for name in wanted.keys() & actual.keys() if wanted[name] != actual[name])
    return {'verified': not (missing or extra or changed), 'missing': missing,
            'extra': extra, 'changed': changed,
            'scope': 'Compared with the supplied baseline; baseline authenticity is not established.'}


def parse_time(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', value
    ):
        raise ValueError('Timestamp requires an explicit ISO-8601 time zone')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.utcoffset() is None:
        raise ValueError('Naive timestamps are not accepted')
    return parsed.astimezone(timezone.utc)


def timeline(data: dict) -> dict:
    if data.get('schema') != SCENARIO_SCHEMA or data.get('synthetic') is not True:
        raise ValueError('This command only accepts the explicitly synthetic teaching schema')
    events = data.get('events')
    if not isinstance(events, list) or not 1 <= len(events) <= MAX_EVENTS:
        raise ValueError('Invalid or oversized event list')
    ids = set()
    ordered = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError('Every event must be a JSON object')
        eid = event.get('id')
        if not isinstance(eid, str) or not re.fullmatch(r'[A-Z][A-Z0-9_-]{1,63}', eid) or eid in ids:
            raise ValueError('Event IDs must be unique and well formed')
        ids.add(eid)
        for field in ('source', 'host', 'kind'):
            if not isinstance(event.get(field), str) or not 1 <= len(event[field]) <= 150:
                raise ValueError(f'Invalid event field: {field}')
        if not isinstance(event.get('details'), dict):
            raise ValueError('Event details must be an object')
        stamp = parse_time(event.get('time'))
        row = {key: event[key] for key in ('id', 'source', 'host', 'kind', 'details')}
        row.update({'time_original': event['time'], 'time_utc': stamp.isoformat().replace('+00:00', 'Z')})
        ordered.append((stamp, eid, row))
    ordered.sort(key=lambda entry: (entry[0], entry[1]))
    groups = defaultdict(list)
    for _, eid, row in ordered:
        groups[row['time_utc']].append(eid)
    return {'schema': 'smartkea.c99-timeline/1', 'synthetic': True,
            'case_id': data.get('case_id'), 'event_count': len(ordered),
            'clock': data.get('clock'), 'scope': data.get('scope'),
            'ordering_note': 'UTC then event ID; equal timestamps do not prove causal order.',
            'equal_timestamps': {stamp: group for stamp, group in groups.items() if len(group) > 1},
            'events': [entry[2] for entry in ordered]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('manifest', help='Hash a small evidence directory without changing it')
    make.add_argument('directory', type=Path)
    check = commands.add_parser('verify', help='Compare bytes against a previously saved baseline')
    check.add_argument('directory', type=Path)
    check.add_argument('baseline', type=Path)
    order = commands.add_parser('timeline', help='Normalize and order synthetic events')
    order.add_argument('scenario', type=Path)
    args = parser.parse_args(argv)
    try:
        status = 0
        if args.command == 'manifest':
            result = manifest(args.directory)
        elif args.command == 'verify':
            result = verify(args.directory, load_json(args.baseline))
            status = 0 if result['verified'] else 1
        else:
            raw = read_regular(args.scenario)
            data = json.loads(raw.decode('utf-8'))
            if not isinstance(data, dict):
                raise ValueError('Expected a JSON object')
            result = timeline(data)
            result['input_sha256'] = hashlib.sha256(raw).hexdigest()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return status
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
