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

`stonemonk2/scottcurtner-wiki` is a **private** repo. There are exactly two
paths to it and one impostor.

**1. Primary — Open Brain MCP.** Read
`scottcurtner-website-publish-protocol.md` via the `read_wiki` tool.
This is the normal case. If it loads, **it is authoritative** — follow it
for all execution steps.

**2. Secondary — `gh` CLI.** If the MCP tool is unreachable, this reads the
same file from the same repo and is equally authoritative:

```bash
gh api repos/stonemonk2/scottcurtner-wiki/contents/scottcurtner-website-publish-protocol.md   -H "Accept: application/vnd.github.raw"
```

`gh` is authenticated as `stonemonk2` with `repo` scope (verified
2026-08-23). Run `gh auth status` if this fails.

**3. If BOTH fail — STOP. Alert Scott. Execute nothing.**

Scott's instruction, 2026-08-23: *"the MCP tool for the wiki should always
be reachable, and if not, I should be alerted that I need to fix it."*

An unreachable wiki is a tooling defect he wants to hear about
immediately, not a condition to route around. Report which path failed and
what the error was, then wait. **The Fallback Protocol below may only be
executed with his explicit go-ahead in that session** — it is a
stale-by-construction copy of a control standard.

> **Do not use `https://raw.githubusercontent.com/stonemonk2/scottcurtner-wiki/...`.**
> The repo is private, so that URL returns `404: Not Found` to any
> unauthenticated request. It was this skill's documented fallback for
> months and could never have worked — it was never exercised, because the
> primary path never failed. Found 2026-08-23. A fallback that has never
> been exercised is not known to work.

Log which path supplied the protocol:

```
[WIKI] Protocol loaded via: read_wiki | gh api | HALTED
```

Then run the divergence check and log it:

```
[CHECK] Skill fallback vs wiki alignment:
        Wiki loaded: YES / NO
        Match: YES / NO
        If NO — [list each step that differs]
```

`gh api` counts as `Wiki loaded: YES` — same file, same repo, different
transport.

## Inputs

```
- Title:       [article title]
- URL:         https://www.scottcurtner.com/articles/[slug]/
- Description: [one sentence — must match the page's meta description exactly]
- File:        articles/[slug]/index.html
```

## Fallback Protocol

> **Requires Scott's explicit go-ahead this session.** Reaching this
> section means both wiki paths failed — see Step 0. Do not execute it
> because the wiki was slow.

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
connect link before `</body>`; site-entity JSON-LD on the homepage only (`Person`
plus `WebSite` — verify, don't re-add); FAQ JSON-LD if the post has a quick-answer
dek (`[SKIP]` with reason if not). `[WARN]` anything not auto-fixable.

> Schema used to be the one item on this list that nothing verified, so the
> `[DONE] SEO check` line asserted it exactly the way the old log asserted
> surfaces. As of 2026-08-08 `check_site.py`'s `seo` group proves it: the
> homepage carries a `Person` or `Organization` node, every JSON-LD block
> parses, and any page with a quick-answer dek has FAQ schema whose question
> is the same sentence as the dek heading.

**6. robots.txt** — confirm `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`,
`Claude-User`, `PerplexityBot`, `Perplexity-User` all still carry `Allow: /`,
and every group still disallows the verification file. This file is
security-adjacent: if a fix is needed, **draft it and get Scott's approval
before writing** — do not edit silently.

## Execution hazard — the guard that always passes

If you script the surface edits with a "skip if already present" guard,
**guard on the article's canonical URL, never on the first line of the
block you are inserting.**

```python
marker = new.strip().split('
')[0]   # WRONG — '<url>' / '## Writing'
marker = url                          # RIGHT — unique to this article
```

On 2026-08-18 the wrong version reported `SKIP` for sitemap.xml and
llms.txt on a **first** run, and neither file was written. **A `SKIP` on a
first publish run is a defect until proven otherwise** — every surface
step must report a write. Step 7 catches it, but read your own stdout
first.

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
[WIKI] Protocol loaded via: read_wiki | gh api | HALTED
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
