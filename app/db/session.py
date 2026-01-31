"""
Configuração do banco de dados SQLAlchemy.
Engine, SessionLocal e Base para os modelos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log de queries SQL quando DEBUG=True
    pool_pre_ping=True,   # Verifica conexão antes de usar
)

# SessionLocal: factory para criar sessões de DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos herdarem
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão de banco de dados.
    Usado nas rotas FastAPI com Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
