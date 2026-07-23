---
layout: challenge.njk
title: Enigma
category: Misc
author: faizath
flag: "Teknocom{pUr3_LuCk_b4bY}"
flagTeaser: "Teknocom{pUr3_LuCk_b4bY}"
description: "Guess a number between 1 and 1000 with only 10 tries, using higher/lower hints. Binary search wins comfortably. nc 38.47.176.164 6128"
tags: [misc, binary-search]
---

## Challenge

We are given netcat access to a number-guessing game:

> Oh, come on… guessing a number between 1 and 1000? Sounds easy, right? Sure, you only get 10 tries...... what could possibly go wrong?
>
> `nc 38.47.176.164 6128`

For every guess, the server responds with a hint telling us whether the target is higher or lower than our guess. We must find the number within only 10 tries.

## Solution

The higher/lower feedback is exactly what a binary search needs. Instead of guessing blindly, we always guess the midpoint of the remaining range and halve the search space with each response.

The search space is 1 to 1000, and each guess cuts it in half. Since `log2(1000) ≈ 9.97 < 10`, at most 10 guesses are required to pin down any number in that range, which fits comfortably within the 10-try limit.

The algorithm is simply:

1. Track a low bound (1) and a high bound (1000).
2. Guess `mid = (low + high) // 2`.
3. If the hint says "higher", set `low = mid + 1`; if it says "lower", set `high = mid - 1`.
4. Repeat until the server confirms the correct number and returns the flag.

## Flag

```
Teknocom{pUr3_LuCk_b4bY}
```
