# 📚 Integração Backend com Disciplinas da Faculdade

## Como usar este backend em cada matéria do semestre

---

## 1️⃣ Introdução a Sistemas de Informação

### O que entregar:

**Documentação do Sistema (5-10 páginas)**

#### 1.1 Visão Geral do Sistema
```
- Contexto: Projeto Metocast precisa centralizar conteúdo
- Problema: Dispersão de informações e baixo alcance
- Solução: Metocast Hub - plataforma centralizada
- Valor gerado: Aumento de alcance e organização
```

#### 1.2 Análise de Stakeholders
```
Stakeholder          | Interesse                | Influência
---------------------|--------------------------|------------
Visitante/Ouvinte    | Acessar episódios        | Alta
Equipe Metocast      | Publicar conteúdo        | Crítica
Coordenação          | Governança e branding    | Alta
Dev/Infra (você)     | Manutenção e evolução    | Crítica
```

#### 1.3 Fluxo de Informação
```
Desenhe diagramas mostrando:
- Como informação entra no sistema (Admin cadastra)
- Como é processada (validação, storage DB)
- Como sai (API → Mobile App → Usuário)
```

#### 1.4 Arquitetura do Sistema
```
Use o código do backend para documentar:
- Camadas (Presentation → Business → Data)
- Tecnologias usadas (FastAPI, PostgreSQL)
- Padrões aplicados (REST, JWT, ORM)
```

**💡 Dica:** Use prints do código e diagramas. Mostre como cada camada funciona.

---

## 2️⃣ Engenharia de Requisitos

### O que entregar:

**Documento de Requisitos Completo**

#### 2.1 Requisitos Funcionais Detalhados

Expanda os RFs da documentação com **critérios de aceite**:

```markdown
RF01 - Listar episódios publicados
Descrição: O sistema deve exibir lista de episódios com status PUBLISHED
Prioridade: ALTA
Critérios de Aceite:
  - CA01: Apenas episódios PUBLISHED são exibidos
  - CA02: Ordenação por data de publicação (mais recente primeiro)
  - CA03: Suporta paginação (skip, limit)
  - CA04: Retorna 200 OK com array JSON
Endpoint implementado: GET /api/episodes
Código: app/api/v1/episodes.py (linha 15)
```

Faça isso para **TODOS os RFs** (mínimo 10 requisitos).

#### 2.2 Requisitos Não-Funcionais Expandidos

```markdown
RNF01 - Segurança
  - Autenticação JWT obrigatória para rotas admin
  - Senha deve ter hash bcrypt
  - Token expira em 30 minutos
  - Implementado em: app/core/security.py

RNF02 - Performance
  - Listagem de episódios < 200ms
  - Suporta 100 requisições/segundo
  - Paginação padrão: 100 registros
```

#### 2.3 Casos de Uso Expandidos

Para cada caso de uso, documente:

**Exemplo: UC03 - Publicar Episódio**

```
Ator Principal: Administrador
Pré-condições: 
  - Admin autenticado
  - Episódio existe no banco
  - Episódio está em DRAFT
  
Fluxo Principal:
  1. Admin seleciona episódio
  2. Admin clica "Publicar"
  3. Sistema valida que episódio existe
  4. Sistema atualiza status para PUBLISHED
  5. Sistema define published_at = now() se não definido
  6. Sistema salva no banco
  7. Sistema retorna episódio atualizado
  
Fluxo Alternativo:
  3a. Episódio não existe
    3a1. Sistema retorna erro 404
  3b. Episódio já publicado
    3b1. Sistema mantém estado atual
    
Pós-condições:
  - Episódio visível na API pública
  - published_at definido
  
Implementação: 
  - Endpoint: PATCH /api/admin/episodes/{id}/publish
  - Código: app/crud/episode.py::publish_episode()
```

#### 2.4 Matriz de Rastreabilidade

| Requisito | Caso de Uso | Endpoint | Arquivo | Teste |
|-----------|-------------|----------|---------|-------|
| RF01 | UC01 | GET /api/episodes | episodes.py | ✓ Manual |
| RF02 | UC02 | GET /api/episodes/{id} | episodes.py | ✓ Manual |
| RF04 | UC04 | POST /api/auth/login | auth.py | ✓ Manual |

**💡 Dica:** Use o código real para preencher esta matriz.

---

## 3️⃣ Interação Humano Computador (IHC)

### O que entregar:

**Análise de Usabilidade + Protótipos**

#### 3.1 Análise de Tarefas

**Tarefa: Publicar um episódio**

