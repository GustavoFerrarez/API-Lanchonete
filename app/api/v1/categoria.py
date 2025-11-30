from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db # Assumindo que get_db existe e retorna Session
## Se get_db não existir, e você quiser usar o get_connection de deps.py
## o padrão muda. Vamos manter o get_db por enquanto,
## pois é o que o repositório espera (Session).

# Importar o CategoriaUpdate
from app.schemas.categoria import CategoriaCreate, CategoriaOut, CategoriaUpdate 
from app.repositories import categoria as repo

rotas = APIRouter(prefix="/v1/categoria", tags=["categoria"])

@rotas.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload)

@rotas.get("/", response_model=list[CategoriaOut])
def list_all(db: Session = Depends(get_db)):
    return repo.get_all(db)


@rotas.get("/{categoria_id}", response_model=CategoriaOut)
def get_id(categoria_id:int, db: Session=Depends(get_db)):
    objeto = repo.get(db, categoria_id)
    if not objeto: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria nao encontrada")
    return objeto


@rotas.put("/{categoria_id}", response_model=CategoriaOut)
def update(categoria_id: int, payload: CategoriaUpdate, db: Session = Depends(get_db)):
    objeto = repo.update(db, categoria_id, payload)
    if not objeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria nao encontrada")
    return objeto

@rotas.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(categoria_id: int, db: Session = Depends(get_db)):
    if not repo.delete(db, categoria_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria nao encontrada")
    # Retorna 204 No Content, que não envia corpo de resposta