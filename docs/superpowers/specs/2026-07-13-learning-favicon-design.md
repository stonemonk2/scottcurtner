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
