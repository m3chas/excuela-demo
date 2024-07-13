import requests
import json
from app.config.config import Config

class FirebaseAuthClient:
    @staticmethod
    def login_with_firebase(email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={Config.FIREBASE_API_KEY}"
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            id_token = response.json().get('idToken')
            return id_token
        else:
            response.raise_for_status()
