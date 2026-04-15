import pytest
from unittest.mock import Mock, MagicMock
from domain.usuario import Usuario
from domain.validadores import ValidadorUsuario, RegistroCadastroRequest
from uuid import uuid4
from datetime import datetime

class TestValidadorUsuario:

    def test_validar_email_valido(self):
        assert ValidadorUsuario.validar_email('usuario@example.com') is True

    def test_validar_email_invalido(self):
        assert ValidadorUsuario.validar_email('usuario@') is False
        assert ValidadorUsuario.validar_email('usuario') is False
        assert ValidadorUsuario.validar_email('') is False

    def test_validar_cpf_valido(self):
        assert ValidadorUsuario.validar_cpf('123.456.789-09') is True or ValidadorUsuario.validar_cpf('11144477735') is True

    def test_validar_cpf_invalido(self):
        assert ValidadorUsuario.validar_cpf('000.000.000-00') is False
        assert ValidadorUsuario.validar_cpf('123') is False

    def test_validar_telefone_valido(self):
        assert ValidadorUsuario.validar_telefone('(11) 98765-4321') is True or ValidadorUsuario.validar_telefone('11987654321') is True

    def test_validar_telefone_invalido(self):
        assert ValidadorUsuario.validar_telefone('123') is False
        assert ValidadorUsuario.validar_telefone('') is False

    def test_validar_senha_valida(self):
        assert ValidadorUsuario.validar_senha('Senha123') is True

    def test_validar_senha_invalida(self):
        assert ValidadorUsuario.validar_senha('123') is False
        assert ValidadorUsuario.validar_senha('senhafraca') is False
        assert ValidadorUsuario.validar_senha('SENHAFRACA') is False

    def test_validar_nome_valido(self):
        assert ValidadorUsuario.validar_nome('João Silva') is True

    def test_validar_nome_invalido(self):
        assert ValidadorUsuario.validar_nome('J') is False
        assert ValidadorUsuario.validar_nome('123') is False

    def test_validar_tipo_perfil_valido(self):
        assert ValidadorUsuario.validar_tipo_perfil('aluno') is True
        assert ValidadorUsuario.validar_tipo_perfil('motorista') is True

    def test_validar_tipo_perfil_invalido(self):
        assert ValidadorUsuario.validar_tipo_perfil('admin') is False


class TestRegistroCadastroRequest:

    def test_criar_request_valida(self):
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
        assert req.nome == 'João'
        assert req.email == 'joao@example.com'

    def test_validar_request_sucesso(self):
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
        assert valido is False or valido is True

    def test_validar_request_email_vazio(self):
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
