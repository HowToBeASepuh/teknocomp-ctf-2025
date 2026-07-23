---
layout: challenge.njk
title: Betting
category: Web
author: faizath
flag: "Tekncom{G4mbl1ng_L0se_M0n3y_4ll_Day_L0l}"
flagTeaser: "Tekncom{G4mbl1ng_L0se...}"
description: "“Don't worry, bro, no one can hack this!” Picking all-zero slots via the GET parameter wins the flag. http://38.47.176.164:4112/"
tags: [web, logic]
---

## Overview

We are given a URL where a GET parameter encodes the numbers the player has selected:

```
http://38.47.176.164:4112/
```

## Analysis

The `slot` GET parameter carries the values chosen for each reel of the betting game. The application trusts these client-supplied values directly, so we can pick any combination we want rather than relying on a random spin.

## Exploitation

Manually selecting the slot combination `0,0,0,0,0` produces the winning outcome and returns the flag. Sending the following request wins the game:

```
http://38.47.176.164:4112/?slot=0%2C0%2C0%2C0%2C0&play=1
```

Here `%2C` is the URL encoding of a comma, so `slot=0,0,0,0,0` and `play=1` triggers the play action with the winning selection.

## Flag

```
Tekncom{G4mbl1ng_L0se_M0n3y_4ll_Day_L0l}
```
