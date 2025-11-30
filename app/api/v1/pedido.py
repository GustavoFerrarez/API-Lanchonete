from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.pedido import PedidoCreate, PedidoOut, PedidoUpdate
from app.repositories import pedido as repo

rotas = APIRouter(prefix="/v1/pedido", tags=["pedido"])

@rotas.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def create(payload: PedidoCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload)

@rotas.get("/", response_model=list[PedidoOut])
def list_all(db: Session = Depends(get_db)):
    return repo.get_all(db)

@rotas.get("/{pedido_id}", response_model=PedidoOut)
def get_id(pedido_id: int, db: Session = Depends(get_db)):
    objeto = repo.get(db, pedido_id)
    if not objeto: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
    return objeto

@rotas.put("/{pedido_id}", response_model=PedidoOut)
def update(pedido_id: int, payload: PedidoUpdate, db: Session = Depends(get_db)):
    objeto = repo.update(db, pedido_id, payload)
    if not objeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")
    return objeto

@rotas.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(pedido_id: int, db: Session = Depends(get_db)):
    if not repo.delete(db, pedido_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido não encontrado")