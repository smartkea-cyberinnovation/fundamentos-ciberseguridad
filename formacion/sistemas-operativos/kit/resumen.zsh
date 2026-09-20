#!/usr/bin/env zsh
# Ejemplo nativo zsh; no es un wrapper de Bash. Validacion nativa pendiente.
emulate -L zsh
setopt ERR_EXIT NO_UNSET PIPE_FAIL EXTENDED_GLOB
if (( $# != 1 )); then print -u2 'Uso: zsh resumen.zsh WORKSPACE'; exit 2; fi
[[ ! -L "$1" ]] || exit 2
cd -- "$1" || exit 2
[[ -f .oslab && ! -L .oslab && -d datos && ! -L datos ]] || exit 2
IFS= read -r marker < .oslab
[[ "$marker" == OSLAB-SYNTHETIC-1 ]] || exit 2
integer count=0 bytes=0
# D incluye ocultos; N produce una lista vacia si no hay coincidencias.
for file in datos/*(DN); do
    [[ -f "$file" && ! -L "$file" ]] || exit 2
    size=$(LC_ALL=C wc -c < "$file") || exit 2
    [[ "$size" == [[:space:]]#<->[[:space:]]# ]] || exit 2
    count=$((count + 1)); bytes=$((bytes + size))
done
printf '{"count":%d,"total_bytes":%d}\n' "$count" "$bytes"
