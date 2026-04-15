import pytest
from unittest.mock import Mock
from uuid import uuid4
from use_cases.localizacao_commands import RegistrarLocalizacao, ObterUltimaLocalizacao, ObterHistoricoLocalizacao
from exceptions import DadosInvalidosException
from tests.factories import VeiculoFactory, LocalizacaoGPSFactory

class TestRegistrarLocalizacao:
    
    def test_registrar_localizacao_sucesso(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        
        gps_repo = Mock()
        gps_repo.criar.return_value = LocalizacaoGPSFactory.criar_localizacao(veiculo.id)
        
        usecase = RegistrarLocalizacao(gps_repo, veiculo_repo)
        localizacao = usecase.executar(str(veiculo.id), -23.5505, -46.6333)
        
        assert localizacao is not None
        assert localizacao.latitude == -23.5505
        assert localizacao.longitude == -46.6333
        gps_repo.criar.assert_called_once()
    
    def test_registrar_localizacao_veiculo_nao_existe(self):
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = None
        
        gps_repo = Mock()
        usecase = RegistrarLocalizacao(gps_repo, veiculo_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(uuid4()), -23.5505, -46.6333)
    
    def test_registrar_localizacao_latitude_invalida(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        
        gps_repo = Mock()
        usecase = RegistrarLocalizacao(gps_repo, veiculo_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id), 91.0, -46.6333)
    
    def test_registrar_localizacao_longitude_invalida(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        
        gps_repo = Mock()
        usecase = RegistrarLocalizacao(gps_repo, veiculo_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id), -23.5505, 181.0)
    
    def test_validar_coordenadas_validas(self):
        assert RegistrarLocalizacao._validar_coordenadas(-90, -180) is True
        assert RegistrarLocalizacao._validar_coordenadas(0, 0) is True
        assert RegistrarLocalizacao._validar_coordenadas(90, 180) is True
        assert RegistrarLocalizacao._validar_coordenadas(-23.5505, -46.6333) is True
    
    def test_validar_coordenadas_invalidas(self):
        assert RegistrarLocalizacao._validar_coordenadas(91, 0) is False
        assert RegistrarLocalizacao._validar_coordenadas(-91, 0) is False
        assert RegistrarLocalizacao._validar_coordenadas(0, 181) is False
        assert RegistrarLocalizacao._validar_coordenadas(0, -181) is False

class TestObterUltimaLocalizacao:
    
    def test_obter_ultima_localizacao_sucesso(self):
        veiculo = VeiculoFactory.criar_veiculo()
        localizacao = LocalizacaoGPSFactory.criar_localizacao(veiculo.id)
        
        gps_repo = Mock()
        gps_repo.obter_ultima_por_veiculo.return_value = localizacao
        
        usecase = ObterUltimaLocalizacao(gps_repo)
        resultado = usecase.executar(str(veiculo.id))
        
        assert resultado is not None
        assert resultado['latitude'] == localizacao.latitude
        gps_repo.obter_ultima_por_veiculo.assert_called_once()
    
    def test_obter_ultima_localizacao_nao_existe(self):
        veiculo = VeiculoFactory.criar_veiculo()
        gps_repo = Mock()
        gps_repo.obter_ultima_por_veiculo.return_value = None
        
        usecase = ObterUltimaLocalizacao(gps_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id))

class TestObterHistoricoLocalizacao:
    
    def test_obter_historico_localizacao_sucesso(self):
        veiculo = VeiculoFactory.criar_veiculo()
        localizacoes = [
            LocalizacaoGPSFactory.criar_localizacao(veiculo.id),
            LocalizacaoGPSFactory.criar_localizacao(veiculo.id)
        ]
        
        gps_repo = Mock()
        gps_repo.obter_historico_veiculo.return_value = localizacoes
        
        usecase = ObterHistoricoLocalizacao(gps_repo)
        resultado = usecase.executar(str(veiculo.id), 100)
        
        assert len(resultado) == 2
        gps_repo.obter_historico_veiculo.assert_called_once()
    
    def test_obter_historico_localizacao_limite_invalido(self):
        veiculo = VeiculoFactory.criar_veiculo()
        gps_repo = Mock()
        
        usecase = ObterHistoricoLocalizacao(gps_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id), 0)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id), 2000)
