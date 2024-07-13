import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'excuela-test-key')
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH')
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY', 'excuela-test-key')
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIREBASE_CREDENTIALS_PATH = 'testing'
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

config = {
    'default': Config,
    'testing': TestingConfig
}