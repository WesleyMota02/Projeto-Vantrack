from exceptions import RotaNaoEncontrada, DadosInvalidos
from domain.rota import RotaCreate

class CriarRota:
    def __init__(self, rota_repository, veiculo_repository, usuario_repository):
        self.rota_repository = rota_repository
        self.veiculo_repository = veiculo_repository
        self.usuario_repository = usuario_repository

    def executar(self, dados: RotaCreate):
        if dados.origem == dados.destino:
            raise DadosInvalidos("Origem e destino não podem ser iguais")
        
        motorista = self.usuario_repository.buscar_por_id(dados.motorista_id)
        if not motorista or motorista['tipo_perfil'] != 'motorista':
            raise DadosInvalidos("Motorista inválido")
        
        veiculo = self.veiculo_repository.buscar_por_id(dados.veiculo_id)
        if not veiculo:
            raise DadosInvalidos("Veículo não encontrado")
        
        if dados.capacidade_maxima > veiculo['capacidade']:
            raise DadosInvalidos("Capacidade da rota não pode exceder capacidade do veículo")
        
        rota = self.rota_repository.criar(dados)
        return rota

class AtualizarRota:
    def __init__(self, rota_repository, veiculo_repository):
        self.rota_repository = rota_repository
        self.veiculo_repository = veiculo_repository

    def executar(self, rota_id, dados):
        rota = self.rota_repository.buscar_por_id(rota_id)
        if not rota:
            raise RotaNaoEncontrada(f"Rota com id {rota_id} não encontrada")
        
        if 'origem' in dados and 'destino' in dados:
            if dados['origem'] == dados['destino']:
                raise DadosInvalidos("Origem e destino não podem ser iguais")
        elif 'origem' in dados and dados['origem'] == rota['destino']:
            raise DadosInvalidos("Origem e destino não podem ser iguais")
        elif 'destino' in dados and dados['destino'] == rota['origem']:
            raise DadosInvalidos("Origem e destino não podem ser iguais")
        
        if 'capacidade_maxima' in dados and 'veiculo_id' in dados:
            veiculo = self.veiculo_repository.buscar_por_id(dados['veiculo_id'])
            if dados['capacidade_maxima'] > veiculo['capacidade']:
                raise DadosInvalidos("Capacidade da rota não pode exceder capacidade do veículo")
        
        rota_atualizada = self.rota_repository.atualizar(rota_id, dados)
        return rota_atualizada

class DeletarRota:
    def __init__(self, rota_repository):
        self.rota_repository = rota_repository

    def executar(self, rota_id):
        rota = self.rota_repository.buscar_por_id(rota_id)
        if not rota:
            raise RotaNaoEncontrada(f"Rota com id {rota_id} não encontrada")
        
        self.rota_repository.desativar(rota_id)
        return {'mensagem': 'Rota deletada com sucesso'}
