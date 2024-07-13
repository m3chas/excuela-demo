import pytest
from app import create_app
from unittest.mock import patch, MagicMock
from datetime import datetime
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Mock de la inicialización de Firebase y Firestore
@pytest.fixture(scope='session', autouse=True)
def mock_firebase():
    with patch('firebase_admin.initialize_app') as mock_initialize_app:
        mock_initialize_app.return_value = None
        with patch('firebase_admin.firestore.client') as mock_firestore_client:
            mock_firestore = MagicMock()
            mock_firestore_client.return_value = mock_firestore

            # Mock del cliente Firestore
            mock_firestore.collection.return_value.add.return_value = (MagicMock(), MagicMock())
            yield mock_initialize_app, mock_firestore_client

# Mock del cliente Firestore para cada prueba
@pytest.fixture(autouse=True)
def mock_firestore_client(mock_firebase):
    _, mock_firestore_client = mock_firebase

    # Configurar el mock para que devuelva el usuario esperado
    mock_user = MagicMock()
    mock_user.id = '1'
    mock_user.to_dict.return_value = {
        'username': 'testuser',
        'password_hash': generate_password_hash('password123'),
        'email': 'test@example.com',
        'created_at': 'mocked_created_at'
    }

    mock_firestore_client.collection.return_value.where.return_value.stream.return_value = [mock_user]

    with patch('app.infrastructure.firebase_client.get_firestore_client', return_value=mock_firestore_client):
        yield mock_firestore_client
