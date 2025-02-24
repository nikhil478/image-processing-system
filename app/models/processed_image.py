from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, ForeignKey("processing_requests.request_id"), nullable=False)
    serial_number = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    input_images = Column(Text, nullable=False)
    output_images = Column(Text, nullable=True) 

    processing_request = relationship("ProcessingRequest", back_populates="processed_images")
