from app.infrastructure.firebase_client import get_firestore_client

class UserRepository:
    
    @staticmethod
    def add_user(user):
        db = get_firestore_client()
        users_ref = db.collection('users')
        users_ref.document(user.id).set({
            'username': user.username,
            'password_hash': user.password_hash,
            'email': user.email,
            'created_at': user.created_at
        })
    
    @staticmethod
    def get_user_by_username(username):
        db = get_firestore_client()
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).stream()
        for doc in query:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            print(f"User found: {user_data}")
            return user_data
        print(f"No user found with username: {username}")
        return None
    
    @staticmethod
    def get_user_by_email(email):
        db = get_firestore_client()
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()
        for doc in query:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        db = get_firestore_client()
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        return None

    @staticmethod
    def update_user(user_id, username, email):
        db = get_firestore_client()
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'username': username,
            'email': email
        })
    
    @staticmethod
    def delete_user(user_id):
        db = get_firestore_client()
        user_ref = db.collection('users').document(user_id)
        user_ref.delete()
