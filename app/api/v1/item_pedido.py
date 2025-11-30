from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoOut, ItemPedidoUpdate
from app.repositories import item_pedido as repo

rotas = APIRouter(prefix="/v1/item_pedido", tags=["item_pedido"])

@rotas.post("/", response_model=ItemPedidoOut, status_code=status.HTTP_201_CREATED)
def create(payload: ItemPedidoCreate, db: Session = Depends(get_db)):
    # O subtotal é calculado dinamicamente no schema de saída
    item = repo.create(db, payload)
    subtotal = item.quantidade * item.preco_unitario
    return {**item.__dict__, "subtotal": subtotal} # Adiciona o subtotal na resposta

@rotas.get("/", response_model=list[ItemPedidoOut])
def list_all(db: Session = Depends(get_db)):
    itens = repo.get_all(db)
    # Adiciona o subtotal para cada item
    return [
        {**item.__dict__, "subtotal": item.quantidade * item.preco_unitario} 
        for item in itens
    ]

@rotas.get("/pedido/{pedido_id}", response_model=list[ItemPedidoOut])
def list_by_pedido_id(pedido_id: int, db: Session = Depends(get_db)):
    """ Lista todos os itens de um pedido específico """
    itens = repo.get_by_pedido_id(db, pedido_id)
    return [
        {**item.__dict__, "subtotal": item.quantidade * item.preco_unitario} 
        for item in itens
    ]

@rotas.get("/{item_id}", response_model=ItemPedidoOut)
def get_id(item_id: int, db: Session = Depends(get_db)):
    item = repo.get(db, item_id)
    if not item: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item não encontrado")
    subtotal = item.quantidade * item.preco_unitario
    return {**item.__dict__, "subtotal": subtotal}

@rotas.put("/{item_id}", response_model=ItemPedidoOut)
def update(item_id: int, payload: ItemPedidoUpdate, db: Session = Depends(get_db)):
    item = repo.update(db, item_id, payload)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item não encontrado")
    subtotal = item.quantidade * item.preco_unitario
    return {**item.__dict__, "subtotal": subtotal}

@rotas.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(item_id: int, db: Session = Depends(get_db)):
    if not repo.delete(db, item_id):
        raise HTTPException(status.HTTP_44_NOT_FOUND, "Item não encontrado")