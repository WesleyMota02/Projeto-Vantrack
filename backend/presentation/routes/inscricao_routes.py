from flask import Blueprint, request, jsonify, current_app
from infra.inscricao_repository import InscricaoRepository
from infra.usuario_repository import UsuarioRepository
from infra.rota_repository import RotaRepository
from use_cases.inscricao_commands import CriarInscricao, CancelarInscricao
from middleware.autenticacao import AutenticacaoMiddleware
from exceptions import DadosInvalidosException, UsuarioNaoEncontradoException

bp = Blueprint('inscricoes', __name__, url_prefix='/api')
auth = AutenticacaoMiddleware()

@bp.route('/alunos/<aluno_id>/inscricoes', methods=['POST'])
@auth.requer_token
@auth.requer_perfil('aluno')
def criar_inscricao(aluno_id):
    try:
        if request.usuario_id != aluno_id:
            return jsonify({'sucesso': False, 'erro': 'Você pode se inscrever apenas em rotas para si mesmo'}), 403

        dados = request.get_json() or request.form.to_dict()
        rota_id = dados.get('rota_id')

        if not rota_id:
            return jsonify({'sucesso': False, 'erro': 'ID da rota é obrigatório'}), 400

        usuario_repo = UsuarioRepository(current_app.db)
        rota_repo = RotaRepository(current_app.db)
        inscricao_repo = InscricaoRepository(current_app.db)
        usecase = CriarInscricao(inscricao_repo, usuario_repo, rota_repo)
        inscricao = usecase.executar(aluno_id, rota_id)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Inscrição realizada com sucesso',
            'inscricao': inscricao.to_dict()
        }), 201

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except UsuarioNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao criar inscrição'}), 500

@bp.route('/alunos/<aluno_id>/inscricoes', methods=['GET'])
@auth.requer_token
def listar_inscricoes_aluno(aluno_id):
    try:
        if request.usuario_id != aluno_id:
            return jsonify({'sucesso': False, 'erro': 'Você só pode visualizar suas próprias inscrições'}), 403

        inscricao_repo = InscricaoRepository(current_app.db)
        inscricoes = inscricao_repo.obter_por_aluno(aluno_id)

        return jsonify({
            'sucesso': True,
            'total': len(inscricoes),
            'inscricoes': [i.to_dict() for i in inscricoes]
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar inscrições'}), 500

@bp.route('/rotas/<rota_id>/inscricoes', methods=['GET'])
@auth.requer_token
def listar_inscricoes_rota(rota_id):
    try:
        inscricao_repo = InscricaoRepository(current_app.db)
        rota_repo = RotaRepository(current_app.db)

        rota = rota_repo.obter_por_id(rota_id)
        if not rota:
            return jsonify({'sucesso': False, 'erro': 'Rota não encontrada'}), 404

        if request.usuario_id != str(rota.motorista_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode visualizar inscrições de suas próprias rotas'}), 403

        inscricoes = inscricao_repo.obter_por_rota(rota_id)

        return jsonify({
            'sucesso': True,
            'total': len(inscricoes),
            'capacidade_disponivel': rota.capacidade_maxima - len(inscricoes),
            'inscricoes': [i.to_dict() for i in inscricoes]
        }), 200

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao listar inscrições'}), 500

@bp.route('/inscricoes/<inscricao_id>', methods=['DELETE'])
@auth.requer_token
@auth.requer_perfil('aluno')
def cancelar_inscricao(inscricao_id):
    try:
        inscricao_repo = InscricaoRepository(current_app.db)
        inscricao = inscricao_repo.obter_por_id(inscricao_id)

        if not inscricao:
            return jsonify({'sucesso': False, 'erro': 'Inscrição não encontrada'}), 404

        if request.usuario_id != str(inscricao.aluno_id):
            return jsonify({'sucesso': False, 'erro': 'Você só pode cancelar suas próprias inscrições'}), 403

        usecase = CancelarInscricao(inscricao_repo)
        usecase.executar(inscricao_id)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Inscrição cancelada com sucesso'
        }), 200

    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao cancelar inscrição'}), 500
