from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db
from app.models.performance import PerformanceReview
from app.models.employee import Employee
from app.schemas.performance import ReviewCreate, ReviewOut
from app.auth import get_current_user, require_roles

router = APIRouter(prefix="/performance", tags=["Performance Reviews"])


@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(require_roles("admin", "manager"))
):
    """Create a performance review. Admin and Manager only."""
    emp = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    review = PerformanceReview(
        employee_id=payload.employee_id,
        reviewer_id=current_user.id,
        period=payload.period,
        score=payload.score,
        comments=payload.comments,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/", response_model=List[ReviewOut])
def list_reviews(
    employee_id: Optional[int] = None,
    period: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """List performance reviews. Employees see only their own."""
    query = db.query(PerformanceReview)
    if current_user.role == "employee":
        query = query.filter(PerformanceReview.employee_id == current_user.id)
    elif employee_id:
        query = query.filter(PerformanceReview.employee_id == employee_id)
    if period:
        query = query.filter(PerformanceReview.period == period)
    return query.order_by(PerformanceReview.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Get a single review by ID."""
    review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user.role == "employee" and review.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(require_roles("admin"))
):
    """Delete a review. Admin only."""
    review = db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()