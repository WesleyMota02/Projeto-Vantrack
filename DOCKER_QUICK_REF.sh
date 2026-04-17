#!/bin/bash
# 🐳 VANTRACK - DOCKER REFERENCE GUIDE
# Quick commands and troubleshooting

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         VANTRACK - DOCKER QUICK REFERENCE                ║"
echo "║         MySQL Containerization Guide                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}📦 PRÉ-REQUISITOS:${NC}"
echo "   1. Docker Desktop (Windows/Mac) ou Docker + Docker Compose (Linux)"
echo "   2. Download: https://www.docker.com/products/docker-desktop"
echo ""

echo -e "${BLUE}🚀 COMANDOS ESSENCIAIS:${NC}"
echo ""

echo -e "${YELLOW}1. INICIAR BANCO DE DADOS${NC}"
echo "   docker-compose up -d"
echo "   → Cria container, executa schema, inicia MySQL"
echo ""

echo -e "${YELLOW}2. VERIFICAR CONTAINERS${NC}"
echo "   docker ps"
echo "   → Mostra 'vantrack_mysql' se estiver rodando"
echo ""

echo -e "${YELLOW}3. VER LOGS EM TEMPO REAL${NC}"
echo "   docker-compose logs -f db"
echo "   → Mostrar logs até MySQL estar pronto (~30 segundos)"
echo "   → Pressione Ctrl+C para sair"
echo ""

echo -e "${YELLOW}4. CONECTAR AO MYSQL CLI${NC}"
echo "   mysql -h localhost -u root -proot"
echo "   → Conecta ao banco"
echo "   USE vantrack;"
echo "   SHOW TABLES;"
echo "   EXIT;"
echo ""

echo -e "${YELLOW}5. TESTAR CONEXÃO (Python)${NC}"
echo "   cd backend"
echo "   python test_complete_flow.py"
echo "   → Deve passar todos os testes"
echo ""

echo -e "${YELLOW}6. PARAR SEM PERDER DADOS${NC}"
echo "   docker-compose down"
echo "   → Container para, dados em ./docker/mysql/data/ preservados"
echo ""

echo -e "${YELLOW}7. REINICIAR${NC}"
echo "   docker-compose up -d"
echo "   → Reinicia com dados anteriores"
echo ""

echo -e "${YELLOW}8. RESETAR TUDO (CUIDADO!)${NC}"
echo "   docker-compose down -v"
echo "   → Remove container E dados"
echo "   → Próximo 'up -d' criará tudo novo"
echo ""

echo -e "${BLUE}📊 ESTRUTURA DE VOLUMES:${NC}"
echo ""
echo -e "${YELLOW}Volume 1: Persistência${NC}"
echo "   ./docker/mysql/data/ ←→ /var/lib/mysql"
echo "   └─ Dados não perdem ao parar container"
echo ""
echo -e "${YELLOW}Volume 2: Auto-Inicialização${NC}"
echo "   ./database/schema.sql ←→ /docker-entrypoint-initdb.d/"
echo "   └─ Executado apenas na PRIMEIRA inicialização"
echo ""

echo -e "${BLUE}🔧 TROUBLESHOOTING:${NC}"
echo ""

echo -e "${YELLOW}Problema: 'Connection refused on port 3306'${NC}"
echo "   1. Verifique: docker ps"
echo "   2. Se não aparecer: docker-compose logs db"
echo "   3. Se porta está em uso:"
echo "      - Windows: netstat -ano | findstr :3306"
echo "      - Linux: lsof -i :3306"
echo ""

echo -e "${YELLOW}Problema: 'MySQL não inicializa'${NC}"
echo "   1. Ver logs: docker-compose logs db"
echo "   2. Limpar e tentar novamente:"
echo "      docker-compose down -v"
echo "      docker-compose up -d"
echo ""

echo -e "${YELLOW}Problema: 'Dados desapareceram'${NC}"
echo "   1. Confirme que ./docker/mysql/data/ existe"
echo "   2. Se estiver vazio, dados foram perdidos"
echo "   3. Para evitar: sempre use 'docker-compose down' (sem -v)"
echo ""

echo -e "${YELLOW}Problema: 'Permission denied em docker/'${NC}"
echo "   1. Linux: chmod -R 755 docker/"
echo "   2. Windows: Executar cmd como Admin"
echo ""

echo -e "${BLUE}📈 MONITORAMENTO:${NC}"
echo ""
echo "Logs contínuos:"
echo "   docker-compose logs -f db"
echo ""
echo "Stats de recurso:"
echo "   docker stats vantrack_mysql"
echo ""
echo "Inspecionar container:"
echo "   docker inspect vantrack_mysql"
echo ""

echo -e "${BLUE}💾 BACKUP E RESTORE:${NC}"
echo ""
echo "Fazer backup:"
echo "   docker exec vantrack_mysql mysqldump -u root -proot vantrack > backup.sql"
echo ""
echo "Restaurar backup:"
echo "   docker exec -i vantrack_mysql mysql -u root -proot vantrack < backup.sql"
echo ""

echo -e "${BLUE}🔐 CREDENCIAIS PADRÃO (DESENVOLVIMENTO):${NC}"
echo "   Hostname: localhost"
echo "   Porta: 3306"
echo "   Usuário: root"
echo "   Senha: root"
echo "   Database: vantrack"
echo ""

echo -e "${BLUE}📋 WORKFLOW TÍPICO:${NC}"
echo ""
echo "   PRIMEIRA VEZ:"
echo "   $ docker-compose up -d"
echo "   $ docker-compose logs -f db    (aguarde ~30s)"
echo "   $ mysql -h localhost -u root -proot"
echo "   $ USE vantrack; SHOW TABLES;"
echo ""
echo "   DESENVOLVIMENTO:"
echo "   $ python backend/app.py"
echo "   $ python backend/test_complete_flow.py"
echo ""
echo "   PARAR:"
echo "   $ docker-compose down"
echo ""
echo "   REINICIAR:"
echo "   $ docker-compose up -d"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Para mais detalhes, veja DOCKER.md${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
