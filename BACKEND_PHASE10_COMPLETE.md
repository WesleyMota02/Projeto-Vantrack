# Vantrack Backend - Phase 10: Protected Routes & Domain Expansion ✅ COMPLETE

## Overview

Phase 10 expands the backend with protected routes, JWT middleware, and introduces 4 new domain models (Veículos, Rotas, Inscrições, GPS). This enables full transportation management functionality.

---

## 🔐 PHASE 10a: Protected Routes & Authentication

### New Files Created (8 files):

**1. Authentication Middleware**
- `middleware/autenticacao.py` (73 lines)
  - `AutenticacaoMiddleware` class with 2 decorators:
    - `@requer_token`: Validates JWT token from Authorization header
    - `@requer_perfil(perfis...)`: Role-based access control

**2. User Query Use Cases**
- `use_cases/usuario_queries.py` (61 lines)
  - `ObterUsuario`: Fetch single user by ID
  - `ListarUsuariosPorTipo`: List all users of specific type (aluno/motorista)
  - `AtualizarPerfilUsuario`: Update user profile (nome, sobrenome, telefone, cidade only)

**3. Protected User Routes**
- `presentation/routes/usuario_routes.py` (115 lines)
  - `GET /api/usuarios/<usuario_id>` - Get user details (protected)
  - `GET /api/alunos` - List all students (protected)
  - `GET /api/motoristas` - List all drivers (protected)
  - `PUT /api/usuarios/<usuario_id>` - Update own profile (protected + self-check)

### New API Endpoints

#### Get User Profile
```
GET /api/usuarios/{usuario_id}
Authorization: Bearer <jwt_token>

Response 200:
{
  "sucesso": true,
  "usuario": {
    "id": "uuid",
    "tipo_perfil": "aluno",
    "nome": "João",
    "email": "joao@example.com",
    ...
  }
}

Response 401: Token not provided or invalid
Response 404: User not found
```

#### List Students
```
GET /api/alunos
Authorization: Bearer <jwt_token>

Response 200:
{
  "sucesso": true,
  "total": 25,
  "alunos": [
    {
      "id": "uuid",
      "nome": "João Silva",
      ...
    },
    ...
  ]
}
```

#### List Drivers
```
GET /api/motoristas
Authorization: Bearer <jwt_token>

Response 200:
{
  "sucesso": true,
  "total": 8,
  "motoristas": [...]
}
```

#### Update Profile
```
PUT /api/usuarios/{usuario_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "nome": "João Updated",
  "telefone": "11987654321",
  "cidade": "São Paulo"
}

Response 200:
{
  "sucesso": true,
  "mensagem": "Perfil atualizado com sucesso",
  "usuario": {...}
}

Response 403: Cannot update other user's profile
Response 404: User not found
```

---

## 🚗 PHASE 10b: Domain Models Expansion

### New Domain Models (4 models):

**1. Veiculo (Vehicle)**
- `domain/veiculo.py` (52 lines)
- Fields: id, motorista_id, placa, modelo, ano, capacidade, ativo, criado_em, atualizado_em
- Represents school bus/vehicle

**2. Rota (Route)**
- `domain/rota.py` (56 lines)
- Fields: id, motorista_id, veiculo_id, nome, origem, destino, horario_partida, capacidade_maxima, ativa, criado_em, atualizado_em
- Represents daily school route

**3. Inscricao (Enrollment)**
- `domain/inscricao.py` (41 lines)
- Fields: id, aluno_id, rota_id, data_inscricao, ativa, criado_em, atualizado_em
- Represents student enrollment in route

**4. LocalizacaoGPS (GPS Location)**
- `domain/localizacao_gps.py` (42 lines)
- Fields: id, veiculo_id, latitude, longitude, timestamp, criado_em
- Tracks real-time vehicle GPS coordinates

### Repository Interfaces (4 interfaces):

**1. IVeiculoRepository**
- `infra/veiculo_repository_interface.py` (33 lines)
- Methods: criar, obter_por_id, obter_por_motorista, obter_por_placa, listar_todos, atualizar, deletar

**2. IRotaRepository**
- `infra/rota_repository_interface.py` (34 lines)
- Methods: criar, obter_por_id, obter_por_motorista, obter_por_veiculo, listar_ativas, atualizar, deletar

**3. IInscricaoRepository**
- `infra/inscricao_repository_interface.py` (33 lines)
- Methods: criar, obter_por_id, obter_por_aluno, obter_por_rota, obter_inscricao, atualizar, deletar

**4. ILocalizacaoGPSRepository**
- `infra/localizacao_gps_repository_interface.py` (28 lines)
- Methods: criar, obter_por_id, obter_ultima_por_veiculo, obter_historico_veiculo, deletar, limpar_historico_veiculo

### Repository Implementations (4 repositories):

**1. VeiculoRepository**
- `infra/veiculo_repository.py` (73 lines)
- CRUD operations for vehicles
- Soft delete via `ativo` flag
- Query by motorista, placa

**2. RotaRepository**
- `infra/rota_repository.py` (78 lines)
- CRUD operations for routes
- Soft delete via `ativa` flag
- Query by motorista, veiculo, or active routes

**3. InscricaoRepository**
- `infra/inscricao_repository.py` (70 lines)
- CRUD operations for enrollments
- Soft delete via `ativa` flag
- Query by aluno, rota, or specific enrollment

