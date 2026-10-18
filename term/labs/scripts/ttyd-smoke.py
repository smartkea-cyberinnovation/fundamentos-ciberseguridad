#!/usr/bin/env python3
"""Bounded local checks for the pinned ttyd 1.7.7 protocol, using only stdlib.

Run inside the disposable Compose terminal container. No arbitrary URL or command
is accepted. This checks ttyd itself; Cloudflare Access needs its own identity test.
Protocol: https://github.com/tsl0922/ttyd/blob/1.7.7/src/protocol.c
"""
import base64
import hashlib
import http.client
import os
import socket
import struct
import sys
import time
import uuid

HOST, PORT = "127.0.0.1", 7681
AUTHORITY = f"{HOST}:{PORT}"
MAX_BYTES = 65536


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def wait_http():
    deadline = time.monotonic() + 20
    while True:
        conn = http.client.HTTPConnection(HOST, PORT, timeout=2)
        try:
            conn.request("GET", "/")
            response = conn.getresponse()
            body = response.read(MAX_BYTES)
            check(response.status == 200, f"ttyd HTTP status: {response.status}")
            check("text/html" in response.getheader("Content-Type", ""), "missing HTML index")
            check(len(body) > 100, "empty ttyd index")
            return
        except (OSError, http.client.HTTPException):
            if time.monotonic() >= deadline:
                raise RuntimeError("ttyd did not become ready within 20 seconds") from None
            time.sleep(0.1)
        finally:
            conn.close()


class WebSocket:
    def __init__(self, origin):
        self.sock = socket.create_connection((HOST, PORT), timeout=3)
        self.buffer = bytearray()
        self.status = None
        try:
            key = base64.b64encode(os.urandom(16)).decode("ascii")
            request = (
                f"GET /ws HTTP/1.1\r\nHost: {AUTHORITY}\r\n"
                "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
                f"Sec-WebSocket-Protocol: tty\r\nOrigin: {origin}\r\n\r\n"
            )
            self.sock.sendall(request.encode("ascii"))
            while b"\r\n\r\n" not in self.buffer:
                chunk = self.sock.recv(4096)
                if not chunk:
                    return  # libwebsockets may reject by closing without a response.
                self.buffer.extend(chunk)
                check(len(self.buffer) <= MAX_BYTES, "oversized WebSocket headers")
            raw, rest = bytes(self.buffer).split(b"\r\n\r\n", 1)
            self.buffer = bytearray(rest)
            lines = raw.decode("iso-8859-1").split("\r\n")
            self.status = int(lines[0].split(" ", 2)[1])
            if self.status == 101:
                headers = {key.lower(): value.strip() for key, value in
                           (line.split(":", 1) for line in lines[1:])}
                # SHA-1 is mandated here by the WebSocket handshake, not a password hash.
                accept = base64.b64encode(hashlib.sha1(
                    (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")
                ).digest()).decode("ascii")
                check(headers.get("sec-websocket-accept") == accept, "invalid WebSocket accept")
                check(headers.get("sec-websocket-protocol") == "tty", "wrong subprotocol")
        except BaseException:
            self.sock.close()
            raise

    def close(self):
        self.sock.close()

    def send(self, payload, opcode=2):
        check(len(payload) < 65536, "oversized client frame")
        mask = os.urandom(4)
        size = len(payload)
        header = bytes([0x80 | opcode, 0x80 | size]) if size < 126 else bytes([0x80 | opcode, 0xFE]) + struct.pack("!H", size)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def read_exact(self, count, deadline):
        while len(self.buffer) < count:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("WebSocket receive deadline")
            self.sock.settimeout(remaining)
            chunk = self.sock.recv(min(MAX_BYTES, count - len(self.buffer)))
            if not chunk:
                raise RuntimeError("ttyd closed WebSocket unexpectedly")
            self.buffer.extend(chunk)
        result = bytes(self.buffer[:count])
        del self.buffer[:count]
        return result

    def frame(self, deadline):
        flags, length = self.read_exact(2, deadline)
        check(flags & 0x80 and not flags & 0x70, "unexpected fragmented/compressed frame")
        check(not length & 0x80, "server must not mask WebSocket frames")
        length &= 0x7F
        if length == 126:
            length = struct.unpack("!H", self.read_exact(2, deadline))[0]
        elif length == 127:
            length = struct.unpack("!Q", self.read_exact(8, deadline))[0]
        check(length <= MAX_BYTES, "oversized server frame")
        return flags & 0x0F, self.read_exact(length, deadline)

    def output(self, seconds, until=None):
        deadline = time.monotonic() + seconds
        result = bytearray()
        while time.monotonic() < deadline:
            try:
                opcode, payload = self.frame(deadline)
            except TimeoutError:
                break
            if opcode == 9:
                self.send(payload, opcode=10)
            elif opcode == 8:
                raise RuntimeError("ttyd sent an unexpected close frame")
            elif opcode in (1, 2) and payload[:1] == b"0":
                result.extend(payload[1:])
                check(len(result) <= MAX_BYTES, "oversized terminal output")
                if until is not None and until in result:
                    return bytes(result)
        if until is not None:
            raise RuntimeError("expected terminal output was not received before deadline")
        return bytes(result)


def run(mode):
    wait_http()
    bad = WebSocket("https://not-this-lab.invalid")
    try:
        check(bad.status != 101, "ttyd accepted a mismatched Origin")
    finally:
        bad.close()
    ws = WebSocket(f"http://{AUTHORITY}")
    try:
        check(ws.status == 101, f"ttyd rejected its own Origin: {ws.status}")
        ws.send(b'{"columns":100,"rows":24}', opcode=1)
        nonce = uuid.uuid4().hex
        if mode == "--read-only":
            initial = ws.output(8, until=b"Actualizacion cada 5 segundos")
            check(b"UID: 10001" in initial, "readonly process has an unexpected UID")
            marker = f"__KEA_READONLY_{nonce}__".encode("ascii")
            ws.send(b"0" + marker + b"\r")
            after = ws.output(7)
            check(marker not in after, "readonly terminal echoed forbidden input")
            check(b"Vista de observacion" in after, "readonly monitor did not continue after input")
        else:
            ws.output(8, until=b"Trabajo persistente:")
            # The success marker is split in the command to distinguish execution
            # from the PTY echo. No files or external systems are modified.
            prefix, suffix = "__KEA_EXEC_", nonce + "__"
            command = (
                'if [ "$(id -u)" = 10001 ] && [ -w /workspace ] && '
                '[ ! -w /etc ] && [ ! -S /var/run/docker.sock ] && '
                "grep -Eq '^NoNewPrivs:[[:space:]]+1$' /proc/self/status; then "
                f"printf '%s%s\\n' '{prefix}' '{suffix}'; fi\r"
            )
            ws.send(b"0" + command.encode("ascii"))
            ws.output(8, until=(prefix + suffix).encode("ascii"))
    finally:
        ws.close()
    print(f"ttyd {mode}: HTTP, wrong-Origin rejection, valid WebSocket and PTY checks passed.")


if __name__ == "__main__":
    if sys.argv[1:] not in (["--read-only"], ["--writable"]):
        print("Usage: ttyd-smoke.py --read-only|--writable (loopback only)", file=sys.stderr)
        raise SystemExit(64)
    try:
        run(sys.argv[1])
    except (OSError, ValueError, RuntimeError, http.client.HTTPException) as error:
        print(f"ttyd smoke failed: {error}", file=sys.stderr)
        raise SystemExit(1) from None
