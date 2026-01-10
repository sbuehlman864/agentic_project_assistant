# validators.py
from __future__ import annotations
from typing import List
from schemas import PRD

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
