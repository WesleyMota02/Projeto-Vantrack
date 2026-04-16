import pytest
from exceptions import InscricaoNaoEncontrada, CapacidadeExcedida, DadosInvalidos, DuplicacaoInscricao
from use_cases.inscricao_commands import CriarInscricao, CancelarInscricao
from domain.inscricao import InscricaoCreate

class TestCriarInscricao:
    @pytest.mark.unit
    def test_criar_inscricao_com_sucesso(self, mocker):
        inscricao_repo = mocker.MagicMock()
        rota_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = {'id': 1, 'tipo_perfil': 'aluno'}
        rota_repo.buscar_por_id.return_value = {'id': 1, 'capacidade_maxima': 50}
        inscricao_repo.inscricao_existe.return_value = False
        inscricao_repo.contar_por_rota.return_value = 10
        inscricao_repo.criar.return_value = {'id': 1, 'aluno_id': 1, 'rota_id': 1}
        
        criar_use_case = CriarInscricao(inscricao_repo, rota_repo, usuario_repo)
        inscricao = InscricaoCreate(aluno_id=1, rota_id=1)
        resultado = criar_use_case.executar(inscricao)
        
        assert resultado['aluno_id'] == 1

    @pytest.mark.unit
    def test_criar_inscricao_aluno_invalido(self, mocker):
        inscricao_repo = mocker.MagicMock()
        rota_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = None
        
        criar_use_case = CriarInscricao(inscricao_repo, rota_repo, usuario_repo)
        inscricao = InscricaoCreate(aluno_id=999, rota_id=1)
        
        with pytest.raises(DadosInvalidos):
            criar_use_case.executar(inscricao)

    @pytest.mark.unit
    def test_criar_inscricao_duplicada(self, mocker):
        inscricao_repo = mocker.MagicMock()
        rota_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = {'id': 1, 'tipo_perfil': 'aluno'}
        rota_repo.buscar_por_id.return_value = {'id': 1, 'capacidade_maxima': 50}
        inscricao_repo.inscricao_existe.return_value = True
        
        criar_use_case = CriarInscricao(inscricao_repo, rota_repo, usuario_repo)
        inscricao = InscricaoCreate(aluno_id=1, rota_id=1)
        
        with pytest.raises(DuplicacaoInscricao):
            criar_use_case.executar(inscricao)

    @pytest.mark.unit
    def test_criar_inscricao_capacidade_excedida(self, mocker):
        inscricao_repo = mocker.MagicMock()
        rota_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = {'id': 1, 'tipo_perfil': 'aluno'}
        rota_repo.buscar_por_id.return_value = {'id': 1, 'capacidade_maxima': 50}
        inscricao_repo.inscricao_existe.return_value = False
        inscricao_repo.contar_por_rota.return_value = 50
        
        criar_use_case = CriarInscricao(inscricao_repo, rota_repo, usuario_repo)
        inscricao = InscricaoCreate(aluno_id=1, rota_id=1)
        
        with pytest.raises(CapacidadeExcedida):
            criar_use_case.executar(inscricao)

class TestCancelarInscricao:
    @pytest.mark.unit
    def test_cancelar_inscricao_com_sucesso(self, mocker):
        inscricao_repo = mocker.MagicMock()
        inscricao_repo.buscar_por_id.return_value = {'id': 1, 'status': 'ativa'}
        inscricao_repo.cancelar.return_value = {'id': 1, 'status': 'cancelada'}
        
        cancelar_use_case = CancelarInscricao(inscricao_repo)
        resultado = cancelar_use_case.executar(1)
        
        assert resultado['status'] == 'cancelada'

    @pytest.mark.unit
    def test_cancelar_inscricao_nao_encontrada(self, mocker):
        inscricao_repo = mocker.MagicMock()
        inscricao_repo.buscar_por_id.return_value = None
        
        cancelar_use_case = CancelarInscricao(inscricao_repo)
        
        with pytest.raises(InscricaoNaoEncontrada):
            cancelar_use_case.executar(999)
