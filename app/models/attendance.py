from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id           = Column(Integer, primary_key=True, index=True)
    employee_id  = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date         = Column(Date, nullable=False)
    clock_in     = Column(DateTime(timezone=True), nullable=True)
    clock_out    = Column(DateTime(timezone=True), nullable=True)
    hours_worked = Column(Float, nullable=True)
    note         = Column(String(255), nullable=True)
    status       = Column(String(20), default="open")

    employee = relationship("Employee", back_populates="attendances")