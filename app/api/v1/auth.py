"""
Rotas de autenticação.
Login e geração de tokens JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas.schemas import Token, LoginRequest, AdminUserResponse
from app.crud.user import authenticate_user, get_user_by_email
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 scheme para extrair token do header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency para obter usuário atual a partir do token JWT.
    Usado em rotas protegidas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login.
    Recebe email e senha, retorna token JWT se credenciais válidas.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=AdminUserResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    """
    Retorna informações do usuário autenticado.
    """
    return current_user
