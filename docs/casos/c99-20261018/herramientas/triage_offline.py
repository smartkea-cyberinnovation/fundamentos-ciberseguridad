#!/usr/bin/env python3
"""Triage local de PHP como bytes: no ejecuta PHP, no usa red ni reconstruye una shell.
La decodificación sólo interpreta escapes de literales, nunca expresiones PHP.
Lexer reducido: no soporta heredoc/nowdoc; informa de esta limitación.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterator

MAX_BYTES = 5 * 1024 * 1024
CALLBACK = 'svgflow.digital/sz/log.php'
KNOWN_SHA256 = {
 '1e07598c2e41b7827840ba6c8611912abd88c0344a5d1eff364eaabeccdc6420': 'PHP sin salto final / blob público',
 '2e89c9c01290c9b2d6979d778fed1868d43aacaad1bd9df1dcc60bf11542b338': 'PHP con LF final normalizado',
 'a00b96a2721884c6bc4b7dcca69cde6d4d2d8ea464aef193b684e00a6dd6be4d': 'Adjunto Markdown de referencia',
}

def decode_literal(literal: str) -> str:
    """Decodifica únicamente un literal PHP entre comillas simples o dobles."""
    if len(literal) < 2 or literal[0] not in "\"'" or literal[-1] != literal[0]:
        raise ValueError('Se requiere un literal delimitado por comillas coincidentes')
    body = literal[1:-1]
    if literal[0] == "'":
        return re.sub(r"\\([\\'])", lambda m: m[1], body)
    escapes = {'n':'\n', 'r':'\r', 't':'\t', 'v':'\v', 'e':'\x1b', 'f':'\f', '\\':'\\', '"':'"', '$':'$'}
    def convert(match: re.Match[str]) -> str:
        part = match[1]
        if part.startswith('x'):
            return chr(int(part[1:], 16))
        if part[0] in '01234567':
            return chr(int(part, 8) & 255)
        return escapes[part]
    return re.sub(r'\\(x[0-9a-fA-F]{1,2}|[0-7]{1,3}|[nrtvef\\"$])', convert, body)

def literals(source: str, warnings: list[dict] | None = None) -> Iterator[tuple[int, str]]:
    """Lee literales completos sólo en bloques PHP estándar o de echo corto.

    No interpreta expresiones, no ejecuta PHP y no es un parser completo.
    CR/LF y ?> terminan comentarios de línea. El HTML externo se ignora.
    Una cadena truncada se registra y no elimina hashes o hallazgos anteriores.
    """
    warnings = [] if warnings is None else warnings
    opening = re.compile(r"<\?(?:php(?=[ \t\r\n]|$)|=)", re.IGNORECASE)
    i, length, in_php = 0, len(source), False
    while i < length:
        if not in_php:
            match = opening.search(source, i)
            if match is None:
                return
            i, in_php = match.end(), True
            continue
        if source.startswith('?>', i):
            i, in_php = i + 2, False
        elif source.startswith('//', i) or (source[i] == '#' and not source.startswith('#[', i)):
            ends = [pos for marker in ('\r', '\n', '?>')
                    if (pos := source.find(marker, i + 1)) >= 0]
            if not ends:
                return
            end = min(ends)
            if source.startswith('?>', end):
                i, in_php = end + 2, False
            else:
                i = end + 1
        elif source.startswith('/*', i):
            end = source.find('*/', i + 2)
            if end < 0:
                warnings.append({'offset': i, 'kind': 'unterminated_block_comment'})
                return
            i = end + 2
        elif source.startswith('<<<', i):
            warnings.append({'offset': i, 'kind': 'unsupported_heredoc_or_nowdoc',
                             'effect': 'El escaneo se detiene; se conservan hallazgos previos.'})
            return
        elif source[i] in "\"'`":
            start, quote, closed = i, source[i], False
            i += 1
            while i < length:
                if source[i] == '\\':
                    i += 2
                elif source[i] == quote:
                    i += 1
                    closed = True
                    break
                else:
                    i += 1
            if not closed:
                warnings.append({'offset': start, 'kind': 'unterminated_quoted_literal',
                                 'delimiter': quote})
                return
            if quote != '`':
                yield start, source[start:i]
        else:
            i += 1

def defang(value: str) -> str:
    return value.replace('https://', 'hxxps://').replace('http://', 'hxxp://').replace('.', '[.]').replace('@', '[@]')

def analyze_bytes(raw: bytes) -> dict:
    if len(raw) > MAX_BYTES:
        raise ValueError(f'Límite de análisis: {MAX_BYTES} bytes')
    text = raw.decode('latin1')
    digest = hashlib.sha256(raw).hexdigest()
    hits, count, encoded = [], 0, 0
    lexer_warnings: list[dict] = []
    for offset, token in literals(text, lexer_warnings):
        count += 1
        value = decode_literal(token)
        encoded += int(bool(re.search(r'\\(?:x[0-9a-fA-F]|[0-7])', token)))
        if CALLBACK in value:
            hits.append({'offset': offset, 'value': defang(value), 'kind': 'callback_literal',
                         'meaning': 'Cadena presente; no demuestra que se ejecute ni que se haya enviado'})
        elif value in ('c99shcook', 'c99shvars', 'irc.dalnet.ru:6667', 'user@host.tld'):
            hits.append({'offset': offset, 'value': defang(value), 'kind': 'context_marker'})
    return {'schema':'c99.triage/1', 'bytes':len(raw), 'sha256':digest,
            'git_blob_sha1':hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(),
            'known_sample':KNOWN_SHA256.get(digest), 'literal_count_reduced_lexer':count,
            'encoded_literal_count':encoded, 'hits':hits, 'sample_executed':False,
            'network_requests':0, 'limits':['No AST, CFG, evaluación de variables ni prueba de explotación.',
                'Heredoc/nowdoc e interpolación compleja requieren tokenizador PHP independiente.',
                'Un comentario o un informe que cite IOC no acredita malware activo.'],
            'unsupported_heredoc_candidate': '<<<' in text,
            'lexer_warnings': lexer_warnings,
            'php_tag_policy': 'standard-and-short-echo; short_open_tag no soportado'}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=Path)
    parser.add_argument('--out', type=Path, help='JSON nuevo; no sobrescribe ficheros existentes')
    args = parser.parse_args()
    try:
        if args.sample.is_symlink() or not args.sample.is_file():
            raise ValueError('La entrada debe ser un fichero regular, no un enlace simbólico')
        if args.sample.stat().st_size > MAX_BYTES:
            raise ValueError('Fichero demasiado grande')
        with args.sample.open('rb') as f:
            raw = f.read(MAX_BYTES + 1)
        result = json.dumps(analyze_bytes(raw), ensure_ascii=False, indent=2) + '\n'
        if args.out:
            if args.out.resolve() == args.sample.resolve():
                raise ValueError('La salida no puede ser la evidencia de entrada')
            with args.out.open('x', encoding='utf-8') as f:
                f.write(result)
        else:
            print(result, end='')
        return 0
    except (OSError, ValueError) as e:
        print(f'Error: {e}', file=sys.stderr); return 2

if __name__ == '__main__':
    raise SystemExit(main())
