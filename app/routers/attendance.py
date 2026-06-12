from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timezone
from app.dependencies import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import ClockInRequest, AttendanceOut
from app.auth import get_current_user

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/clock-in", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def clock_in(
    payload: ClockInRequest,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Clock in for today. Async I/O-bound operation."""
    today = date.today()
    existing = db.query(Attendance).filter(
        Attendance.employee_id == current_user.id,
        Attendance.date == today,
        Attendance.status == "open"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in today. Clock out first.")
    record = Attendance(
        employee_id=current_user.id,
        date=today,
        clock_in=datetime.now(timezone.utc),
        note=payload.note,
        status="open"
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/clock-out", response_model=AttendanceOut)
async def clock_out(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Clock out and calculate hours worked."""
    today = date.today()
    record = db.query(Attendance).filter(
        Attendance.employee_id == current_user.id,
        Attendance.date == today,
        Attendance.status == "open"
    ).first()
    if not record:
        raise HTTPException(status_code=400, detail="No open clock-in found for today")
    clock_out_time = datetime.now(timezone.utc)
    record.clock_out = clock_out_time
    record.hours_worked = round(
        (clock_out_time - record.clock_in.replace(tzinfo=timezone.utc)).total_seconds() / 3600, 2
    )
    record.status = "closed"
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[AttendanceOut])
def list_attendance(
    employee_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """List attendance records. Employees see only their own."""
    query = db.query(Attendance)
    if current_user.role == "employee":
        query = query.filter(Attendance.employee_id == current_user.id)
    elif employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if from_date:
        query = query.filter(Attendance.date >= from_date)
    if to_date:
        query = query.filter(Attendance.date <= to_date)
    return query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()