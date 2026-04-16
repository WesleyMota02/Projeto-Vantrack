from flask import Blueprint, request, jsonify
from infra.usuario_repository import UsuarioRepository
from use_cases.autenticar_usuario import AutenticarUsuario, CadastrarUsuario, RecuperarSenha
from domain.usuario import UsuarioCreate, UsuarioLogin, UsuarioRecuperarSenha
from exceptions import VantrackException
import os

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        dados = request.get_json()
        
        # Validação básica
        campos_obrigatorios = ['email', 'cpf', 'nome', 'telefone', 'cidade', 'tipo_perfil', 'senha']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        usuario_create = UsuarioCreate(**dados)
        usuario_repo = UsuarioRepository(request.app.db)
        cadastrar_use_case = CadastrarUsuario(usuario_repo)
        
        resultado = cadastrar_use_case.executar(usuario_create)
        return jsonify(resultado), 201
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao cadastrar usuário'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        
        if 'email' not in dados or 'senha' not in dados:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        usuario_login = UsuarioLogin(**dados)
        usuario_repo = UsuarioRepository(request.app.db)
        autenticar_use_case = AutenticarUsuario(usuario_repo)
        
        resultado = autenticar_use_case.executar(usuario_login.email, usuario_login.senha)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 401
    except Exception as e:
        return jsonify({'erro': 'Erro ao fazer login'}), 500

@bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    try:
        dados = request.get_json()
        
        if 'email' not in dados or 'nova_senha' not in dados:
            return jsonify({'erro': 'Email e nova_senha são obrigatórios'}), 400
        
        usuario_recuperar = UsuarioRecuperarSenha(**dados)
        usuario_repo = UsuarioRepository(request.app.db)
        recuperar_use_case = RecuperarSenha(usuario_repo)
        
        resultado = recuperar_use_case.executar(usuario_recuperar.email, usuario_recuperar.nova_senha)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao recuperar senha'}), 500
