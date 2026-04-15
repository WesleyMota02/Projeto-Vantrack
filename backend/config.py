import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-prod')
    JWT_EXPIRY = int(os.getenv('JWT_EXPIRY', 86400))

    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/vantrack')
    BCRYPT_LOG_ROUNDS = 12

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql://user:password@localhost:5432/vantrack_test'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
