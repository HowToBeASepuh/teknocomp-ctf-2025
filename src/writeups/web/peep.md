---
layout: challenge.njk
title: PEEP
category: Web
author: faizath
flag: "Teknocom{Oops_Found_Your_Silly_Fl4g_Haha}"
flagTeaser: "Teknocom{Oops_Found_Your...}"
description: "A Node.js click-counter whose naive path sanitizer (single replace of '../' + stateful global-regex test) plus path.join with an absolute segment allows path traversal. http://38.47.176.164:4852/"
attachments:
  - { name: index.js, path: /files/web/peep/index.js }
tags: [web, path-traversal, nodejs]
---

## Overview

We are given a simple web service called PEEP, described as "the more you click, the more you win." The challenge implicitly nudges players to look for a shortcut instead of clicking forever:

```
http://38.47.176.164:4852/
```

## Analysis

From the project structure and the `index.js` code, the Node.js server exposes two dynamic endpoints (`/click` and `/clicks`) plus a static handler that reads files from the `static` folder.

The static handler contains a "path sanitization" attempt that looks naive:

- The `clean` function only removes the substring `'../'` using `replace` once per call.
- It then decides whether to recurse based on `regex.test`, using a global regex `/\.\.\//g`.

The combination of these two behaviors is the flaw:

- `replace` only removes the first occurrence.
- `test` on a global regex is stateful — the regex keeps a `lastIndex` between calls, so successive tests do not restart from the beginning of the string.

Together these create a gap where certain traversal patterns slip through the sanitizer.

Worse, the result of `clean(req.url)` is passed straight into:

```js
path.join(__dirname, 'static', ...)
```

If the third segment is an absolute path (starting with `/`), `path.join` discards the `__dirname` and `'static'` prefixes entirely, so the read escapes the static folder.

## Exploitation

Understanding these two characteristics, we can build a payload that contains no straight literal `../` yet still "collapses" into an absolute path to root after the cleaning and normalization performed by the system.

The effective trick is to use overlapping "double-dot" segments such as a repeated `....//`. The `../` matcher only removes part of each dot-slash pair, leaving a run of double slashes, which on POSIX systems are treated as a single slash. The remaining absolute path then points directly at the target file at the root of the container filesystem.

On the challenge instance it is enough to request the following path from the server:

```
http://38.47.176.164:4852/....//....//flag.txt
```

The response comes back with status 200 and contains the flag. This shows that the path sanitization fails to prevent traversal to root, while `path.join` gives an absolute path a way to ignore the `static` base directory.

## Why the sanitizer is broken

Conceptually, the weakness has two sides: fragile sanitization, and path joining that trusts absolute input.

- Correct sanitization should normalize the path deterministically (for example with `path.normalize`), reject any path that escapes the allowed directory by validating the final resolved path against a pinned root, and avoid using a stateful global regex for security logic.
- When relying on `path.join`, the server must reject the result if the joined value is an absolute path, or if the final resolved path does not live under the `static` directory.

With those mitigations in place, a payload like `....//....//flag.txt` could no longer escape the static directory sandbox and read sensitive files such as `flag.txt` at the container root.

## Flag

```
Teknocom{Oops_Found_Your_Silly_Fl4g_Haha}
```
