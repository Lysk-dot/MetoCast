"""
Aplicação principal FastAPI - Metocast Hub API.
Configura rotas, middlewares e documentação.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, episodes, links, admin_episodes, admin_links

# Criar instância do FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gerenciamento de episódios e links do Metocast",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Lista de origens permitidas para CORS
origins = [
    "http://localhost:5173",      # Desenvolvimento local
    "http://localhost:3000",      # Frontend alternativo
    "http://192.168.15.10:5173",  # Rede local (Dell T110)
    "https://lysk-dot.github.io", # GitHub Pages
    # Adicione seu domínio CloudFlare quando tiver
    # "https://metocast.seudominio.com",
    # "https://api.metocast.seudominio.com",
]

# Em produção, use as origins do settings (variável de ambiente)
import os
if os.getenv("DEBUG", "True").lower() == "false":
    origins = settings.origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Rotas Públicas ====================
# Rotas acessíveis sem autenticação

# Autenticação
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

# Episódios públicos (apenas PUBLISHED)
app.include_router(episodes.router, prefix=settings.API_V1_PREFIX)

# Links oficiais públicos
app.include_router(links.router, prefix=settings.API_V1_PREFIX)


# ==================== Rotas Administrativas ====================
# Rotas protegidas por autenticação JWT

# Admin: Episódios (CRUD completo)
app.include_router(admin_episodes.router, prefix=settings.ADMIN_API_PREFIX)

# Admin: Links oficiais (CRUD completo)
app.include_router(admin_links.router, prefix=settings.ADMIN_API_PREFIX)


# ==================== Endpoints Básicos ====================

@app.get("/")
def root():
    """Endpoint raiz - informações da API."""
    return {
        "message": "Metocast Hub API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ==================== Event Handlers ====================

@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a aplicação."""
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} iniciado!")
    print(f"📚 Documentação: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao encerrar a aplicação."""
    print("👋 Aplicação encerrada!")
