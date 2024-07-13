# Excuela API

Este proyecto es una API RESTful desarrollada con Flask que permite la gestión de usuarios y la autenticación mediante JSON Web Tokens (JWT).

## Requisitos

- Docker
- Docker Compose

## Configuración y Ejecución

1. Clonar el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd excuela
    ```

2. Construir y ejecutar los contenedores con Docker Compose:
    ```sh
    docker-compose up --build
    ```

3. La aplicación estará disponible en `http://localhost:5000`.

## Implementación de Datos con Firestore y Autenticación con Firebase Auth

### Configuración de Firestore

La base de datos utilizada en este proyecto es Firestore, un servicio de base de datos en la nube de Firebase. Los datos de los usuarios se almacenan en una colección llamada `users`.

### Configuración de Firebase Auth

Firebase Auth se utiliza para manejar la autenticación de usuarios. Los usuarios pueden registrarse y autenticarse mediante esta API, y sus datos se almacenan tanto en Firebase Auth como en Firestore.

#### Registro de Usuarios

Durante el registro, se crea un nuevo usuario en Firebase Auth y se almacena un documento en Firestore con la información del usuario. Aquí tienes un ejemplo de cómo se maneja en el servicio:

```python
from firebase_admin import auth
from ..infrastructure.firebase_client import init_firebase
from ..domain.entities.user import User
from werkzeug.security import generate_password_hash
from ..infrastructure.repositories.user_repository import UserRepository

db = init_firebase()

class UserService:

    @staticmethod
    def register_user(username, password, email):
        # Validar que el username y email sean únicos
        if UserRepository.get_user_by_username(username):
            raise ValueError("Username already exists")
        
        if UserRepository.get_user_by_email(email):
            raise ValueError("Email already exists")
        
        # Crear nuevo usuario en Firebase Auth
        user_record = auth.create_user(email=email, password=password)
        
        # Crear nuevo usuario en Firestore
        password_hash = generate_password_hash(password)
        new_user = User(id=user_record.uid, username=username, password_hash=password_hash, email=email)
        db.collection('users').document(user_record.uid).set(new_user.__dict__)
        return {'message': 'User registered successfully'}
```

#### Inicio de Sesión y Obtención de Tokens

Al iniciar sesión, se valida el usuario con Firebase Auth y se genera un JSON Web Token (JWT) para la sesión del usuario. El token se obtiene utilizando la REST API de Firebase Auth. Aquí tienes un ejemplo de cómo se maneja en el servicio:

```python
from firebase_admin import auth
from ..infrastructure.firebase_client import init_firebase
from flask_jwt_extended import create_access_token

db = init_firebase()

class UserService:

    @staticmethod
    def authenticate_user(data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = auth.get_user_by_email(email)
            if user:
                # Aquí deberías validar la contraseña utilizando un servicio de validación de Firebase
                token = create_access_token(identity=user.uid)
                return {'access_token': token}
        except auth.AuthError:
            return None
```

### Ejemplo de Configuración

Para utilizar Firebase Auth y Firestore, necesitas configurar las credenciales de Firebase en tu proyecto. Crea un archivo firebase_credentials.json y coloca tus credenciales de Firebase en él. Asegúrate de actualizar tu archivo .env para incluir la ruta a tus credenciales:

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=<TU_SECRET_KEY>
FIREBASE_APPLICATION_CREDENTIALS=firebase_credentials.json

```

## Documentación de la API

### Rutas de Usuario

#### Registro de Usuario

- **Ruta:** `/register`
- **Método:** `POST`
- **Descripción:** Registra un nuevo usuario.
- **Datos de entrada:**
    ```json
    {
        "username": "exampleuser",
        "password": "examplepassword",
        "email": "user@example.com"
    }
    ```
- **Respuesta exitosa:**
    ```json
    {
        "message": "User registered successfully"
    }
    ```
- **Errores posibles:**
    - `400 Bad Request` si el `username` o `email` ya existen.

#### Login de Usuario

- **Ruta:** `/login`
- **Método:** `POST`
- **Descripción:** Autentica a un usuario.
- **Datos de entrada:**
    ```json
    {
        "username": "exampleuser",
        "password": "examplepassword"
    }
    ```
- **Respuesta exitosa:**
    ```json
    {
        "access_token": "<JWT_TOKEN>"
    }
    ```
- **Errores posibles:**
    - `401 Unauthorized` si las credenciales son inválidas.

#### Obtener Información del Usuario

- **Ruta:** `/user`
- **Método:** `GET`
- **Descripción:** Obtiene la información del usuario autenticado.
- **Requiere autenticación:** Sí
- **Respuesta exitosa:**
    ```json
    {
        "id": "user_id",
        "username": "exampleuser",
        "email": "user@example.com",
        "created_at": "2023-07-13T12:34:56"
    }
    ```

#### Actualizar Información del Usuario

- **Ruta:** `/user`
- **Método:** `PUT`
- **Descripción:** Actualiza la información del usuario autenticado.
- **Requiere autenticación:** Sí
- **Datos de entrada:**
    ```json
    {
        "username": "newusername",
        "email": "newemail@example.com"
    }
    ```
- **Respuesta exitosa:**
    ```json
    {
        "message": "User updated successfully"
    }
    ```

#### Eliminar Usuario

- **Ruta:** `/user`
- **Método:** `DELETE`
- **Descripción:** Elimina la cuenta del usuario autenticado.
- **Requiere autenticación:** Sí
- **Respuesta exitosa:**
    ```json
    {
        "message": "User deleted successfully"
    }
    ```

## Pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando:
```sh
docker-compose run -e FLASK_ENV=testing web pytest
```

## Clean Arquitecture

El codigo ha sido organizado utilizando el patron de diseño Clean Arquitecture de esta manera:

```sh
app/
├── api/
├── config/
├── domain/
│   ├── entities/
│   └── services/
├── infrastructure/
│   ├── repository/
│   └── firebase_client.py
├── interface/
│   ├── controllers/
│   ├── decorators/
│   ├── tests/
│   └── auth.py
├── __init__.py
.env
.env.testing
conftest.py
```

