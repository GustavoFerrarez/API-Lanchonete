from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Connection
from sqlalchemy import text
from app.db.deps import get_connection
from app.schemas.categoria import CategoriaCreate, CategoriaOut

rotas = APIRouter()

@rotas.get("/categorias")
def listar_categorias(conn: Connection = Depends(get_connection)):
    sql = text("SELECT * FROM categorias")
    linhas =  conn.execute(sql).mappings().all()
    return linhas


@rotas.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create(payload: CategoriaCreate, conn: Connection = Depends(get_connection)):
    ##return repo.create(db, payload)
    nome = payload.nome
    sql = text("""
               INSERT INTO categorias (nome)
               VALUES (:nome) RETURNING id, nome
               """)
    try:
        result =  conn.execute(sql, {"nome":nome}).mappings().one()
        #conn.commit() ## engine.begin() ja faz o commit automatico
        return result
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            f"Erro ao inserir categoria: {e}")