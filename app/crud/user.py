"""
Operações CRUD para AdminUser.
Funções para criar, ler, atualizar usuários administradores.
"""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.models import AdminUser
from app.schemas.schemas import AdminUserCreate, AdminUserUpdate
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[AdminUser]:
    """Busca usuário por email."""
    return db.query(AdminUser).filter(AdminUser.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[AdminUser]:
    """Busca usuário por ID."""
    return db.query(AdminUser).filter(AdminUser.id == user_id).first()


def create_user(db: Session, user: AdminUserCreate) -> AdminUser:
    """
    Cria novo usuário admin.
    Hash da senha é gerado automaticamente.
    """
    db_user = AdminUser(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role="ADMIN"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[AdminUser]:
    """
    Autentica usuário verificando email e senha.
    
    Returns:
        AdminUser se credenciais válidas, None caso contrário
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    
    return user


def update_user(
    db: Session,
    user_id: int,
    user_update: AdminUserUpdate
) -> Optional[AdminUser]:
    """Atualiza usuário existente."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Se senha foi fornecida, gera novo hash
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
