# Architecture Decision Records (ADR) - Vantrack

## ADR-001: Reestruturação de Arquivos Frontend para Clean Architecture

**Data:** 15 de Abril de 2026  
**Status:** ACEITO  
**Responsável:** @Architect, @Orchestrator  

---

### 1. Contexto

O projeto Vantrack apresentava uma estrutura de arquivos frontend fragmentada:
- Arquivos HTML soltos na raiz com nomenclatura inconsistente
- CSS duplicado em `src/css/` com nomes mistos (camelCase/snake_case)
- JavaScript em `src/js/` com nomes inconsistentes (`Script.js` vs `telas_cad.js`)
- Imagens em `src/img/` sem padronização de referências

Esta estrutura violava os princípios de Clean Architecture e dificultava a manutenção e escalabilidade.

---

### 2. Decisão

Reestruturar o projeto para:

1. **Nomenclatura Uniforme:** Todos os arquivos em **kebab-case** (ex: `cadastro-aluno.html`, `recuperar-senha.html`)
2. **Centralização de Assets:** Criar pasta `/assets` na raiz com subpastas `/css`, `/js` e `/img`
3. **Padrão de Caminhos:** Atualizar todas as referências de `<link>`, `<script>` e `<img>` para apontar ao novo padrão `assets/*`
4. **Compatibilidade:** Manter arquivos antigos temporariamente sem deletar; remover em ciclo futuro após validação em produção

---

### 3. Estrutura Final

```
Projeto-vantrack/
├── index.html                      # Login principal (reorganizado)
├── cadastro-aluno.html             # Cadastro de Alunos
├── cadastro-motorista.html         # Cadastro de Motoristas
├── recuperar-senha.html            # Recuperação de Senha
├── perfil.html                     # Escolha de Perfil
├── gps.html                        # Rastreamento GPS
│
├── assets/                         # ⭐ NOVO: Centralização de Assets
│   ├── css/
│   │   ├── login.css
│   │   ├── style.css
│   │   ├── style-aluno.css
│   │   ├── recuperar-senha.css
│   │   ├── gps.css
│   │   └── perfil.css
│   ├── js/
│   │   ├── login.js
│   │   ├── script.js               # Consolidação: Script.js + lógicas de cadastro
│   │   ├── telas-cad.js            # Renomeado de telas_cad.js
│   │   └── gps.js
│   └── img/
│       ├── aluno.png
│       ├── motorista.png
│       └── van.png.png
│
├── src/                            # ⚠️ LEGADO: Manter até migração total
│   ├── css/                        # Será removido após validação
│   ├── js/                         # Será removido após validação
│   └── img/                        # Será removido após validação
│
└── vantrack-backend/               # Backend (não afetado)
```

---

### 4. Mudanças Realizadas

#### 4.1 Nomes de Arquivos (Kebab-case)
- `cadastro_aluno.html` → `cadastro-aluno.html`
- `cadastro_motorista.html` → `cadastro-motorista.html`
- `recuperar.html` → `recuperar-senha.html`
- `Script.js` → `script.js`
- `telas_cad.js` → `telas-cad.js`
- `Style.css` → `style.css`
- `recuperar.css` → `recuperar-senha.css`

#### 4.2 Referências Atualizadas
Todos os arquivos HTML foram atualizados com novos caminhos:

**Antes:**
```html
<link rel="stylesheet" href="src/css/login.css">
<script src="src/js/Script.js"></script>
<img src="src/img/van.png.png" alt="Van">
```

**Depois:**
```html
<link rel="stylesheet" href="assets/css/login.css">
<script src="assets/js/script.js"></script>
<img src="assets/img/van.png.png" alt="Van">
```

#### 4.3 Links Internos Atualizados
No `index.html` e `perfil.html`, os links entre páginas foram ajustados:
```html
<!-- Antes -->
<a href="recuperar.html">...</a>
<a href="cadastro_motorista.html">...</a>

<!-- Depois -->
<a href="recuperar-senha.html">...</a>
<a href="cadastro-motorista.html">...</a>
```

