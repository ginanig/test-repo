# backend/app/credits/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from . import schemas, services, models
from ..core.database import get_db, engine
from ..auth.router import get_current_active_user 
from ..auth.models import User as AuthUser 

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/credits",
    tags=["Credits & Billing"],
    responses={404: {"description": "Not found"}},
)

@router.get("/packages", response_model=List[schemas.CreditPackageRead])
async def list_credit_packages(db: Session = Depends(get_db)):
    packages = services.list_active_credit_packages(db)
    return packages

@router.post("/purchase", response_model=schemas.PurchaseResponse)
async def purchase_credit_package(
    purchase_request: schemas.PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: Annotated[AuthUser, Depends(get_current_active_user)] = Depends()
):
    if current_user is None: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    response = await services.process_package_purchase(db, purchase_request, current_user)
    return response
