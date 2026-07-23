---
layout: challenge.njk
title: PrimeSum
category: Crypto
author: faizath
flag: "Teknocom{Br1ng_Me_Th3_Pr1m3s_p_plus_q}"
flagTeaser: "Teknocom{Br1ng_Me_Th3_Pr1m3s...}"
description: "Classic RSA but you're given p+q instead of a prime. Factor via ed-1 candidates for phi(n), then a perfect-square discriminant of x^2-(p+q)x+n."
attachments:
  - { name: enc.py, path: /files/crypto/primesum/enc.py }
  - { name: output.txt, path: /files/crypto/primesum/output.txt }
tags: [crypto, rsa, factorization]
---

## Overview

We are given a crypto CTF challenge titled PrimeSum. From the description, the challenge is about classic RSA, but with a small twist. Usually in an RSA challenge we are given one of the prime factors `p` or `q`, but this time what we get is not a factor but their sum, `p + q`. At first glance this information looks not very useful, yet this is precisely where the crack to break the encryption lies.

## Analysis

In RSA we know that the modulus `n` is the product of `p` and `q`, and the totient `phi(n)` is `(p-1)(q-1)`, which can be rewritten as `n - (p+q) + 1`. Because this challenge provides both `e` and `d`, we can exploit the relation `ed = 1 (mod phi(n))`. This means `ed - 1` is a multiple of `phi(n)`. From here we can guess candidates for `phi(n)` by factoring `ed - 1`. Each time we find a suitable divisor, we can compute `n = phi(n) + (p+q) - 1`. Once `n` is obtained, we can test whether the discriminant of the quadratic equation `x^2 - (p+q)x + n = 0` is a perfect square. If it is, then we have successfully found valid `p` and `q`.

## Exploitation

After obtaining the pair `p` and `q`, the next step is easy. We already have the ciphertext `c` and the private exponent `d`. Decryption is done with `m = c^d mod n`. This result `m` is then converted into a byte string, and finally reads clearly as the flag.

## Flag

```
Teknocom{Br1ng_Me_Th3_Pr1m3s_p_plus_q}
```
