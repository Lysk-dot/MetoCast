# ⚡ COMANDOS RÁPIDOS - METOCAST HUB

## 🚀 Setup Inicial (primeira vez)

```bash
# 1. Clonar o projeto
git clone <seu-repo>
cd metocast-hub-backend

# 2. Criar arquivo de ambiente
cp .env.example .env

# 3. Editar .env (trocar SECRET_KEY!)
nano .env  # ou vim, code, etc

# 4. Iniciar containers
docker-compose up -d

# 5. Ver logs (Ctrl+C para sair)
docker-compose logs -f api

# 6. Criar tabelas do banco
docker-compose exec api alembic upgrade head

# 7. Popular dados iniciais
docker-compose exec api python seed.py

# 8. Testar no navegador
# Abrir: http://localhost:8000/docs
```

---

## 🔧 Comandos do Dia a Dia

### Docker

```bash
# Iniciar tudo
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f api

# Parar tudo
docker-compose down

# Reiniciar apenas API
docker-compose restart api

# Acessar shell da API
docker-compose exec api bash

# Acessar PostgreSQL
docker-compose exec db psql -U metocast -d metocast_hub
```

### Database

```bash
# Criar nova migration (após alterar models.py)
docker-compose exec api alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrations
docker-compose exec api alembic upgrade head

# Reverter última migration
docker-compose exec api alembic downgrade -1

# Ver histórico de migrations
docker-compose exec api alembic history

# Executar seed novamente
docker-compose exec api python seed.py
```

### Desenvolvimento

```bash
# Rodar sem Docker (desenvolvimento local)
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload

# Instalar nova dependência
pip install nome-pacote
pip freeze > requirements.txt

# Rebuild container após mudança no requirements.txt
docker-compose up -d --build
```

---

## 🧪 Testes Rápidos com cURL

### Login

```bash
# Login (salve o token!)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@metocast.com",
    "password": "admin123"
  }'

# Resposta:
# {"access_token": "eyJhbG...", "token_type": "bearer"}
```

### Episódios (público)

```bash
# Listar episódios publicados
curl http://localhost:8000/api/episodes

# Ver detalhe de episódio
curl http://localhost:8000/api/episodes/1

# Listar links oficiais
curl http://localhost:8000/api/links
```

### Admin (precisa token)

```bash
# Substituir TOKEN_AQUI pelo seu token!

# Listar todos episódios (incluindo rascunhos)
curl -H "Authorization: Bearer TOKEN_AQUI" \
  http://localhost:8000/api/admin/episodes

# Criar episódio
curl -X POST http://localhost:8000/api/admin/episodes \
  -H "Authorization: Bearer TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Novo Episódio",
    "description": "Descrição aqui",
    "spotify_url": "https://spotify.com/...",
    "tags": "ciência,tech"
  }'

# Publicar episódio ID 2
curl -X PATCH http://localhost:8000/api/admin/episodes/2/publish \
  -H "Authorization: Bearer TOKEN_AQUI"

# Despublicar episódio ID 2
curl -X PATCH http://localhost:8000/api/admin/episodes/2/unpublish \
  -H "Authorization: Bearer TOKEN_AQUI"

# Deletar episódio ID 3
curl -X DELETE http://localhost:8000/api/admin/episodes/3 \
  -H "Authorization: Bearer TOKEN_AQUI"
```

---

## 🗄️ Comandos SQL Úteis

```bash
# Acessar PostgreSQL
docker-compose exec db psql -U metocast -d metocast_hub
```

```sql
-- Ver todas as tabelas
\dt

-- Ver estrutura da tabela episodes
\d episodes

-- Contar episódios
SELECT COUNT(*) FROM episodes;

-- Ver episódios publicados
SELECT id, title, status FROM episodes WHERE status = 'PUBLISHED';

-- Ver último episódio
SELECT * FROM episodes ORDER BY created_at DESC LIMIT 1;

-- Resetar senha do admin (hash de 'novaSenha123')
UPDATE admin_users 
SET password_hash = '$2b$12$...' 
WHERE email = 'admin@metocast.com';

-- Sair do psql
\q
```

---

## 🔍 Debugging

### Ver logs específicos

