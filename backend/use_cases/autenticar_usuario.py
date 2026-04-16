import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from exceptions import SenhaInvalida, UsuarioNaoEncontrado, EmailJaCadastrado, CPFJaCadastrado
from domain.usuario import UsuarioCreate, Usuario

class AutenticarUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def executar(self, email, senha):
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontrado(f"Usuário com email {email} não encontrado")
        
        if not bcrypt.checkpw(senha.encode(), usuario['senha_hash'].encode()):
            raise SenhaInvalida("Senha incorreta")
        
        # Gerar JWT
        payload = {
            'usuario_id': usuario['id'],
            'email': usuario['email'],
            'tipo_perfil': usuario['tipo_perfil'],
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, os.getenv('JWT_SECRET', 'seu-secreto-jwt-super-seguro'), algorithm='HS256')
        
        return {
            'token': token,
            'usuario': {
                'id': usuario['id'],
                'email': usuario['email'],
                'nome': usuario['nome'],
                'tipo_perfil': usuario['tipo_perfil']
            }
        }

class CadastrarUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def executar(self, dados: UsuarioCreate):
        # Validar duplicatas
        if self.usuario_repository.email_existe(dados.email):
            raise EmailJaCadastrado(f"Email {dados.email} já cadastrado")
        
        if self.usuario_repository.cpf_existe(dados.cpf):
            raise CPFJaCadastrado(f"CPF {dados.cpf} já cadastrado")
        
        # Hash da senha
        senha_hash = bcrypt.hashpw(dados.senha.encode(), bcrypt.gensalt()).decode()
        
        usuario = Usuario(
            email=dados.email,
            cpf=dados.cpf,
            nome=dados.nome,
            telefone=dados.telefone,
            cidade=dados.cidade,
            tipo_perfil=dados.tipo_perfil,
            senha_hash=senha_hash
        )
        
        resultado = self.usuario_repository.criar(usuario)
        
        return {
            'id': resultado['id'],
            'email': resultado['email'],
            'nome': resultado['nome'],
            'tipo_perfil': resultado['tipo_perfil'],
            'mensagem': 'Usuário cadastrado com sucesso'
        }

class RecuperarSenha:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def executar(self, email, nova_senha):
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontrado(f"Usuário com email {email} não encontrado")
        
        # Hash da nova senha
        senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
        
        self.usuario_repository.atualizar(usuario['id'], {'senha_hash': senha_hash})
        
        return {'mensagem': 'Senha atualizada com sucesso'}