---

### 5. Consequências Positivas

✅ **Melhor Organização:** Assets centralizados e fáceis de localizar  
✅ **Consistência:** Nomenclatura uniforme facilita buscas (`grep`) e automação  
✅ **Escalabilidade:** Estrutura pronta para novos assets (fontes, ícones, SVGs)  
✅ **Manutenção:** Reduz cognitive load ao compreender a estrutura  
✅ **Clean Architecture:** Separação clara entre lógica e apresentação  

---

### 6. Riscos & Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Links quebrados em produção | Alto | Validação completa em navegador antes de deploy |
| Cache de browser desatualizado | Médio | Instruir usuários a fazer hard refresh (Ctrl+Shift+R) |
| Arquivos antigos deixados para trás | Baixo | Remover `src/` após 1 ciclo de produção |

---

### 7. Próximos Passos

1. **Curto Prazo:** Remover arquivos antigos em `src/` após validação em staging
2. **Médio Prazo:** Documentar padrão de assets no `README.md`
3. **Longo Prazo:** Considerar bundling (Webpack/Vite) se o projeto crescer além de 50KB de CSS/JS

---

### 8. Aprovação

- **@Architect:** ✅ Estrutura validada
- **@Orchestrator:** ✅ Documentação completa

**Versão do ADR:** v1.0  
**Última Atualização:** 15/04/2026

---

## ADR-002: Refatoração de CSS com Design System Unificado

**Data:** 15 de Abril de 2026  
**Status:** ACEITO  
**Responsável:** @Architect, @Dev  

---

### 1. Contexto

Os arquivos CSS apresentavam:
- **Duplicação de Variáveis:** Cada arquivo CSS definia seu próprio `:root` com cores e sombras
- **Regras Conflitantes:** `#card-cadastro` declarado 2x com paddings diferentes
- **Posicionamento Frágil:** Logo da van usando `position: relative; top: 100px` com magic numbers
- **Falta de Componentes:** Classes como `.campo`, `.btn-cadastrar` repetidas em múltiplos arquivos
- **Nomenclatura Inconsistente:** Variáveis como `--azul-fundo`, `--fundo-pagina`, `--bg-light`

---

### 2. Decisão

Implementar **Design System centralizado** com:

1. **`global.css`** — Único ponto de verdade para variáveis, reset e tipografia
2. **`components.css`** — Classes reutilizáveis (`.input-group`, `.btn`, `.card`)
3. **CSSs Específicos** — `login.css`, `cadastro.css`, `recuperar-senha.css`, `perfil.css`, `gps.css`
   - Sem duplicação de :root, *, ou body{font-family}
   - Apenas estilos exclusivos da página

---

### 3. Estrutura de CSS

#### 3.1 `global.css` (Centralizado)
```css
:root {
  --primary-blue: #0F6CD5;
  --text-primary: #1f2933;
  --shadow-md: 0 8px 20px rgba(0, 0, 0, 0.25);
  /* ... todas as variáveis */
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Poppins", ...; }
```

#### 3.2 `components.css` (Reutilizável)
```css
.input-group { display: flex; gap: 8px; ... }
.btn { border: none; cursor: pointer; ... }
.card { background-color: var(--white); box-shadow: var(--shadow-lg); ... }
```

#### 3.3 Arquivos Específicos
Exemplo `cadastro.css`:
```css
body { background: linear-gradient(...); }
#tela-cadastro { display: flex; ... }
.topo-cadastro { ... }
/* Sem :root, sem *, sem body{font-family} */
```

---

### 4. Refatorações Críticas

#### 4.1 Logo da Van — Antes
```css
#logo-van {
  position: relative; 
  top: 100px;
  transform: translate(-60%, -160%);  /* magic numbers */
  z-index: 10;
}
```

