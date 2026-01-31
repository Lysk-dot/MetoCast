"""
Script para popular banco com dados iniciais.
Cria usuário admin padrão e alguns dados de exemplo.
"""
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.crud.link import create_link
from app.crud.episode import create_episode
from app.schemas.schemas import (
    AdminUserCreate, OfficialLinkCreate, EpisodeCreate
)
from app.models.models import LinkType, EpisodeStatus


def seed_admin_user(db):
    """Cria usuário admin padrão."""
    admin_email = "admin@metocast.com"
    
    # Verifica se já existe
    existing = get_user_by_email(db, admin_email)
    if existing:
        print(f"✓ Admin já existe: {admin_email}")
        return existing
    
    # Criar novo admin
    admin = AdminUserCreate(
        name="Administrador Metocast",
        email=admin_email,
        password="admin123"  # MUDAR EM PRODUÇÃO!
    )
    
    user = create_user(db, admin)
    print(f"✓ Admin criado: {admin_email} / senha: admin123")
    return user


def seed_official_links(db):
    """Cria links oficiais de exemplo."""
    links_data = [
        {
            "label": "Spotify",
            "url": "https://open.spotify.com/show/metocast",
            "type": LinkType.SPOTIFY,
            "order": 1
        },
        {
            "label": "YouTube",
            "url": "https://youtube.com/@metocast",
            "type": LinkType.YOUTUBE,
            "order": 2
        },
        {
            "label": "Instagram",
            "url": "https://instagram.com/metocast",
            "type": LinkType.INSTAGRAM,
            "order": 3
        }
    ]
    
    for link_data in links_data:
        link = OfficialLinkCreate(**link_data)
        create_link(db, link)
        print(f"✓ Link criado: {link_data['label']}")


def seed_example_episodes(db):
    """Cria episódios de exemplo."""
    episodes_data = [
        {
            "title": "Episódio 1 - Introdução ao Metocast",
            "description": "Neste primeiro episódio apresentamos o projeto...",
            "status": EpisodeStatus.PUBLISHED,
            "spotify_url": "https://open.spotify.com/episode/exemplo1",
            "youtube_url": "https://youtube.com/watch?v=exemplo1",
            "tags": "introdução,primeiro,lançamento"
        },
        {
            "title": "Episódio 2 - Metodologia Científica",
            "description": "Discutimos os fundamentos da metodologia científica...",
            "status": EpisodeStatus.DRAFT,
            "tags": "ciência,metodologia"
        }
    ]
    
    for ep_data in episodes_data:
        episode = EpisodeCreate(**ep_data)
        create_episode(db, episode)
        print(f"✓ Episódio criado: {ep_data['title']}")


def main():
    """Executa seed do banco."""
    print("🌱 Iniciando seed do banco de dados...")
    
    db = SessionLocal()
    try:
        seed_admin_user(db)
        seed_official_links(db)
        seed_example_episodes(db)
        
        print("\n✅ Seed concluído com sucesso!")
        print("\n📝 Credenciais de acesso:")
        print("   Email: admin@metocast.com")
        print("   Senha: admin123")
        print("\n⚠️  IMPORTANTE: Altere a senha em produção!")
        
    except Exception as e:
        print(f"\n❌ Erro no seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
