from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.estoque import Estoque  
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoUpdate
from fastapi import HTTPException, status 

# --- FUNÇÃO HELPER DE NEGÓCIO ---
def atualizar_total_pedido(db: Session, pedido_id: int):
    subtotais = db.query(
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario)
    ).filter(ItemPedido.pedido_id == pedido_id)
    
    novo_total = subtotais.scalar() or 0.0

    pedido = db.get(Pedido, pedido_id)
    if pedido:
        pedido.total = novo_total
        db.add(pedido)

# --- FUNÇÕES CRUD ---

def create(db: Session, payload: ItemPedidoCreate) -> ItemPedido:
    # 1. Buscar o Produto
    produto = db.get(Produto, payload.produto_id)
    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    # --- 2. LÓGICA DE ESTOQUE (NOVO) ---
    # Busca o registro de estoque deste produto
    item_estoque = db.query(Estoque).filter(Estoque.produto_id == payload.produto_id).first()
    
    # Se não existir registro na tabela estoque
    if not item_estoque:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Produto sem registro de estoque. Contate o administrador."
        )
        
    # Verifica se tem quantidade suficiente
    if item_estoque.quantidade < payload.quantidade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Estoque insuficiente. Restam apenas {item_estoque.quantidade} unidades."
        )

    # Subtrai a quantidade do estoque
    item_estoque.quantidade -= payload.quantidade
    db.add(item_estoque) 
    # -----------------------------------

    # 3. Verificar se o Pedido existe
    pedido = db.get(Pedido, payload.pedido_id)
    if not pedido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
        
    # 4. Criar o ItemPedido
    objeto = ItemPedido(
        produto_id=payload.produto_id,
        quantidade=payload.quantidade,
        pedido_id=payload.pedido_id,
        preco_unitario=produto.preco
    )
    
    db.add(objeto)
    
    # 5. Commit e Atualização de totais
    db.commit() # Salva o item e a baixa no estoque
    
    atualizar_total_pedido(db, payload.pedido_id)
    db.commit() # Salva o novo total do pedido
    
    db.refresh(objeto)
    return objeto

def get(db: Session, item_id: int) -> ItemPedido | None:
    return db.get(ItemPedido, item_id)

def get_all(db: Session) -> list[ItemPedido]:
    return db.query(ItemPedido).order_by(ItemPedido.id).all()

def get_by_pedido_id(db: Session, pedido_id: int) -> list[ItemPedido]:
    return db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido_id).all()

def update(db: Session, item_id: int, payload: ItemPedidoUpdate) -> ItemPedido | None:
    # Nota: Atualizar quantidade num cenário real exigiria devolver o antigo ao estoque
    # e subtrair o novo. Para simplificar, mantivemos apenas a atualização do item.
    objeto = get(db, item_id)
    if not objeto:
        return None
    
    objeto.quantidade = payload.quantidade
        
    db.add(objeto)
    
    db.commit()
    atualizar_total_pedido(db, objeto.pedido_id)
    db.commit()
    
    db.refresh(objeto)
    return objeto

def delete(db: Session, item_id: int) -> bool:
    objeto = get(db, item_id)
    if not objeto:
        return False
        
    pedido_id = objeto.pedido_id
    
    # Nota: Num sistema real, ao deletar o item, você deveria devolver a quantidade ao estoque:
    # item_estoque = db.query(Estoque).filter(Estoque.produto_id == objeto.produto_id).first()
    # if item_estoque:
    #     item_estoque.quantidade += objeto.quantidade
    
    db.delete(objeto)
    
    db.commit()
    atualizar_total_pedido(db, pedido_id)
    db.commit()
    
    return True