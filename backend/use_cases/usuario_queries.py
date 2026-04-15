from infra.usuario_repository import UsuarioRepository
from exceptions import UsuarioNaoEncontradoException, DadosInvalidosException

class ObterUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, usuario_id: str) -> dict:
        if not usuario_id or not usuario_id.strip():
            raise DadosInvalidosException("ID do usuário é obrigatório")

        usuario = self.repo.obter_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoException(usuario_id)

        return usuario.to_dict(include_senha_hash=False)

class ListarUsuariosPorTipo:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, tipo_perfil: str) -> list:
        if tipo_perfil not in ['aluno', 'motorista']:
            raise DadosInvalidosException("Tipo de perfil inválido (aluno ou motorista)")

        usuarios = self.repo.listar_por_tipo(tipo_perfil)
        return [u.to_dict(include_senha_hash=False) for u in usuarios]

class AtualizarPerfilUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, usuario_id: str, dados_atualizacao: dict) -> dict:
        if not usuario_id or not usuario_id.strip():
            raise DadosInvalidosException("ID do usuário é obrigatório")

        usuario_existente = self.repo.obter_por_id(usuario_id)
        if not usuario_existente:
            raise UsuarioNaoEncontradoException(usuario_id)

        campos_atualizaveis = ['nome', 'sobrenome', 'telefone', 'cidade']
        dados_filtrados = {k: v for k, v in dados_atualizacao.items() if k in campos_atualizaveis}

        if not dados_filtrados:
            return usuario_existente.to_dict(include_senha_hash=False)

        usuario_atualizado = self.repo.atualizar(usuario_id, dados_filtrados)
        if not usuario_atualizado:
            raise DadosInvalidosException("Erro ao atualizar usuário")

        return usuario_atualizado.to_dict(include_senha_hash=False)
