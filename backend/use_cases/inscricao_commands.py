from exceptions import InscricaoNaoEncontrada, CapacidadeExcedida, DadosInvalidos, DuplicacaoInscricao
from domain.inscricao import InscricaoCreate

class CriarInscricao:
    def __init__(self, inscricao_repository, rota_repository, usuario_repository):
        self.inscricao_repository = inscricao_repository
        self.rota_repository = rota_repository
        self.usuario_repository = usuario_repository

    def executar(self, dados: InscricaoCreate):
        aluno = self.usuario_repository.buscar_por_id(dados.aluno_id)
        if not aluno or aluno['tipo_perfil'] != 'aluno':
            raise DadosInvalidos("Aluno inválido")
        
        rota = self.rota_repository.buscar_por_id(dados.rota_id)
        if not rota:
            raise DadosInvalidos("Rota não encontrada")
        
        if self.inscricao_repository.inscricao_existe(dados.aluno_id, dados.rota_id):
            raise DuplicacaoInscricao("Aluno já inscrito nesta rota")
        
        inscritos = self.inscricao_repository.contar_por_rota(dados.rota_id)
        if inscritos >= rota['capacidade_maxima']:
            raise CapacidadeExcedida("Rota atingiu capacidade máxima")
        
        inscricao = self.inscricao_repository.criar(dados)
        return inscricao

class CancelarInscricao:
    def __init__(self, inscricao_repository):
        self.inscricao_repository = inscricao_repository

    def executar(self, inscricao_id):
        inscricao = self.inscricao_repository.buscar_por_id(inscricao_id)
        if not inscricao:
            raise InscricaoNaoEncontrada(f"Inscrição com id {inscricao_id} não encontrada")
        
        inscricao_cancelada = self.inscricao_repository.cancelar(inscricao_id)
        return inscricao_cancelada
