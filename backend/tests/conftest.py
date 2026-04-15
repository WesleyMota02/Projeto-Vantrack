import pytest
import os
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_db():
    """Mock database connection"""
    db = Mock()
    db.execute_query = Mock(return_value=[])
    db.execute_single = Mock(return_value=None)
    db.execute_insert = Mock(return_value={})
    db.execute_update = Mock(return_value=0)
    db.execute_delete = Mock(return_value=0)
    return db

@pytest.fixture
def app_context():
    """Flask app context for testing"""
    from app import criar_app
    os.environ['FLASK_ENV'] = 'testing'
    app = criar_app()
    with app.app_context():
        yield app

@pytest.fixture
def client(app_context):
    """Flask test client"""
    return app_context.test_client()

@pytest.fixture
def valid_user_data():
    """Valid user registration data"""
    return {
        'nome': 'João',
        'sobrenome': 'Silva',
        'cpf': '11144477735',
        'email': 'joao@test.com',
        'telefone': '11987654321',
        'cidade': 'São Paulo',
        'senha': 'Senha123',
        'tipo_perfil': 'aluno'
    }

@pytest.fixture
def valid_vehicle_data():
    """Valid vehicle data"""
    return {
        'placa': 'ABC1234',
        'modelo': 'Mercedes Sprinter',
        'ano': 2022,
        'capacidade': 50
    }

@pytest.fixture
def valid_route_data():
    """Valid route data"""
    return {
        'nome': 'Rota Centro-Norte',
        'origem': 'Escola Centro',
        'destino': 'Bairro Norte',
        'horario_partida': '07:30',
        'capacidade_maxima': 50
    }

@pytest.fixture
def valid_gps_data():
    """Valid GPS data"""
    return {
        'latitude': -23.5505,
        'longitude': -46.6333
    }

@pytest.fixture
def jwt_token():
    """Sample JWT token for testing"""
    import jwt
    from datetime import datetime, timedelta
    
    payload = {
        'usuario_id': '550e8400-e29b-41d4-a716-446655440000',
        'email': 'test@example.com',
        'tipo_perfil': 'aluno',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    
    return jwt.encode(payload, 'jwt-secret-key-change-in-prod', algorithm='HS256')

@pytest.fixture
def motorista_token():
    """Sample JWT token for motorista"""
    import jwt
    from datetime import datetime, timedelta
    
    payload = {
        'usuario_id': '550e8400-e29b-41d4-a716-446655440001',
        'email': 'motorista@example.com',
        'tipo_perfil': 'motorista',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    
    return jwt.encode(payload, 'jwt-secret-key-change-in-prod', algorithm='HS256')
