from datetime import datetime
from domain.localizacao_gps import LocalizacaoGPS
from infra.localizacao_gps_repository import LocalizacaoGPSRepository
from infra.veiculo_repository import VeiculoRepository
from exceptions import DadosInvalidosException

class RegistrarLocalizacao:

    def __init__(self, repo: LocalizacaoGPSRepository, veiculo_repo: VeiculoRepository):
        self.repo = repo
        self.veiculo_repo = veiculo_repo

    def executar(self, veiculo_id: str, latitude: float, longitude: float) -> LocalizacaoGPS:
        if not veiculo_id or not veiculo_id.strip():
            raise DadosInvalidosException("ID do veículo é obrigatório")

        veiculo = self.veiculo_repo.obter_por_id(veiculo_id)
        if not veiculo:
            raise DadosInvalidosException(f"Veículo '{veiculo_id}' não encontrado")

        if not self._validar_coordenadas(latitude, longitude):
            raise DadosInvalidosException("Coordenadas inválidas")

        localizacao = LocalizacaoGPS(
            veiculo_id=veiculo_id,
            latitude=float(latitude),
            longitude=float(longitude),
            timestamp=datetime.utcnow()
        )

        return self.repo.criar(localizacao)

    @staticmethod
    def _validar_coordenadas(latitude: float, longitude: float) -> bool:
        try:
            lat = float(latitude)
            lon = float(longitude)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (ValueError, TypeError):
            return False

class ObterUltimaLocalizacao:

    def __init__(self, repo: LocalizacaoGPSRepository):
        self.repo = repo

    def executar(self, veiculo_id: str) -> dict:
        if not veiculo_id or not veiculo_id.strip():
            raise DadosInvalidosException("ID do veículo é obrigatório")

        localizacao = self.repo.obter_ultima_por_veiculo(veiculo_id)
        if not localizacao:
            raise DadosInvalidosException(f"Nenhuma localização registrada para o veículo '{veiculo_id}'")

        return localizacao.to_dict()

class ObterHistoricoLocalizacao:

    def __init__(self, repo: LocalizacaoGPSRepository):
        self.repo = repo

    def executar(self, veiculo_id: str, limite: int = 100) -> list:
        if not veiculo_id or not veiculo_id.strip():
            raise DadosInvalidosException("ID do veículo é obrigatório")

        if limite < 1 or limite > 1000:
            raise DadosInvalidosException("Limite inválido (1-1000)")

        localizacoes = self.repo.obter_historico_veiculo(veiculo_id, limite)
        return [loc.to_dict() for loc in localizacoes]
