# Mission: Agentic Operations — Maturity Ladder (full map unlocked: M1–M4)

## Why
Scott is climbing the "Agentic Operations Knowledge Map" (`docs/inbox/2026-07-03/Agentic knowledge development.md` — a private planning doc that lives outside this repo, not a public link) — a four-milestone arc ending at Head-of-Agentic-Operations capability. He already operates a heavily agentic codebase (Vernant) every day; this mission formalizes the foundations so each capability is explainable and teachable, not just used. The immediate target is the M1 readiness signal.

## Success looks like
- Explains, unprompted and in his own words, why "not in context = doesn't exist" — and can defend it against pushback
- Ships a reliable single-tool agent (call → observe → decide → repeat) and can show the full context sent on every turn
- Has self-annotated every M1 Cluster A concept at "can apply unprompted" or better
- Has run the doc's M1 exercises: log full per-turn context, overflow a context window and measure degradation, rewrite one vague prompt three ways
- Designs a grounded multi-step agent — reasoning pattern, memory strategy, retrieval design — and justifies each choice as a cost/quality tradeoff, not a copied recipe (M2)
- Debugs a failing agent from traces alone, and builds an eval suite that catches a planted regression (M3)
- Owns SLOs for a live agent and independently runs an observe → fix → verify improvement cycle (M4)

## Constraints
- Gate on demonstrated capability, not calendar time (per the source rubric)
- Scott is an expert practitioner *user* of agents — move fast on mechanics he sees daily; anchor examples to his real tooling (Claude Code sessions, Vernant's pipeline)
- Repo tooling for hands-on work: Python 3.12 + uv

## Out of scope
- Skipping gates: all four milestones are unlocked for study (Scott's requests 2026-07-03, learning records 0001–0002), but each readiness signal passes only on demonstrated capability — the M1 single-tool-agent build is still the first proof due
