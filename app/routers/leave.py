from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.dependencies import get_db
from app.models.leave import LeaveRequest
from app.models.employee import Employee
from app.schemas.leave import LeaveRequestCreate, LeaveActionRequest, LeaveOut
from app.auth import get_current_user, require_roles

router = APIRouter(prefix="/leave", tags=["Leave"])


@router.post("/request", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
def request_leave(
    payload: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Submit a leave request."""
    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    days = (payload.end_date - payload.start_date).days + 1
    leave = LeaveRequest(
        employee_id=current_user.id,
        leave_type=payload.leave_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        days=days,
        reason=payload.reason,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.get("/", response_model=List[LeaveOut])
def list_leaves(
    status: Optional[str] = None,
    leave_type: Optional[str] = None,
    employee_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """List leave requests. Employees see only their own."""
    query = db.query(LeaveRequest)
    if current_user.role == "employee":
        query = query.filter(LeaveRequest.employee_id == current_user.id)
    elif employee_id:
        query = query.filter(LeaveRequest.employee_id == employee_id)
    if status:
        query = query.filter(LeaveRequest.status == status)
    if leave_type:
        query = query.filter(LeaveRequest.leave_type == leave_type)
    return query.order_by(LeaveRequest.submitted_at.desc()).offset(skip).limit(limit).all()


@router.patch("/{leave_id}/action", response_model=LeaveOut)
def action_leave(
    leave_id: int,
    payload: LeaveActionRequest,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(require_roles("admin", "manager"))
):
    """Approve or reject a leave request. Admin and Manager only."""
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if leave.status != "pending":
        raise HTTPException(status_code=400, detail="Can only act on pending requests")
    if leave.employee_id == current_user.id:
        raise HTTPException(status_code=403, detail="Cannot action your own leave request")
    leave.status     = "approved" if payload.action == "approve" else "rejected"
    leave.approved_by = current_user.id
    leave.comment    = payload.comment
    leave.action_at  = datetime.now(timezone.utc)
    db.commit()
    db.refresh(leave)
    return leave