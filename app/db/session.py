"""
Configuração do banco de dados SQLAlchemy.
Engine, SessionLocal e Base para os modelos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configurar args de conexão (SSL para produção Railway)
connect_args = {}
database_url = settings.DATABASE_URL

# Railway usa SSL - ajusta URL se necessário
if "railway" in database_url or "rlwy" in database_url:
    # Para alguns drivers, precisa sslmode
    if "sslmode" not in database_url:
        if "?" in database_url:
            database_url += "&sslmode=require"
        else:
            database_url += "?sslmode=require"

# Engine do SQLAlchemy
engine = create_engine(
    database_url,
    echo=settings.DEBUG,  # Log de queries SQL quando DEBUG=True
    pool_pre_ping=True,   # Verifica conexão antes de usar
    connect_args=connect_args
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
