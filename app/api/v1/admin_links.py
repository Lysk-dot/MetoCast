"""
Rotas administrativas de links oficiais.
CRUD completo de links (requer autenticação).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import (
    OfficialLinkResponse, OfficialLinkCreate,
    OfficialLinkUpdate, MessageResponse
)
from app.crud.link import get_link, get_links, create_link, update_link, delete_link
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/links", tags=["admin-links"])


@router.get("", response_model=List[OfficialLinkResponse])
def list_all_links(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todos os links oficiais."""
    return get_links(db)


@router.post("", response_model=OfficialLinkResponse, status_code=status.HTTP_201_CREATED)
def create_new_link(
    link: OfficialLinkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cria novo link oficial."""
    return create_link(db, link)


@router.get("/{link_id}", response_model=OfficialLinkResponse)
def get_link_by_id(
    link_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Detalhe de link específico."""
    link = get_link(db, link_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    return link


@router.put("/{link_id}", response_model=OfficialLinkResponse)
def update_link_by_id(
    link_id: int,
    link_update: OfficialLinkUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Atualiza link existente."""
    updated_link = update_link(db, link_id, link_update)
    if not updated_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    return updated_link


@router.delete("/{link_id}", response_model=MessageResponse)
def delete_link_by_id(
    link_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deleta link oficial."""
    deleted = delete_link(db, link_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    return {"message": "Link deletado com sucesso"}
