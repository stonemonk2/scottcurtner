# Learning Section Design

Date: 2026-07-03
Status: Approved by Scott, ready for implementation planning

## Context

Scott has started building a personal AI/agentic-systems curriculum under
`learning/agentic-operations/`, driven by a private teaching-agent process
(`MISSION.md`, `NOTES.md`, `RESOURCES.md`) built around an external "Agentic
Operations Knowledge Map" rubric (a four-stage maturity ladder, M1–M4, gated
on demonstrated capability).

As of this revision, Scott has written the **full mental-model spine**: one
intro lesson per level (`0001` = Level 1, `0002` = Level 2, `0003` = Level 3,
`0004` = Level 4 — lesson numbers are workspace-sequential, not per-level),
plus a matching vocabulary reference page per level (`m1`–`m4-core-vocabulary.html`).
He requested Levels 2–4 material unlocked ahead of their gates, recorded in
`learning-records/0001-m2-unlocked-by-request.md` and
`learning-records/0002-full-map-unlocked.md`. Each level still has several
hands-on practice lessons planned in `NOTES.md` that don't exist as files
yet, ending in a gated "readiness check" lesson per level.

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
- No stub pages / dead links for unwritten practice lessons. They appear as
  plain non-linked list items until they exist.
- No public surfacing of `learning-records/` — tidy the language for a public
  repo, but don't link them from any page.
- No build tooling, no Jekyll config changes — stays pure static HTML.

## Architecture

```
learning/
  index.html                              NEW — hub (lists courses)
  agentic-operations/
    index.html                            NEW — course landing page
    lessons/
      0001-not-in-context-doesnt-exist.html       EDIT — copy tidy + breadcrumb
      0002-match-the-pattern-to-the-problem.html  EDIT — copy tidy + breadcrumb
      0003-traces-before-prompts.html              EDIT — copy tidy + breadcrumb
      0004-own-the-feedback-loop.html               EDIT — copy tidy + breadcrumb
    reference/
      m1-core-vocabulary.html                 EDIT — copy tidy + breadcrumb
      m2-core-vocabulary.html                 EDIT — copy tidy + breadcrumb
      m3-core-vocabulary.html                 EDIT — copy tidy + breadcrumb
      m4-core-vocabulary.html                 EDIT — copy tidy + breadcrumb
    learning-records/
      0001-m2-unlocked-by-request.md           EDIT — tidy language, stays unlinked
      0002-full-map-unlocked.md                EDIT — tidy language, stays unlinked
    MISSION.md, NOTES.md, RESOURCES.md         EDIT — reword for public repo
```

No files move. Two new landing pages are added; the rest get copy-only edits.

## Page content

### `learning/index.html` (hub)

- Kicker "Scott Curtner · Learning"; H1 "Learning"; lede along the lines of
  "Structured, hands-on courses on AI and agent-building — built and
  published as I go."
- One course card (styled in the section's own paper/serif visual language,
  echoing the main site's `.article-card` pattern): **Agentic Operations**,
  one-line description, status tag ("4-level spine complete, hands-on
  practice in progress"), links to the course landing page.
- A small link back to the main site.

### `learning/agentic-operations/index.html` (course landing page)

- Kicker "Learning · Agentic Operations"; H1 "Agentic Operations"; lede
  "Learn to build AI agents, one real concept at a time."
- Short "how this course works" paragraph: four levels, each gates on
  demonstrated capability (explain it back + a working exercise), not just
  reading; nudge to keep your own AI assistant open alongside the lessons.
- **Roadmap, in two parts**, reflecting the real structure (lessons
  0001–0004 are one intro lesson per level, not four Level-1 lessons):
  - **"Start here" — the mental-model spine**: the 4 written lessons in
    reading order, each tagged with its level, all real links:
    - ✓ 0001 Not in Context = Doesn't Exist (Level 1)
    - ✓ 0002 Match the Pattern to the Problem (Level 2)
    - ✓ 0003 Traces Before Prompts (Level 3)
    - ✓ 0004 Own the Feedback Loop (Level 4)
  - **Per-level practice sections**, one per level, each listing that
    level's planned hands-on lessons (titles pulled from `NOTES.md`) as
    plain muted non-link text until written, ending in that level's gated
    "readiness check" lesson:
    - **Level 1 · Foundations** — Tokens & Cost; Anatomy of a Tool Call;
      Ship the Single-Tool Agent; Break It on Purpose *(gate)*
    - **Level 2 · Developing** — Structured Prompting & Instruction
      Hierarchy; Prompt-Injection Lab; Build the ReAct Multi-Hop Agent;
      Build a Small RAG Pipeline; Episodic Memory *(gate)*
    - **Level 3 · Advanced** — Run Lifecycle & Durability; Orchestrator
      Build; Tracing Instrumentation + Eval Set; Critic/Verifier Step
      *(gate)*
    - **Level 4 · Operational Leadership** — SLO Definition + Dashboard;
      Guardrails & Least Privilege; HITL Checkpoint Policy; Full
      Improvement Cycle *(gate)*
- Each level's card links to its vocabulary reference, labeled "Level N
  Vocabulary" in visible link text (filenames stay `m1`–`m4-core-vocabulary.html`).

### Edits to all four lessons and all four reference pages

- Replace visible "M1 Foundational" / "M2 Developing" / "M3 Advanced" /
  "M4 Operational Leader" copy in kickers/headers with "Level 1 ·
  Foundations" / "Level 2 · Developing" / "Level 3 · Advanced" / "Level 4 ·
  Operational Leadership". The M-numbering stays as-is in the private
  MISSION.md/rubric and in filenames — this is a reader-facing label swap
  only.
- Add a breadcrumb line at the top of each (`Learning / Agentic Operations
  / Lesson 0001`, etc., and equivalent for each reference page) linking
  back to the course page and hub. The existing "Sister lessons" cross-links
  between 0001↔0002↔0003↔0004 already work and stay as-is.
- Drop the raw `docs/inbox/2026-07-03/...` rubric citation from each public
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
- **learning-records/0001 and 0002**: light language tidy only (these stay
  unlinked from any public page per Scott's decision — repo-only artifacts,
  not part of the published course).

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
- Click through the full path: main site nav → hub → course page → each of
  the 4 lessons → each of the 4 reference pages → back links all round-trip
  correctly, including the existing sister-lesson cross-links.
- Confirm all not-yet-written practice lessons render as inert text, not
  broken links.
- Confirm `learning-records/` files are not linked from any HTML page.
- Validate `sitemap.xml` is well-formed XML after edits.