#### 4.1 Logo da Van — Depois
```css
#logo-van {
  width: 140px;
  height: auto;
  /* Flexbox do .header-login cuida do posicionamento */
}

.header-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;  /* espaçamento sólido */
}
```

#### 4.2 Unificação de Nomenclatura
- ❌ `--azul-fundo`, `--fundo-pagina`, `--bg-light`
- ✅ `--bg-light` (único)

- ❌ `--cinza-placeholder`, `--cinza-ph`, `--placeholder-gray`
- ✅ `--placeholder-gray` (único)

---

### 5. Estrutura Final de CSS

```
assets/css/
├── global.css                 # 56 linhas - :root, reset, tipografia
├── components.css             # 174 linhas - componentes reutilizáveis
├── login.css                  # Refatorado - sem :root
├── cadastro.css               # Novo - sem :root
├── recuperar-senha.css        # Refatorado - sem :root
├── perfil.css                 # Refatorado - sem :root
└── gps.css                    # Refatorado - sem :root
```

**Arquivos Removidos:**
- ❌ `style.css` (duplicação)
- ❌ `style-aluno.css` (consolidado em `cadastro.css`)

---

### 6. Inclusão em HTMLs

**Padrão Novo:**
```html
<head>
  <link rel="stylesheet" href="assets/css/global.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/[pagina].css">
</head>
```

---

### 7. Benefícios

