from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin    = "admin"
    manager  = "manager"
    employee = "employee"


class StatusEnum(str, enum.Enum):
    active   = "active"
    inactive = "inactive"


class Employee(Base):
    __tablename__ = "employees"

    id                = Column(Integer, primary_key=True, index=True)
    full_name         = Column(String(150), nullable=False)
    email             = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password   = Column(String, nullable=False)
    phone             = Column(String(20), nullable=True)
    job_title         = Column(String(100), nullable=True)
    hire_date         = Column(Date, nullable=True)
    role              = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    status            = Column(Enum(StatusEnum), default=StatusEnum.active, nullable=False)
    department_id     = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at        = Column(DateTime(timezone=True), server_default=func.now())

    department     = relationship("Department", back_populates="employees")
    attendances    = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee",
                                  foreign_keys="LeaveRequest.employee_id")
    salaries       = relationship("Salary", back_populates="employee")
    reviews        = relationship("PerformanceReview", back_populates="employee",
                                  foreign_keys="PerformanceReview.employee_id")