import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def get_firestore_client():
    return firestore.client()
