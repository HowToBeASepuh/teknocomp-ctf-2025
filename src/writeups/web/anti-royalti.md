---
layout: challenge.njk
title: Anti Royalti
category: Web
author: faizath
flag: "Teknocom{L1st3n1ng_t0_Mus1c_1s_Fr33_Dud3_G0v_D03s_N0th1ng_4nym0r3}"
flagTeaser: "Teknocom{L1st3n1ng_t0_Mus1c...}"
description: "A Flask playlist app renders the username with the |safe filter and re-renders a stored HTML file — a stored Server-Side Template Injection (SSTI)."
tags: [web, ssti, jinja2, flask]
---

## Overview

We are given a Flask web application that lets users build music playlists:

```
http://38.47.176.164:4111/
```

The application exposes several interesting endpoints: a main page for creating a playlist, an endpoint for processing the playlist that was created, and an endpoint for viewing a playlist that already exists.

## Analysis

Reviewing the source code reveals a fairly serious vulnerability. The `/create_playlist` endpoint accepts user input in the form of a `username` and a `text` field. What is interesting is how the application handles the `username` input. Inside the `playlist.html` template, the username is rendered through the `|safe` filter, which means the input is not escaped and can execute HTML or template code.

The core of the vulnerability lies in the application's workflow:

1. When a user creates a playlist, the application renders the `playlist.html` template with the supplied data and then saves the rendered output as an HTML file in the `templates/uploads/` directory.
2. That file can later be accessed through the `/view_playlist/<uuid>` endpoint, which re-renders the stored HTML file.

The problem is that when the already-rendered HTML file is saved, any template injection payload placed in the username is stored in its raw form. Later, when that file is rendered again through `/view_playlist`, the payload is executed as a Jinja2 template, giving us the ability to run Python code on the server. This is a stored Server-Side Template Injection (SSTI).

## Exploitation

To exploit this, we craft an SSTI payload that will be executed when the stored HTML file is re-rendered. The payload used is:

```jinja2
{{ config.__class__.__init__.__globals__['os'].popen('cat flag.txt').read() }}
```

This reads the `flag.txt` file from the server's directory.

The exploitation process is as follows:

1. Send a POST request to `/create_playlist` with the SSTI payload in the `username` field. The application processes the request and returns a page containing a link to view the newly created playlist. That link points to `/view_playlist/<uuid>`, where the SSTI payload will be executed.
2. Access that link. The application renders the stored HTML file and executes the SSTI payload, which runs the `cat flag.txt` command on the server and displays its output on the web page. The output is the contents of the flag file.

The exploit succeeds because the application does not adequately sanitize the `username` input, uses the `|safe` filter that permits template code execution, and stores and re-renders a previously rendered HTML file, which allows the payload to be persisted and executed on the second render.

## Flag

```
Teknocom{L1st3n1ng_t0_Mus1c_1s_Fr33_Dud3_G0v_D03s_N0th1ng_4nym0r3}
```
