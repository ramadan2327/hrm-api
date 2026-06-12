from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db
from app.models.employee import Employee
from app.models.department import Department
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.auth import hash_password, get_current_user, require_roles

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/dashboard/summary", tags=["Dashboard"])
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """Dashboard summary — shows key HR metrics at a glance."""
    from app.models.attendance import Attendance
    from app.models.leave import LeaveRequest, LeaveStatusEnum
    from datetime import date

    total_employees   = db.query(Employee).filter(Employee.status == "active").count()
    total_departments = db.query(Department).count()
    pending_leaves    = db.query(LeaveRequest).filter(LeaveRequest.status == "pending").count()
    on_leave_today    = db.query(LeaveRequest).filter(
        LeaveRequest.status == LeaveStatusEnum.approved,
        LeaveRequest.start_date <= date.today(),
        LeaveRequest.end_date   >= date.today()
    ).count()
    clocked_in_today  = db.query(Attendance).filter(
        Attendance.date   == date.today(),
        Attendance.status == "open"
    ).count()

    return {
        "total_active_employees":    total_employees,
        "total_departments":         total_departments,
        "pending_leave_requests":    pending_leaves,
        "employees_on_leave_today":  on_leave_today,
        "employees_clocked_in_today": clocked_in_today,
        "generated_at":              date.today().isoformat(),
    }


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """List all employees. Admin and Manager only."""
    query = db.query(Employee)
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    if status:
        query = query.filter(Employee.status == status)
    if search:
        query = query.filter(Employee.full_name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Create a new employee. Admin only."""
    if db.query(Employee).filter(Employee.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    if payload.department_id:
        if not db.query(Department).filter(Department.id == payload.department_id).first():
            raise HTTPException(status_code=404, detail="Department not found")
    emp = Employee(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        phone=payload.phone,
        job_title=payload.job_title,
        hire_date=payload.hire_date,
        role=payload.role,
        department_id=payload.department_id,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user)
):
    """Get employee by ID. Employees can only view their own profile."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    if current_user.role == "employee" and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return emp


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager"))
):
    """Update employee. Admin and Manager only."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    return emp


@router.patch("/{employee_id}/deactivate", response_model=EmployeeOut)
def deactivate_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    """Deactivate an employee. Admin only."""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    if emp.status == "inactive":
        raise HTTPException(status_code=400, detail="Employee is already inactive")
    emp.status = "inactive"
    db.commit()
    db.refresh(emp)
    return emp