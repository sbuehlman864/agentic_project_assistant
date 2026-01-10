# test_goal_interpretation_llm.py
from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to path so we can import schemas and llm
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from schemas import GoalInterpretation
from llm import call_llm_json

SYSTEM_PROMPT = """
You are a careful assistant.
Return ONLY valid JSON. No markdown, no extra text.
"""

def build_user_prompt(idea: str, constraints: list[str]) -> str:
    return f"""
Create a GoalInterpretation JSON object for this project idea.

Idea:
{idea}

Constraints:
{json.dumps(constraints, indent=2)}

Return ONLY JSON with EXACTLY these keys:
- title (string)
- one_liner (string)
- target_users (array of strings)
- constraints (array of strings)
- assumptions (array of strings)
- success_metrics (array of strings)

Rules:
- Keep it realistic for an MVP.
- Make title short (2–6 words).
- Provide 2–5 items for each list field.
"""

def main():
    idea = "A web app that helps college students turn class syllabi into weekly plans and track progress."
    constraints = [
        "Solo developer",
        "MVP in 2 weeks",
        "Demoable locally",
        "No external integrations in v1",
    ]

    user_prompt = build_user_prompt(idea, constraints)

    raw = call_llm_json(SYSTEM_PROMPT, user_prompt)

    # Validate + coerce into your schema
    goal = GoalInterpretation.model_validate(raw)

    print("✅ Validated GoalInterpretation:")
    print(json.dumps(goal.model_dump(), indent=2))

if __name__ == "__main__":
    main()
