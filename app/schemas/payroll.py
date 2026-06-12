from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class SalaryCreate(BaseModel):
    amount: float = Field(gt=0)
    currency: str = "SLL"
    effective_date: date


class SalaryOut(BaseModel):
    id: int
    employee_id: int
    amount: float
    currency: str
    effective_date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class PaySummaryItem(BaseModel):
    employee_id: int
    full_name: str
    annual_salary: float
    monthly_salary: float
    currency: str


class PaySummaryOut(BaseModel):
    month: str
    data: List[PaySummaryItem]
    total_payroll: float