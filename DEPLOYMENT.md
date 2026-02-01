# 📝 Documentação de Deploy - MetoCast

## Data: 01/02/2026

---

## 🚀 Deploy Backend (Railway)

### 1. Configuração do Procfile
**Arquivo:** `Procfile`

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: alembic upgrade head
```

- Configura execução automática de migrações no deploy
- Inicia servidor Uvicorn na porta dinâmica do Railway

---

### 2. Correção de Configuração do Banco de Dados

**Arquivo:** `app/core/config.py`

**Problema:** Railway fornece `DATABASE_PUBLIC_URL` em vez de `DATABASE_URL`

**Solução:**
```python
@model_validator(mode='after')
def set_database_url(self):
    if not self.DATABASE_URL and self.DATABASE_PUBLIC_URL:
        self.DATABASE_URL = self.DATABASE_PUBLIC_URL
    return self
```

---

### 3. Correção de Conexão SSL PostgreSQL

**Arquivo:** `app/db/session.py`

**Problema:** Railway PostgreSQL requer SSL

**Solução:**
```python
connect_args = {}
if settings.DATABASE_URL and 'railway' in settings.DATABASE_URL.lower():
    connect_args = {"sslmode": "require"}
```

---

### 4. Migrações e Seed

**Comandos executados no Railway via terminal:**

```bash
# Conectar ao PostgreSQL Railway
export DATABASE_URL="postgresql://postgres:XuarRAEFtvpHnQCXQuCCUUIlpjZczYkf@shuttle.proxy.rlwy.net:21819/railway"

# Executar migrações
alembic upgrade head

# Popular banco com dados iniciais
python seed.py
```

**Resultado:**
- ✅ Tabelas criadas: `users`, `episodes`, `links`
- ✅ Admin criado: `admin@metocast.com` / `admin123`
- ✅ 3 episódios de exemplo criados

---

### 5. Correção de CORS

**Arquivo:** `app/main.py`

**Problema:** Frontend GitHub Pages bloqueado por CORS

**Solução:**
```python
allow_origins=[
    "http://localhost:5173",
    "https://lysk-dot.github.io"
]
```

---

## 🌐 Deploy Frontend (GitHub Pages)

### 1. Correção de Roteamento SPA

**Arquivo:** `src/App.jsx`

**Problema:** GitHub Pages não suporta rotas client-side com BrowserRouter

**Solução:** Mudança para HashRouter
```jsx
import { HashRouter } from 'react-router-dom';

<HashRouter>
  <Routes>...</Routes>
</HashRouter>
```

**URLs resultantes:**
- Home: `/#/`
- Login: `/#/login`
- Admin: `/#/admin`

---

### 2. Correção de Autenticação

#### 2.1. Endpoint de Verificação
**Arquivo:** `src/services/api.js`

**Problema:** Endpoint `/auth/verify` não existe na API

**Solução:** Mudança para `/auth/me`

#### 2.2. Fluxo de Autenticação
**Arquivo:** `src/services/auth.js`

**Problema:** `verifyToken` fazia logout automático em qualquer erro

**Solução:**
```javascript
verifyToken: async () => {
  try {
    const response = await api.verifyToken();
    localStorage.setItem('metocast_user', JSON.stringify(response.data));
    return true;
  } catch (error) {
    console.error('Token inválido:', error);
    return false; // Não faz logout
  }
}
```

#### 2.3. Interceptor de Erros
**Arquivo:** `src/services/api.js`

**Problema:** Interceptor redirecionava para login em qualquer 401

**Solução:** Removido redirecionamento automático, apenas log de erro

---

### 3. Correção de Formulários

#### 3.1. Schema de Episódios
**Arquivo:** `src/components/Admin/EpisodeForm.jsx`

**Problemas:**
- Campo `thumbnail_url` → deveria ser `cover_image_url`
- Status em lowercase → deveria ser uppercase

**Soluções:**
```javascript
cover_image_url: formData.cover_image_url || null,
status: formData.status || 'DRAFT', // Uppercase
```

#### 3.2. Parsing de Tags
**Arquivos:** `EpisodeManager.jsx`, `EpisodeCard.jsx`

**Problema:** API retorna tags como string, frontend esperava array

**Solução:**
```javascript
const getTags = (tags) => {
  if (!tags) return [];
  if (typeof tags === 'string') return tags.split(',').map(t => t.trim());
  return tags;
};
```

---

### 4. Correção Crítica: URLs Hardcoded

**Arquivo:** `src/pages/AdminPanel.jsx`

**Problema:** Todas as chamadas `fetch` tinham `localhost:8000` hardcoded

**Solução:** Substituição global para Railway
```bash
sed -i "s|http://localhost:8000/api|https://metocast-production.up.railway.app/api|g" AdminPanel.jsx
```

**Chamadas corrigidas:**
- `/api/admin/episodes` (GET, POST, PUT, DELETE)
- `/api/admin/links` (GET, POST, PUT, DELETE)

---

### 5. Detecção de Ambiente

**Arquivo:** `src/services/api.js`

**Problema:** `import.meta.env.PROD` não funcionava corretamente

**Solução:** Detecção via hostname
```javascript
const isProduction = window.location.hostname.includes('github.io');

const API_BASE = isProduction
  ? 'https://metocast-production.up.railway.app/api'
  : 'http://localhost:8000/api';
```

---

## 📦 Processo de Deploy

