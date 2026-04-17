from flask import Blueprint, request, jsonify, current_app
from infra.veiculo_repository import VeiculoRepository
from use_cases.veiculo_commands import CriarVeiculo, AtualizarVeiculo, DeletarVeiculo
from domain.veiculo import VeiculoCreate
from middleware.autenticacao import requer_token, requer_perfil
from exceptions import VantrackException

bp = Blueprint('veiculo', __name__, url_prefix='/api/veiculos')

@bp.route('', methods=['POST'])
@requer_token
@requer_perfil('motorista')
def criar_veiculo():
    try:
        dados = request.get_json()
        veiculo_repo = VeiculoRepository(current_app.db)
        criar_use_case = CriarVeiculo(veiculo_repo)
        
        veiculo_create = VeiculoCreate(**dados)
        resultado = criar_use_case.executar(veiculo_create)
        return jsonify(resultado), 201
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar veículo'}), 500

@bp.route('/<int:veiculo_id>', methods=['GET'])
@requer_token
def obter_veiculo(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculo = veiculo_repo.buscar_por_id(veiculo_id)
        if not veiculo:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
        return jsonify(veiculo), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter veículo'}), 500

@bp.route('', methods=['GET'])
@requer_token
def listar_veiculos():
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculos = veiculo_repo.listar_todos()
        return jsonify(veiculos), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar veículos'}), 500

@bp.route('/<int:veiculo_id>', methods=['PUT'])
@requer_token
@requer_perfil('motorista')
def atualizar_veiculo(veiculo_id):
    try:
        dados = request.get_json()
        veiculo_repo = VeiculoRepository(current_app.db)
        atualizar_use_case = AtualizarVeiculo(veiculo_repo)
        
        resultado = atualizar_use_case.executar(veiculo_id, dados)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar veículo'}), 500

@bp.route('/<int:veiculo_id>', methods=['DELETE'])
@requer_token
@requer_perfil('motorista')
def deletar_veiculo(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        deletar_use_case = DeletarVeiculo(veiculo_repo)
        
        resultado = deletar_use_case.executar(veiculo_id)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao deletar veículo'}), 500
