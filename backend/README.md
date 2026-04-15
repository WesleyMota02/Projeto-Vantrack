# Vantrack Backend - Python/Flask

Clean Architecture backend for Vantrack (Sistema de Transporte Escolar)

## Arquitetura

```
backend/
├── domain/              # Entidades de negócio
│   ├── usuario.py
│   └── validadores.py
├── infra/              # Camada de infraestrutura
│   ├── usuario_repository.py
│   └── repository_interface.py
├── use_cases/          # Lógica de negócio
│   ├── cadastrar_usuario.py
│   ├── autenticar_usuario.py
│   └── recuperar_senha.py
├── presentation/       # Camada de apresentação
│   ├── routes/
│   │   └── auth_routes.py
│   ├── dtos.py         # Objetos de transferência de dados
│   └── __init__.py
├── middleware/         # Middleware da aplicação
│   └── token_middleware.py
├── config.py           # Configuração da aplicação
├── database.py         # Abstração de banco de dados
├── app.py              # Inicialização da aplicação
├── requirements.txt    # Dependências Python
└── tests/              # Testes unitários
```

## Dependências

```bash
pip install -r requirements.txt
```

## Configuração de Ambiente

1. Criar arquivo `.env`:
```bash
cp .env.example .env
```

2. Preencher variáveis:
```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/vantrack_db
JWT_SECRET=sua-chave-secreta-super-segura-aqui
JWT_EXPIRY=86400
FLASK_ENV=development
```

## Inicializar Banco de Dados

```bash
python -c "from database import Database; db = Database('DATABASE_URL'); db.init_db('DATABASE_URL', '../database/schema.sql')"
```

## Executar Aplicação

```bash
python app.py
```

Servidor rodará em: `http://localhost:5000`

## Endpoints

### Cadastro
- `POST /api/alunos/cadastrar` - Registrar aluno
- `POST /api/motoristas/cadastrar` - Registrar motorista

### Autenticação
- `POST /api/login` - Login (retorna JWT token)
- `POST /api/recuperar-senha` - Recuperar senha

## Testes

```bash
pytest tests/
```

## Padrões de Código

- **Sem comentários**: Código auto-documentável com nomes semânticos
- **Exceções específicas**: Nunca lance `Exception` genérica
- **Separação de camadas**: Domain → Use Cases → Infra → Presentation
- **Validação primeiro**: Sempre valide dados ANTES de processar
- **Hashing de senhas**: Sempre use bcrypt com BCRYPT_LOG_ROUNDS=12

## Status

✅ Implementação completa da camada de autenticação
- Repository pattern para acesso a dados
- Use cases para lógica de negócio
- DTOs para serialização
- Validação robusta com Pydantic
- JWT token generation
- Bcrypt password hashing
- Middleware de autenticação
