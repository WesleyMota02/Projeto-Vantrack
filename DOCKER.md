# 🐳 VANTRACK - GUIA COMPLETO DE DOCKER COMPOSE

> **Containerização do MySQL para ambiente de desenvolvimento padronizado**

---

## 📋 O que é Docker Compose?

Docker Compose é uma ferramenta que permite definir e executar múltiplos containers Docker usando um arquivo `YAML`. No nosso caso, estamos usando para:

✅ Isolar o MySQL em um container  
✅ Padronizar o ambiente em todas as máquinas  
✅ Eliminar conflitos com MySQL instalado localmente  
✅ Persistir dados automaticamente  
✅ Auto-inicializar o banco com nosso schema  

---

## 🚀 Quick Start

### Pré-requisitos

- **Docker Desktop** instalado (Windows/Mac) ou **Docker + Docker Compose** (Linux)
  - Download: https://www.docker.com/products/docker-desktop
  - Linux: `sudo apt-get install docker.io docker-compose`

### Comandos Essenciais

```bash
# 1️⃣ INICIAR BANCO DE DADOS
docker-compose up -d

# 2️⃣ VERIFICAR SE ESTÁ RODANDO
docker ps

# 3️⃣ VER LOGS
docker-compose logs -f db

# 4️⃣ CONECTAR AO MYSQL
mysql -h localhost -u root -proot

# 5️⃣ PARAR BANCO
docker-compose down

# 6️⃣ PARAR E APAGAR DADOS
docker-compose down -v
```

---

## 📁 Estrutura de Diretórios

```
Projeto-vantrack/
├── docker/
│   └── mysql/
│       ├── data/                      # 🔒 Dados do MySQL (IGNORADO no Git)
│       │   ├── .gitkeep              # Mantém estrutura vazia no Git
│       │   └── ...                   # (Preenchido em runtime)
│       └── .gitkeep                  # (Mantém pasta vazia no Git)
│
├── database/
│   └── schema.sql                     # 📄 Schema SQL (executado na 1ª inicialização)
│
├── backend/
│   ├── app.py
│   └── database.py
│
├── docker-compose.yml                 # ⚙️ Configuração do Docker
├── .gitignore                         # 🔒 Ignora docker/mysql/data/
└── README.md
```

---

## 🔧 Configuração Detalhada

### docker-compose.yml

```yaml
version: '3.8'                          # Versão do Docker Compose API

services:
  db:                                   # Nome do serviço
    image: mysql:8.0                   # Imagem MySQL versão 8.0
    container_name: vantrack_mysql     # Nome do container
    
    environment:                        # Variáveis de ambiente
      MYSQL_ROOT_PASSWORD: root         # Senha do root
      MYSQL_DATABASE: vantrack          # Banco criado automaticamente
      MYSQL_INITDB_ARGS: "--character-set-server=utf8mb4"
    
    ports:
      - "3306:3306"                    # Porta: <local>:<container>
    
    volumes:
      # Persistência: dados não são perdidos ao parar o container
      - ./docker/mysql/data:/var/lib/mysql
      
      # Auto-inicialização: schema.sql executado 1ª vez
      - ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    
    healthcheck:                        # Verificação de saúde
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    
    restart: unless-stopped             # Reinicia automaticamente
```

---

## 📊 Fluxo de Inicialização

```
1️⃣ docker-compose up -d
   ↓
2️⃣ Docker baixa imagem mysql:8.0
   ↓
3️⃣ Container é criado (vantrack_mysql)
   ↓
4️⃣ MySQL inicializa
   ↓
5️⃣ schema.sql é executado automaticamente
   ↓
6️⃣ 10 tabelas são criadas
   ↓
7️⃣ Dados são salvos em ./docker/mysql/data/
   ↓
✅ BANCO PRONTO PARA USAR!
```

---

## 💾 Volumes Explicados

### Volume 1: Persistência de Dados

