from infra.usuario_repository import UsuarioRepository
from exceptions import EmailNaoEncontradoException, DadosInvalidosException

class RecuperarSenha:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, email: str) -> dict:
        if not email or not email.strip():
            raise DadosInvalidosException("E-mail é obrigatório")

        usuario = self.repo.obter_por_email(email)
        if not usuario:
            raise EmailNaoEncontradoException(email)

        return {
            'usuario_id': str(usuario.id),
            'email': usuario.email,
            'nome': usuario.nome,
            'mensagem': 'E-mail de recuperação será enviado em breve'
        }
