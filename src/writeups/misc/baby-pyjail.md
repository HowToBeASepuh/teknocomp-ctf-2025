---
layout: challenge.njk
title: Baby Pyjail
category: Misc
author: faizath
flag: "Teknocom{Fr33d0m_4ft3r_th3_J41l}"
flagTeaser: "Teknocom{Fr33d0m_4ft3r_th3...}"
description: "A Python sandbox with restricted builtins. Escape via ().__class__.__base__.__subclasses__() to reach BaseRequestHandler's globals and the real __builtins__. nc 38.47.176.164 1002"
tags: [misc, pyjail, sandbox-escape]
---

## Challenge

We are given a CTF challenge named Baby Pyjail with a simple description: "Just baby pyjail — `nc 38.47.176.164 1002`". From the description we already know this is a pyjail, a Python sandbox that restricts the builtins so that players cannot directly access dangerous functions such as `open`, `eval`, or `__import__`. Typically only safe functions like `print` and `input` are available.

## Recon

The first step is to send simple Python expressions to test what is allowed. After probing, the environment indeed leaves only a very limited set of builtins. However, in a classic Python sandbox there is always a way to regain access to the real builtins.

One common trick is to use `().__class__.__base__.__subclasses__()`, which returns a list of all subclasses of `object`. From that list, we can look for a specific class that originates from a module the server program has already imported.

## Escape

In this case, the server uses `socketserver`, which automatically loads several classes such as `BaseRequestHandler` and `TCPServer`. This means we can locate the `BaseRequestHandler` class through `object.__subclasses__()`. Once the class is found, we access `__init__.__globals__` to obtain the global dictionary of the module where the class is defined. From there we can grab the real `__builtins__`.

With the real builtins in hand, we can finally call `__import__` to access the `builtins` module and invoke `open`. The file we are after is, of course, `flag.txt`.

```python
print([c for c in ().__class__.__base__.__subclasses__() if c.__name__=='BaseRequestHandler'][0].__init__.__globals__['__builtins__']['__import__']('builtins').open('flag.txt').read())
```

After running this against the server via `nc 38.47.176.164 1002`, the payload successfully reads the contents of `flag.txt` and prints the flag.

## Flag

```
Teknocom{Fr33d0m_4ft3r_th3_J41l}
```