```yaml
volumes:
  - ./docker/mysql/data:/var/lib/mysql
```

**O que faz?**  
- Mapeia pasta local `./docker/mysql/data/` para `/var/lib/mysql` do container
- Todos os dados SQL são salvos na máquina local
- Quando você para o container, os dados permanecem

**Benefício:**  
```
Sem volume:
  docker-compose down  →  Dados perdidos ❌

Com volume:
  docker-compose down  →  Dados salvos em ./docker/mysql/data/ ✅
  docker-compose up    →  Dados são restaurados automaticamente
```

### Volume 2: Auto-Inicialização

```yaml
volumes:
  - ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
```

**O que faz?**  
- `/docker-entrypoint-initdb.d/` é a pasta especial do MySQL
- Qualquer `.sql` nessa pasta é executado na **PRIMEIRA inicialização**
- Nosso `schema.sql` cria as 10 tabelas automaticamente

**Fluxo:**
```
1ª INICIALIZAÇÃO:
  docker-compose up -d  →  MySQL roda schema.sql  →  10 tabelas criadas ✅

REINICIALIZAÇÕES:
  docker-compose up -d  →  Dados já existem  →  Schema ignorado (seguro!) ✅
```

---

## 🔐 Segurança e Credenciais

### Configuração Padrão (DESENVOLVIMENTO)

```
Hostname: localhost
Porta: 3306
Usuário: root
Senha: root
Database: vantrack
```

### Para Produção

Modifique `docker-compose.yml`:

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}  # Use variáveis de ambiente
  MYSQL_DATABASE: ${MYSQL_DATABASE}
  MYSQL_USER: ${MYSQL_USER}
  MYSQL_PASSWORD: ${MYSQL_PASSWORD}
```

E crie um arquivo `.env.docker`:

```
MYSQL_ROOT_PASSWORD=senha_forte_aqui
MYSQL_DATABASE=vantrack
MYSQL_USER=vantrack_user
MYSQL_PASSWORD=senha_forte_usuario
```

Execute com:
```bash
docker-compose --env-file .env.docker up -d
```

---

## 🧪 Testando a Conexão

### Terminal 1: Verificar Container

```bash
# Ver containers rodando
docker ps

# Ver logs
docker-compose logs -f db

# Inspecionar container
docker inspect vantrack_mysql
```

### Terminal 2: Conectar via MySQL CLI

```bash
# Conectar ao banco
mysql -h localhost -u root -proot

# Usar o banco
USE vantrack;

# Ver tabelas
SHOW TABLES;

# Contar usuários
SELECT COUNT(*) FROM usuarios;

# Sair
EXIT;
```

### Terminal 3: Testar via Python

```bash
# Ativar venv
.venv\Scripts\activate

# Rodar testes
cd backend
python test_complete_flow.py

# Deve retornar: ✅ All tests passed!
```

---

## 🛠️ Troubleshooting

### Problema: "Connection refused on port 3306"

**Causa:** Container não iniciou ou porta já está em uso

**Solução:**
```bash
# Verificar containers
docker ps -a

# Ver logs
docker-compose logs db

# Se porta está em uso, libere ou mude em docker-compose.yml
# Mudar para porta 3307:
ports:
  - "3307:3306"
```

### Problema: "Dados desapareceram após docker-compose down"

**Causa:** Volume não foi mapeado corretamente

**Verificar:**
```bash
# Checar volumes
docker inspect vantrack_mysql

# Deve ter:
# "Mounts": [
#   {"Source": "/caminho/local/docker/mysql/data", "Destination": "/var/lib/mysql"}
# ]

# Se não estiver, execute:
docker-compose down -v
docker-compose up -d  # Recria com volumes corretos
```

### Problema: "Permission denied" no docker/mysql/data/

**Causa:** Permissões incorretas (Linux)

**Solução:**
```bash
# Dar permissões à pasta
chmod 755 docker/mysql/data
sudo chown $(whoami):$(whoami) docker/mysql/data
```

### Problema: "Cannot connect: No such file or directory"

**Causa:** Docker não está rodando

**Solução:**
```bash
# Windows/Mac: Abra Docker Desktop
# Linux: Inicie o daemon
sudo systemctl start docker

