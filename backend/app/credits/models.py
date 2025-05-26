# backend/app/credits/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class CreditPackage(Base):
    __tablename__ = "credit_packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False) # Preço em BRL, por exemplo
    credits_awarded = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TransactionStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Link com a tabela User
    package_id = Column(Integer, ForeignKey("credit_packages.id"), nullable=True) # Pode ser null se for um ajuste manual de crédito
    
    amount_paid = Column(Float, nullable=False) # Valor efetivamente pago
    credits_purchased = Column(Integer, nullable=False) # Quantidade de créditos
    
    status = Column(SAEnum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    payment_gateway_charge_id = Column(String, nullable=True) # ID da cobrança no Stripe, por exemplo
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User") # Relacionamento para fácil acesso ao usuário
    package = relationship("CreditPackage") # Relacionamento para fácil acesso ao pacote
