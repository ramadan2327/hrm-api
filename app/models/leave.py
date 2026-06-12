from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class LeaveTypeEnum(str, enum.Enum):
    annual  = "annual"
    sick    = "sick"
    unpaid  = "unpaid"


class LeaveStatusEnum(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id           = Column(Integer, primary_key=True, index=True)
    employee_id  = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type   = Column(Enum(LeaveTypeEnum), nullable=False)
    start_date   = Column(Date, nullable=False)
    end_date     = Column(Date, nullable=False)
    days         = Column(Integer, nullable=False)
    reason       = Column(Text, nullable=True)
    status       = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending)
    approved_by  = Column(Integer, ForeignKey("employees.id"), nullable=True)
    comment      = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    action_at    = Column(DateTime(timezone=True), nullable=True)

    employee = relationship("Employee", back_populates="leave_requests",
                            foreign_keys=[employee_id])