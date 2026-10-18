#!/usr/bin/env bash
# Create a new directory with synthetic evidence; refuse existing paths/symlinks.
set -Eeuo pipefail
umask 077

if (( $# > 1 )); then printf 'Usage: make-fixtures.sh [new-directory]\n' >&2; exit 64; fi
destination=${1:-./evidence-synthetic}
if [[ -z "$destination" || -e "$destination" || -L "$destination" ]]; then
  printf 'Destination must be a new directory: %s\n' "$destination" >&2
  exit 73
fi
mkdir -m 0700 -- "$destination"
mkdir -m 0700 -- "$destination/logs" "$destination/config" "$destination/reports"
cat > "$destination/logs/access.log" <<'DATA'
192.0.2.10 - - [07/Oct/2026:09:00:00 +0000] "GET /health HTTP/1.1" 200 69
192.0.2.20 - - [07/Oct/2026:09:00:10 +0000] "GET / HTTP/1.1" 200 891
192.0.2.20 - - [07/Oct/2026:09:01:00 +0000] "GET /no-existe HTTP/1.1" 404 39
198.51.100.30 - - [07/Oct/2026:09:02:00 +0000] "HEAD /robots.txt HTTP/1.1" 200 43
192.0.2.20 - - [07/Oct/2026:09:03:00 +0000] "GET /catalog.json HTTP/1.1" 200 172
203.0.113.40 - - [07/Oct/2026:09:04:00 +0000] "GET /training-only HTTP/1.1" 404 39
DATA
cat > "$destination/logs/auth-synthetic.log" <<'DATA'
2026-10-07T09:10:00Z lab-vm sshd: Failed publickey for learner-demo from 192.0.2.50 port 50100 ssh2
2026-10-07T09:10:12Z lab-vm sshd: Failed publickey for learner-demo from 192.0.2.50 port 50101 ssh2
2026-10-07T09:12:00Z lab-vm sshd: Accepted publickey for learner-demo from 192.0.2.60 port 50102 ssh2
DATA
cat > "$destination/config/service.env.example" <<'DATA'
SERVICE_NAME=synthetic-lab
LOG_LEVEL=info
HTTP_PORT=8080
DATA
printf '%s\n' 'SYNTHETIC DATA: documentation IPs; fake events; never a real incident.' > "$destination/README.txt"
(
  cd -- "$destination"
  find logs config -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)
printf 'Created synthetic evidence in %s\n' "$destination"
