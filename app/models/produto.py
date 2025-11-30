from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    
    
    nome = Column("nome_produto", String) 

    preco = Column(Float)
    
    descricao = Column(Text, nullable=True) 
    imagem_url = Column(Text, nullable=True) 
    ingredientes = Column(Text, nullable=True) 

    categoria_id = Column(
        Integer, 
        ForeignKey("categorias.id", ondelete="CASCADE"),
        nullable=False
    )
    categoria = relationship("Categoria", back_populates="produtos")