```bash
# Logs da API
docker-compose logs api

# Logs do banco
docker-compose logs db

# Últimas 50 linhas
docker-compose logs --tail=50 api

# Seguir logs em tempo real
docker-compose logs -f api
```

### Verificar se tá rodando

```bash
# Ver containers ativos
docker-compose ps

# Testar endpoint de health
curl http://localhost:8000/health

# Ver uso de recursos
docker stats
```

### Problemas comuns

```bash
# Erro "port already in use"
# Mudar porta no docker-compose.yml: "8001:8000"

# Banco não conecta
docker-compose down
docker-compose up -d db
# Aguardar 10 segundos
docker-compose up -d api

# Reset completo (CUIDADO: apaga dados!)
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head
docker-compose exec api python seed.py
```

---

## 🎨 Formatação e Linting (opcional)

```bash
# Instalar ferramentas
pip install black isort flake8

# Formatar código
black app/

# Organizar imports
isort app/

# Verificar style
flake8 app/
```

---

## 📦 Backup e Restore

### Backup do banco

```bash
# Fazer backup
docker-compose exec db pg_dump -U metocast metocast_hub > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T db psql -U metocast metocast_hub < backup_20260131.sql
```

### Backup do projeto

```bash
# Backup completo (sem node_modules, venv, etc)
tar -czf metocast-backup-$(date +%Y%m%d).tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='venv' \
  metocast-hub-backend/
```

---

## 🚀 Deploy (quando for para produção)

```bash
# 1. Atualizar .env com valores de produção
# - Trocar SECRET_KEY
# - Trocar senhas do banco
# - DEBUG=False

# 2. Build para produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 3. Aplicar migrations
docker-compose exec api alembic upgrade head

# 4. Criar admin
docker-compose exec api python seed.py
```

---

## 📊 Monitoramento

```bash
# Ver uso de recursos
docker stats

# Ver espaço em disco
df -h

# Ver logs de erro
docker-compose logs api | grep ERROR

# Ver requisições (se tiver log customizado)
docker-compose logs api | grep "GET\|POST\|PUT\|DELETE"
```

---

## 🎯 Atalhos VSCode + Copilot

```
Ctrl+I          - Abrir chat Copilot
Ctrl+Shift+I    - Copilot inline
Tab             - Aceitar sugestão
Alt+]           - Próxima sugestão
Alt+[           - Sugestão anterior
Ctrl+Enter      - Ver mais sugestões

# Comandos no chat:
/explain        - Explicar código
/fix            - Corrigir bugs
/tests          - Gerar testes
```

---

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Port 8000 ocupado | Mudar para 8001 no docker-compose.yml |
| Banco não conecta | `docker-compose restart db` |
| Migration falha | `alembic downgrade -1` e tentar novamente |
| 401 Unauthorized | Token expirado, fazer login novamente |
| CORS error | Adicionar origem no .env ALLOWED_ORIGINS |
| Import error | Verificar __init__.py em todas as pastas |

---

## 📝 Workflow Típico

```bash
# 1. Atualizar código do Git
git pull

# 2. Reiniciar se necessário
docker-compose restart api

# 3. Fazer mudança no código
# ... editar arquivos ...

# 4. Se mudou models.py:
docker-compose exec api alembic revision --autogenerate -m "Mudança X"
docker-compose exec api alembic upgrade head

# 5. Testar no Swagger
# Abrir http://localhost:8000/docs

# 6. Commit
git add .
git commit -m "Adicionado feature X"
git push
```

---

## 🎉 One-liners Úteis

```bash
# Ver quantos episódios publicados
docker-compose exec db psql -U metocast metocast_hub -c "SELECT COUNT(*) FROM episodes WHERE status='PUBLISHED';"

# Criar backup rápido
docker-compose exec db pg_dump -U metocast metocast_hub > backup.sql

# Ver último episódio criado
docker-compose exec db psql -U metocast metocast_hub -c "SELECT title, created_at FROM episodes ORDER BY created_at DESC LIMIT 1;"

# Resetar senha admin para 'admin123'
docker-compose exec api python -c "from app.core.security import get_password_hash; print(get_password_hash('admin123'))"
```

---

## 📚 Links Úteis

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Alembic Docs:** https://alembic.sqlalchemy.org/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

---

**💡 Dica:** Salve este arquivo como favorito! Você vai usar muito.

**Última atualização:** 31/01/2026
