from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import re
from app.dependencies import get_db
from app.models.payroll import Salary
from app.models.employee import Employee
from app.schemas.payroll import SalaryCreate, SalaryOut, PaySummaryOut, PaySummaryItem
from app.auth import require_roles

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.put("/{employee_id}/salary", response_model=SalaryOut)
def set_salary(
    employee_id: int,
    payload: SalaryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Set or update employee salary. Admin only."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    salary = Salary(
        employee_id=employee_id,
        amount=payload.amount,
        currency=payload.currency,
        effective_date=payload.effective_date,
    )
    db.add(salary)
    db.commit()
    db.refresh(salary)
    return salary


@router.get("/summary", response_model=PaySummaryOut)
def pay_summary(
    month: str,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Get monthly pay summary. Admin only. Format: YYYY-MM"""
    if not re.match(r"^\d{4}-\d{2}$", month):
        raise HTTPException(status_code=400, detail="month must be in format YYYY-MM")
    query = db.query(Employee).filter(Employee.status == "active")
    if employee_id:
        query = query.filter(Employee.id == employee_id)
    employees = query.all()
    data = []
    for emp in employees:
        latest = (
            db.query(Salary)
            .filter(
                Salary.employee_id == emp.id,
                Salary.effective_date <= f"{month}-28"
            )
            .order_by(Salary.effective_date.desc())
            .first()
        )
        annual = latest.amount if latest else 0.0
        data.append(PaySummaryItem(
            employee_id=emp.id,
            full_name=emp.full_name,
            annual_salary=annual,
            monthly_salary=round(annual / 12, 2),
            currency=latest.currency if latest else "SLL",
        ))
    total = round(sum(d.monthly_salary for d in data), 2)
    return PaySummaryOut(month=month, data=data, total_payroll=total)


@router.get("/{employee_id}/history", response_model=List[SalaryOut])
def salary_history(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Get salary history for an employee. Admin only."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return (
        db.query(Salary)
        .filter(Salary.employee_id == employee_id)
        .order_by(Salary.effective_date.desc())
        .all()
    )