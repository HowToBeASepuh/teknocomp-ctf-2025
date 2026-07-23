---
layout: challenge.njk
title: ARX
category: Crypto
author: faizath
flag: "Teknocom{B4byARX_St34m_C1ph3r_K33ps_T3kn0c0m_Fl4g_X9Q2}"
flagTeaser: "Teknocom{B4byARX_St34m...}"
description: "A homemade 64-byte ARX stream cipher. The keystream tail reveals the '0' padding, enabling byte-by-byte backward reconstruction of the flag."
attachments:
  - { name: enc.py, path: /files/crypto/arx/enc.py }
  - { name: output.txt, path: /files/crypto/arx/output.txt }
tags: [crypto, stream-cipher, arx]
---

## Overview

We are given a crypto CTF challenge with two files: `enc.py`, which holds the encryption code, and `output.txt`, which holds the encrypted result. Reading `enc.py` tells us the algorithm is not a standard one; instead it is a homemade construction — a stream cipher built on simple ARX operations. The cipher works over a 64-byte state that is filled with the flag plus `'0'` padding characters until it reaches the full length of 64. The keystream is produced by the formula `b_t = g1(s_t) + g2(s_{t+1}) (mod 256)`, where `g1` and `g2` are simple non-linear functions based on bit shifts and XOR.

## Analysis

The first step in the analysis is to look at the keystream pattern present in `output.txt`. At the end of the output we see a run of the byte `0x01` repeated eight times. This is a strong hint that the state in the tail portion is nothing more than `'0'` padding. Why? Because when we test `g1(0x30)` and `g2(0x30)` for the ASCII value of `'0'`, their sum modulo 256 does indeed produce `0x01`. From this we can conclude that the real flag length is 55 characters, while the remainder is `'0'` padding, 9 characters long.

## Exploitation

Once the padding portion has been recovered, we can perform a backward analysis. Knowing the output value `b_t` and the result of `g2(s_{t+1})`, we can compute `g1(s_t)` in reverse. The function `g1` itself has a unique property in which every output has two possible inputs that are the bitwise complement of one another. By trying both possibilities while ensuring the result remains a sensible ASCII character, we can reconstruct the flag byte by byte, from the back toward the front.

## Flag

```
Teknocom{B4byARX_St34m_C1ph3r_K33ps_T3kn0c0m_Fl4g_X9Q2}
```
