from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                # Remover el prefijo 'Bearer' si está presente
                token = token.split(' ')[1] if ' ' in token else token
                decoded_token = auth.verify_id_token(token)
                request.user = decoded_token
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': str(e)}), 401
        else:
            return jsonify({'error': 'Authorization token is missing'}), 401
    return decorated_function
