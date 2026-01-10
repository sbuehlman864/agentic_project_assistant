import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from schemas import GoalInterpretation, PRD
from llm import call_llm_json
from tools import write_markdown, render_prd_md

SYSTEM = "Return ONLY valid JSON. No markdown."

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

    # 2) PRD generation
    prd_prompt = f"""
Using this goal interpretation, return PRD JSON with keys:
title, problem, target_users, goals, non_goals, user_stories,
functional_requirements, nonfunctional_requirements, risks, open_questions.

GoalInterpretation:
{json.dumps(gi.model_dump(), indent=2)}

Rules:
- Provide 6–10 functional requirements
- Provide 4–8 nonfunctional requirements
- Provide 6–10 user stories
- Keep scope MVP-realistic
"""
    prd_dict = call_llm_json(SYSTEM, prd_prompt)
    prd = PRD.model_validate(prd_dict)

    md = render_prd_md(prd)
    path = write_markdown("PRD.md", md)

    print("✅ Wrote:", path)

if __name__ == "__main__":
    main()
