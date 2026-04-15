import pytest
from unittest.mock import Mock, MagicMock, patch
from uuid import uuid4
from domain.veiculo import Veiculo
from infra.veiculo_repository import VeiculoRepository
from use_cases.veiculo_commands import CriarVeiculo, AtualizarVeiculo, DeletarVeiculo
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException
from tests.factories import UsuarioFactory, VeiculoFactory

class TestCriarVeiculo:
    
    def test_criar_veiculo_sucesso(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        veiculo_repo = Mock()
        veiculo_repo.obter_por_placa.return_value = None
        veiculo_repo.criar.return_value = VeiculoFactory.criar_veiculo(motorista.id)
        
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        dados = {
            'placa': 'ABC1234',
            'modelo': 'Mercedes Sprinter',
            'ano': 2022,
            'capacidade': 50
        }
        
        veiculo = usecase.executar(str(motorista.id), dados)
        
        assert veiculo is not None
        assert veiculo.placa == 'ABC1234'
        assert veiculo.modelo == 'Mercedes Sprinter'
        veiculo_repo.criar.assert_called_once()
    
    def test_criar_veiculo_motorista_nao_existe(self):
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = None
        
        veiculo_repo = Mock()
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        
        dados = {'placa': 'ABC1234', 'modelo': 'Mercedes', 'ano': 2022, 'capacidade': 50}
        
        with pytest.raises(UsuarioNaoEncontradoException):
            usecase.executar(str(uuid4()), dados)
    
    def test_criar_veiculo_placa_duplicada(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        veiculo_existente = VeiculoFactory.criar_veiculo(motorista.id, "ABC1234")
        veiculo_repo = Mock()
        veiculo_repo.obter_por_placa.return_value = veiculo_existente
        
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        dados = {'placa': 'ABC1234', 'modelo': 'Mercedes', 'ano': 2022, 'capacidade': 50}
        
        with pytest.raises(DadosInvalidosException) as exc_info:
            usecase.executar(str(motorista.id), dados)
        
        assert "já cadastrada" in str(exc_info.value)
    
    def test_criar_veiculo_placa_invalida(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        veiculo_repo = Mock()
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        
        dados = {'placa': 'AB', 'modelo': 'Mercedes', 'ano': 2022, 'capacidade': 50}
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)
    
    def test_criar_veiculo_ano_invalido(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        veiculo_repo = Mock()
        veiculo_repo.obter_por_placa.return_value = None
        
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        dados = {'placa': 'ABC1234', 'modelo': 'Mercedes', 'ano': 1950, 'capacidade': 50}
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)
    
    def test_criar_veiculo_capacidade_invalida(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        veiculo_repo = Mock()
        veiculo_repo.obter_por_placa.return_value = None
        
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        dados = {'placa': 'ABC1234', 'modelo': 'Mercedes', 'ano': 2022, 'capacidade': 600}
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(motorista.id), dados)

class TestAtualizarVeiculo:
    
    def test_atualizar_veiculo_sucesso(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        veiculo_repo.obter_por_placa.return_value = None
        veiculo_atualizado = VeiculoFactory.criar_veiculo(veiculo.motorista_id, "XYZ9999")
        veiculo_repo.atualizar.return_value = veiculo_atualizado
        
        usecase = AtualizarVeiculo(veiculo_repo)
        dados = {'placa': 'XYZ9999', 'ano': 2023}
        
        resultado = usecase.executar(str(veiculo.id), dados)
        
        assert resultado is not None
        veiculo_repo.atualizar.assert_called_once()
    
    def test_atualizar_veiculo_nao_existe(self):
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = None
        
        usecase = AtualizarVeiculo(veiculo_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(uuid4()), {})
    
    def test_atualizar_veiculo_placa_invalida(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        
        usecase = AtualizarVeiculo(veiculo_repo)
        dados = {'placa': 'AB'}
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(veiculo.id), dados)

class TestDeletarVeiculo:
    
    def test_deletar_veiculo_sucesso(self):
        veiculo = VeiculoFactory.criar_veiculo()
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = veiculo
        veiculo_repo.deletar.return_value = True
        
        usecase = DeletarVeiculo(veiculo_repo)
        resultado = usecase.executar(str(veiculo.id))
        
        assert resultado is True
        veiculo_repo.deletar.assert_called_once()
    
    def test_deletar_veiculo_nao_existe(self):
        veiculo_repo = Mock()
        veiculo_repo.obter_por_id.return_value = None
        
        usecase = DeletarVeiculo(veiculo_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(uuid4()))
