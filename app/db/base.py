from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Importar todos os modelos para que o Base os conheça
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido