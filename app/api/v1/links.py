"""
Rotas públicas de links oficiais.
Listagem de links das redes sociais e plataformas do Metocast.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.schemas import OfficialLinkResponse
from app.crud.link import get_links

router = APIRouter(prefix="/links", tags=["links"])


@router.get("", response_model=List[OfficialLinkResponse])
def list_official_links(db: Session = Depends(get_db)):
    """
    Lista todos os links oficiais do projeto.
    Ordenados pelo campo 'order'.
    """
    links = get_links(db)
    return links
