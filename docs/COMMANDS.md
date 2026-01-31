# Comandos Executados - Histórico de Setup

Este documento registra todos os comandos executados durante a configuração do projeto em 31/01/2026.

---

## 1. Verificação Inicial do Repositório

```bash
# Verificar status do git
git status
# Resultado: On branch main, up to date with 'origin/main', working tree clean

# Verificar repositório remoto
git remote -v
# Resultado: origin https://github.com/Lysk-dot/MetoCast.git
```

---

## 2. Descompactar Projeto

```bash
# Descompactar arquivo do projeto
tar -xzf metocast-hub-backend.tar.gz

# Verificar conteúdo
ls -la
```

---

## 3. Verificação do Docker

```bash
# Verificar se Docker está instalado
which docker
# Resultado: /usr/bin/docker

# Verificar docker-compose (antigo)
which docker-compose
# Resultado: não encontrado

# Verificar Docker Compose (plugin)
docker compose version
# Resultado: Docker Compose version v5.0.2
```

---

## 4. Tentativas de Build Docker (Falharam)

### Tentativa 1 - Build padrão
```bash
docker compose up -d
# Resultado: ERRO - DNS failure resolving 'deb.debian.org'
```

### Tentativa 2 - Build sem cache
```bash
docker compose build --no-cache
# Resultado: ERRO - Mesmo problema de DNS
```

### Tentativa 3 - Build com network=host
```bash
docker build --network=host -t metocast-api .
# Resultado: ERRO - permission denied mounting sysfs
```

### Tentativa 4 - Build com add-host
```bash
docker build --add-host=pypi.org:151.101.0.223 --add-host=files.pythonhosted.org:151.101.0.223 -t metocast-api-build .
# Resultado: ERRO - Connection timeout
```

---

## 5. Diagnóstico de Rede

```bash
# Testar conectividade do host
ping -c 2 8.8.8.8
# Resultado: OK - 2 packets transmitted, 2 received

# Verificar configuração DNS do sistema
cat /etc/resolv.conf
# Resultado: nameserver 127.0.0.53 (systemd-resolved)

# Verificar configuração do Docker daemon
cat /etc/docker/daemon.json
# Resultado: contém "userns-remap": "default" (causa provável do problema)
```

---

## 6. Alterações no Dockerfile

```bash
# Modificação: Removida instalação de pacotes do sistema
# Arquivo: Dockerfile
# Linhas removidas:
#   RUN apt-get update && apt-get install -y \
#       gcc \
#       postgresql-client \
#       && rm -rf /var/lib/apt/lists/*
```

---

## 7. Alterações no docker-compose.yml

```bash
# Adicionado DNS ao serviço api
# Arquivo: docker-compose.yml
# Linhas adicionadas:
#     dns:
#       - 8.8.8.8
#       - 8.8.4.4
```

---

## 8. Subir Apenas o PostgreSQL

```bash
# Subir apenas o container do banco
docker compose up -d db

# Resultado:
# ✔ Network metocast_metocast_network Created
# ✔ Volume metocast_postgres_data Created
# ✔ Container metocast_db Created

# Verificar status
docker ps
# CONTAINER ID   IMAGE                STATUS    PORTS                    NAMES
# 3220cf593509   postgres:15-alpine   Up        0.0.0.0:5432->5432/tcp   metocast_db
```

---

## 9. Configurar Ambiente Python Local

```bash
# Verificar versão do Python
python3 --version
# Resultado: Python 3.12.3

# Tentativa de criar venv (falhou - falta python3-venv)
python3 -m venv venv
# Resultado: ERRO - ensurepip not available

# Configurar ambiente via VS Code/Copilot
# Criado: .venv com Python 3.12.3
```

---

## 10. Instalar Dependências Python

```bash
# Pacotes instalados via install_python_packages:
# - fastapi==0.109.0
# - uvicorn[standard]==0.27.0
# - python-multipart==0.0.6
# - sqlalchemy==2.0.25
# - alembic==1.13.1
# - psycopg2-binary==2.9.9
# - python-jose[cryptography]==3.3.0
# - passlib[bcrypt]==1.7.4
# - bcrypt==4.1.2
# - python-dotenv==1.0.0
# - pydantic==2.5.3
# - pydantic-settings==2.1.0
# - email-validator==2.1.0.post1
```

---

## 11. Alteração do .env

```bash
# Alterada URL do banco para acesso local
# Arquivo: .env
# Antes:  DATABASE_URL=postgresql://metocast:metocast123@db:5432/metocast_hub
# Depois: DATABASE_URL=postgresql://metocast:metocast123@localhost:5432/metocast_hub
```

---

## 12. Configurar Banco de Dados

```bash
# Criar migration inicial
/home/felipe/MetoCast/MetoCast/.venv/bin/alembic revision --autogenerate -m "Initial migration"

# Resultado:
# INFO - Detected added table 'admin_users'
# INFO - Detected added table 'episodes'
# INFO - Detected added table 'official_links'
# Generating alembic/versions/2ad7d10a79d6_initial_migration.py ... done

# Aplicar migrations
/home/felipe/MetoCast/MetoCast/.venv/bin/alembic upgrade head

# Resultado:
# INFO - Running upgrade -> 2ad7d10a79d6, Initial migration
```

---

## 13. Popular Banco com Dados Iniciais

```bash
/home/felipe/MetoCast/MetoCast/.venv/bin/python seed.py

# Resultado:
# ✓ Admin criado: admin@metocast.com / senha: admin123
# ✓ Link criado: Spotify
# ✓ Link criado: YouTube
# ✓ Link criado: Instagram
# ✓ Episódio criado: Episódio 1 - Introdução ao Metocast
# ✓ Episódio criado: Episódio 2 - Metodologia Científica
# ✅ Seed concluído com sucesso!
```

---

## 14. Iniciar API

```bash
/home/felipe/MetoCast/MetoCast/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Resultado:
# INFO:     Started server process
# INFO:     Waiting for application startup.
# 🚀 Metocast Hub API v1.0.0 iniciado!
# 📚 Documentação: http://localhost:8000/docs
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Resumo de Comandos para Reproduzir o Setup

```bash
# 1. Clonar e entrar no diretório
git clone https://github.com/Lysk-dot/MetoCast.git
cd MetoCast

# 2. Subir PostgreSQL
docker compose up -d db

# 3. Ativar ambiente virtual (já existe)
source .venv/bin/activate

# 4. Aplicar migrations
alembic upgrade head

# 5. Popular banco
python seed.py

# 6. Iniciar API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

*Documentação gerada em 31/01/2026*
