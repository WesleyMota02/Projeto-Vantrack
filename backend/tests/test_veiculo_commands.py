import pytest
from exceptions import DadosInvalidos, VeiculoNaoEncontrado
from use_cases.veiculo_commands import CriarVeiculo, AtualizarVeiculo, DeletarVeiculo
from domain.veiculo import VeiculoCreate

class TestCriarVeiculo:
    @pytest.mark.unit
    def test_criar_veiculo_com_sucesso(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.placa_existe.return_value = False
        veiculo_repo.criar.return_value = {'id': 1, 'placa': 'ABC1234', 'modelo': 'Sprinter'}
        
        criar_use_case = CriarVeiculo(veiculo_repo)
        veiculo = VeiculoCreate(placa='ABC1234', modelo='Sprinter', ano=2023, capacidade=50, motorista_id=1)
        resultado = criar_use_case.executar(veiculo)
        
        assert resultado['placa'] == 'ABC1234'
        veiculo_repo.criar.assert_called_once()

    @pytest.mark.unit
    def test_criar_veiculo_placa_duplicada(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.placa_existe.return_value = True
        
        criar_use_case = CriarVeiculo(veiculo_repo)
        veiculo = VeiculoCreate(placa='ABC1234', modelo='Sprinter', ano=2023, capacidade=50, motorista_id=1)
        
        with pytest.raises(DadosInvalidos):
            criar_use_case.executar(veiculo)

    @pytest.mark.unit
    def test_criar_veiculo_validacao_ano(self, mocker):
        with pytest.raises(ValueError):
            VeiculoCreate(placa='ABC1234', modelo='Sprinter', ano=1999, capacidade=50, motorista_id=1)

    @pytest.mark.unit
    def test_criar_veiculo_validacao_capacidade(self, mocker):
        with pytest.raises(ValueError):
            VeiculoCreate(placa='ABC1234', modelo='Sprinter', ano=2023, capacidade=150, motorista_id=1)

    @pytest.mark.unit
    def test_criar_veiculo_capacidade_zero(self, mocker):
        with pytest.raises(ValueError):
            VeiculoCreate(placa='ABC1234', modelo='Sprinter', ano=2023, capacidade=0, motorista_id=1)

class TestAtualizarVeiculo:
    @pytest.mark.unit
    def test_atualizar_veiculo_com_sucesso(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234', 'modelo': 'Sprinter'}
        veiculo_repo.placa_existe.return_value = False
        veiculo_repo.atualizar.return_value = {'id': 1, 'placa': 'XYZ9999', 'modelo': 'Sprinter'}
        
        atualizar_use_case = AtualizarVeiculo(veiculo_repo)
        resultado = atualizar_use_case.executar(1, {'placa': 'XYZ9999'})
        
        assert resultado['placa'] == 'XYZ9999'

    @pytest.mark.unit
    def test_atualizar_veiculo_nao_encontrado(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.buscar_por_id.return_value = None
        
        atualizar_use_case = AtualizarVeiculo(veiculo_repo)
        
        with pytest.raises(VeiculoNaoEncontrado):
            atualizar_use_case.executar(999, {'placa': 'XYZ9999'})

    @pytest.mark.unit
    def test_atualizar_veiculo_placa_duplicada(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234', 'modelo': 'Sprinter'}
        veiculo_repo.placa_existe.return_value = True
        
        atualizar_use_case = AtualizarVeiculo(veiculo_repo)
        
        with pytest.raises(DadosInvalidos):
            atualizar_use_case.executar(1, {'placa': 'OUTRO'})

class TestDeletarVeiculo:
    @pytest.mark.unit
    def test_deletar_veiculo_com_sucesso(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.buscar_por_id.return_value = {'id': 1, 'placa': 'ABC1234'}
        
        deletar_use_case = DeletarVeiculo(veiculo_repo)
        resultado = deletar_use_case.executar(1)
        
        assert 'mensagem' in resultado
        veiculo_repo.deletar.assert_called_once_with(1)

    @pytest.mark.unit
    def test_deletar_veiculo_nao_encontrado(self, mocker):
        veiculo_repo = mocker.MagicMock()
        veiculo_repo.buscar_por_id.return_value = None
        
        deletar_use_case = DeletarVeiculo(veiculo_repo)
        
        with pytest.raises(VeiculoNaoEncontrado):
            deletar_use_case.executar(999)
