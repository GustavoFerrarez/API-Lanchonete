from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Estoque(Base):
    __tablename__ = "estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    
    # Relacionamento com Produto
    # ondelete="CASCADE" garante que se o produto sumir, o estoque some também
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), unique=True)
    produto = relationship("Produto")