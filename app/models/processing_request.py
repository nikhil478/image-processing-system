from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class ProcessingRequest(Base):
    __tablename__ = "processing_requests"

    request_id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    processed_images = relationship("ProcessedImage", back_populates="processing_request")