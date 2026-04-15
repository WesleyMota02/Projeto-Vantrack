from uuid import uuid4
from domain.rota import Rota
from infra.rota_repository import RotaRepository
from infra.usuario_repository import UsuarioRepository
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException

class CriarRota:

    def __init__(self, repo: RotaRepository, usuario_repo: UsuarioRepository):
        self.repo = repo
        self.usuario_repo = usuario_repo

    def executar(self, motorista_id: str, dados: dict) -> Rota:
        if not motorista_id or not motorista_id.strip():
            raise DadosInvalidosException("ID do motorista é obrigatório")

        motorista = self.usuario_repo.obter_por_id(motorista_id)
        if not motorista or motorista.tipo_perfil != 'motorista':
            raise UsuarioNaoEncontradoException(motorista_id)

        nome = dados.get('nome', '').strip()
        if not nome or len(nome) < 3:
            raise DadosInvalidosException("Nome da rota inválido (mínimo 3 caracteres)")

        origem = dados.get('origem', '').strip()
        if not origem or len(origem) < 3:
            raise DadosInvalidosException("Origem inválida (mínimo 3 caracteres)")

        destino = dados.get('destino', '').strip()
        if not destino or len(destino) < 3:
            raise DadosInvalidosException("Destino inválido (mínimo 3 caracteres)")

        if origem.upper() == destino.upper():
            raise DadosInvalidosException("Origem e destino não podem ser iguais")

        horario_partida = dados.get('horario_partida', '').strip()
        if not self._validar_horario(horario_partida):
            raise DadosInvalidosException("Horário inválido (formato: HH:MM)")

        capacidade_maxima = dados.get('capacidade_maxima', 50)
        if not isinstance(capacidade_maxima, int) or capacidade_maxima < 1 or capacidade_maxima > 500:
            raise DadosInvalidosException("Capacidade máxima inválida (1-500)")

        veiculo_id = dados.get('veiculo_id')

        rota = Rota(
            id=uuid4(),
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            nome=nome,
            origem=origem,
            destino=destino,
            horario_partida=horario_partida,
            capacidade_maxima=capacidade_maxima,
            ativa=True
        )

        return self.repo.criar(rota)

    @staticmethod
    def _validar_horario(horario: str) -> bool:
        try:
            partes = horario.split(':')
            if len(partes) != 2:
                return False
            hh = int(partes[0])
            mm = int(partes[1])
            return 0 <= hh <= 23 and 0 <= mm <= 59
        except (ValueError, AttributeError):
            return False

class AtualizarRota:

    def __init__(self, repo: RotaRepository):
        self.repo = repo

    def executar(self, rota_id: str, dados: dict) -> Rota:
        if not rota_id or not rota_id.strip():
            raise DadosInvalidosException("ID da rota é obrigatório")

        rota_existente = self.repo.obter_por_id(rota_id)
        if not rota_existente:
            raise DadosInvalidosException(f"Rota '{rota_id}' não encontrada")

        dados_atualizacao = {}

        if 'nome' in dados:
            nome = dados['nome'].strip()
            if len(nome) < 3:
                raise DadosInvalidosException("Nome inválido (mínimo 3 caracteres)")
            dados_atualizacao['nome'] = nome

        if 'origem' in dados:
            origem = dados['origem'].strip()
            if len(origem) < 3:
                raise DadosInvalidosException("Origem inválida (mínimo 3 caracteres)")
            dados_atualizacao['origem'] = origem

        if 'destino' in dados:
            destino = dados['destino'].strip()
            if len(destino) < 3:
                raise DadosInvalidosException("Destino inválido (mínimo 3 caracteres)")
            dados_atualizacao['destino'] = destino

        if 'horario_partida' in dados:
            horario = dados['horario_partida'].strip()
            if not CriarRota._validar_horario(horario):
                raise DadosInvalidosException("Horário inválido (formato: HH:MM)")
            dados_atualizacao['horario_partida'] = horario

        if 'capacidade_maxima' in dados:
            capacidade = int(dados['capacidade_maxima'])
            if capacidade < 1 or capacidade > 500:
                raise DadosInvalidosException("Capacidade máxima inválida (1-500)")
            dados_atualizacao['capacidade_maxima'] = capacidade

        if 'veiculo_id' in dados:
            dados_atualizacao['veiculo_id'] = dados['veiculo_id']

        if not dados_atualizacao:
            return rota_existente

        return self.repo.atualizar(rota_id, dados_atualizacao)

class DeletarRota:

    def __init__(self, repo: RotaRepository):
        self.repo = repo

    def executar(self, rota_id: str) -> bool:
        if not rota_id or not rota_id.strip():
            raise DadosInvalidosException("ID da rota é obrigatório")

        rota = self.repo.obter_por_id(rota_id)
        if not rota:
            raise DadosInvalidosException(f"Rota '{rota_id}' não encontrada")

        return self.repo.deletar(rota_id)
