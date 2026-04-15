from flask import Blueprint, request, jsonify, current_app
from infra.usuario_repository import UsuarioRepository
from use_cases.cadastrar_usuario import CadastrarUsuario
from use_cases.autenticar_usuario import AutenticarUsuario
from use_cases.recuperar_senha import RecuperarSenha
from presentation.dtos import UsuarioResponseDTO, LoginResponseDTO, CadastroDTO, LoginDTO
from exceptions import (
    UsuarioJaExisteException, DadosInvalidosException, EmailNaoEncontradoException,
    SenhaInvalidaException, ErroGeracaoTokenException
)

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/alunos/cadastrar', methods=['POST'])
def cadastrar_aluno():
    try:
        dados = request.get_json() or request.form.to_dict()
        dados['tipo_perfil'] = 'aluno'

        repo = UsuarioRepository(current_app.db)
        usecase = CadastrarUsuario(repo)
        usuario = usecase.executar(dados)

        dto = UsuarioResponseDTO.from_usuario(usuario)
        return jsonify({
            'sucesso': True,
            'mensagem': 'Aluno cadastrado com sucesso',
            'usuario': dto.to_dict()
        }), 201

    except UsuarioJaExisteException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 409
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e), 'detalhes': e.detalhes}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao cadastrar aluno'}), 500

@bp.route('/motoristas/cadastrar', methods=['POST'])
def cadastrar_motorista():
    try:
        dados = request.get_json() or request.form.to_dict()
        dados['tipo_perfil'] = 'motorista'

        repo = UsuarioRepository(current_app.db)
        usecase = CadastrarUsuario(repo)
        usuario = usecase.executar(dados)

        dto = UsuarioResponseDTO.from_usuario(usuario)
        return jsonify({
            'sucesso': True,
            'mensagem': 'Motorista cadastrado com sucesso',
            'usuario': dto.to_dict()
        }), 201

    except UsuarioJaExisteException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 409
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e), 'detalhes': e.detalhes}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao cadastrar motorista'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json() or request.form.to_dict()

        email = dados.get('email', '').strip()
        senha = dados.get('senha', '')
        perfil = dados.get('perfil', 'aluno').strip()

        repo = UsuarioRepository(current_app.db)
        usecase = AutenticarUsuario(repo)
        usuario_dict, token = usecase.executar(email, senha, perfil)

        usuario_dto = UsuarioResponseDTO(**usuario_dict)
        response_dto = LoginResponseDTO(usuario=usuario_dto, token=token)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Login realizado com sucesso',
            'dados': response_dto.to_dict()
        }), 200

    except EmailNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except SenhaInvalidaException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 401
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except ErroGeracaoTokenException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao fazer login'}), 500

@bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    try:
        dados = request.get_json() or request.form.to_dict()
        email = dados.get('email', '').strip()

        repo = UsuarioRepository(current_app.db)
        usecase = RecuperarSenha(repo)
        resultado = usecase.executar(email)

        return jsonify({
            'sucesso': True,
            'mensagem': resultado['mensagem']
        }), 200

    except EmailNaoEncontradoException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 404
    except DadosInvalidosException as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': 'Erro ao recuperar senha'}), 500
