from uuid import uuid4
from domain.inscricao import Inscricao
from infra.inscricao_repository import InscricaoRepository
from infra.usuario_repository import UsuarioRepository
from infra.rota_repository import RotaRepository
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException

class CriarInscricao:

    def __init__(self, repo: InscricaoRepository, usuario_repo: UsuarioRepository, rota_repo: RotaRepository):
        self.repo = repo
        self.usuario_repo = usuario_repo
        self.rota_repo = rota_repo

    def executar(self, aluno_id: str, rota_id: str) -> Inscricao:
        if not aluno_id or not aluno_id.strip():
            raise DadosInvalidosException("ID do aluno é obrigatório")

        if not rota_id or not rota_id.strip():
            raise DadosInvalidosException("ID da rota é obrigatório")

        aluno = self.usuario_repo.obter_por_id(aluno_id)
        if not aluno or aluno.tipo_perfil != 'aluno':
            raise UsuarioNaoEncontradoException(aluno_id)

        rota = self.rota_repo.obter_por_id(rota_id)
        if not rota:
            raise DadosInvalidosException(f"Rota '{rota_id}' não encontrada")

        if not rota.ativa:
            raise DadosInvalidosException("Rota inativa, não pode inscrever alunos")

        inscricao_existente = self.repo.obter_inscricao(aluno_id, rota_id)
        if inscricao_existente:
            raise DadosInvalidosException(f"Aluno já inscrito nesta rota")

        inscricoes_rota = self.repo.obter_por_rota(rota_id)
        if len(inscricoes_rota) >= rota.capacidade_maxima:
            raise DadosInvalidosException(f"Rota lotada (capacidade: {rota.capacidade_maxima})")

        inscricao = Inscricao(
            id=uuid4(),
            aluno_id=aluno_id,
            rota_id=rota_id,
            ativa=True
        )

        return self.repo.criar(inscricao)

class CancelarInscricao:

    def __init__(self, repo: InscricaoRepository):
        self.repo = repo

    def executar(self, inscricao_id: str) -> bool:
        if not inscricao_id or not inscricao_id.strip():
            raise DadosInvalidosException("ID da inscrição é obrigatório")

        inscricao = self.repo.obter_por_id(inscricao_id)
        if not inscricao:
            raise DadosInvalidosException(f"Inscrição '{inscricao_id}' não encontrada")

        return self.repo.deletar(inscricao_id)
