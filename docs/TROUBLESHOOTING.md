# Troubleshooting - Metocast Hub API

Guia para resolução de problemas comuns.

---

## 🐳 Problemas com Docker

### DNS não funciona durante build

**Sintoma:**
```
Temporary failure resolving 'deb.debian.org'
E: Unable to locate package gcc
```

**Causa:** O Docker não consegue resolver DNS durante o build. Geralmente causado por configuração `userns-remap` no daemon.json.

**Soluções:**

1. **Adicionar DNS ao daemon.json (requer sudo):**
```bash
sudo nano /etc/docker/daemon.json
```
Adicionar:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
Reiniciar Docker:
```bash
sudo systemctl restart docker
```

2. **Usar network=host no build:**
```bash
docker build --network=host -t metocast-api .
```

3. **Solução adotada:** Rodar API localmente e apenas PostgreSQL no Docker.

---

### Container não inicia

**Sintoma:**
```
Container metocast_api exited with code 1
```

**Diagnóstico:**
```bash
# Ver logs
docker logs metocast_api

# Ver logs em tempo real
docker logs -f metocast_api
```

**Causas comuns:**
- Porta já em uso
- Banco de dados não está pronto
- Variáveis de ambiente faltando

---

### Porta já em uso

**Sintoma:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use
```

**Solução:**
```bash
# Encontrar processo usando a porta
sudo lsof -i :5432

# Matar processo
sudo kill -9 <PID>

# Ou mudar a porta no docker-compose.yml
ports:
  - "5433:5432"  # Usar porta externa diferente
```

---

## 🐍 Problemas com Python

### Módulo não encontrado

**Sintoma:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução:**
```bash
# Verificar se está no ambiente virtual correto
which python

# Ativar ambiente virtual
source .venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

---

### Erro de versão do Python

**Sintoma:**
```
SyntaxError: invalid syntax
```

**Verificar versão:**
```bash
python --version
# Precisa ser 3.11+
```

---

### Warning do bcrypt

**Sintoma:**
```
(trapped) error reading bcrypt version
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**Impacto:** Nenhum - é apenas warning de compatibilidade.

**Solução (opcional):**
```bash
pip install bcrypt==4.0.1
```

---

## 🗄️ Problemas com Banco de Dados

### Não consegue conectar ao PostgreSQL

**Sintoma:**
```
psycopg2.OperationalError: could not connect to server
```

**Diagnóstico:**
```bash
# Verificar se container está rodando
docker ps | grep metocast_db

# Verificar logs do PostgreSQL
docker logs metocast_db

# Testar conexão
docker exec -it metocast_db psql -U metocast -d metocast_hub -c "SELECT 1"
```

**Causas comuns:**

1. **Container não está rodando:**
```bash
docker compose up -d db
```

2. **URL errada no .env:**
```env
# Para Docker:
DATABASE_URL=postgresql://metocast:metocast123@db:5432/metocast_hub

# Para local:
DATABASE_URL=postgresql://metocast:metocast123@localhost:5432/metocast_hub
```

3. **Credenciais erradas** - verificar docker-compose.yml

---

### Migration falha

**Sintoma:**
```
alembic.util.exc.CommandError: Target database is not up to date
```

**Solução:**
```bash
# Ver estado atual
alembic current

# Ver histórico
alembic history

# Aplicar todas migrations
alembic upgrade head

# Se necessário, resetar (APAGA DADOS!)
alembic downgrade base
alembic upgrade head
```

---

### Tabela não existe

**Sintoma:**
```
sqlalchemy.exc.ProgrammingError: relation "episodes" does not exist
```

**Solução:**
```bash
# Aplicar migrations
alembic upgrade head
```

---

## 🔐 Problemas de Autenticação

### Token inválido

**Sintoma:**
```json
{"detail": "Could not validate credentials"}
```

**Causas:**
1. Token expirado (padrão: 30 min)
2. SECRET_KEY diferente no .env
3. Token mal formatado

**Solução:**
```bash
# Fazer login novamente
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@metocast.com", "password": "admin123"}'
```

---

### Senha incorreta

**Sintoma:**
```json
{"detail": "Email ou senha incorretos"}
```

**Solução:**
```bash
# Resetar senha via seed (CUIDADO: cria novo admin)
python seed.py

# Ou acessar banco diretamente e deletar usuário
docker exec -it metocast_db psql -U metocast -d metocast_hub
DELETE FROM admin_users WHERE email = 'admin@metocast.com';
\q

python seed.py
```

---

## 🌐 Problemas de Rede

### CORS bloqueando requisições

**Sintoma:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solução:**
Adicionar origem no .env:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://seu-dominio.com
```

---

### API não acessível externamente

**Sintoma:** Funciona em localhost mas não pelo IP

**Soluções:**

1. **Verificar se está escutando em 0.0.0.0:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Verificar firewall:**
```bash
sudo ufw status
sudo ufw allow 8000
```

3. **Verificar se a porta está aberta:**
```bash
netstat -tlnp | grep 8000
```

---

## 📝 Logs e Debug

### Ativar modo debug

No .env:
```env
DEBUG=True
```

### Ver logs do SQLAlchemy

```python
# Em app/db/session.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Mostra todas as queries SQL
)
```

### Ver logs do Uvicorn

```bash
uvicorn app.main:app --log-level debug
```

---

## 🔧 Reset Completo

Se nada funcionar, reset completo:

```bash
# 1. Parar tudo
docker compose down -v

# 2. Remover ambiente virtual
rm -rf .venv

# 3. Recriar ambiente
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Subir banco
docker compose up -d db

# 5. Aguardar banco iniciar
sleep 5

# 6. Aplicar migrations
alembic upgrade head

# 7. Popular dados
python seed.py

# 8. Iniciar API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📞 Ainda com Problemas?

1. Verifique os logs detalhados
2. Consulte a documentação oficial:
   - [FastAPI](https://fastapi.tiangolo.com/)
   - [SQLAlchemy](https://docs.sqlalchemy.org/)
   - [Alembic](https://alembic.sqlalchemy.org/)
   - [Docker](https://docs.docker.com/)

---

*Documentação gerada em 31/01/2026*
