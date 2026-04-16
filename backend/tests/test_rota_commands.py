import pytest
from exceptions import RotaNaoEncontrada, DadosInvalidos
from use_cases.rota_commands import CriarRota, AtualizarRota, DeletarRota
from domain.rota import RotaCreate

class TestCriarRota:
    @pytest.mark.unit
    def test_criar_rota_com_sucesso(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = {'id': 1, 'tipo_perfil': 'motorista'}
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'capacidade': 50}
        rota_repo.criar.return_value = {'id': 1, 'nome': 'Rota 1', 'origem': 'SP', 'destino': 'Campinas'}
        
        criar_use_case = CriarRota(rota_repo, veiculo_repo, usuario_repo)
        rota = RotaCreate(nome='Rota 1', origem='SP', destino='Campinas', horario_partida='08:00',
                         capacidade_maxima=50, motorista_id=1, veiculo_id=1)
        resultado = criar_use_case.executar(rota)
        
        assert resultado['nome'] == 'Rota 1'

    @pytest.mark.unit
    def test_criar_rota_origem_destino_iguais(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        criar_use_case = CriarRota(rota_repo, veiculo_repo, usuario_repo)
        
        with pytest.raises(DadosInvalidos):
            RotaCreate(nome='Rota 1', origem='SP', destino='SP', horario_partida='08:00',
                      capacidade_maxima=50, motorista_id=1, veiculo_id=1)

    @pytest.mark.unit
    def test_criar_rota_motorista_invalido(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = None
        
        criar_use_case = CriarRota(rota_repo, veiculo_repo, usuario_repo)
        rota = RotaCreate(nome='Rota 1', origem='SP', destino='Campinas', horario_partida='08:00',
                         capacidade_maxima=50, motorista_id=999, veiculo_id=1)
        
        with pytest.raises(DadosInvalidos):
            criar_use_case.executar(rota)

    @pytest.mark.unit
    def test_criar_rota_capacidade_excede_veiculo(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        
        usuario_repo.buscar_por_id.return_value = {'id': 1, 'tipo_perfil': 'motorista'}
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'capacidade': 30}
        
        criar_use_case = CriarRota(rota_repo, veiculo_repo, usuario_repo)
        rota = RotaCreate(nome='Rota 1', origem='SP', destino='Campinas', horario_partida='08:00',
                         capacidade_maxima=50, motorista_id=1, veiculo_id=1)
        
        with pytest.raises(DadosInvalidos):
            criar_use_case.executar(rota)

class TestAtualizarRota:
    @pytest.mark.unit
    def test_atualizar_rota_com_sucesso(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        rota_repo.buscar_por_id.return_value = {'id': 1, 'origem': 'SP', 'destino': 'Campinas', 'capacidade_maxima': 50}
        rota_repo.atualizar.return_value = {'id': 1, 'nome': 'Rota Atualizada'}
        
        atualizar_use_case = AtualizarRota(rota_repo, veiculo_repo)
        resultado = atualizar_use_case.executar(1, {'nome': 'Rota Atualizada'})
        
        assert resultado['nome'] == 'Rota Atualizada'

    @pytest.mark.unit
    def test_atualizar_rota_nao_encontrada(self, mocker):
        rota_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        rota_repo.buscar_por_id.return_value = None
        
        atualizar_use_case = AtualizarRota(rota_repo, veiculo_repo)
        
        with pytest.raises(RotaNaoEncontrada):
            atualizar_use_case.executar(999, {'nome': 'Nova Rota'})

class TestDeletarRota:
    @pytest.mark.unit
    def test_deletar_rota_com_sucesso(self, mocker):
        rota_repo = mocker.MagicMock()
        rota_repo.buscar_por_id.return_value = {'id': 1, 'nome': 'Rota 1'}
        
        deletar_use_case = DeletarRota(rota_repo)
        resultado = deletar_use_case.executar(1)
        
        assert 'mensagem' in resultado
        rota_repo.desativar.assert_called_once_with(1)

    @pytest.mark.unit
    def test_deletar_rota_nao_encontrada(self, mocker):
        rota_repo = mocker.MagicMock()
        rota_repo.buscar_por_id.return_value = None
        
        deletar_use_case = DeletarRota(rota_repo)
        
        with pytest.raises(RotaNaoEncontrada):
            deletar_use_case.executar(999)
