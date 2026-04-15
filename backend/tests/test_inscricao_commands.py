import pytest
from unittest.mock import Mock
from uuid import uuid4
from use_cases.inscricao_commands import CriarInscricao, CancelarInscricao
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException
from tests.factories import UsuarioFactory, RotaFactory, InscricaoFactory

class TestCriarInscricao:
    
    def test_criar_inscricao_sucesso(self):
        aluno = UsuarioFactory.criar_aluno()
        rota = RotaFactory.criar_rota()
        
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = aluno
        
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        
        inscricao_repo = Mock()
        inscricao_repo.obter_inscricao.return_value = None
        inscricao_repo.obter_por_rota.return_value = []
        inscricao_repo.criar.return_value = InscricaoFactory.criar_inscricao(aluno.id, rota.id)
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        inscricao = usecase.executar(str(aluno.id), str(rota.id))
        
        assert inscricao is not None
        inscricao_repo.criar.assert_called_once()
    
    def test_criar_inscricao_aluno_nao_existe(self):
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = None
        
        rota_repo = Mock()
        inscricao_repo = Mock()
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(UsuarioNaoEncontradoException):
            usecase.executar(str(uuid4()), str(uuid4()))
    
    def test_criar_inscricao_aluno_nao_e_aluno(self):
        motorista = UsuarioFactory.criar_motorista()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = motorista
        
        rota_repo = Mock()
        inscricao_repo = Mock()
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(UsuarioNaoEncontradoException):
            usecase.executar(str(motorista.id), str(uuid4()))
    
    def test_criar_inscricao_rota_nao_existe(self):
        aluno = UsuarioFactory.criar_aluno()
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = aluno
        
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = None
        
        inscricao_repo = Mock()
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(aluno.id), str(uuid4()))
    
    def test_criar_inscricao_rota_inativa(self):
        aluno = UsuarioFactory.criar_aluno()
        rota = RotaFactory.criar_rota()
        rota.ativa = False
        
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = aluno
        
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        
        inscricao_repo = Mock()
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(DadosInvalidosException) as exc_info:
            usecase.executar(str(aluno.id), str(rota.id))
        
        assert "inativa" in str(exc_info.value).lower()
    
    def test_criar_inscricao_ja_inscrito(self):
        aluno = UsuarioFactory.criar_aluno()
        rota = RotaFactory.criar_rota()
        inscricao_existente = InscricaoFactory.criar_inscricao(aluno.id, rota.id)
        
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = aluno
        
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        
        inscricao_repo = Mock()
        inscricao_repo.obter_inscricao.return_value = inscricao_existente
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(DadosInvalidosException) as exc_info:
            usecase.executar(str(aluno.id), str(rota.id))
        
        assert "já inscrito" in str(exc_info.value).lower()
    
    def test_criar_inscricao_rota_lotada(self):
        aluno = UsuarioFactory.criar_aluno()
        rota = RotaFactory.criar_rota()
        rota.capacidade_maxima = 1
        
        usuario_repo = Mock()
        usuario_repo.obter_por_id.return_value = aluno
        
        rota_repo = Mock()
        rota_repo.obter_por_id.return_value = rota
        
        inscricao_repo = Mock()
        inscricao_repo.obter_inscricao.return_value = None
        inscricoes_existentes = [InscricaoFactory.criar_inscricao(uuid4(), rota.id)]
        inscricao_repo.obter_por_rota.return_value = inscricoes_existentes
        
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        
        with pytest.raises(DadosInvalidosException) as exc_info:
            usecase.executar(str(aluno.id), str(rota.id))
        
        assert "lotada" in str(exc_info.value).lower()

class TestCancelarInscricao:
    
    def test_cancelar_inscricao_sucesso(self):
        inscricao = InscricaoFactory.criar_inscricao()
        inscricao_repo = Mock()
        inscricao_repo.obter_por_id.return_value = inscricao
        inscricao_repo.deletar.return_value = True
        
        usecase = CancelarInscricao(inscricao_repo)
        resultado = usecase.executar(str(inscricao.id))
        
        assert resultado is True
        inscricao_repo.deletar.assert_called_once()
    
    def test_cancelar_inscricao_nao_existe(self):
        inscricao_repo = Mock()
        inscricao_repo.obter_por_id.return_value = None
        
        usecase = CancelarInscricao(inscricao_repo)
        
        with pytest.raises(DadosInvalidosException):
            usecase.executar(str(uuid4()))
