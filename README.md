# Metocast Hub - Backend API

API REST para gerenciamento de episódios e links oficiais do projeto Metocast.

## 🚀 Tecnologias

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Migrations de banco
- **JWT** - Autenticação via tokens
- **Docker** - Containerização

## 📁 Estrutura do Projeto

```
metocast-hub-backend/
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
├── alembic/                 # Migrations
├── docker-compose.yml       # Docker Compose
├── Dockerfile              # Imagem Docker
├── requirements.txt        # Dependências Python
├── seed.py                 # Script de seed
└── .env.example            # Exemplo de variáveis de ambiente
```

## 🔧 Setup Inicial

### 1. Clonar e preparar ambiente

```bash
# Clonar o repositório
git clone <seu-repo>
cd metocast

# Criar arquivo .env (copiar do exemplo)
cp .env.example .env
```

### 2. Editar .env

Abra o arquivo `.env` e ajuste as variáveis conforme necessário:

```env
DATABASE_URL=postgresql://metocast:metocast123@db:5432/metocast_hub
SECRET_KEY=MUDE-ESTA-CHAVE-EM-PRODUCAO
```

### 3. Iniciar com Docker

```bash
# Iniciar containers (banco + API)
docker-compose up -d

# Ver logs
docker-compose logs -f api
```

### 4. Criar tabelas do banco (migrations)

```bash
# Criar migration inicial
docker-compose exec api alembic revision --autogenerate -m "Initial migration"

# Aplicar migrations
docker-compose exec api alembic upgrade head
```

### 5. Popular banco com dados iniciais

```bash
docker-compose exec api python seed.py
```

Isso criará:
- ✓ Usuário admin (admin@metocast.com / admin123)
- ✓ Links oficiais de exemplo
- ✓ Episódios de exemplo

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@metocast.com",
    "password": "admin123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Usar token nas requisições protegidas

```bash
curl -X GET http://localhost:8000/api/admin/episodes \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📡 Endpoints da API

### Públicos (sem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Health check |
| POST | `/api/auth/login` | Login e geração de token |
| GET | `/api/episodes` | Lista episódios publicados |
| GET | `/api/episodes/{id}` | Detalhe de episódio |
| GET | `/api/links` | Lista links oficiais |

### Administrativos (requer token)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/admin/episodes` | Lista todos episódios |
| POST | `/api/admin/episodes` | Criar episódio |
| GET | `/api/admin/episodes/{id}` | Detalhe (inclui rascunhos) |
| PUT | `/api/admin/episodes/{id}` | Atualizar episódio |
| DELETE | `/api/admin/episodes/{id}` | Deletar episódio |
| PATCH | `/api/admin/episodes/{id}/publish` | Publicar episódio |
| PATCH | `/api/admin/episodes/{id}/unpublish` | Despublicar episódio |
| GET | `/api/admin/links` | Lista links |
| POST | `/api/admin/links` | Criar link |
| PUT | `/api/admin/links/{id}` | Atualizar link |
| DELETE | `/api/admin/links/{id}` | Deletar link |

## 🧪 Testando a API

### Criar episódio

```bash
curl -X POST http://localhost:8000/api/admin/episodes \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Novo Episódio",
    "description": "Descrição do episódio",
    "spotify_url": "https://spotify.com/...",
    "youtube_url": "https://youtube.com/...",
    "tags": "ciência,tecnologia"
  }'
```

### Publicar episódio

```bash
curl -X PATCH http://localhost:8000/api/admin/episodes/1/publish \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Listar episódios publicados (público)

```bash
curl http://localhost:8000/api/episodes
```

## 🔄 Migrations (Alembic)

```bash
# Criar nova migration
docker-compose exec api alembic revision --autogenerate -m "Descrição"

# Aplicar migrations
docker-compose exec api alembic upgrade head

# Reverter última migration
docker-compose exec api alembic downgrade -1

# Ver histórico
docker-compose exec api alembic history
```

## 🛠️ Comandos Úteis

```bash
# Ver logs da API
docker-compose logs -f api

# Reiniciar API
docker-compose restart api

# Acessar shell do container
docker-compose exec api bash

# Acessar PostgreSQL
docker-compose exec db psql -U metocast -d metocast_hub

# Parar tudo
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose down -v
```

## 🐛 Debug e Desenvolvimento

### Rodar sem Docker (desenvolvimento local)

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor (hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Próximos Passos

- [ ] Adicionar testes automatizados (pytest)
- [ ] Implementar cache (Redis)
- [ ] Adicionar rate limiting
- [ ] Logs estruturados
- [ ] Monitoramento (Prometheus/Grafana)
- [ ] CI/CD pipeline

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
2. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
3. Push para a branch (`git push origin feature/nova-feature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto é parte do programa de extensão universitária Metocast.

---

**Desenvolvido com ❤️ para o projeto Metocast**
# Test
