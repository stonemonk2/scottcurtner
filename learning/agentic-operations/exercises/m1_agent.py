# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "python-dotenv"]
# ///
"""M1 single-tool agent — Lesson 0005 reference implementation.

A calculator agent built as a manual tool-use loop, logging the FULL context
sent to the model on every turn (the M1 exercise: read what the model sees).

Run:      uv run docs/learning/agentic-operations/exercises/m1_agent.py
          uv run .../m1_agent.py "your own arithmetic question"
Self-test (no API call): uv run .../m1_agent.py --selftest
"""
import ast
import json
import operator
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

def _load_env() -> None:
    """Load the nearest .env by walking up from this file, so the agent runs both
    inside the Vernant monorepo and as a standalone public (BYOK) repo."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").is_file():
            load_dotenv(parent / ".env")
            return
    load_dotenv()  # fall back to cwd search; real environment vars still win


_load_env()

MODEL = "claude-opus-4-8"
PRICE_IN, PRICE_OUT = 5.00, 25.00  # $/1M tokens, platform.claude.com pricing (2026-06)
LOG = Path(__file__).with_name("context_log.jsonl")

SYSTEM = (
    "You are a careful calculation assistant. For ANY arithmetic, use the "
    "calculator tool - never compute in your head. State the final answer plainly."
)

TOOLS = [{
    "name": "calculator",
    "description": (
        "Evaluate one arithmetic expression (numbers, + - * / ** and parentheses only). "
        "Call this for every arithmetic step; do not do mental math."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "e.g. '(137 * 41) + 2**10 / 7'"}
        },
        "required": ["expression"],
    },
}]

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def calculate(expression: str) -> str:
    """The tool body. The model only PROPOSES text; this code is what makes it
    real - and safe (AST whitelist, not eval())."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError(f"unsupported syntax: {ast.dump(node)}")
    return str(ev(ast.parse(expression, mode="eval").body))


def _jsonable(o):
    return o.model_dump() if hasattr(o, "model_dump") else str(o)


def log_turn(turn: int, messages: list) -> None:
    """The M1 exercise: persist the ENTIRE world the model is about to see."""
    record = {"turn": turn, "system": SYSTEM, "tools": TOOLS, "messages": messages}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=_jsonable) + "\n")


def selftest() -> None:
    assert calculate("(137 * 41) + 2**10 / 7") == str(137 * 41 + 2 ** 10 / 7)
    assert calculate("-3 * (2 + 5)") == "-21"
    for bad in ("__import__('os')", "x + 1", "1j * 2"):
        try:
            calculate(bad)
            raise AssertionError(f"unsafe/invalid expression accepted: {bad}")
        except ValueError:
            pass
    class Fake:  # stands in for an SDK content block
        def model_dump(self):
            return {"type": "text", "text": "hi"}
    line = json.dumps({"messages": [{"role": "assistant", "content": [Fake()]}]},
                      default=_jsonable)
    assert json.loads(line)["messages"][0]["content"][0]["text"] == "hi"
    print("selftest OK")


def main() -> None:
    if "--selftest" in sys.argv:
        selftest()
        return
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        sys.exit("No Anthropic credentials found. Add ANTHROPIC_API_KEY=... to the repo "
                 ".env (loaded automatically) or export it in your shell, then re-run.")

    question = " ".join(sys.argv[1:]) or "What is (137 * 41) + 2**10 / 7? Work step by step."
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    total_in = total_out = 0

    for turn in range(1, 11):  # ponytail: hard stop at 10 iterations, raise if you need more
        log_turn(turn, messages)
        response = client.messages.create(
            model=MODEL, max_tokens=16000, system=SYSTEM, tools=TOOLS, messages=messages,
        )
        total_in += response.usage.input_tokens
        total_out += response.usage.output_tokens
        print(f"\n--- turn {turn}: stop_reason={response.stop_reason}  "
              f"in={response.usage.input_tokens} out={response.usage.output_tokens} tokens")

        for block in response.content:
            if block.type == "text":
                print(block.text)

        if response.stop_reason != "tool_use":
            break

        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                try:
                    result, is_error = calculate(block.input["expression"]), False
                except Exception as e:
                    result, is_error = f"Error: {e}", True
                print(f"  [tool] calculator({block.input['expression']!r}) -> {result}")
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": result, "is_error": is_error})
        messages.append({"role": "user", "content": results})

    cost = total_in / 1e6 * PRICE_IN + total_out / 1e6 * PRICE_OUT
    print(f"\n=== total: {total_in} in / {total_out} out tokens ~= ${cost:.4f}")
    print(f"=== full per-turn context written to {LOG} - go read it")


if __name__ == "__main__":
    main()
