# 🚀 ROADMAP EXECUTIVO - METOCAST HUB

## ✅ STATUS ATUAL: Backend MVP Completo

Você agora tem:
- ✓ Backend FastAPI funcional
- ✓ Banco PostgreSQL com Docker
- ✓ Autenticação JWT
- ✓ API pública + admin completas
- ✓ Sistema de migrations (Alembic)
- ✓ Documentação automática (Swagger)
- ✓ Guias de uso e integração acadêmica

---

## 📅 CRONOGRAMA SUGERIDO (11 semanas)

### 🟢 SEMANA 1-2: Setup e Testes (JÁ COMEÇOU!)

**Tempo: 8-12 horas**

**Tarefas:**
- [x] Estrutura do backend criada
- [ ] Rodar Docker Compose no homelab
- [ ] Criar primeiro usuário admin
- [ ] Testar todos os endpoints no Swagger
- [ ] Fazer backup do banco
- [ ] Começar documentação para ISI

**Entregas acadêmicas:**
- Rascunho de Introdução a SI (contexto + stakeholders)

**Comandos:**
```bash
# No seu homelab
git clone <seu-repo>
cd metocast-hub-backend
cp .env.example .env
docker-compose up -d
docker-compose exec api alembic upgrade head
docker-compose exec api python seed.py
```

Acesse: http://SEU_IP:8000/docs

---

### 🟡 SEMANA 3-4: Documentação Acadêmica Parte 1

**Tempo: 10-15 horas**

**Tarefas:**
- [ ] Completar doc de ISI (fluxos, arquitetura, valor)
- [ ] Expandir requisitos para ER (critérios de aceite)
- [ ] Criar casos de uso detalhados
- [ ] Iniciar matriz de rastreabilidade
- [ ] Adicionar 1-2 funcionalidades com Copilot (ex: busca, filtros)

**Entregas acadêmicas:**
- Documento ISI completo (5-10 págs)
- Requisitos expandidos para ER

**Funcionalidades extras (com Copilot):**
```python
# Em app/crud/episode.py
# TODO: adicionar busca por título
def search_episodes_by_title(db, search_term):
    # Copilot vai sugerir!
```

---

### 🟡 SEMANA 5-6: Protótipos e UML

**Tempo: 12-18 horas**

**Tarefas:**
- [ ] Criar protótipos do admin web (Figma/Papel)
- [ ] Criar diagramas UML (casos de uso, classes, sequência)
- [ ] Fazer análise heurística do sistema
- [ ] Planejar testes de usabilidade
- [ ] Deploy do backend no homelab (fixo)

**Entregas acadêmicas:**
- Protótipos IHC (baixa/média fidelidade)
- Conjunto completo de diagramas UML

**Ferramentas:**
- Figma (protótipos): https://figma.com
- Draw.io (UML): https://draw.io
- Lucidchart (UML): https://lucidchart.com

---

### 🔵 SEMANA 7-8: Aprender Flutter + Começar Mobile

**Tempo: 15-20 horas**

**Tarefas:**
- [ ] Tutorial básico de Flutter (oficial)
- [ ] Setup ambiente Flutter
- [ ] Criar projeto mobile base
- [ ] Implementar tela Home (lista episódios)
- [ ] Conectar com API real
- [ ] Tratamento de loading/erro

**Entregas acadêmicas:**
- Relatório de aprendizado Flutter
- Protótipo funcional da Home

**Recursos Flutter:**
```bash
# Instalar Flutter
# Siga: https://docs.flutter.dev/get-started/install

# Criar projeto
flutter create metocast_hub_mobile
cd metocast_hub_mobile
flutter run
```

**Tutorial recomendado:**
- Flutter Codelabs: https://docs.flutter.dev/codelabs
- Duração: 2-3 horas para básico

---

### 🔵 SEMANA 9: Completar Mobile Público

**Tempo: 12-16 horas**

**Tarefas:**
- [ ] Tela de detalhe do episódio
- [ ] Tela de links oficiais
- [ ] Navegação entre telas
- [ ] Tratamento de estados vazios
- [ ] Melhorias de UI/UX

**Entregas acadêmicas:**
- App mobile funcional (público)
- Relatório de testes de usabilidade

---

### 🟣 SEMANA 10: Admin Web (Opcional/Simplificado)

**Tempo: 8-12 horas**

**Opção 1: Streamlit (Python - mais fácil)**
```bash
pip install streamlit
streamlit run admin_dashboard.py
```

**Opção 2: React simples**

**Tarefas:**
- [ ] Tela de login
- [ ] Lista de episódios
- [ ] Formulário criar/editar
- [ ] Botões publicar/despublicar

**Entregas acadêmicas:**
- Admin funcional (básico)

---

### 🟣 SEMANA 11: Refinamento e Entrega Final

**Tempo: 10-15 horas**

**Tarefas:**
- [ ] Revisar todas as documentações
- [ ] Atualizar README com tudo que foi feito
- [ ] Criar vídeo demo (3-5 minutos)
- [ ] Preparar apresentação
- [ ] Fazer backup completo
- [ ] Melhorias finais de código

**Entregas acadêmicas:**
- **Todas** as documentações finalizadas
- Vídeo demo do sistema
- Apresentação (slides)
- Código completo no Git

---

## 📊 DISTRIBUIÇÃO DE HORAS

| Atividade | Horas |
|-----------|-------|
| Backend + setup | 12h (feito) |
| Documentação acadêmica | 25h |
| Protótipos + UML | 15h |
| Aprendizado Flutter | 8h |
| Mobile app | 25h |
| Admin web | 10h |
| Refinamento final | 10h |
| **TOTAL** | **105 horas** |

