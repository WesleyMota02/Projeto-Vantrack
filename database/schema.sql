CREATE TABLE usuarios (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  tipo_perfil ENUM('aluno', 'motorista') NOT NULL,
  nome VARCHAR(100) NOT NULL,
  sobrenome VARCHAR(100) NOT NULL,
  cpf VARCHAR(11) UNIQUE NOT NULL,
  email VARCHAR(254) UNIQUE NOT NULL,
  telefone VARCHAR(11) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  senha_hash VARCHAR(255) NOT NULL,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_usuarios_email (email),
  INDEX idx_usuarios_cpf (cpf),
  INDEX idx_usuarios_tipo_perfil (tipo_perfil)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sessoes (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  usuario_id CHAR(36) NOT NULL,
  token_hash VARCHAR(255) UNIQUE NOT NULL,
  ip_address VARCHAR(45),
  user_agent VARCHAR(500),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expira_em TIMESTAMP NOT NULL,
  revogado_em TIMESTAMP NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  INDEX idx_sessoes_usuario_id (usuario_id),
  INDEX idx_sessoes_token_hash (token_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE veiculos (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  motorista_id CHAR(36) NOT NULL,
  placa VARCHAR(8) UNIQUE NOT NULL,
  modelo VARCHAR(100) NOT NULL,
  ano INT NOT NULL,
  capacidade_passageiros INT NOT NULL,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (motorista_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  INDEX idx_veiculos_motorista_id (motorista_id),
  INDEX idx_veiculos_placa (placa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE rotas (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  motorista_id CHAR(36) NOT NULL,
  veiculo_id CHAR(36) NULL,
  titulo VARCHAR(255) NOT NULL,
  local_saida VARCHAR(255) NOT NULL,
  local_chegada VARCHAR(255) NOT NULL,
  horario_saida TIME NOT NULL,
  horario_chegada TIME NULL,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (motorista_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE SET NULL,
  INDEX idx_rotas_motorista_id (motorista_id),
  INDEX idx_rotas_veiculo_id (veiculo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE inscricoes (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  aluno_id CHAR(36) NOT NULL,
  rota_id CHAR(36) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'ativa',
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (aluno_id, rota_id),
  FOREIGN KEY (aluno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
  INDEX idx_inscricoes_aluno_id (aluno_id),
  INDEX idx_inscricoes_rota_id (rota_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE localizacoes_gps (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  veiculo_id CHAR(36) NOT NULL,
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,
  velocidade DECIMAL(6, 2) NULL,
  direcao DECIMAL(3, 0) NULL,
  precisao DECIMAL(6, 2) NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE,
  INDEX idx_localizacoes_veiculo_id (veiculo_id),
  INDEX idx_localizacoes_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE enderecos (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  aluno_id CHAR(36) NOT NULL,
  rota_id CHAR(36) NOT NULL,
  endereco_coleta VARCHAR(500) NOT NULL,
  endereco_entrega VARCHAR(500) NOT NULL,
  latitude_coleta DECIMAL(10, 8) NULL,
  longitude_coleta DECIMAL(11, 8) NULL,
  latitude_entrega DECIMAL(10, 8) NULL,
  longitude_entrega DECIMAL(11, 8) NULL,
  principal BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (aluno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
  INDEX idx_enderecos_aluno_id (aluno_id),
  INDEX idx_enderecos_rota_id (rota_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE presenca_diaria (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  aluno_id CHAR(36) NOT NULL,
  rota_id CHAR(36) NOT NULL,
  data DATE NOT NULL,
  vai_embarcar BOOLEAN NOT NULL DEFAULT true,
  confirmado_em TIMESTAMP NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE (aluno_id, rota_id, data),
  FOREIGN KEY (aluno_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
  INDEX idx_presenca_diaria_aluno_id (aluno_id),
  INDEX idx_presenca_diaria_rota_id (rota_id),
  INDEX idx_presenca_diaria_data (data)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE mensagens_chat (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  remetente_id CHAR(36) NOT NULL,
  destinatario_id CHAR(36) NOT NULL,
  texto TEXT NOT NULL,
  lido BOOLEAN DEFAULT false,
  lido_em TIMESTAMP NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (remetente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (destinatario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  INDEX idx_mensagens_chat_remetente_id (remetente_id),
  INDEX idx_mensagens_chat_destinatario_id (destinatario_id),
  INDEX idx_mensagens_chat_criado_em (criado_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dois_fatores (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  usuario_id CHAR(36) NOT NULL,
  dispositivo_hash VARCHAR(255) NOT NULL,
  codigo_2fa VARCHAR(6) NOT NULL,
  metodo ENUM('SMS', 'EMAIL') NOT NULL,
  telefone_sms VARCHAR(11) NULL,
  email_envio VARCHAR(254) NULL,
  verificado BOOLEAN DEFAULT false,
  tentativas_restantes INT DEFAULT 3,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expira_em TIMESTAMP NOT NULL,
  verificado_em TIMESTAMP NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  INDEX idx_dois_fatores_usuario_id (usuario_id),
  INDEX idx_dois_fatores_dispositivo_hash (dispositivo_hash),
  INDEX idx_dois_fatores_expira_em (expira_em)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
