from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext # 1. Importar

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """ Gera o hash da senha """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifica se a senha em texto plano bate com o hash """
    return pwd_context.verify(plain_password, hashed_password)

# --- Funções CRUD ---

def create(db: Session, payload: UsuarioCreate) -> Usuario:
    # 3. Hashear a senha ANTES de criar
    hashed_password = get_password_hash(payload.senha)
    
    # Criar um dicionário sem a senha original
    usuario_data = payload.model_dump(exclude={"senha"})
    
    objeto = Usuario(**usuario_data, senha=hashed_password)
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, usuario_id: int) -> Usuario | None:
    return db.get(Usuario, usuario_id)

def get_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).order_by(Usuario.id).all()

def update(db: Session, usuario_id: int, payload: UsuarioUpdate) -> Usuario | None:
    objeto = get(db, usuario_id)
    if not objeto:
        return None
    
    update_data = payload.model_dump(exclude_unset=True)
    
    # 4. Hashear a nova senha se ela for alterada
    if "senha" in update_data and update_data["senha"]:
        hashed_password = get_password_hash(update_data["senha"])
        update_data["senha"] = hashed_password
    else:
        # Garante que não salve um campo 'senha' vazio
        update_data.pop("senha", None) 
        
    for key, value in update_data.items():
        setattr(objeto, key, value)
        
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def delete(db: Session, usuario_id: int) -> bool:
    objeto = get(db, usuario_id)
    if not objeto:
        return False
        
    db.delete(objeto)
    db.commit()
    return True