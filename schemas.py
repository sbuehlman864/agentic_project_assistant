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