```
Objetivo: Admin quer tornar episódio visível ao público
Frequência: 1-2 vezes por semana
Complexidade: Baixa

Passos atuais (via API):
1. Fazer login → POST /auth/login
2. Criar episódio → POST /admin/episodes
3. Publicar → PATCH /admin/episodes/{id}/publish

Análise:
- ✓ Poucos passos
- ✓ Endpoints claros
- ✗ Sem interface visual (precisa de admin web)
- ✗ Sem feedback visual imediato
```

#### 3.2 Personas Expandidas

**Persona 1: Maria (Editora de Conteúdo)**
```
Idade: 24 anos
Formação: Jornalismo
Função: Produtora de conteúdo do Metocast
Tecnologia: Usa computador diariamente, familiarizada com CMSs

Objetivos:
- Publicar episódio rapidamente
- Corrigir erros de digitação após publicar
- Ver quantas pessoas visualizaram

Frustrações:
- APIs sem interface são intimidadoras
- Medo de "quebrar" algo
- Não sabe se episódio foi publicado corretamente

Como o sistema atende:
✓ API estruturada e segura
✓ Validações evitam erros
✗ Falta interface visual amigável (próxima fase!)
```

#### 3.3 Protótipos do Painel Admin (Figma/Papel)

Crie protótipos de:

**Tela 1: Login**
```
┌────────────────────────┐
│   Metocast Hub Admin   │
│                        │
│  Email: [_________]    │
│  Senha: [_________]    │
│                        │
│      [ ENTRAR ]        │
└────────────────────────┘
```

**Tela 2: Lista de Episódios**
```
┌─────────────────────────────────────────┐
│ 🎙️ Metocast Hub     Admin: maria@...   │
├─────────────────────────────────────────┤
│ [+ Novo Episódio]  [Filtros: ▼ Todos]  │
├─────────────────────────────────────────┤
│                                         │
│ ● PUBLICADO  Ep. 10 - IA na Educação   │
│   12/01/2026 | 🎵 Spotify 📺 YouTube   │
│   [Editar] [Despublicar]                │
│                                         │
│ ○ RASCUNHO   Ep. 11 - Metodologia...   │
│   Em edição  | 🎵 ─  📺 ─              │
│   [Editar] [Publicar]                   │
│                                         │
└─────────────────────────────────────────┘
```

#### 3.4 Heurísticas de Nielsen

Avalie o backend atual:

| Heurística | Avaliação | Evidência |
|------------|-----------|-----------|
| 1. Visibilidade do status | ⚠️ Parcial | API retorna status, mas sem UI |
| 2. Correspondência mundo real | ✓ Boa | Termos claros (publish, draft) |
| 3. Controle e liberdade | ✓ Boa | Pode despublicar |
| 4. Consistência | ✓ Excelente | Padrão REST consistente |
| 5. Prevenção de erros | ✓ Boa | Validação Pydantic |

#### 3.5 Teste de Usabilidade

**Recrute 3 pessoas da equipe Metocast:**

Tarefa: "Publique um episódio usando o Swagger UI"

Métricas:
- Tempo para completar
- Número de erros
- Satisfação (escala 1-5)

Documente os resultados!

---

## 4️⃣ Modelagem de Sistemas UML

### O que entregar:

**Diagramas UML do Sistema**

#### 4.1 Diagrama de Casos de Uso

```
        ┌─────────┐
        │Visitante│
        └────┬────┘
             │
    ┌────────┼────────┐
    │        │        │
    v        v        v
(Listar  (Ver     (Acessar
 Episód.) Detalhe) Links)
 
        ┌────────┐
        │ Admin  │
        └────┬───┘
             │
    ┌────────┼─────────────┐
    │        │             │
    v        v             v
(Autenticar) (Gerenciar  (Publicar
              Episódios)  Episódio)
```

Use uma ferramenta como draw.io ou Lucidchart.

#### 4.2 Diagrama de Classes

```python
┌─────────────────────────┐
│       Episode           │
├─────────────────────────┤
│ - id: int               │
│ - title: str            │
│ - description: str      │
│ - status: EpisodeStatus │
│ - published_at: datetime│
│ - spotify_url: str      │
│ - youtube_url: str      │
│ - tags: str             │
├─────────────────────────┤
│ + publish()             │
│ + unpublish()           │
└─────────────────────────┘
         │ 1
         │
         │ *
┌─────────────────────────┐
│    OfficialLink         │
├─────────────────────────┤
│ - id: int               │
│ - label: str            │
│ - url: str              │
│ - type: LinkType        │
│ - order: int            │
└─────────────────────────┘

┌─────────────────────────┐
│     AdminUser           │
├─────────────────────────┤
│ - id: int               │
│ - email: str            │
│ - password_hash: str    │
│ - role: str             │
└─────────────────────────┘
```

**💡 Dica:** Baseie-se em `app/models/models.py`

