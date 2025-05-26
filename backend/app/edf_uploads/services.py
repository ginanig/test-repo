# backend/app/edf_uploads/services.py
import os
import shutil 
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from typing import Optional, List
from uuid import uuid4 

from . import models, schemas
from ..auth.models import User
# import boto3 
# from botocore.exceptions import ClientError
# from ..core.config import settings

SIMULATED_S3_BUCKET = "eeg-platform-data-mock"
UPLOAD_DIR = "temp_uploads" 
os.makedirs(UPLOAD_DIR, exist_ok=True) # Garante que o diretório de upload exista

def save_edf_metadata(db: Session, metadata_create: schemas.EdfFileMetadataCreate) -> models.EdfFileMetadata:
    db_metadata = models.EdfFileMetadata(**metadata_create.dict())
    db.add(db_metadata)
    db.commit()
    db.refresh(db_metadata)
    return db_metadata

async def process_edf_upload(db: Session, file: UploadFile, current_user: User) -> models.EdfFileMetadata:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided.")
    
    if not file.filename.lower().endswith(".edf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only EDF files are allowed.")

    s3_object_name = f"user_{current_user.id}/edf_files/{uuid4()}_{file.filename}"
    
    temp_file_path = os.path.join(UPLOAD_DIR, s3_object_name.replace("/", "_")) 
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(f"Local save error: {e}")
        raise HTTPException(status_code=500, detail=f"Could not save file locally: {e}")
    finally:
        await file.close() 
    
    file_size = os.path.getsize(temp_file_path) 

    MAX_FILE_SIZE_BYTES = 500 * 1024 * 1024 
    if file_size > MAX_FILE_SIZE_BYTES:
        os.remove(temp_file_path) 
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_BYTES // (1024*1024)}."
        )

    metadata_values = {
        "user_id": current_user.id,
        "filename": file.filename,
        "s3_bucket": SIMULATED_S3_BUCKET, 
        "s3_key": s3_object_name,
        "file_size_bytes": file_size, 
        "processing_status": "UPLOADED"
    }
    metadata_create = schemas.EdfFileMetadataCreate(**metadata_values)
    
    db_metadata = save_edf_metadata(db, metadata_create)
    
    return db_metadata

def get_edf_file_metadata(db: Session, file_id: int, user_id: int) -> Optional[models.EdfFileMetadata]:
    return db.query(models.EdfFileMetadata).filter(models.EdfFileMetadata.id == file_id, models.EdfFileMetadata.user_id == user_id).first()

def list_user_edf_files(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.EdfFileMetadata]:
    return db.query(models.EdfFileMetadata).filter(models.EdfFileMetadata.user_id == user_id).order_by(models.EdfFileMetadata.upload_timestamp.desc()).offset(skip).limit(limit).all()
