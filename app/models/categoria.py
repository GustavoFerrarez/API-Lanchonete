from sqlalchemy import Column, Integer, String, Text 
from sqlalchemy.orm import relationship
from app.db.base import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    
    # CORREÇÃO:
    # Diz ao SQLAlchemy que a coluna no banco de dados é "nome_categoria",
    # mas em Python, queremos continuar acessando como "nome".
    nome = Column("nome_categoria", String) 
    
    descricao = Column(Text, nullable=True)
    
    produtos = relationship(
        "Produto", 
        back_populates="categoria",
        cascade="all, delete-orphan")