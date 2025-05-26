# backend/app/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, services, models
from ..core.database import get_db, engine # Adicionado engine
from ..core.security import decode_access_token
from typing import Annotated # Para Depends com Python 3.9+

# Cria as tabelas no banco de dados (apenas para desenvolvimento/teste inicial)
# Em produção, você usaria Alembic para migrações.
models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

# --- Dependência para obter o usuário atual a partir do token ---
async def get_current_user(token: Annotated[str, Depends(services.oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = services.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Endpoints ---
@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = services.create_user(db=db, user=user)
    return created_user

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[schemas.UserLogin, Depends()], db: Session = Depends(get_db)):
    # Nota: FastAPI usa python-multipart para processar form data se não for JSON.
    # Se você enviar JSON, use: user_login: schemas.UserLogin
    # Aqui, para compatibilidade com OAuth2PasswordRequestForm, FastAPI espera form data.
    # Se quiser JSON, mude o Depends() para o schema diretamente.
    # Por simplicidade, vamos manter UserLogin e assumir que o cliente envia JSON.
    # Para usar OAuth2PasswordRequestForm, seria:
    # from fastapi.security import OAuth2PasswordRequestForm
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    # e então usar form_data.username e form_data.password

    # Usando o schema UserLogin diretamente (espera JSON)
    token = services.login_user(db, user_login=form_data)
    return token

@router.post("/password-recovery", status_code=status.HTTP_200_OK)
async def request_password_recovery(recovery_request: schemas.PasswordRecoveryRequest, db: Session = Depends(get_db)):
    # Em um app real, isso enviaria um email com um link/token de recuperação.
    # Aqui, apenas simulamos e logamos no console.
    success = services.request_password_recovery(db, email=recovery_request.email)
    if not success:
        # Não informamos se o email foi encontrado ou não para evitar enumeração de usuários
        # mas retornamos um status que sugere que a operação foi aceita.
        print(f"Password recovery attempt for non-existing or problematic email: {recovery_request.email}")
    return {"msg": "If an account with that email exists, a password recovery link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_data: schemas.PasswordReset, db: Session = Depends(get_db)):
    success = services.reset_password(db, reset_data=reset_data)
    if not success:
        # A função service.reset_password já levanta HTTPExceptions em caso de falha
        # Este retorno é para o caso de sucesso.
        pass # Não é necessário, pois a exceção seria levantada antes
    return {"msg": "Password has been reset successfully."}

@router.get("/users/me", response_model=schemas.UserRead)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    # Endpoint protegido para obter informações do usuário logado
    return current_user

# Adicionar a dependência oauth2_scheme em services.py
# (Esta linha é um comentário para você, a adição real é no services.py)
