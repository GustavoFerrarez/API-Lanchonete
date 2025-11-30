from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.produto import ProdutoCreate, ProdutoOut, ProdutoUpdate
from app.repositories import produto as repo
from app.services.produto import criar_produto

rotas = APIRouter(prefix="/v1/produto", tags=["produto"])

@rotas.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def create(payload: ProdutoCreate, db: Session = Depends(get_db)):
    criar_produto(payload)
    return repo.create(db, payload)

@rotas.get("/", response_model=list[ProdutoOut])
def list_all(db: Session = Depends(get_db)):
    return repo.get_all(db)

@rotas.get("/{produto_id}", response_model=ProdutoOut)
def get_id(produto_id:int, db: Session=Depends(get_db)):
    objeto = repo.get(db, produto_id)
    if not objeto: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto nao encontrado")
    return objeto

@rotas.put("/{produto_id}", response_model=ProdutoOut)
def update(produto_id: int, payload: ProdutoUpdate, db: Session = Depends(get_db)):
    objeto = repo.update(db, produto_id, payload)
    if not objeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto nao encontrado")
    return objeto

@rotas.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(produto_id: int, db: Session = Depends(get_db)):
    if not repo.delete(db, produto_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto nao encontrado")