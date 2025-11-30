from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_usuario: Optional[str] = 'cliente'

class UsuarioCreate(UsuarioBase):
    senha: str # Senha é obrigatória na criação

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    tipo_usuario: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    