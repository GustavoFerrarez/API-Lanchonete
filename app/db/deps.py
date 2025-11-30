from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from app.db.session import engine

# Cria uma "fábrica" de sessões ligada ao seu engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependência do FastAPI para gerenciar a sessão do banco de dados (ORM).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()