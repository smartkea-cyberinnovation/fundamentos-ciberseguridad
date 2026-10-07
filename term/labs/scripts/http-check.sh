#!/usr/bin/env bash
# Fixed lab target: a short GET with bounded time and no automatic redirections.
set -Eeuo pipefail
umask 077
if (( $# )); then printf 'Usage: http-check.sh (fixed target http://web:8080/health)\n' >&2; exit 64; fi
command -v curl >/dev/null 2>&1 || { printf 'curl is required.\n' >&2; exit 69; }
command -v jq >/dev/null 2>&1 || { printf 'jq is required.\n' >&2; exit 69; }
curl --noproxy '*' --proto '=http' --fail --silent --show-error --connect-timeout 2 --max-time 5 http://web:8080/health \
  | jq -e '.status == "ok" and .service == "smartkea-lab-web" and .synthetic == true'
