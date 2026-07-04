# Teaching Notes — Agentic Operations

## Learner profile
- Scott builds and operates Vernant (agentic analytical pipeline: Python/PydanticAI/Temporal) and works inside Claude Code daily — an expert practitioner *user* of agents formalizing the foundations.
- Implication for ZPD: vocabulary can move fast; anchor every abstract concept to something he already sees daily (session compaction, context windows filling up, tool permission prompts).

## Open questions to confirm with Scott
- Mission "Why" was derived from the source doc + the /teach invocation, not interviewed. Confirm: is this arc for his own mastery, for onboarding future hires (the doc is written as a new-hire rubric), or both? Affects how much emphasis to put on "can teach it" vs "can apply unprompted."

## Planned lesson arcs
Lesson numbers are workspace-sequential, assigned at write time (0001 = M1 mental model, 0002 = M2 pattern map). Arcs below use slugs, not numbers.

ALL 16 LESSONS BUILT 2026-07-03 (4 theory spine + 12 hands-on). Collapsed the M1 tokens/tool-call warm-ups into the build lesson (just-in-time theory) per the plan; realized count is 16, not the earlier 19–21 estimate. Each hands-on lesson ends with a self-grade rubric; each milestone's last hands-on lesson folds in the readiness check.

**M1** (gate: explain "not in context = doesn't exist" + ship a reliable single-tool agent):
- `0001-not-in-context-doesnt-exist.html` — core mental model + Cluster A vocabulary (DONE)
- `0005-build-the-single-tool-agent.html` — guided build; tokens/cost + tool-call anatomy taught inline; logs full per-turn context (DONE). Working script: `exercises/m1_agent.py` (self-test PASSED; live path needs a key — checkpoint 0)
- `0006-break-it-on-purpose.html` — context-overflow lab + vague-prompt-three-ways + M1 readiness check (DONE)

**M2** (gate: build a grounded multi-step agent and justify each pattern choice — learning record 0001):
- `0002-match-the-pattern-to-the-problem.html` — M2 decision map (DONE)
- `0007-structured-prompting-and-the-injection-lab.html` — structured rewrite + injection attack/defend (DONE)
- `0008-react-multi-hop-build.html` — ReAct multi-hop w/ logged thought/action/observation (DONE)
- `0009-rag-build-and-break.html` — RAG pipeline + chunking-collapse lab (DONE)
- `0010-episodic-memory.html` — recall-a-past-run build + M2 readiness check (DONE)

**M3** (gate: debug from traces alone + eval catches a planted regression — learning record 0002):
- `0003-traces-before-prompts.html` — M3 decision map (DONE)
- `0011-orchestrator-bakeoff.html` — orchestrator vs single, settled with traces (DONE)
- `0012-tracing-and-planted-regression.html` — trace instrumentation + planted-regression eval (DONE)
- `0013-critic-verifier-step.html` — verifier step, measured silent-wrong reduction + M3 readiness check (DONE)

**M4** (gate: own SLOs + independently run observe→fix→verify — learning record 0002):
- `0004-own-the-feedback-loop.html` — M4 map (DONE)
- `0014-slo-dashboard.html` — four-SLO dashboard from real traces (DONE)
- `0015-guardrails-and-hitl.html` — least-privilege scoping + injection defense + HITL checkpoint by risk (DONE)
- `0016-the-improvement-loop.html` — full observe→fix→verify capstone + M4 readiness check (DONE)

**Reference sheets:** m1/m2/m3/m4-core-vocabulary.html + agent-loop-and-tool-call.html (code, built with 0005). All cross-linked.

**Blocker for the learner:** repo `.env` has NO Anthropic key (verified 2026-07-03: dotenv_values shows no ANTHROPIC_* key; ant CLI not installed). Lesson 0005 checkpoint 0 walks adding `ANTHROPIC_API_KEY` to `.env`. Until then the hands-on runs can't execute live; `m1_agent.py --selftest` works offline.

**BYOK public version scaffolded 2026-07-03.** The workspace is now publishable as a standalone public repo without exposing Scott's tokens. Added: `.env.example` (blank key + Console link), `README.md` (BYOK contract + quick start), `.gitignore` (ignores `.env`, run artifacts, `__pycache__`). `m1_agent.py` now walks up from its own dir to find the nearest `.env` (`_load_env()`) instead of the Vernant-specific `parents[4]` path, so it runs in both the monorepo and a lifted-out repo. Lesson 0005 checkpoint 0 rewritten for a public/BYOK audience (`cp .env.example .env`, key-never-committed note). Distribution decision was BYOK (learner runs on their own key) — recommended over a hosted proxy/static-only; a key must never reach client-side code or a committed repo.

## Preferences observed
- Scott approved the M1 package format ("this was great!", 2026-07-03) — keep the structure: printable reference sheet + short lesson + closed-book quiz + own-words rubric, sister styling across milestones.
