import pytest
from datetime import date
from use_cases.dashboard_commands import (
    ObtenerDashboardMotorista,
    ObtenerDashboardAluno,
    ConfirmarPresenca,
    EnviarMensagem,
    ObtenerConversa,
    ListarMensagensNaoLidas,
    AtualizarEndereco,
    UsuarioNaoAutorizado
)
from exceptions import VantrackException
from domain.dashboard import PresencaDiaria, MensagemChat, EnderecoAluno


@pytest.mark.unit
class TestObtenerDashboardMotorista:
    
    def test_motorista_nao_autorizado(self, mocker):
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'aluno'}
        
        rota_repo = mocker.MagicMock()
        inscricao_repo = mocker.MagicMock()
        presenca_repo = mocker.MagicMock()
        mensagem_repo = mocker.MagicMock()
        
        use_case = ObtenerDashboardMotorista(
            usuario_repo, rota_repo, inscricao_repo, presenca_repo, mensagem_repo
        )
        
        with pytest.raises(UsuarioNaoAutorizado):
            use_case.executar('1')
    
    def test_motorista_sem_rotas(self, mocker):
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'motorista', 'nome': 'João'}
        
        rota_repo = mocker.MagicMock()
        rota_repo.listar_por_motorista.return_value = []
        
        inscricao_repo = mocker.MagicMock()
        presenca_repo = mocker.MagicMock()
        mensagem_repo = mocker.MagicMock()
        mensagem_repo.contar_nao_lidas_por_usuario.return_value = 0
        
        use_case = ObtenerDashboardMotorista(
            usuario_repo, rota_repo, inscricao_repo, presenca_repo, mensagem_repo
        )
        
        resultado = use_case.executar('1')
        
        assert resultado['motorista']['id'] == '1'
        assert resultado['rotas'] == []
        assert resultado['mensagens_nao_lidas'] == 0


@pytest.mark.unit
class TestConfirmarPresenca:
    
    def test_aluno_nao_autorizado(self, mocker):
        presenca_repo = mocker.MagicMock()
        inscricao_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'motorista'}
        
        use_case = ConfirmarPresenca(presenca_repo, inscricao_repo, usuario_repo)
        
        with pytest.raises(UsuarioNaoAutorizado):
            use_case.executar('1', True)
    
    def test_aluno_sem_inscricoes(self, mocker):
        presenca_repo = mocker.MagicMock()
        inscricao_repo = mocker.MagicMock()
        inscricao_repo.listar_por_aluno.return_value = []
        
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'aluno'}
        
        use_case = ConfirmarPresenca(presenca_repo, inscricao_repo, usuario_repo)
        
        with pytest.raises(VantrackException):
            use_case.executar('1', True)


@pytest.mark.unit
class TestEnviarMensagem:
    
    def test_mensagem_vazia(self, mocker):
        mensagem_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.side_effect = lambda id: {'id': id, 'nome': 'Usuário'}
        
        use_case = EnviarMensagem(mensagem_repo, usuario_repo)
        
        with pytest.raises(VantrackException):
            use_case.executar('1', '2', '')
    
    def test_enviar_mensagem_sucesso(self, mocker):
        mensagem_repo = mocker.MagicMock()
        mensagem_repo.criar.return_value = {
            'id': 'msg-1',
            'remetente_id': '1',
            'destinatario_id': '2',
            'texto': 'Olá',
            'lido': False
        }
        
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.side_effect = lambda id: {'id': id, 'nome': 'Usuário'}
        
        use_case = EnviarMensagem(mensagem_repo, usuario_repo)
        resultado = use_case.executar('1', '2', 'Olá')
        
        assert resultado['id'] == 'msg-1'
        assert resultado['texto'] == 'Olá'
        assert resultado['lido'] == False


@pytest.mark.unit
class TestObtenerConversa:
    
    def test_usuario_nao_encontrado(self, mocker):
        mensagem_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.side_effect = [{'id': '1'}, None]
        
        use_case = ObtenerConversa(mensagem_repo, usuario_repo)
        
        with pytest.raises(VantrackException):
            use_case.executar('1', '2')
    
    def test_obter_conversa_sucesso(self, mocker):
        mensagem_repo = mocker.MagicMock()
        mensagem_repo.listar_conversa.return_value = [
            {'id': 'msg-1', 'texto': 'Oi'},
            {'id': 'msg-2', 'texto': 'Olá'}
        ]
        mensagem_repo.marcar_conversa_como_lida.return_value = None
        
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.side_effect = [
            {'id': '1', 'nome': 'João'},
            {'id': '2', 'nome': 'Maria'}
        ]
        
        use_case = ObtenerConversa(mensagem_repo, usuario_repo)
        resultado = use_case.executar('1', '2', 50)
        
        assert resultado['usuario']['nome'] == 'João'
        assert resultado['outro_usuario']['nome'] == 'Maria'
        assert len(resultado['mensagens']) == 2


@pytest.mark.unit
class TestListarMensagensNaoLidas:
    
    def test_listar_nao_lidas_sucesso(self, mocker):
        mensagem_repo = mocker.MagicMock()
        mensagem_repo.listar_nao_lidas_por_usuario.return_value = [
            {'id': 'msg-1', 'texto': 'Nova mensagem'}
        ]
        mensagem_repo.contar_nao_lidas_por_usuario.return_value = 1
        
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'nome': 'João'}
        
        use_case = ListarMensagensNaoLidas(mensagem_repo, usuario_repo)
        resultado = use_case.executar('1')
        
        assert resultado['total_nao_lidas'] == 1
        assert len(resultado['mensagens']) == 1


@pytest.mark.unit
class TestAtualizarEndereco:
    
    def test_aluno_nao_autorizado(self, mocker):
        endereco_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'motorista'}
        
        inscricao_repo = mocker.MagicMock()
        
        use_case = AtualizarEndereco(endereco_repo, usuario_repo, inscricao_repo)
        
        with pytest.raises(UsuarioNaoAutorizado):
            use_case.executar('1', 'Rua A', 'Rua B')
    
    def test_aluno_sem_inscricoes(self, mocker):
        endereco_repo = mocker.MagicMock()
        usuario_repo = mocker.MagicMock()
        usuario_repo.buscar_por_id.return_value = {'id': '1', 'tipo_perfil': 'aluno'}
        
        inscricao_repo = mocker.MagicMock()
        inscricao_repo.listar_por_aluno.return_value = []
        
        use_case = AtualizarEndereco(endereco_repo, usuario_repo, inscricao_repo)
        
        with pytest.raises(VantrackException):
            use_case.executar('1', 'Rua A', 'Rua B')
