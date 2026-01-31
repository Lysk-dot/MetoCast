# Guia de Setup - Metocast Hub API

> Documentação do processo de configuração realizado em 31/01/2026

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Arquitetura](#arquitetura)
4. [Instalação](#instalação)
5. [Configuração](#configuração)
6. [Execução](#execução)
7. [Credenciais](#credenciais)
8. [Endpoints da API](#endpoints-da-api)
9. [Problemas Conhecidos](#problemas-conhecidos)
10. [Comandos Úteis](#comandos-úteis)

---

## Visão Geral

O **Metocast Hub** é uma API REST desenvolvida com FastAPI para gerenciamento de episódios e links oficiais do projeto Metocast.

### Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.12.3 | Linguagem principal |
| FastAPI | 0.109.0 | Framework web |
| PostgreSQL | 15-alpine | Banco de dados |
| SQLAlchemy | 2.0.25 | ORM |
| Alembic | 1.13.1 | Migrations |
| Docker | - | Container do banco |

---

## Pré-requisitos

- Python 3.11+ instalado
- Docker instalado e rodando
- Git configurado

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente                               │
│                    (Browser/App)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI (porta 8000)                       │
│                  Rodando localmente                          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Auth      │  │  Episodes   │  │   Official Links    │  │
│  │   (JWT)     │  │   CRUD      │  │      CRUD           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL (Docker - porta 5432)                │
│                  Container: metocast_db                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Lysk-dot/MetoCast.git
cd MetoCast
```

### 2. Configurar variáveis de ambiente

O arquivo `.env` já está configurado:

```env
# Database
DATABASE_URL=postgresql://metocast:metocast123@localhost:5432/metocast_hub

# Security
SECRET_KEY=lysk-9068
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_PREFIX=/api
ADMIN_API_PREFIX=/api/admin

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:5173

# App
PROJECT_NAME="Metocast Hub API"
VERSION=1.0.0
DEBUG=True
```

### 3. Criar ambiente virtual Python

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

**Pacotes instalados:**
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- python-multipart==0.0.6
- sqlalchemy==2.0.25
- alembic==1.13.1
- psycopg2-binary==2.9.9
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- bcrypt==4.1.2
- python-dotenv==1.0.0
- pydantic==2.5.3
- pydantic-settings==2.1.0
- email-validator==2.1.0.post1

---

## Configuração

### 1. Subir o banco de dados (Docker)

```bash
docker compose up -d db
```

Isso criará:
- Container: `metocast_db`
- Rede: `metocast_metocast_network`
- Volume: `metocast_postgres_data`

### 2. Verificar se o container está rodando

```bash
docker ps
```

Saída esperada:
```
CONTAINER ID   IMAGE                COMMAND                  STATUS         PORTS
3220cf593509   postgres:15-alpine   "docker-entrypoint.s…"   Up             0.0.0.0:5432->5432/tcp
```

### 3. Criar migration inicial

```bash
.venv/bin/alembic revision --autogenerate -m "Initial migration"
```

### 4. Aplicar migrations

```bash
.venv/bin/alembic upgrade head
```

### 5. Popular banco com dados iniciais

```bash
.venv/bin/python seed.py
```

Saída esperada:
```
✓ Admin criado: admin@metocast.com / senha: admin123
✓ Link criado: Spotify
✓ Link criado: YouTube
✓ Link criado: Instagram
✓ Episódio criado: Episódio 1 - Introdução ao Metocast
✓ Episódio criado: Episódio 2 - Metodologia Científica
✅ Seed concluído com sucesso!
```

---

## Execução

### Iniciar a API

```bash
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Ou com reload automático (desenvolvimento):

```bash
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### URLs de Acesso

| Descrição | URL |
|-----------|-----|
| API Base | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Acesso Externo (Tailscale) | http://100.87.142.37:8000 |

---

## Credenciais

### Administrador

| Campo | Valor |
|-------|-------|
| Email | `admin@metocast.com` |
| Senha | `admin123` |
| Role | ADMIN |

⚠️ **IMPORTANTE:** Altere a senha em produção!

### Banco de Dados

| Campo | Valor |
|-------|-------|
| Host | localhost |
| Porta | 5432 |
| Database | metocast_hub |
| Usuário | metocast |
| Senha | metocast123 |

---

## Endpoints da API

### Públicos (sem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/episodes` | Listar episódios publicados |
| GET | `/api/episodes/{id}` | Obter episódio por ID |
| GET | `/api/links` | Listar links oficiais |

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login` | Login (retorna JWT) |
| POST | `/api/auth/register` | Registrar novo admin |

### Admin (requer JWT)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/admin/episodes` | Listar todos episódios |
| POST | `/api/admin/episodes` | Criar episódio |
| PUT | `/api/admin/episodes/{id}` | Atualizar episódio |
| DELETE | `/api/admin/episodes/{id}` | Deletar episódio |
| GET | `/api/admin/links` | Listar todos links |
| POST | `/api/admin/links` | Criar link |
| PUT | `/api/admin/links/{id}` | Atualizar link |
| DELETE | `/api/admin/links/{id}` | Deletar link |

---

## Problemas Conhecidos

### DNS do Docker não funciona durante build

**Problema:** O Docker não consegue resolver DNS durante o build da imagem, causando falha ao executar `apt-get update` e `pip install`.

**Causa:** Configuração `userns-remap` no `/etc/docker/daemon.json` pode causar problemas de rede.

**Solução adotada:** 
- PostgreSQL roda em container Docker
- API roda localmente com ambiente virtual Python

**Solução permanente (requer sudo):**
Adicionar DNS ao daemon.json:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
E reiniciar o Docker:
```bash
sudo systemctl restart docker
```

### Warning bcrypt

**Problema:** Warning ao executar seed.py:
```
(trapped) error reading bcrypt version
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**Impacto:** Nenhum - é apenas um warning de compatibilidade entre versões do bcrypt e passlib. O hash de senha funciona normalmente.

---

## Comandos Úteis

### Docker

```bash
# Ver containers rodando
docker ps

# Ver logs do banco
docker logs metocast_db

# Parar todos containers
docker compose down

# Remover volumes (APAGA DADOS!)
docker compose down -v

# Reiniciar banco
docker compose restart db
```

### Alembic (Migrations)

```bash
# Criar nova migration
.venv/bin/alembic revision --autogenerate -m "descrição"

# Aplicar migrations
.venv/bin/alembic upgrade head

# Reverter última migration
.venv/bin/alembic downgrade -1

# Ver histórico
.venv/bin/alembic history
```

### API

```bash
# Iniciar em modo desenvolvimento
.venv/bin/uvicorn app.main:app --reload --port 8000

# Iniciar em modo produção
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Banco de Dados

```bash
# Conectar ao PostgreSQL
docker exec -it metocast_db psql -U metocast -d metocast_hub

# Listar tabelas
\dt

# Ver estrutura de uma tabela
\d episodes

# Sair
\q
```

---

## Estrutura do Projeto

```
metocast-hub-backend/
├── alembic/                 # Migrations
│   └── versions/            # Arquivos de migration
├── app/
│   ├── api/
│   │   └── v1/              # Rotas da API v1
│   │       ├── auth.py      # Autenticação e JWT
│   │       ├── episodes.py  # Episódios públicos
│   │       ├── links.py     # Links públicos
│   │       ├── admin_episodes.py  # Admin: episódios
│   │       └── admin_links.py     # Admin: links
│   ├── core/                # Configurações e segurança
│   │   ├── config.py        # Settings da aplicação
│   │   └── security.py      # JWT e hash de senhas
│   ├── crud/                # Operações de banco
│   │   ├── episode.py
│   │   ├── link.py
│   │   └── user.py
│   ├── db/                  # Configuração do banco
│   │   └── session.py
│   ├── models/              # Modelos SQLAlchemy
│   │   └── models.py
│   ├── schemas/             # Schemas Pydantic
│   │   └── schemas.py
│   └── main.py              # Aplicação FastAPI
├── docs/                    # Documentação
├── .env                     # Variáveis de ambiente
├── .env.example             # Exemplo de variáveis
├── alembic.ini              # Configuração Alembic
├── docker-compose.yml       # Docker Compose
├── Dockerfile               # Imagem Docker
├── requirements.txt         # Dependências Python
├── seed.py                  # Script de seed
└── README.md                # Documentação principal
```

---

*Documentação gerada em 31/01/2026*
