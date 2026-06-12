from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from app.models.employee import RoleEnum, StatusEnum


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6)
    phone: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[date] = None
    role: RoleEnum = RoleEnum.employee
    department_id: Optional[int] = None


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    department_id: Optional[int] = None
    status: Optional[StatusEnum] = None


class EmployeeOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    job_title: Optional[str]
    hire_date: Optional[date]
    role: RoleEnum
    status: StatusEnum
    department_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}