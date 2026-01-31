# 🤖 Guia: Expandindo o Backend com GitHub Copilot

Este guia te ensina como usar o Copilot para adicionar novas funcionalidades ao backend do Metocast Hub.

## 📋 Pré-requisitos

- VSCode instalado
- GitHub Copilot ativo
- Backend já funcionando (seguiu o README.md)

---

## 🎯 Como o Copilot vai te ajudar

O Copilot é **seu par de programação**. Ele:
- ✓ Sugere código baseado em comentários
- ✓ Completa funções automaticamente
- ✓ Gera código repetitivo (CRUD, validações)
- ✓ Ajuda com sintaxe que você não lembra

---

## 🚀 Exemplos Práticos

### Exemplo 1: Adicionar campo "duration" aos episódios

**Passo 1: Atualizar o modelo**

Abra `app/models/models.py` e adicione um comentário:

```python
class Episode(Base):
    # ... campos existentes ...
    
    # TODO: adicionar campo duration (duração em minutos)
```

O Copilot vai sugerir algo como:

```python
duration = Column(Integer, nullable=True)  # duração em minutos
```

**Passo 2: Atualizar o schema**

Abra `app/schemas/schemas.py` e adicione:

```python
class EpisodeBase(BaseModel):
    # ... campos existentes ...
    
    # TODO: adicionar duration ao schema
```

Copilot sugere:

```python
duration: Optional[int] = None
```

**Passo 3: Criar migration**

```bash
docker-compose exec api alembic revision --autogenerate -m "Add duration to episodes"
docker-compose exec api alembic upgrade head
```

---

### Exemplo 2: Adicionar filtro de busca por título

**Abra `app/crud/episode.py` e adicione:**

```python
# TODO: criar função para buscar episódios por título
# Deve aceitar search_term e retornar lista de episódios que contêm o termo no título
def search_episodes_by_title(db: Session, search_term: str) -> List[Episode]:
```

Copilot vai sugerir a implementação completa!

**Depois, adicione a rota em `app/api/v1/episodes.py`:**

```python
# TODO: adicionar endpoint GET /episodes/search?q=termo
# Deve usar a função search_episodes_by_title
```

---

### Exemplo 3: Adicionar estatísticas de episódios

**Crie novo arquivo `app/api/v1/stats.py`:**

```python
"""
Rotas de estatísticas.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/stats", tags=["stats"])

# TODO: criar endpoint que retorna:
# - total de episódios publicados
# - total de episódios em rascunho
# - último episódio publicado
# - média de episódios por mês
```

Copilot vai gerar o código! Depois registre a rota em `main.py`.

---

## 💡 Dicas para usar o Copilot efetivamente

### 1. Escreva comentários claros

❌ Ruim:
```python
# fazer coisa
```

✅ Bom:
```python
# TODO: criar função que retorna episódios dos últimos 7 dias
# Deve receber db session e retornar lista de Episode ordenada por data
```

### 2. Use nomes descritivos

```python
# Copilot entende melhor quando você usa nomes claros
def get_recent_episodes_last_week(db: Session):
    # Copilot vai sugerir a query certa!
```

### 3. Aceite e modifique

- Use `Tab` para aceitar sugestão
- Use `Alt+]` para próxima sugestão
- Use `Alt+[` para sugestão anterior
- **Sempre revise o código sugerido!**

### 4. Use o padrão existente

Copilot aprende com seu código. Se você já tem funções CRUD, ele vai sugerir código similar para novas entidades.

---

## 🎓 Exercícios para Praticar

### Exercício 1: Sistema de Tags

**Objetivo:** Criar tabela separada para tags (ao invés de string)

**Passos:**
1. Criar modelo `Tag` em `models.py`
2. Criar relacionamento many-to-many com `Episode`
3. Criar CRUD para tags
4. Atualizar rotas para aceitar lista de tags

**Prompt para Copilot:**
```python
# TODO: criar modelo Tag com relacionamento many-to-many com Episode
# Tag deve ter: id, name, slug
# Episode deve ter lista de tags
```

---

### Exercício 2: Upload de Imagem de Capa

**Objetivo:** Permitir upload real de imagens (ao invés de URL)

**Passos:**
1. Criar pasta `uploads/` para armazenar imagens
2. Criar endpoint POST `/api/admin/episodes/{id}/cover`
3. Validar tipo de arquivo (apenas imagens)
4. Salvar arquivo e atualizar `cover_image_url`

**Prompt para Copilot:**
```python
# TODO: criar endpoint para upload de imagem de capa
# Deve aceitar multipart/form-data
# Validar extensão (jpg, png, webp)
# Salvar em uploads/ com nome único
# Retornar URL da imagem
```

