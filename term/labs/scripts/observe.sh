#!/usr/bin/env bash
# A readonly dashboard for the current lab container; no shared student session.
set -Eeuo pipefail
while :; do
  printf '\033[2J\033[HSmartKEA · Vista de observacion · %s\n\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  printf 'Modo solo lectura. Muestra este contenedor, no la sesion de otra persona.\n'
  printf 'Usuario: %s · UID: %s · kernel: %s\n\n' "$(id -un)" "$(id -u)" "$(uname -r)"
  printf 'Memoria visible (los limites de cgroup pueden ser inferiores):\n'
  free -m
  printf '\nConexiones TCP en escucha del contenedor:\n'
  ss -lnt
  printf '\nEstado del objetivo HTTP local:\n'
  if ! curl --noproxy '*' --fail --silent --show-error --max-time 2 http://web:8080/health; then
    printf 'web todavia no disponible; inicia el servicio web del laboratorio.\n'
  fi
  printf '\nActualizacion cada 5 segundos. Para escribir, activar perfil terminal-write.\n'
  sleep 5
done
