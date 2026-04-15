from flask import Blueprint, request, jsonify, current_app
from infra.veiculo_repository import VeiculoRepository
from infra.usuario_repository import UsuarioRepository
from use_cases.veiculo_commands import CriarVeiculo, AtualizarVeiculo, DeletarVeiculo
from use_cases.usuario_queries import ObterUsuario
from middleware.autenticacao import AutenticacaoMiddleware
from presentation.dtos import UsuarioResponseDTO
from exceptions import (
    DadosInvalidosException, UsuarioNaoEncontradoException
)

bp = Blueprint('veiculos', __name__, url_prefix='/api')
auth = AutenticacaoMiddleware()

@bp.route('/motoristas/<motorista_id>/veiculos', methods=['POST'])
@auth.requer_token
@auth.requer_perfil('motorista')
def criar_veiculo(motorista_id):
    try:
        if request.usuario_id != motorista_id:
            return jsonify({'sucesso': False, 'erro': 'Você pode criar veículos apenas para si mesmo'}), 403

        dados = request.get_json() or request.form.to_dict()

        usuario_repo = UsuarioRepository(current_app.db)
        veiculo_repo = VeiculoRepository(current_app.db)
        usecase = CriarVeiculo(veiculo_repo, usuario_repo)
        veiculo = usecase.executar(motorista_id, dados)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Veículo criado com sucesso',
            'veiculo': veiculo.to_dict()
        }), 201

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except UsuarioNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao criar veículo'}), 500

@bp.route('/motoristas/<motorista_id>/veiculos', methods=['GET'])
@auth.requer_token
def listar_veiculos_motorista(motorista_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculos = veiculo_repo.obter_por_motorista(motorista_id)

        return jsonify({
            'sucesso': True,
            'total': len(veiculos),
            'veiculos': [v.to_dict() for v in veiculos]
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar veículos'}), 500

@bp.route('/veiculos/<veiculo_id>', methods=['GET'])
@auth.requer_token
def obter_veiculo(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculo = veiculo_repo.obter_por_id(veiculo_id)

        if not veiculo:
            return jsonify({'sucesso': False, 'erro': 'Veículo não encontrado'}), 404

        return jsonify({
            'sucesso': True,
            'veiculo': veiculo.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao obter veículo'}), 500

@bp.route('/veiculos/<veiculo_id>', methods=['PUT'])
@auth.requer_token
@auth.requer_perfil('motorista')
def atualizar_veiculo(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculo = veiculo_repo.obter_por_id(veiculo_id)

        if not veiculo:
            return jsonify({'sucesso': False, 'erro': 'Veículo não encontrado'}), 404

        if request.usuario_id != str(veiculo.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode atualizar seus próprios veículos'}), 403

        dados = request.get_json() or request.form.to_dict()
        usecase = AtualizarVeiculo(veiculo_repo)
        veiculo_atualizado = usecase.executar(veiculo_id, dados)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Veículo atualizado com sucesso',
            'veiculo': veiculo_atualizado.to_dict()
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao atualizar veículo'}), 500

@bp.route('/veiculos/<veiculo_id>', methods=['DELETE'])
@auth.requer_token
@auth.requer_perfil('motorista')
def deletar_veiculo(veiculo_id):
    try:
        veiculo_repo = VeiculoRepository(current_app.db)
        veiculo = veiculo_repo.obter_por_id(veiculo_id)

        if not veiculo:
            return jsonify({'sucesso': False, 'erro': 'Veículo não encontrado'}), 404

        if request.usuario_id != str(veiculo.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode deletar seus próprios veículos'}), 403

        usecase = DeletarVeiculo(veiculo_repo)
        usecase.executar(veiculo_id)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Veículo deletado com sucesso'
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao deletar veículo'}), 500
