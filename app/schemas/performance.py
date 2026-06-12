from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    employee_id: int
    period: str
    score: float = Field(ge=1.0, le=5.0)
    comments: Optional[str] = None


class ReviewOut(BaseModel):
    id: int
    employee_id: int
    reviewer_id: Optional[int]
    period: str
    score: float
    comments: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}