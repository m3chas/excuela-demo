from app.infrastructure.auth.firebase_auth_client import FirebaseAuthClient

class AuthService:
    @staticmethod
    def login_with_firebase(email, password):
        return FirebaseAuthClient.login_with_firebase(email, password)
