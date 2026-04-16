from flask import Blueprint, request, jsonify
from infra.endereco_repository import EnderecoRepository
from infra.presenca_diaria_repository import PresencaDiariaRepository
from infra.mensagem_chat_repository import MensagemChatRepository
from infra.usuario_repository import UsuarioRepository
from infra.rota_repository import RotaRepository
from infra.inscricao_repository import InscricaoRepository
from infra.veiculo_repository import VeiculoRepository
from infra.localizacao_gps_repository import LocalizacaoGPSRepository
from use_cases.dashboard_commands import (
    ObtenerDashboardMotorista,
    ObtenerDashboardAluno,
    ConfirmarPresenca,
    EnviarMensagem,
    ObtenerConversa,
    ListarMensagensNaoLidas,
    AtualizarEndereco
)
from middleware.autenticacao import requer_token, requer_perfil
from exceptions import VantrackException

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/motorista', methods=['GET'])
@requer_token
@requer_perfil('motorista')
def dashboard_motorista():
    try:
        motorista_id = request.usuario_id
        
        usuario_repo = UsuarioRepository(request.app.db)
        rota_repo = RotaRepository(request.app.db)
        inscricao_repo = InscricaoRepository(request.app.db)
        presenca_repo = PresencaDiariaRepository(request.app.db)
        mensagem_repo = MensagemChatRepository(request.app.db)
        
        use_case = ObtenerDashboardMotorista(
            usuario_repo, rota_repo, inscricao_repo, presenca_repo, mensagem_repo
        )
        
        resultado = use_case.executar(motorista_id)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 403
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter dashboard do motorista'}), 500

@bp.route('/aluno', methods=['GET'])
@requer_token
@requer_perfil('aluno')
def dashboard_aluno():
    try:
        aluno_id = request.usuario_id
        
        usuario_repo = UsuarioRepository(request.app.db)
        inscricao_repo = InscricaoRepository(request.app.db)
        presenca_repo = PresencaDiariaRepository(request.app.db)
        endereco_repo = EnderecoRepository(request.app.db)
        rota_repo = RotaRepository(request.app.db)
        veiculo_repo = VeiculoRepository(request.app.db)
        localizacao_repo = LocalizacaoGPSRepository(request.app.db)
        
        use_case = ObtenerDashboardAluno(
            usuario_repo, inscricao_repo, presenca_repo, endereco_repo, 
            rota_repo, veiculo_repo, localizacao_repo
        )
        
        resultado = use_case.executar(aluno_id)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 403
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter dashboard do aluno'}), 500

@bp.route('/presenca', methods=['POST'])
@requer_token
@requer_perfil('aluno')
def confirmar_presenca():
    try:
        aluno_id = request.usuario_id
        dados = request.get_json()
        
        if 'vai_embarcar' not in dados:
            return jsonify({'erro': 'Campo vai_embarcar é obrigatório'}), 400
        
        inscricao_repo = InscricaoRepository(request.app.db)
        presenca_repo = PresencaDiariaRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        
        use_case = ConfirmarPresenca(presenca_repo, inscricao_repo, usuario_repo)
        resultado = use_case.executar(aluno_id, dados['vai_embarcar'])
        
        return jsonify(resultado), 201
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao confirmar presença'}), 500

@bp.route('/mensagens', methods=['POST'])
@requer_token
def enviar_mensagem():
    try:
        remetente_id = request.usuario_id
        dados = request.get_json()
        
        if 'destinatario_id' not in dados or 'texto' not in dados:
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        mensagem_repo = MensagemChatRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        
        use_case = EnviarMensagem(mensagem_repo, usuario_repo)
        resultado = use_case.executar(remetente_id, dados['destinatario_id'], dados['texto'])
        
        return jsonify(resultado), 201
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao enviar mensagem'}), 500

@bp.route('/mensagens/<outro_usuario_id>', methods=['GET'])
@requer_token
def obter_conversa(outro_usuario_id):
    try:
        usuario_id = request.usuario_id
        limit = request.args.get('limit', 50, type=int)
        
        mensagem_repo = MensagemChatRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        
        use_case = ObtenerConversa(mensagem_repo, usuario_repo)
        resultado = use_case.executar(usuario_id, outro_usuario_id, limit)
        
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter conversa'}), 500

@bp.route('/mensagens-nao-lidas', methods=['GET'])
@requer_token
def listar_nao_lidas():
    try:
        usuario_id = request.usuario_id
        
        mensagem_repo = MensagemChatRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        
        use_case = ListarMensagensNaoLidas(mensagem_repo, usuario_repo)
        resultado = use_case.executar(usuario_id)
        
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar mensagens não lidas'}), 500

@bp.route('/endereco', methods=['POST'])
@requer_token
@requer_perfil('aluno')
def atualizar_endereco():
    try:
        aluno_id = request.usuario_id
        dados = request.get_json()
        
        campos_obrigatorios = ['endereco_coleta', 'endereco_entrega']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        endereco_repo = EnderecoRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        inscricao_repo = InscricaoRepository(request.app.db)
        
        use_case = AtualizarEndereco(endereco_repo, usuario_repo, inscricao_repo)
        resultado = use_case.executar(
            aluno_id,
            dados['endereco_coleta'],
            dados['endereco_entrega'],
            dados.get('lat_coleta'),
            dados.get('lon_coleta'),
            dados.get('lat_entrega'),
            dados.get('lon_entrega')
        )
        
        return jsonify(resultado), 201
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar endereço'}), 500
