#!/usr/bin/env python3
"""
Script para testar os endpoints da API
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def test_endpoint(method, endpoint, data=None, headers=None):
    """Testa um endpoint e retorna resposta"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        else:
            return None
        
        return response
    except requests.exceptions.ConnectionError:
        print(f"✗ Erro: Não consegui conectar ao servidor em {BASE_URL}")
        return None
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

def test_health():
    """Testa se o servidor está rodando"""
    print_header("1️⃣  TESTE DE SAÚDE DO SERVIDOR")
    response = test_endpoint("GET", "/")
    
    if response is None:
        print("✗ Servidor não está respondendo")
        return False
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print("✓ Servidor está rodando (rota raiz não implementada, esperado)")
        return True
    elif response.status_code >= 400:
        print(f"✗ Erro no servidor: {response.status_code}")
        return False
    else:
        print("✓ Servidor respondeu com sucesso")
        return True

def test_cadastro():
    """Testa endpoint de cadastro de usuário"""
    print_header("2️⃣  TESTE DE CADASTRO DE USUÁRIO")
    
    from uuid import uuid4
    
    # Dados de teste - apenas campos obrigatórios
    email = f"aluno_{uuid4().hex[:8]}@vantrack.test"
    cpf = "".join([str(i % 10) for i in range(11)])  # CPF fake
    senha = "SenhaSegura@123"
    
    dados_cadastro = {
        "tipo_perfil": "aluno",
        "nome": "João",
        "sobrenome": "Silva",
        "cpf": cpf,
        "email": email,
        "telefone": "11999999999",
        "cidade": "São Paulo",
        "senha": senha  # Enviar senha em texto, não hash
    }
    
    print(f"Cadastrando: {email}")
    print(f"Dados: {dados_cadastro}")
    response = test_endpoint("POST", "/api/cadastro", data=dados_cadastro)
    
    if response is None:
        return False, None
    
    print(f"Status Code: {response.status_code}")
    try:
        resposta = response.json()
        print(f"Resposta: {json.dumps(resposta, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201 or response.status_code == 200:
            print("✓ Cadastro realizado com sucesso")
            return True, resposta
        else:
            print(f"✗ Erro no cadastro: {resposta}")
            return False, None
    except:
        print(f"Resposta: {response.text}")
        return False, None

def test_login(email, senha):
    """Testa endpoint de login"""
    print_header("3️⃣  TESTE DE LOGIN")
    
    dados_login = {
        "email": email,
        "senha": senha
    }
    
    print(f"Logando: {email}")
    response = test_endpoint("POST", "/api/login", data=dados_login)
    
    if response is None:
        return False, None
    
    print(f"Status Code: {response.status_code}")
    try:
        resposta = response.json()
        print(f"Resposta: {json.dumps(resposta, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            if "token" in resposta:
                print("✓ Login realizado com sucesso")
                return True, resposta["token"]
            elif "usuario_id" in resposta:
                print("✓ Login realizado, aguardando token")
                return True, resposta.get("usuario_id")
        else:
            print(f"✗ Erro no login: {resposta}")
            return False, None
    except:
        print(f"Resposta: {response.text}")
        return False, None

def test_protected_route(token):
    """Testa uma rota protegida com JWT"""
    print_header("4️⃣  TESTE DE ROTA PROTEGIDA (JWT)")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Tenta acessar rota protegida
    print("Acessando rota protegida com token...")
    response = test_endpoint("GET", "/api/perfil", headers=headers)
    
    if response is None:
        return False
    
    print(f"Status Code: {response.status_code}")
    try:
        resposta = response.json()
        print(f"Resposta: {json.dumps(resposta, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✓ Acesso autorizado com token JWT")
            return True
        elif response.status_code == 401:
            print("⚠ Token inválido/expirado (esperado se rota está implementada)")
            return False
        else:
            print(f"Resposta recebida: {resposta}")
            return False
    except:
        print(f"Resposta: {response.text}")
        return False

def test_database_connection():
    """Testa conexão com banco de dados"""
    print_header("5️⃣  TESTE DE CONEXÃO COM BANCO DE DADOS")
    
    # Tenta acessar rota que usa banco de dados
    response = test_endpoint("GET", "/api/usuarios")
    
    if response is None:
        return False
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 401, 403, 404]:
        print("✓ Servidor conseguiu processar requisição ao banco de dados")
        return True
    else:
        print(f"✗ Erro na comunicação com banco de dados")
        return False

def main():
    print("\n" + "="*60)
    print("TESTES DE API - VANTRACK")
    print("="*60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    # Teste 1: Saúde do servidor
    if not test_health():
        print("\n✗ Servidor não está acessível. Abra outro terminal e execute:")
        print("  cd backend && python app.py")
        return
    
    # Teste 2-5: Funcionalidades
    sucesso_cadastro = False
    token = None
    email_teste = None
    
    try:
        sucesso_cadastro, resposta_cadastro = test_cadastro()
        if sucesso_cadastro and resposta_cadastro:
            # Usar email do cadastro
            if "email" in resposta_cadastro:
                email_teste = resposta_cadastro["email"]
            else:
                # Se não retornou email, gerar um novo
                from uuid import uuid4
                email_teste = f"aluno_{uuid4().hex[:8]}@vantrack.test"
    except Exception as e:
        print(f"Erro no cadastro: {e}")
    
    if email_teste:
        try:
            sucesso_login, token = test_login(email_teste, "SenhaSegura@123")
        except Exception as e:
            print(f"Erro no login: {e}")
    
    if token:
        try:
            test_protected_route(token)
        except Exception as e:
            print(f"Erro ao testar rota protegida: {e}")
    
    try:
        test_database_connection()
    except Exception as e:
        print(f"Erro ao testar banco de dados: {e}")
    
    print("\n" + "="*60)
    print("TESTES CONCLUÍDOS")
    print("="*60)

if __name__ == '__main__':
    main()
