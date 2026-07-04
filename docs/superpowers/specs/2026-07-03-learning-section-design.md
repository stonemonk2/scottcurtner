# Learning Section Design

Date: 2026-07-03
Status: Approved by Scott, ready for implementation planning

## Context

Scott has started building a personal AI/agentic-systems curriculum under
`learning/agentic-operations/`, driven by a private teaching-agent process
(`MISSION.md`, `NOTES.md`, `RESOURCES.md`) built around an external "Agentic
Operations Knowledge Map" rubric (a four-stage maturity ladder, M1–M4, gated
on demonstrated capability). One lesson (`0001-not-in-context-doesnt-exist.html`)
and one reference page (`m1-core-vocabulary.html`) already exist and work.

Scott wants this to become a real public section of scottcurtner.com — a
self-serve course, not just a personal log — while keeping the existing
lesson content and mechanics (quizzes, own-words rubric gate) intact.

## Goals

- Publish `/learning/` as a hub that can hold multiple courses over time
  (only "Agentic Operations" exists today).
- Give the Agentic Operations course a proper landing page showing the
  planned lesson roadmap, not just a bare lesson file.
- Soften the internal M1–M4/gate jargon into public-friendly "Level 1–4"
  language on anything a reader sees, without touching the private rubric
  mapping Scott uses internally.
- Keep the section's existing warm/paper visual identity (Georgia serif,
  cream background, rust-orange accent) distinct from the main site's
  navy/DM Sans corporate branding.
- Surface the section from the main site nav.
- Tidy the internal working docs so they read fine if a visitor finds them
  on GitHub, without stripping out the "here's my process" transparency
  that fits Scott's other writing (e.g. the publish-control article).

## Non-goals

- No embedded chat/tutor agent on the pages — lessons assume the reader
  brings their own AI assistant (Claude, ChatGPT, etc.) alongside, as the
  existing footer copy already suggests.
- No restyle of the main site, and no restyle of the lesson/reference pages
  beyond copy edits (kicker text, breadcrumbs, footer).
- No stub pages / dead links for unwritten lessons (0002–0005). They appear
  as plain non-linked list items until they exist.
- No build tooling, no Jekyll config changes — stays pure static HTML.

## Architecture

```
learning/
  index.html                              NEW — hub (lists courses)
  agentic-operations/
    index.html                            NEW — course landing page
    lessons/
      0001-not-in-context-doesnt-exist.html   EDIT — copy tidy + breadcrumb
    reference/
      m1-core-vocabulary.html                 EDIT — copy tidy + breadcrumb
    MISSION.md, NOTES.md, RESOURCES.md         EDIT — reword for public repo
```

No files move. Two new landing pages are added; three existing files get
copy-only edits.

## Page content

### `learning/index.html` (hub)

- Kicker "Scott Curtner · Learning"; H1 "Learning"; lede along the lines of
  "Structured, hands-on courses on AI and agent-building — built and
  published as I go."
- One course card (styled in the section's own paper/serif visual language,
  echoing the main site's `.article-card` pattern): **Agentic Operations**,
  one-line description, status tag ("Level 1 in progress"), links to the
  course landing page.
- A small link back to the main site.

### `learning/agentic-operations/index.html` (course landing page)

- Kicker "Learning · Agentic Operations"; H1 "Agentic Operations"; lede
  "Learn to build AI agents, one real concept at a time."
- Short "how this course works" paragraph: leveled, each level gates on
  demonstrated capability (explain it back + a working exercise), not just
  reading; nudge to keep your own AI assistant open alongside the lessons.
- Roadmap section: **Level 1 · Foundations — in progress**, listing all 5
  planned lessons with ✓/○ status. Only lesson 0001 is a real link;
  0002–0005 render as plain muted (non-link) text until written.
- One line acknowledging Levels 2–4 exist as a planned arc (structured
  prompting/RAG, memory, multi-agent, evals — per NOTES.md) without
  overpromising specifics or dates.
- Link to the vocabulary reference, labeled "Level 1 Vocabulary" in visible
  link text (filename stays `m1-core-vocabulary.html`).

### Edits to `0001-not-in-context-doesnt-exist.html` and `m1-core-vocabulary.html`

- Replace visible "M1 Foundational" copy in kickers/headers with
  "Level 1 · Foundations". The M-numbering stays as-is in the private
  MISSION.md/rubric — this is a reader-facing label swap only.
- Add a breadcrumb line at the top (`Learning / Agentic Operations / Lesson
  0001`, and equivalent for the reference page) linking back to the course
  page and hub.
- Drop the raw `docs/inbox/2026-07-03/...` rubric citation from the public
  footer (it points outside the repo and means nothing to a reader);
  replace with "Part of the Agentic Operations course" linking to the
  course landing page.

## Working-doc tidy-ups

- **NOTES.md**: reword "Open questions to confirm with Scott" → "Open
  questions" (drop second-person address). Keep the actual content —
  learner profile, planned lesson arc — since it's legitimate "here's the
  process" material.
- **MISSION.md**: add a one-line note that the `docs/inbox/2026-07-03/...`
  path is a private source doc, not a public link, so it doesn't read as a
  mysterious dead citation.
- **RESOURCES.md**: same fix — turn the `../../inbox/...` markdown link to
  the rubric doc into plain text (still cites it, just not a clickable
  404).

## Site integration & mechanics

- Add "Learning" to the main nav in `index.html`: About · Experience ·
  Credentials · Writing · **Learning** · Connect → `/learning/`.
- Add the hub, course page, lesson, and reference URLs to `sitemap.xml` and
  `llms.txt`, matching the existing article entries' format.
- Apply the site's existing SEO conventions (canonical tag, OG tags, title
  tag) to the two new pages, consistent with the recent SEO audit commit.
- No `.nojekyll` or other build changes.

## Testing / verification

- Open each new/edited page directly in a browser; confirm nav links,
  breadcrumbs, and the lesson-status roadmap render correctly in both light
  and dark color schemes (the existing pages already use
  `prefers-color-scheme` — new pages must match).
- Click through the full path: main site nav → hub → course page → lesson
  0001 → reference page → back links all round-trip correctly.
- Confirm 0002–0005 are inert text, not broken links.
- Validate `sitemap.xml` is well-formed XML after edits.
