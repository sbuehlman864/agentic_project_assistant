import sys
from pathlib import Path

# Add parent directory to path so we can import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas import GoalInterpretation

gi = GoalInterpretation(
    title="Study Planner",
    one_liner="Helps students create weekly study plans and track progress.",
    target_users=["College students"],
    constraints=["MVP in 2 weeks", "Local demo"],
    assumptions=["Users will input assignments manually"],
    success_metrics=["Users plan at least 5 tasks/week", "Weekly retention > 40%"],
)

print(gi.model_dump())
