#!/bin/sh
# Keep the packaged binary and all arguments, without Kali's privilege assumption.
# https://bugs.kali.org/view.php?id=9085
# https://nmap.org/book/man-misc-options.html
unset NMAP_PRIVILEGED
NMAP_UNPRIVILEGED=1
export NMAP_UNPRIVILEGED
exec /usr/lib/nmap/nmap "$@"
