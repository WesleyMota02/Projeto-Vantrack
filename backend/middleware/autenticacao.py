import jwt
import os
from functools import wraps
from flask import request, jsonify
from exceptions import TokenInvalido, PermissaoNegada

def requer_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'erro': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'erro': 'Token não fornecido'}), 401
        
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET', 'seu-secreto-jwt-super-seguro'), algorithms=['HS256'])
            request.usuario_id = payload['usuario_id']
            request.tipo_perfil = payload['tipo_perfil']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorator

def requer_perfil(*perfis_permitidos):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.tipo_perfil not in perfis_permitidos:
                return jsonify({'erro': 'Acesso negado'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
