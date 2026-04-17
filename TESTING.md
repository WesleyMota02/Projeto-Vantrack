# 📋 GUIA DE TESTES - VANTRACK

## 🚀 Como Rodar os Testes

### Prerequisitos
1. Servidor Flask rodando: `cd backend && python app.py`
2. MySQL conectado e banco `vantrack` criado
3. Python venv ativado

### Teste 1: Fluxo Completo (Cadastro + Login + Endpoints)
```bash
cd backend
python test_complete_flow.py
```

**Testa:**
- ✓ Cadastro de usuário
- ✓ Login com JWT
- ✓ Endpoints protegidos
- ✓ Validação de credenciais
- ✓ Prevenção de duplicatas

### Teste 2: Setup de Banco de Dados
```bash
cd backend
python setup_database.py
```

**Verifica:**
- ✓ Conexão MySQL
- ✓ Criação de schema
- ✓ 10 tabelas criadas
- ✓ Índices criados

### Teste 3: Debug de Cadastro
```bash
cd backend
python debug_cadastro.py
```

**Testa:**
- ✓ Lógica de cadastro isolated
- ✓ Hash de senha
- ✓ Busca de usuário no banco

### Teste 4: Verificação de Banco
```bash
cd backend
python check_db.py
```

**Verifica:**
- ✓ Últimos usuários criados
- ✓ Contagem de usuários ativos
- ✓ Integridade de dados

### Teste 5: API Endpoints (Simples)
```bash
cd backend
python test_api.py
```

**Testa:**
- ✓ Saúde do servidor (ping)
- ✓ Cadastro via HTTP
- ✓ Conexão com banco

---

## 📊 Testes Manual via cURL

### Cadastro
```bash
curl -X POST http://localhost:5000/api/cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_perfil": "aluno",
    "nome": "João",
    "sobrenome": "Silva",
    "cpf": "12345678901",
    "email": "joao@test.com",
    "telefone": "11987654321",
    "cidade": "São Paulo",
    "senha": "SenhaSegura@123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@test.com",
    "senha": "SenhaSegura@123"
  }'
```

**Resposta contém:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": "uuid",
    "email": "joao@test.com",
    "nome": "João",
    "tipo_perfil": "aluno"
  }
}
```

### Usar Token em Endpoints Protegidos
```bash
curl -X GET http://localhost:5000/api/perfil \
  -H "Authorization: Bearer TOKEN_AQUI" \
  -H "Content-Type: application/json"
```

---

## 🧪 Status dos Testes

| Teste | Status | Descrição |
|-------|--------|-----------|
| Cadastro | ✅ PASS | Usuário criado com sucesso |
| Login | ✅ PASS | JWT token gerado corretamente |
| Validação Email Duplicado | ✅ PASS | Rejeita email já existente |
| Senha Incorreta | ✅ PASS | Retorna 401 Unauthorized |
| JWT Validation | ✅ PASS | Endpoints protegidos funcionam |
| Database Connection | ✅ PASS | MySQL conectado e funcional |
| Socket.IO | ⏳ PENDING | Precisa teste manual |
| 2FA | ⏳ TODO | Implementar após testes básicos |

---

## 🐛 Troubleshooting

### "Connection refused on localhost:5000"
- Certifique-se que o servidor está rodando: `python backend/app.py`
- Verifique se a porta 5000 não está em uso

### "Database connection error"
- Verifique MySQL está rodando
- Confirme credenciais em `.env`
- Execute: `python setup_database.py`

### "Token validation failed"
- Verifique JWT_SECRET em `.env`
- Token pode ter expirado (24h validade)
- Faça novo login

---

## 📈 Próximos Testes

1. Socket.IO GPS Realtime
2. Socket.IO Chat Messaging
3. 2FA Flow
4. Performance Testing
5. Load Testing

