# backend/app/edf_uploads/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class EdfFileMetadataBase(BaseModel):
    filename: str
    file_size_bytes: int
    s3_bucket: Optional[str] = None
    s3_key: str
    
    patient_info: Optional[Dict[str, Any]] = None
    n_channels: Optional[int] = None
    sfreq: Optional[float] = None
    duration_seconds: Optional[float] = None
    processing_status: Optional[str] = "UPLOADED"

class EdfFileMetadataCreate(EdfFileMetadataBase):
    user_id: int 

class EdfFileMetadataRead(EdfFileMetadataBase):
    id: int
    user_id: int
    upload_timestamp: datetime

    class Config:
        orm_mode = True

class EdfUploadResponse(BaseModel):
    message: str
    file_id: int
    filename: str
    s3_key: str
