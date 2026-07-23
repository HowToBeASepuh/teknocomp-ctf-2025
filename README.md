# TeknoCom 2025 CTF — HowToBeASepuh Write-Ups

English write-ups for the **Cyber Security (CTF) branch of the TeknoCom International Competition
2025** (hosted by Universitas Teknokrat Indonesia), by team **HowToBeASepuh** (Institut Teknologi
Bandung) — 3rd place. Built as a static site with [Eleventy (11ty)](https://www.11ty.dev/).

## Challenges

| Category | Challenges |
|----------|-----------|
| Rev      | Reversify, Ba1ted, Overfit |
| Pwn      | Lomgin, Stacktrip |
| Web      | Betting, Anti Royalti, PEEP |
| Foren    | phake |
| Crypto   | ARX, King Caesar, PrimeSum, Pailliiered, Sqrt Madness |
| Misc     | Baby Pyjail, Enigma |

## Local development

```bash
npm install
npm start        # dev server at http://localhost:8080
npm run build    # build static site into _site/
```

## Project layout

```
description.txt          Competition blurb (source of truth, shown on the home page)
.source/                 Original challenge files + source PDF write-up (archival)
eleventy.config.js       Eleventy config (ESM)
src/
  _data/site.js          Site metadata; reads description.txt
  _data/authors.js       Team-member author registry (avatar + GitHub)
  _includes/             base.njk (shell) + challenge.njk (write-up layout)
  assets/                style.css, prism.css, theme.js
  index.njk              Landing page + challenge index grouped by category
  writeups/<cat>/*.md    One markdown file per challenge
  files/<cat>/<chall>/   Downloadable challenge attachments
```

Note: the Forensics challenge `phake` ships the original `chall.pcap`; the thousands of
Wireshark-exported HTTP objects in `.source/Foren/phake/http-objects/` are intentionally not bundled.
