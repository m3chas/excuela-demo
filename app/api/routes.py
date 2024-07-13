from flask import Flask
from app.interface.controllers.user_controller import user_bp

def register_routes(app: Flask):
    app.register_blueprint(user_bp, url_prefix='/api')