**4. LocalizacaoGPSRepository**
- `infra/localizacao_gps_repository.py` (81 lines)
- Insert GPS coordinates
- Query latest location by vehicle
- Query historical data with limit
- Cleanup old data (retention policy)

---

## 📊 Database Schema Extensions

The new domain models integrate with existing PostgreSQL schema:

### Veiculos Table
```sql
CREATE TABLE veiculos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    motorista_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    placa VARCHAR(20) UNIQUE NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano INTEGER NOT NULL,
    capacidade INTEGER DEFAULT 50,
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Rotas Table
```sql
CREATE TABLE rotas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    motorista_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    veiculo_id UUID REFERENCES veiculos(id) ON DELETE SET NULL,
    nome VARCHAR(100) NOT NULL,
    origem VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    horario_partida TIME NOT NULL,
    capacidade_maxima INTEGER DEFAULT 50,
    ativa BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Inscricoes Table
```sql
CREATE TABLE inscricoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    rota_id UUID NOT NULL REFERENCES rotas(id) ON DELETE CASCADE,
    data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativa BOOLEAN DEFAULT true,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aluno_id, rota_id)
);
```

### Localizacoes_GPS Table
```sql
CREATE TABLE localizacoes_gps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    veiculo_id UUID NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_veiculo_timestamp (veiculo_id, timestamp DESC)
);
```

---

## 🔒 Security Features Added

✅ **JWT Token Validation**
- Bearer token format enforcement
- Token expiry validation
- Claims extraction (usuario_id, email, tipo_perfil)

✅ **Role-Based Access Control**
- `@requer_perfil('aluno', 'motorista')` decorator
- Protects sensitive endpoints
- Returns 403 if user lacks permission

✅ **Self-Update Protection**
- PUT /api/usuarios/{id} validates request.usuario_id == id
- Prevents unauthorized profile modifications

✅ **Soft Deletes**
- `ativo` / `ativa` flags instead of hard deletes
- Maintains referential integrity
- Audit trail preservation

---

## 🏗️ Architecture Summary

```
PRESENTATION LAYER
├── routes/auth_routes.py         [POST: cadastro, login, recuperar]
├── routes/usuario_routes.py      [GET: usuarios, alunos, motoristas | PUT: usuario]
└── middleware/autenticacao.py    [JWT + role validation]

USE CASES LAYER
├── cadastrar_usuario.py          [Registration]
├── autenticar_usuario.py         [Login]
├── recuperar_senha.py            [Password recovery]
└── usuario_queries.py            [Queries: ObterUsuario, ListarPorTipo, Atualizar]

DOMAIN LAYER
├── usuario.py                    [User entity]
├── veiculo.py                    [Vehicle entity]
├── rota.py                       [Route entity]
├── inscricao.py                  [Enrollment entity]
├── localizacao_gps.py           [GPS location entity]
└── validadores.py               [Input validators]

INFRASTRUCTURE LAYER
├── usuario_repository.py         [User CRUD]
├── veiculo_repository.py         [Vehicle CRUD]
├── rota_repository.py            [Route CRUD]
├── inscricao_repository.py       [Enrollment CRUD]
├── localizacao_gps_repository.py [GPS CRUD]
└── database.py                   [Connection pooling]
```

---

## 📈 Metrics

| Aspect | Count |
|--------|-------|
| New API Endpoints | 4 (protected) |
| New Domain Models | 4 |
| New Repositories | 4 |
| New Repository Interfaces | 4 |
| New Use Cases | 3 |
| Total Files Created | 16 |
| Total Lines of Code | ~950 |
| Protected Routes | 4 |
| Database Tables Extended | 4 |

---

## 🚀 Deployment Checklist

- [x] Protected routes with JWT verification
- [x] Role-based access control implemented
- [x] 4 domain models created
- [x] 4 repositories fully implemented
- [x] Soft delete pattern applied
- [x] GPS tracking ready
- [x] Self-update protection
- [x] API blueprints registered in app
- [x] Exception handling consistent
- [x] Type hints throughout

---

## 🔄 Integration with Frontend

Frontend can now:

1. **Get user profile after login**
   - Send Authorization header: `Authorization: Bearer <token>`
   - GET /api/usuarios/{usuario_id}

2. **View list of students/drivers**
   - GET /api/alunos (for driver apps)
   - GET /api/motoristas (for admin/student apps)

3. **Update own profile**
   - PUT /api/usuarios/{usuario_id}
   - Update nome, sobrenome, telefone, cidade

---

## 📝 Next Steps (Phase 11+)

1. **CRUD Routes for Rotas/Veículos/Inscrições**
   - POST /api/rotas, GET /api/rotas/{id}, PUT, DELETE
   - Similar for vehicles, enrollments, GPS

2. **GPS Tracking Real-time**
   - WebSocket for live GPS updates
   - Endpoint for GPS data submission from mobile app

3. **Validation Rules**
   - Vehicle plate validation
   - Route time validation
   - Enrollment capacity checks

4. **API Documentation**
   - Swagger/OpenAPI integration

---

## ✅ Status: Phase 10 COMPLETE

🟢 **All protected routes implemented**
🟢 **4 domain models fully defined**
🟢 **4 repositories production-ready**
🟢 **JWT + Role-based authentication working**
🟢 **Soft delete pattern applied**
🟢 **Database schema ready (existing from Phase 9)**

Ready for Phase 11: CRUD operations & real-time GPS tracking.
