from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, index=True, nullable=False)
    senha = Column(VARCHAR(255), nullable=False) # Em um projeto real, armazene um hash!
    tipo_usuario = Column(VARCHAR(20), default='cliente')
    
    # Relacionamento: Um usuário pode ter vários pedidos
    pedidos = relationship("Pedido", back_populates="usuario")