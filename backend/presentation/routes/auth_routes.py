from flask import Blueprint, request, jsonify, current_app
from infra.usuario_repository import UsuarioRepository
from infra.dois_fatores_repository import Dois_FatoresRepository
from use_cases.autenticar_usuario import AutenticarUsuario, CadastrarUsuario, RecuperarSenha
from use_cases.dois_fatores_commands import GenerarCodigoVerificacao2FA, EnviarCodigoVerificacao2FA
from domain.usuario import UsuarioCreate, UsuarioLogin, UsuarioRecuperarSenha
from exceptions import VantrackException
import os
import hashlib
import traceback
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        dados = request.get_json()
        
        # Validação básica - Verifica presença de campos obrigatórios
        campos_obrigatorios = ['email', 'cpf', 'nome', 'telefone', 'cidade', 'tipo_perfil', 'senha']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
        # VALIDAÇÃO CRÍTICA: Verifica se os campos estão vazios ou são None
        # Isso evita erros falsos de duplicidade no banco de dados
        campos_vazios = []
        for campo in campos_obrigatorios:
            valor = dados.get(campo)
            # Verifica se é None, string vazia, ou string apenas com espaços
            if valor is None or (isinstance(valor, str) and len(valor.strip()) == 0):
                campos_vazios.append(campo)
        
        if campos_vazios:
            return jsonify({'erro': f'Campos obrigatórios estão vazios: {", ".join(campos_vazios)}'}), 400
        
        # VALIDAÇÃO ADICIONAL: CPF e Telefone devem ter dígitos suficientes
        cpf_apenas_digitos = dados.get('cpf', '').replace('.', '').replace('-', '').replace('/', '')
        telefone_apenas_digitos = dados.get('telefone', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        if len(cpf_apenas_digitos) < 11:
            return jsonify({'erro': 'CPF deve ter pelo menos 11 dígitos'}), 400
        
        if len(telefone_apenas_digitos) < 10:
            return jsonify({'erro': 'Telefone deve ter pelo menos 10 dígitos'}), 400
        
        usuario_create = UsuarioCreate(**dados)
        usuario_repo = UsuarioRepository(current_app.db)
        cadastrar_use_case = CadastrarUsuario(usuario_repo)
        
        resultado = cadastrar_use_case.executar(usuario_create)
        return jsonify(resultado), 201
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao cadastrar: {str(e)}\n{traceback.format_exc()}")
        print(f"ERRO NO CADASTRO: {e}")
        print(traceback.format_exc())
        return jsonify({'erro': 'Erro ao cadastrar usuário'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        
        if 'email' not in dados or 'senha' not in dados:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        usuario_login = UsuarioLogin(**dados)
        usuario_repo = UsuarioRepository(current_app.db)
        autenticar_use_case = AutenticarUsuario(usuario_repo)
        
        resultado = autenticar_use_case.executar(usuario_login.email, usuario_login.senha)
        
        # Por enquanto, login simples sem 2FA
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 401
    except Exception as e:
        logger.error(f"Erro ao fazer login: {str(e)}\n{traceback.format_exc()}")
        print(f"ERRO NO LOGIN: {e}")
        print(traceback.format_exc())
        return jsonify({'erro': 'Erro ao fazer login'}), 500

@bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    try:
        dados = request.get_json()
        
        if 'email' not in dados or 'nova_senha' not in dados:
            return jsonify({'erro': 'Email e nova_senha são obrigatórios'}), 400
        
        usuario_recuperar = UsuarioRecuperarSenha(**dados)
        usuario_repo = UsuarioRepository(current_app.db)
        recuperar_use_case = RecuperarSenha(usuario_repo)
        
        resultado = recuperar_use_case.executar(usuario_recuperar.email, usuario_recuperar.nova_senha)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao recuperar senha'}), 500
