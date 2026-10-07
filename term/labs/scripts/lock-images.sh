#!/usr/bin/env bash
# Writes approved base-image digests to stdout after pulling official references.
set -Eeuo pipefail
umask 077
if (( $# )); then printf 'Usage: lock-images.sh > base-images.lock.env\n' >&2; exit 64; fi
command -v docker >/dev/null 2>&1 || { printf 'Docker CLI required.\n' >&2; exit 69; }
for entry in 'KALI_IMAGE=kalilinux/kali-rolling:latest' 'PYTHON_IMAGE=python:3.13-slim-bookworm'; do
  key=${entry%%=*}
  reference=${entry#*=}
  docker pull "$reference" >&2
  digest=$(docker image inspect --format '{{index .RepoDigests 0}}' "$reference")
  if [[ ! "$digest" =~ ^[a-zA-Z0-9./:_-]+@sha256:[a-f0-9]{64}$ ]]; then
    printf 'Invalid or missing image digest for %s\n' "$reference" >&2
    exit 65
  fi
  printf '%s=%s\n' "$key" "$digest"
done
