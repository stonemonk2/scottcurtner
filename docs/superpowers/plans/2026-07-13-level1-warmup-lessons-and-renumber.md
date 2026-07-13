# Level 1 Warm-Up Lessons, Course Renumber & M→Level Rename — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two new Level 1 hands-on lessons (Tokens & Cost, Anatomy of a Tool Call), renumber all course lessons to reading order, rename every learner-facing "M#" term and filename to "Level #", wire next-lesson links through the whole course, and end the final lesson with a congratulations block.

**Architecture:** Static hand-authored HTML site (GitHub Pages, no build step). All changes are file renames plus text edits, driven by two small one-off Python scripts (deterministic token replacement) and hand-authored HTML for the new lessons. A repo-resident link-checker script is written first and serves as the regression test after every task.

**Tech Stack:** Plain HTML/CSS (no framework), Python 3.12 (scripts, run via `uv run python` or `python`), git. Lesson code samples use the `anthropic` Python SDK.

**Spec:** `docs/superpowers/specs/2026-07-13-level1-warmup-lessons-and-renumber-design.md`

## Global Constraints

- Learner-facing terminology is **"Level 1"–"Level 4"** — no "M1"–"M4" may remain in any HTML under `learning/`, nor in `learning/agentic-operations/README.md`, `.env.example`, or `exercises/level1_agent.py`.
- Internal planning docs (`NOTES.md`, `MISSION.md`, `RESOURCES.md`, `learning-records/`) KEEP their M1–M4 milestone language; only file paths/lesson numbers are corrected there.
- Final lesson numbering = reading order: 0001–0004 foundations (unchanged files), 0005 tokens-and-cost (new), 0006 anatomy-of-a-tool-call (new), then old 0005→0007, 0006→0008, 0007→0009, 0008→0010, 0009→0011, 0010→0012, 0011→0013, 0012→0014, 0013→0015, 0014→0016, 0015→0017, 0016→0018.
- File renames: `reference/m{N}-core-vocabulary.html` → `reference/level-{N}-vocabulary.html` (N=1..4); `exercises/m1_agent.py` → `exercises/level1_agent.py`. `reference/agent-loop-and-tool-call.html` keeps its name.
- **No redirect stubs** — old URLs 404 (explicit decision).
- Model string in lesson code samples: `claude-opus-4-8`, priced $5 / $25 per million input/output tokens (matches existing lesson copy and the claude-api reference).
- Today's date for lastmod/notes: **2026-07-13**.
- New lesson pages copy the `<head>` + `<style>` block verbatim from `lessons/0007-build-the-single-tool-agent.html` (post-rename), changing only title/description/canonical-type metadata as specified per task. This keeps the sister styling identical.
- Commit after each task. Do not push — Scott decides when to publish.

---

### Task 1: Link-checker script (the regression test)

**Files:**
- Create: `scripts/check_learning_links.py`

**Interfaces:**
- Produces: `python scripts/check_learning_links.py [links|tags|terms ...]` — exits 0 when clean, 1 with a printed failure list otherwise. No args = run all three checks. Later tasks call this exact command.

- [ ] **Step 1: Write the checker**

```python
"""Checks the learning/ HTML tree: relative links resolve, no malformed
closing anchor tags, no leftover M1-M4 milestone terms."""
import re
import sys
import pathlib
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path("learning")
checks = sys.argv[1:] or ["links", "tags", "terms"]
failures = []

for page in sorted(ROOT.rglob("*.html")):
    text = page.read_text(encoding="utf-8")

    if "links" in checks:
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = unquote(urlparse(url).path)
            if not path_part:
                continue
            if path_part.startswith("/"):
                target = pathlib.Path.cwd() / path_part.lstrip("/")
            else:
                target = page.parent / path_part
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                failures.append(f"{page}: broken link {url}")

    if "tags" in checks:
        if re.search(r"<\\a>", text):
            n = len(re.findall(r"<\\a>", text))
            failures.append(f"{page}: {n} malformed closing tag(s) <\\a>")

    if "terms" in checks:
        for m in re.finditer(r"\bM[1-4]\b", text):
            failures.append(f"{page}: leftover milestone term {m.group(0)}")

print(f"{len(failures)} failure(s)")
for f in failures:
    print(" -", f)
sys.exit(1 if failures else 0)
```

- [ ] **Step 2: Baseline run — expect failures**

Run: `python scripts/check_learning_links.py`
Expected: exit 1. The `tags` check reports ~10 lesson files with `<\a>`; the `terms` check reports many M1–M4 hits. The `links` check should report **zero** broken links — if it reports any, inspect them (they may be pre-existing bugs worth noting to Scott) before proceeding.

- [ ] **Step 3: Verify links-only mode passes**

