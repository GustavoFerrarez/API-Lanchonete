from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.repositories import usuario as repo

rotas = APIRouter(prefix="/v1/usuario", tags=["usuario"])

@rotas.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create(payload: UsuarioCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload)

@rotas.get("/", response_model=list[UsuarioOut])
def list_all(db: Session = Depends(get_db)):
    return repo.get_all(db)

@rotas.get("/{usuario_id}", response_model=UsuarioOut)
def get_id(usuario_id: int, db: Session = Depends(get_db)):
    objeto = repo.get(db, usuario_id)
    if not objeto: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    return objeto

@rotas.put("/{usuario_id}", response_model=UsuarioOut)
def update(usuario_id: int, payload: UsuarioUpdate, db: Session = Depends(get_db)):
    objeto = repo.update(db, usuario_id, payload)
    if not objeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    return objeto

@rotas.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(usuario_id: int, db: Session = Depends(get_db)):
    if not repo.delete(db, usuario_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")