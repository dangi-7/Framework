from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class EvaluationBase(SQLModel):
    app_name: str = Field(index=True)
    audience: Optional[str] = None
    summary: Optional[str] = None
    pedagogical_design: int
    ui_ux: int
    engagement: int
    technical_performance: int
    learning_effectiveness: int
    quality_score: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Evaluation(EvaluationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EvaluationCreate(EvaluationBase):
    pass
