# backend/app/edf_uploads/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class EdfFileMetadata(Base):
    __tablename__ = "edf_file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    s3_bucket = Column(String, nullable=True) 
    s3_key = Column(String, unique=True, nullable=False) 
    
    file_size_bytes = Column(Integer, nullable=False)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    patient_info = Column(JSON, nullable=True) 
    n_channels = Column(Integer, nullable=True)
    sfreq = Column(Float, nullable=True) 
    duration_seconds = Column(Float, nullable=True)
    
    processing_status = Column(String, default="UPLOADED", index=True) # e.g., UPLOADED, PROCESSING, COMPLETED, FAILED

    user = relationship("User")
