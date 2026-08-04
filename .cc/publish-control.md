---
# publish-control — MIGRATED 2026-08-04

This protocol has moved. Do not execute the steps that used to live here.

## Use instead

**`/publish`** — the skill at `.claude/skills/publish/SKILL.md`, tracked in
git and available on every machine after a `git pull`. Same two-agent loop,
same wiki-first-with-fallback design, plus mechanical verification.

## What changed

1. **`articles/index.html` is now a required surface.** The old protocol
   covered `sitemap.xml`, `llms.txt`, and the homepage — never the `/articles/`
   hub. Three published articles silently fell off it. The skill updates it as
   step 4.

2. **`[DONE]` is now verified, not asserted.** Every run ends with
   `python scripts/check_site.py`, which reads the filesystem and checks each
   surface, SEO tag, internal link, and robots.txt group. A step is not done
   until the checker confirms it. Claude chat validation still runs, but it
   judges the writing, not the bookkeeping.

3. **The wiki is unchanged as the authority.** It gained the hub step and the
   verification step; the divergence check in the skill still compares against
   it on every run.

## If you are somewhere without skill support

The checker is plain stdlib Python and runs anywhere, from any directory:

```bash
python scripts/check_site.py
```

Exit 0 means every article on disk is present on every metadata surface with
valid tags. Exit 1 lists exactly what is missing. Fix, re-run, then publish.

The authoritative protocol text is always the wiki:
`https://raw.githubusercontent.com/stonemonk2/scottcurtner-wiki/main/scottcurtner-website-publish-protocol.md`
