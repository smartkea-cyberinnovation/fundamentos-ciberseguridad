#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
if (( $# != 1 )); then printf 'Usage: verify-evidence.sh synthetic-directory\n' >&2; exit 64; fi
directory=$1
if [[ ! -d "$directory" || -L "$directory" ]]; then printf 'Expected a real directory.\n' >&2; exit 66; fi
cd -- "$directory"
if [[ ! -f SHA256SUMS || -L SHA256SUMS ]]; then printf 'Expected regular SHA256SUMS.\n' >&2; exit 66; fi
for path in logs config logs/access.log logs/auth-synthetic.log config/service.env.example; do
  if [[ -L "$path" ]]; then printf 'Symlinks are not accepted in synthetic evidence.\n' >&2; exit 65; fi
done
# This exercise verifies exactly the generated files, never arbitrary host paths.
declare -A seen=()
while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ ! "$line" =~ ^[a-f0-9]{64}\ \ (logs/access\.log|logs/auth-synthetic\.log|config/service\.env\.example)$ ]]; then
    printf 'Unexpected manifest entry.\n' >&2; exit 65
  fi
  path=${line:66}
  if [[ -n ${seen[$path]:-} ]]; then printf 'Duplicate manifest entry.\n' >&2; exit 65; fi
  seen[$path]=1
done < SHA256SUMS
if (( ${#seen[@]} != 3 )); then printf 'Expected all three synthetic files.\n' >&2; exit 65; fi
# sha256sum verifies bytes against a locally generated manifest. It is not a signature.
sha256sum --check --strict SHA256SUMS