Run: `python scripts/check_learning_links.py links`
Expected: `0 failure(s)`, exit 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/check_learning_links.py
git commit -m "Add learning-tree link/tag/term checker"
```

---

### Task 2: Rename files and renumber every reference

**Files:**
- Rename: 12 lesson files, 4 vocabulary reference files, 1 exercise script (exact list in Step 1)
- Modify: every `.html`, `.md`, `.py` under `learning/` plus `sitemap.xml` (scripted token replacement)
- Create then delete: `_tmp_renumber.py` (repo root, one-off)

**Interfaces:**
- Produces: the final file tree and internally consistent numbering that Tasks 3–9 assume. After this task, `lessons/0007-build-the-single-tool-agent.html` is the build lesson, `reference/level-1-vocabulary.html` exists, `exercises/level1_agent.py` exists.

- [ ] **Step 1: git mv all renamed files**

```bash
cd learning/agentic-operations
git mv lessons/0016-the-improvement-loop.html            lessons/0018-the-improvement-loop.html
git mv lessons/0015-guardrails-and-hitl.html             lessons/0017-guardrails-and-hitl.html
git mv lessons/0014-slo-dashboard.html                   lessons/0016-slo-dashboard.html
git mv lessons/0013-critic-verifier-step.html            lessons/0015-critic-verifier-step.html
git mv lessons/0012-tracing-and-planted-regression.html  lessons/0014-tracing-and-planted-regression.html
git mv lessons/0011-orchestrator-bakeoff.html            lessons/0013-orchestrator-bakeoff.html
git mv lessons/0010-episodic-memory.html                 lessons/0012-episodic-memory.html
git mv lessons/0009-rag-build-and-break.html             lessons/0011-rag-build-and-break.html
git mv lessons/0008-react-multi-hop-build.html           lessons/0010-react-multi-hop-build.html
git mv lessons/0007-structured-prompting-and-the-injection-lab.html lessons/0009-structured-prompting-and-the-injection-lab.html
git mv lessons/0006-break-it-on-purpose.html             lessons/0008-break-it-on-purpose.html
git mv lessons/0005-build-the-single-tool-agent.html     lessons/0007-build-the-single-tool-agent.html
git mv reference/m1-core-vocabulary.html reference/level-1-vocabulary.html
git mv reference/m2-core-vocabulary.html reference/level-2-vocabulary.html
git mv reference/m3-core-vocabulary.html reference/level-3-vocabulary.html
git mv reference/m4-core-vocabulary.html reference/level-4-vocabulary.html
git mv exercises/m1_agent.py exercises/level1_agent.py
cd ../..
```

- [ ] **Step 2: Write the one-off renumber script at repo root as `_tmp_renumber.py`**

```python
import re
import pathlib

files = [p for p in pathlib.Path("learning").rglob("*")
         if p.suffix in {".html", ".md", ".py"}]
files.append(pathlib.Path("sitemap.xml"))

# Descending order is load-bearing: 0016->0018 first, 0005->0007 last,
# so freshly written targets are never re-matched by a later source.
renames = [(f"{n:04d}", f"{n + 2:04d}") for n in range(16, 4, -1)]
strings = [
    ("m1-core-vocabulary", "level-1-vocabulary"),
    ("m2-core-vocabulary", "level-2-vocabulary"),
    ("m3-core-vocabulary", "level-3-vocabulary"),
    ("m4-core-vocabulary", "level-4-vocabulary"),
    ("m1_agent", "level1_agent"),
]

for path in files:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in renames:
        # lookbehind excludes digits AND '.' so decimals like 0.0005 are safe
        text = re.sub(rf"(?<![0-9.]){old}(?![0-9])", new, text)
    for old, new in strings:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("updated", path)
```

- [ ] **Step 3: Run it and delete it**

Run: `python _tmp_renumber.py` then `del _tmp_renumber.py` (or `rm _tmp_renumber.py` in bash)
Expected: prints an `updated <path>` line for most lesson files, the course index, reference pages, `NOTES.md`, `README.md`, `RESOURCES.md`, `exercises/level1_agent.py`, and `sitemap.xml`.

- [ ] **Step 4: Verify no old references remain and links resolve**

Run:
```bash
grep -rnE "0005-build-the|0006-break-it|0007-structured|0008-react|0009-rag-build|0010-episodic|0011-orchestrator|0012-tracing|0013-critic|0014-slo|0015-guardrails|0016-the-improvement|m[1-4]-core-vocabulary|m1_agent" learning sitemap.xml
python scripts/check_learning_links.py links
```
Expected: grep finds nothing; checker prints `0 failure(s)`.

- [ ] **Step 5: Spot-check semantics survived**

Run: `grep -n "0015 verifier\|0013 verifier\|0014 evals\|0012 evals" learning/agentic-operations/lessons/*.html`
Expected: the SLO lesson (now 0016) says "the 0015 verifier" and the critic references say "your 0014 evals" — i.e. in-prose lesson numbers shifted by 2. No "0013 verifier" or "0012 evals" hits remain.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "Renumber lessons to reading order; rename vocabulary pages and exercise script to Level naming"
```

---

### Task 3: M→Level terminology sweep (learner-facing files)

**Files:**
- Modify: all `learning/**/*.html`, `learning/agentic-operations/README.md`, `learning/agentic-operations/.env.example`, `learning/agentic-operations/exercises/level1_agent.py`
- Create then delete: `_tmp_sweep.py` (repo root, one-off)

- [ ] **Step 1: Confirm the Python file's M-hits are comments/docstrings only**

Run: `grep -n "M[1-4]" learning/agentic-operations/exercises/level1_agent.py`
Expected: matches only inside comments or docstrings. If any match is inside executable code or a string literal used at runtime, stop and handle that occurrence by hand before running the sweep.

- [ ] **Step 2: Write `_tmp_sweep.py` at repo root**

```python
import re
import pathlib

targets = list(pathlib.Path("learning").rglob("*.html"))
targets += [
    pathlib.Path("learning/agentic-operations/README.md"),
    pathlib.Path("learning/agentic-operations/.env.example"),
    pathlib.Path("learning/agentic-operations/exercises/level1_agent.py"),
]

for path in targets:
    text = path.read_text(encoding="utf-8")
    new = re.sub(r"\bM([1-4])\b", r"Level \1", text)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
        print("updated", path)
