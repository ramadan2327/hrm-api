from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ClockInRequest(BaseModel):
    note: Optional[str] = None


class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    date: date
    clock_in: Optional[datetime]
    clock_out: Optional[datetime]
    hours_worked: Optional[float]
    note: Optional[str]
    status: str

    model_config = {"from_attributes": True}