✅ **DRY (Don't Repeat Yourself):** Variáveis definidas uma única vez  
✅ **Manutenibilidade:** Trocar cor = alterar `:root`  
✅ **Escalabilidade:** Novo componente = adicionar classe em `components.css`  
✅ **Performance:** Consolidação reduz arquivo CSS total  
✅ **Responsividade:** Flexbox em vez de `position: absolute` com magic numbers  
✅ **Zero Comentários Redundantes:** Código autoexplicativo  

---

### 8. Riscos & Validação

| Risco | Mitigação |
|-------|-----------|
| Variável não encontrada em global.css | Verificar em global.css antes de usar |
| Conflito de especificidade CSS | Ordem: global → components → page-specific |
| Cache do navegador obsoleto | Usar Ctrl+Shift+R em desenvolvimento |

---

### 9. Aprovação

- **@Architect:** ✅ Design System validado
- **@Dev:** ✅ Refatoração concluída e testada
- **@Orchestrator:** ✅ Documentação completa

**Versão do ADR:** v1.1 (com ADR-002)  
**Última Atualização:** 15/04/2026

---

## ADR-003: Sistema de Validação, Segurança e Modularização Frontend

**Data:** 15 de Abril de 2026  
**Status:** ACEITO  
**Responsável:** @QA_Sec, @Dev  

---

### 1. Contexto

O JavaScript frontend apresentava vulnerabilidades e anti-patterns:
- ❌ Sem validação de entrada (CPF, email, telefone, senha)
- ❌ Alertas genéricos (`alert()`) em vez de feedback visual elegante
- ❌ Duplicação de código em múltiplos scripts
- ❌ Sem sanitização de inputs (risco de XSS)
- ❌ Requisições sem tratamento robusto de erros
- ❌ Senhas sem requisitos mínimos de força
- ❌ Sem módulos reutilizáveis

---

### 2. Decisão

Implementar **Sistema de Validação Centralizado** com 4 módulos JavaScript:

#### 2.1 `validators.js` — Lógica de Validação Reutilizável
```javascript
Validators = {
  email(email),          // RFC 5321 + max 254 chars
  cpf(cpf),              // Algoritmo de dígito verificador
  phone(phone),          // Formato brasileiro (11 dígitos)
  password(password),    // Min 8 chars, maiúsculas, minúsculas, números
  passwordStrength(pwd), // 0-6 níveis
  name(name),            // 2-100 chars, apenas letras
  formatCPF(cpf),        // XXX.XXX.XXX-XX
  formatPhone(phone),    // (XX) XXXXX-XXXX
  sanitizeInput(input)   // Remove < > e limita a 255 chars
}
```

#### 2.2 `config.js` — Configuração Centralizada
```javascript
Config = {
  API_BASE_URL,      // http://localhost:3000/api
  ENDPOINTS,         // rotas de login, cadastro, etc
  ERROR_MESSAGES,    // mensagens padronizadas
  STORAGE_KEYS,      // chaves do localStorage
  VALIDATION_RULES   // limites de caracteres
}
```

#### 2.3 `ui-feedback.js` — Feedback Visual Elegante
```javascript
UIFeedback = {
  showError(element, message),      // Marca input como inválido + exibe mensagem
  clearError(element),               // Remove estado de erro
  showSuccess(message),              // Toast verde de sucesso
  showWarning(message),              // Toast laranja de aviso
  showError(message),                // Toast vermelho de erro
  setLoading(button, isLoading),    // Desabilita botão + spinner animado
  showPasswordStrength(password)     // Indicador visual de força
}
```

#### 2.4 `script.js` (Refatorado) — Lógica de Negócio
```javascript
FormValidator = {
  validateRegistration(formData),    // CPF + email + senha + telefone
  validateLogin(formData),            // email + senha + perfil
  showErrors(form, errors)            // Popula campo com erro
}

PasswordToggle = { init() }            // Mostrar/esconder senha (reutilizável)
LoginModule = { init() }               // Lógica específica de login
```

---

### 3. Requisitos de Validação Implementados

| Campo | Validações | Mensagem |
|-------|-----------|----------|
| Email | RFC 5321, max 254 chars | "E-mail inválido." |
| CPF | Dígito verificador (2 módulos 11) | "CPF inválido." |
| Telefone | 11 dígitos, começa com 1x | "Telefone inválido. Use formato brasileiro (11 dígitos)." |
| Senha | Min 8 chars, [A-Z], [a-z], [0-9] | "Senha fraca. Use maiúsculas, minúsculas, números..." |
| Nome/Sobrenome | 2-100 chars, apenas letras + acentos | "Nome inválido (mínimo 2 caracteres, máximo 100)." |
| Cidade | 2-100 chars | "Cidade inválida." |

---

### 4. Fluxo de Validação (Front-end)

```
Usuário preenche formulário
         ↓
Clica em "Cadastrar" ou "Entrar"
         ↓
FormValidator.validateRegistration(formData)
  ├─ CPF válido?
  ├─ Email válido?
  ├─ Telefone válido?
  ├─ Senha forte?
  └─ Todos os campos obrigatórios?
         ↓
SIM → Envia para backend (API)
NÃO → FormValidator.showErrors(form, errors)
      └─ UIFeedback.showError(campo, mensagem)
         └─ Campo marca com .is-invalid (border-color: #f44336)
         └─ Mensagem de erro aparece abaixo do campo
```

---

### 5. Melhorias de Segurança Implementadas

✅ **Sanitização de Entrada:**
```javascript
Validators.sanitizeInput(input) // Remove < > e limita a 255 chars
```

✅ **Validação Dupla (Front + Back):**
- Front: UX imediato, feedback em tempo real
- Back: Segurança real, impedindo requisições malformadas

✅ **Indicador de Força de Senha:**
```javascript
UIFeedback.showPasswordStrength(password) // Mostra: Fraca/Regular/Boa/Forte/Excelente
```

✅ **Feedback Elegante (Sem Alertas):**
```
❌ ANTES: alert("❌ CPF inválido");
✅ DEPOIS: Toast vermelho flutuante em 5 segundos + campo com borda vermelha
```

✅ **Armazenamento de Sessão:**
```javascript
localStorage.setItem("usuarioLogado", JSON.stringify(user));
localStorage.setItem("lembrarMe", email); // "Lembrar-me"
```

---

### 6. Estrutura de Arquivos Criada

```
assets/js/
├── config.js              # Configuração centralizada (API, endpoints, mensagens)
├── validators.js          # Funções de validação reutilizáveis
├── ui-feedback.js         # Feedback visual (toasts, erros, loading)
├── script.js              # Lógica de login e cadastro (refatorada)
├── login.js               # Mini-módulo específico de login
├── gps.js                 # GPS com melhor tratamento de erros
└── [outros]
```

---

### 7. Arquivos de Configuração Criados

**Frontend (`.env.example` na raiz)**
```env
API_BASE_URL=http://localhost:3000/api
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
NODE_ENV=development
```

**Backend (`vantrack-backend/.env.example`)**
```env
PORT=3000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=...
JWT_SECRET=...
BCRYPT_ROUNDS=10
```

---

### 8. Código Exemplo — Cadastro com Validações

```javascript
formCadastro.addEventListener("submit", async (event) => {
  event.preventDefault();
  UIFeedback.clearAllErrors(formCadastro);

  const formData = {
    nome: document.getElementById('nome')?.value.trim() || '',
    // ... outros campos
  };

  // Validação no front
  const errors = FormValidator.validateRegistration(formData);
  if (errors) {
    FormValidator.showErrors(formCadastro, errors);
    UIFeedback.showWarning("Verifique os erros no formulário.");
    return;
  }

  // Desabilita botão enquanto envia
  UIFeedback.setLoading(submitButton, true);

  try {
    const response = await fetch(`${Config.API_BASE_URL}${Config.ENDPOINTS.ALUNOS_CADASTRAR}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      UIFeedback.showSuccess(result.message);
      formCadastro.reset();
      // Redireciona após 1.5s
    } else {
      UIFeedback.showError(result.message);
    }
  } catch (error) {
    UIFeedback.showError(Config.ERROR_MESSAGES.NETWORK_ERROR);
  } finally {
    UIFeedback.setLoading(submitButton, false);
  }
});
```

---

### 9. CSS Adicionado para Feedback Visual

```css
.toast {
  position: fixed; bottom: -100px; /* fora da tela */
  transition: bottom 0.3s ease-in-out;
}
.toast.show { bottom: 20px; } /* anima para dentro */

