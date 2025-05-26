# backend/app/credits/services.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import func # Para simulated_charge_id
from fastapi import HTTPException, status
from typing import Optional, List # Adicionado List
from . import models, schemas
from ..auth.models import User 
# import stripe
# from ..core.config import settings
# stripe.api_key = settings.STRIPE_SECRET_KEY

def get_credit_package(db: Session, package_id: int) -> Optional[models.CreditPackage]:
    return db.query(models.CreditPackage).filter(models.CreditPackage.id == package_id, models.CreditPackage.is_active == True).first()

def list_active_credit_packages(db: Session) -> List[models.CreditPackage]:
    return db.query(models.CreditPackage).filter(models.CreditPackage.is_active == True).order_by(models.CreditPackage.price).all()

def create_transaction_db(db: Session, user: User, package: models.CreditPackage, charge_id: Optional[str] = None, status: models.TransactionStatus = models.TransactionStatus.PENDING) -> models.Transaction:
    transaction = models.Transaction(
        user_id=user.id,
        package_id=package.id,
        amount_paid=package.price, 
        credits_purchased=package.credits_awarded,
        status=status,
        payment_gateway_charge_id=charge_id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def simulate_stripe_payment_intent(package: models.CreditPackage, user: User):
    print(f"Simulating Stripe Payment Intent for user {user.email} and package {package.name}")
    simulated_client_secret = f"pi_{package.id}_{user.id}_secret_{str(func.now())}" # Convertido func.now() para str
    simulated_charge_id = f"ch_{package.id}_{user.id}_{str(func.now())}" # Convertido func.now() para str
    return simulated_client_secret, simulated_charge_id

async def process_package_purchase(db: Session, purchase_request: schemas.PurchaseRequest, current_user: User) -> schemas.PurchaseResponse:
    package = get_credit_package(db, package_id=purchase_request.package_id)
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit package not found or not active.")
    
    client_secret, charge_id = simulate_stripe_payment_intent(package, current_user)
    
    transaction = create_transaction_db(db, user=current_user, package=package, charge_id=charge_id, status=models.TransactionStatus.PENDING)
    
    return schemas.PurchaseResponse(
        message="PaymentIntent created successfully. Please confirm payment on the client-side.",
        client_secret=client_secret,
        transaction_id=transaction.id
    )
