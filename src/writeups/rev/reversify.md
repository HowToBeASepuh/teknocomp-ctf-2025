---
layout: challenge.njk
title: Reversify
category: Rev
author: faizath
flag: "Teknocom{kn0w_th3_bin4ry_fi1e_with_s0m3_str1ng}"
flagTeaser: "Teknocom{kn0w_th3_bin4ry...}"
description: "This program asks you to enter the flag. Beware there are multiple fake flags; the real flag is split into several parts inside the binary and only combining them correctly gives the real flag."
tags: [reversing, strings, elf]
---

## Overview

We are given a binary for the challenge called Reversify. The description tells us the program will ask us to enter the flag, and warns that there are many fake flags meant to mislead us: the real flag is split into several parts inside the binary. From the start I approached it with light reversing, focusing on identifying the architecture, inspecting the strings, and then validating the order in which the flag fragments are assembled.

## Analysis

The first step was to confirm the file format. A simple `file main` command showed that this is a 64-bit ELF for Linux. Once I knew the target, I tried running the program without meaningful input to observe its basic behavior. The program immediately asked to "enter the flag" and returned a wrong-answer response when arbitrary input was provided. This confirmed that validation happens entirely inside the binary, not by calling any external service.

Because the description mentions the existence of fake flags, I started with string enumeration. The command:

```bash
strings -n 5 main | grep -i 'Teknocom'
```

displayed many candidates of the form `Teknocom{...}` that were clearly designed as traps. However, among that row of decoys, a few fragments appeared that did not form a complete flag on their own, but instead looked like pieces that complement each other. The fragments that looked relevant were `Teknocom{kn0w`, `_th3_bin4ry`, `_fi1e_with`, and `_s0m3_str1ng}`. The pattern was interesting because they were all consistent with the snake_case and leetspeak naming style commonly used in CTFs.

To make sure this was not a coincidence, I opened the binary in a disassembler. There I saw a routine that assembles a result buffer from several separate string literals. The concatenation order matched exactly the four fragments above. The opening piece contains the prefix and the opening curly brace, the two middle pieces are keywords joined by underscores, and the final piece closes with the closing curly brace. When combined, the four produce a coherent, natural-reading sentence, something that rarely happens with fake flags.

## Solution

As a final verification, I ran the program and entered the combination of the four fragments. The program responded with a correct message, confirming that this is the valid flag. The presence of many "ready-made" fake flags inside the binary is the misdirection, but the hint that the real flag is split and needs to be reassembled makes the fragment-combination approach the most sensible solution.

```text
Teknocom{kn0w_th3_bin4ry_fi1e_with_s0m3_str1ng}
```

## Flag

`Teknocom{kn0w_th3_bin4ry_fi1e_with_s0m3_str1ng}`
