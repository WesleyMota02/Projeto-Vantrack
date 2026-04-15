from uuid import uuid4
from domain.veiculo import Veiculo
from infra.veiculo_repository import VeiculoRepository
from exceptions import UsuarioNaoEncontradoException, DadosInvalidosException

class CriarVeiculo:

    def __init__(self, repo: VeiculoRepository, usuario_repo):
        self.repo = repo
        self.usuario_repo = usuario_repo

    def executar(self, motorista_id: str, dados: dict) -> Veiculo:
        if not motorista_id or not motorista_id.strip():
            raise DadosInvalidosException("ID do motorista é obrigatório")

        motorista = self.usuario_repo.obter_por_id(motorista_id)
        if not motorista or motorista.tipo_perfil != 'motorista':
            raise UsuarioNaoEncontradoException(motorista_id)

        placa = dados.get('placa', '').strip().upper()
        if not placa or len(placa) < 5:
            raise DadosInvalidosException("Placa inválida (mínimo 5 caracteres)")

        if self.repo.obter_por_placa(placa):
            raise DadosInvalidosException(f"Placa '{placa}' já cadastrada")

        modelo = dados.get('modelo', '').strip()
        if not modelo or len(modelo) < 3:
            raise DadosInvalidosException("Modelo inválido (mínimo 3 caracteres)")

        ano = dados.get('ano', 2000)
        if not isinstance(ano, int) or ano < 1990 or ano > 2100:
            raise DadosInvalidosException("Ano inválido (1990-2100)")

        capacidade = dados.get('capacidade', 50)
        if not isinstance(capacidade, int) or capacidade < 1 or capacidade > 500:
            raise DadosInvalidosException("Capacidade inválida (1-500)")

        veiculo = Veiculo(
            id=uuid4(),
            motorista_id=motorista_id,
            placa=placa,
            modelo=modelo,
            ano=ano,
            capacidade=capacidade,
            ativo=True
        )

        return self.repo.criar(veiculo)

class AtualizarVeiculo:

    def __init__(self, repo: VeiculoRepository):
        self.repo = repo

    def executar(self, veiculo_id: str, dados: dict) -> Veiculo:
        if not veiculo_id or not veiculo_id.strip():
            raise DadosInvalidosException("ID do veículo é obrigatório")

        veiculo_existente = self.repo.obter_por_id(veiculo_id)
        if not veiculo_existente:
            raise DadosInvalidosException(f"Veículo '{veiculo_id}' não encontrado")

        dados_atualizacao = {}

        if 'placa' in dados:
            placa = dados['placa'].strip().upper()
            if placa != veiculo_existente.placa:
                if self.repo.obter_por_placa(placa):
                    raise DadosInvalidosException(f"Placa '{placa}' já cadastrada")
            dados_atualizacao['placa'] = placa

        if 'modelo' in dados:
            modelo = dados['modelo'].strip()
            if len(modelo) < 3:
                raise DadosInvalidosException("Modelo inválido (mínimo 3 caracteres)")
            dados_atualizacao['modelo'] = modelo

        if 'ano' in dados:
            ano = int(dados['ano'])
            if ano < 1990 or ano > 2100:
                raise DadosInvalidosException("Ano inválido (1990-2100)")
            dados_atualizacao['ano'] = ano

        if 'capacidade' in dados:
            capacidade = int(dados['capacidade'])
            if capacidade < 1 or capacidade > 500:
                raise DadosInvalidosException("Capacidade inválida (1-500)")
            dados_atualizacao['capacidade'] = capacidade

        if not dados_atualizacao:
            return veiculo_existente

        return self.repo.atualizar(veiculo_id, dados_atualizacao)

class DeletarVeiculo:

    def __init__(self, repo: VeiculoRepository):
        self.repo = repo

    def executar(self, veiculo_id: str) -> bool:
        if not veiculo_id or not veiculo_id.strip():
            raise DadosInvalidosException("ID do veículo é obrigatório")

        veiculo = self.repo.obter_por_id(veiculo_id)
        if not veiculo:
            raise DadosInvalidosException(f"Veículo '{veiculo_id}' não encontrado")

        return self.repo.deletar(veiculo_id)
