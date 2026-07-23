---
layout: challenge.njk
title: Sqrt Madness
category: Crypto
author: faizath
flag: "Teknocom{Br4inTw1st3d_Sqrt_Ch4ll3nge}"
flagTeaser: "Teknocom{Br4inTw1st3d_Sqrt...}"
description: "Given a perfect square k, find huge integers a,b with (a^2+ab+b^2)/(2ab+1)=k. Use the base solution a0=r, b0=r(2k-1) and Vieta jumping to exceed 2048 bits."
attachments:
  - { name: server.py, path: /files/crypto/sqrt-madness/server.py }
  - { name: poc.py, path: /files/crypto/sqrt-madness/poc.py }
tags: [crypto, vieta-jumping, number-theory]
---

## Overview

We are given a CTF challenge titled "Sqrt Madness" with a fairly challenging description: "Solve the impossible math madness… if you dare." When run, we are asked to connect to the server via `nc 38.47.176.164 2014`. From the available server code, we can see that the server gives us a value `k` that is always a perfect square, then asks us to find a pair of large integers `a` and `b` that satisfy the equation:

```
(a^2 + ab + b^2) / (2ab + 1) = k
```

There is an additional requirement: the values `a` and `b` must be larger than 2048 bits. If we succeed, we can pass several levels until we finally obtain the flag.

## Analysis

The main trick of this challenge lies in the fact that `k` is always a perfect square, say `k = r^2`. With a little algebraic manipulation, we can find a simple exact solution:

```
a0 = r
b0 = r * (2k - 1)
```

If this pair `(a0, b0)` is plugged into the equation, the result is exactly `k` with no remainder. So we already have a valid solution; it is just that the size of `a0` may be too small to pass the bit-length requirement.

To make `a` and `b` very large, we use the Vieta jumping method. The basic idea is to exploit the symmetry of the quadratic equation in the variables `a` and `b`. If `(a, b)` is a solution, then `(a' = (2k - 1)b - a, b)` is also a solution. This way, we can grow the values until they exceed 2048 bits. The process can be repeated several times, and in just a few steps the values `a` and `b` swell enormously.

## Exploitation

With that understanding, the next step is to build a Python script that:

1. Opens a connection to the server with a socket.
2. Reads the value `k` sent by the server.
3. Computes the square root `r` of `k`.
4. Forms the initial solution `(a0, b0)`.
5. Performs Vieta jumping until `a` and `b` are large enough.
6. Sends the result back in JSON format.
7. Repeats until all levels are passed and the flag appears.

```python
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
  a=r
  b = r*T # = r*(2k-1)

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
```

This script automatically performs all of those steps until the server hands over the flag. After the script is run, the connection displays a full opening message full of mockery typical of math CTF challenges, then finally the server sends the flag that marks the successful completion of the challenge.

## Flag

```
Teknocom{Br4inTw1st3d_Sqrt_Ch4ll3nge}
```
