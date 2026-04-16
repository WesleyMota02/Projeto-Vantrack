from exceptions import VeiculoNaoEncontrado, LocalicaoGPSInvalida
from domain.localizacao_gps import LocalizacaoGPSCreate

class RegistrarLocalizacao:
    def __init__(self, localizacao_repository, veiculo_repository):
        self.localizacao_repository = localizacao_repository
        self.veiculo_repository = veiculo_repository

    def executar(self, dados: LocalizacaoGPSCreate):
        veiculo = self.veiculo_repository.buscar_por_id(dados.veiculo_id)
        if not veiculo:
            raise VeiculoNaoEncontrado(f"Veículo com id {dados.veiculo_id} não encontrado")
        
        localizacao = self.localizacao_repository.criar(dados)
        return localizacao

class ObterUltimaLocalizacao:
    def __init__(self, localizacao_repository, veiculo_repository):
        self.localizacao_repository = localizacao_repository
        self.veiculo_repository = veiculo_repository

    def executar(self, veiculo_id):
        veiculo = self.veiculo_repository.buscar_por_id(veiculo_id)
        if not veiculo:
            raise VeiculoNaoEncontrado(f"Veículo com id {veiculo_id} não encontrado")
        
        localizacao = self.localizacao_repository.obter_ultima_localizacao(veiculo_id)
        return localizacao

class ObterHistoricoLocalizacao:
    def __init__(self, localizacao_repository, veiculo_repository):
        self.localizacao_repository = localizacao_repository
        self.veiculo_repository = veiculo_repository

    def executar(self, veiculo_id, limite=100):
        veiculo = self.veiculo_repository.buscar_por_id(veiculo_id)
        if not veiculo:
            raise VeiculoNaoEncontrado(f"Veículo com id {veiculo_id} não encontrado")
        
        if limite > 500:
            limite = 500
        
        historico = self.localizacao_repository.obter_historico(veiculo_id, limite)
        return historico
