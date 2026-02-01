"""
Configurações da aplicação usando Pydantic Settings.
Carrega variáveis de ambiente do arquivo .env
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database - tenta DATABASE_URL ou DATABASE_PUBLIC_URL (Railway)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        os.getenv("DATABASE_PUBLIC_URL", "postgresql://metocast:metocast123@localhost:5432/metocast_hub")
    )
    
    # Security
    SECRET_KEY: str = "sua-chave-secreta-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_PREFIX: str = "/api"
    ADMIN_API_PREFIX: str = "/api/admin"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # App
    PROJECT_NAME: str = "Metocast Hub API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    @property
    def origins_list(self) -> List[str]:
        """Converte string de origins em lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()
