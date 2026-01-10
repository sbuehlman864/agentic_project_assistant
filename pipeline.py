# pipeline.py
from __future__ import annotations
import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import io, csv, json, time
from typing import Dict, Any, List

from schemas import GoalInterpretation, PRD, MilestonesDoc, TasksDoc
from llm import call_llm_json
from validators import validate_prd, validate_milestones, validate_tasks
from tools import render_prd_md, render_milestones_md, tasks_to_rows

SYSTEM = "Return ONLY valid JSON. No markdown, no extra text."

def run_pipeline(idea: str, constraints: List[str], max_attempts: int = 3) -> Dict[str, Any]:
    start_time = time.time()
    
    # 1) GoalInterpretation
    gi_prompt = f"""
Return GoalInterpretation JSON with keys:
- title (string)
- one_liner (string)
- target_users (array of strings)
- constraints (array of strings)
- assumptions (array of strings)
- success_metrics (array of strings, NOT objects)

Each success_metric should be a simple string describing the metric.

Idea: {idea}
Constraints: {json.dumps(constraints)}

Example format:
{{
  "title": "Project Name",
  "one_liner": "Brief description",
  "target_users": ["User type 1", "User type 2"],
  "constraints": ["Constraint 1", "Constraint 2"],
  "assumptions": ["Assumption 1", "Assumption 2"],
  "success_metrics": ["Metric 1: description", "Metric 2: description"]
}}
"""
    gi_dict = call_llm_json(SYSTEM, gi_prompt)
    gi = GoalInterpretation.model_validate(gi_dict)

    # 2) PRD + revise loop
    prd_prompt = f"""
Using this goal interpretation, return PRD JSON with these exact keys:
- title (string)
- problem (string)
- target_users (array of strings)
- goals (array of strings)
- non_goals (array of strings)
- user_stories (array of strings, NOT objects - use format "As a [user], I want [goal] so that [benefit]")
- functional_requirements (array of strings)
- nonfunctional_requirements (array of strings)
- risks (array of strings)
- open_questions (array of strings)

GoalInterpretation:
{json.dumps(gi.model_dump(), indent=2)}

Rules:
- Provide 6–10 functional_requirements
- Provide 4–8 nonfunctional_requirements
- Provide 6–10 user_stories as simple strings (e.g., "As a user, I want to add expenses so that I can track spending")
- Keep scope MVP-realistic
- All arrays must contain strings, NOT objects or nested structures
"""
    prd_dict = call_llm_json(SYSTEM, prd_prompt)
    prd_issues = []
    for attempt in range(1, max_attempts + 1):
        prd = PRD.model_validate(prd_dict)
        prd_issues = validate_prd(prd)
        if not prd_issues:
            break
        if attempt == max_attempts:
            break
        revise_prompt = f"""
You previously returned this PRD JSON:
{json.dumps(prd.model_dump(), indent=2)}

Issues:
{json.dumps(prd_issues, indent=2)}

Fix with minimal changes.
Return corrected PRD JSON ONLY with the same keys.
"""
        prd_dict = call_llm_json(SYSTEM, revise_prompt)

    # 3) Milestones + revise loop
    milestones_prompt = f"""
Using this PRD JSON, return MilestonesDoc JSON with keys:
title, milestones (array). Each milestone: name, objective, deliverables, est_days.

PRD:
{json.dumps(prd.model_dump(), indent=2)}

Rules:
- Provide 3–6 milestones
- Each milestone: 2–5 deliverables
- est_days realistic for solo MVP
- Order logically
"""
    mdoc_dict = call_llm_json(SYSTEM, milestones_prompt)
    m_issues = []
    for attempt in range(1, max_attempts + 1):
        mdoc = MilestonesDoc.model_validate(mdoc_dict)
        m_issues = validate_milestones(mdoc)
        if not m_issues:
            break
        if attempt == max_attempts:
            break
        revise_prompt = f"""
You previously returned this MilestonesDoc JSON:
{json.dumps(mdoc.model_dump(), indent=2)}

Issues:
{json.dumps(m_issues, indent=2)}

Fix with minimal changes. Return corrected MilestonesDoc JSON ONLY.
"""
        mdoc_dict = call_llm_json(SYSTEM, revise_prompt)

    # 4) Tasks + revise loop
    tasks_prompt = f"""
Using this PRD and Milestones, return TasksDoc JSON with keys:
title, tasks (array). Each task: task_id, title, type, priority, estimate_hours, depends_on, acceptance_criteria.

PRD:
{json.dumps(prd.model_dump(), indent=2)}

Milestones:
{json.dumps(mdoc.model_dump(), indent=2)}

Rules:
- Return 20–45 tasks
- task_id like T001, T002, ...
- type in: backend, frontend, data, ml, infra, docs, testing
- priority in: P0, P1, P2
- depends_on references earlier task_ids only
- every task has >=1 acceptance_criteria
"""
    tdoc_dict = call_llm_json(SYSTEM, tasks_prompt)
    t_issues = []
    for attempt in range(1, max_attempts + 1):
        tdoc = TasksDoc.model_validate(tdoc_dict)
        t_issues = validate_tasks(tdoc)
        if not t_issues:
            break
        if attempt == max_attempts:
            break
        revise_prompt = f"""
You previously returned this TasksDoc JSON:
{json.dumps(tdoc.model_dump(), indent=2)}

Issues:
{json.dumps(t_issues, indent=2)}

Fix with minimal changes. Return corrected TasksDoc JSON ONLY.
"""
        tdoc_dict = call_llm_json(SYSTEM, revise_prompt)

    # Render artifacts (strings)
    prd_md = render_prd_md(prd)
    milestones_md = render_milestones_md(mdoc)

    # Build CSV text in-memory
    rows = tasks_to_rows(tdoc)
    output = io.StringIO()
    fieldnames = ["task_id","title","type","priority","estimate_hours","depends_on","acceptance_criteria"]
    w = csv.DictWriter(output, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    tasks_csv = output.getvalue()

    # Calculate total execution time
    end_time = time.time()
    duration_seconds = end_time - start_time

    return {
        "goal": gi,
        "prd": prd,
        "milestones": mdoc,
        "tasks": tdoc,
        "prd_md": prd_md,
        "milestones_md": milestones_md,
        "tasks_csv": tasks_csv,
        "duration_seconds": duration_seconds,
        "issues": {
            "prd": prd_issues,
            "milestones": m_issues,
            "tasks": t_issues,
        },
    }
