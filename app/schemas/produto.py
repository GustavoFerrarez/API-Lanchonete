from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria_id: Optional[int] = None
    descricao: Optional[str] = None 
    imagem_url: Optional[str] = None 
    ingredientes: Optional[str] = None 

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    categoria_id: Optional[int] = None
    descricao: Optional[str] = None 
    imagem_url: Optional[str] = None 
    ingredientes: Optional[str] = None 
    