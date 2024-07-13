from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from .config.config import config
from .infrastructure.firebase_client import initialize_firebase
from .api.routes import register_routes

def create_app(config_name='default'):
    """Crear e inicializar una instancia de la aplicación Flask."""
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    initialize_firebase()

    # Inicializar JWT
    jwt = JWTManager(app)

    # Registrar blueprints
    register_routes(app)
    
    return app
