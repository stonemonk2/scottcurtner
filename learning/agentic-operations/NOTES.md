# Teaching Notes — Agentic Operations

## Learner profile
- Scott builds and operates Vernant (agentic analytical pipeline: Python/PydanticAI/Temporal) and works inside Claude Code daily — an expert practitioner *user* of agents formalizing the foundations.
- Implication for ZPD: vocabulary can move fast; anchor every abstract concept to something he already sees daily (session compaction, context windows filling up, tool permission prompts).

## Open questions to confirm with Scott
- Mission "Why" was derived from the source doc + the /teach invocation, not interviewed. Confirm: is this arc for his own mastery, for onboarding future hires (the doc is written as a new-hire rubric), or both? Affects how much emphasis to put on "can teach it" vs "can apply unprompted."

## Planned lesson arcs
Lesson numbers match reading order as of 2026-07-13 (originally workspace-sequential; renumbered when the Level 1 warm-ups were added — see update note below). Arcs below use slugs, not numbers.

ALL 16 LESSONS BUILT 2026-07-03 (4 theory spine + 12 hands-on). Collapsed the M1 tokens/tool-call warm-ups into the build lesson (just-in-time theory) per the plan; realized count is 16, not the earlier 19–21 estimate. Each hands-on lesson ends with a self-grade rubric; each milestone's last hands-on lesson folds in the readiness check.

2026-07-13 UPDATE: un-collapsed the M1 warm-ups per Scott's request — dedicated `0005-tokens-and-cost.html` and `0006-anatomy-of-a-tool-call.html` built as full practice lessons (the BYOK checkpoint moved into 0005; the build lesson keeps a short key check). All lessons renumbered to reading order: old 0005–0016 became 0007–0018; old URLs 404 by design (clean break, no redirects — Scott's call). Count is now 18 (4 theory spine + 14 hands-on). Learner-facing pages say "Level 1–4"; M1–M4 remain internal shorthand here (M1 = Level 1, M2 = Level 2, M3 = Level 3, M4 = Level 4). Reference sheets renamed m*-core-vocabulary.html → level-*-vocabulary.html; exercise script renamed m1_agent.py → level1_agent.py.

**M1** (gate: explain "not in context = doesn't exist" + ship a reliable single-tool agent):
- `0001-not-in-context-doesnt-exist.html` — core mental model + Cluster A vocabulary (DONE)
- `0005-tokens-and-cost.html` — tokenize real text + predict-then-spend cost lab; BYOK checkpoint 0 (DONE 2026-07-13)
- `0006-anatomy-of-a-tool-call.html` — one manual tool round-trip: propose/execute/append/resend + break-the-contract 400 (DONE 2026-07-13)
- `0007-build-the-single-tool-agent.html` — guided build; prereqs 0005/0006 (tokens/cost, tool-call anatomy) now taught there, so checkpoint 0 here is just a short key check; logs full per-turn context (DONE). Working script: `exercises/level1_agent.py` (self-test PASSED; live path needs a key)
- `0008-break-it-on-purpose.html` — context-overflow lab + vague-prompt-three-ways + M1 readiness check (DONE)

**M2** (gate: build a grounded multi-step agent and justify each pattern choice — learning record 0001):
- `0002-match-the-pattern-to-the-problem.html` — M2 decision map (DONE)
- `0009-structured-prompting-and-the-injection-lab.html` — structured rewrite + injection attack/defend (DONE)
- `0010-react-multi-hop-build.html` — ReAct multi-hop w/ logged thought/action/observation (DONE)
- `0011-rag-build-and-break.html` — RAG pipeline + chunking-collapse lab (DONE)
- `0012-episodic-memory.html` — recall-a-past-run build + M2 readiness check (DONE)

**M3** (gate: debug from traces alone + eval catches a planted regression — learning record 0002):
- `0003-traces-before-prompts.html` — M3 decision map (DONE)
- `0013-orchestrator-bakeoff.html` — orchestrator vs single, settled with traces (DONE)
- `0014-tracing-and-planted-regression.html` — trace instrumentation + planted-regression eval (DONE)
- `0015-critic-verifier-step.html` — verifier step, measured silent-wrong reduction + M3 readiness check (DONE)

**M4** (gate: own SLOs + independently run observe→fix→verify — learning record 0002):
- `0004-own-the-feedback-loop.html` — M4 map (DONE)
- `0016-slo-dashboard.html` — four-SLO dashboard from real traces (DONE)
- `0017-guardrails-and-hitl.html` — least-privilege scoping + injection defense + HITL checkpoint by risk (DONE)
- `0018-the-improvement-loop.html` — full observe→fix→verify capstone + M4 readiness check (DONE)

**Reference sheets:** level-1/2/3/4-vocabulary.html + agent-loop-and-tool-call.html (code, built with 0007). All cross-linked.

**Blocker for the learner:** repo `.env` has NO Anthropic key (verified 2026-07-03: dotenv_values shows no ANTHROPIC_* key; ant CLI not installed). Lesson 0005 checkpoint 0 walks adding `ANTHROPIC_API_KEY` to `.env` (0007 checkpoint 0 just re-verifies it's set). Until then the hands-on runs can't execute live; `level1_agent.py --selftest` works offline.

**BYOK public version scaffolded 2026-07-03.** The workspace is now publishable as a standalone public repo without exposing Scott's tokens. Added: `.env.example` (blank key + Console link), `README.md` (BYOK contract + quick start), `.gitignore` (ignores `.env`, run artifacts, `__pycache__`). `level1_agent.py` now walks up from its own dir to find the nearest `.env` (`_load_env()`) instead of the Vernant-specific `parents[4]` path, so it runs in both the monorepo and a lifted-out repo. Lesson 0007 checkpoint 0 rewritten for a public/BYOK audience (`cp .env.example .env`, key-never-committed note); as of the 2026-07-13 un-collapse this content now lives in Lesson 0005 checkpoint 0. Distribution decision was BYOK (learner runs on their own key) — recommended over a hosted proxy/static-only; a key must never reach client-side code or a committed repo.

## Preferences observed
- Scott approved the M1 package format ("this was great!", 2026-07-03) — keep the structure: printable reference sheet + short lesson + closed-book quiz + own-words rubric, sister styling across milestones.
