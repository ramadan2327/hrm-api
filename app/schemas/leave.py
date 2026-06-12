from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.models.leave import LeaveTypeEnum, LeaveStatusEnum


class LeaveRequestCreate(BaseModel):
    leave_type: LeaveTypeEnum
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveActionRequest(BaseModel):
    action: str = Field(pattern="^(approve|reject)$")
    comment: Optional[str] = None


class LeaveOut(BaseModel):
    id: int
    employee_id: int
    leave_type: LeaveTypeEnum
    start_date: date
    end_date: date
    days: int
    reason: Optional[str]
    status: LeaveStatusEnum
    approved_by: Optional[int]
    comment: Optional[str]
    submitted_at: datetime
    action_at: Optional[datetime]

    model_config = {"from_attributes": True}