# validators.py
from __future__ import annotations
from typing import List
from schemas import PRD
from schemas import MilestonesDoc
from schemas import TasksDoc

ALLOWED_TYPES = {"backend", "frontend", "data", "ml", "infra", "docs", "testing"}
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}

def validate_prd(prd: PRD) -> List[str]:
    issues: List[str] = []

    if not prd.title.strip():
        issues.append("PRD title is empty.")
    if len(prd.problem.strip()) < 40:
        issues.append("PRD problem statement is too short (aim for 40+ characters).")

    if len(prd.target_users) < 1:
        issues.append("PRD target_users should have at least 1 item.")

    if not (6 <= len(prd.functional_requirements) <= 10):
        issues.append(f"functional_requirements should be 6–10 items, got {len(prd.functional_requirements)}.")

    if not (4 <= len(prd.nonfunctional_requirements) <= 8):
        issues.append(f"nonfunctional_requirements should be 4–8 items, got {len(prd.nonfunctional_requirements)}.")

    if not (6 <= len(prd.user_stories) <= 10):
        issues.append(f"user_stories should be 6–10 items, got {len(prd.user_stories)}.")

    # Optional: require some goals
    if len(prd.goals) < 3:
        issues.append("goals should have at least 3 items.")
    if len(prd.non_goals) < 2:
        issues.append("non_goals should have at least 2 items.")

    return issues


def validate_milestones(mdoc: MilestonesDoc) -> List[str]:
    issues: List[str] = []

    if not mdoc.title.strip():
        issues.append("Milestones title is empty.")

    if not (3 <= len(mdoc.milestones) <= 6):
        issues.append(f"milestones should be 3–6 items, got {len(mdoc.milestones)}.")

    for idx, m in enumerate(mdoc.milestones, 1):
        if len(m.name.strip()) < 3:
            issues.append(f"Milestone {idx} has a very short name.")
        if len(m.objective.strip()) < 20:
            issues.append(f"Milestone {idx} objective is too short.")
        if len(m.deliverables) < 2:
            issues.append(f"Milestone {idx} should have at least 2 deliverables.")
        if not (1 <= m.est_days <= 14):
            issues.append(f"Milestone {idx} est_days should be 1–14 for MVP solo scope, got {m.est_days}.")

    return issues


def validate_tasks(tdoc: TasksDoc) -> list[str]:
    issues: list[str] = []

    n = len(tdoc.tasks)
    if not (20 <= n <= 45):
        issues.append(f"tasks should be 20–45 items, got {n}.")

    # task_id uniqueness
    ids = [t.task_id for t in tdoc.tasks]
    if len(set(ids)) != len(ids):
        issues.append("task_id values are not unique.")

    # basic field checks
    for t in tdoc.tasks:
        if not t.task_id.strip():
            issues.append("A task has an empty task_id.")
            break
        if len(t.title.strip()) < 5:
            issues.append(f"Task {t.task_id} title too short.")
            break
        if t.type not in ALLOWED_TYPES:
            issues.append(f"Task {t.task_id} has invalid type '{t.type}'.")
            break
        if t.priority not in ALLOWED_PRIORITIES:
            issues.append(f"Task {t.task_id} has invalid priority '{t.priority}'.")
            break
        if not (0.5 <= t.estimate_hours <= 24):
            issues.append(f"Task {t.task_id} estimate_hours should be 0.5–24, got {t.estimate_hours}.")
            break
        if len(t.acceptance_criteria) < 1:
            issues.append(f"Task {t.task_id} missing acceptance_criteria.")
            break

    # dependency correctness (depends_on must reference existing ids)
    id_set = set(ids)
    for t in tdoc.tasks:
        for dep in t.depends_on:
            if dep not in id_set:
                issues.append(f"Task {t.task_id} depends_on unknown id '{dep}'.")
                return issues
            if dep == t.task_id:
                issues.append(f"Task {t.task_id} depends on itself.")
                return issues

    return issues
