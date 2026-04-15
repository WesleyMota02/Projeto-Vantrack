import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def criar_app():
    app = Flask(__name__)

    from config import config
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    CORS(app)

    from database import Database
    db = Database(app.config['DATABASE_URL'])
    app.db = db

    from presentation.routes import auth_routes, usuario_routes, veiculo_routes, rota_routes, inscricao_routes, gps_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(veiculo_routes.bp)
    app.register_blueprint(rota_routes.bp)
    app.register_blueprint(inscricao_routes.bp)
    app.register_blueprint(gps_routes.bp)

    @app.errorhandler(404)
    def nao_encontrado(e):
        return {'erro': 'Rota não encontrada'}, 404

    @app.errorhandler(500)
    def erro_interno(e):
        return {'erro': 'Erro interno do servidor'}, 500

    return app

if __name__ == '__main__':
    app = criar_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
