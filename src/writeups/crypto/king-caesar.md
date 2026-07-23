---
layout: challenge.njk
title: King Caesar
category: Crypto
author: faizath
flag: "Teknocom{Th1s_C4es4r_1s_4_J0k3_S1mpl3r_Th4n_Y0u}"
flagTeaser: "Teknocom{Th1s_C4es4r_1s_4_J0k3...}"
description: "Each WORD of the message is Caesar-shifted by a repeating pattern 3,5,2,4,1. Uniform ROT13/ROT23 only yields fake flags."
tags: [crypto, caesar, classical]
---

## Overview

We are given a ciphertext string `Whnqrfrp{Wk1v_H4jx4w_1u_4_K0l3_V1pso3u_Ym4s_A0w}` under the challenge title "King Caesar". The description explains that this secret message has been shifted using a repeating letter-shift pattern, namely 3, 5, 2, 4, 1. The challenge is to find the real flag, because applying a uniform ROT13 or even a uniform ROT23 only produces a fake flag.

## Analysis

The first step is to observe the flag format, which is usually of the form `{...}` with words separated by underscores. Each word inside the flag is treated as a single unit, which is then shifted according to the pattern. So the first word is shifted by 3 letters, the second word by 5, the third word by 2, the fourth word by 4, the fifth word by 1, and then the pattern repeats for the following words.

## Exploitation

We apply this pattern to the ciphertext:

- Word 1 `Wk1v`, shifted back 3 letters, becomes `Th1s`.
- Word 2 `H4jx4w`, shifted back 5 letters, becomes `C4es4r`.
- Word 3 `1u`, shifted back 2 letters, becomes `1s`.
- Word 4 `4`, shifted by 4, stays `4` because it is a digit.
- Word 5 `K0l3`, shifted back 1 letter, becomes `J0k3`.
- Word 6 `V1pso3u`, shifted back 3 letters, becomes `S1mpl3r`.
- Word 7 `Ym4s`, shifted back 5 letters, becomes `Th4n`.
- Word 8 `A0w`, shifted back 2 letters, becomes `Y0u`.

After processing every word according to the pattern, the final result is the hidden real flag.

## Flag

```
Teknocom{Th1s_C4es4r_1s_4_J0k3_S1mpl3r_Th4n_Y0u}
```
