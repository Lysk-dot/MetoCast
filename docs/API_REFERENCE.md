# API Reference - Metocast Hub

Documentação completa de todos os endpoints da API.

**Base URL:** `http://localhost:8000`

---

## 📑 Índice

1. [Autenticação](#autenticação)
2. [Episódios (Público)](#episódios-público)
3. [Links (Público)](#links-público)
4. [Admin - Episódios](#admin---episódios)
5. [Admin - Links](#admin---links)
6. [Schemas](#schemas)

---

## Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação. Para acessar endpoints administrativos, inclua o token no header:

```
Authorization: Bearer <token>
```

### POST /api/auth/login

Realiza login e retorna o token JWT.

**Request Body:**
```json
{
  "email": "admin@metocast.com",
  "password": "admin123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response 401:**
```json
{
  "detail": "Email ou senha incorretos"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@metocast.com", "password": "admin123"}'
```

---

### POST /api/auth/register

Registra um novo usuário administrador.

**Request Body:**
```json
{
  "name": "Novo Admin",
  "email": "novo@metocast.com",
  "password": "senha123"
}
```

**Response 201:**
```json
{
  "id": 2,
  "name": "Novo Admin",
  "email": "novo@metocast.com",
  "role": "ADMIN",
  "is_active": true,
  "created_at": "2026-01-31T15:00:00"
}
```

---

## Episódios (Público)

Endpoints públicos para listar episódios publicados.

### GET /api/episodes

Lista todos os episódios publicados.

**Query Parameters:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| skip | int | Pular N registros (default: 0) |
| limit | int | Limitar resultados (default: 100) |

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Episódio 1 - Introdução ao Metocast",
    "description": "Neste primeiro episódio apresentamos o projeto...",
    "published_at": null,
    "status": "PUBLISHED",
    "cover_image_url": null,
    "spotify_url": "https://open.spotify.com/episode/exemplo1",
    "youtube_url": "https://youtube.com/watch?v=exemplo1",
    "tags": "introdução,primeiro,lançamento",
    "created_at": "2026-01-31T15:00:53"
  }
]
```

**cURL Example:**
```bash
curl http://localhost:8000/api/episodes
```

---

### GET /api/episodes/{id}

Obtém um episódio específico por ID.

**Path Parameters:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | int | ID do episódio |

**Response 200:**
```json
{
  "id": 1,
  "title": "Episódio 1 - Introdução ao Metocast",
  "description": "Neste primeiro episódio apresentamos o projeto...",
  "published_at": null,
  "status": "PUBLISHED",
  "cover_image_url": null,
  "spotify_url": "https://open.spotify.com/episode/exemplo1",
  "youtube_url": "https://youtube.com/watch?v=exemplo1",
  "tags": "introdução,primeiro,lançamento",
  "created_at": "2026-01-31T15:00:53"
}
```

**Response 404:**
```json
{
  "detail": "Episódio não encontrado"
}
```

---

## Links (Público)

Endpoints públicos para listar links oficiais.

### GET /api/links

Lista todos os links oficiais ordenados.

**Response 200:**
```json
[
  {
    "id": 1,
    "label": "Spotify",
    "url": "https://open.spotify.com/show/metocast",
    "type": "SPOTIFY",
    "order": 1,
    "created_at": "2026-01-31T15:00:53"
  },
  {
    "id": 2,
    "label": "YouTube",
    "url": "https://youtube.com/@metocast",
    "type": "YOUTUBE",
    "order": 2,
    "created_at": "2026-01-31T15:00:53"
  },
  {
    "id": 3,
    "label": "Instagram",
    "url": "https://instagram.com/metocast",
    "type": "INSTAGRAM",
    "order": 3,
    "created_at": "2026-01-31T15:00:53"
  }
]
```

**cURL Example:**
```bash
curl http://localhost:8000/api/links
```

---

## Admin - Episódios

🔒 **Requer autenticação JWT**

### GET /api/admin/episodes

Lista todos os episódios (incluindo drafts).

**Headers:**
```
Authorization: Bearer <token>
```

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Episódio 1 - Introdução ao Metocast",
    "status": "PUBLISHED",
    ...
  },
  {
    "id": 2,
    "title": "Episódio 2 - Metodologia Científica",
    "status": "DRAFT",
    ...
  }
]
```

---

### POST /api/admin/episodes

Cria um novo episódio.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Episódio 3 - Novo Tema",
  "description": "Descrição do episódio...",
  "status": "DRAFT",
  "spotify_url": "https://open.spotify.com/episode/xxx",
  "youtube_url": "https://youtube.com/watch?v=xxx",
  "tags": "tag1,tag2"
}
```

**Response 201:**
```json
{
  "id": 3,
  "title": "Episódio 3 - Novo Tema",
  "description": "Descrição do episódio...",
  "published_at": null,
  "status": "DRAFT",
  "cover_image_url": null,
  "spotify_url": "https://open.spotify.com/episode/xxx",
  "youtube_url": "https://youtube.com/watch?v=xxx",
  "tags": "tag1,tag2",
  "created_at": "2026-01-31T16:00:00"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/admin/episodes \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Episódio 3 - Novo Tema",
    "description": "Descrição do episódio...",
    "status": "DRAFT"
  }'
```

---

### PUT /api/admin/episodes/{id}

Atualiza um episódio existente.

**Path Parameters:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | int | ID do episódio |

**Request Body:**
```json
{
  "title": "Título Atualizado",
  "status": "PUBLISHED"
}
```

**Response 200:**
```json
{
  "id": 1,
  "title": "Título Atualizado",
  "status": "PUBLISHED",
  ...
}
```

---

### DELETE /api/admin/episodes/{id}

Deleta um episódio.

**Response 204:** No content

**Response 404:**
```json
{
  "detail": "Episódio não encontrado"
}
```

---

## Admin - Links

🔒 **Requer autenticação JWT**

### GET /api/admin/links

Lista todos os links oficiais.

---

### POST /api/admin/links

Cria um novo link.

**Request Body:**
```json
{
  "label": "Twitter",
  "url": "https://twitter.com/metocast",
  "type": "TWITTER",
  "order": 4
}
```

---

### PUT /api/admin/links/{id}

Atualiza um link existente.

---

### DELETE /api/admin/links/{id}

Deleta um link.

---

## Schemas

### Episode Status

```typescript
enum EpisodeStatus {
  DRAFT = "DRAFT"
  PUBLISHED = "PUBLISHED"
  ARCHIVED = "ARCHIVED"
}
```

### Link Type

```typescript
enum LinkType {
  SPOTIFY = "SPOTIFY"
  YOUTUBE = "YOUTUBE"
  INSTAGRAM = "INSTAGRAM"
  TWITTER = "TWITTER"
  WEBSITE = "WEBSITE"
  OTHER = "OTHER"
}
```

### Episode Schema

```typescript
interface Episode {
  id: number
  title: string
  description: string | null
  published_at: datetime | null
  status: EpisodeStatus
  cover_image_url: string | null
  spotify_url: string | null
  youtube_url: string | null
  tags: string | null  // comma-separated
  created_at: datetime
  updated_at: datetime | null
}
```

### OfficialLink Schema

```typescript
interface OfficialLink {
  id: number
  label: string
  url: string
  type: LinkType
  order: number
  created_at: datetime
  updated_at: datetime | null
}
```

### AdminUser Schema

```typescript
interface AdminUser {
  id: number
  name: string
  email: string
  role: "ADMIN" | "EDITOR"
  is_active: boolean
  created_at: datetime
  updated_at: datetime | null
}
```

---

## Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 204 | Deletado com sucesso |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Não encontrado |
| 422 | Erro de validação |
| 500 | Erro interno do servidor |

---

## Testando a API

### Via Swagger UI

Acesse: http://localhost:8000/docs

1. Clique em "Authorize" 🔓
2. Faça login em `/api/auth/login`
3. Cole o token no formato: `Bearer <token>`
4. Teste os endpoints

### Via cURL

```bash
# 1. Fazer login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@metocast.com", "password": "admin123"}' \
  | jq -r '.access_token')

# 2. Usar o token
curl http://localhost:8000/api/admin/episodes \
  -H "Authorization: Bearer $TOKEN"
```

---

*Documentação gerada em 31/01/2026*