# Verifique status
docker ps
```

---

## 📊 Monitoramento

### Ver Status em Tempo Real

```bash
# Logs contínuos
docker-compose logs -f db

# Stats do container
docker stats vantrack_mysql

# Inspecionar container
docker inspect vantrack_mysql
```

### Backup de Dados

```bash
# Fazer dump do banco
docker exec vantrack_mysql mysqldump -u root -proot vantrack > backup.sql

# Restaurar dump
docker exec -i vantrack_mysql mysql -u root -proot vantrack < backup.sql
```

---

## 🔄 Ciclo de Vida Completo

### 1️⃣ Primeiro Uso

```bash
docker-compose up -d
# → Cria tudo do zero
# → Executa schema.sql
# → 10 tabelas criadas
```

### 2️⃣ Desenvolvimento Normal

```bash
# Banco já está rodando
# Desenvolva normalmente
python backend/app.py
```

### 3️⃣ Parar sem Perder Dados

```bash
docker-compose down
# → Container para
# → Dados salvos em docker/mysql/data/
```

### 4️⃣ Reiniciar

```bash
docker-compose up -d
# → Container reinicia
# → Dados são restaurados
# → Pronto para usar!
```

### 5️⃣ Resetar (Perder Dados)

```bash
docker-compose down -v
# → Remove container E volumes
# → Próximo 'up -d' criará tudo novo
```

---

## ⚙️ Configurações Avançadas

### Aumentar Limite de Memória

```yaml
services:
  db:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

### Adicionar Variáveis Customizadas

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
  MYSQL_DATABASE: ${DB_NAME}
  MYSQL_CHARSET: utf8mb4
  MYSQL_COLLATION: utf8mb4_unicode_ci
  TZ: 'America/Sao_Paulo'
```

### Múltiplos Bancos de Dados

Crie um arquivo `docker/mysql/init.sql`:

```sql
CREATE DATABASE vantrack;
CREATE DATABASE vantrack_test;
GRANT ALL PRIVILEGES ON vantrack.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON vantrack_test.* TO 'root'@'%';
```

E adicione ao docker-compose.yml:

```yaml
volumes:
  - ./docker/mysql/init.sql:/docker-entrypoint-initdb.d/01-init.sql
```

---

## 📚 Referências

- **Docker Compose Official:** https://docs.docker.com/compose/
- **MySQL Docker:** https://hub.docker.com/_/mysql
- **Docker Compose Spec:** https://github.com/compose-spec/compose-spec
- **Healthchecks:** https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck

---

## ✅ Checklist de Implementação

- [x] `docker-compose.yml` criado
- [x] Pasta `docker/mysql/data/` criada
- [x] `.gitkeep` adicionado para manter estrutura
- [x] `.gitignore` atualizado para ignorar dados
- [x] Schema SQL configurado para auto-inicialização
- [x] Healthcheck configurado
- [x] Volume de persistência configurado
- [x] Documentação completa criada

---

## 🎯 Próximas Etapas

1. **Testar inicialização:**
   ```bash
   docker-compose up -d
   docker ps
   mysql -h localhost -u root -proot -e "USE vantrack; SHOW TABLES;"
   ```

2. **Integrar com backend:**
   - Backend continua usando `localhost:3306`
   - Sem mudanças necessárias no código
   - Apenas levantar MySQL com Docker Compose

3. **Produção:**
   - Criar `.env.docker` com credenciais reais
   - Usar variáveis de ambiente
   - Considerear usar volumes nomeados
   - Adicionar healthchecks mais robustos

---

**Status:** ✅ Docker Compose Implementado  
**Última Atualização:** 17/04/2026  
**Versão:** 1.0.0
