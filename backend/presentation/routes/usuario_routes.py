from flask import Blueprint, request, jsonify, current_app
from infra.usuario_repository import UsuarioRepository
from use_cases.usuario_queries import ObterUsuario, ListarUsuariosPorTipo, AtualizarPerfilUsuario
from middleware.autenticacao import AutenticacaoMiddleware
from exceptions import (
    UsuarioNaoEncontradoException, DadosInvalidosException
)

bp = Blueprint('usuarios', __name__, url_prefix='/api')
auth = AutenticacaoMiddleware()

@bp.route('/usuarios/<usuario_id>', methods=['GET'])
@auth.requer_token
def obter_usuario(usuario_id):
    try:
        repo = UsuarioRepository(current_app.db)
        usecase = ObterUsuario(repo)
        usuario = usecase.executar(usuario_id)

        return jsonify({
            'sucesso': True,
            'usuario': usuario
        }), 200

    except UsuarioNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao obter usuário'}), 500

@bp.route('/alunos', methods=['GET'])
@auth.requer_token
@auth.requer_perfil('aluno', 'motorista')
def listar_alunos():
    try:
        repo = UsuarioRepository(current_app.db)
        usecase = ListarUsuariosPorTipo(repo)
        alunos = usecase.executar('aluno')

        return jsonify({
            'sucesso': True,
            'total': len(alunos),
            'alunos': alunos
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar alunos'}), 500

@bp.route('/motoristas', methods=['GET'])
@auth.requer_token
@auth.requer_perfil('aluno', 'motorista')
def listar_motoristas():
    try:
        repo = UsuarioRepository(current_app.db)
        usecase = ListarUsuariosPorTipo(repo)
        motoristas = usecase.executar('motorista')

        return jsonify({
            'sucesso': True,
            'total': len(motoristas),
            'motoristas': motoristas
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar motoristas'}), 500

@bp.route('/usuarios/<usuario_id>', methods=['PUT'])
@auth.requer_token
def atualizar_usuario(usuario_id):
    try:
        if request.usuario_id != usuario_id:
            return jsonify({'sucesso': False, 'erro': 'Você só pode atualizar seu próprio perfil'}), 403

        dados = request.get_json() or request.form.to_dict()

        repo = UsuarioRepository(current_app.db)
        usecase = AtualizarPerfilUsuario(repo)
        usuario_atualizado = usecase.executar(usuario_id, dados)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Perfil atualizado com sucesso',
            'usuario': usuario_atualizado
        }), 200

    except UsuarioNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao atualizar usuário'}), 500
