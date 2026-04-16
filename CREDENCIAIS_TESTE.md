# 🔐 Credenciais de Teste - VanTrack

## Dados para Login

### 👨‍🚗 MOTORISTA
```
Email:  motorista@teste.com
Senha:  123456
CPF:    12345678901
```

**Dados Completos:**
- Nome: João
- Sobrenome: Silva
- Telefone: 11987654321
- Cidade: São Paulo

---

### 👨‍🎓 ALUNO
```
Email:  aluno@teste.com
Senha:  123456
CPF:    98765432101
```

**Dados Completos:**
- Nome: Maria
- Sobrenome: Santos
- Telefone: 11912345678
- Cidade: São Paulo

---

## 📝 Como Adicionar ao Banco de Dados

### Opção 1: Usar a API de Cadastro (Recomendado)

**Motorista:**
```bash
curl -X POST http://localhost:5000/api/cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "motorista@teste.com",
    "senha": "123456",
    "cpf": "12345678901",
    "nome": "João",
    "sobrenome": "Silva",
    "telefone": "11987654321",
    "cidade": "São Paulo",
    "tipo_perfil": "motorista"
  }'
```

**Aluno:**
```bash
curl -X POST http://localhost:5000/api/cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "aluno@teste.com",
    "senha": "123456",
    "cpf": "98765432101",
    "nome": "Maria",
    "sobrenome": "Santos",
    "telefone": "11912345678",
    "cidade": "São Paulo",
    "tipo_perfil": "aluno"
  }'
```

### Opção 2: Inserção Manual no PostgreSQL

Use DBeaver ou psql para executar:

```sql
-- Motorista de teste
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES (
    'motorista',
    'João',
    'Silva',
    '12345678901',
    'motorista@teste.com',
    '11987654321',
    'São Paulo',
    '$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS/cWc/zriCj'
);

-- Aluno de teste
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES (
    'aluno',
    'Maria',
    'Santos',
    '98765432101',
    'aluno@teste.com',
    '11912345678',
    'São Paulo',
    '$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS/cWc/zriCj'
);

-- Verificar inserção
SELECT id, tipo_perfil, nome, email FROM usuarios 
WHERE email IN ('motorista@teste.com', 'aluno@teste.com');
```

---

## 🧪 Fluxo de Teste Recomendado

### 1️⃣ Login Normal (Dispositivo Conhecido)
```
1. Acesse: http://localhost:3000 (ou seu frontend)
2. Selecione "Motorista"
3. Email: motorista@teste.com
4. Senha: 123456
5. Clique em "Entrar"
```

**Resultado Esperado:**
- ✅ Login bem-sucedido (sem 2FA)
- ✅ Redirecionado para Dashboard Motorista

### 2️⃣ Primeiro Login (Novo Dispositivo - com 2FA)
```
1. Limpar localStorage/sessionStorage do navegador
2. Usar uma senha/email diferente ou novo navegador
3. Fazer login com mesma conta
```

**Resultado Esperado:**
- 📱 Página 2FA aparece
- ✉️ Código de 6 dígitos é enviado (SMS/Email)
- ✅ Após verificação: Login completo

### 3️⃣ Teste de Alertas e Validações
```
Teste "Email inválido" → Error
Teste "Senha vazia" → Error
Teste "Perfil não selecionado" → Error
Teste "Senha incorreta" → Error
```

---

## 📊 Fluxo Completo do Sistema

```
┌─────────────┐
│   Login     │
└──────┬──────┘
       │
       ├─→ ✅ Email + Senha corretos?
       │   └─→ Verificar dispositivo
       │       ├─→ 🆕 Novo dispositivo (User-Agent + IP)
       │       │   └─→ Gerar código 2FA (6 dígitos)
       │       │       └─→ Enviar via SMS/Email (Twilio/SMTP)
       │       │           └─→ Página 2FA
       │       │               └─→ ✅ Código correto?
       │       │                   └─→ ✅ Login OK → Dashboard
       │       │
       │       └─→ ✅ Dispositivo conhecido
       │           └─→ ✅ Login OK → Dashboard
       │
       └─→ ❌ Email/Senha incorretos?
           └─→ Error: "Credenciais inválidas"
```

---

## 🎯 Dashboards Esperados

### Dashboard Motorista
- Início (Checklist, Próxima Rota, Mensagens)
- Lista de Alunos
- Rotas
- Chat (WebSocket em tempo real)

### Dashboard Aluno
- Rastreamento (Mapa Leaflet em tempo real)
- Frequência (Calendário + Toggle SIM/NÃO)
- Chat com Motorista (WebSocket em tempo real)
- Configurações

---

## ⚙️ Variáveis de Ambiente Necessárias

Para 2FA funcionar, configure no `backend/.env`:

```env
# Twilio SMS
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# SMTP Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=seu_app_password
```

---

## 🚀 Pronto para Testar!

Escolha uma credencial acima e faça login para ver o sistema em ação! 🎉
