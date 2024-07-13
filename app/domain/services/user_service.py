from firebase_admin import auth
import datetime
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from app.infrastructure.repository.user_repository import UserRepository
from app.domain.entities.user import User 
from app.config.config import Config
from app.domain.services.auth_service import AuthService
from firebase_admin._auth_utils import EmailAlreadyExistsError

class UserService:
    
    @staticmethod
    def register_user(username, password, email):
        # Validar que el username y email sean únicos
        if UserRepository.get_user_by_username(username):
            raise ValueError("Username already exists")
        
        if UserRepository.get_user_by_email(email):
            raise ValueError("Email already exists")

        # Creamos el usuario en Firebase Auth
        try:
            user_record = auth.create_user(email=email,password=password)
        except EmailAlreadyExistsError:
            raise ValueError("Email already exists in Firebase")

        # Creamos el usuario en Firestore, usando el UID de Firebase como ID
        # password_hash es solo para propositos de demostracion de como
        # almacenar datos y contraseñas de manera segura en firestore.
        password_hash = generate_password_hash(password)
        user = User(id=user_record.uid, username=username, password_hash=password_hash, email=email)
        UserRepository.add_user(user)
        
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        user_data = UserRepository.get_user_by_username(username)
        if not user_data:
            raise ValueError("Invalid username or password")
        
        email = user_data['email']
        try:
            id_token = AuthService.login_with_firebase(email, password)
            return {'user_data': user_data, 'id_token': id_token}
        except requests.exceptions.HTTPError as e:
            raise ValueError("Invalid username or password") from e

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id, username, email):
        UserRepository.update_user(user_id, username, email)
    
    @staticmethod
    def delete_user(user_id):
        # Eliminar usuario de Firebase Authentication
        try:
            auth.delete_user(user_id)
        except auth.AuthError as e:
            raise ValueError("Error deleting user from Firebase Authentication: " + str(e))
        
        UserRepository.delete_user(user_id)
