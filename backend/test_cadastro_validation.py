#!/usr/bin/env python3
"""
Script de teste para validar a correção de campos vazios no cadastro
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_test(test_name, status):
    icon = "✓" if status else "✗"
    print(f"  [{icon}] {test_name}")

def test_empty_fields():
    """Testa cadastro com campos vazios"""
    print_header("TESTE 1: CADASTRO COM CAMPOS VAZIOS")
    
    print("\n  Enviando payload com campos vazios...")
    
    # Teste 1: Nome vazio
    payload = {
        "nome": "",
        "cpf": "12345678901",
        "email": "teste@example.com",
        "telefone": "11987654321",
        "cidade": "São Paulo",
        "tipo_perfil": "aluno",
        "senha": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Teste: Nome vazio")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 400 and "campos obrigatórios estão vazios" in response.json().get("erro", "").lower():
        print_test("Nome vazio rejeitado com mensagem adequada", True)
    else:
        print_test("Nome vazio rejeitado com mensagem adequada", False)
    
    # Teste 2: Email vazio
    payload = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "",
        "telefone": "11987654321",
        "cidade": "São Paulo",
        "tipo_perfil": "aluno",
        "senha": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Teste: Email vazio")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 400 and "campos obrigatórios estão vazios" in response.json().get("erro", "").lower():
        print_test("Email vazio rejeitado com mensagem adequada", True)
    else:
        print_test("Email vazio rejeitado com mensagem adequada", False)
    
    # Teste 3: CPF vazio
    payload = {
        "nome": "João Silva",
        "cpf": "",
        "email": "joao@example.com",
        "telefone": "11987654321",
        "cidade": "São Paulo",
        "tipo_perfil": "aluno",
        "senha": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Teste: CPF vazio")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 400 and "campos obrigatórios estão vazios" in response.json().get("erro", "").lower():
        print_test("CPF vazio rejeitado com mensagem adequada", True)
    else:
        print_test("CPF vazio rejeitado com mensagem adequada", False)
    
    # Teste 4: Todos vazios
    payload = {
        "nome": "",
        "cpf": "",
        "email": "",
        "telefone": "",
        "cidade": "",
        "tipo_perfil": "",
        "senha": ""
    }
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Teste: Todos os campos vazios")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 400 and "campos obrigatórios estão vazios" in response.json().get("erro", "").lower():
        print_test("Todos vazios rejeitado com mensagem adequada", True)
    else:
        print_test("Todos vazios rejeitado com mensagem adequada", False)

def test_valid_cadastro():
    """Testa cadastro com dados válidos"""
    print_header("TESTE 2: CADASTRO COM DADOS VÁLIDOS")
    
    timestamp = int(time.time())
    
    payload = {
        "nome": f"Teste Valido {timestamp}",
        "cpf": f"{timestamp % 100000000000:011d}",
        "email": f"teste{timestamp}@example.com",
        "telefone": "11987654321",
        "cidade": "São Paulo",
        "tipo_perfil": "aluno",
        "senha": "senha123"
    }
    
    print(f"\n  Enviando dados válidos:")
    print(f"  Nome: {payload['nome']}")
    print(f"  CPF: {payload['cpf']}")
    print(f"  Email: {payload['email']}")
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Status Code: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code in [200, 201]:
        print_test("Cadastro válido aceito", True)
    else:
        print_test("Cadastro válido aceito", False)

def test_invalid_cpf_length():
    """Testa cadastro com CPF muito curto"""
    print_header("TESTE 3: CADASTRO COM CPF INVÁLIDO (MUITO CURTO)")
    
    payload = {
        "nome": "João Silva",
        "cpf": "123",  # Muito curto
        "email": "joao@example.com",
        "telefone": "11987654321",
        "cidade": "São Paulo",
        "tipo_perfil": "aluno",
        "senha": "senha123"
    }
    
    print(f"\n  CPF: {payload['cpf']} (apenas 3 dígitos)")
    
    response = requests.post(f"{BASE_URL}/cadastro", json=payload)
    print(f"\n  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code == 400 and "dígitos" in response.json().get("erro", "").lower():
        print_test("CPF curto rejeitado com mensagem adequada", True)
    else:
        print_test("CPF curto rejeitado com mensagem adequada", False)

def main():
    print("\n")
    print("#" * 80)
    print("# TESTES DE VALIDAÇÃO DE CADASTRO - VANTRACK")
    print("#" * 80)
    print(f"# Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"# Base URL: {BASE_URL}")
    print("#" * 80)
    
    try:
        # Teste de conexão
        print("\n  Verificando conexão com o backend...")
        response = requests.get(f"{BASE_URL}/cadastro", timeout=5)
        print("  ✓ Backend está respondendo")
    except Exception as e:
        print(f"  ✗ Erro ao conectar ao backend: {e}")
        print(f"  Certifique-se de que o servidor está rodando em {BASE_URL}")
        return
    
    try:
        test_empty_fields()
        test_invalid_cpf_length()
        test_valid_cadastro()
    except Exception as e:
        print(f"\n✗ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("  TESTES CONCLUÍDOS")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
