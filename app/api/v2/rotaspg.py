from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v2 import categoria_rotas


api_rotas = APIRouter()

api_rotas.include_router(categoria_rotas.rotas)
