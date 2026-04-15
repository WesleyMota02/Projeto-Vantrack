import os
import jwt
from functools import wraps
from flask import request, jsonify
from exceptions import ErroAutenticacaoException

class AutenticacaoMiddleware:

    def __init__(self, jwt_secret: str = None):
        self.jwt_secret = jwt_secret or os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-prod')

    def requer_token(self, f):
        @wraps(f)
        def decorador(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                auth_header = request.headers.get('Authorization')
                try:
                    partes = auth_header.split(" ")
                    if len(partes) != 2 or partes[0].lower() != 'bearer':
                        return jsonify({'sucesso': False, 'erro': 'Formato de autorização inválido'}), 401
                    token = partes[1]
                except (IndexError, AttributeError):
                    return jsonify({'sucesso': False, 'erro': 'Formato de token inválido'}), 401

            if not token:
                return jsonify({'sucesso': False, 'erro': 'Token não fornecido'}), 401

            try:
                payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
                request.usuario_id = payload.get('usuario_id')
                request.email = payload.get('email')
                request.tipo_perfil = payload.get('tipo_perfil')
            except jwt.ExpiredSignatureError:
                return jsonify({'sucesso': False, 'erro': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'sucesso': False, 'erro': 'Token inválido'}), 401
            except Exception as e:
                return jsonify({'sucesso': False, 'erro': 'Erro ao validar token'}), 401

            return f(*args, **kwargs)

        return decorador

    def requer_perfil(self, *perfis_permitidos):
        def decorator(f):
            @wraps(f)
            def decorador(*args, **kwargs):
                if not hasattr(request, 'tipo_perfil'):
                    return jsonify({'sucesso': False, 'erro': 'Token não verificado'}), 401

                if request.tipo_perfil not in perfis_permitidos:
                    return jsonify({
                        'sucesso': False, 
                        'erro': f'Acesso negado. Perfis permitidos: {", ".join(perfis_permitidos)}'
                    }), 403

                return f(*args, **kwargs)

            return decorador
        return decorator
