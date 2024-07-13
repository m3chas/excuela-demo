import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

def test_login_user(client, mock_firestore_client):
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })

