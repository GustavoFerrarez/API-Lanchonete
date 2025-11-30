from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate # Importar CategoriaUpdate

def create(db:Session, payload: CategoriaCreate) -> Categoria:
    objeto = Categoria(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, categoria_id: int) -> Categoria | None:
    return db.get(Categoria, categoria_id)

def get_all(db: Session) -> list[Categoria]:
    return db.query(Categoria).order_by(Categoria.id).all()

# --- DEFS FALTANTES ---

def update(db: Session, categoria_id: int, payload: CategoriaUpdate) -> Categoria | None:
    """ Atualiza uma categoria """
    objeto = get(db, categoria_id) # Reutiliza a função get
    if not objeto:
        return None
    
    # Pega os dados do payload que não são None
    update_data = payload.model_dump(exclude_unset=True) 
    
    # Atualiza os campos do objeto
    for key, value in update_data.items():
        setattr(objeto, key, value)
        
    db.add(objeto) # Adiciona a sessão (necessário para o commit)
    db.commit()
    db.refresh(objeto)
    return objeto

def delete(db: Session, categoria_id: int) -> bool:
    """ Deleta uma categoria """
    objeto = get(db, categoria_id)
    if not objeto:
        return False
        
    db.delete(objeto)
    db.commit()
    return True