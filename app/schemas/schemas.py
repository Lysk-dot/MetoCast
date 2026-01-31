"""
Schemas Pydantic para validação e serialização de dados.
Define a estrutura de entrada e saída da API.
"""
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class EpisodeStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class LinkType(str, Enum):
    INSTAGRAM = "INSTAGRAM"
    YOUTUBE = "YOUTUBE"
    SPOTIFY = "SPOTIFY"
    SITE = "SITE"
    OTHER = "OTHER"


# ==================== Episode Schemas ====================

class EpisodeBase(BaseModel):
    """Schema base de episódio (campos comuns)."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    spotify_url: Optional[str] = None
    youtube_url: Optional[str] = None
    tags: Optional[str] = None  # Formato: "tag1,tag2,tag3"


class EpisodeCreate(EpisodeBase):
    """Schema para criar episódio."""
    status: EpisodeStatus = EpisodeStatus.DRAFT


class EpisodeUpdate(BaseModel):
    """Schema para atualizar episódio (todos campos opcionais)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    spotify_url: Optional[str] = None
    youtube_url: Optional[str] = None
    tags: Optional[str] = None
    status: Optional[EpisodeStatus] = None


class EpisodePublish(BaseModel):
    """Schema para publicar episódio."""
    published_at: Optional[datetime] = None  # Se None, usa datetime.now()


class EpisodeInDB(EpisodeBase):
    """Schema de episódio no banco (inclui campos gerados)."""
    id: int
    status: EpisodeStatus
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Permite criar a partir de modelo SQLAlchemy


# Alias para retorno público
EpisodeResponse = EpisodeInDB


# ==================== OfficialLink Schemas ====================

class OfficialLinkBase(BaseModel):
    """Schema base de link oficial."""
    label: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., min_length=1, max_length=500)
    type: LinkType = LinkType.OTHER
    order: int = Field(default=0, ge=0)


class OfficialLinkCreate(OfficialLinkBase):
    """Schema para criar link oficial."""
    pass


class OfficialLinkUpdate(BaseModel):
    """Schema para atualizar link (todos campos opcionais)."""
    label: Optional[str] = Field(None, min_length=1, max_length=100)
    url: Optional[str] = Field(None, min_length=1, max_length=500)
    type: Optional[LinkType] = None
    order: Optional[int] = Field(None, ge=0)


class OfficialLinkInDB(OfficialLinkBase):
    """Schema de link no banco."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Alias
OfficialLinkResponse = OfficialLinkInDB


# ==================== AdminUser Schemas ====================

class AdminUserBase(BaseModel):
    """Schema base de usuário admin."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class AdminUserCreate(AdminUserBase):
    """Schema para criar admin."""
    password: str = Field(..., min_length=8)


class AdminUserUpdate(BaseModel):
    """Schema para atualizar admin."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class AdminUserInDB(AdminUserBase):
    """Schema de admin no banco."""
    id: int
    role: str
    is_active: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Alias
AdminUserResponse = AdminUserInDB


# ==================== Auth Schemas ====================

class Token(BaseModel):
    """Schema de resposta de autenticação."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Dados extraídos do token."""
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema de requisição de login."""
    email: EmailStr
    password: str


# ==================== Generic Responses ====================

class MessageResponse(BaseModel):
    """Resposta genérica com mensagem."""
    message: str


class ErrorResponse(BaseModel):
    """Resposta de erro."""
    detail: str
