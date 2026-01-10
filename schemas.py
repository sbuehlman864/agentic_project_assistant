from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List

class GoalInterpretation(BaseModel):
    title: str
    one_liner: str
    target_users: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)


class PRD(BaseModel):
    title: str
    problem: str
    target_users: List[str] = Field(default_factory=list)

    goals: List[str] = Field(default_factory=list)
    non_goals: List[str] = Field(default_factory=list)

    user_stories: List[str] = Field(default_factory=list)

    functional_requirements: List[str] = Field(default_factory=list)
    nonfunctional_requirements: List[str] = Field(default_factory=list)

    risks: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)


class Milestone(BaseModel):
    name: str
    objective: str
    deliverables: List[str] = Field(default_factory=list)
    est_days: int

class MilestonesDoc(BaseModel):
    title: str
    milestones: List[Milestone] = Field(default_factory=list)
