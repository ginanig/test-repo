# backend/app/auth/services.py
from fastapi.security import OAuth2PasswordBearer # Adicionar esta linha
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas
from ..core.security import get_password_hash, verify_password, create_access_token
from ..core.config import settings # Import settings
from datetime import timedelta
from typing import Optional # Ensure Optional is imported for type hinting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # Adicionar esta linha

# --- Funções CRUD para Usuário ---
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=True # Por padrão, ativa o usuário. Pode mudar para envio de email de confirmação.
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções de Autenticação ---
def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, user_login: schemas.UserLogin) -> schemas.Token:
    db_user = authenticate_user(db, email=user_login.email, password=user_login.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "user_id": db_user.id}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

# --- Funções de Recuperação de Senha (Simuladas) ---
def request_password_recovery(db: Session, email: str) -> bool:
    user = get_user_by_email(db, email)
    if not user:
        # Não revele se o email existe ou não por segurança, mas para debug pode ser útil
        # raise HTTPException(status_code=404, detail="User not found")
        return False # Simula que o processo foi iniciado
    
    # Lógica para gerar um token de recuperação e enviar email (simulado)
    # Por exemplo, poderia salvar um token no DB com um tempo de expiração
    print(f"Password recovery requested for {email}. Token: fake_recovery_token_for_{email}")
    return True

def reset_password(db: Session, reset_data: schemas.PasswordReset) -> bool:
    # Lógica para validar o token (simulado)
    # Por exemplo, buscar o token no DB, verificar expiração e usuário associado
    # Aqui, vamos assumir que o token é válido se contiver "fake_recovery_token_for_"
    
    if not reset_data.token.startswith("fake_recovery_token_for_"):
        raise HTTPException(status_code=400, detail="Invalid or expired recovery token")

    # Extrair o email do token (simulação)
    try:
        email_from_token = reset_data.token.split("fake_recovery_token_for_")[1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    user = get_user_by_email(db, email_from_token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found based on token")

    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    return True
