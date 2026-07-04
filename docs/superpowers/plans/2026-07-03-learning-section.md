# Learning Section Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `/learning/` as a public section of scottcurtner.com: a course hub, an Agentic Operations course landing page showing the real four-level spine + practice roadmap, softened public-facing copy on the existing lesson/reference pages, tidied working docs, and a main-site nav link — per `docs/superpowers/specs/2026-07-03-learning-section-design.md`.

**Architecture:** Pure static HTML/CSS, no build tooling — matches the rest of the site. Two brand-new pages (`learning/index.html` hub, `learning/agentic-operations/index.html` course landing page) reuse the warm paper/serif visual language already established in the existing lesson pages (`--paper`/`--ink`/`--muted`/`--accent`/`--rule`/`--card` CSS custom properties, Georgia serif body, system-ui sans-serif kickers/headings). The 4 existing lessons and 4 existing reference pages get small, surgical copy edits (kicker relabel, breadcrumb, footer citation swap) — their quiz/rubric JS and CSS are untouched. Internal working docs get light language tidy for a public repo. The main site gets one nav link.

**Tech Stack:** HTML5, CSS3 (no JS frameworks), Git Bash (`grep`, `test -f`, `python -c` for XML validation).

## Global Constraints

- No embedded chat/tutor agent — lessons assume the reader's own AI assistant, unchanged from current copy.
- No restyle of the main site (`index.html`'s navy/DM Sans branding stays untouched beyond the one nav link).
- No restyle of existing lesson/reference pages beyond copy edits (kicker text, breadcrumb, footer) — do not touch their `<style>` blocks, quiz JS, or content sections.
- Reuse existing CSS custom properties (`--paper`, `--ink`, `--muted`, `--accent`, `--rule`, `--card`, plus `--good` where a "done" checkmark color is needed) in both new pages — do not invent a new palette.
- Unwritten practice lessons render as plain non-link text (`<span class="pending">`) — never a placeholder `href`.
- `learning-records/0001-m2-unlocked-by-request.md` and `learning-records/0002-full-map-unlocked.md` must not be linked from any HTML page.
- Use root-absolute `/` links only for "back to main site" links; use relative paths (`../`, `../../`) for everything inside the `learning/` subtree.
- Filenames and internal M1–M4 labels in `MISSION.md`/`NOTES.md`/`RESOURCES.md` and in file paths (`m1-core-vocabulary.html`, etc.) stay as-is — only reader-facing copy (kickers, headers, footers, new pages) uses "Level 1–4" language.
- Stage changes with `git add <exact files>` (never `git add -A`), commit after every task.

---

### Task 1: Learning hub page

**Files:**
- Create: `learning/index.html`

**Interfaces:**
- Produces: page at path `/learning/`, containing a link `href="agentic-operations/"` to the course landing page (consumed by Task 8's nav link and Task 9's sitemap entry).

- [ ] **Step 1: Write the pre-check (expect fail — file doesn't exist yet)**

Run: `test -f "C:/dev/scottcurtner-website/learning/index.html" && echo EXISTS || echo MISSING`
Expected: `MISSING`

- [ ] **Step 2: Create `learning/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://www.scottcurtner.com/learning/" />
<title>Learning | Scott Curtner</title>
<meta name="description" content="Structured, hands-on courses on AI and agent-building, published as I go.">
<meta name="author" content="Scott Curtner">
<meta property="og:title" content="Learning | Scott Curtner">
<meta property="og:description" content="Structured, hands-on courses on AI and agent-building, published as I go.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.scottcurtner.com/learning/">
<style>
  :root {
    --paper: #fdfbf5; --ink: #1f2328; --muted: #6b7075;
    --accent: #a5402d; --rule: #d8d3c8; --card: #f4f0e6;
  }
  @media (prefers-color-scheme: dark) {
    :root { --paper: #16181c; --ink: #d9dce1; --muted: #8b919a;
            --accent: #e07a5f; --rule: #33383f; --card: #1e2126; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--paper); color: var(--ink);
         font-family: Georgia, 'Times New Roman', serif; line-height: 1.6; font-size: 17px; }
  main { max-width: 44rem; margin: 0 auto; padding: 3rem 1.5rem 4rem; }
  .breadcrumb { font-family: system-ui, sans-serif; font-size: .8rem; color: var(--muted); margin: 0 0 1rem; }
  .breadcrumb a { color: var(--muted); }
  .kicker { font-family: system-ui, sans-serif; font-size: .72rem; letter-spacing: .14em;
            text-transform: uppercase; color: var(--muted); margin-bottom: .8rem; }
  h1 { font-size: 2.1rem; font-weight: normal; margin: 0 0 .4rem; line-height: 1.2; }
  .lede { font-style: italic; color: var(--muted); margin-top: 0; }
  a { color: var(--accent); }
  .course-card { display: block; border: 1px solid var(--rule); border-radius: 6px;
                 padding: 1.2rem 1.4rem; margin: 1.6rem 0; text-decoration: none; color: inherit; }
  .course-card:hover { border-color: var(--accent); }
  .course-card h2 { font-family: system-ui, sans-serif; font-size: 1.3rem; font-weight: 600;
                     color: var(--ink); margin: 0 0 .5rem; }
  .course-card p { margin: 0 0 .8rem; color: var(--muted); font-size: .95rem; font-family: Georgia, serif; }
  .status { display: block; font-family: system-ui, sans-serif; font-size: .72rem; letter-spacing: .08em;
            text-transform: uppercase; color: var(--accent); margin-bottom: .5rem; }
  .cta { font-family: system-ui, sans-serif; font-size: .9rem; font-weight: 600; color: var(--accent); }
  footer { margin-top: 3rem; font-size: .85rem; color: var(--muted);
           border-top: 1px solid var(--rule); padding-top: 1rem;
           font-family: system-ui, sans-serif; }
</style>
</head>
<body>
<main>
  <p class="breadcrumb"><a href="/">scottcurtner.com</a> / Learning</p>
  <div class="kicker">Scott Curtner · Learning</div>
  <h1>Learning</h1>
  <p class="lede">Structured, hands-on courses on AI and agent-building — built and published as I go.</p>

  <a class="course-card" href="agentic-operations/">
    <span class="status">4-level spine complete · hands-on practice in progress</span>
    <h2>Agentic Operations</h2>
    <p>Learn to build AI agents, one real concept at a time — from "the context window is the model's entire world" to owning SLOs for a live agent in production.</p>
    <span class="cta">Start the course &rarr;</span>
  </a>

  <footer>
    More courses may appear here over time. Each is self-contained — read, quiz yourself, and bring
    your own AI assistant along for follow-up questions.
  </footer>
</main>
</body>
</html>
```

- [ ] **Step 3: Verify it exists and links correctly**

Run:
```bash
test -f "C:/dev/scottcurtner-website/learning/index.html" && echo EXISTS
grep -q 'href="agentic-operations/"' "C:/dev/scottcurtner-website/learning/index.html" && echo LINK_OK
grep -q '<title>Learning | Scott Curtner</title>' "C:/dev/scottcurtner-website/learning/index.html" && echo TITLE_OK
```
Expected: `EXISTS`, `LINK_OK`, `TITLE_OK` all print.

- [ ] **Step 4: Commit**

```bash
git add learning/index.html
git commit -m "Add Learning hub page"
```

---

### Task 2: Agentic Operations course landing page

**Files:**
- Create: `learning/agentic-operations/index.html`

**Interfaces:**
- Consumes: hub page at `/learning/` (Task 1) as its breadcrumb parent (`../`).
- Produces: page at path `/learning/agentic-operations/`, linking to all 4 existing lessons (`lessons/0001-not-in-context-doesnt-exist.html`, `lessons/0002-match-the-pattern-to-the-problem.html`, `lessons/0003-traces-before-prompts.html`, `lessons/0004-own-the-feedback-loop.html`) and all 4 existing reference pages (`reference/m1-core-vocabulary.html` … `reference/m4-core-vocabulary.html`). Consumed by Tasks 3–6 as the breadcrumb link target (`../`) from lessons/reference pages, and by Task 8's nav link and Task 9's sitemap entry.

- [ ] **Step 1: Write the pre-check (expect fail — file doesn't exist yet)**

Run: `test -f "C:/dev/scottcurtner-website/learning/agentic-operations/index.html" && echo EXISTS || echo MISSING`
Expected: `MISSING`

- [ ] **Step 2: Create `learning/agentic-operations/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://www.scottcurtner.com/learning/agentic-operations/" />
<title>Agentic Operations — Learning | Scott Curtner</title>
<meta name="description" content="A four-level, hands-on course in building AI agents — from the context window as the model's entire world to owning SLOs for a live agent in production.">
<meta name="author" content="Scott Curtner">
<meta property="og:title" content="Agentic Operations — Learning | Scott Curtner">
<meta property="og:description" content="A four-level, hands-on course in building AI agents — from the context window as the model's entire world to owning SLOs for a live agent in production.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.scottcurtner.com/learning/agentic-operations/">
<style>
  :root {
    --paper: #fdfbf5; --ink: #1f2328; --muted: #6b7075;
    --accent: #a5402d; --rule: #d8d3c8; --card: #f4f0e6;
    --good: #2e7d4f;
  }
  @media (prefers-color-scheme: dark) {
    :root { --paper: #16181c; --ink: #d9dce1; --muted: #8b919a;
            --accent: #e07a5f; --rule: #33383f; --card: #1e2126;
            --good: #6fbf8f; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--paper); color: var(--ink);
         font-family: Georgia, 'Times New Roman', serif; line-height: 1.6; font-size: 17px; }
  main { max-width: 44rem; margin: 0 auto; padding: 3rem 1.5rem 4rem; }
  .breadcrumb { font-family: system-ui, sans-serif; font-size: .8rem; color: var(--muted); margin: 0 0 1rem; }
  .breadcrumb a { color: var(--muted); }
  .kicker { font-family: system-ui, sans-serif; font-size: .72rem; letter-spacing: .14em;
            text-transform: uppercase; color: var(--muted); margin-bottom: .8rem; }
  h1 { font-size: 2.1rem; font-weight: normal; margin: 0 0 .4rem; line-height: 1.2; }
  .lede { font-style: italic; color: var(--muted); margin-top: 0; }
  h2 { font-family: system-ui, sans-serif; font-size: .8rem; letter-spacing: .12em;
       text-transform: uppercase; color: var(--accent); font-weight: 600; margin: 2.6rem 0 .9rem; }
  h3 { font-family: system-ui, sans-serif; font-size: 1.05rem; font-weight: 600;
       color: var(--ink); margin: 1.8rem 0 .3rem; }
  a { color: var(--accent); }
  .level-status { font-family: system-ui, sans-serif; font-size: .8rem; color: var(--muted); margin: 0 0 .7rem; }
  ul.roadmap { list-style: none; padding: 0; margin: 0 0 .5rem; font-family: system-ui, sans-serif; font-size: .95rem; }
  ul.roadmap li { padding: .45rem 0; border-bottom: 1px dashed var(--rule); }
  ul.roadmap li:last-child { border-bottom: none; }
  .done { color: var(--good); font-weight: 600; margin-right: .3rem; }
  .pending { color: var(--muted); }
  .pending-mark { color: var(--rule); margin-right: .3rem; }
  .gate-tag { font-size: .78rem; color: var(--accent); margin-left: .3rem; }
  footer { margin-top: 3rem; font-size: .85rem; color: var(--muted);
           border-top: 1px solid var(--rule); padding-top: 1rem;
           font-family: system-ui, sans-serif; }
</style>
</head>
<body>
<main>
  <p class="breadcrumb"><a href="/">scottcurtner.com</a> / <a href="../">Learning</a> / Agentic Operations</p>
  <div class="kicker">Learning · Agentic Operations</div>
  <h1>Agentic Operations</h1>
  <p class="lede">Learn to build AI agents, one real concept at a time.</p>

  <p>This course is four levels, each building on the last. You move on when you can explain the
  idea yourself and the hands-on exercise works — not just when you've read the page. Keep your own
  AI assistant (Claude, ChatGPT, whatever you use) open alongside these lessons; working through
  follow-up questions with it is part of the method, not a detour.</p>

  <h2>Start here — the mental-model spine</h2>
  <p>These four lessons are the spine of the whole course — one per level, best read in order.
  Everything else below is hands-on practice built on top of them.</p>
  <ul class="roadmap">
    <li><span class="done">&#10003;</span><a href="lessons/0001-not-in-context-doesnt-exist.html">0001 — Not in Context = Doesn't Exist</a> <span class="pending">(Level 1)</span></li>
    <li><span class="done">&#10003;</span><a href="lessons/0002-match-the-pattern-to-the-problem.html">0002 — Match the Pattern to the Problem</a> <span class="pending">(Level 2)</span></li>
    <li><span class="done">&#10003;</span><a href="lessons/0003-traces-before-prompts.html">0003 — Traces Before Prompts</a> <span class="pending">(Level 3)</span></li>
    <li><span class="done">&#10003;</span><a href="lessons/0004-own-the-feedback-loop.html">0004 — Own the Feedback Loop</a> <span class="pending">(Level 4)</span></li>
  </ul>

  <h2>The practice ladder</h2>
  <p>Each level's hands-on lessons are still being written. This is the planned arc — check back as
  they ship.</p>

  <h3>Level 1 · Foundations</h3>
  <p class="level-status">Spine lesson done · <a href="reference/m1-core-vocabulary.html">Level 1 Vocabulary</a></p>
  <ul class="roadmap">
    <li><span class="pending-mark">&#9675;</span><span class="pending">Tokens &amp; Cost</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Anatomy of a Tool Call</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Ship the Single-Tool Agent</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Break It on Purpose</span><span class="gate-tag">(gate)</span></li>
  </ul>

  <h3>Level 2 · Developing</h3>
  <p class="level-status">Spine lesson done · <a href="reference/m2-core-vocabulary.html">Level 2 Vocabulary</a></p>
  <ul class="roadmap">
    <li><span class="pending-mark">&#9675;</span><span class="pending">Structured Prompting &amp; Instruction Hierarchy</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Prompt-Injection Lab</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Build the ReAct Multi-Hop Agent</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Build a Small RAG Pipeline</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Episodic Memory</span><span class="gate-tag">(gate)</span></li>
  </ul>

  <h3>Level 3 · Advanced</h3>
  <p class="level-status">Spine lesson done · <a href="reference/m3-core-vocabulary.html">Level 3 Vocabulary</a></p>
  <ul class="roadmap">
    <li><span class="pending-mark">&#9675;</span><span class="pending">Run Lifecycle &amp; Durability</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Orchestrator Build</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Tracing Instrumentation + Eval Set</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Critic/Verifier Step</span><span class="gate-tag">(gate)</span></li>
  </ul>

  <h3>Level 4 · Operational Leadership</h3>
  <p class="level-status">Spine lesson done · <a href="reference/m4-core-vocabulary.html">Level 4 Vocabulary</a></p>
  <ul class="roadmap">
    <li><span class="pending-mark">&#9675;</span><span class="pending">SLO Definition + Dashboard</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Guardrails &amp; Least Privilege</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">HITL Checkpoint Policy</span></li>
    <li><span class="pending-mark">&#9675;</span><span class="pending">Full Improvement Cycle</span><span class="gate-tag">(gate)</span></li>
  </ul>

  <footer>
    Part of <a href="../">Learning</a> on scottcurtner.com.
  </footer>
</main>
</body>
</html>
```

- [ ] **Step 3: Verify it exists and every real link resolves to an existing file**

Run (from repo root `C:/dev/scottcurtner-website`):
```bash
test -f learning/agentic-operations/index.html && echo EXISTS
for f in lessons/0001-not-in-context-doesnt-exist.html lessons/0002-match-the-pattern-to-the-problem.html lessons/0003-traces-before-prompts.html lessons/0004-own-the-feedback-loop.html reference/m1-core-vocabulary.html reference/m2-core-vocabulary.html reference/m3-core-vocabulary.html reference/m4-core-vocabulary.html; do
  test -f "learning/agentic-operations/$f" && echo "OK: $f" || echo "MISSING: $f"
done
grep -q 'href="../"' learning/agentic-operations/index.html && echo HUB_LINK_OK
```
Expected: `EXISTS`, `OK: <each of the 8 paths>`, `HUB_LINK_OK` — no `MISSING` lines.

- [ ] **Step 4: Commit**

```bash
git add learning/agentic-operations/index.html
git commit -m "Add Agentic Operations course landing page"
```

---

### Task 3: Tidy Level 1 public copy (lesson 0001 + reference m1)

**Files:**
- Modify: `learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html`
- Modify: `learning/agentic-operations/reference/m1-core-vocabulary.html`

**Interfaces:**
- Consumes: `/learning/` (Task 1) and `/learning/agentic-operations/` (Task 2) as breadcrumb/footer link targets.

- [ ] **Step 1: Pre-check — confirm old copy present (this should currently succeed)**

Run:
```bash
grep -q "M1 Foundational" "learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html" && echo OLD_KICKER_PRESENT
grep -q "docs/inbox/2026-07-03" "learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html" && echo OLD_FOOTER_PRESENT
grep -q "M1 Foundational" "learning/agentic-operations/reference/m1-core-vocabulary.html" && echo OLD_REF_KICKER_PRESENT
```
Expected: all three print (the old copy is still there).

- [ ] **Step 2: Edit the lesson's kicker and add a breadcrumb**

In `learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html`, replace:

```html
<main>
  <div class="kicker">Agentic Operations · Lesson 0001 · M1 Foundational</div>
  <h1>Not in Context = Doesn't Exist</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0001</p>
  <div class="kicker">Agentic Operations · Lesson 0001 · Level 1 · Foundations</div>
  <h1>Not in Context = Doesn't Exist</h1>
```

- [ ] **Step 3: Edit the lesson's footer**

Replace:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://www.youtube.com/watch?v=zjkBMFhNj_g">Karpathy — The Busy Person's Intro to LLMs</a> (1 hr; watch before Lesson 0002 if you can).<br>
    Reference: <a href="../reference/m1-core-vocabulary.html">M1 Core Vocabulary</a> ·
    Rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

with:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://www.youtube.com/watch?v=zjkBMFhNj_g">Karpathy — The Busy Person's Intro to LLMs</a> (1 hr; watch before Lesson 0002 if you can).<br>
    Reference: <a href="../reference/m1-core-vocabulary.html">Level 1 Vocabulary</a> ·
    Part of the <a href="../">Agentic Operations</a> course.<br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

- [ ] **Step 4: Edit the reference page's kicker and add a breadcrumb**

In `learning/agentic-operations/reference/m1-core-vocabulary.html`, replace:

```html
<main>
  <header>
    <div class="kicker">Agentic Operations · Reference · M1 Foundational</div>
    <h1>M1 Core Vocabulary</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Level 1 Vocabulary</p>
  <header>
    <div class="kicker">Agentic Operations · Reference · Level 1 · Foundations</div>
    <h1>M1 Core Vocabulary</h1>
```

- [ ] **Step 5: Edit the reference page's footer**

Replace:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0001-not-in-context-doesnt-exist.html">Lesson 0001</a> ·
    Source rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code>
  </footer>
```

with:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0001-not-in-context-doesnt-exist.html">Lesson 0001</a> ·
    Part of the <a href="../">Agentic Operations</a> course.
  </footer>
```

- [ ] **Step 6: Verify the edits landed and old copy is gone**

Run:
```bash
grep -q "Level 1 · Foundations" learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html && echo LESSON_NEW_OK
! grep -q "M1 Foundational" learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html && echo LESSON_OLD_GONE
! grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html && echo LESSON_RUBRIC_GONE
grep -q "Level 1 · Foundations" learning/agentic-operations/reference/m1-core-vocabulary.html && echo REF_NEW_OK
! grep -q "M1 Foundational" learning/agentic-operations/reference/m1-core-vocabulary.html && echo REF_OLD_GONE
```
Expected: all five lines print.

- [ ] **Step 7: Commit**

```bash
git add learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html learning/agentic-operations/reference/m1-core-vocabulary.html
git commit -m "Tidy Level 1 lesson and reference copy for public course"
```

---

### Task 4: Tidy Level 2 public copy (lesson 0002 + reference m2)

**Files:**
- Modify: `learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html`
- Modify: `learning/agentic-operations/reference/m2-core-vocabulary.html`

**Interfaces:**
- Consumes: `/learning/` (Task 1) and `/learning/agentic-operations/` (Task 2).

- [ ] **Step 1: Pre-check**

Run:
```bash
grep -q "M2 Developing" learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html && echo OLD_KICKER_PRESENT
grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html && echo OLD_FOOTER_PRESENT
grep -q "M2 Developing" learning/agentic-operations/reference/m2-core-vocabulary.html && echo OLD_REF_KICKER_PRESENT
```
Expected: all three print.

- [ ] **Step 2: Edit the lesson's kicker and add a breadcrumb**

Replace:

```html
<main>
  <div class="kicker">Agentic Operations · Lesson 0002 · M2 Developing</div>
  <h1>Match the Pattern to the Problem</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0002</p>
  <div class="kicker">Agentic Operations · Lesson 0002 · Level 2 · Developing</div>
  <h1>Match the Pattern to the Problem</h1>
```

- [ ] **Step 3: Edit the lesson's footer**

Replace:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://arxiv.org/abs/2210.03629">ReAct: Synergizing Reasoning and Acting in Language Models</a> (Yao et al.) — read §1–2; it's short and the trace examples are the whole idea.<br>
    Reference: <a href="../reference/m2-core-vocabulary.html">M2 Core Vocabulary</a> ·
    Sister lessons: <a href="0001-not-in-context-doesnt-exist.html">0001</a> · <a href="0003-traces-before-prompts.html">0003</a> ·
    Rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

with:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://arxiv.org/abs/2210.03629">ReAct: Synergizing Reasoning and Acting in Language Models</a> (Yao et al.) — read §1–2; it's short and the trace examples are the whole idea.<br>
    Reference: <a href="../reference/m2-core-vocabulary.html">Level 2 Vocabulary</a> ·
    Sister lessons: <a href="0001-not-in-context-doesnt-exist.html">0001</a> · <a href="0003-traces-before-prompts.html">0003</a> ·
    Part of the <a href="../">Agentic Operations</a> course.<br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

- [ ] **Step 4: Edit the reference page's kicker and add a breadcrumb**

Replace:

```html
<main>
  <header>
    <div class="kicker">Agentic Operations · Reference · M2 Developing</div>
    <h1>M2 Core Vocabulary</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Level 2 Vocabulary</p>
  <header>
    <div class="kicker">Agentic Operations · Reference · Level 2 · Developing</div>
    <h1>M2 Core Vocabulary</h1>
```

- [ ] **Step 5: Edit the reference page's footer**

Replace:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0002-match-the-pattern-to-the-problem.html">Lesson 0002</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m3-core-vocabulary.html">M3</a> · <a href="m4-core-vocabulary.html">M4</a> ·
    Source rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code>
  </footer>
```

with:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0002-match-the-pattern-to-the-problem.html">Lesson 0002</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m3-core-vocabulary.html">M3</a> · <a href="m4-core-vocabulary.html">M4</a> ·
    Part of the <a href="../">Agentic Operations</a> course.
  </footer>
```

- [ ] **Step 6: Verify**

Run:
```bash
grep -q "Level 2 · Developing" learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html && echo LESSON_NEW_OK
! grep -q "M2 Developing" learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html && echo LESSON_OLD_GONE
! grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html && echo LESSON_RUBRIC_GONE
grep -q "Level 2 · Developing" learning/agentic-operations/reference/m2-core-vocabulary.html && echo REF_NEW_OK
! grep -q "M2 Developing" learning/agentic-operations/reference/m2-core-vocabulary.html && echo REF_OLD_GONE
```
Expected: all five lines print.

- [ ] **Step 7: Commit**

```bash
git add learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html learning/agentic-operations/reference/m2-core-vocabulary.html
git commit -m "Tidy Level 2 lesson and reference copy for public course"
```

---

### Task 5: Tidy Level 3 public copy (lesson 0003 + reference m3)

**Files:**
- Modify: `learning/agentic-operations/lessons/0003-traces-before-prompts.html`
- Modify: `learning/agentic-operations/reference/m3-core-vocabulary.html`

**Interfaces:**
- Consumes: `/learning/` (Task 1) and `/learning/agentic-operations/` (Task 2).

- [ ] **Step 1: Pre-check**

Run:
```bash
grep -q "M3 Advanced" learning/agentic-operations/lessons/0003-traces-before-prompts.html && echo OLD_KICKER_PRESENT
grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0003-traces-before-prompts.html && echo OLD_FOOTER_PRESENT
grep -q "M3 Advanced" learning/agentic-operations/reference/m3-core-vocabulary.html && echo OLD_REF_KICKER_PRESENT
```
Expected: all three print.

- [ ] **Step 2: Edit the lesson's kicker and add a breadcrumb**

Replace:

```html
<main>
  <div class="kicker">Agentic Operations · Lesson 0003 · M3 Advanced</div>
  <h1>Traces Before Prompts</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0003</p>
  <div class="kicker">Agentic Operations · Lesson 0003 · Level 3 · Advanced</div>
  <h1>Traces Before Prompts</h1>
```

- [ ] **Step 3: Edit the lesson's footer**

Replace:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://www.anthropic.com/engineering/multi-agent-research-system">How we built our multi-agent research system</a> (Anthropic) — the most honest public account of what multi-agent actually costs and buys.<br>
    Reference: <a href="../reference/m3-core-vocabulary.html">M3 Core Vocabulary</a> ·
    Sister lessons: <a href="0002-match-the-pattern-to-the-problem.html">0002</a> · <a href="0004-own-the-feedback-loop.html">0004</a> ·
    Rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

with:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://www.anthropic.com/engineering/multi-agent-research-system">How we built our multi-agent research system</a> (Anthropic) — the most honest public account of what multi-agent actually costs and buys.<br>
    Reference: <a href="../reference/m3-core-vocabulary.html">Level 3 Vocabulary</a> ·
    Sister lessons: <a href="0002-match-the-pattern-to-the-problem.html">0002</a> · <a href="0004-own-the-feedback-loop.html">0004</a> ·
    Part of the <a href="../">Agentic Operations</a> course.<br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

- [ ] **Step 4: Edit the reference page's kicker and add a breadcrumb**

Replace:

```html
<main>
  <header>
    <div class="kicker">Agentic Operations · Reference · M3 Advanced</div>
    <h1>M3 Core Vocabulary</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Level 3 Vocabulary</p>
  <header>
    <div class="kicker">Agentic Operations · Reference · Level 3 · Advanced</div>
    <h1>M3 Core Vocabulary</h1>
```

- [ ] **Step 5: Edit the reference page's footer**

Replace:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0003-traces-before-prompts.html">Lesson 0003</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m2-core-vocabulary.html">M2</a> · <a href="m4-core-vocabulary.html">M4</a> ·
    Source rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code>
  </footer>
```

with:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0003-traces-before-prompts.html">Lesson 0003</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m2-core-vocabulary.html">M2</a> · <a href="m4-core-vocabulary.html">M4</a> ·
    Part of the <a href="../">Agentic Operations</a> course.
  </footer>
```

- [ ] **Step 6: Verify**

Run:
```bash
grep -q "Level 3 · Advanced" learning/agentic-operations/lessons/0003-traces-before-prompts.html && echo LESSON_NEW_OK
! grep -q "M3 Advanced" learning/agentic-operations/lessons/0003-traces-before-prompts.html && echo LESSON_OLD_GONE
! grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0003-traces-before-prompts.html && echo LESSON_RUBRIC_GONE
grep -q "Level 3 · Advanced" learning/agentic-operations/reference/m3-core-vocabulary.html && echo REF_NEW_OK
! grep -q "M3 Advanced" learning/agentic-operations/reference/m3-core-vocabulary.html && echo REF_OLD_GONE
```
Expected: all five lines print.

- [ ] **Step 7: Commit**

```bash
git add learning/agentic-operations/lessons/0003-traces-before-prompts.html learning/agentic-operations/reference/m3-core-vocabulary.html
git commit -m "Tidy Level 3 lesson and reference copy for public course"
```

---

### Task 6: Tidy Level 4 public copy (lesson 0004 + reference m4)

**Files:**
- Modify: `learning/agentic-operations/lessons/0004-own-the-feedback-loop.html`
- Modify: `learning/agentic-operations/reference/m4-core-vocabulary.html`

**Interfaces:**
- Consumes: `/learning/` (Task 1) and `/learning/agentic-operations/` (Task 2).

- [ ] **Step 1: Pre-check**

Run:
```bash
grep -q "M4 Operational Leader" learning/agentic-operations/lessons/0004-own-the-feedback-loop.html && echo OLD_KICKER_PRESENT
grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0004-own-the-feedback-loop.html && echo OLD_FOOTER_PRESENT
grep -q "M4 Operational Leader" learning/agentic-operations/reference/m4-core-vocabulary.html && echo OLD_REF_KICKER_PRESENT
```
Expected: all three print.

- [ ] **Step 2: Edit the lesson's kicker and add a breadcrumb**

Replace:

```html
<main>
  <div class="kicker">Agentic Operations · Lesson 0004 · M4 Operational Leader</div>
  <h1>Own the Feedback Loop</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0004</p>
  <div class="kicker">Agentic Operations · Lesson 0004 · Level 4 · Operational Leadership</div>
  <h1>Own the Feedback Loop</h1>
```

- [ ] **Step 3: Edit the lesson's footer**

Replace:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://sre.google/sre-book/service-level-objectives/">Service Level Objectives — Google SRE Book, ch. 4</a> (free online; substitute "agent run" for "request" as you read).<br>
    Reference: <a href="../reference/m4-core-vocabulary.html">M4 Core Vocabulary</a> ·
    Sister lesson: <a href="0003-traces-before-prompts.html">0003 — Traces Before Prompts</a> ·
    Rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

with:

```html
  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://sre.google/sre-book/service-level-objectives/">Service Level Objectives — Google SRE Book, ch. 4</a> (free online; substitute "agent run" for "request" as you read).<br>
    Reference: <a href="../reference/m4-core-vocabulary.html">Level 4 Vocabulary</a> ·
    Sister lesson: <a href="0003-traces-before-prompts.html">0003 — Traces Before Prompts</a> ·
    Part of the <a href="../">Agentic Operations</a> course.<br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
```

- [ ] **Step 4: Edit the reference page's kicker and add a breadcrumb**

Replace:

```html
<main>
  <header>
    <div class="kicker">Agentic Operations · Reference · M4 Operational Leader</div>
    <h1>M4 Core Vocabulary</h1>
```

with:

```html
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Level 4 Vocabulary</p>
  <header>
    <div class="kicker">Agentic Operations · Reference · Level 4 · Operational Leadership</div>
    <h1>M4 Core Vocabulary</h1>
```

- [ ] **Step 5: Edit the reference page's footer**

Replace:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0004-own-the-feedback-loop.html">Lesson 0004</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m2-core-vocabulary.html">M2</a> · <a href="m3-core-vocabulary.html">M3</a> ·
    Source rubric: <code>docs/inbox/2026-07-03/Agentic knowledge development.md</code>
  </footer>
```

with:

```html
  <footer>
    Agentic Operations workspace · <a href="../lessons/0004-own-the-feedback-loop.html">Lesson 0004</a> ·
    Sister sheets: <a href="m1-core-vocabulary.html">M1</a> · <a href="m2-core-vocabulary.html">M2</a> · <a href="m3-core-vocabulary.html">M3</a> ·
    Part of the <a href="../">Agentic Operations</a> course.
  </footer>
```

- [ ] **Step 6: Verify**

Run:
```bash
grep -q "Level 4 · Operational Leadership" learning/agentic-operations/lessons/0004-own-the-feedback-loop.html && echo LESSON_NEW_OK
! grep -q "M4 Operational Leader<" learning/agentic-operations/lessons/0004-own-the-feedback-loop.html && echo LESSON_OLD_GONE
! grep -q "docs/inbox/2026-07-03" learning/agentic-operations/lessons/0004-own-the-feedback-loop.html && echo LESSON_RUBRIC_GONE
grep -q "Level 4 · Operational Leadership" learning/agentic-operations/reference/m4-core-vocabulary.html && echo REF_NEW_OK
! grep -q "M4 Operational Leader<" learning/agentic-operations/reference/m4-core-vocabulary.html && echo REF_OLD_GONE
```
Expected: all five lines print. (Matching `M4 Operational Leader<` rather than the bare phrase avoids a false failure against the new "Level 4 · Operational Leadership" string, which also contains "Operational Lead...".)

- [ ] **Step 7: Commit**

```bash
git add learning/agentic-operations/lessons/0004-own-the-feedback-loop.html learning/agentic-operations/reference/m4-core-vocabulary.html
git commit -m "Tidy Level 4 lesson and reference copy for public course"
```

---

### Task 7: Tidy internal working docs for a public repo

**Files:**
- Modify: `learning/agentic-operations/MISSION.md`
- Modify: `learning/agentic-operations/NOTES.md`
- Modify: `learning/agentic-operations/RESOURCES.md`
- Modify: `learning/agentic-operations/learning-records/0001-m2-unlocked-by-request.md`
- Modify: `learning/agentic-operations/learning-records/0002-full-map-unlocked.md`

**Interfaces:** None — these are repo-only working docs, not linked from any HTML page (per Global Constraints).

- [ ] **Step 1: Pre-check**

Run:
```bash
grep -q "Open questions to confirm with Scott" learning/agentic-operations/NOTES.md && echo NOTES_OLD_PRESENT
grep -q '\[Rubric: Agentic Operations Knowledge Map (local)\]' learning/agentic-operations/RESOURCES.md && echo RESOURCES_OLD_PRESENT
grep -q '\[\[MISSION.md\]\]' learning/agentic-operations/learning-records/0001-m2-unlocked-by-request.md && echo RECORD1_OLD_PRESENT
grep -q '\[\[0001-m2-unlocked-by-request\]\]' learning/agentic-operations/learning-records/0002-full-map-unlocked.md && echo RECORD2_OLD_PRESENT
```
Expected: all four print.

- [ ] **Step 2: Edit `MISSION.md`**

Replace:

```markdown
## Why
Scott is climbing the "Agentic Operations Knowledge Map" (`docs/inbox/2026-07-03/Agentic knowledge development.md`) — a four-milestone arc ending at Head-of-Agentic-Operations capability. He already operates a heavily agentic codebase (Vernant) every day; this mission formalizes the foundations so each capability is explainable and teachable, not just used. The immediate target is the M1 readiness signal.
```

with:

```markdown
## Why
Scott is climbing the "Agentic Operations Knowledge Map" (`docs/inbox/2026-07-03/Agentic knowledge development.md` — a private planning doc that lives outside this repo, not a public link) — a four-milestone arc ending at Head-of-Agentic-Operations capability. He already operates a heavily agentic codebase (Vernant) every day; this mission formalizes the foundations so each capability is explainable and teachable, not just used. The immediate target is the M1 readiness signal.
```

- [ ] **Step 3: Edit `NOTES.md`**

Replace:

```markdown
## Open questions to confirm with Scott
```

with:

```markdown
## Open questions
```

- [ ] **Step 4: Edit `RESOURCES.md`**

Replace:

```markdown
- [Rubric: Agentic Operations Knowledge Map (local)](../../inbox/2026-07-03/Agentic%20knowledge%20development.md)
  The curriculum source of truth: four maturity stages, per-stage concepts, intuitions, exercises, and readiness signals. Use for: deciding what to teach next and when a milestone gate is passed.
```

with:

```markdown
- Rubric: Agentic Operations Knowledge Map — a private planning doc outside this repo (not a public link).
  The curriculum source of truth: four maturity stages, per-stage concepts, intuitions, exercises, and readiness signals. Use for: deciding what to teach next and when a milestone gate is passed.
```

- [ ] **Step 5: Edit `learning-records/0001-m2-unlocked-by-request.md`**

Replace:

```markdown
Scott explicitly requested M2 teaching material (2026-07-03) as a sister set to the M1 package, while the M1 hands-on lessons (tool loop build, overflow experiment) are still pending. [[MISSION.md]] updated: M2 is now in scope; M3+ remains out.
```

with:

```markdown
Scott explicitly requested M2 teaching material (2026-07-03) as a sister set to the M1 package, while the M1 hands-on lessons (tool loop build, overflow experiment) are still pending. MISSION.md updated: M2 is now in scope; M3+ remains out.
```

- [ ] **Step 6: Edit `learning-records/0002-full-map-unlocked.md`**

Replace:

```markdown
Scott requested M3 and M4 sister sets (2026-07-03) immediately after M2, so the workspace now covers the full maturity map. Same posture as [[0001-m2-unlocked-by-request]]: study material for all four stages exists, but each gate passes only on demonstrated capability — the rubric's "move by demonstrated capability, not calendar time" is unchanged.
```

with:

```markdown
Scott requested M3 and M4 sister sets (2026-07-03) immediately after M2, so the workspace now covers the full maturity map. Same posture as learning-records/0001-m2-unlocked-by-request.md: study material for all four stages exists, but each gate passes only on demonstrated capability — the rubric's "move by demonstrated capability, not calendar time" is unchanged.
```

- [ ] **Step 7: Verify**

Run:
```bash
! grep -q "Open questions to confirm with Scott" learning/agentic-operations/NOTES.md && echo NOTES_OK
grep -q "private planning doc" learning/agentic-operations/MISSION.md && echo MISSION_OK
! grep -q '\[Rubric: Agentic Operations Knowledge Map (local)\]' learning/agentic-operations/RESOURCES.md && echo RESOURCES_OK
! grep -q '\[\[MISSION.md\]\]' learning/agentic-operations/learning-records/0001-m2-unlocked-by-request.md && echo RECORD1_OK
! grep -q '\[\[0001-m2-unlocked-by-request\]\]' learning/agentic-operations/learning-records/0002-full-map-unlocked.md && echo RECORD2_OK
```
Expected: all five lines print.

- [ ] **Step 8: Commit**

```bash
git add learning/agentic-operations/MISSION.md learning/agentic-operations/NOTES.md learning/agentic-operations/RESOURCES.md learning/agentic-operations/learning-records/0001-m2-unlocked-by-request.md learning/agentic-operations/learning-records/0002-full-map-unlocked.md
git commit -m "Tidy working docs for a public repo"
```

---

### Task 8: Add "Learning" to the main site nav

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: `/learning/` (Task 1).

- [ ] **Step 1: Pre-check**

Run: `grep -q 'href="/learning/"' index.html && echo PRESENT || echo MISSING`
Expected: `MISSING`

- [ ] **Step 2: Edit the nav**

Replace:

```html
<nav>
  <a href="#" class="nav-logo">Scott <span>Curtner</span></a>
  <ul class="nav-links">
    <li><a href="#about">About</a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#credentials">Credentials</a></li>
    <li><a href="#writing">Writing</a></li>
    <li><a href="#connect">Connect</a></li>
  </ul>
</nav>
```

with:

```html
<nav>
  <a href="#" class="nav-logo">Scott <span>Curtner</span></a>
  <ul class="nav-links">
    <li><a href="#about">About</a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#credentials">Credentials</a></li>
    <li><a href="#writing">Writing</a></li>
    <li><a href="/learning/">Learning</a></li>
    <li><a href="#connect">Connect</a></li>
  </ul>
</nav>
```

- [ ] **Step 3: Verify**

Run: `grep -q 'href="/learning/">Learning</a>' index.html && echo PRESENT`
Expected: `PRESENT`

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add Learning link to main site nav"
```

---

### Task 9: Register the new pages in sitemap.xml and llms.txt

**Files:**
- Modify: `sitemap.xml`
- Modify: `llms.txt`

**Interfaces:**
- Consumes: all URLs produced by Tasks 1–2 (hub, course page) and the existing lesson/reference URLs.

- [ ] **Step 1: Pre-check**

Run: `grep -q "scottcurtner.com/learning/" sitemap.xml && echo PRESENT || echo MISSING`
Expected: `MISSING`

- [ ] **Step 2: Add entries to `sitemap.xml`**

Replace the closing tag:

```xml
</urlset>
```

with:

```xml
  <url>
    <loc>https://www.scottcurtner.com/learning/</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/lessons/0003-traces-before-prompts.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/lessons/0004-own-the-feedback-loop.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/reference/m1-core-vocabulary.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/reference/m2-core-vocabulary.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/reference/m3-core-vocabulary.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://www.scottcurtner.com/learning/agentic-operations/reference/m4-core-vocabulary.html</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
```

- [ ] **Step 3: Add a Learning section to `llms.txt`**

Replace:

```markdown
## Optional
```

with:

```markdown
## Learning

- [Agentic Operations](https://www.scottcurtner.com/learning/agentic-operations/): A hands-on, four-level course on building AI agents — from "the context window is the model's entire world" to owning SLOs for a live agent in production. Written and published as I go.

## Optional
```

- [ ] **Step 4: Verify `sitemap.xml` is well-formed and both files contain the new entries**

Run:
```bash
python -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('XML_OK')"
grep -c "scottcurtner.com/learning/" sitemap.xml
grep -q "Agentic Operations" llms.txt && echo LLMS_OK
```
Expected: `XML_OK`, a count of `10`, and `LLMS_OK`.

- [ ] **Step 5: Commit**

```bash
git add sitemap.xml llms.txt
git commit -m "Add Learning section pages to sitemap.xml and llms.txt"
```

---

### Task 10: Full link-integrity sweep and manual visual QA

**Files:** None created or modified — this task only verifies Tasks 1–9.

- [ ] **Step 1: Automated link-integrity sweep**

Run this from the repo root — it extracts every local `href` from the new/edited learning pages and confirms the target file exists:

```bash
cd "C:/dev/scottcurtner-website"
FAIL=0
for base in learning/index.html learning/agentic-operations/index.html \
  learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html \
  learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html \
  learning/agentic-operations/lessons/0003-traces-before-prompts.html \
  learning/agentic-operations/lessons/0004-own-the-feedback-loop.html \
  learning/agentic-operations/reference/m1-core-vocabulary.html \
  learning/agentic-operations/reference/m2-core-vocabulary.html \
  learning/agentic-operations/reference/m3-core-vocabulary.html \
  learning/agentic-operations/reference/m4-core-vocabulary.html; do
  dir=$(dirname "$base")
  grep -oE 'href="[^"#][^"]*"' "$base" | sed -E 's/href="([^"]*)"/\1/' | while read -r href; do
    href="${href%%#*}"
    case "$href" in
      ""|http*|/) continue ;;
      /*) target=".$href" ;;
      *) target="$dir/$href" ;;
    esac
    resolved=$(python -c "import os,sys; print(os.path.normpath(sys.argv[1]))" "$target")
    if [ -d "$resolved" ]; then resolved="$resolved/index.html"; fi
    if [ ! -f "$resolved" ]; then
      echo "BROKEN in $base -> $href (resolved: $resolved)"
      FAIL=1
    fi
  done
done
test "$FAIL" = "0" && echo ALL_LINKS_OK
```

Expected: `ALL_LINKS_OK`, with no `BROKEN in ...` lines above it.

- [ ] **Step 2: Confirm `learning-records/` files are not linked from any HTML page**

Run:
```bash
grep -rl "learning-records" --include="*.html" learning/ && echo FOUND_LINK || echo NO_LINKS_FOUND
```
Expected: `NO_LINKS_FOUND`.

- [ ] **Step 3: Manual visual QA (human step — not automatable)**

Open these paths directly in a browser (e.g. `file:///C:/dev/scottcurtner-website/learning/index.html`), and repeat with the OS/browser set to both light and dark mode:
- `learning/index.html`
- `learning/agentic-operations/index.html`
- `learning/agentic-operations/lessons/0001-not-in-context-doesnt-exist.html`
- `index.html` (confirm the new "Learning" nav link appears and navigates correctly)

Confirm: breadcrumbs render and are clickable, the roadmap's checkmarks/circles are legible in both color schemes, and clicking through hub → course → a lesson → its reference page → back to hub all work.

- [ ] **Step 4: Report results**

No commit for this task — it's verification only. If Step 1 or Step 2 finds a problem, fix it in the relevant earlier task's files and re-run this task before considering the plan complete.
