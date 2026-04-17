#!/usr/bin/env python3
"""
Script para debug do erro de cadastro
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv('.env')

from database import Database
from infra.usuario_repository import UsuarioRepository
from use_cases.autenticar_usuario import CadastrarUsuario
from domain.usuario import UsuarioCreate

db = Database()

print("=" * 60)
print("DEBUG DE CADASTRO")
print("=" * 60)

try:
    # Dados de teste
    from uuid import uuid4
    
    dados = {
        "tipo_perfil": "aluno",
        "nome": "João",
        "sobrenome": "Silva",
        "cpf": f"00000000{str(uuid4().int % 1000).zfill(3)}",
        "email": f"test_{uuid4().hex[:8]}@test.com",
        "telefone": "11999999999",
        "cidade": "São Paulo",
        "senha": "SenhaSegura@123"
    }
    
    print(f"\n1. Criando UsuarioCreate com dados:")
    for k, v in dados.items():
        print(f"   {k}: {v}")
    
    usuario_create = UsuarioCreate(**dados)
    print(f"✓ UsuarioCreate criado: {usuario_create}")
    
    print(f"\n2. Criando repositório...")
    usuario_repo = UsuarioRepository(db)
    print(f"✓ Repositório criado")
    
    print(f"\n3. Criando use case de cadastro...")
    cadastrar_use_case = CadastrarUsuario(usuario_repo)
    print(f"✓ Use case criado")
    
    print(f"\n4. Executando cadastro...")
    resultado = cadastrar_use_case.executar(usuario_create)
    
    print(f"✓ Cadastro bem-sucedido!")
    print(f"Resultado: {resultado}")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERRO: {e}")
    print(f"\nTraceback:")
    traceback.print_exc()

print("\n" + "=" * 60)
