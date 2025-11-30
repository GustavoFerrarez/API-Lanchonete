from app.schemas.produto import ProdutoCreate
from fastapi import HTTPException, status

def criar_produto(payload: ProdutoCreate):
    preco = payload.preco
    if preco <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "#Preco deve ser maior que zero!")
    