from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.categoria import Categoria
from fastapi import HTTPException
from app.schemas.produto import ProdutoCreate, ProdutoUpdate

def create(db: Session, payload: ProdutoCreate) -> Produto:
    categoria = db.get(Categoria, payload.categoria_id)
    if not categoria:
        raise HTTPException(
            status_code = 400,
            detail="Categoria nao encontrada"
        )
    objeto = Produto(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)

def get_all(db: Session) -> list[Produto]:
    return db.query(Produto).order_by(Produto.id).all()

# --- DEFS FALTANTES ---

def update(db: Session, produto_id: int, payload: ProdutoUpdate) -> Produto | None:
    """ Atualiza um produto """
    objeto = get(db, produto_id)
    if not objeto:
        return None
        
    # Verifica se a categoria nova existe (se ela for enviada)
    if payload.categoria_id:
        categoria = db.get(Categoria, payload.categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=400,
                detail="Categoria nao encontrada"
            )

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(objeto, key, value)
        
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def delete(db: Session, produto_id: int) -> bool:
    """ Deleta um produto """
    objeto = get(db, produto_id)
    if not objeto:
        return False
        
    db.delete(objeto)
    db.commit()
    return True