```

- [ ] **Step 3: Run it and delete it**

Run: `python _tmp_sweep.py` then delete the script.
Expected: `updated` lines for ~16 lesson files, the 4 vocabulary pages, `agent-loop-and-tool-call.html`, and possibly README/.env/py.

- [ ] **Step 4: Verify zero leftovers (case-insensitive) and readability**

Run:
```bash
python scripts/check_learning_links.py terms
grep -rniE "\bm[1-4]\b" learning --include="*.html"
grep -rn "Level [1-4]/00" learning --include="*.html"
```
Expected: checker prints `0 failure(s)`; case-insensitive grep finds nothing. The third grep locates compound phrases like "the Level 1/0009 lesson" (was "the M1/0007 lesson" in the guardrails lesson) — read each hit in context and smooth the wording if it reads awkwardly, e.g. rewrite `the Level 1/0009 lesson at production stakes` to `the lesson of Level 1 and Lesson 0009, at production stakes`.

- [ ] **Step 5: Read one full lesson to confirm natural phrasing**

Read `learning/agentic-operations/lessons/0002-match-the-pattern-to-the-problem.html` end to end. Sentences like "Level 1 established that the context window is the model's entire world" and "Level 2 vocabulary doesn't pass the Level 1 gate" must read naturally. Fix any awkward output of the blanket replacement by hand.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "Replace learner-facing M1-M4 milestone terms with Level 1-4"
```

---

### Task 4: New Lesson 0005 — Tokens & Cost

**Files:**
- Create: `learning/agentic-operations/lessons/0005-tokens-and-cost.html`
- Reference (read-only): `learning/agentic-operations/lessons/0007-build-the-single-tool-agent.html` (head/style source, and the BYOK checkpoint text to relocate)

**Interfaces:**
- Produces: page at `lessons/0005-tokens-and-cost.html` containing the BYOK "Checkpoint 0". Task 6 rewrites 0007's own Checkpoint 0 to point here; Task 7 links here from 0004; Task 8 lists it in the index and sitemap.

- [ ] **Step 1: Create the file scaffold**

Copy everything from the start of `lessons/0007-build-the-single-tool-agent.html` through `</head>` (doctype, `<html lang>`, meta tags, `<style>` block) verbatim into the new file, then apply these metadata changes:
- `<title>` → same pattern as 0007's title with the lesson name/number swapped to `Tokens & Cost` / `0005` (e.g. if 0007's is `Build the Single-Tool Agent — ... `, mirror it).
- Any `<meta name="description">` / `og:description` → `Hands-on lab: tokenize real text, predict a call's cost, and read real dollars off a live Claude API response — Level 1 of the Agentic Operations course.`
- Any `<link rel="canonical">` / `og:url` → `https://www.scottcurtner.com/learning/agentic-operations/lessons/0005-tokens-and-cost.html`
- Any `og:title` → mirror the new `<title>`.
If 0007's head has none of these meta tags, do not add them.

- [ ] **Step 2: Write the body**

