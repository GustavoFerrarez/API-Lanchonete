from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.usuario import Usuario # Para verificar se o usuário existe
from app.schemas.pedido import PedidoCreate, PedidoUpdate
from fastapi import HTTPException

def create(db: Session, payload: PedidoCreate) -> Pedido:
    # Verifica se o usuário existe
    usuario = db.get(Usuario, payload.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    objeto = Pedido(**payload.model_dump())
    # Valores padrão já são definidos no model
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, pedido_id: int) -> Pedido | None:
    return db.get(Pedido, pedido_id)

def get_all(db: Session) -> list[Pedido]:
    return db.query(Pedido).order_by(Pedido.id).all()

def update(db: Session, pedido_id: int, payload: PedidoUpdate) -> Pedido | None:
    objeto = get(db, pedido_id)
    if not objeto:
        return None
    
    update_data = payload.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(objeto, key, value)
        
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def delete(db: Session, pedido_id: int) -> bool:
    objeto = get(db, pedido_id)
    if not objeto:
        return False
        
    db.delete(objeto)
    db.commit()
    return True