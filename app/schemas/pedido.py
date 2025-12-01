from pydantic import BaseModel, ConfigDict
from typing import Optional

class PedidoBase(BaseModel):
    usuario_id: Optional[int] = None
    observacoes: Optional[str] = None

class PedidoCreate(PedidoBase):
    # Pedidos são criados vazios e os itens adicionados depois,
    # ou podemos receber os itens aqui. Vamos manter simples por enquanto.
    pass

class PedidoUpdate(BaseModel):
    status: Optional[str] = None
    observacoes: Optional[str] = None
    # 'total' e 'usuario_id' geralmente não são atualizáveis manualmente

class PedidoOut(PedidoBase):
    id: int
    status: str
    total: float
    model_config = ConfigDict(from_attributes=True)