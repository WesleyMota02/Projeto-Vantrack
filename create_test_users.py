#!/usr/bin/env python
# Script para criar usuários de teste

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import bcrypt
from datetime import datetime

# Gerar hash de senhas
senha_teste = '123456'
senha_hash = bcrypt.hashpw(senha_teste.encode(), bcrypt.gensalt()).decode()

print('=' * 60)
print('CREDENCIAIS DE TESTE - VANTRACK')
print('=' * 60)
print()

print('🔑 MOTORISTA:')
print(f'  Email: motorista@teste.com')
print(f'  Senha: {senha_teste}')
print()

print('🔑 ALUNO:')
print(f'  Email: aluno@teste.com')
print(f'  Senha: {senha_teste}')
print()

print('=' * 60)
print('SQL PARA EXECUTAR NO BANCO:')
print('=' * 60)
print()

sql = f"""-- Limpar usuários de teste anteriores (opcional)
DELETE FROM usuarios WHERE email IN ('motorista@teste.com', 'aluno@teste.com');

-- Motorista de teste
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES ('motorista', 'João', 'Silva', '12345678901', 'motorista@teste.com', '11987654321', 'São Paulo', '{senha_hash}');

-- Aluno de teste
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES ('aluno', 'Maria', 'Santos', '98765432101', 'aluno@teste.com', '11912345678', 'São Paulo', '{senha_hash}');

-- Verificar inserção
SELECT id, tipo_perfil, nome, email FROM usuarios WHERE email IN ('motorista@teste.com', 'aluno@teste.com');
"""

print(sql)
print()
print('=' * 60)
print('⚠️  COPIE E EXECUTE NO psql OU DBeaver')
print('=' * 60)