---

### Exercício 3: Paginação Avançada

**Objetivo:** Melhorar paginação com metadados

**Prompts:**
```python
# TODO: criar schema PaginatedResponse com:
# - items: lista de episódios
# - total: total de registros
# - page: página atual
# - per_page: itens por página
# - total_pages: total de páginas
```

---

## 🐛 Debugging com Copilot

**Se algo não funciona:**

1. Adicione comentário explicando o erro:
```python
# ERRO: esta query retorna None mas deveria retornar Episode
# Verificar se o filtro está correto
```

2. Copilot pode sugerir correção!

---

## 📚 Recursos Adicionais

### Documentação FastAPI
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)

### Comandos úteis do Copilot

- `Ctrl+I` (VSCode): Abrir chat do Copilot
- `Ctrl+Shift+I`: Copilot inline chat
- `/explain`: Pedir explicação de código
- `/fix`: Pedir correção de bugs
- `/tests`: Gerar testes automaticamente

---

## ✅ Checklist: Adicionando Nova Feature

Antes de criar uma nova funcionalidade, siga este checklist:

- [ ] **1. Modelo** - Adicionar campos necessários em `models.py`
- [ ] **2. Schema** - Criar/atualizar schemas em `schemas.py`
- [ ] **3. CRUD** - Criar operações de banco em `crud/`
- [ ] **4. Rotas** - Adicionar endpoints em `api/v1/`
- [ ] **5. Migration** - Criar e aplicar migration do Alembic
- [ ] **6. Testar** - Testar no Swagger UI (`/docs`)
- [ ] **7. Documentar** - Atualizar README se necessário

---

## 🎯 Projeto Prático: Sistema de Comentários

Vamos criar um sistema completo de comentários nos episódios usando Copilot!

### Fase 1: Modelo de Dados

**Abra `app/models/models.py` e adicione:**

```python
# TODO: criar modelo Comment para comentários em episódios
# Campos:
# - id (int, primary key)
# - episode_id (foreign key para Episode)
# - author_name (string, máx 100 chars)
# - content (text)
# - created_at (datetime, automático)
# - is_approved (boolean, default False)
# Relacionamento: Episode deve ter lista de comments
```

### Fase 2: Schemas

**Abra `app/schemas/schemas.py`:**

```python
# TODO: criar schemas para Comment:
# - CommentBase: author_name, content
# - CommentCreate: herda Base
# - CommentInDB: adiciona id, episode_id, created_at, is_approved
# - CommentResponse: alias para InDB
```

### Fase 3: CRUD

**Crie `app/crud/comment.py`:**

```python
# TODO: criar funções CRUD para comments:
# - get_comment(db, comment_id) -> retorna Comment ou None
# - get_comments_by_episode(db, episode_id, approved_only=True) -> lista Comment
# - create_comment(db, episode_id, comment_data) -> cria e retorna Comment
# - approve_comment(db, comment_id) -> marca is_approved=True
# - delete_comment(db, comment_id) -> deleta Comment
```

### Fase 4: Rotas Públicas

**Crie `app/api/v1/comments.py`:**

```python
# TODO: criar rotas públicas de comentários:
# GET /api/episodes/{episode_id}/comments - lista aprovados
# POST /api/episodes/{episode_id}/comments - criar comentário
```

### Fase 5: Rotas Admin

**Crie `app/api/v1/admin_comments.py`:**

```python
# TODO: criar rotas admin de comentários (requer autenticação):
# GET /api/admin/comments - lista todos
# PATCH /api/admin/comments/{id}/approve - aprovar
# DELETE /api/admin/comments/{id} - deletar
```

### Fase 6: Registrar Rotas

**Em `app/main.py`:**

```python
# TODO: importar e registrar rotas de comentários
# Rotas públicas em /api
# Rotas admin em /api/admin
```

### Fase 7: Migration

```bash
docker-compose exec api alembic revision --autogenerate -m "Add comments table"
docker-compose exec api alembic upgrade head
```

### Fase 8: Testar

Acesse http://localhost:8000/docs e teste!

---

## 🎉 Parabéns!

Você agora sabe como:
- ✓ Usar Copilot para expandir o backend
- ✓ Adicionar novas funcionalidades
- ✓ Criar CRUDs completos
- ✓ Trabalhar com relacionamentos

**Próximo passo:** Explore as funcionalidades mais avançadas e adapte o sistema às necessidades do Metocast!

---

**Dúvidas?** Experimente perguntar ao Copilot Chat! Digite `Ctrl+I` e faça sua pergunta sobre o código.
