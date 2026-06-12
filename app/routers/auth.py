from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.employee import Employee
from app.schemas.token import Token
from app.schemas.employee import EmployeeCreate, EmployeeOut
from app.auth import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with email and password. Returns JWT token."""
    user = db.query(Employee).filter(Employee.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):
    """Register a new user account."""
    if db.query(Employee).filter(Employee.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
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