---
name: publish
description: Execute the scottcurtner.com publish protocol for a new article — update sitemap.xml, llms.txt, the homepage Writing section, and the /articles/ hub, verify SEO tags and robots.txt, then prove it with scripts/check_site.py. Use when publishing or releasing an article, or when asked to run the publish control.
argument-hint: "[article slug or title]"
---

# scottcurtner.com — Publish Control

Executes all dependency updates for a new article, then **verifies them
mechanically** and produces a structured log. Runs the same on any machine.

The wiki is the authority. This file is the fallback and the runner.

## Step 0 — Load protocol from wiki

Read `scottcurtner-website-publish-protocol.md` via the Open Brain MCP
`read_wiki` tool, or from
`https://raw.githubusercontent.com/stonemonk2/scottcurtner-wiki/main/scottcurtner-website-publish-protocol.md`.

If it loads, **it is authoritative** — follow it for all execution steps.
If unreachable, log this and execute the Fallback Protocol below:

```
[FALLBACK] Wiki unreachable — executing hardcoded fallback protocol.
           Reason: [error or timeout]
```

Either way, run the divergence check and log it:

```
[CHECK] Skill fallback vs wiki alignment:
        Wiki loaded: YES / NO
        Match: YES / NO
        If NO — [list each step that differs]
```

## Inputs

```
- Title:       [article title]
- URL:         https://www.scottcurtner.com/articles/[slug]/
- Description: [one sentence — must match the page's meta description exactly]
- File:        articles/[slug]/index.html
```

## Fallback Protocol

Execute without asking for confirmation. All six steps must appear in the log.
A silent omission is a protocol failure.

**1. sitemap.xml** — add a `<url>` entry: `<loc>` canonical URL, `<lastmod>`
today YYYY-MM-DD, `<changefreq>` monthly, `<priority>` 0.8 (1.0 for the
homepage only). Never list `google3daeab9f4ca3935f.html`.

**2. llms.txt** — add under `## Writing`, newest-first, format
`- [Title](URL): Description.` Description matches the meta description exactly.

**3. index.html — Writing section** — add a card at position 1:

```html
<a href="articles/[slug]/" class="article-card">
  <div>
    <div class="article-date">Month YYYY · scottcurtner.com</div>
    <div class="article-title">[Article title]</div>
    <div class="article-excerpt">[Meta description, exactly]</div>
  </div>
  <div class="article-arrow">→</div>
</a>
```

**4. articles/index.html — the hub** — add the same card at position 1, but
with `href="[slug]/"` (relative to `/articles/`) and two-space indentation to
match the surrounding cards.

> Three articles drifted out of the hub because no version of this protocol
> named it. It is a required surface, not an optional one.

**5. New page SEO check** — confirm present, add if missing: `<link
rel="canonical">` first in `<head>`; `<meta name="description">` under 160
chars; `<title>` under 60; `og:title`, `og:description`, `og:url`, `og:type`;
`og:image` (absolute URL, if a hero image exists in `articles/[slug]/images/`
— `[WARN]` if not); inline SVG favicon; a footer block carrying the LinkedIn
connect link before `</body>`; Organization JSON-LD on the homepage only (verify,
don't re-add); FAQ JSON-LD if the post has a quick-answer dek (`[SKIP]` with
reason if not). `[WARN]` anything not auto-fixable.

**6. robots.txt** — confirm `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`,
`Claude-User`, `PerplexityBot`, `Perplexity-User` all still carry `Allow: /`,
and every group still disallows the verification file. This file is
security-adjacent: if a fix is needed, **draft it and get Scott's approval
before writing** — do not edit silently.

## Step 7 — Verify (required)

```bash
python scripts/check_site.py
```

Stdlib only, no venv, runs from any directory. It reads the filesystem as the
source of truth and checks every surface, every SEO tag, every link, and
robots.txt.

**A step is not done until the checker says so.** If it exits non-zero, fix
what it reports and run it again. Never write `[DONE]` against a step the
checker did not confirm — that is the failure mode this replaces. Paste the
real tail of its output into the log.

Warnings do not block publishing. Report them; let Scott decide.

## Output log

```
PUBLISH RUN — [YYYY-MM-DD] — [Article Title]
[FALLBACK] ... (only if it fired)
[CHECK] Skill fallback vs wiki alignment: Wiki loaded: Y/N  Match: Y/N
[DONE] sitemap.xml — added [URL], lastmod [date]
[DONE] llms.txt — added entry under ## Writing
[DONE] index.html — card added at position 1
[DONE] articles/index.html — hub card added at position 1
[DONE] SEO check — canonical, OG tags, favicon, meta description,
       connect footer, Organization + FAQ schema
[DONE] robots.txt — AI search crawlers confirmed allowed
[VERIFIED] check_site.py — PASS, 0 violations, [n] warning(s)
[WARN]  [anything flagged but not auto-fixed]
```

Then prompt Scott:

> Paste this log into Claude chat and say:
> "Validate CC publish log against wiki protocol"

Chat's job is now the judgment layer — does the excerpt represent the piece,
is the framing right, is the description honest. The mechanical facts are
already settled by step 7.

## Post-publish (manual, not executable here)

- Commit `Publish: [article title]` and push to main
- Verify live: fetch the URL and sitemap.xml, confirm render + lastmod
  (a green push can still 404 until Pages finishes deploying)
- Search Console: resubmit sitemap (optional nudge)
- LinkedIn: test the URL unfurl before sharing
- Update `blog-pipeline.md` Published Articles table
- LinkedIn packaging per `blog-content-development.md`
