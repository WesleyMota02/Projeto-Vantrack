from exceptions import VeiculoNaoEncontrado, CapacidadeExcedida, DadosInvalidos
from domain.veiculo import VeiculoCreate

class CriarVeiculo:
    def __init__(self, veiculo_repository):
        self.veiculo_repository = veiculo_repository

    def executar(self, dados: VeiculoCreate):
        if self.veiculo_repository.placa_existe(dados.placa):
            raise DadosInvalidos(f"Veículo com placa {dados.placa} já existe")
        
        veiculo = self.veiculo_repository.criar(dados)
        return veiculo

class AtualizarVeiculo:
    def __init__(self, veiculo_repository):
        self.veiculo_repository = veiculo_repository

    def executar(self, veiculo_id, dados):
        veiculo = self.veiculo_repository.buscar_por_id(veiculo_id)
        if not veiculo:
            raise VeiculoNaoEncontrado(f"Veículo com id {veiculo_id} não encontrado")
        
        if 'placa' in dados and dados['placa'] != veiculo['placa']:
            if self.veiculo_repository.placa_existe(dados['placa']):
                raise DadosInvalidos(f"Placa {dados['placa']} já cadastrada")
        
        veiculo_atualizado = self.veiculo_repository.atualizar(veiculo_id, dados)
        return veiculo_atualizado

class DeletarVeiculo:
    def __init__(self, veiculo_repository):
        self.veiculo_repository = veiculo_repository

    def executar(self, veiculo_id):
        veiculo = self.veiculo_repository.buscar_por_id(veiculo_id)
        if not veiculo:
            raise VeiculoNaoEncontrado(f"Veículo com id {veiculo_id} não encontrado")
        
        self.veiculo_repository.deletar(veiculo_id)
        return {'mensagem': 'Veículo deletado com sucesso'}
