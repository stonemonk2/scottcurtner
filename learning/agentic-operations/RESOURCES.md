# Agentic Operations Resources

## Knowledge

- Rubric: Agentic Operations Knowledge Map — a private planning doc outside this repo (not a public link).
  The curriculum source of truth: four maturity stages, per-stage concepts, intuitions, exercises, and readiness signals. Use for: deciding what to teach next and when a milestone gate is passed.
- [Video: "The Busy Person's Intro to LLMs" — Andrej Karpathy (1 hr)](https://www.youtube.com/watch?v=zjkBMFhNj_g)
  The best single mental model of what an LLM is: two files, training as compression, inference as next-token prediction. Use for: M1 Cluster A fundamentals (LLM, token). Primary source for Lesson 0001.
- [Article: "Building Effective Agents" — Anthropic](https://www.anthropic.com/research/building-effective-agents)
  Workflows vs. agents; an agent is an LLM using tools in a loop; tool definitions deserve as much prompt-engineering attention as prompts. Use for: the "agent" and "tool call" vocabulary and the single-tool loop lesson.
- [Article: "Effective context engineering for AI agents" — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context curation as "the #1 job of engineers building AI agents"; bloated or irrelevant context as the silent killer of reliability. Use for: "context management = performance."
- [Research: "Context Rot" — Chroma](https://research.trychroma.com/context-rot)
  18-model study showing performance degrades non-uniformly as input length grows (incl. lost-in-the-middle effects). Use for: grounding "more context is not better context" in measurement.
- [Docs: Tool use with Claude — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
  The mechanical round-trip: model proposes a structured tool call, your code executes it and returns the result. Use for: building the M1 single-tool agent.
- [Paper: "ReAct: Synergizing Reasoning and Acting in Language Models" — Yao et al., 2022](https://arxiv.org/abs/2210.03629)
  The workhorse pattern for tool-using agents: interleaved thought → action → observation, with actions pulling external information back into reasoning. Use for: M2 Cluster C; the multi-hop ReAct build. Primary source for Lesson 0002.
- [Paper: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" — Wei et al., 2022](https://arxiv.org/abs/2201.11903)
  Where "reason step-by-step before answering" comes from; a few worked exemplars unlock linear reasoning. Use for: M2 Cluster C (CoT).
- [Paper: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" — Yao et al., NeurIPS 2023](https://arxiv.org/abs/2305.10601)
  Branch, self-evaluate, look ahead, backtrack — search over reasoning paths for exploration-shaped problems. Use for: M2 Cluster C (ToT) and the cost/quality tradeoff argument.
- [Series: Prompt injection — Simon Willison](https://simonwillison.net/series/prompt-injection/)
  From the coiner of the term: the attack class, real examples, and why most proposed fixes don't hold. Use for: M2 Cluster A injection basics; the "still unsolved" framing.
- [Docs: Prompt engineering overview — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
  Official technique catalog: clarity, examples, XML structure, role prompting, prompt chaining. Use for: M2 Cluster A structured prompting.
- [Article: "How we built our multi-agent research system" — Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  Real orchestrator/subagent system with honest failure stories (50 subagents for simple queries, endless searching, agents distracting each other). Use for: M3 Cluster A — context isolation as the real reason for multi-agent, and why extra agents must be justified. Primary source for Lesson 0003.
- [Docs: LLM observability & tracing — Langfuse](https://langfuse.com/docs/observability/overview)
  Open-source trace capture: every LLM call, tool invocation, and retrieval step with timing, inputs, outputs. Use for: M3 Cluster D tracing; the instrumentation exercise. (Vernant already has a langfuse-bridge worktree — the hands-on lesson can use the real stack.)
- [Article: "Durable execution meets AI" — Temporal](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai)
  Checkpointing and resuming long agent runs; replay-based recovery. Use for: M3 Cluster B durability. (Vernant runs on Temporal — anchor here.)
- [Article: "Your AI Product Needs Evals" — Hamel Husain](https://hamel.dev/blog/posts/evals/)
  The canonical practitioner essay on eval systems as the root cause of AI product success/failure; three eval levels. Use for: M3 Cluster D evals.
- [Article: "Using LLM-as-a-Judge for Evaluation" — Hamel Husain](https://hamel.dev/blog/posts/llm-judge/)
  How to build a judge you can trust: measure agreement with humans, collect critiques, recalibrate. Use for: M3 Cluster D LLM-as-judge with human recalibration.
- [Book chapter: "Service Level Objectives" — Google SRE Book, ch. 4](https://sre.google/sre-book/service-level-objectives/)
  The canonical SLI/SLO/SLA text. Use for: M4 Cluster A — defining agent SLOs (success rate, latency, cost-per-task, escalation). Primary source for Lesson 0004.
- [Framework: OWASP Top 10 for LLM Applications — OWASP GenAI](https://genai.owasp.org/)
  The standard risk taxonomy: prompt injection (LLM01), excessive permissions, output handling. Use for: M4 Cluster C guardrails and least-privilege tool scoping.

## Wisdom (Communities)

- None chosen yet — see Gaps.

## Gaps

- A high-signal community for agent builders (needed by M2 at the latest) — evaluate candidates next session before proposing any.
- A hands-on tokenizer playground for token intuition — verify a good one before the tokens & cost lesson.
- A practical RAG build guide (chunking strategies, retrieval evaluation) — verify one before the M2 RAG hands-on lesson.
