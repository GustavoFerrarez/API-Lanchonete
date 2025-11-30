from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoUpdate
from fastapi import HTTPException

# --- FUNÇÃO HELPER DE NEGÓCIO ---
# Esta função calcula o total do pedido somando os subtotais dos seus itens
# e atualiza o pedido principal.
def atualizar_total_pedido(db: Session, pedido_id: int):
    # Calcula a soma de (quantidade * preco_unitario) para todos os itens
    # de um pedido específico.
    subtotais = db.query(
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario)
    ).filter(ItemPedido.pedido_id == pedido_id)
    
    novo_total = subtotais.scalar() or 0.0

    # Busca o pedido e atualiza seu total
    pedido = db.get(Pedido, pedido_id)
    if pedido:
        pedido.total = novo_total
        db.add(pedido)
        # O commit será feito pela função principal (create, update, delete)
        
# --- FUNÇÕES CRUD ---

def create(db: Session, payload: ItemPedidoCreate) -> ItemPedido:
    # 1. Buscar o Produto para pegar o preço
    produto = db.get(Produto, payload.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # 2. Verificar se o Pedido existe
    pedido = db.get(Pedido, payload.pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
    # 3. Criar o ItemPedido
    objeto = ItemPedido(
        produto_id=payload.produto_id,
        quantidade=payload.quantidade,
        pedido_id=payload.pedido_id,
        preco_unitario=produto.preco # Regra de negócio: Preço vem do produto!
    )
    
    db.add(objeto)
    
    # 4. Atualizar o total do pedido (usando a função helper)
    # Fazemos o commit aqui para que o 'objeto' exista no DB
    # antes de 'atualizar_total_pedido' ser chamado
    db.commit()
    atualizar_total_pedido(db, payload.pedido_id)
    db.commit() # Commit final para o total do pedido
    
    db.refresh(objeto)
    return objeto

def get(db: Session, item_id: int) -> ItemPedido | None:
    return db.get(ItemPedido, item_id)

def get_all(db: Session) -> list[ItemPedido]:
    return db.query(ItemPedido).order_by(ItemPedido.id).all()

def get_by_pedido_id(db: Session, pedido_id: int) -> list[ItemPedido]:
    """ Busca todos os itens de um pedido específico """
    return db.query(ItemPedido).filter(ItemPedido.pedido_id == pedido_id).all()

def update(db: Session, item_id: int, payload: ItemPedidoUpdate) -> ItemPedido | None:
    objeto = get(db, item_id)
    if not objeto:
        return None
    
    # Atualiza os campos (apenas quantidade)
    objeto.quantidade = payload.quantidade
        
    db.add(objeto)
    
    # Atualiza o total e commita
    db.commit()
    atualizar_total_pedido(db, objeto.pedido_id)
    db.commit()
    
    db.refresh(objeto)
    return objeto

def delete(db: Session, item_id: int) -> bool:
    objeto = get(db, item_id)
    if not objeto:
        return False
        
    pedido_id = objeto.pedido_id # Salva o ID antes de deletar
    
    db.delete(objeto)
    
    # Atualiza o total e commita
    db.commit()
    atualizar_total_pedido(db, pedido_id)
    db.commit()
    
    return True