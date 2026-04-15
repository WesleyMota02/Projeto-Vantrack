import os
import jwt
from datetime import datetime, timedelta
import bcrypt
from infra.usuario_repository import UsuarioRepository
from exceptions import EmailNaoEncontradoException, SenhaInvalidaException, ErroGeracaoTokenException, DadosInvalidosException

class AutenticarUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        self.jwt_secret = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-prod')
        self.jwt_expiry = int(os.getenv('JWT_EXPIRY', 86400))

    def executar(self, email: str, senha: str, tipo_perfil: str) -> tuple[dict, str]:
        if not email or not senha:
            raise DadosInvalidosException("E-mail e senha são obrigatórios")

        if tipo_perfil not in ['aluno', 'motorista']:
            raise DadosInvalidosException("Tipo de perfil inválido")

        usuario = self.repo.obter_por_email(email)
        if not usuario:
            raise EmailNaoEncontradoException(email)

        if usuario.tipo_perfil != tipo_perfil:
            raise DadosInvalidosException("Tipo de perfil não corresponde ao usuário")

        if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha_hash.encode('utf-8')):
            raise SenhaInvalidaException()

        payload = {
            'usuario_id': str(usuario.id),
            'email': usuario.email,
            'tipo_perfil': usuario.tipo_perfil,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiry)
        }

        try:
            token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        except Exception as e:
            raise ErroGeracaoTokenException()

        return usuario.to_dict(include_senha_hash=False), token
