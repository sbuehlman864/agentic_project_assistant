from __future__ import annotations

# test_prd_revision_loop.py
import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from schemas import GoalInterpretation, PRD, MilestonesDoc, TasksDoc
from llm import call_llm_json
from tools import write_markdown, render_prd_md, render_milestones_md, append_jsonl_log, tasks_to_rows, write_csv
from validators import validate_prd, validate_milestones, validate_tasks



SYSTEM = "Return ONLY valid JSON. No markdown, no extra text."
ALLOWED_TYPES = {"backend", "frontend", "data", "ml", "infra", "docs", "testing"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}

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

    # 6) Initial milestone generation prompt
    milestones_prompt = f"""
Using this PRD JSON, return MilestonesDoc JSON with keys:
title, milestones (array).

Each milestone must have keys:
name, objective, deliverables (array of strings), est_days (int).

PRD:
{json.dumps(prd.model_dump(), indent=2)}

Rules:
- Provide 3–6 milestones
- Each milestone must have 2–5 deliverables
- Keep estimates realistic for a solo developer MVP
- Order milestones logically (foundation → features → polish)
"""

    mdoc_dict = call_llm_json(SYSTEM, milestones_prompt)

    # 7) Validate + revise loop
    max_attempts = 3
    attempt = 1

    while True:
        mdoc = MilestonesDoc.model_validate(mdoc_dict)
        issues = validate_milestones(mdoc)

        append_jsonl_log({
            "event": "milestones_validation",
            "attempt": attempt,
            "issues": issues,
            "milestones": mdoc.model_dump(),
        })
        # Write iteration MDOC
        md1 = render_milestones_md(mdoc)
        iteration_path = write_markdown(f"MDOC_iteration_{attempt}.md", md1)
        print(f"📝 Wrote iteration {attempt}: {iteration_path}")

        if not issues:
            break
        if attempt >= max_attempts:
            print("⚠️ Reached max attempts; writing best-effort milestones.")
            break

        revise_prompt = f"""
You previously returned this MilestonesDoc JSON:
{json.dumps(mdoc.model_dump(), indent=2)}

Issues:
{json.dumps(issues, indent=2)}

Fix with minimal changes.
Return corrected MilestonesDoc JSON ONLY with the same keys:
title, milestones (each: name, objective, deliverables, est_days).
"""
        mdoc_dict = call_llm_json(SYSTEM, revise_prompt)
        attempt += 1

    # 8) Write milestones artifact
    md = render_milestones_md(mdoc)
    path = write_markdown("MILESTONES.md", md)
    print("✅ Wrote:", path)

    # 9) Generate tasks from PRD and Milestones
    tasks_prompt = f"""
Using this PRD and Milestones, return TasksDoc JSON with keys:
title, tasks (array).

Each task must have keys:
task_id (string), title (string),
type (one of: backend, frontend, data, ml, infra, docs, testing),
priority (one of: P0, P1, P2),
estimate_hours (number),
depends_on (array of task_id strings),
acceptance_criteria (array of strings).

PRD:
{json.dumps(prd.model_dump(), indent=2)}

Milestones:
{json.dumps(mdoc.model_dump(), indent=2)}

Rules:
- Return 20–45 tasks total
- Every task MUST have at least 1 acceptance_criteria bullet
- Use task_ids like T001, T002, ...
- depends_on must reference earlier task_ids only (no forward refs)
- Ensure a sensible ordering: setup -> core -> features -> polish -> tests/docs
"""

    tdoc_dict = call_llm_json(SYSTEM, tasks_prompt)

    max_attempts = 3
    attempt = 1

    while True:
        tdoc = TasksDoc.model_validate(tdoc_dict)
        issues = validate_tasks(tdoc)

        append_jsonl_log({
            "event": "tasks_validation",
            "attempt": attempt,
            "issues": issues,
            "task_count": len(tdoc.tasks),
        })    


        if not issues:
            break
        if attempt >= max_attempts:
            print("⚠️ Reached max attempts; writing best-effort TASKS.csv.")
            break

        revise_prompt = f"""
You previously returned this TasksDoc JSON:
{json.dumps(tdoc.model_dump(), indent=2)}

Issues:
{json.dumps(issues, indent=2)}

Fix ONLY what is necessary with minimal changes.
Return corrected TasksDoc JSON ONLY with the same keys and rules:
- 20–45 tasks
- unique task_id like T001...
- type in {sorted(list(ALLOWED_TYPES))}
- priority in {sorted(list(ALLOWED_PRIORITIES))}
- depends_on must reference valid existing task_ids and no self-deps
- every task must have acceptance_criteria
"""
        tdoc_dict = call_llm_json(SYSTEM, revise_prompt)
        attempt += 1

    # Write CSV
    rows = tasks_to_rows(tdoc)
    # Convert dict rows to list format for write_csv
    fieldnames = ["task_id", "title", "type", "priority", "estimate_hours", "depends_on", "acceptance_criteria"]
    csv_rows = [fieldnames] + [[row[field] for field in fieldnames] for row in rows]
    csv_path = write_csv("TASKS.csv", csv_rows)
    print("✅ Wrote:", csv_path)


if __name__ == "__main__":
    main()