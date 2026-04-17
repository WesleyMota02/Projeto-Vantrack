#!/usr/bin/env python3
"""
Script para verificar dados diretos no banco
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv('.env')

from database import Database

db = Database()

print("=" * 60)
print("VERIFICANDO DADOS NO BANCO")
print("=" * 60)

try:
    # Ver últimos usuários criados
    print("\n1. Últimos 5 usuários no banco:")
    query = "SELECT id, email, nome, tipo_perfil, ativo FROM usuarios ORDER BY criado_em DESC LIMIT 5"
    usuarios = db.execute_query(query, fetch=True)
    
    if usuarios:
        for usr in usuarios:
            print(f"  • {usr['email']} - {usr['id']} - ativo={usr['ativo']}")
    else:
        print("  (Nenhum usuário encontrado)")
    
    # Teste de SELECT com ativo=TRUE
    print("\n2. Testando SELECT com ativo=TRUE:")
    query2 = "SELECT COUNT(*) as total FROM usuarios WHERE ativo = TRUE"
    result = db.execute_query_one(query2)
    print(f"  Total de usuários ativos: {result}")
    
    print("\n✓ Verificação concluída")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERRO: {e}")
    traceback.print_exc()

print("=" * 60)
