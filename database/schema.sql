CREATE TABLE usuarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tipo_perfil VARCHAR(20) NOT NULL CHECK (tipo_perfil IN ('aluno', 'motorista')),
  nome VARCHAR(100) NOT NULL,
  sobrenome VARCHAR(100) NOT NULL,
  cpf VARCHAR(11) UNIQUE NOT NULL,
  email VARCHAR(254) UNIQUE NOT NULL,
  telefone VARCHAR(11) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  senha_hash VARCHAR(255) NOT NULL,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT cpf_length CHECK (LENGTH(cpf) = 11),
  CONSTRAINT telefone_length CHECK (LENGTH(telefone) = 11),
  CONSTRAINT email_length CHECK (LENGTH(email) <= 254)
);

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_cpf ON usuarios(cpf);
CREATE INDEX idx_usuarios_tipo_perfil ON usuarios(tipo_perfil);

CREATE TABLE sessoes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) UNIQUE NOT NULL,
  ip_address INET,
  user_agent VARCHAR(500),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expira_em TIMESTAMP NOT NULL,
  revogado_em TIMESTAMP
);

CREATE INDEX idx_sessoes_usuario_id ON sessoes(usuario_id);
CREATE INDEX idx_sessoes_token_hash ON sessoes(token_hash);

CREATE TABLE veiculos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  motorista_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  placa VARCHAR(8) UNIQUE NOT NULL,
  modelo VARCHAR(100) NOT NULL,
  ano INT NOT NULL,
  capacidade_passageiros INT NOT NULL CHECK (capacidade_passageiros > 0),
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT motorista_deve_ser_motorista CHECK (EXISTS(SELECT 1 FROM usuarios WHERE id = motorista_id AND tipo_perfil = 'motorista'))
);

CREATE INDEX idx_veiculos_motorista_id ON veiculos(motorista_id);
CREATE INDEX idx_veiculos_placa ON veiculos(placa);

CREATE TABLE rotas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  motorista_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  veiculo_id UUID REFERENCES veiculos(id) ON DELETE SET NULL,
  titulo VARCHAR(255) NOT NULL,
  local_saida VARCHAR(255) NOT NULL,
  local_chegada VARCHAR(255) NOT NULL,
  horario_saida TIME NOT NULL,
  horario_chegada TIME,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rotas_motorista_id ON rotas(motorista_id);
CREATE INDEX idx_rotas_veiculo_id ON rotas(veiculo_id);

CREATE TABLE inscricoes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aluno_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  rota_id UUID NOT NULL REFERENCES rotas(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa', 'pausada', 'cancelada')),
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(aluno_id, rota_id),
  CONSTRAINT aluno_deve_ser_aluno CHECK (EXISTS(SELECT 1 FROM usuarios WHERE id = aluno_id AND tipo_perfil = 'aluno'))
);

CREATE INDEX idx_inscricoes_aluno_id ON inscricoes(aluno_id);
CREATE INDEX idx_inscricoes_rota_id ON inscricoes(rota_id);

CREATE TABLE localizacoes_gps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  veiculo_id UUID NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
  latitude NUMERIC(10, 8) NOT NULL,
  longitude NUMERIC(11, 8) NOT NULL,
  velocidade NUMERIC(6, 2),
  direcao NUMERIC(3, 0),
  precisao NUMERIC(6, 2),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_localizacoes_veiculo_id ON localizacoes_gps(veiculo_id);
CREATE INDEX idx_localizacoes_timestamp ON localizacoes_gps(timestamp);

CREATE TABLE enderecos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aluno_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  rota_id UUID NOT NULL REFERENCES rotas(id) ON DELETE CASCADE,
  endereco_coleta VARCHAR(500) NOT NULL,
  endereco_entrega VARCHAR(500) NOT NULL,
  latitude_coleta NUMERIC(10, 8),
  longitude_coleta NUMERIC(11, 8),
  latitude_entrega NUMERIC(10, 8),
  longitude_entrega NUMERIC(11, 8),
  principal BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_enderecos_aluno_id ON enderecos(aluno_id);
CREATE INDEX idx_enderecos_rota_id ON enderecos(rota_id);

CREATE TABLE presenca_diaria (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aluno_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  rota_id UUID NOT NULL REFERENCES rotas(id) ON DELETE CASCADE,
  data DATE NOT NULL,
  vai_embarcar BOOLEAN NOT NULL DEFAULT true,
  confirmado_em TIMESTAMP,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(aluno_id, rota_id, data)
);

CREATE INDEX idx_presenca_diaria_aluno_id ON presenca_diaria(aluno_id);
CREATE INDEX idx_presenca_diaria_rota_id ON presenca_diaria(rota_id);
CREATE INDEX idx_presenca_diaria_data ON presenca_diaria(data);

CREATE TABLE mensagens_chat (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  remetente_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  destinatario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  texto TEXT NOT NULL,
  lido BOOLEAN DEFAULT false,
  lido_em TIMESTAMP,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mensagens_chat_remetente_id ON mensagens_chat(remetente_id);
CREATE INDEX idx_mensagens_chat_destinatario_id ON mensagens_chat(destinatario_id);
CREATE INDEX idx_mensagens_chat_criado_em ON mensagens_chat(criado_em);

CREATE TABLE dois_fatores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  dispositivo_hash VARCHAR(255) NOT NULL,
  codigo_2fa VARCHAR(6) NOT NULL,
  metodo VARCHAR(10) NOT NULL CHECK (metodo IN ('SMS', 'EMAIL')),
  telefone_sms VARCHAR(11),
  email_envio VARCHAR(254),
  verificado BOOLEAN DEFAULT false,
  tentativas_restantes INT DEFAULT 3,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expira_em TIMESTAMP NOT NULL,
  verificado_em TIMESTAMP
);

CREATE INDEX idx_dois_fatores_usuario_id ON dois_fatores(usuario_id);
CREATE INDEX idx_dois_fatores_dispositivo_hash ON dois_fatores(dispositivo_hash);
CREATE INDEX idx_dois_fatores_expira_em ON dois_fatores(expira_em);
