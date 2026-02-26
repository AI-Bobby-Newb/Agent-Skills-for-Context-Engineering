#!/usr/bin/env python3
"""Interactive 1-shot prompt generator.

Given a simple project summary, this tool asks focused clarification questions and
builds a production-ready one-shot prompt.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Question:
    key: str
    prompt: str
    hint: str


CORE_QUESTIONS = [
    Question(
        key="goal",
        prompt="What should the final deliverable accomplish?",
        hint="Define success in one sentence.",
    ),
    Question(
        key="audience",
        prompt="Who is the target user or audience?",
        hint="Be specific (e.g., junior developers, finance analysts, parents).",
    ),
    Question(
        key="output_format",
        prompt="What output format do you want from the AI?",
        hint="Examples: bullet list, JSON, markdown table, code files.",
    ),
    Question(
        key="constraints",
        prompt="What hard constraints must be followed?",
        hint="Include time, budget, stack, legal, style, or platform limits.",
    ),
    Question(
        key="quality_bar",
        prompt="How should quality be measured?",
        hint="Define acceptance criteria or test expectations.",
    ),
    Question(
        key="non_goals",
        prompt="What should explicitly NOT be included?",
        hint="List boundaries to avoid scope creep.",
    ),
]

EXTRA_QUESTIONS = [
    Question(
        key="data_inputs",
        prompt="What inputs/data should the solution use?",
        hint="Mention sources, schema, sample records, or allowed assumptions.",
    ),
    Question(
        key="edge_cases",
        prompt="What edge cases or failure modes must be handled?",
        hint="Think null values, outages, security, scaling, ambiguous user input.",
    ),
    Question(
        key="tone",
        prompt="What tone/style should the response use?",
        hint="Examples: concise technical, friendly coach, executive summary.",
    ),
    Question(
        key="examples",
        prompt="Do you have examples of ideal output?",
        hint="Optional but high-leverage.",
    ),
]


KEYWORDS = {
    "web": ["ui_framework", "deployment_target"],
    "api": ["api_style", "auth_requirements"],
    "data": ["data_volume", "privacy_requirements"],
    "agent": ["tool_access", "memory_strategy"],
}

KEYWORD_QUESTIONS = {
    "ui_framework": Question(
        key="ui_framework",
        prompt="Which UI framework or frontend stack should be used?",
        hint="E.g., React, Vue, Svelte, plain HTML/CSS.",
    ),
    "deployment_target": Question(
        key="deployment_target",
        prompt="Where will this run in production?",
        hint="E.g., Vercel, AWS Lambda, on-prem, local desktop.",
    ),
    "api_style": Question(
        key="api_style",
        prompt="What API style is required?",
        hint="REST, GraphQL, gRPC, webhook-first, etc.",
    ),
    "auth_requirements": Question(
        key="auth_requirements",
        prompt="What authentication/authorization requirements exist?",
        hint="OAuth, API keys, RBAC, SSO, public/no auth.",
    ),
    "data_volume": Question(
        key="data_volume",
        prompt="What data scale should the system handle?",
        hint="Approx rows/events/users and expected growth.",
    ),
    "privacy_requirements": Question(
        key="privacy_requirements",
        prompt="Any compliance or privacy requirements?",
        hint="PII handling, GDPR, HIPAA, retention limits, audit trails.",
    ),
    "tool_access": Question(
        key="tool_access",
        prompt="What tools can the agent call?",
        hint="Browser, filesystem, code interpreter, internal APIs, none.",
    ),
    "memory_strategy": Question(
        key="memory_strategy",
        prompt="Should the agent maintain memory between sessions?",
        hint="No memory, short-term only, long-term profile, vector DB, etc.",
    ),
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def choose_keyword_questions(summary: str) -> list[Question]:
    summary_l = summary.lower()
    selected_keys: list[str] = []
    for keyword, keys in KEYWORDS.items():
        if keyword in summary_l:
            selected_keys.extend(keys)
    seen = set()
    result = []
    for key in selected_keys:
        if key not in seen:
            seen.add(key)
            result.append(KEYWORD_QUESTIONS[key])
    return result


def build_question_set(summary: str) -> list[Question]:
    return [*CORE_QUESTIONS, *choose_keyword_questions(summary), *EXTRA_QUESTIONS]


def ask_questions(questions: Iterable[Question]) -> dict[str, str]:
    answers: dict[str, str] = {}
    for q in questions:
        print(f"\n• {q.prompt}")
        print(f"  Hint: {q.hint}")
        value = input("  Answer: ").strip()
        answers[q.key] = value or "Not specified"
    return answers


def compose_prompt(summary: str, answers: dict[str, str]) -> str:
    context_lines = "\n".join(f"- {k}: {v}" for k, v in answers.items())
    sections = [
        "You are an elite product + engineering execution assistant.",
        "## Project Summary",
        summary,
        "## Clarified Requirements",
        context_lines,
        "## Your Task",
        "Produce the best possible solution for this request in one response.",
        "### Must Do",
        "1. Restate the objective and constraints in a compact spec.",
        "2. Propose an execution plan optimized for speed and quality.",
        "3. Deliver the requested output in the required format.",
        "4. Address edge cases, risks, and trade-offs explicitly.",
        "5. Include validation steps/tests against the quality bar.",
        "6. Respect non-goals and avoid unnecessary scope expansion.",
        "### Output Requirements",
        "- Be concrete and implementation-ready.",
        "- Use assumptions only when unavoidable, and label them clearly.",
        '- If information is missing, provide a "best default" and explain why.',
        "- Keep the response efficient, high-signal, and free of fluff.",
    ]
    return "\n\n".join(sections)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a high-quality one-shot AI prompt.")
    parser.add_argument("summary", help="Basic summary of what the user wants to build.")
    parser.add_argument(
        "--answers-json",
        help="Optional JSON object of pre-filled answers for non-interactive use.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = normalize(args.summary)
    if not summary:
        raise SystemExit("Summary cannot be empty.")

    questions = build_question_set(summary)

    if args.answers_json:
        try:
            answers = json.loads(args.answers_json)
            if not isinstance(answers, dict):
                raise ValueError("answers-json must decode to an object")
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON for --answers-json: {exc}") from exc
    else:
        print("I will ask targeted questions to sharpen your brief before generating a one-shot prompt.")
        answers = ask_questions(questions)

    final_answers = {q.key: normalize(str(answers.get(q.key, "Not specified"))) for q in questions}
    prompt = compose_prompt(summary, final_answers)

    print("\n" + "=" * 80)
    print("PERFECT 1-SHOT PROMPT")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()
