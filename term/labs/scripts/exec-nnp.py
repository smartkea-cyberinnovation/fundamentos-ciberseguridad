#!/usr/bin/env python3
"""Irreversibly enable Linux no_new_privs before exec, including under Swarm."""
import ctypes
import os
import sys

if os.geteuid() == 0:
    raise SystemExit("Refusing to start a terminal as root.")
if len(sys.argv) < 2 or sys.argv[1] != "/usr/local/bin/ttyd":
    raise SystemExit("This launcher only starts the fixed ttyd binary.")
libc = ctypes.CDLL(None, use_errno=True)
libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
libc.prctl.restype = ctypes.c_int
if libc.prctl(38, 1, 0, 0, 0) != 0:  # PR_SET_NO_NEW_PRIVS from linux/prctl.h
    raise OSError(ctypes.get_errno(), "PR_SET_NO_NEW_PRIVS failed")
os.execv(sys.argv[1], sys.argv[1:])
