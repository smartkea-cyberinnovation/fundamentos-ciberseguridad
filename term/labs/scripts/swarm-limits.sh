#!/usr/bin/env bash
# Run as the lab administrator after each stack deploy; no port publication.
set -Eeuo pipefail
if (( $# != 1 )) || [[ ! "$1" =~ ^[a-z][a-z0-9-]{1,40}$ ]]; then
  printf 'Usage: swarm-limits.sh stack-name (lowercase letters, digits, hyphens)\n' >&2
  exit 64
fi
stack_name=$1
command -v docker >/dev/null 2>&1 || { printf 'Docker CLI required.\n' >&2; exit 69; }
docker service update --limit-pids 32 --init "${stack_name}_web"
docker service update --limit-pids 128 --init "${stack_name}_terminal"
docker service update --limit-pids 64 --init "${stack_name}_cloudflared"
