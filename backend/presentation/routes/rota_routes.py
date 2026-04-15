from flask import Blueprint, request, jsonify, current_app
from infra.rota_repository import RotaRepository
from infra.usuario_repository import UsuarioRepository
from use_cases.rota_commands import CriarRota, AtualizarRota, DeletarRota
from middleware.autenticacao import AutenticacaoMiddleware
from exceptions import (
    DadosInvalidosException, UsuarioNaoEncontradoException
)

bp = Blueprint('rotas', __name__, url_prefix='/api')
auth = AutenticacaoMiddleware()

@bp.route('/motoristas/<motorista_id>/rotas', methods=['POST'])
@auth.requer_token
@auth.requer_perfil('motorista')
def criar_rota(motorista_id):
    try:
        if request.usuario_id != motorista_id:
            return jsonify({'sucesso': False, 'erro': 'Você pode criar rotas apenas para si mesmo'}), 403

        dados = request.get_json() or request.form.to_dict()

        usuario_repo = UsuarioRepository(current_app.db)
        rota_repo = RotaRepository(current_app.db)
        usecase = CriarRota(rota_repo, usuario_repo)
        rota = usecase.executar(motorista_id, dados)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Rota criada com sucesso',
            'rota': rota.to_dict()
        }), 201

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except UsuarioNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao criar rota'}), 500

@bp.route('/motoristas/<motorista_id>/rotas', methods=['GET'])
@auth.requer_token
def listar_rotas_motorista(motorista_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        rotas = rota_repo.obter_por_motorista(motorista_id)

        return jsonify({
            'sucesso': True,
            'total': len(rotas),
            'rotas': [r.to_dict() for r in rotas]
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar rotas'}), 500

@bp.route('/rotas', methods=['GET'])
@auth.requer_token
def listar_rotas_ativas():
    try:
        rota_repo = RotaRepository(current_app.db)
        rotas = rota_repo.listar_ativas()

        return jsonify({
            'sucesso': True,
            'total': len(rotas),
            'rotas': [r.to_dict() for r in rotas]
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar rotas'}), 500

@bp.route('/rotas/<rota_id>', methods=['GET'])
@auth.requer_token
def obter_rota(rota_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        rota = rota_repo.obter_por_id(rota_id)

        if not rota:
            return jsonify({'sucesso': False, 'erro': 'Rota não encontrada'}), 404

        return jsonify({
            'sucesso': True,
            'rota': rota.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao obter rota'}), 500

@bp.route('/rotas/<rota_id>', methods=['PUT'])
@auth.requer_token
@auth.requer_perfil('motorista')
def atualizar_rota(rota_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        rota = rota_repo.obter_por_id(rota_id)

        if not rota:
            return jsonify({'sucesso': False, 'erro': 'Rota não encontrada'}), 404

        if request.usuario_id != str(rota.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode atualizar suas próprias rotas'}), 403

        dados = request.get_json() or request.form.to_dict()
        usecase = AtualizarRota(rota_repo)
        rota_atualizada = usecase.executar(rota_id, dados)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Rota atualizada com sucesso',
            'rota': rota_atualizada.to_dict()
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao atualizar rota'}), 500

@bp.route('/rotas/<rota_id>', methods=['DELETE'])
@auth.requer_token
@auth.requer_perfil('motorista')
def deletar_rota(rota_id):
    try:
        rota_repo = RotaRepository(current_app.db)
        rota = rota_repo.obter_por_id(rota_id)

        if not rota:
            return jsonify({'sucesso': False, 'erro': 'Rota não encontrada'}), 404

        if request.usuario_id != str(rota.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode deletar suas próprias rotas'}), 403

        usecase = DeletarRota(rota_repo)
        usecase.executar(rota_id)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Rota deletada com sucesso'
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao deletar rota'}), 500
