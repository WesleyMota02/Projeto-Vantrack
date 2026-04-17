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
        
        # Validação básica
        campos_obrigatorios = ['email', 'cpf', 'nome', 'telefone', 'cidade', 'tipo_perfil', 'senha']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
        
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
        
        # NOVO: Detecção de novo dispositivo para ativar 2FA
        usuario_id = resultado['usuario_id']
        user_agent = request.headers.get('User-Agent', 'unknown')
        ip_address = request.remote_addr
        dispositivo_hash = hashlib.sha256(f"{user_agent}:{ip_address}".encode()).hexdigest()
        
        # Verificar se este dispositivo já foi verificado
        dois_fatores_repo = Dois_FatoresRepository(current_app.db)
        codigo_ativo = dois_fatores_repo.buscar_ativo_por_usuario_e_dispositivo(usuario_id, dispositivo_hash)
        
        # Se não há código ativo para este dispositivo, é um novo dispositivo - requer 2FA
        if not codigo_ativo:
            # Gerar código 2FA
            generar_use_case = GenerarCodigoVerificacao2FA(usuario_repo, dois_fatores_repo)
            codigo_resultado = generar_use_case.executar(usuario_id, dispositivo_hash, 'SMS')
            
            # Enviar código
            enviar_use_case = EnviarCodigoVerificacao2FA(dois_fatores_repo)
            try:
                enviar_use_case.executar(codigo_resultado['dois_fatores_id'])
            except:
                # Se falhar enviar, continua mesmo assim - usuário pode reenviar
                pass
            
            # Retornar response indicando que 2FA é necessário
            return jsonify({
                'requer_2fa': True,
                'dois_fatores_id': codigo_resultado['dois_fatores_id'],
                'usuario_id': usuario_id,
                'metodo': codigo_resultado['metodo'],
                'telefone_mascarado': codigo_resultado['telefone_sms_mascarado'],
                'mensagem': 'Novo dispositivo detectado. Verifique seu celular e insira o código de 6 dígitos.'
            }), 200
        else:
            # Dispositivo conhecido - login normal sem 2FA
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
        usuario_repo = UsuarioRepository(current_app.db)
        recuperar_use_case = RecuperarSenha(usuario_repo)
        
        resultado = recuperar_use_case.executar(usuario_recuperar.email, usuario_recuperar.nova_senha)
        return jsonify(resultado), 200
    
    except VantrackException as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro ao recuperar senha'}), 500
