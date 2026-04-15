import bcrypt
from uuid import uuid4
from domain.usuario import Usuario
from domain.validadores import ValidadorUsuario, RegistroCadastroRequest
from infra.usuario_repository import UsuarioRepository
from exceptions import UsuarioJaExisteException, DadosInvalidosException

class CadastrarUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, dados: dict) -> Usuario:
        req = RegistroCadastroRequest(dados)
        valido, erros = req.validar()

        if not valido:
            raise DadosInvalidosException("Dados de cadastro inválidos", erros)

        if self.repo.obter_por_email(req.email):
            raise UsuarioJaExisteException('email', req.email)

        if self.repo.obter_por_cpf(req.cpf):
            raise UsuarioJaExisteException('cpf', req.cpf)

        senha_hash = bcrypt.hashpw(req.senha.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

        usuario = Usuario(
            id=uuid4(),
            tipo_perfil=req.tipo_perfil,
            nome=req.nome,
            sobrenome=req.sobrenome,
            cpf=req.cpf,
            email=req.email,
            telefone=req.telefone,
            cidade=req.cidade,
            senha_hash=senha_hash,
            ativo=True
        )

        return self.repo.criar(usuario)