.error-message { color: #f44336; font-size: 12px; }
input.is-invalid { border-color: #f44336; background-color: #ffebee; }

.spinner { animation: spin 0.6s linear infinite; }
```

---

### 10. Benefícios

✅ **Segurança:** Validação dupla (front + back) previne injeções de dados inválidos  
✅ **UX:** Feedback visual elegante em vez de alertas genéricos  
✅ **Manutenibilidade:** Validadores centralizados em 1 arquivo  
✅ **Reutilização:** `UIFeedback` usada em qualquer formulário futuro  
✅ **DRY:** Sem duplicação de regras de validação  
✅ **Escalabilidade:** `Config.ENDPOINTS` facilita adicionar novas rotas  
✅ **Acessibilidade:** `aria-label`, `aria-live`, `aria-invalid` nos elementos  

---

### 11. Estrutura Final de Inclusão HTML

```html
<head>
  <link rel="stylesheet" href="assets/css/global.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/[page].css">
</head>

<body>
  <!-- ... conteúdo ... -->
  <script src="assets/js/config.js"></script>
  <script src="assets/js/validators.js"></script>
  <script src="assets/js/ui-feedback.js"></script>
  <script src="assets/js/script.js"></script>
</body>
```

---

### 12. Aprovação

- **@QA_Sec:** ✅ Validações duplas confirmadas (front + back)
- **@Dev:** ✅ Modularização concluída e testada
- **@Reviewer:** ✅ Zero comentários redundantes mantido
- **@Orchestrator:** ✅ Documentação completa

**Versão do ADR:** v1.2 (com ADR-003)  
**Última Atualização:** 15/04/2026
