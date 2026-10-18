#!/usr/bin/env bash
# Fixed command contract: no URL arguments, shell interpolation, or arbitrary command.
set -Eeuo pipefail
umask 077

if [[ $(id -u) -eq 0 ]]; then
  printf 'Refusing to run a web terminal as root. Use the image UID 10001.\n' >&2
  exit 77
fi
if (( $# > 1 )); then
  printf 'Usage: ttyd-start.sh [--read-only|--writable]\n' >&2
  exit 64
fi
mode=${1:---read-only}
case "$mode" in --read-only|--writable) ;; *) printf 'Unsupported terminal mode.\n' >&2; exit 64 ;; esac

help_text=$(ttyd --help 2>&1)
if [[ "$help_text" != *'--check-origin'* || "$help_text" != *'--writable'* ]]; then
  printf 'ttyd must support --check-origin and --writable (verified upstream 1.7.7).\n' >&2
  exit 78
fi
args=(--interface 0.0.0.0 --port 7681 --check-origin --max-clients 1 --cwd /workspace
      --client-option 'fontSize=16'
      --client-option 'theme={"background":"#ffffff","foreground":"#17233b","cursor":"#174ac5"}')
if [[ "$mode" == --writable ]]; then
  exec /opt/lab/bin/exec-nnp.py /usr/local/bin/ttyd "${args[@]}" --writable /bin/bash --noprofile --rcfile /opt/lab/config/bashrc
fi
exec /opt/lab/bin/exec-nnp.py /usr/local/bin/ttyd "${args[@]}" /opt/lab/bin/observe.sh