#### 4.3 Diagrama de Sequência

**Fluxo: Admin publica episódio**

```
Admin    Frontend    API         DB
  │          │        │          │
  │── login ─┤        │          │
  │          │── POST /auth/login─┤
  │          │        │───query──┤
  │          │        │◄──user───┤
  │          │◄── token ──────────┤
  │◄─ token ┤        │          │
  │          │        │          │
  │─ publish ┤        │          │
  │          │── PATCH /episodes/1/publish
  │          │        │───update─┤
  │          │        │◄─episode─┤
  │          │◄── 200 OK ────────┤
  │◄─success─┤        │          │
```

#### 4.4 Diagrama de Estados

**Estados do Episode:**

```
    ┌──────┐
    │DRAFT │
    └───┬──┘
        │
        │ publish()
        v
  ┌──────────┐
  │PUBLISHED │
  └─────┬────┘
        │
        │ unpublish()
        v
    ┌──────┐
    │DRAFT │
    └──────┘
```

#### 4.5 Diagrama de Componentes

```
┌─────────────────────────────────────┐
│         FastAPI Application         │
│  ┌──────────┐  ┌─────────────────┐  │
│  │API Routes│  │Authentication   │  │
│  └────┬─────┘  └────────┬────────┘  │
│       │                 │           │
│  ┌────v─────────────────v────────┐  │
│  │      Business Logic (CRUD)    │  │
│  └────────────┬──────────────────┘  │
│               │                     │
│  ┌────────────v──────────────────┐  │
│  │     Database Layer (ORM)      │  │
│  └────────────┬──────────────────┘  │
└───────────────┼─────────────────────┘
                │
        ┌───────v────────┐
        │   PostgreSQL   │
        └────────────────┘
```

---

## 5️⃣ Eletiva (Exemplo: Gestão de Projetos)

### Como integrar:

#### 5.1 Cronograma Real do Projeto

Documente suas sprints:

```
Sprint 1 (Sem 1-2): Setup e Backend Base
├─ Configurar ambiente Docker
├─ Criar modelos de dados
├─ Implementar API pública
└─ Status: ✓ Concluído

Sprint 2 (Sem 3-4): Admin e Autenticação
├─ Sistema de autenticação JWT
├─ CRUD administrativo
├─ Testes manuais
└─ Status: 🔄 Em andamento
```

#### 5.2 Gestão de Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Servidor homelab cair | Média | Alto | Backup diário, docs de restore |
| Complexidade do Flutter | Alta | Médio | Começar com tutoriais, usar templates |
| Scope creep | Média | Alto | MVP fechado, backlog controlado |

#### 5.3 Métricas de Progresso

```
Total de requisitos: 15
Implementados: 12 (80%)
Testados: 8 (53%)
Documentados: 15 (100%)

Endpoints criados: 16
Modelos de dados: 3
Linhas de código: ~2000
```

---

## 📋 Checklist Geral de Entregas

### Para cada disciplina:

**Introdução a SI:**
- [ ] Documento descrevendo contexto, stakeholders e arquitetura
- [ ] Diagramas de fluxo de informação
- [ ] Análise de valor gerado pelo sistema

**Engenharia de Requisitos:**
- [ ] Lista completa de RF e RNF
- [ ] Casos de uso expandidos (cenários)
- [ ] Matriz de rastreabilidade
- [ ] Validação com stakeholder (professor/coordenação Metocast)

**IHC:**
- [ ] Personas detalhadas
- [ ] Protótipos (baixa/média fidelidade)
- [ ] Análise heurística
- [ ] Relatório de teste de usabilidade

**Modelagem UML:**
- [ ] Diagrama de casos de uso
- [ ] Diagrama de classes
- [ ] 3-4 diagramas de sequência
- [ ] Diagrama de estados
- [ ] Diagrama de componentes

**Eletiva:**
- [ ] Aplicar conceitos específicos ao projeto
- [ ] Documentar aprendizados

---

## 🎯 Próxima Semana

Agora que o backend está pronto:

1. **Testar tudo localmente** (siga o README.md)
2. **Documentar** arquitetura para ISI
3. **Expandir requisitos** para ER
4. **Começar protótipos** para IHC
5. **Criar diagramas UML**

**Tempo estimado:** 10-15 horas para documentação completa de todas as disciplinas.

---

**Dúvidas?** Use o Copilot para te ajudar a gerar documentação! Exemplo:

```python
# Prompt para Copilot:
"""
Crie uma análise de risco para o projeto Metocast Hub
considerando:
- Riscos técnicos (servidor, tecnologias)
- Riscos de prazo
- Riscos de escopo
Para cada risco, defina probabilidade, impacto e mitigação
"""
```
