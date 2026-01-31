"""
Rotas administrativas de episódios.
CRUD completo e publicação de episódios (requer autenticação).
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.schemas import (
    EpisodeResponse, EpisodeCreate, EpisodeUpdate,
    EpisodePublish, MessageResponse
)
from app.crud.episode import (
    get_episode, get_episodes, create_episode,
    update_episode, delete_episode, publish_episode, unpublish_episode
)
from app.api.v1.auth import get_current_user
from app.models.models import EpisodeStatus

router = APIRouter(prefix="/episodes", tags=["admin-episodes"])


@router.get("", response_model=List[EpisodeResponse])
def list_all_episodes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filtrar por status: DRAFT ou PUBLISHED"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Lista todos os episódios (incluindo rascunhos).
    Apenas para admins autenticados.
    """
    status_filter = None
    if status:
        try:
            status_filter = EpisodeStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status inválido. Use DRAFT ou PUBLISHED"
            )
    
    episodes = get_episodes(db, skip=skip, limit=limit, status=status_filter)
    return episodes


@router.post("", response_model=EpisodeResponse, status_code=status.HTTP_201_CREATED)
def create_new_episode(
    episode: EpisodeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cria novo episódio.
    Por padrão criado como DRAFT.
    """
    return create_episode(db, episode)


@router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode_by_id(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Detalhe de episódio específico (incluindo rascunhos)."""
    episode = get_episode(db, episode_id)
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    return episode


@router.put("/{episode_id}", response_model=EpisodeResponse)
def update_episode_by_id(
    episode_id: int,
    episode_update: EpisodeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Atualiza episódio existente."""
    updated_episode = update_episode(db, episode_id, episode_update)
    if not updated_episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    return updated_episode


@router.delete("/{episode_id}", response_model=MessageResponse)
def delete_episode_by_id(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deleta episódio."""
    deleted = delete_episode(db, episode_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    return {"message": "Episódio deletado com sucesso"}


@router.patch("/{episode_id}/publish", response_model=EpisodeResponse)
def publish_episode_by_id(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Publica episódio (muda status para PUBLISHED).
    Define published_at como datetime atual se não foi definido.
    """
    published = publish_episode(db, episode_id)
    if not published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    return published


@router.patch("/{episode_id}/unpublish", response_model=EpisodeResponse)
def unpublish_episode_by_id(
    episode_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Despublica episódio (muda status para DRAFT)."""
    unpublished = unpublish_episode(db, episode_id)
    if not unpublished:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    return unpublished
