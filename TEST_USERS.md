#!/usr/bin/env python3
# Script para gerar credenciais de teste

print('=' * 70)
print('CREDENCIAIS DE TESTE - VANTRACK')
print('=' * 70)
print()

print('🔑 MOTORISTA:')
print('  Email: motorista@teste.com')
print('  Senha: 123456')
print()

print('🔑 ALUNO:')
print('  Email: aluno@teste.com')
print('  Senha: 123456')
print()

print('=' * 70)
print('INSTRUÇÕES PARA INSERIR NO BANCO:')
print('=' * 70)
print()

print('1. Abra DBeaver ou psql')
print('2. Conecte ao banco "vantrack"')
print('3. Execute o SQL abaixo:')
print()

print("""-- Motorista de teste (CPF: 12345678901)
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES (
    'motorista',
    'João',
    'Silva',
    '12345678901',
    'motorista@teste.com',
    '11987654321',
    'São Paulo',
    '$2b$12$ABC123DEF456GHI789JKL01234567890123456MOTORISTA'
);

-- Aluno de teste (CPF: 98765432101)
INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
VALUES (
    'aluno',
    'Maria',
    'Santos',
    '98765432101',
    'aluno@teste.com',
    '11912345678',
    'São Paulo',
    '$2b$12$ABC123DEF456GHI789JKL01234567890123456ALUNO12'
);

-- Verificar:
SELECT id, tipo_perfil, nome, email FROM usuarios 
WHERE email IN ('motorista@teste.com', 'aluno@teste.com');
""")

print()
print('⚠️  NOTA: A senha hash acima é apenas um placeholder.')
print('    A API usará bcrypt para hashear senhas automaticamente.')
print()
print('=' * 70)
print()

# Alternativa: usar a rota de cadastro
print('ALTERNATIVA - Usar API de CADASTRO:')
print()
print('POST http://localhost:5000/api/cadastro')
print('{')
print('  "email": "motorista@teste.com",')
print('  "senha": "123456",')
print('  "cpf": "12345678901",')
print('  "nome": "João",')
print('  "sobrenome": "Silva",')
print('  "telefone": "11987654321",')
print('  "cidade": "São Paulo",')
print('  "tipo_perfil": "motorista"')
print('}')
print()
print('POST http://localhost:5000/api/cadastro')
print('{')
print('  "email": "aluno@teste.com",')
print('  "senha": "123456",')
print('  "cpf": "98765432101",')
print('  "nome": "Maria",')
print('  "sobrenome": "Santos",')
print('  "telefone": "11912345678",')
print('  "cidade": "São Paulo",')
print('  "tipo_perfil": "aluno"')
print('}')
