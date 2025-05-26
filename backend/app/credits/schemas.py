# backend/app/credits/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .models import TransactionStatus # Importar o Enum

class CreditPackageBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    credits_awarded: int
    is_active: bool = True

class CreditPackageCreate(CreditPackageBase):
    pass

class CreditPackageRead(CreditPackageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    user_id: int
    package_id: Optional[int] = None
    amount_paid: float
    credits_purchased: int
    status: TransactionStatus
    payment_gateway_charge_id: Optional[str] = None

class TransactionCreate(BaseModel): 
    package_id: int

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    package: Optional[CreditPackageRead] = None 

    class Config:
        orm_mode = True

class PurchaseRequest(BaseModel):
    package_id: int

class PurchaseResponse(BaseModel):
    message: str
    transaction_id: Optional[int] = None
    client_secret: Optional[str] = None