### Backend (Railway)
1. Push para GitHub
2. Railway detecta mudanças automaticamente
3. Executa `release: alembic upgrade head`
4. Inicia aplicação com `web: uvicorn...`

### Frontend (GitHub Pages)
```bash
cd /home/felipe/MetoCast-Web
npm run build
npx gh-pages -d dist -f
```

**Cache busting:** GitHub Pages CDN pode demorar 1-3 minutos para atualizar

---

## 🔐 Credenciais

### Admin
- **Email:** `admin@metocast.com`
- **Senha:** `admin123`

### Banco de Dados (Railway)
- **URL:** `postgresql://postgres:XuarRAEFtvpHnQCXQuCCUUIlpjZczYkf@shuttle.proxy.rlwy.net:21819/railway`

---

## 🌍 URLs de Acesso

### Backend
- **API:** https://metocast-production.up.railway.app/api
- **Docs:** https://metocast-production.up.railway.app/docs
- **Redoc:** https://metocast-production.up.railway.app/redoc

### Frontend
- **Site:** https://lysk-dot.github.io/MetoCast-Web/
- **Login:** https://lysk-dot.github.io/MetoCast-Web/#/login
- **Admin:** https://lysk-dot.github.io/MetoCast-Web/#/admin

---

## ✅ Funcionalidades Implementadas

### Público
- [x] Listagem de episódios publicados
- [x] Visualização de detalhes do episódio
- [x] Links para Spotify/YouTube
- [x] Links sociais
- [x] Parsing correto de tags

### Admin
- [x] Login com JWT
- [x] Persistência de sessão
- [x] CRUD completo de episódios
- [x] Publicar/despublicar episódios
- [x] Upload de capa (URL)
- [x] Gerenciamento de links
- [x] Busca de episódios

---

## 🐛 Problemas Resolvidos

1. ✅ DATABASE_URL não configurada → `DATABASE_PUBLIC_URL` como fallback
2. ✅ Erro SSL PostgreSQL → `sslmode: require`
3. ✅ CORS bloqueado → Adicionado GitHub Pages
4. ✅ Tags causando erro → Conversão string→array
5. ✅ 404 em rotas → HashRouter
6. ✅ Logout automático → Removido de `verifyToken`
7. ✅ Endpoint inexistente → `/auth/verify` → `/auth/me`
8. ✅ URLs localhost → Mudança para Railway
9. ✅ `import.meta.env.PROD` → Detecção por hostname
10. ✅ Cache CDN GitHub → Force push com `-f`

---

## 📊 Estrutura do Banco

### Tabela: users
- id (PK)
- email (unique)
- hashed_password
- is_active
- created_at

### Tabela: episodes
- id (PK)
- title
- description
- cover_image_url
- spotify_url
- youtube_url
- tags (string CSV)
- status (DRAFT/PUBLISHED)
- published_at
- created_at
- updated_at

### Tabela: links
- id (PK)
- title
- url
- icon
- order
- is_active
- created_at

---

## 🔄 Workflow de Atualização

### Adicionar Episódio
1. Login no admin
2. Clicar "+ Novo Episódio"
3. Preencher:
   - Título
   - Descrição
   - URL da capa (Spotify image CDN)
   - URL Spotify/YouTube
   - Tags (separadas por vírgula)
   - Status: DRAFT ou PUBLISHED
4. Salvar

### Extrair Dados do Spotify
```bash
# Via fetch_webpage tool
fetch_webpage("https://open.spotify.com/episode/ID")
```

**Estrutura da imagem Spotify:**
```
https://image-cdn-ak.spotifycdn.com/image/ab6772ab000015be[HASH]
```

---

## 📝 Notas Importantes

1. **Cache:** GitHub Pages CDN pode demorar para atualizar
   - Solução: Janela anônima ou Ctrl+Shift+R

2. **CORS:** Sempre adicionar novos domínios em `app/main.py`

3. **SSL:** Railway PostgreSQL sempre requer SSL

4. **Tags:** API aceita string CSV, frontend converte para array

5. **Status:** Backend aceita apenas `DRAFT` ou `PUBLISHED` (uppercase)

6. **HashRouter:** Todas as rotas com `#/` para compatibilidade com GitHub Pages

---

## 🛠️ Comandos Úteis

### Desenvolvimento Local
```bash
# Backend
cd /home/felipe/MetoCast
source .venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd /home/felipe/MetoCast-Web
npm run dev
```

### Deploy
```bash
# Backend: git push (auto-deploy no Railway)
cd /home/felipe/MetoCast
git add -A
git commit -m "Update"
git push

# Frontend
cd /home/felipe/MetoCast-Web
npm run build
npx gh-pages -d dist -f
```

### Migrations
```bash
# Criar migration
alembic revision --autogenerate -m "Description"

# Aplicar
alembic upgrade head

# Reverter
alembic downgrade -1
```

---

## 🎯 Próximos Passos (Sugestões)

1. [ ] Implementar upload real de imagens (S3/Cloudinary)
2. [ ] Adicionar paginação de episódios
3. [ ] Sistema de categorias além de tags
4. [ ] Analytics de visualizações
5. [ ] RSS feed para podcatchers
6. [ ] Preview de episódios antes de publicar
7. [ ] Edição em massa de episódios
8. [ ] Logs de ações do admin
9. [ ] Recuperação de senha
10. [ ] Multi-admin com níveis de permissão

---

**Documentação gerada em:** 01/02/2026  
**Status:** ✅ Sistema em produção e funcional
