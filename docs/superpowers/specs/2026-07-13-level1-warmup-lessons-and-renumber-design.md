# Design: Level 1 warm-up lessons, course renumbering, and M→Level rename

**Date:** 2026-07-13
**Course:** `learning/agentic-operations/` on scottcurtner.com
**Approved by:** Scott (conversation, 2026-07-13)

## Why

Lesson 0001's "Next" section promises two lessons — "Tokens & Cost" and "Anatomy of a
Tool Call" — that were never built. `NOTES.md` records they were deliberately collapsed
into the build lesson, but Scott wants them as real lessons: dedicated hands-on warm-up
labs that the build lesson then assumes. At the same time, learner-facing pages still use
internal milestone names (M1–M4) that the course index already translates as Level 1–4,
several lessons lack next-lesson links, and ten lessons have malformed `<\a>` closing
tags.

## Decisions (all confirmed with Scott)

1. **Terminology:** every learner-facing "M#" becomes "Level #" ("M1 gate" → "Level 1
   gate", "M2 vocabulary" → "Level 2 vocabulary").
2. **Add both lessons** as full-weight hands-on labs in the approved lesson format (win
   box, staged exercises with pass checks, key box, self-grade rubric, Next link,
   primary-source footer, sister styling).
3. **Renumber all lessons** so filenames match reading order. No redirect stubs — old
   URLs 404 (clean break).
4. **Rename M-numbered files too:** the four vocabulary reference pages and the exercise
   script.

## New reading order and renumber map

Foundations (unchanged files): 0001 → 0002 → 0003 → 0004.
Then the practice ladder:

| New number | File | Status |
|---|---|---|
| 0005 | `lessons/0005-tokens-and-cost.html` | **new** |
| 0006 | `lessons/0006-anatomy-of-a-tool-call.html` | **new** |
| 0007 | `lessons/0007-build-the-single-tool-agent.html` | was 0005 |
| 0008 | `lessons/0008-break-it-on-purpose.html` | was 0006 · Level 1 gate |
| 0009 | `lessons/0009-structured-prompting-and-the-injection-lab.html` | was 0007 |
| 0010 | `lessons/0010-react-multi-hop-build.html` | was 0008 |
| 0011 | `lessons/0011-rag-build-and-break.html` | was 0009 |
| 0012 | `lessons/0012-episodic-memory.html` | was 0010 · Level 2 gate |
| 0013 | `lessons/0013-orchestrator-bakeoff.html` | was 0011 |
| 0014 | `lessons/0014-tracing-and-planted-regression.html` | was 0012 |
| 0015 | `lessons/0015-critic-verifier-step.html` | was 0013 · Level 3 gate |
| 0016 | `lessons/0016-slo-dashboard.html` | was 0014 |
| 0017 | `lessons/0017-guardrails-and-hitl.html` | was 0015 |
| 0018 | `lessons/0018-the-improvement-loop.html` | was 0016 · Level 4 gate |

File renames outside `lessons/`:

- `reference/m1-core-vocabulary.html` → `reference/level-1-vocabulary.html` (same for
  m2/m3/m4 → level-2/3/4)
- `reference/agent-loop-and-tool-call.html` — unchanged
- `exercises/m1_agent.py` → `exercises/level1_agent.py` (docstring/comment M-terms also
  become Level 1; script behavior unchanged)

## New lesson 0005 — Tokens & Cost

Slug: `0005-tokens-and-cost.html`. Kicker: `Agentic Operations · Lesson 0005 · Level 1 ·
Foundations · Hands-on lab`. Prerequisite: Lesson 0001. Delivers 0001's promise:
"tokenize real text and read cost off a real API response."

- **Checkpoint 0 — Bring your own key.** Moved verbatim-in-spirit from the current build
  lesson (BYOK contract, `.env` setup, verify-without-printing check). This is now the
  first lesson that needs a key.
- **Stage 1 — Count tokens without spending.** Use the token-counting endpoint (free) on
  real text: a prose paragraph, a code snippet, a string of numbers. Pass: state the
  counts and explain why tokens ≠ words (~4 chars/token English prose; code and unusual
  text tokenize worse).
- **Stage 2 — Predict, then spend.** Estimate one small call's cost from the model's
  price sheet ($5 / $25 per MTok input/output for `claude-opus-4-8`, matching existing
  lesson copy), make the call, read `usage.input_tokens` / `usage.output_tokens`, compute
  actual dollars. Pass: prediction within ~2×; can point at every usage field.
- **Stage 3 — Watch history get priced.** Run a 3-turn conversation, appending each
  response; watch input tokens climb per turn. Pass: explain why turn 3's input is
  bigger than turn 1's even though the new question is short. (Sets up the build
  lesson's context-log stage.)
- **Key box:** tokens are the unit every design decision in this course is eventually
  denominated in.
- **Self-grade rubric** + **Next** → Lesson 0006.
- **Footer:** primary source = Anthropic token-counting docs + pricing page; reference =
  Level 1 Vocabulary; sister lessons 0001 · 0006.

## New lesson 0006 — Anatomy of a Tool Call

Slug: `0006-anatomy-of-a-tool-call.html`. Same kicker pattern. Prerequisites: 0001 and
0005 (key). Companion: the Agent Loop & Tool-Call Round-Trip reference sheet (which
stays the code-skeleton cheat sheet; this lesson is the by-hand dissection — one
round-trip, no loop, no script: the learner is the tool).

- **Stage 1 — Define the tool.** The calculator schema; the description is a prompt
  (say *when* to call, not just what it does).
- **Stage 2 — Trigger the proposal.** Send the arithmetic question with `tools=` set;
  get `stop_reason == "tool_use"`; print and read the block: `id`, `name`, `input`.
  Pass: articulate that nothing has been computed — this is text the model proposed.
- **Stage 3 — Be the tool.** Compute the answer yourself, hand-write the `tool_result`
  block with the matching `tool_use_id`, send it back, get `end_turn`. Pass: final
  answer arrives and you performed every step your future agent code will automate.
- **Stage 4 — Break the contract.** Send a mismatched `tool_use_id` (or omit the
  result) and read the API error. Pass: explain that the protocol is enforced by the
  API, not a convention.
- **Key box:** the model only ever proposes; execution always happens on your side of
  the wire — which is where reliability and security live.
- **Self-grade rubric** + **Next** → Lesson 0007 ("now do it in code, with a loop").
- **Footer:** primary source = "How tool use works" (Claude tool-use docs); reference =
  Agent Loop & Tool-Call Round-Trip + Level 1 Vocabulary; sister lessons 0005 · 0007.

Exact SDK call signatures in both lessons are verified against the claude-api reference
skill during implementation, not trusted from memory.

## Changes to existing pages

- **Build lesson (new 0007):** Checkpoint 0 shrinks to a one-line "key set in Lesson
  0005 — verify" check; Stage 1's token-usage aside and Stage 2's schema intro gain
  one-line callbacks to 0005/0006. Lede's "second half of the M1 gate" reworded to
  Level 1 phrasing.
- **M→Level sweep:** all learner-facing HTML under `learning/` (16 existing lessons,
  course index, 5 reference pages) — every `M1`–`M4` term becomes `Level 1`–`Level 4`
  with natural phrasing ("the M2 hands-on arc" → "the Level 2 hands-on arc"; "the
  M1/0007 lesson" → "the Level 1/0009 lesson", renumbered).
- **Lesson-number references:** every in-text mention, sister-lesson footer,
  prerequisite link, and `<title>`/kicker/canonical/og-url (where present) updated to the new numbers
  (found exhaustively by grep, e.g. "the 0013 verifier" → 0015, "your 0012 evals" →
  0014).
- **Next-lesson links:** every lesson's Next section links its successor:
  0001→0002→0003→0004→0005→…→0018. 0001's stale paragraph (naming the never-built
  lessons) is rewritten to point at 0002 and mention the Level 1 practice ladder now
  starting at 0005. 0003's Next keeps its prose but gains the explicit next link to
  0004. Broken `<\a>` closing tags (ten lessons) fixed to `</a>`.
- **0018 (The Improvement Loop):** the Next section becomes a congratulations block —
  all 18 lessons and all four level gates complete — pointing back to the course index
  and suggesting where to apply the skills next. No next link.
- **Course index (`agentic-operations/index.html`):** Level 1 ladder lists 0005, 0006,
  0007, 0008 (gate on 0008); later levels renumbered; vocabulary links point at renamed
  files; new lessons marked live (✓).
- **Learning index (`learning/index.html`):** "16 lessons live" → "18 lessons live".
- **`sitemap.xml`:** two entries added, twelve lesson URLs rewritten, and the four
  vocabulary URLs rewritten if present (check the sitemap's current coverage first).
- **Internal docs (`NOTES.md`, `MISSION.md`, `RESOURCES.md`, `learning-records/`,
  `README.md`, `.env.example`):** file paths and lesson numbers corrected everywhere.
  `README.md` and `.env.example` are public-repo-facing, so their M-terms also become
  Level terms. NOTES/MISSION/RESOURCES/learning-records keep M1–M4 milestone language
  (it maps to the private knowledge-map source doc); NOTES.md gains one line: "M1–M4
  (internal) = Level 1–4 (published)." NOTES.md's planned-lesson list is updated to
  reflect the un-collapse (0005/0006 built 2026-07-13, count now 18).

## Verification (before claiming done)

1. Link check: script walks every HTML file under `learning/` and asserts every
   relative `href`/`src` resolves to an existing file.
2. `grep -E '\bM[1-4]\b'` over `learning/**/*.html` returns zero matches.
3. Grep for all old filenames (12 lessons, 4 vocab pages, `m1_agent`) over the repo
   returns zero matches outside `docs/superpowers/` and git history.
4. `grep '<\\a>'` over `learning/` returns zero matches.
5. `sitemap.xml` entries correspond 1:1 with the HTML files under `learning/` that were
   listed before, plus the two new lessons.
6. Both new lessons read end-to-end for copy quality; API snippets checked against the
   claude-api reference skill; new pages render (styles/quiz buttons) in a browser.

## Out of scope

- No redirect stubs (explicit clean-break decision).
- No changes to articles or other site sections.
- No new reference sheets; `agent-loop-and-tool-call.html` content untouched except the
  M→Level sweep, renumbered lesson references, and renamed script path.
- Git push / publish: commit locally; Scott decides when to push (post-publish
  verification per memory: confirm pages + sitemap live via Tavily after push).
