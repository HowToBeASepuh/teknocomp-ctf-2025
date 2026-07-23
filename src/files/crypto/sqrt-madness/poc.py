#!/usr/bin/env python3
import json, math, socket, sys

HOST = "38.47.176.164"
PORT = 2014
TARGET_BITS = 2048

def make_pair(k: int, target_bits: int = TARGET_BITS):
    r = math.isqrt(k)
    assert r*r == k, "k is not a perfect square"
    T = 2*k - 1

    # Base exact solution
    a = r
    b = r*T  # = r*(2k-1)

    # Vieta jumps to blow up bit-lengths while preserving the equality
    while a.bit_length() <= target_bits or b.bit_length() <= target_bits:
        a = T*b - a
        if b.bit_length() <= target_bits:
            b = T*a - b
    return a, b

def recv_json_lines(f):
    """Yield JSON objects from a file-like socket, skipping banner lines."""
    for line in f:
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            # Probably the banner or snarky text
            sys.stdout.write(line.decode() if isinstance(line, (bytes, bytearray)) else line)
            sys.stdout.flush()

def main():
    with socket.create_connection((HOST, PORT)) as s:
        f_r = s.makefile("rb")
        f_w = s.makefile("wb", buffering=0)

        for msg in recv_json_lines(f_r):
            if "k" in msg:
                k = int(msg["k"])
                a, b = make_pair(k, TARGET_BITS)
                out = json.dumps({"a": a, "b": b}).encode() + b"\n"
                f_w.write(out)
            elif "flag" in msg:
                print(msg["flag"])
                return
            elif "error" in msg:
                print("[server]", msg["error"])
                return

if __name__ == "__main__":
    main()
