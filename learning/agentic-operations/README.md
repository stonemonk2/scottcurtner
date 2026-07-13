# Agentic Operations — a hands-on course

Eighteen short lessons that take you from *"an LLM predicts the next token"* to
*owning the improvement loop that keeps a production agent honest as the model
shifts beneath it.* Four mental-model lessons and fourteen build-and-break labs,
one arc per milestone (Level 1 Foundational → Level 4 Operational Leader).

Open `lessons/0001-not-in-context-doesnt-exist.html` in a browser to start.
The lessons are self-contained HTML — no build step, no server.

## Bring Your Own Key (BYOK)

The hands-on lessons run a real agent against the Anthropic API. **This course
never ships an API key.** You run it on *your own* key, which:

- stays on **your** machine,
- is read from a local `.env` that is **gitignored** (it can't be committed), and
- is **never** printed, logged, or sent anywhere except Anthropic's API.

The whole Level 1–Level 2 hands-on costs well under a dollar of your own credit.

### Quick start

```bash
# 1. Get a key at https://console.anthropic.com  ->  API Keys
# 2. Create your local .env from the template and paste your key in:
cp .env.example .env          # then edit .env:  ANTHROPIC_API_KEY=sk-ant-...

# 3. Confirm the key is set — without printing it:
uv run python -c "from dotenv import dotenv_values; print('ANTHROPIC_API_KEY' in dotenv_values('.env'))"
# -> True

# 4. Run the first agent (uv reads the inline dependencies; no venv setup needed):
uv run exercises/level1_agent.py "what is 17 * 23 + 4?"

# Offline, no key required — verifies the calculator + safety logic:
uv run exercises/level1_agent.py --selftest
```

The agent walks up from its own directory to find the nearest `.env`, so it
works whether this folder is a standalone repo or nested inside a larger one.

## What's here

| Path | What it is |
|---|---|
| `lessons/*.html` | The 18 lessons (0001–0018). Start at 0001. |
| `reference/*.html` | Printable cheat-sheets: per-milestone vocabulary + the agent-loop code reference. |
| `exercises/level1_agent.py` | The tested single-tool agent you build in Lesson 0007. |
| `.env.example` | Template — copy to `.env` and add your key. |
| `MISSION.md` · `RESOURCES.md` | Why this course exists, and the verified sources every lesson cites. |

## Publishing this as a public repo

This directory is self-contained: lift it out (`git subtree split` or a plain
copy) as its own repository and it works as-is. Before publishing, confirm
`.env` is absent from the tree and that `.gitignore` lists it — your key must
never enter git history.