Use exactly this body (the breadcrumb/kicker/footer match the sister-lesson pattern; the Checkpoint 0 text is the build lesson's BYOK checkpoint relocated with one sentence adjusted):

```html
<body>
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0005</p>
  <div class="kicker">Agentic Operations · Lesson 0005 · Level 1 · Foundations · Hands-on lab</div>
  <h1>Tokens &amp; Cost</h1>
  <p class="lede">The unit everything is denominated in: watch your words become tokens, and read real dollars off a real API response.</p>

  <div class="win"><strong>Your win for this lesson:</strong> you'll tokenize real text, predict
  what a call will cost, and check the prediction against the usage numbers on a live response.
  Prerequisite: <a href="0001-not-in-context-doesnt-exist.html">Lesson 0001</a>.</div>

  <p>Lesson 0001 established that the context window is the model's entire world. This lesson
  prices that world. Models don't read words — they read <strong>tokens</strong>, chunks of a few
  characters each, and every API bill, rate limit, and context-window ceiling you will ever meet
  is denominated in them. Work in a terminal at the repo root; the snippets below run in
  <code>uv run python</code>.</p>

  <h2>Checkpoint 0 · Bring your own key</h2>
  <p>This course runs on <strong>your own</strong> Anthropic API key — it stays on your machine,
  is never committed, and never reaches anyone else. Copy the template, then paste your key into
  the new <code>.env</code>:</p>
<pre><code>cp .env.example .env      # then edit .env:  ANTHROPIC_API_KEY=sk-ant-...</code></pre>
  <p>Create a key at the <a href="https://console.anthropic.com">Anthropic Console</a> if you
  don't have one. <code>.env</code> is gitignored, so the key can't be committed by accident.
  Verify it's set without printing the secret:</p>
<pre><code>uv run python -c "from dotenv import dotenv_values; print('ANTHROPIC_API_KEY' in dotenv_values('.env'))"</code></pre>
  <div class="check"><strong>Pass:</strong> prints <code>True</code>. The whole Level 1 hands-on
  track runs on well under a dollar of your own credit.</div>

  <h2>Stage 1 · Count tokens without spending anything</h2>
  <p>The API has a counting endpoint that tokenizes your input without running the model. Point
  it at three different kinds of text and compare:</p>
<pre><code>import anthropic
client = anthropic.Anthropic()

samples = {
    "prose":   "The context window is the model's entire world. If a fact "
               "is not in the window, it does not exist for this call.",
    "code":    "def total(xs):\n    return sum(x.amount for x in xs if x.ok)",
    "numbers": "3.14159 2.71828 1.41421 0.57721 6.02214",
}
for name, text in samples.items():
    n = client.messages.count_tokens(
        model="claude-opus-4-8",
        messages=[{"role": "user", "content": text}],
    ).input_tokens
    print(f"{name}: {len(text)} chars -&gt; {n} tokens")</code></pre>
  <div class="check"><strong>Pass:</strong> you can state roughly how many characters one token
  buys in English prose (about four), and explain why code and bare numbers do worse. Then try
  your own: paste a paragraph from Lesson 0001 and predict its count before running.</div>

  <h2>Stage 2 · Predict, then spend</h2>
  <p>This course's model, <code>claude-opus-4-8</code>, is priced at $5 per million input tokens
  and $25 per million output tokens. Estimate before you spend: count the input, guess the output
  length, do the arithmetic — then make the call and read the real numbers off
  <code>response.usage</code>.</p>
<pre><code>QUESTION = ("Explain in about 200 words why LLM APIs price input and "
            "output tokens differently.")

n_in = client.messages.count_tokens(
    model="claude-opus-4-8",
    messages=[{"role": "user", "content": QUESTION}],
).input_tokens
guess_out = 300  # ~200 words of output
estimate = n_in / 1e6 * 5.00 + guess_out / 1e6 * 25.00
print(f"predicted: {n_in} in, ~{guess_out} out -&gt; ${estimate:.5f}")

response = client.messages.create(
    model="claude-opus-4-8", max_tokens=2000,
    messages=[{"role": "user", "content": QUESTION}],
)
u = response.usage
actual = u.input_tokens / 1e6 * 5.00 + u.output_tokens / 1e6 * 25.00
print(f"actual:    {u.input_tokens} in, {u.output_tokens} out -&gt; ${actual:.5f}")</code></pre>
  <div class="check"><strong>Pass:</strong> your prediction lands within about 2× of the actual,
  and you can point at every number: which one you controlled (<code>max_tokens</code> is a
  ceiling, not a target), which one the model chose, and which one the counting endpoint got
  exactly right.</div>

  <h2>Stage 3 · Watch history get priced</h2>
  <p>The model is stateless — every turn re-sends the whole conversation (Lesson 0001). That
  sentence has a price. Run a three-turn conversation and watch input tokens climb even though
  each new question is short:</p>
<pre><code>messages = []
for question in [
    "Name three moons of Jupiter.",
    "Which of those is the largest?",
    "How was it discovered?",
]:
    messages.append({"role": "user", "content": question})
    response = client.messages.create(
        model="claude-opus-4-8", max_tokens=2000, messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})
    print(f"turn {len(messages) // 2}: input_tokens={response.usage.input_tokens}")</code></pre>
  <div class="check"><strong>Pass:</strong> input tokens grow every turn, and you can explain why
  turn 3 pays for turns 1 and 2 all over again. That growth curve is statelessness, priced —
  you'll watch it again in Lesson 0007 when you log an agent's full context every turn.</div>

  <div class="key"><strong>The load-bearing sentence:</strong> tokens are the currency of this
  whole field — every design decision in this course (what goes in context, when to retrieve,
  when to summarize, when to spawn a subagent) eventually shows up as a token line-item on
  somebody's bill.</div>

  <h2>Self-grade</h2>
  <button class="btn" onclick="document.getElementById('rubric').style.display='block'">Reveal grading rubric</button>
  <div id="rubric" class="key">
    You own this lesson when all three are true:
    <ul>
      <li><strong>You can estimate</strong> — given a paragraph, you predict its token count
      within ~25% before counting it</li>
      <li><strong>You can price a call</strong> — from input tokens, output tokens, and the two
      prices; nothing else needed</li>
      <li><strong>You can explain the curve</strong> — why input tokens grow every turn, in one
      sentence, starting from statelessness</li>
    </ul>
  </div>

  <h2>Next</h2>
  <p><a href="0006-anatomy-of-a-tool-call.html">Lesson 0006 — Anatomy of a Tool Call</a>: one
  complete tool round-trip by hand — you'll see that a "tool call" is just structured text the
  model proposes, and that you are the one who makes it real.</p>

  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://platform.claude.com/docs/en/build-with-claude/token-counting">Token counting — Claude Platform Docs</a> (the endpoint you just used) ·
    <a href="https://platform.claude.com/docs/en/pricing">current pricing</a>.<br>
    Reference: <a href="../reference/level-1-vocabulary.html">Level 1 Vocabulary</a> ·
    Sister lessons: <a href="0001-not-in-context-doesnt-exist.html">0001</a> · <a href="0006-anatomy-of-a-tool-call.html">0006</a><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
</main>
</body>
</html>
```

Note: inside `<pre><code>` blocks, `->` in Python output strings is written `-&gt;` above for HTML correctness — keep those entity escapes.

- [ ] **Step 3: Verify rendering and internal state**

Run: `python scripts/check_learning_links.py links`
Expected: exactly **one** failure — `0005-tokens-and-cost.html: broken link 0006-anatomy-of-a-tool-call.html` (created next task). Anything else is a bug in this task.
Open the file in a browser (`start learning\agentic-operations\lessons\0005-tokens-and-cost.html`) and confirm: styling matches sister lessons, the rubric button reveals the rubric, code blocks render with escapes resolved (`->` shows as an arrow, `&amp;` as `&`).

- [ ] **Step 4: Commit**

```bash
git add learning/agentic-operations/lessons/0005-tokens-and-cost.html
git commit -m "Add Lesson 0005 - Tokens & Cost (Level 1 warm-up lab, BYOK checkpoint moves here)"
```

---

### Task 5: New Lesson 0006 — Anatomy of a Tool Call

**Files:**
- Create: `learning/agentic-operations/lessons/0006-anatomy-of-a-tool-call.html`
- Reference (read-only): `lessons/0007-build-the-single-tool-agent.html` (head/style source)

**Interfaces:**
- Consumes: `0005-tokens-and-cost.html` (prerequisite link), `../reference/agent-loop-and-tool-call.html` (companion reference).
- Produces: page at `lessons/0006-anatomy-of-a-tool-call.html`; resolves Task 4's one expected broken link.

- [ ] **Step 1: Create the file scaffold**

Same head-copy procedure as Task 4 Step 1, with:
- Title lesson name/number: `Anatomy of a Tool Call` / `0006`.
- Description: `Dissect one tool-call round-trip by hand — the model proposes, you execute. Level 1 of the Agentic Operations course.`
- Canonical/og:url (if the pattern exists): `https://www.scottcurtner.com/learning/agentic-operations/lessons/0006-anatomy-of-a-tool-call.html`

- [ ] **Step 2: Write the body**

```html
<body>
<main>
  <p style="font-family:system-ui,sans-serif;font-size:.8rem;color:var(--muted);margin:0 0 1rem;"><a href="../../" style="color:var(--muted);">Learning</a> / <a href="../" style="color:var(--muted);">Agentic Operations</a> / Lesson 0006</p>
  <div class="kicker">Agentic Operations · Lesson 0006 · Level 1 · Foundations · Hands-on lab</div>
  <h1>Anatomy of a Tool Call</h1>
  <p class="lede">One round-trip, by hand: the model proposes, you execute — and this time, you are the tool.</p>

  <div class="win"><strong>Your win for this lesson:</strong> one complete tool-call round-trip
  executed manually in a Python REPL — no loop, no framework, no tool code. Prerequisites:
  <a href="0001-not-in-context-doesnt-exist.html">Lesson 0001</a> and
  <a href="0005-tokens-and-cost.html">Lesson 0005</a> (your key is set up). Companion reference:
  <a href="../reference/agent-loop-and-tool-call.html">The Agent Loop &amp; Tool-Call Round-Trip</a>.</div>

  <p>Before you build an agent (next lesson), slow the machinery down to one frame at a time. A
  "tool call" sounds like the model reaches out and runs your code. It doesn't. The model emits
  structured text saying what it would like run; your code decides whether and how to run it; you
  mail the result back. In this lesson you play the part of the code — by hand — so there is
  nowhere for that fact to hide. Open a REPL at the repo root with <code>uv run python</code> and
  keep it open for all four stages.</p>

  <h2>Stage 1 · Define the tool</h2>
  <p>A tool definition is three things: a name, a description, and a JSON Schema for the input.
  The description is a prompt — it should say <em>when</em> to call the tool, not just what it
  does:</p>
<pre><code>import anthropic
client = anthropic.Anthropic()

TOOLS = [{
    "name": "calculator",
    "description": "Evaluate one arithmetic expression. Call this for every "
                   "arithmetic step; do not do mental math.",
    "input_schema": {
        "type": "object",
        "properties": {"expression": {"type": "string"}},
        "required": ["expression"],
    },
}]</code></pre>
  <div class="check"><strong>Pass:</strong> you can say what each of the three parts is for, and
  why the description says "do not do mental math" instead of just "evaluates arithmetic."</div>

  <h2>Stage 2 · Trigger the proposal</h2>
<pre><code>messages = [{"role": "user", "content": "What is 137 * 41?"}]
response = client.messages.create(
    model="claude-opus-4-8", max_tokens=2000,
    tools=TOOLS, messages=messages,
)
print(response.stop_reason)          # tool_use
block = next(b for b in response.content if b.type == "tool_use")
print(block.id, block.name, block.input)</code></pre>
  <p>Stop and look. <code>stop_reason == "tool_use"</code> means the model has paused mid-turn,
  waiting on you. The block carries an <code>id</code> (a claim ticket), a <code>name</code>
  (which tool), and an <code>input</code> (the arguments). Nothing has been computed. No code has
  run anywhere. This is a proposal, written in JSON.</p>
  <div class="check"><strong>Pass:</strong> you can point at the id, the name, and the input —
  and say out loud what has <em>not</em> happened yet.</div>

  <h2>Stage 3 · Be the tool</h2>
  <p>Normally your code would execute the expression. Today you are the code: work out 137 × 41
  yourself, then hand the answer back as a <code>tool_result</code> whose
  <code>tool_use_id</code> matches the proposal's id:</p>
<pre><code>messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": [{
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": "5617",
}]})
final = client.messages.create(
    model="claude-opus-4-8", max_tokens=2000,
    tools=TOOLS, messages=messages,
)
print(final.stop_reason)             # end_turn
print(next(b.text for b in final.content if b.type == "text"))</code></pre>
  <div class="check"><strong>Pass:</strong> the model answers using <em>your</em> number. You
  just performed, by hand, every step your agent code will automate in Lesson 0007: execute the
  proposal, append the assistant content verbatim, append a matching tool_result, call again.</div>

  <h2>Stage 4 · Break the contract</h2>
  <p>The id-matching isn't a convention — the API enforces it. Rebuild the same follow-up with a
  wrong id and watch the request get refused outright:</p>
<pre><code>bad = messages[:-1] + [{"role": "user", "content": [{
    "type": "tool_result",
    "tool_use_id": "toolu_bogus",
    "content": "5617",
}]}]
client.messages.create(model="claude-opus-4-8", max_tokens=2000,
                       tools=TOOLS, messages=bad)
# anthropic.BadRequestError (HTTP 400): the tool_use id has no matching result</code></pre>
  <div class="check"><strong>Pass:</strong> you get a 400 error, not a confused answer. Every
  proposal must be answered by id — that enforced contract is what makes the loop in the
  reference sheet reliable.</div>

  <div class="key"><strong>The load-bearing sentence:</strong> the model only ever proposes;
  execution always happens on your side of the wire — which is why reliability (bounded loops,
  errors returned as results) and security (never trust the model's input to a tool) are your
  code's job, not the model's.</div>

  <h2>Self-grade</h2>
  <button class="btn" onclick="document.getElementById('rubric').style.display='block'">Reveal grading rubric</button>
  <div id="rubric" class="key">
    You own this lesson when:
    <ul>
      <li><strong>You can narrate the round-trip</strong> — send, propose, execute, append,
      resend — without notes</li>
      <li><strong>You can say what a tool_use block is</strong> — structured text with a
      claim-ticket id, not an action</li>
      <li><strong>You can predict the failure</strong> — what happens when the id doesn't match,
      and why the API enforces it</li>
    </ul>
  </div>

  <h2>Next</h2>
  <p><a href="0007-build-the-single-tool-agent.html">Lesson 0007 — Build the Single-Tool
  Agent</a>: do it in code, with a loop — ship the agent that automates the round-trip you just
  performed by hand, and log the world it sees on every turn.</p>

  <footer>
    <strong>Primary source for this lesson:</strong>
    <a href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview">Tool use with Claude — Claude Platform Docs</a> (read "How tool use works" — it is the round-trip you just did by hand).<br>
    Reference: <a href="../reference/agent-loop-and-tool-call.html">Agent Loop &amp; Tool-Call Round-Trip</a> · <a href="../reference/level-1-vocabulary.html">Level 1 Vocabulary</a> ·
    Sister lessons: <a href="0005-tokens-and-cost.html">0005</a> · <a href="0007-build-the-single-tool-agent.html">0007</a><br><br>
    Stuck or curious? Ask your teaching agent — follow-up questions are part of the method, not an interruption.
  </footer>
</main>
</body>
</html>
```

- [ ] **Step 3: Verify**

Run: `python scripts/check_learning_links.py links`
Expected: `0 failure(s)` (Task 4's dangling link now resolves).
Open in a browser; confirm styling, rubric button, and code rendering.

- [ ] **Step 4: Commit**

```bash
git add learning/agentic-operations/lessons/0006-anatomy-of-a-tool-call.html
git commit -m "Add Lesson 0006 - Anatomy of a Tool Call (manual round-trip lab)"
```

---

### Task 6: Rewire the build lesson (0007) around the warm-ups

**Files:**
- Modify: `learning/agentic-operations/lessons/0007-build-the-single-tool-agent.html`

- [ ] **Step 1: Replace Checkpoint 0 with a short key check**

Find the whole `<h2>Checkpoint 0 · Bring your own key</h2>` section (heading through its `<div class="check">…</div>`) and replace with:

```html
  <h2>Checkpoint 0 · Key check</h2>
  <p>Your Anthropic API key should already be set from
  <a href="0005-tokens-and-cost.html">Lesson 0005 — Tokens &amp; Cost</a>. Verify without
  printing the secret:</p>
<pre><code>uv run python -c "from dotenv import dotenv_values; print('ANTHROPIC_API_KEY' in dotenv_values('.env'))"</code></pre>
  <div class="check"><strong>Pass:</strong> prints <code>True</code>. If it doesn't, do Lesson
  0005's Checkpoint 0 first. This build spends a few thousand tokens per run — pennies on the
  prices you learned there.</div>
```

- [ ] **Step 2: Callbacks in Stage 1 and Stage 2**

In Stage 1, replace the sentence fragment
`and the usage object prices the call in tokens —
  the unit everything in this field is denominated in.`
with
`and the usage object prices the call in tokens —
  the unit you learned to count and price in Lesson 0005.`

In Stage 2, replace
`<p>Add the calculator tool definition (see the reference sheet for the exact schema) and a`
with
`<p>Add the calculator tool definition — the same schema you dissected in Lesson 0006 (exact
  version also on the reference sheet) — and a`

- [ ] **Step 3: Update the win-box prerequisites**

Replace
```html
  built and ran, plus a per-turn context log you have personally read. Prerequisite:
  <a href="0001-not-in-context-doesnt-exist.html">Lesson 0001</a>. Companion reference:
```
with
```html
  built and ran, plus a per-turn context log you have personally read. Prerequisites:
  <a href="0001-not-in-context-doesnt-exist.html">Lesson 0001</a>,
  <a href="0005-tokens-and-cost.html">0005</a> and
  <a href="0006-anatomy-of-a-tool-call.html">0006</a>. Companion reference:
```

- [ ] **Step 4: Update the sister-lessons footer line**

The footer's sister-lessons line currently links 0001 and 0008 (post-renumber). Replace it with:

```html
    Sister lessons: <a href="0006-anatomy-of-a-tool-call.html">0006</a> · <a href="0008-break-it-on-purpose.html">0008</a><br><br>
```

- [ ] **Step 5: Verify**

Run: `python scripts/check_learning_links.py links`
Expected: `0 failure(s)`.
Then `grep -n "Bring your own key" learning/agentic-operations/lessons/*.html` — expected: only `0005-tokens-and-cost.html` matches.

- [ ] **Step 6: Commit**

```bash
git add learning/agentic-operations/lessons/0007-build-the-single-tool-agent.html
git commit -m "Build lesson assumes the warm-ups: key check replaces BYOK, callbacks to 0005/0006"
```

---

### Task 7: Broken tags, next-lesson links in 0001–0004, congratulations in 0018

**Files:**
- Modify: the ~10 lesson files containing `<\a>`; `lessons/0001-…`, `0002-…`, `0003-…`, `0004-…`; `lessons/0018-the-improvement-loop.html`

- [ ] **Step 1: Fix every malformed closing anchor tag**

Replace the literal string `<\a>` with `</a>` in every lesson file that has it (grep first: `grep -rln '<\\a>' learning`). A one-liner works:

```bash
grep -rl '<\\a>' learning --include="*.html" | xargs sed -i 's|<\\a>|</a>|g'
```

Run: `python scripts/check_learning_links.py tags` — expected `0 failure(s)`.

- [ ] **Step 2: Rewrite Lesson 0001's Next section**

In `0001-not-in-context-doesnt-exist.html`, replace the paragraph after `<h2>Next</h2>` (the stale "Tokens &amp; Cost … Anatomy of a Tool Call … single-tool agent" text) with:

```html
  <p>Next in the foundations:
  <a href="0002-match-the-pattern-to-the-problem.html">Lesson 0002 — Match the Pattern to the
  Problem</a> — every design choice is a justified answer to "what goes in the window, and why?"
  And when you reach the Level 1 practice ladder,
  <a href="0005-tokens-and-cost.html">Lesson 0005 — Tokens &amp; Cost</a> delivers on this
  lesson's promise: you'll tokenize real text and read cost off a real API response.</p>
```

- [ ] **Step 3: Add the next link to Lesson 0002**

In `0002-match-the-pattern-to-the-problem.html`, after the existing Next paragraph (ending `…doesn't pass the Level 1 gate.</p>`), append:

```html
  <p>Next: <a href="0003-traces-before-prompts.html">Lesson 0003 — Traces Before Prompts</a>.</p>
```

- [ ] **Step 4: Add the explicit next link to Lesson 0003**

In `0003-traces-before-prompts.html`, after the existing Next paragraph (the one that already mentions Own the Feedback Loop mid-sentence), append:

```html
  <p>Next: <a href="0004-own-the-feedback-loop.html">Lesson 0004 — Own the Feedback Loop</a>.</p>
```

- [ ] **Step 5: Add the next link to Lesson 0004**

In `0004-own-the-feedback-loop.html`, after the existing Next paragraph (ending `…each gate passes on demonstrated capability, not coverage.</p>`), append:

```html
  <p>Next: <a href="0005-tokens-and-cost.html">Lesson 0005 — Tokens &amp; Cost</a> — the first
  rung of the practice ladder.</p>
```

- [ ] **Step 6: Congratulations block in Lesson 0018**

`0018-the-improvement-loop.html` has no Next section (it was the last lesson). Immediately before its `<footer>`, insert:

```html
  <h2>You've finished the course</h2>
  <div class="key"><strong>Congratulations.</strong> This was the final lesson — all 18 lessons,
  all four level gates: you can explain why "not in context = doesn't exist," you've shipped and
  broken a real agent, you've justified pattern choices, debugged from traces alone, caught a
  planted regression, and run the full observe → fix → verify loop with your own SLOs. That's the
  whole map. From here, the course's habits belong in your real systems — and the
  <a href="../">course index</a> and reference sheets stay put whenever you want to revisit a
  rung of the ladder.</div>
```

- [ ] **Step 7: Verify the full Next chain**

Run: `python scripts/check_learning_links.py`
Expected: `0 failure(s)` on all three checks.
Then verify every lesson 0001–0017 has a link to its numeric successor in its Next section, and 0018 has the congratulations block:

```bash
python - <<'EOF'
import pathlib, re
lessons = sorted(pathlib.Path("learning/agentic-operations/lessons").glob("[0-9]*.html"))
names = [p.name for p in lessons]
assert len(names) == 18, names
for i, p in enumerate(lessons[:-1]):
    nxt = names[i + 1]
    text = p.read_text(encoding="utf-8")
    assert nxt in text, f"{p.name} does not link to {nxt}"
final = lessons[-1].read_text(encoding="utf-8")
assert "Congratulations" in final, "0018 missing congratulations"
print("next-chain OK: 17 links + congratulations present")
EOF
```
Expected: `next-chain OK: 17 links + congratulations present`.

- [ ] **Step 8: Commit**

```bash
git add learning/agentic-operations/lessons
git commit -m "Fix broken closing anchors, wire next-lesson links through foundations, congratulate at 0018"
```

---

### Task 8: Course index, learning index, sitemap

**Files:**
- Modify: `learning/agentic-operations/index.html`, `learning/index.html`, `sitemap.xml`

- [ ] **Step 1: Insert the two new lessons into the Level 1 ladder**

In `learning/agentic-operations/index.html`, the Level 1 roadmap list already shows 0007/0008 (renumbered in Task 2). Insert two `<li>` entries above them so the block reads:

```html
  <h3>Level 1 · Foundations</h3>
  <p class="level-status"><a href="reference/level-1-vocabulary.html">Level 1 Vocabulary</a></p>
  <ul class="roadmap">
    <li><span class="done">&#10003;</span><a href="lessons/0005-tokens-and-cost.html">0005 — Tokens &amp; Cost</a></li>
    <li><span class="done">&#10003;</span><a href="lessons/0006-anatomy-of-a-tool-call.html">0006 — Anatomy of a Tool Call</a></li>
    <li><span class="done">&#10003;</span><a href="lessons/0007-build-the-single-tool-agent.html">0007 — Build the Single-Tool Agent</a></li>
    <li><span class="done">&#10003;</span><a href="lessons/0008-break-it-on-purpose.html">0008 — Break It on Purpose</a> <span class="gate-tag">(gate)</span></li>
  </ul>
```

(Only the two new `<li>` lines are added; everything else should already match — if it doesn't, Task 2 missed something: stop and investigate.)

- [ ] **Step 2: Update the course card count**

In `learning/index.html`, change `<span class="status">16 lessons live</span>` to `<span class="status">18 lessons live</span>`.

- [ ] **Step 3: Sitemap — add the two new lessons and refresh lastmod**

In `sitemap.xml` (lesson URLs were renumbered by Task 2):
1. Add two new `<url>` entries after the `0004-own-the-feedback-loop.html` entry, following the existing entry format, `changefreq` `monthly`, `priority` `0.7`, `lastmod` `2026-07-13`:
   - `https://www.scottcurtner.com/learning/agentic-operations/lessons/0005-tokens-and-cost.html`
   - `https://www.scottcurtner.com/learning/agentic-operations/lessons/0006-anatomy-of-a-tool-call.html`
2. Set `<lastmod>2026-07-13</lastmod>` on every URL under `https://www.scottcurtner.com/learning/` (they all changed: renamed, term-swept, or link-rewired).

- [ ] **Step 4: Verify sitemap ↔ file tree correspondence**

```bash
python - <<'EOF'
import pathlib, re
sm = pathlib.Path("sitemap.xml").read_text(encoding="utf-8")
urls = set(re.findall(r"<loc>https://www\.scottcurtner\.com/(learning/[^<]+)</loc>", sm))
disk = set()
for p in pathlib.Path("learning").rglob("*.html"):
    rel = p.as_posix()
    disk.add(rel[:-len("index.html")] if rel.endswith("index.html") else rel)
missing_from_sitemap = disk - urls
missing_from_disk = urls - disk
assert not missing_from_disk, f"sitemap URLs with no file: {missing_from_disk}"
assert not missing_from_sitemap, f"files not in sitemap: {missing_from_sitemap}"
print(f"sitemap OK: {len(urls)} learning URLs match disk")
EOF
```
Expected: `sitemap OK: 25 learning URLs match disk` (2 index pages + 18 lessons + 5 reference pages).

- [ ] **Step 5: Commit**

```bash
git add learning/agentic-operations/index.html learning/index.html sitemap.xml
git commit -m "Index and sitemap: 18 lessons live, Level 1 ladder gains 0005/0006"
```

---

### Task 9: Internal planning docs

**Files:**
- Modify: `learning/agentic-operations/NOTES.md`
- Verify only: `MISSION.md`, `RESOURCES.md`, `learning-records/*.md` (paths already corrected by Task 2's replacement; M-terms stay)

- [ ] **Step 1: Update the numbering-convention line**

In `NOTES.md`, replace:
```
Lesson numbers are workspace-sequential, assigned at write time (0001 = M1 mental model, 0002 = M2 pattern map). Arcs below use slugs, not numbers.
```
with:
```
Lesson numbers match reading order as of 2026-07-13 (originally workspace-sequential; renumbered when the Level 1 warm-ups were added — see update note below). Arcs below use slugs, not numbers.
```

- [ ] **Step 2: Append the un-collapse update note**

Immediately after the `ALL 16 LESSONS BUILT 2026-07-03 …` paragraph, add:

```
2026-07-13 UPDATE: un-collapsed the M1 warm-ups per Scott's request — dedicated `0005-tokens-and-cost.html` and `0006-anatomy-of-a-tool-call.html` built as full practice lessons (the BYOK checkpoint moved into 0005; the build lesson keeps a short key check). All lessons renumbered to reading order: old 0005–0016 became 0007–0018; old URLs 404 by design (clean break, no redirects — Scott's call). Count is now 18 (4 theory spine + 14 hands-on). Learner-facing pages say "Level 1–4"; M1–M4 remain internal shorthand here (M1 = Level 1, M2 = Level 2, M3 = Level 3, M4 = Level 4). Reference sheets renamed m*-core-vocabulary.html → level-*-vocabulary.html; exercise script renamed m1_agent.py → level1_agent.py.
```

- [ ] **Step 3: Add the two new lessons to the M1 arc list**

In the `**M1**` block (whose existing entries Task 2 already renumbered to 0007/0008), insert above the build-lesson line:

```
- `0005-tokens-and-cost.html` — tokenize real text + predict-then-spend cost lab; BYOK checkpoint 0 (DONE 2026-07-13)
- `0006-anatomy-of-a-tool-call.html` — one manual tool round-trip: propose/execute/append/resend + break-the-contract 400 (DONE 2026-07-13)
```

- [ ] **Step 4: Verify the other internal docs need no edits**

Run: `grep -nE "0005-build|0006-break|m1_agent|m[1-4]-core" learning/agentic-operations/MISSION.md learning/agentic-operations/RESOURCES.md learning/agentic-operations/learning-records/*.md`
Expected: no matches (Task 2 handled any path references). M1–M4 terms in these files are expected and stay.

- [ ] **Step 5: Verify `level1_agent.py` still self-tests**

Run: `uv run learning/agentic-operations/exercises/level1_agent.py --selftest`
Expected: self-test PASSED output (offline path; no API key needed). If `uv` is unavailable in this environment, run `python learning/agentic-operations/exercises/level1_agent.py --selftest` and note which interpreter was used.

- [ ] **Step 6: Commit**

```bash
git add learning/agentic-operations/NOTES.md
git commit -m "NOTES: record the un-collapse, renumber, and Level naming decisions"
```

---

### Task 10: Full verification pass

**Files:**
- No new files. Read-only verification of everything above.

- [ ] **Step 1: Full checker**

Run: `python scripts/check_learning_links.py`
Expected: `0 failure(s)` — links, tags, and terms all clean.

- [ ] **Step 2: Repo-wide stale-reference grep**

```bash
grep -rnE "0005-build-the|0006-break-it|0007-structured|0008-react|0009-rag-build|0010-episodic|0011-orchestrator|0012-tracing|0013-critic|0014-slo|0015-guardrails|0016-the-improvement|m[1-4]-core-vocabulary|m1_agent" . \
  --include="*.html" --include="*.md" --include="*.py" --include="*.xml" \
  | grep -v "docs/superpowers" | grep -v ".superpowers"
```
Expected: no output (the spec/plan docs and prior sdd transcripts are the only allowed holders of old names).

- [ ] **Step 3: Next-chain and sitemap re-checks**

Re-run the Task 7 Step 7 script and the Task 8 Step 4 script. Both must pass.

- [ ] **Step 4: Human-quality read-through**

Read both new lessons end-to-end in a browser plus lessons 0001, 0002, 0007, and 0018 (highest-churn pages). Check: prose reads in the course voice, no "Level 1"-substitution artifacts, code blocks are copy-pasteable (entities render as `->`, `&`), rubric buttons work, every Next link goes where its text says.

- [ ] **Step 5: Confirm clean tree**

Run: `git status`
Expected: clean working tree (every change committed under Tasks 1–9). Do **not** push — Scott decides when to publish (post-push, memory says verify pages + sitemap live via Tavily).
