from flask import Blueprint, request, jsonify
from infra.inscricao_repository import InscricaoRepository
from infra.rota_repository import RotaRepository
from infra.usuario_repository import UsuarioRepository
from use_cases.inscricao_commands import CriarInscricao, CancelarInscricao
from domain.inscricao import InscricaoCreate
from middleware.autenticacao import requer_token, requer_perfil
from exceptions import VantrackException

bp = Blueprint('inscricao', __name__, url_prefix='/api/inscricoes')

@bp.route('', methods=['POST'])
@requer_token
@requer_perfil('aluno')
def criar_inscricao():
    try:
        dados = request.get_json()
        inscricao_repo = InscricaoRepository(request.app.db)
        rota_repo = RotaRepository(request.app.db)
        usuario_repo = UsuarioRepository(request.app.db)
        
        criar_use_case = CriarInscricao(inscricao_repo, rota_repo, usuario_repo)
        
        inscricao_create = InscricaoCreate(**dados)
        resultado = criar_use_case.executar(inscricao_create)
        return jsonify(resultado), 201
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar inscrição'}), 500

@bp.route('/<int:inscricao_id>', methods=['GET'])
@requer_token
def obter_inscricao(inscricao_id):
    try:
        inscricao_repo = InscricaoRepository(request.app.db)
        inscricao = inscricao_repo.buscar_por_id(inscricao_id)
        if not inscricao:
            return jsonify({'erro': 'Inscrição não encontrada'}), 404
        return jsonify(inscricao), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao obter inscrição'}), 500

@bp.route('', methods=['GET'])
@requer_token
def listar_inscricoes():
    try:
        inscricao_repo = InscricaoRepository(request.app.db)
        inscricoes = inscricao_repo.listar_todas()
        return jsonify(inscricoes), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar inscrições'}), 500

@bp.route('/<int:inscricao_id>/cancelar', methods=['POST'])
@requer_token
@requer_perfil('aluno')
def cancelar_inscricao(inscricao_id):
    try:
        inscricao_repo = InscricaoRepository(request.app.db)
        cancelar_use_case = CancelarInscricao(inscricao_repo)
        
        resultado = cancelar_use_case.executar(inscricao_id)
        return jsonify(resultado), 200
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao cancelar inscrição'}), 500
