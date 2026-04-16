import pytest
from exceptions import VeiculoNaoEncontrado, LocalicaoGPSInvalida
from use_cases.localizacao_commands import RegistrarLocalizacao, ObterUltimaLocalizacao, ObterHistoricoLocalizacao
from domain.localizacao_gps import LocalizacaoGPSCreate

class TestRegistrarLocalizacao:
    @pytest.mark.unit
    def test_registrar_localizacao_com_sucesso(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234'}
        localizacao_repo.criar.return_value = {'id': 1, 'latitude': -23.5505, 'longitude': -46.6333}
        
        registrar_use_case = RegistrarLocalizacao(localizacao_repo, veiculo_repo)
        localizacao = LocalizacaoGPSCreate(latitude=-23.5505, longitude=-46.6333, veiculo_id=1)
        resultado = registrar_use_case.executar(localizacao)
        
        assert resultado['latitude'] == -23.5505

    @pytest.mark.unit
    def test_registrar_localizacao_veiculo_invalido(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = None
        
        registrar_use_case = RegistrarLocalizacao(localizacao_repo, veiculo_repo)
        localizacao = LocalizacaoGPSCreate(latitude=-23.5505, longitude=-46.6333, veiculo_id=999)
        
        with pytest.raises(VeiculoNaoEncontrado):
            registrar_use_case.executar(localizacao)

    @pytest.mark.unit
    def test_validacao_latitude_invalida(self, mocker):
        with pytest.raises(ValueError):
            LocalizacaoGPSCreate(latitude=91, longitude=-46.6333, veiculo_id=1)

    @pytest.mark.unit
    def test_validacao_longitude_invalida(self, mocker):
        with pytest.raises(ValueError):
            LocalizacaoGPSCreate(latitude=-23.5505, longitude=181, veiculo_id=1)

class TestObterUltimaLocalizacao:
    @pytest.mark.unit
    def test_obter_ultima_localizacao_com_sucesso(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234'}
        localizacao_repo.obter_ultima_localizacao.return_value = {'id': 1, 'latitude': -23.5505}
        
        obter_use_case = ObterUltimaLocalizacao(localizacao_repo, veiculo_repo)
        resultado = obter_use_case.executar(1)
        
        assert resultado['id'] == 1

    @pytest.mark.unit
    def test_obter_ultima_localizacao_veiculo_invalido(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = None
        
        obter_use_case = ObterUltimaLocalizacao(localizacao_repo, veiculo_repo)
        
        with pytest.raises(VeiculoNaoEncontrado):
            obter_use_case.executar(999)

class TestObterHistoricoLocalizacao:
    @pytest.mark.unit
    def test_obter_historico_com_sucesso(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234'}
        localizacao_repo.obter_historico.return_value = [
            {'id': 1, 'latitude': -23.5505},
            {'id': 2, 'latitude': -23.5506}
        ]
        
        obter_use_case = ObterHistoricoLocalizacao(localizacao_repo, veiculo_repo)
        resultado = obter_use_case.executar(1, 100)
        
        assert len(resultado) == 2

    @pytest.mark.unit
    def test_obter_historico_limite_maximo(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234'}
        localizacao_repo.obter_historico.return_value = []
        
        obter_use_case = ObterHistoricoLocalizacao(localizacao_repo, veiculo_repo)
        obter_use_case.executar(1, 1000)
        
        localizacao_repo.obter_historico.assert_called_with(1, 500)

    @pytest.mark.unit
    def test_obter_historico_veiculo_invalido(self, mocker):
        localizacao_repo = mocker.MagicMock()
        veiculo_repo = mocker.MagicMock()
        
        veiculo_repo.buscar_por_id.return_value = None
        
        obter_use_case = ObterHistoricoLocalizacao(localizacao_repo, veiculo_repo)
        
        with pytest.raises(VeiculoNaoEncontrado):
            obter_use_case.executar(999, 100)
