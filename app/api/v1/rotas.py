from fastapi import APIRouter
from app.api.v1 import produto, categoria, usuario, pedido 

# 1. IMPORTAR AS NOVAS ROTAS DE item_pedido
from app.api.v1 import item_pedido

api_rotas = APIRouter()

# 2. INCLUIR TODAS AS 5 ROTAS
api_rotas.include_router(produto.rotas)
api_rotas.include_router(categoria.rotas)
api_rotas.include_router(usuario.rotas)
api_rotas.include_router(pedido.rotas)
api_rotas.include_router(item_pedido.rotas)