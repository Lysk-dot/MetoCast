"""
Operações CRUD para OfficialLink.
Funções para criar, ler, atualizar e deletar links oficiais.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import OfficialLink
from app.schemas.schemas import OfficialLinkCreate, OfficialLinkUpdate


def get_link(db: Session, link_id: int) -> Optional[OfficialLink]:
    """Busca link por ID."""
    return db.query(OfficialLink).filter(OfficialLink.id == link_id).first()


def get_links(db: Session) -> List[OfficialLink]:
    """
    Lista todos os links oficiais ordenados por 'order'.
    """
    return db.query(OfficialLink).order_by(OfficialLink.order).all()


def create_link(db: Session, link: OfficialLinkCreate) -> OfficialLink:
    """Cria novo link oficial."""
    db_link = OfficialLink(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def update_link(
    db: Session,
    link_id: int,
    link_update: OfficialLinkUpdate
) -> Optional[OfficialLink]:
    """Atualiza link existente."""
    db_link = get_link(db, link_id)
    if not db_link:
        return None
    
    update_data = link_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_link, field, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link


def delete_link(db: Session, link_id: int) -> bool:
    """
    Deleta link oficial.
    
    Returns:
        True se deletado, False se não encontrado
    """
    db_link = get_link(db, link_id)
    if not db_link:
        return False
    
    db.delete(db_link)
    db.commit()
    return True
