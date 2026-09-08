# Design: Learning-section favicon

**Date:** 2026-07-13 · **Approved by:** Scott (conversation)

## Why

The 25 learning pages are the only section of scottcurtner.com with no favicon.
Every other page embeds one as an inline SVG data-URI (most: navy "SC" monogram).

## Decision

A learning-specific icon — Scott chose the **learning symbol** option over reusing
the SC monogram: 32×32 rounded square (`rx=6`) filled terracotta `#a5402d` (the
learning palette's accent), with a filled open-book glyph in cream `#fdfbf5` (two
page panels meeting at a center spine, plus a thin terracotta spine line for
legibility at 16px). Encoded as an inline `data:image/svg+xml` URI following the
site's existing convention (`%3C`/`%3E`/`%23` encoding, single quotes) — no image
files.

## Placement

One identical line added to the `<head>` of all 25 learning pages (2 indexes,
18 lessons, 5 reference pages), inserted immediately after the viewport meta:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,…">
```

## Side effect

`scripts/check_learning_links.py` must skip `data:` hrefs (its skip list covers
only http/https/mailto/#; without the fix, the new links would misparse as
relative paths → 25 false broken-link failures). One-line change to the skip
tuple.

## Out of scope

Pre-existing favicon inconsistencies outside learning/: three article pages
reference nonexistent `/favicon.png` / `/favicon.ico`; two use one-off emoji
icons.

## Verification

Checker fully green (with the skip fix); grep asserts exactly 25 learning pages
carry the identical icon line; visual tab check by Scott after publish.

---

## Superseded in part — 2026-09-08

**The design decision stands. The encoding does not.**

The terracotta open book is still the learning section's icon, and reusing the
SC monogram here is still the wrong answer. What changed is where it lives: the
inline `data:image/svg+xml` URI specified above — "no image files" — is exactly
what prevents Google Search from displaying a favicon, because a data URI has no
stable, independently crawlable URL. Google requires a real square file that is
a multiple of 48x48.

All 25 learning pages now carry four links to hosted files instead:

```html
<link rel="icon" href="/favicon-learning.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon-learning.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-learning-48x48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-learning-192x192.png">
```

The files are generated from `favicon-learning.svg` — the same geometry and the
same two colours, transcribed from the data URI above — by
`scripts/gen_favicons.ps1`, which also builds the sitewide `favicon.*` set.

**The `data:` skip in `check_learning_links.py` is now dead weight for this
case** and can stay or go; the new hrefs are ordinary root-relative paths, which
means the link checkers now *prove the icon files exist*. The old encoding could
not be verified against disk at all — that is the second thing this fixes.

`check_site.py` gained a `check_favicon()` control the same day: it fails any
page whose favicon is a data URI, and it knows that `learning/` takes the
`favicon-learning` prefix, so a well-meaning consistency sweep that points these
pages at the monogram is now a build failure rather than a silent loss.
