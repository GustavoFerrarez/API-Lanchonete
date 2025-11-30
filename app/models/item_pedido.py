from sqlalchemy import Column, Integer, NUMERIC, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(NUMERIC(10, 2), nullable=False)
    # O subtotal é gerado pelo banco, como no seu Estrutura do BANCO.txt
    
    # Relacionamento: Um item pertence a um pedido
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    pedido = relationship("Pedido", back_populates="itens")
    
    # Relacionamento: Um item refere-se a um produto
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="SET NULL")) 
    produto = relationship("Produto") # Simplifiquei