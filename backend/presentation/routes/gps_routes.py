from flask import Blueprint, request, jsonify, current_app
from infra.localizacao_gps_repository import LocalizacaoGPSRepository
from infra.veiculo_repository import VeiculoRepository
from use_cases.localizacao_commands import RegistrarLocalizacao, ObterUltimaLocalizacao, ObterHistoricoLocalizacao
from middleware.autenticacao import AutenticacaoMiddleware
from exceptions import DadosInvalidosException

bp = Blueprint('gps', __name__, url_prefix='/api')
auth = AutenticacaoMiddleware()

@bp.route('/veiculos/<veiculo_id>/localizacao', methods=['POST'])
@auth.requer_token
@auth.requer_perfil('motorista')
def registrar_localizacao(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculo = veiculo_repo.obter_por_id(veiculo_id)

        if not veiculo:
            return jsonify({'sucesso': False, 'erro': 'Veículo não encontrado'}), 404

        if request.usuario_id != str(veiculo.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode registrar localizações de seus próprios veículos'}), 403

        dados = request.get_json() or request.form.to_dict()
        latitude = dados.get('latitude')
        longitude = dados.get('longitude')

        if not latitude or not longitude:
            return jsonify({'sucesso': False, 'erro': 'Latitude e longitude são obrigatórias'}), 400

        gps_repo = LocalizacaoGPSRepository(current_app.db)
        usecase = RegistrarLocalizacao(gps_repo, veiculo_repo)
        localizacao = usecase.executar(veiculo_id, latitude, longitude)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Localização registrada com sucesso',
            'localizacao': localizacao.to_dict()
        }), 201

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao registrar localização'}), 500

@bp.route('/veiculos/<veiculo_id>/localizacao/ultima', methods=['GET'])
@auth.requer_token
def obter_ultima_localizacao(veiculo_id):
    try:
        gps_repo = LocalizacaoGPSRepository(current_app.db)
        usecase = ObterUltimaLocalizacao(gps_repo)
        localizacao = usecase.executar(veiculo_id)

        return jsonify({
            'sucesso': True,
            'localizacao': localizacao
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao obter localização'}), 500

@bp.route('/veiculos/<veiculo_id>/localizacao/historico', methods=['GET'])
@auth.requer_token
def obter_historico_localizacao(veiculo_id):
    try:
        limite = request.args.get('limite', default=100, type=int)

        gps_repo = LocalizacaoGPSRepository(current_app.db)
        usecase = ObterHistoricoLocalizacao(gps_repo)
        localizacoes = usecase.executar(veiculo_id, limite)

        return jsonify({
            'sucesso': True,
            'total': len(localizacoes),
            'localizacoes': localizacoes
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao obter histórico de localizações'}), 500
