from sqlalchemy import Column, Integer, String, VARCHAR, NUMERIC, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(VARCHAR(20), default='novo')
    total = Column(NUMERIC(10, 2), default=0)
    observacoes = Column(TEXT)
    
    # Relacionamento: Um pedido pertence a um usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    usuario = relationship("Usuario", back_populates="pedidos")
    
    # Relacionamento: Um pedido tem vários itens
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")