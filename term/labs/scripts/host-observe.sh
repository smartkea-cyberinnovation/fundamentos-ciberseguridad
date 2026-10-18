#!/usr/bin/env bash
set -Eeuo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
while :; do
  printf '\033[2J\033[HSmartKEA · VM dedicada · observacion propia\n'
  "$script_dir/diagnose.sh"
  printf '\nVista de estado; no muestra la sesion de otra persona. Actualizacion: 10 s.\n'
  sleep 10
done
