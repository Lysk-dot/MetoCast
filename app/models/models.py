"""
Modelos de banco de dados usando SQLAlchemy ORM.
Define as tabelas: Episode, OfficialLink e AdminUser.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from app.db.session import Base


class EpisodeStatus(str, Enum):
    """Status possíveis de um episódio."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class LinkType(str, Enum):
    """Tipos de links oficiais."""
    INSTAGRAM = "INSTAGRAM"
    YOUTUBE = "YOUTUBE"
    SPOTIFY = "SPOTIFY"
    SITE = "SITE"
    OTHER = "OTHER"


class Episode(Base):
    """
    Modelo de episódio do podcast.
    
    Representa um episódio com título, descrição, links
    e status de publicação.
    """
    __tablename__ = "episodes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(EpisodeStatus), default=EpisodeStatus.DRAFT, nullable=False)
    cover_image_url = Column(String(500), nullable=True)
    spotify_url = Column(String(500), nullable=True)
    youtube_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # Formato: "tag1,tag2,tag3"
    
    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Episode(id={self.id}, title='{self.title}', status={self.status})>"


class OfficialLink(Base):
    """
    Links oficiais do projeto Metocast.
    
    Links para redes sociais e plataformas onde o podcast está disponível.
    """
    __tablename__ = "official_links"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)  # Ex: "Instagram", "Spotify"
    url = Column(String(500), nullable=False)
    type = Column(SQLEnum(LinkType), default=LinkType.OTHER, nullable=False)
    order = Column(Integer, default=0, nullable=False)  # Para ordenação na exibição
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<OfficialLink(id={self.id}, label='{self.label}', type={self.type})>"


class AdminUser(Base):
    """
    Usuário administrador do sistema.
    
    Usuários que podem acessar o painel administrativo
    e gerenciar episódios e links.
    """
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="ADMIN", nullable=False)
    is_active = Column(Integer, default=1)  # 1 = ativo, 0 = inativo
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AdminUser(id={self.id}, email='{self.email}', role={self.role})>"
