from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    id          = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    period      = Column(String(20), nullable=False)
    score       = Column(Float, nullable=False)
    comments    = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="reviews",
                            foreign_keys=[employee_id])