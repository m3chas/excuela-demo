from flask import request, jsonify, Blueprint
from app.domain.services.user_service import UserService
from firebase_admin import auth
from app.interface.decorators.auth_decorator import firebase_auth_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    try:
        user = UserService.register_user(username, password, email)
        return jsonify({
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        result = UserService.authenticate_user(username, password)
        token = result['id_token']
        return jsonify({'token': token}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/user', methods=['GET'])
@firebase_auth_required
def get_user_info():
    current_user_id = request.user['uid']
    user_data = UserService.get_user_by_id(current_user_id)
    if user_data:
        return jsonify({
            'id': user_data['id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'created_at': user_data['created_at']
        }), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user', methods=['PUT'])
@firebase_auth_required
def update_user_info():
    current_user_id = request.user['uid']
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    try:
        UserService.update_user(current_user_id, username, email)
        return jsonify({'message': 'User updated successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/user', methods=['DELETE'])
@firebase_auth_required
def delete_user():
    current_user_id = request.user['uid']
    
    try:
        UserService.delete_user(current_user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
