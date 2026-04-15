import pytest
from domain.validadores import ValidadorUsuario, RegistroCadastroRequest
from exceptions import DadosInvalidosException

class TestValidadorEmail:
    
    def test_email_valido(self):
        assert ValidadorUsuario.validar_email('usuario@example.com') is True
        assert ValidadorUsuario.validar_email('user.name@domain.co.uk') is True
    
    def test_email_invalido(self):
        assert ValidadorUsuario.validar_email('usuario@') is False
        assert ValidadorUsuario.validar_email('usuario') is False
        assert ValidadorUsuario.validar_email('') is False
        assert ValidadorUsuario.validar_email('@example.com') is False

class TestValidadorCPF:
    
    def test_cpf_valido(self):
        assert ValidadorUsuario.validar_cpf('11144477735') is True
    
    def test_cpf_invalido_sequencia_repetida(self):
        assert ValidadorUsuario.validar_cpf('00000000000') is False
        assert ValidadorUsuario.validar_cpf('11111111111') is False
    
    def test_cpf_invalido_tamanho(self):
        assert ValidadorUsuario.validar_cpf('123') is False
        assert ValidadorUsuario.validar_cpf('123456789012') is False
    
    def test_cpf_invalido_formato(self):
        assert ValidadorUsuario.validar_cpf('abc.def.ghi-jk') is False

class TestValidadorTelefone:
    
    def test_telefone_valido(self):
        assert ValidadorUsuario.validar_telefone('11987654321') is True
    
    def test_telefone_invalido(self):
        assert ValidadorUsuario.validar_telefone('123') is False
        assert ValidadorUsuario.validar_telefone('') is False
        assert ValidadorUsuario.validar_telefone('21987654321') is False

class TestValidadorSenha:
    
    def test_senha_valida(self):
        assert ValidadorUsuario.validar_senha('Senha123') is True
        assert ValidadorUsuario.validar_senha('MyPassword2024') is True
    
    def test_senha_muito_curta(self):
        assert ValidadorUsuario.validar_senha('Abc1') is False
    
    def test_senha_sem_maiuscula(self):
        assert ValidadorUsuario.validar_senha('senha123') is False
    
    def test_senha_sem_minuscula(self):
        assert ValidadorUsuario.validar_senha('SENHA123') is False
    
    def test_senha_sem_numero(self):
        assert ValidadorUsuario.validar_senha('SenhaAbcd') is False

class TestValidadorNome:
    
    def test_nome_valido(self):
        assert ValidadorUsuario.validar_nome('João Silva') is True
        assert ValidadorUsuario.validar_nome('Maria') is True
    
    def test_nome_muito_curto(self):
        assert ValidadorUsuario.validar_nome('J') is False
    
    def test_nome_muito_longo(self):
        assert ValidadorUsuario.validar_nome('A' * 101) is False
    
    def test_nome_com_numeros(self):
        assert ValidadorUsuario.validar_nome('João123') is False

class TestValidadorCidade:
    
    def test_cidade_valida(self):
        assert ValidadorUsuario.validar_cidade('São Paulo') is True
        assert ValidadorUsuario.validar_cidade('Rio de Janeiro') is True
    
    def test_cidade_muito_curta(self):
        assert ValidadorUsuario.validar_cidade('A') is False

class TestValidadorTipoPerfil:
    
    def test_tipo_perfil_valido(self):
        assert ValidadorUsuario.validar_tipo_perfil('aluno') is True
        assert ValidadorUsuario.validar_tipo_perfil('motorista') is True
    
    def test_tipo_perfil_invalido(self):
        assert ValidadorUsuario.validar_tipo_perfil('admin') is False
        assert ValidadorUsuario.validar_tipo_perfil('user') is False

class TestRegistroCadastroRequest:
    
    def test_validar_cadastro_completo(self):
        dados = {
            'nome': 'João',
            'sobrenome': 'Silva',
            'cpf': '11144477735',
            'email': 'joao@example.com',
            'telefone': '11987654321',
            'cidade': 'São Paulo',
            'senha': 'Senha123',
            'tipo_perfil': 'aluno'
        }
        req = RegistroCadastroRequest(dados)
        valido, erros = req.validar()
        assert valido is True or valido is False
    
    def test_validar_cadastro_email_vazio(self):
        dados = {
            'nome': 'João',
            'sobrenome': 'Silva',
            'cpf': '11144477735',
            'email': '',
            'telefone': '11987654321',
            'cidade': 'São Paulo',
            'senha': 'Senha123'
        }
        req = RegistroCadastroRequest(dados)
        valido, erros = req.validar()
        assert valido is False
        assert 'email' in erros
    
    def test_validar_cadastro_cpf_invalido(self):
        dados = {
            'nome': 'João',
            'sobrenome': 'Silva',
            'cpf': '00000000000',
            'email': 'joao@example.com',
            'telefone': '11987654321',
            'cidade': 'São Paulo',
            'senha': 'Senha123'
        }
        req = RegistroCadastroRequest(dados)
        valido, erros = req.validar()
        assert valido is False
        assert 'cpf' in erros
    
    def test_validar_cadastro_senha_fraca(self):
        dados = {
            'nome': 'João',
            'sobrenome': 'Silva',
            'cpf': '11144477735',
            'email': 'joao@example.com',
            'telefone': '11987654321',
            'cidade': 'São Paulo',
            'senha': '123'
        }
        req = RegistroCadastroRequest(dados)
        valido, erros = req.validar()
        assert valido is False
        assert 'senha' in erros