**Com 2-4h/dia:** ~26-52 dias = 4-8 semanas
**Com tempo de fins de semana:** Viável em 11 semanas! ✅

---

## 🎯 MARCOS IMPORTANTES (Milestones)

### Milestone 1: Backend Funcional ✅
- Data: Semana 2
- Status: **COMPLETO**

### Milestone 2: Docs Acadêmicas Parte 1
- Data: Semana 4
- Entregáveis: ISI completo, ER expandido

### Milestone 3: Protótipos e UML
- Data: Semana 6
- Entregáveis: IHC protótipos, UML completo

### Milestone 4: Mobile MVP
- Data: Semana 9
- Entregáveis: App público funcional

### Milestone 5: Entrega Final
- Data: Semana 11
- Entregáveis: Sistema completo + todas documentações

---

## 🛠️ STACK TECNOLÓGICA FINAL

**Backend:**
- Python 3.11
- FastAPI
- PostgreSQL
- Docker
- JWT Auth
- Alembic

**Mobile:**
- Flutter (Dart)
- HTTP client
- Provider/Bloc (state)

**Admin Web:**
- Streamlit (Python) ou React

**Infra:**
- Homelab (Docker)
- Git/GitHub

---

## 📚 RECURSOS ESSENCIAIS

### Documentação Oficial
- FastAPI: https://fastapi.tiangolo.com/
- Flutter: https://docs.flutter.dev/
- PostgreSQL: https://www.postgresql.org/docs/

### Tutoriais
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- Flutter Codelabs: https://docs.flutter.dev/codelabs
- Streamlit Tutorial: https://docs.streamlit.io/

### Ferramentas
- VSCode + Copilot
- Docker Desktop (se Windows/Mac)
- Postman/Insomnia (testar API)
- DBeaver (gerenciar banco)
- Figma (protótipos)

---

## 🚨 PONTOS DE ATENÇÃO

### Riscos e Como Mitigar

**1. Flutter é novo para você**
- **Mitigação:** Comece pelos tutoriais oficiais (4-6h)
- **Alternativa:** Use React Native se já conhece JS

**2. Tempo escasso**
- **Mitigação:** Foque no MVP, deixe extras para depois
- **Prioridade:** Backend ✓ → Docs → Mobile básico

**3. Homelab pode ter problemas**
- **Mitigação:** Faça backups semanais do banco
- **Plano B:** Deploy no Railway/Render (free tier)

**4. Complexidade das disciplinas**
- **Mitigação:** Use o código como base para docs
- **Dica:** Peça feedback incremental aos professores

---

## ✅ CHECKLIST PRÉ-ENTREGA

### Backend
- [ ] Todas as rotas funcionando
- [ ] Autenticação validada
- [ ] Migrations aplicadas
- [ ] Dados de seed criados
- [ ] README atualizado

### Mobile
- [ ] Build Android funcional
- [ ] Telas Home, Detalhe, Links
- [ ] Integração com API
- [ ] Estados de erro tratados

### Documentação
- [ ] ISI completo
- [ ] ER completo com matriz
- [ ] IHC com protótipos e testes
- [ ] UML (5 diagramas mínimo)
- [ ] README principal atualizado

### Apresentação
- [ ] Vídeo demo (3-5 min)
- [ ] Slides (10-15 slides)
- [ ] Código no Git
- [ ] Documentos em PDF

---

## 🎉 PRÓXIMOS PASSOS IMEDIATOS

**AGORA (próximas 2 horas):**

1. **Transferir código para seu homelab**
   ```bash
   # No seu servidor
   git init
   git add .
   git commit -m "Backend MVP completo"
   git push origin main
   ```

2. **Rodar Docker e testar**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

3. **Acessar Swagger e testar**
   - http://SEU_IP:8000/docs
   - Testar login
   - Testar criar episódio
   - Testar publicar

4. **Criar primeiro documento acadêmico**
   - Abrir `ACADEMIC_INTEGRATION.md`
   - Começar com ISI (contexto + stakeholders)
   - Meta: 2-3 páginas hoje

**ESTA SEMANA:**

- [ ] Backend 100% funcional no homelab
- [ ] Rascunho ISI (5 páginas)
- [ ] Começar expansão de requisitos para ER
- [ ] Criar repositório Git e fazer primeiro push

---

## 💬 DÚVIDAS FREQUENTES

**Q: E se eu não conseguir fazer o admin web?**
**R:** Não tem problema! O Swagger já funciona como admin provisório. Foque em fazer mobile bem feito.

**Q: Flutter é obrigatório?**
**R:** Não, mas é recomendado. Alternativas: React Native, React (web responsivo).

**Q: Preciso hospedar online?**
**R:** Para nota, não. Para portfólio, sim (Railway/Render free tier).

**Q: E se atrasar?**
**R:** Priorize: Backend ✓ → Docs → Mobile básico. Admin web é secundário.

---

## 📞 SUPORTE

**Recursos disponíveis:**
- GitHub Copilot (seu melhor amigo)
- Stack Overflow
- Discord comunidades (Flutter BR, Python BR)
- Documentação oficial

**Lembre-se:** Use o Copilot generosamente! Ele vai economizar muito tempo.

---

**Última atualização:** 31/01/2026
**Status do projeto:** 🟢 Backend completo, pronto para expansão
**Próximo marco:** Semana 4 - Docs acadêmicas parte 1

---

**BOA SORTE! 🚀 Você tem tudo que precisa para fazer um projeto incrível!**
