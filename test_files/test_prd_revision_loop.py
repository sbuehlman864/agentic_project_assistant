from __future__ import annotations

# test_prd_revision_loop.py
import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from schemas import GoalInterpretation, PRD
from llm import call_llm_json
from tools import write_markdown, render_prd_md, append_jsonl_log
from validators import validate_prd

SYSTEM = "Return ONLY valid JSON. No markdown, no extra text."

def main():
    idea = "A web app that helps college students turn class syllabi into weekly plans and track progress."
    constraints = ["Solo developer", "MVP in 2 weeks", "Demoable locally", "No external integrations in v1"]

    # 1) Goal interpretation
    gi_prompt = f"""
Return GoalInterpretation JSON with keys:
title, one_liner, target_users, constraints, assumptions, success_metrics.

Idea: {idea}
Constraints: {json.dumps(constraints)}
"""
    gi_dict = call_llm_json(SYSTEM, gi_prompt)
    gi = GoalInterpretation.model_validate(gi_dict)

    append_jsonl_log({"event": "goal_interpretation", "data": gi.model_dump()})

    # 2) Initial PRD generation
    prd_prompt = f"""
Using this goal interpretation, return PRD JSON with keys:
title, problem, target_users, goals, non_goals, user_stories,
functional_requirements, nonfunctional_requirements, risks, open_questions.

GoalInterpretation:
{json.dumps(gi.model_dump(), indent=2)}

Rules:
- Provide 6–10 functional_requirements
- Provide 4–8 nonfunctional_requirements
- Provide 6–10 user_stories
- Keep scope MVP-realistic
"""
    prd_dict = call_llm_json(SYSTEM, prd_prompt)

    # 3) Validate + revise loop
    max_attempts = 3
    attempt = 1

    while True:
        prd = PRD.model_validate(prd_dict)  # schema validation
        issues = validate_prd(prd)          # quality validation

        append_jsonl_log({
            "event": "prd_validation",
            "attempt": attempt,
            "issues": issues,
            "prd": prd.model_dump(),
        })

        # Write iteration PRD
        md = render_prd_md(prd)
        iteration_path = write_markdown(f"PRD_iteration_{attempt}.md", md)
        print(f"📝 Wrote iteration {attempt}: {iteration_path}")

        if not issues:
            break

        if attempt >= max_attempts:
            print("⚠️ Reached max attempts; writing best-effort PRD.")
            break

        revise_prompt = f"""
You previously returned this PRD JSON:
{json.dumps(prd.model_dump(), indent=2)}

It has these issues:
{json.dumps(issues, indent=2)}

Fix the issues with minimal changes.
Return corrected PRD JSON ONLY with the same keys:
title, problem, target_users, goals, non_goals, user_stories,
functional_requirements, nonfunctional_requirements, risks, open_questions.
"""
        prd_dict = call_llm_json(SYSTEM, revise_prompt)
        attempt += 1

    # 4) Write final artifact
    md = render_prd_md(prd)
    path = write_markdown("PRD.md", md)
    print("✅ Wrote final PRD:", path)

if __name__ == "__main__":
    main()
