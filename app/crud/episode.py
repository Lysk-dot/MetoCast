"""
Operações CRUD para Episode.
Funções para criar, ler, atualizar e deletar episódios no banco.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.models import Episode, EpisodeStatus
from app.schemas.schemas import EpisodeCreate, EpisodeUpdate


def get_episode(db: Session, episode_id: int) -> Optional[Episode]:
    """Busca episódio por ID."""
    return db.query(Episode).filter(Episode.id == episode_id).first()


def get_episodes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[EpisodeStatus] = None
) -> List[Episode]:
    """
    Lista episódios com paginação e filtro opcional por status.
    
    Args:
        db: Sessão do banco
        skip: Quantos registros pular (para paginação)
        limit: Limite de registros a retornar
        status: Filtro opcional por status
    """
    query = db.query(Episode)
    
    if status:
        query = query.filter(Episode.status == status)
    
    return query.order_by(Episode.published_at.desc()).offset(skip).limit(limit).all()


def get_published_episodes(db: Session, skip: int = 0, limit: int = 100) -> List[Episode]:
    """Lista apenas episódios publicados."""
    return get_episodes(db, skip, limit, status=EpisodeStatus.PUBLISHED)


def create_episode(db: Session, episode: EpisodeCreate) -> Episode:
    """Cria novo episódio."""
    db_episode = Episode(**episode.model_dump())
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode


def update_episode(
    db: Session,
    episode_id: int,
    episode_update: EpisodeUpdate
) -> Optional[Episode]:
    """
    Atualiza episódio existente.
    Apenas campos fornecidos são atualizados (exclude_unset=True).
    """
    db_episode = get_episode(db, episode_id)
    if not db_episode:
        return None
    
    update_data = episode_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_episode, field, value)
    
    db.commit()
    db.refresh(db_episode)
    return db_episode


def publish_episode(db: Session, episode_id: int) -> Optional[Episode]:
    """Publica um episódio (muda status para PUBLISHED)."""
    db_episode = get_episode(db, episode_id)
    if not db_episode:
        return None
    
    db_episode.status = EpisodeStatus.PUBLISHED
    if not db_episode.published_at:
        db_episode.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_episode)
    return db_episode


def unpublish_episode(db: Session, episode_id: int) -> Optional[Episode]:
    """Despublica um episódio (muda status para DRAFT)."""
    db_episode = get_episode(db, episode_id)
    if not db_episode:
        return None
    
    db_episode.status = EpisodeStatus.DRAFT
    
    db.commit()
    db.refresh(db_episode)
    return db_episode


def delete_episode(db: Session, episode_id: int) -> bool:
    """
    Deleta episódio.
    
    Returns:
        True se deletado, False se não encontrado
    """
    db_episode = get_episode(db, episode_id)
    if not db_episode:
        return False
    
    db.delete(db_episode)
    db.commit()
    return True
