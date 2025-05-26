# backend/app/core/config.py
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do arquivo .env

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db") # Default para SQLite se não definido
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env" # Especifica o arquivo .env a ser usado (opcional se load_dotenv() for usado)
        # case_sensitive = True # Descomente se suas variáveis de ambiente forem case-sensitive

settings = Settings()
