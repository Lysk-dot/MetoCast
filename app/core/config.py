"""
Configurações da aplicação usando Pydantic Settings.
Carrega variáveis de ambiente do arquivo .env
"""
import os
from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import List, Optional


class Settings(BaseSettings):
    # Database - Railway pode usar DATABASE_URL ou DATABASE_PUBLIC_URL
    DATABASE_URL: Optional[str] = None
    DATABASE_PUBLIC_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "metocast-super-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_PREFIX: str = "/api"
    ADMIN_API_PREFIX: str = "/api/admin"
    
    # CORS - adicione URLs de produção do frontend
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://localhost:5173,https://lysk-dot.github.io,https://metocast.vercel.app"
    
    # App
    PROJECT_NAME: str = "Metocast Hub API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False  # False em produção
    
    @model_validator(mode='after')
    def set_database_url(self):
        """Usa DATABASE_URL se disponível, senão DATABASE_PUBLIC_URL"""
        if not self.DATABASE_URL:
            if self.DATABASE_PUBLIC_URL:
                self.DATABASE_URL = self.DATABASE_PUBLIC_URL
            else:
                self.DATABASE_URL = "postgresql://metocast:metocast123@localhost:5432/metocast_hub"
        return self
    
    @property
    def origins_list(self) -> List[str]:
        """Converte string de origins em lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()
