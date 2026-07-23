---
layout: challenge.njk
title: Overfit
category: Rev
author: faizath
flag: "Teknocom{L00k_M0m_1_Tr41n3d_A_N3ural_N3tw0rk_F0r_4_Fl4g}"
flagTeaser: "Teknocom{L00k_M0m_1_Tr41n3d...}"
description: "Someone thought neural networks make things secure. Prove them wrong — invert a 2-layer sigmoid MLP analytically to recover the secret input."
tags: [neural-network, numpy, inversion, math]
---

## Overview

We are given a model file named `Overfit.npz` for the "Overfit" challenge, with a description saying that someone thought neural networks make things secure. The key to solving it is realizing that the model is nothing more than a 2-layer MLP with sigmoid activations that has overfit onto a secret vector. Because each layer uses a sigmoid and its weight matrices are full rank, this network can essentially be inverted analytically. We simply "unwrap" each layer using the logit function, then solve the linear system to get back to the original input, which then quantizes into ASCII bytes.

## Analysis

The structure is `y = σ(W₂ σ(W₁ x + b₁) + b₂)`. We take the logit of the output to undo the sigmoid, giving `z₂ = logit(y) − b₂`, then solve `W₂ a₁ = z₂` to obtain `a₁`. Since `a₁ = σ(z₁)`, we take the logit again so that `z₁ = logit(a₁) − b₁`, then solve `W₁ x = z₁` to obtain `x`. In the implementation, it is far more stable to solve the linear systems than to compute the matrix inverse explicitly. The resulting values of `x` turn out to lie on a grid of multiples of 1/127. Multiplying by 127 and rounding to the nearest integer produces a sequence of bytes which, when read as ASCII, form the flag.

For numerical stability, before calling logit the values should lie in the open range 0 to 1. In practice, use a small clamp such as `clip(p, 1e−9, 1−1e−9)` on both `y` and `a₁`. After that, the linear system can be solved with `np.linalg.solve`. The final stage is converting `x` to bytes by rounding, then decoding to a string.

## Solution

A concise example implementation looks like this, assuming `Overfit.npz` contains `W1`, `b1`, `W2`, `b2`, and `y`:

```python
import numpy as np

def logit(p, eps=1e-9):
  p = np.clip(p, eps, 1 - eps)
  return np.log(p) - np.log(1 - p)

data = np.load("Overfit.npz", allow_pickle=True)
W1, b1 = data["W1"], data["b1"]
W2, b2 = data["W2"], data["b2"]
y    = data["y"]     # keluaran jaringan untuk input rahasia

z2 = logit(y) - b2
a1 = np.linalg.solve(W2, z2)
z1 = logit(a1) - b1
x = np.linalg.solve(W1, z1)

bytes_arr = np.rint(x * 127).astype(np.uint8)
flag = bytes_arr.tobytes().decode("ascii")
print(flag)
```

Running the steps above shows that the model really did just "memorize" its input. This is a classic example that overfitting is not cryptography. Invertible activations, combined with full-rank weights, make the inversion path straightforward and applicable layer by layer.

## Flag

`Teknocom{L00k_M0m_1_Tr41n3d_A_N3ural_N3tw0rk_F0r_4_Fl4g}`
