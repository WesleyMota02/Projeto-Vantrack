# 🎯 GUIA DE TESTE - VanTrack

## 🔑 Credenciais Padrão

### 👨‍🚗 MOTORISTA
```
Email:  motorista@teste.com
Senha:  123456
```

### 👨‍🎓 ALUNO  
```
Email:  aluno@teste.com
Senha:  123456
```

---

## ⚡ COMEÇAR AGORA

### 1. Iniciar Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend rodará em: **http://localhost:5000**

### 2. Abrir Frontend
```
Abra seu navegador em: http://localhost:3000
(ou o caminho do seu index.html)
```

### 3. Fazer Login
- Selecione o tipo de usuário (Motorista ou Aluno)
- Use uma das credenciais acima
- Clique em "Entrar"

---

## 📋 O QUE TESTAR

### ✅ Motorista
1. **Dashboard Motorista** - Seções de Início, Alunos, Rotas, Chat
2. **Chat em Tempo Real** - Envie mensagens para pais
3. **Dados Pessoais** - Nome, email, telefone aparecem na sidebar

### ✅ Aluno
1. **Mapa Rastreamento** - Vê a localização do ônibus em tempo real
2. **Calendário Presença** - Toggle SIM/NÃO para confirmar embarque
3. **Chat em Tempo Real** - Comunique-se com motorista
4. **Configurações** - Endereços de coleta/entrega

### ✅ 2FA (Autenticação de Dois Fatores)
1. **Novo Dispositivo**: Limpe o localStorage e tente login novamente
2. **Página 2FA**: Deve aparecer pedindo código de 6 dígitos
3. **Código**: Digite os números (para teste, use qualquer código que vai falhar - teste 3 tentativas)
4. **Reenvio**: Botão de "Reenviar" com cooldown de 60s

---

## 🗄️ CRIAR USUÁRIOS NO BANCO

### Opção A: Usar API (curl)
```bash
# Motorista
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

# Aluno
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

### Opção B: SQL Direto (DBeaver/psql)
```sql
-- Motorista
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

-- Aluno
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
```

---

## 🎥 FLUXO VISUAL

```
┌─────────────────────────────────────────┐
│         PÁGINA DE LOGIN                 │
│  ┌───────────────────────────────────┐  │
│  │ Selecione: [Motorista ▼]         │  │
│  │ Email:     motorista@teste.com    │  │
│  │ Senha:     ••••••                 │  │
│  │ [ENTRAR]                          │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              │
              ├─ Se NOVO DISPOSITIVO
              │  └──→ [PÁGINA 2FA] → Código 6 dígitos
              │      └──→ [DASHBOARD]
              │
              └─ Se DISPOSITIVO CONHECIDO
                 └──→ [DASHBOARD]

