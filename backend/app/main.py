# backend/app/main.py
from fastapi import FastAPI
from .auth import router as auth_router
from .credits import router as credits_router # Nova importação
from .edf_uploads import router as edf_router # Nova importação
# from .core.database import engine, Base # Removido Base, engine é usado no router de auth

# Base.metadata.create_all(bind=engine) # Movido para auth.router para ser mais modular
                                     # ou melhor ainda, usar Alembic.

app = FastAPI(
    title="EEG Platform API",
    version="0.1.0",
    description="API para a plataforma de análise de EEG.",
    # Adicionar mais metadados se necessário
)

@app.on_event("startup")
async def startup_event():
    # Em um app de produção, você usaria Alembic ou similar para gerenciar migrações de DB.
    # Para desenvolvimento rápido, pode-se criar tabelas aqui, mas é melhor no módulo específico
    # ou via um script de inicialização.
    # models.Base.metadata.create_all(bind=engine) # Exemplo se fosse centralizado
    print("Startup: Tabelas de autenticação (e outras) devem ser criadas se não existirem (via auth.router).")
    # Aqui você poderia adicionar lógica para verificar conexão com DB, Redis, etc.

app.include_router(auth_router.router)
app.include_router(credits_router.router) # Nova linha para o router de créditos
app.include_router(edf_router.router) # Nova linha para o router de EDF uploads

@app.get("/")
async def root():
    return {"message": "Welcome to EEG Platform API. Visit /docs for API documentation."}

# Outros routers serão adicionados aqui (e.g., para créditos, uploads)
