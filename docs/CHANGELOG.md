# Changelog - Metocast Hub API

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [1.0.0] - 2026-01-31

### 🚀 Setup Inicial

#### Adicionado
- Configuração inicial do ambiente de desenvolvimento
- Ambiente virtual Python (.venv) com Python 3.12.3
- Container Docker para PostgreSQL 15-alpine
- Migrations do Alembic configuradas e aplicadas
- Seed inicial com dados de exemplo

#### Configurado
- Arquivo `.env` com variáveis de ambiente
- Conexão com banco de dados local (localhost:5432)
- CORS para desenvolvimento local
- Autenticação JWT

#### Dados Iniciais Criados
- **Admin:** admin@metocast.com / admin123
- **Links oficiais:**
  - Spotify
  - YouTube
  - Instagram
- **Episódios:**
  - Episódio 1 - Introdução ao Metocast (PUBLISHED)
  - Episódio 2 - Metodologia Científica (DRAFT)

### 🔧 Alterações Técnicas

#### Dockerfile
- Removida instalação de `gcc` e `postgresql-client` devido a problemas de DNS do Docker

**Antes:**
```dockerfile
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
```

**Depois:**
```dockerfile
# Removido - API roda localmente
```

#### docker-compose.yml
- Adicionada configuração de DNS para o serviço `api`:
```yaml
dns:
  - 8.8.8.8
  - 8.8.4.4
```

#### .env
- Alterada URL do banco de `db` para `localhost`:
```env
# Antes
DATABASE_URL=postgresql://metocast:metocast123@db:5432/metocast_hub

# Depois
DATABASE_URL=postgresql://metocast:metocast123@localhost:5432/metocast_hub
```

### 📦 Dependências Instaladas

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.1.0.post1
```

### 🐛 Problemas Encontrados

1. **DNS Docker não funciona durante build**
   - Causa: Configuração `userns-remap` no daemon.json
   - Solução: API roda localmente, apenas PostgreSQL no Docker

2. **Warning bcrypt**
   - Warning de compatibilidade passlib/bcrypt
   - Impacto: Nenhum - funciona normalmente

### 📝 Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `alembic/versions/2ad7d10a79d6_initial_migration.py` | Migration inicial |
| `docs/SETUP_GUIDE.md` | Guia completo de setup |
| `docs/CHANGELOG.md` | Este arquivo |
| `docs/COMMANDS.md` | Comandos executados |
| `docs/API_REFERENCE.md` | Referência da API |

---

## Versões Futuras

### [1.1.0] - Planejado
- [ ] Resolver problema de DNS do Docker
- [ ] Implementar upload de imagens de capa
- [ ] Adicionar paginação nos endpoints
- [ ] Testes automatizados

### [1.2.0] - Planejado
- [ ] Cache com Redis
- [ ] Rate limiting
- [ ] Logs estruturados

---

*Última atualização: 31/01/2026*
