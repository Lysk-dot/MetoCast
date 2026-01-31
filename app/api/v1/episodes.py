"""
Rotas públicas de episódios.
Listagem e detalhes de episódios publicados (sem autenticação).
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import EpisodeResponse
from app.crud.episode import get_episode, get_published_episodes

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get("", response_model=List[EpisodeResponse])
def list_published_episodes(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=100, description="Limite de registros"),
    db: Session = Depends(get_db)
):
    """
    Lista episódios publicados.
    Retorna apenas episódios com status PUBLISHED.
    """
    episodes = get_published_episodes(db, skip=skip, limit=limit)
    return episodes


@router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode_detail(
    episode_id: int,
    db: Session = Depends(get_db)
):
    """
    Detalhe de um episódio específico.
    Retorna 404 se episódio não existe ou não está publicado.
    """
    episode = get_episode(db, episode_id)
    
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    
    # Apenas episódios publicados são acessíveis publicamente
    if episode.status != "PUBLISHED":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episódio não encontrado"
        )
    
    return episode
