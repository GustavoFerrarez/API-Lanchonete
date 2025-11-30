## conexao com postgresql

from sqlalchemy import create_engine
from app.core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.PG_USER}:{settings.PG_PASSWORD}"
    f"@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}"
)

engine = create_engine(
    DATABASE_URL,
    pool_size = 10,   # maximo de conexoes
    max_overflow = 0, # evita criar conexoes extras
    pool_timeout= 5,  # tempo de retorno em segundos
    pool_pre_ping= True # verifica se a conexao esta "viva"
)

def get_connection():
    with engine.connect() as conn:
        yield conn  ## garante contexto com fechamento automatico


if __name__ == "__main__":
    from sqlalchemy import text
    with engine.connect() as conn:

        sql = "SELECT * FROM categorias"
        result = conn.execute(text(sql))
        rows = result.fetchall()
        for row in rows:
            print(f"id: {row.id} - nome: {row.nome_categoria}")