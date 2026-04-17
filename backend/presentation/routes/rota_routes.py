from flask import Blueprint, request, jsonify, current_app
from infra.rota_repository import RotaRepository
from infra.veiculo_repository import VeiculoRepository
from infra.usuario_repository import UsuarioRepository
from use_cases.rota_commands import CriarRota, AtualizarRota, DeletarRota
from domain.rota import RotaCreate
from middleware.autenticacao import requer_token, requer_perfil
from exceptions import VantrackException

bp = Blueprint('rota', __name__, url_prefix='/api/rotas')

@bp.route('', methods=['POST'])
@requer_token
@requer_perfil('motorista')
def criar_rota():
    try:
        dados = request.get_json()
        rota_repo = RotaRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        usuario_repo = UsuarioRepository(current_app.db)
        
        criar_use_case = CriarRota(rota_repo, veiculo_repo, usuario_repo)
        
        rota_create = RotaCreate(**dados)
        resultado = criar_use_case.executar(rota_create)
        return jsonify(resultado), 201
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar rota'}), 500

@bp.route('/<int:rota_id>', methods=['GET'])
@requer_token
def obter_rota(rota_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        rota = rota_repo.buscar_por_id(rota_id)
        if not rota:
            return jsonify({'erro': 'Rota não encontrada'}), 404
        return jsonify(rota), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter rota'}), 500

@bp.route('', methods=['GET'])
@requer_token
def listar_rotas():
    try:
        rota_repo = RotaRepository(current_app.db)
        rotas = rota_repo.listar_ativas()
        return jsonify(rotas), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar rotas'}), 500

@bp.route('/<int:rota_id>', methods=['PUT'])
@requer_token
@requer_perfil('motorista')
def atualizar_rota(rota_id):
    try:
        dados = request.get_json()
        rota_repo = RotaRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        
        atualizar_use_case = AtualizarRota(rota_repo, veiculo_repo)
        resultado = atualizar_use_case.executar(rota_id, dados)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar rota'}), 500

@bp.route('/<int:rota_id>', methods=['DELETE'])
@requer_token
@requer_perfil('motorista')
def deletar_rota(rota_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        deletar_use_case = DeletarRota(rota_repo)
        
        resultado = deletar_use_case.executar(rota_id)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao deletar rota'}), 500
