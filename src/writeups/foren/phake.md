---
layout: challenge.njk
title: phake
category: Foren
author: faizath
flag: "Teknocom{y0u_4ctu4lly_f0und_1t_lol}"
flagTeaser: "Teknocom{y0u_4ctu4lly_f0und...}"
description: "“Something valuable is hidden. Will you discover it?” A pcap where an HTTP object carries the flag as application/octet-stream."
attachments:
  - { name: chall.pcap, path: /files/foren/phake/chall.pcap }
tags: [forensics, pcap, wireshark, http]
---

## Overview

We are given a file `chall.pcap` containing several network transactions. The challenge hint is:

> "Something valuable is hidden. Will you discover it?"

## Analysis

The file can be opened with Wireshark. Filtering the list of transmissions by `http` narrows the capture down to the HTTP traffic.

Scrolling through the filtered list, the 90th transmission stands out: a PHP file returns the flag with the content type `application/octet-stream`. Inspecting that HTTP object reveals the flag in the response body.

## Flag

```
Teknocom{y0u_4ctu4lly_f0und_1t_lol}
```