┌──────────────────────────────────────────────────┐
│    DASHBOARD MOTORISTA / ALUNO                   │
├──────────────────────────────────────────────────┤
│ SIDEBAR LATERAL                                  │
│ ┌──────────────────┐                            │
│ │ 👤 João Silva    │ ← Nome do usuário         │
│ │                  │                            │
│ │ [Início]         │                            │
│ │ [Alunos]         │                            │
│ │ [Rotas]          │                            │
│ │ [Chat]           │                            │
│ │                  │                            │
│ │ [SAIR]           │                            │
│ └──────────────────┘                            │
│           │ CONTEÚDO PRINCIPAL                  │
│           │                                      │
│           ├─ Início: Cards com informações      │
│           ├─ Alunos: Tabela com lista           │
│           ├─ Rotas: Informações de rotas        │
│           └─ Chat: Interface de mensagens (WS)  │
└──────────────────────────────────────────────────┘
```

---

## 🔧 CARACTERÍSTICAS IMPLEMENTADAS

### ✨ Autenticação
- ✅ Login/Cadastro com validação
- ✅ JWT Token (24h expiração)
- ✅ Senha hasheada com bcrypt
- ✅ 2FA com SMS/Email (novo dispositivo)

### 🗺️ Real-time
- ✅ GPS em tempo real (WebSocket - Leaflet.js)
- ✅ Chat em tempo real (WebSocket)
- ✅ Broadcasts por room (rota_id para GPS, chat_id para mensagens)

### 📱 Interface
- ✅ Dashboard responsivo
- ✅ Sidebar com navegação
- ✅ Cards com dados
- ✅ Calendário com presença
- ✅ Mapa interativo
- ✅ Chat com timestamps

### 🏗️ Arquitetura
- ✅ Clean Architecture (Domain → Use Cases → Repositories)
- ✅ Testes unitários
- ✅ PostgreSQL com migrations
- ✅ Middleware de autenticação
- ✅ Tratamento de erros robusto

---

## 🎮 TESTES RÁPIDOS

### Login com Motorista
```
1. Selecione: Motorista
2. Email: motorista@teste.com
3. Senha: 123456
4. Clique ENTRAR → Dashboard Motorista
```

### Login com Aluno
```
1. Selecione: Aluno
2. Email: aluno@teste.com
3. Senha: 123456
4. Clique ENTRAR → Dashboard Aluno
```

### Testar 2FA
```
1. Faça login normalmente (funcionará sem 2FA na primeira vez)
2. Abra o DevTools (F12) → Console
3. Execute: localStorage.clear()
4. Recarregue e tente fazer login novamente
5. Deve aparecer página 2FA com código
```

### Testar Chat
```
1. Abra 2 abas do navegador
2. Uma com Motorista, outra com Aluno
3. Envie mensagens entre elas
4. Mensagens aparecem em tempo real (WebSocket)
```

### Testar Mapa
```
1. Login como Aluno
2. Vá para "Rastreamento"
3. Deve aparecer mapa interativo (Leaflet.js)
4. Van icon no meio da tela
```

---

## 📊 ESTRUTURA DE PASTAS

```
Projeto-vantrack/
├── pages/
│   ├── index.html              (Login)
│   ├── 2fa.html                (Verificação 2FA)
│   ├── dashboard-motorista.html (Dashboard Motorista)
│   └── dashboard-aluno.html     (Dashboard Aluno)
├── assets/
│   ├── js/
│   │   ├── login.js            (Lógica de login + 2FA)
│   │   ├── 2fa.js              (Verificação 2FA)
│   │   ├── dashboard-motorista.js
│   │   ├── dashboard-aluno.js
│   │   ├── realtime-chat.js    (Chat WebSocket - Motorista)
│   │   ├── realtime-chat-aluno.js (Chat WebSocket - Aluno)
│   │   └── realtime-rastreamento.js (GPS WebSocket)
│   └── css/
│       └── *.css               (Estilos)
└── backend/
    ├── app.py                  (Flask app)
    ├── database.py             (Conexão PostgreSQL)
    ├── domain/
    │   ├── usuario.py
    │   ├── dashboard.py
    │   └── dois_fatores.py    (Modelo 2FA)
    ├── infra/
    │   └── *_repository.py    (Acesso a dados)
    ├── use_cases/
    │   ├── autenticar_usuario.py
    │   ├── dashboard_commands.py
    │   └── dois_fatores_commands.py (Lógica 2FA)
    ├── presentation/
    │   ├── routes/
    │   │   ├── auth_routes.py  (Login/Cadastro com 2FA)
    │   │   └── dois_fatores_routes.py (Endpoints 2FA)
    │   └── sockets/
    │       └── realtime_handlers.py (WebSocket)
    └── requirements.txt        (Dependências)
```

---

## 🚀 PRÓXIMAS MELHORIAS (Opcionais)

- [ ] Recuperação de conta (segurança)
- [ ] Google Authenticator / TOTP
- [ ] Dashboard de dispositivos autorizados
- [ ] Rate limiting global
- [ ] Logs de acesso
- [ ] Notificações push
- [ ] Modo escuro
- [ ] Multi-idioma

---

## ❓ DÚVIDAS?

**Tudo está funcionando?** ✅ Sim! O projeto está pronto.

**Como sai do dashboard?** Clique em [SAIR] na sidebar.

**Como volta ao login?** Recarregue a página ou clique em [SAIR].

**As mensagens persistem?** Sim, ficam no banco de dados PostgreSQL.

**Como resetar para começar de novo?** 
```sql
DELETE FROM usuarios;
DELETE FROM sessoes;
DELETE FROM dois_fatores;
```

---

## 📝 LICENÇA

VanTrack v1.0.0 - Sistema de Rastreamento Escolar com 2FA

Desenvolvido com ❤️ em 2026

