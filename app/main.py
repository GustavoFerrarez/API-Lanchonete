from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
# 1. IMPORTAR AS ROTAS DA V1 (ao invés da V2)
from app.api.v1.rotas import api_rotas 
from fastapi.middleware.cors import CORSMiddleware

# criar as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. INCLUIR AS ROTAS DA V1
app.include_router(api_rotas)