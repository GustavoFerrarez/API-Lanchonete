from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0) # Garante que a quantidade seja maior que 0

class ItemPedidoCreate(ItemPedidoBase):
    pedido_id: int

class ItemPedidoUpdate(BaseModel):
    quantidade: int = Field(gt=0) # Só permite atualizar a quantidade

class ItemPedidoOut(ItemPedidoBase):
    id: int
    pedido_id: int
    produto_id: Optional[int] = None
    preco_unitario: float
    subtotal: float # Vamos calcular isso no repositório
    
    model_config = ConfigDict(from_attributes=True)