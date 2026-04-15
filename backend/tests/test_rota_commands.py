import pytest
from unittest.mock import Mock
from uuid import uuid4
from use_cases.rota_commands import CriarRota, AtualizarRota, DeletarRota
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException
from tests.factories import UsuarioFactory, RotaFactory

class TestCriarRota:
    
    def test_criar_rota_sucesso(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        rota_repo = Mock()
        rota_repo.criar.return_value = RotaFactory.criar_rota(motorista.id)
        
        usecase = CriarRota(rota_repo, usuario_repo)
        dados = {
            'nome': 'Rota Centro-Norte',
            'origem': 'Escola Centro',
            'destino': 'Bairro Norte',
            'horario_partida': '07:30',
            'capacidade_maxima': 50
        }
        
        rota = usecase.executar(str(motorista.id), dados)
        
        assert rota is not None
        assert rota.nome == 'Rota Centro-Norte'
        rota_repo.criar.assert_called_once()
    
    def test_criar_rota_motorista_nao_existe(self):
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = None
        
        rota_repo = Mock()
        usecase = CriarRota(rota_repo, usuario_repo)
        
        dados = {
            'nome': 'Rota',
            'origem': 'A',
            'destino': 'B',
            'horario_partida': '07:30',
            'capacidade_maxima': 50
        }
        
        with pytest.raises(UsuarioNaoEncontradoException):
            usecase.executar(str(uuid4()), dados)
    
    def test_criar_rota_origem_igual_destino(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        rota_repo = Mock()
        usecase = CriarRota(rota_repo, usuario_repo)
        
        dados = {
            'nome': 'Rota',
            'origem': 'São Paulo',
            'destino': 'São Paulo',
            'horario_partida': '07:30',
            'capacidade_maxima': 50
        }
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)
    
    def test_criar_rota_horario_invalido(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        rota_repo = Mock()
        usecase = CriarRota(rota_repo, usuario_repo)
        
        dados = {
            'nome': 'Rota',
            'origem': 'A',
            'destino': 'B',
            'horario_partida': '25:70',
            'capacidade_maxima': 50
        }
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)
    
    def test_criar_rota_nome_muito_curto(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        rota_repo = Mock()
        usecase = CriarRota(rota_repo, usuario_repo)
        
        dados = {
            'nome': 'AB',
            'origem': 'A',
            'destino': 'B',
            'horario_partida': '07:30',
            'capacidade_maxima': 50
        }
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)
    
    def test_validar_horario_valido(self):
        assert CriarRota._validar_horario('00:00') is True
        assert CriarRota._validar_horario('12:30') is True
        assert CriarRota._validar_horario('23:59') is True
    
    def test_validar_horario_invalido(self):
        assert CriarRota._validar_horario('25:00') is False
        assert CriarRota._validar_horario('12:60') is False
        assert CriarRota._validar_horario('invalid') is False
        assert CriarRota._validar_horario('') is False

class TestAtualizarRota:
    
    def test_atualizar_rota_sucesso(self):
        rota = RotaFactory.criar_rota()
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        rota_atualizada = RotaFactory.criar_rota(rota.motorista_id)
        rota_atualizada.horario_partida = '08:00'
        rota_repo.atualizar.return_value = rota_atualizada
        
        usecase = AtualizarRota(rota_repo)
        dados = {'horario_partida': '08:00'}
        
        resultado = usecase.executar(str(rota.id), dados)
        
        assert resultado is not None
        rota_repo.atualizar.assert_called_once()
    
    def test_atualizar_rota_nao_existe(self):
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = None
        
        usecase = AtualizarRota(rota_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(uuid4()), {})

class TestDeletarRota:
    
    def test_deletar_rota_sucesso(self):
        rota = RotaFactory.criar_rota()
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        rota_repo.deletar.return_value = True
        
        usecase = DeletarRota(rota_repo)
        resultado = usecase.executar(str(rota.id))
        
        assert resultado is True
        rota_repo.deletar.assert_called_once()
