#!/usr/bin/env bash
# Read-only, bounded diagnostic. Never collects env, history, passwords or cmdlines.
set -Eeuo pipefail
umask 077
export LC_ALL=C

if (( $# )); then
  printf 'Usage: diagnose.sh > diagnostic.txt\nNo arguments are accepted.\n' >&2
  exit 64
fi

section() { printf '\n## %s\n' "$1"; }
run() {
  local binary=$1
  shift
  if ! command -v "$binary" >/dev/null 2>&1; then
    printf '[unavailable] %s\n' "$binary"
    return 0
  fi
  local code=0
  if command -v timeout >/dev/null 2>&1; then
    timeout --signal=TERM 5s "$binary" "$@" || code=$?
  else
    "$binary" "$@" || code=$?
  fi
  if (( code )); then printf '[exit=%s] %s\n' "$code" "$binary"; fi
}

printf '# SmartKEA Linux diagnostic\nUTC: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
section 'Kernel and user'; run uname -srmo; run id
section 'Load and memory'; run uptime; run free -m
section 'Filesystems (metadata only)'; run df -hT
section 'Network interfaces'; run ip -brief address
section 'Routes'; run ip route show
section 'TCP listeners (no process arguments)'; run ss -lnt
section 'Tools present'
for binary in bash sh git docker curl jq nmap shellcheck ttyd; do
  if command -v "$binary" >/dev/null 2>&1; then printf '%s: present\n' "$binary"; else printf '%s: absent\n' "$binary"; fi
done
printf '\nReport complete. Inspect hostnames, IPs and usernames before sharing.\n'
