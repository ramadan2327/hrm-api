from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Salary(Base):
    __tablename__ = "salaries"

    id             = Column(Integer, primary_key=True, index=True)
    employee_id    = Column(Integer, ForeignKey("employees.id"), nullable=False)
    amount         = Column(Float, nullable=False)
    currency       = Column(String(10), default="SLL")
    effective_date = Column(Date, nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="salaries")