import os
import jwt
from functools import wraps
from flask import request, jsonify
from exceptions import ErroAutenticacaoException

class TokenMiddleware:

    def __init__(self, jwt_secret: str):
        self.jwt_secret = jwt_secret

    def verificar_token(self, f):
        @wraps(f)
        def decorador(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                auth_header = request.headers.get('Authorization')
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'erro': 'Formato de token inválido'}), 401

            if not token:
                return jsonify({'erro': 'Token não fornecido'}), 401

            try:
                payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
                request.usuario_id = payload.get('usuario_id')
                request.email = payload.get('email')
                request.tipo_perfil = payload.get('tipo_perfil')
            except jwt.ExpiredSignatureError:
                return jsonify({'erro': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'erro': 'Token inválido'}), 401

            return f(*args, **kwargs)

        return decorador
