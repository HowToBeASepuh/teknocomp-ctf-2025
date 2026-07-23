---
layout: challenge.njk
title: Ba1ted
category: Rev
author: faizath
flag: "Teknocom{c0ngr4ts_but_n0t_r34llyy}"
flagTeaser: "Teknocom{c0ngr4ts_but...}"
description: "Enter the correct password to get the flag. It uses constructor functions that check the password before main() runs; the 24-char password is checked in small parts and one wrong character exits immediately."
tags: [reversing, init_array, constructors, elf]
---

## Overview

We are given a binary for the challenge called "Ba1ted", with a description saying the program looks simple: enter the correct password to get the flag. The twist is that the password is checked inside constructor functions that execute before `main()` runs. This means validation happens very early, and the program will exit immediately if even a single character is wrong. Our goal is to understand the checking flow at the constructor stage, then reassemble the 24-character password from the small pieces that are verified one by one.

## Analysis

Analysis begins by confirming that the binary is an ELF that uses the `.init_array` section. This section contains a list of function pointers that the runtime executes automatically before `main()`. With tools like `readelf` or `objdump`, the order of the constructor functions can be pulled from `.init_array`. From this we can see a total of fourteen entries. The first two entries are simple sanity checks that force the program's argument count to be two and the length of `argv[1]` to be exactly 24. The next twelve entries are checkers that perform two-character substring comparisons against the supplied password.

Each checker follows a consistent pattern. Every function reads two characters from `argv[1]` at an increasing global offset, then calls `strncmp` to compare them against two reference characters that come from a long string in `.rodata`. If they match, the global offset is increased by 2 and control continues to the next constructor. If they do not match, the function calls `exit`, so the program stops right there. The core trick is that the checker order does not follow the natural order in the source code, but rather follows the exact order as recorded in `.init_array`. Because of this, reconstructing the password must follow the constructor order, not the address order in `.text` or the position of the symbols.

After mapping the constructor order from `.init_array`, each constructor is traced to its reference string in `.rodata`. Each one points to a long sequence of random-looking characters that is actually only used as the source of the two characters at the offset currently being tested. The strategy is to take two characters from each reference string according to the current global offset, in the exact order of `.init_array`, then append them in sequence until the total reaches 24 characters. In practice, we walk through the 12 checker constructors, each time taking two characters, so we get 12 times 2 characters that, when assembled, form the complete password.

## Solution

With those steps, the twelve two-character pieces combine into the final 24-character password: `c0ngr4ts_but_n0t_r34llyy`. This password is then tried as an argument when running the program. Inside `main()`, if all the earlier checks passed, the program prints a congratulatory message and the flag in the format `Teknocom{<password>}`, then calls `_exit(0)`. Because `_exit` does not flush the standard buffers, the output sometimes does not appear if stdout is still buffered. The fix is to run the program with stdout unbuffered using:

```bash
stdbuf -o0 -e0 ./main 'c0ngr4ts_but_n0t_r34llyy'
```

or simply pipe it to `cat` so the buffer is flushed out.

The correct password is `c0ngr4ts_but_n0t_r34llyy`. After entering it, the program displays the flag: `Teknocom{c0ngr4ts_but_n0t_r34llyy}`.

## Flag

`Teknocom{c0ngr4ts_but_n0t_r34llyy}`
