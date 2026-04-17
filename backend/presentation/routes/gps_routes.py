from flask import Blueprint, request, jsonify, current_app
from infra.localizacao_gps_repository import LocalizacaoGPSRepository
from infra.veiculo_repository import VeiculoRepository
from use_cases.localizacao_commands import RegistrarLocalizacao, ObterUltimaLocalizacao, ObterHistoricoLocalizacao
from domain.localizacao_gps import LocalizacaoGPSCreate
from middleware.autenticacao import requer_token, requer_perfil
from exceptions import VantrackException

bp = Blueprint('gps', __name__, url_prefix='/api/gps')

@bp.route('/registrar', methods=['POST'])
@requer_token
@requer_perfil('motorista')
def registrar_localizacao():
    try:
        dados = request.get_json()
        localizacao_repo = LocalizacaoGPSRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        
        registrar_use_case = RegistrarLocalizacao(localizacao_repo, veiculo_repo)
        
        localizacao_create = LocalizacaoGPSCreate(**dados)
        resultado = registrar_use_case.executar(localizacao_create)
        return jsonify(resultado), 201
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao registrar localização'}), 500

@bp.route('/<int:veiculo_id>/ultima', methods=['GET'])
@requer_token
def obter_ultima_localizacao(veiculo_id):
    try:
        localizacao_repo = LocalizacaoGPSRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        
        obter_use_case = ObterUltimaLocalizacao(localizacao_repo, veiculo_repo)
        resultado = obter_use_case.executar(veiculo_id)
        
        if not resultado:
            return jsonify({'erro': 'Nenhuma localização registrada'}), 404
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter última localização'}), 500

@bp.route('/<int:veiculo_id>/historico', methods=['GET'])
@requer_token
def obter_historico_localizacao(veiculo_id):
    try:
        limite = request.args.get('limite', 100, type=int)
        localizacao_repo = LocalizacaoGPSRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        
        obter_use_case = ObterHistoricoLocalizacao(localizacao_repo, veiculo_repo)
        resultado = obter_use_case.executar(veiculo_id, limite)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter histórico de localizações'}), 500
