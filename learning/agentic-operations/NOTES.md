# Teaching Notes — Agentic Operations

## Learner profile
- Scott builds and operates Vernant (agentic analytical pipeline: Python/PydanticAI/Temporal) and works inside Claude Code daily — an expert practitioner *user* of agents formalizing the foundations.
- Implication for ZPD: vocabulary can move fast; anchor every abstract concept to something he already sees daily (session compaction, context windows filling up, tool permission prompts).

## Open questions
- Mission "Why" was derived from the source doc + the /teach invocation, not interviewed. Confirm: is this arc for his own mastery, for onboarding future hires (the doc is written as a new-hire rubric), or both? Affects how much emphasis to put on "can teach it" vs "can apply unprompted."

## Planned lesson arcs
Lesson numbers are workspace-sequential, assigned at write time (0001 = M1 mental model, 0002 = M2 pattern map). Arcs below use slugs, not numbers.

**M1** (gate: explain "not in context = doesn't exist" + ship a reliable single-tool agent):
- `0001-not-in-context-doesnt-exist.html` — core mental model + Cluster A vocabulary (DONE 2026-07-03)
- tokens & cost: hands-on tokenizer, reading usage/cost off a real API response
- anatomy of a tool call: schema → proposal → execution → result fed back
- build & ship the single-tool agent (Python/uv), logging the full context sent every turn
- break it on purpose: context-overflow experiment + vague-prompt-three-ways; M1 readiness check

**M2** (gate: build a grounded multi-step agent and justify each pattern choice — unlocked by request, learning record 0001):
- `0002-match-the-pattern-to-the-problem.html` — the M2 decision map: CoT/ReAct/ToT as cost/quality tradeoffs, memory as retrieval-and-injection, retrieval caps quality, injection basics (DONE 2026-07-03)
- structured prompting + instruction hierarchy: rewrite a weak prompt with role/constraints/format/few-shot
- prompt-injection lab: hijack your own agent with untrusted data, then defend it
- build the ReAct multi-hop agent with logged thought/action/observation
- build a small RAG pipeline; deliberately break the chunking and watch grounding collapse
- episodic memory: agent recalls a prior session's outcome and changes its plan; M2 readiness check

**M3** (gate: debug a failing agent from traces alone + eval suite that catches a planted regression — unlocked, learning record 0002):
- `0003-traces-before-prompts.html` — M3 decision map: single-agent default, context isolation as the real multi-agent reason, silent confident failures, trajectory evals (DONE 2026-07-03)
- run lifecycle & durability: state, stop conditions, checkpoint/resume (anchor: Vernant's Temporal pipeline)
- orchestrator build: 2–3 subagents vs. one agent — prove it with traces, or admit it doesn't win
- tracing instrumentation + eval set that catches a deliberately planted regression (anchor: Langfuse)
- critic/verifier step: measure the reduction in silent wrong answers; M3 readiness check

**M4** (gate: own SLOs for a live agent + independently run observe → fix → verify — unlocked, learning record 0002):
- `0004-own-the-feedback-loop.html` — M4 map: SLOs as first-class metrics, eval suite as ground truth, cost/reliability/quality as one surface, HITL by risk (DONE 2026-07-03)
- SLO definition + dashboard for one live agent (success rate, latency, cost-per-task, escalation)
- guardrails & least privilege: input/output validation, injection defense, tool-permission scoping
- HITL checkpoint policy for one high-stakes action; measure its throughput cost
- full improvement cycle: catch a live regression, ship a gated fix, prove the suite would have blocked it; M4 readiness check

## Preferences observed
- Scott approved the M1 package format ("this was great!", 2026-07-03) — keep the structure: printable reference sheet + short lesson + closed-book quiz + own-words rubric, sister styling across milestones.
