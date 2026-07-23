---
layout: challenge.njk
title: Pailliiered
category: Crypto
author: faizath
flag: "Teknocom{Breaking_P41ll13r_Really_Was_A_Bad_Idea}"
flagTeaser: "Teknocom{Breaking_P41ll13r...}"
description: "A Paillier service leaks E(4). Its additive homomorphism lets us craft E(M) for any M via exponentiation and have the server decrypt our target string."
attachments:
  - { name: server.py, path: /files/crypto/pailliiered/server.py }
  - { name: poc.py, path: /files/crypto/pailliiered/poc.py }
tags: [crypto, paillier, homomorphic]
---

## Overview

We are given a crypto challenge called "Pailliiered" that opens a TCP service at `nc 38.47.176.164 1006`. This service prints the Paillier modulus `n`, hides `g`, and then hands us one sample ciphertext `E(4)`. The challenge essentially asks us to "encrypt" a particular string, namely "Please give me the flag", and send that ciphertext back so the server decrypts it and releases the flag. The trick is very simple: the Paillier scheme has an additive homomorphism. From the single sample `E(4)` we can build `E(M)` for any message `M` using only exponentiation. Use the fact that `E(m)^k = E(k*m)`. Take `k = M * inv(4) mod n`, then compute `c = E(4)^k mod n^2`. When sent to the server, `c` decrypts exactly to `M`, which is the bytes of "Please give me the flag", so the server spits out the flag.

## Analysis

Why does this work? Paillier encryption has the form `c = g^m * r^n mod n^2`. Multiplying ciphertexts accumulates the addition of plaintexts, so `E(m1)*E(m2) = E(m1+m2)`. More generally, raising a ciphertext to the power `k` gives `E(k*m)`. Because 4 is coprime with the odd `n`, 4 has an inverse modulo `n`. Thus `E(4)^k` becomes `E(M)` when `k` is chosen as `M*inv(4) mod n`. The vulnerability in this challenge is that the server leaks `E(4)`, so we do not need the full public key to perform arbitrary encryption — we only need to exploit the homomorphism.

## Exploitation

The practical implementation is nice to build with pwntools so the connection is verbose. The flow: connect to the host, receive the banner, parse `n` and `E(4)` with regex, turn the target "Please give me the flag" into a big-endian integer, compute `inv(4) mod n`, then send `c = pow(E4, k, n*n)`. Below is a sample script with verbosity turned on so each stage is clearly visible in the log.

```python
import socket, re

HOST, PORT = "38.47.176.164", 1006

# Integer value of b"Please give me the flag"
M = 7703033469609239351985350025414201079417630703156486503 #
int.from_bytes(..., "big")

def recv_until(sock, needle):
  buf = b""
  while needle not in buf:
     chunk = sock.recv(8192)
     if not chunk:
         break
     buf += chunk
  return buf

with socket.create_connection((HOST, PORT)) as s:
   banner = recv_until(s, b"Please give me the flag")
   text = banner.decode()
   print(text)

  # Parse n and E(4) from the banner
  n = int(re.search(r"Public key \(n, g\) = \((\d+), \?\)", text).group(1))
  c4 = int(re.search(r"E\(4\) = (\d+)", text).group(1))
  s2 = n * n

  # Compute k = M * inv(4) mod n (Python 3.8+: pow(4, -1, n) is the modular inverse)
  inv4 = pow(4, -1, n)
  k = (M * inv4) % n

  # Craft ciphertext: c = (E(4))^k mod n^2 == E(M)
  c = pow(c4, k, s2)

  # Send it
  s.sendall(str(c).encode() + b"\n")

  # Print the server's reply (should include the flag)
  try:
     while True:
       out = s.recv(4096)
       if not out:
           break
      print(out.decode(), end="")
  except Exception:
    pass
```

## Flag

```
Teknocom{Breaking_P41ll13r_Really_Was_A_Bad_Idea}
```
