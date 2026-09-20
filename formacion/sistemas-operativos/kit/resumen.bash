#!/usr/bin/env bash
# Resumen nativo no recursivo. No ejecuta entradas ni altera el workspace.
set -u
set -o pipefail
if [[ $# -ne 1 ]]; then printf '%s\n' 'Uso: bash resumen.bash WORKSPACE' >&2; exit 2; fi
if [[ -L "$1" ]]; then printf '%s\n' 'No se admiten enlaces' >&2; exit 2; fi
cd -- "$1" || exit 2
if [[ ! -f .oslab || -L .oslab || ! -d datos || -L datos ]]; then exit 2; fi
IFS= read -r marker < .oslab || exit 2
if [[ "$marker" != OSLAB-SYNTHETIC-1 ]]; then exit 2; fi
shopt -s nullglob dotglob
count=0; bytes=0
for file in datos/*; do
    if [[ ! -f "$file" || -L "$file" ]]; then printf '%s\n' 'Entrada no regular' >&2; exit 2; fi
    size=$(LC_ALL=C wc -c < "$file") || exit 2
    if [[ ! "$size" =~ ^[[:space:]]*[0-9]+[[:space:]]*$ ]]; then exit 2; fi
    count=$((count + 1)); bytes=$((bytes + size))
done
printf '{"count":%d,"total_bytes":%d}\n' "$count" "$bytes"
