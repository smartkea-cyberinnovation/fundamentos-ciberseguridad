#!/usr/bin/env bash
# Host mode is ONLY for a dedicated disposable student VM. See CONEXION-TTYD.md.
set -Eeuo pipefail
umask 077
if [[ $(id -u) -eq 0 ]]; then printf 'Run this terminal as the student, never as root.\n' >&2; exit 77; fi
if (( $# > 1 )); then printf 'Usage: ttyd-host-start.sh [--read-only|--writable|--observe]\n' >&2; exit 64; fi
mode=${1:---read-only}
case "$mode" in --read-only|--writable|--observe) ;; *) printf 'Unsupported mode.\n' >&2; exit 64 ;; esac
command -v ttyd >/dev/null 2>&1 || { printf 'Install a supported ttyd version first.\n' >&2; exit 69; }
help_text=$(ttyd --help)
if [[ "$help_text" != *'--writable'* || "$help_text" != *'--check-origin'* ]]; then
  printf 'This launcher requires ttyd --writable and --check-origin.\n' >&2; exit 78
fi
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
work_dir=${HOME:?}/term-workspace
mkdir -p -m 0700 -- "$work_dir"
port=7681
if [[ "$mode" == --observe ]]; then port=7682; fi
args=(--interface 127.0.0.1 --port "$port" --check-origin --max-clients 1 --cwd "$work_dir"
      --client-option 'fontSize=16'
      --client-option 'theme={"background":"#ffffff","foreground":"#17233b","cursor":"#174ac5"}')
if [[ "$mode" == --read-only ]]; then
  exec ttyd "${args[@]}" "$script_dir/host-observe.sh"
fi
command -v tmux >/dev/null 2>&1 || { printf 'tmux is required for this mode.\n' >&2; exit 69; }
if [[ "$mode" == --observe ]]; then
  exec ttyd "${args[@]}" tmux attach-session -r -t smartkea-lab
fi
# Intentional per-student shared tmux session, confined to that student's VM.
# Do not enable no_new_privs here: privileged host exercises explicitly use sudo.
exec ttyd "${args[@]}" --writable tmux new-session -A -s smartkea-lab
