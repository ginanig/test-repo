# backend/app/edf_uploads/router.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Annotated

from . import schemas, services, models
from ..core.database import get_db, engine
from ..auth.router import get_current_active_user
from ..auth.models import User as AuthUser

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/edf",
    tags=["EDF File Uploads"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload", response_model=schemas.EdfUploadResponse)
async def upload_edf_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Annotated[AuthUser, Depends(get_current_active_user)] = Depends()
):
    '''
    Uploads an EDF file.
    The file is "simulated" to be stored in S3 and its metadata is saved in the database.
    Max file size is 500.
    '''
    if not current_user: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    try:
        metadata = await services.process_edf_upload(db, file, current_user)
    except HTTPException as e:
        raise e 
    except Exception as e:
        print(f"Unexpected error during EDF upload: {e}") 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred processing the file.")

    return schemas.EdfUploadResponse(
        message="File uploaded successfully (simulated). Metadata saved.",
        file_id=metadata.id,
        filename=metadata.filename,
        s3_key=metadata.s3_key
    )

@router.get("/files", response_model=List[schemas.EdfFileMetadataRead])
async def list_my_edf_files(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Annotated[AuthUser, Depends(get_current_active_user)] = Depends()
):
    if not current_user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    files = services.list_user_edf_files(db, user_id=current_user.id, skip=skip, limit=limit)
    return files

@router.get("/files/{file_id}", response_model=schemas.EdfFileMetadataRead)
async def get_edf_file_details(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[AuthUser, Depends(get_current_active_user)] = Depends()
):
    if not current_user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    file_metadata = services.get_edf_file_metadata(db, file_id=file_id, user_id=current_user.id)
    if not file_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File metadata not found or you do not have permission to access it.")
    return file_metadata
