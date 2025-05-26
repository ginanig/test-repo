# backend/app/auth/schemas.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

# Esquema base para usuário (informações públicas)
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Esquema para criação de usuário (recebe a senha)
class UserCreate(UserBase):
    password: constr(min_length=8)

# Esquema para ler usuário (não inclui a senha)
class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    # updated_at: Optional[datetime] # Descomente se quiser incluir

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos ORM

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para o token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquema para recuperação de senha (solicitação)
class PasswordRecoveryRequest(BaseModel):
    email: EmailStr

# Esquema para resetar a senha
class PasswordReset(BaseModel):
    token: str # Token enviado por email (simulado aqui)
    new_password: constr(min_length=8)
