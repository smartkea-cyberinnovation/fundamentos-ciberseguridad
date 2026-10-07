#!/usr/bin/env bash
# Explicit local smoke run. Creates and later stops only project term-smoke-PID.
set -Eeuo pipefail
umask 077
if (( $# )); then printf 'Usage: smoke.sh\n' >&2; exit 64; fi
lab_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
project="term-smoke-$$"
command -v docker >/dev/null 2>&1 || { printf 'Docker CLI required.\n' >&2; exit 69; }
compose=(docker compose --project-name "$project" -f "$lab_dir/compose.yaml")
terminal_ids=()
cleanup() {
  for terminal_id in "${terminal_ids[@]}"; do
    docker rm --force "$terminal_id" >/dev/null 2>&1 || true
  done
  "${compose[@]}" down --volumes --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT
"${compose[@]}" config --quiet
"${compose[@]}" build web toolbox
"${compose[@]}" up --wait web
"${compose[@]}" run --rm --no-deps -T toolbox /opt/lab/bin/http-check.sh
"${compose[@]}" run --rm --no-deps -T toolbox sh -c 'test "$(id -u)" = 10001 && test ! -S /var/run/docker.sock && test ! -w /etc && test -w /workspace'
"${compose[@]}" run --rm --no-deps -T toolbox nmap -sT -Pn -sV --version-light --max-retries 1 --host-timeout 20s -p 8080 web
"${compose[@]}" run --rm --no-deps -T toolbox /opt/lab/bin/make-fixtures.sh /workspace/evidence-smoke
"${compose[@]}" run --rm --no-deps -T toolbox /opt/lab/bin/verify-evidence.sh /workspace/evidence-smoke
"${compose[@]}" run --rm --no-deps -T toolbox sh -c 'awk "/NoNewPrivs/{print; if (\$2 != 1) exit 1}" /proc/self/status'
# `compose run` does not publish service ports unless --service-ports is given.
# Both probes stay on 127.0.0.1 inside their disposable terminal container.
for terminal_service in terminal terminal-write; do
  terminal_id=$("${compose[@]}" run --detach --no-deps "$terminal_service")
  terminal_ids+=("$terminal_id")
  terminal_mode=--read-only
  if [[ "$terminal_service" == terminal-write ]]; then terminal_mode=--writable; fi
  if ! docker exec "$terminal_id" python3 /opt/lab/bin/ttyd-smoke.py "$terminal_mode"; then
    docker logs --tail 60 "$terminal_id" >&2 || true
    exit 1
  fi
  docker rm --force "$terminal_id" >/dev/null
done
printf 'Smoke complete; isolated temporary project will be removed.\n'
